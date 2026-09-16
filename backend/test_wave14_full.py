"""
🌊 WAVE 14 TEST SUITE — PERFECT MATCH + ADMIN SUPREME
=====================================================
  A. age-rule pure (1-day-older block, same-day OK, 0–12mo first, fallback, unknown)
  B. profession pure (job_group + affinity + rerank order, score math intact)
  C. NRI pure (detect_nri country/location/india)
  D. religion→caste pure (43 Hindu A–Z + Muslim/Christian + alias + fallback)
  E. age API (interest block + credit intact + top-matches skip/flag + score + match-send)
  F. profession API (same-group first ordering + scores unchanged + labels)
  G. NRI API (register country + search nri_only + profile fields + top-matches nri_only)
  H. safe-pay manual (config + order + offer + UTR confirm + idempotent + guards)
  I. safe-pay razorpay (HMAC ok/tamper/replay — env keys)
  J. offers admin (seed/create/duplicate/toggle/expiry)
  K. ads update (dates/districts/days + guards)
  L. bot matches (top-3 text, masked, skips)
  M. meta endpoints (religions + castes)
  N. regression guards (surname/gothram fields intact, score math untouched)

Run:  WA_TEST_FAST=1 python3 test_wave14_full.py   (backend/ nunchi)
"""
import hashlib
import hmac
import os
import re
import sys

os.environ.setdefault("WA_TEST_FAST", "1")
os.environ.setdefault("OTP_DEV_MODE", "true")
os.environ.setdefault("WA_LONG_PAUSE_CHANCE", "0")
os.environ.setdefault("WHATSAPP_MODE", "off")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS, FAIL, FAILED = 0, 0, []
PHONE_RE = re.compile(r"(?<![\d•])[6-9]\d{9}(?!\d)")


def section(t):
    print(f"\n=== {t} ===")


def check(name, cond, extra=None):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        FAILED.append(name)
        print(f"  ❌ {name} :: {str(extra)[:220]}")


from fastapi.testclient import TestClient
import hardening as H
import main
import matchpro as MP
import paypro as PP
import ads as ADS
import topmatch

client = TestClient(main.app, raise_server_exceptions=False)
HDR_ADMIN = {"X-Admin-Key": H.ADMIN_KEY}

# clean pay stores (deterministic counts)
PP.PAY_ORDERS.clear(); PP.OFFERS.clear(); PP.RECEIPTS.clear(); PP._SEQ = 0
try:
    os.remove(PP.PERSIST_FILE)
except OSError:
    pass

# ═══════════════════════════════════════════════════════════════════════════
section("A. AGE-RULE PURE (DOB-date accurate)")
# ═══════════════════════════════════════════════════════════════════════════
G = {"gender": "Groom", "dob": "1998-05-10", "age": 27}
B_OLDER1 = {"gender": "Bride", "dob": "1998-05-09", "age": 27}   # 1 day peddadi
B_SAME = {"gender": "Bride", "dob": "1998-05-10", "age": 27}     # same date
B_YOUNG6 = {"gender": "Bride", "dob": "1998-11-10", "age": 27}   # 6mo younger
B_YOUNG2Y = {"gender": "Bride", "dob": "2000-05-10", "age": 25}  # 2y younger

r = MP.age_rule_check(B_OLDER1, G)
check("A1 1-day-older bride BLOCK", r["blocked"] is True and r["reason"] == "bride_older"
      and r["gap_days"] == -1 and r["via"] == "dob", r)
check("A2 verdict telugu 🚫+roju", "🚫" in r["verdict_telugu"] and "roju" in r["verdict_telugu"])
r = MP.age_rule_check(G, B_OLDER1)   # direction flip
check("A3 direction-independent block", r["blocked"] is True and r["reason"] == "bride_older")
r = MP.age_rule_check(B_SAME, G)
check("A4 same-day OK", r["blocked"] is False and r["gap_days"] == 0, r)
check("A5 0-12mo tier FIRST",
      MP.age_priority_key(G, B_YOUNG6) < MP.age_priority_key(G, B_YOUNG2Y)
      and MP.age_priority_key(G, B_YOUNG6)[0] == 0,
      (MP.age_priority_key(G, B_YOUNG6), MP.age_priority_key(G, B_YOUNG2Y)))
check("A6 blocked tier last (9,..)", MP.age_priority_key(G, B_OLDER1)[0] == 9)
r = MP.age_rule_check({"gender": "Bride", "age": 29}, {"gender": "Groom", "age": 27})
check("A7 age-fallback bride older BLOCK", r["blocked"] is True and r["via"] == "age_years", r)
r = MP.age_rule_check({"gender": "Bride", "age": 27}, {"gender": "Groom", "age": 27})
check("A8 age-fallback equal ALLOW", r["blocked"] is False and r["reason"] == "age_ok", r)
r = MP.age_rule_check({"gender": "Bride"}, {"gender": "Groom"})
check("A9 unknown → no block + rank-low note",
      r["blocked"] is False and r["via"] == "unknown" and "rank" in r["verdict_telugu"], r)
r = MP.age_rule_check(G, dict(G))
check("A10 same-gender N/A", r["applicable"] is False and r["blocked"] is False, r)
f = MP.filter_age_ok(dict(G, tsap_id="M"),
                     [dict(B_OLDER1, tsap_id="X1"), dict(B_YOUNG6, tsap_id="X2"),
                      dict(B_SAME, tsap_id="X3")])
check("A11 filter: 1 skip + 2 kept", f["skipped_ids"] == ["X1"] and len(f["kept"]) == 2, f)

# ═══════════════════════════════════════════════════════════════════════════
section("B. PROFESSION PURE")
# ═══════════════════════════════════════════════════════════════════════════
check("B1 doctor group", MP.job_group({"job": "Doctor at Apollo"}) == "doctor")
check("B2 software group", MP.job_group({"job": "Software Engineer", "company": "TCS"}) == "software")
check("B3 govt group", MP.job_group({"job": "Group-2 Officer", "company": "Govt of TS"}) == "govt")
check("B4 teacher group", MP.job_group({"job": "School Teacher"}) == "teacher")
check("B5 unknown → other", MP.job_group({"job": "xyz abc"}) == "other")
a = MP.profession_affinity({"job": "Doctor"}, {"job": "MBBS Surgeon"})
check("B6 doctor×doctor same+boost", a["same_group"] is True and a["boost"] == 12 and "💼" in a["reason_telugu"], a)
a = MP.profession_affinity({"job": "Doctor"}, {"job": "Software Engineer"})
check("B7 diff group no boost", a["same_group"] is False and a["boost"] == 4, a)
me = {"job": "Doctor"}
rows = [{"tsap_id": "S1", "score": 95, "profile": {"job": "Software Engineer"}, "reasons": ["x"]},
        {"tsap_id": "D1", "score": 70, "profile": {"job": "Doctor"}, "reasons": []},
        {"tsap_id": "D2", "score": 88, "profile": {"job": "MBBS"}, "reasons": []}]
rr = MP.rerank_profession(me, rows)
check("B8 rerank: doctors first, score-order within",
      [x["tsap_id"] for x in rr] == ["D2", "D1", "S1"], [x["tsap_id"] for x in rr])
check("B9 score math UNTOUCHED", {x["tsap_id"]: x["score"] for x in rr} == {"S1": 95, "D1": 70, "D2": 88})
check("B10 reason prepended", rr[0]["reasons"] and "💼" in rr[0]["reasons"][0], rr[0]["reasons"][:1])
check("B11 profession dict shape",
      rr[0]["profession"] == {"group": "doctor", "group_telugu": "🩺 Doctor/Medical", "same_group": True},
      rr[0]["profession"])

# ═══════════════════════════════════════════════════════════════════════════
section("C. NRI PURE")
# ═══════════════════════════════════════════════════════════════════════════
check("C1 USA → NRI", MP.detect_nri("USA", "", "")["is_nri"] is True)
check("C2 India → local", MP.detect_nri("India", "", "") == {"is_nri": False, "country": "India", "via": "india"})
check("C3 empty → local India", MP.detect_nri("", "", "")["is_nri"] is False)
check("C4 Dallas location → NRI", MP.detect_nri("", "Dallas, USA", "")["is_nri"] is True)
check("C5 Hyderabad → local", MP.detect_nri("India", "Hyderabad", "Hyderabad")["is_nri"] is False)
check("C6 Dubai → NRI", MP.detect_nri("UAE", "Dubai", "")["is_nri"] is True)

# ═══════════════════════════════════════════════════════════════════════════
section("D. RELIGION→CASTE PURE")
# ═══════════════════════════════════════════════════════════════════════════
check("D1 7 religions", MP.RELIGIONS == ["Hindu", "Muslim", "Christian", "Sikh", "Jain", "Buddhist", "Other"])
h = MP.castes_for("Hindu")
check("D2 Hindu 43", len(h["castes"]) == 43, len(h["castes"]))
check("D3 Hindu A–Z sorted", h["castes"] == sorted(h["castes"]) and h["castes"][0] == "Adi Andhra", h["castes"][:3])
m = MP.castes_for("Muslim")
check("D4 Muslim groups A–Z", "Syed" in m["castes"] and m["castes"] == sorted(m["castes"]), m["castes"][:3])
c = MP.castes_for("Christian")
check("D5 Christian groups", "CSI" in c["castes"] and len(c["castes"]) >= 8, c["castes"])
check("D6 alias Islam→Muslim", MP.castes_for("Islam")["religion"] == "Muslim")
check("D7 unknown → Hindu fallback", MP.castes_for("Zoro")["religion"] == "Zoro" and len(MP.castes_for("Zoro")["castes"]) == 43)

# ═══════════════════════════════════════════════════════════════════════════
section("E–G. API REGISTERS (age + profession + NRI)")
# ═══════════════════════════════════════════════════════════════════════════
client.post("/api/demo/seed")
BASE = {"height": "5'6\"", "marital_status": "Pelli Kaledu", "education": "BTech",
        "salary": "60k", "state": "TS", "district": "Hyderabad", "religion": "Hindu"}
GG = dict(BASE, gender="Groom", age="27", dob="1998-05-10", phone="9948011111",
          full_name="Wave Fourteen Groom Alpuri", job="Doctor", caste="Reddy", gothram="GTA")
BB1 = dict(BASE, gender="Bride", age="27", dob="1998-05-09", phone="9948022222",
           full_name="Wave Fourteen Bride Bokka", job="Teacher", caste="Kamma", gothram="GTB")
BB2 = dict(BASE, gender="Bride", age="26", dob="2000-06-01", phone="9948033333",
           full_name="Wave Fourteen Bride Chillara", job="Doctor at Apollo", caste="Kapu", gothram="GTC")
BB3 = dict(BASE, gender="Bride", age="27", dob="1999-03-03", phone="9948044444",
           full_name="Wave Fourteen Bride Domala", job="Software Engineer", caste="Velama", gothram="GTD")
BNRI = dict(BASE, gender="Bride", age="25", dob="2001-01-01", phone="9948055555",
            full_name="Wave Fourteen Bride Endla", job="Nurse", caste="Reddy", gothram="GTE",
            state="AP", district="Guntur", country="USA", work_location="New Jersey, USA")
g = client.post("/api/register", data=GG).json()
b1 = client.post("/api/register", data=BB1).json()
b2 = client.post("/api/register", data=BB2).json()
b3 = client.post("/api/register", data=BB3).json()
bn = client.post("/api/register", data=BNRI).json()
GID, B1, B2, B3, NRI = (x.get("tsap_id", "") for x in (g, b1, b2, b3, bn))
check("E0 5 register", all([GID, B1, B2, B3, NRI]), (GID, B1, B2, B3, NRI))
for _u in main.DB_USERS:
    if _u.get("tsap_id") in (GID, B1, B2, B3, NRI):
        _u["is_approved"] = True

ib = client.post("/api/interest/send", json={"from_id": GID, "to_id": B1})
check("E1 1-day-older interest BLOCK age_rule",
      ib.status_code == 400 and ib.json().get("reason") == "age_rule",
      (ib.status_code, str(ib.json())[:150]))
cr = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("E2 block ayina credit intact", cr >= 3, cr)
io = client.post("/api/interest/send", json={"from_id": GID, "to_id": B2})
check("E3 younger-bride interest OK", io.status_code == 200 and io.json().get("success") is True,
      (io.status_code, str(io.json())[:150]))
tm = client.get(f"/api/top-matches/{GID}?limit=30&min_score=0").json()
ids = [r.get("tsap_id") for r in tm.get("results", [])]
check("E4 age_skipped field + B1 skipped",
      "age_skipped" in tm and B1 not in ids and B1 in tm.get("age_skipped_ids", []),
      (tm.get("age_skipped"), tm.get("age_skipped_ids", [])[:5]))
check("E5 B2 kanipisthundi", B2 in ids)
tm2 = client.get(f"/api/top-matches/{GID}?limit=30&min_score=0&include_age_block=1").json()
check("E6 include_age_block=1 tho B1 kanipisthundi",
      B1 in [r.get("tsap_id") for r in tm2.get("results", [])])
sc = client.get(f"/api/match/score?a={GID}&b={B1}").json()
check("E7 score age verdict blocked", sc.get("age_rule", {}).get("blocked") is True
      and sc.get("age_rule", {}).get("gap_days") == -1, sc.get("age_rule"))
sc2 = client.get(f"/api/match/score?a={GID}&b={B2}").json()
check("E8 score age verdict ok", sc2.get("age_rule", {}).get("blocked") is False
      and sc2.get("age_rule", {}).get("via") == "dob", sc2.get("age_rule"))
ms = client.get(f"/api/admin/match-send/{GID}?limit=30&min_score=0", headers=HDR_ADMIN).json()
check("E9 match-send age_skipped", "age_skipped" in ms and ms.get("age_skipped", 0) >= 1
      and B1 not in [r.get("tsap_id") for r in ms.get("results", [])],
      (ms.get("age_skipped"), ms.get("age_skipped_ids", [])[:5]))

# F. profession-first ordering property: same-group anni mundu, scores intact
res = tm.get("results", [])
groups = [(r.get("profession") or {}).get("same_group", False) for r in res]
check("F1 same-group block first (ordering)",
      groups == sorted(groups, reverse=True) and any(groups), groups[:12])
check("F2 B2 (doctor) B3 (software) kanna mundu", ids.index(B2) < ids.index(B3) if B2 in ids and B3 in ids else False,
      ([i for i in ids if i in (B2, B3)], [(r.get("tsap_id"), r.get("score")) for r in res if r.get("tsap_id") in (B2, B3)]))
direct = {r["tsap_id"]: r["score"] for r in
          topmatch.find_top_matches_v2(next(u for u in main.DB_USERS if u["tsap_id"] == GID),
                                       [u for u in main.DB_USERS if u.get("tsap_id") in ids], limit=100, min_score=0)}
check("F3 API scores == engine scores (math intact)",
      all(r.get("score") == direct.get(r.get("tsap_id")) for r in res), "mismatch!")
check("F4 profession_label + is_nri fields",
      all("profession_label" in r and "is_nri" in r for r in res))
sr = client.get(f"/api/search?viewer_id={GID}&profession_first=true&limit=30").json().get("results", [])
same_flags = [bool((r.get("profession") or {}).get("same_group")) or "💼" in " ".join(r.get("reasons", []) or [])
              for r in sr]
check("F5 search profession_first ordering", same_flags == sorted(same_flags, reverse=True), same_flags[:10])

# G. NRI API
nr = client.get("/api/search?nri_only=true&limit=100").json().get("results", [])
check("G1 nri_only contains NRI bride", NRI in [r.get("tsap_id") for r in nr],
      [r.get("tsap_id") for r in nr][:8])
check("G2 nri_only anni NRI", all(r.get("is_nri") for r in nr), len(nr))
pf = client.get(f"/api/search/{NRI}").json().get("profile", {})
check("G3 profile is_nri + country", pf.get("is_nri") is True and pf.get("country") == "USA", pf)
tmn = client.get(f"/api/top-matches/{GID}?limit=30&min_score=0&nri_only=1").json()
check("G4 top-matches nri_only", tmn.get("nri_only") is True and NRI in [r.get("tsap_id") for r in tmn.get("results", [])]
      and all(r.get("is_nri") for r in tmn.get("results", [])), tmn.get("count"))
check("G5 local profile is_nri False",
      client.get(f"/api/search/{B2}").json().get("profile", {}).get("is_nri") is False)

# ═══════════════════════════════════════════════════════════════════════════
section("H. SAFE-PAY MANUAL-UPI")
# ═══════════════════════════════════════════════════════════════════════════
cfg = client.get("/api/pay/config").json()
check("H1 config manual mode (no keys)", cfg.get("success") and cfg.get("mode") == "manual_upi"
      and "secret" not in str(cfg).lower().replace("razorpay secure", ""), cfg)
check("H2 config has plans + offers + upi", "plans" in cfg and "offers" in cfg and "upi_id" in cfg)
o1 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_99"}).json()
check("H3 order S_99 server amount", o1.get("success") and o1["pay_order"]["final_amount"] == 99
      and o1["pay_order"]["mode"] == "manual_upi", o1)
PO1 = o1["pay_order"]["id"]
bad = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "FREE"})
check("H4 FREE ref reject", bad.status_code == 400, bad.status_code)
bad2 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "lottery", "ref": "X"})
check("H5 bad purpose reject", bad2.status_code == 400, bad2.status_code)
bad3 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_99",
                                            "offer_code": "BOGUS99"})
check("H6 bad offer reject", bad3.status_code == 400, bad3.status_code)
seed = client.post("/api/admin/offers/seed", json={"valid_from": "2020-01-01", "valid_to": "2030-12-31"},
                   headers=HDR_ADMIN).json()
check("H7 festival seed 4", seed.get("success") and len(seed.get("added", [])) == 4, seed)
o2 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_199",
                                          "offer_code": "diwali25"}).json()
po2 = o2.get("pay_order", {})
check("H8 DIWALI25 25% off 199", o2.get("success") and po2.get("discount") == 49
      and po2.get("final_amount") == 150, po2)
PO2 = po2.get("id", "")
st = client.get(f"/api/pay/status/{PO1}").json()
check("H9 status created + no secrets", st.get("success") and st["order"]["status"] == "created"
      and "signature" not in st["order"] and "payment_id" not in st["order"], st)
cr0 = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
cf_noutr = client.post(f"/api/admin/payments/{PO1}/confirm", json={}, headers=HDR_ADMIN)
check("H10 UTR lekunda confirm NO", cf_noutr.status_code == 400, cf_noutr.status_code)
cf = client.post(f"/api/admin/payments/{PO1}/confirm", json={"utr": "411111111111"}, headers=HDR_ADMIN).json()
check("H11 UTR confirm fulfill", cf.get("success") and "success" in cf.get("message_telugu", ""), cf)
cr1 = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("H12 S_99 → +5 credits", cr1 - cr0 == 5, (cr0, cr1))
cf2 = client.post(f"/api/admin/payments/{PO1}/confirm", json={"utr": "411111111111"}, headers=HDR_ADMIN).json()
cr2 = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("H13 double-confirm idempotent", cf2.get("duplicate") is True and cr2 == cr1, (cf2, cr2))
vf = client.post("/api/pay/verify", json={"order_id": PO2, "razorpay_order_id": "o1",
                                           "razorpay_payment_id": "p1", "razorpay_signature": "s1"})
check("H14 manual mode lo online-verify honest-fail", vf.status_code == 400, vf.status_code)
al = client.get("/api/admin/payments", headers=HDR_ADMIN).json()
check("H15 admin payments list + stats", al.get("success") and al.get("count", 0) >= 2
      and al.get("stats", {}).get("paid", 0) >= 1, al.get("stats"))
_saved_fast = os.environ.pop("WA_TEST_FAST", None)   # enforcement ON (temp)
noauth = client.get("/api/admin/payments")
check("H16 admin key lekunda 403", noauth.status_code == 403, noauth.status_code)
noauth2 = client.get("/api/admin/payments", headers=HDR_ADMIN)
check("H17 admin key tho OK", noauth2.status_code == 200, noauth2.status_code)
if _saved_fast is not None:
    os.environ["WA_TEST_FAST"] = _saved_fast

# ═══════════════════════════════════════════════════════════════════════════
section("I. SAFE-PAY RAZORPAY (HMAC)")
# ═══════════════════════════════════════════════════════════════════════════
os.environ["RAZORPAY_KEY_ID"] = "rzp_test_w14key"
os.environ["RAZORPAY_KEY_SECRET"] = "w14_secret_abc123"
# 🌊 WAVE 25: server-side RZP order create — network stub (offline sandbox)
import paypro as _PP14
_PPx = _PP14._rzp_create_order
_PP14._rzp_create_order = lambda pid, amt, label: {"ok": True, "rzp_order_id": "rzp_o_w14",
                                                   "rzp_amount": int(amt) * 100}
cfg2 = client.get("/api/pay/config").json()
check("I1 keys unte razorpay mode + key_id only",
      cfg2.get("mode") == "razorpay" and cfg2.get("key_id") == "rzp_test_w14key"
      and "w14_secret" not in str(cfg2), cfg2)
o3 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_29"}).json()
po3 = o3.get("pay_order", {})
check("I2 razorpay order + paise + server order_id",
      po3.get("mode") == "razorpay" and po3.get("checkout_amount_paise") == 2900
      and po3.get("rzp_order_id") == "rzp_o_w14", po3)
PO3 = po3.get("id", "")


def _sig(order_id, pay_id):
    return hmac.new(b"w14_secret_abc123", f"{order_id}|{pay_id}".encode(), hashlib.sha256).hexdigest()


crb = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
v3 = client.post("/api/pay/verify", json={"order_id": PO3, "razorpay_order_id": "rzp_o_w14",
                                           "razorpay_payment_id": "pay_w14_ok1",
                                           "razorpay_signature": _sig("rzp_o_w14", "pay_w14_ok1")}).json()
cra = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("I3 valid HMAC → paid + receipt", v3.get("success") and v3.get("receipt", {}).get("payment_id") == "pay_w14_ok1"
      and cra - crb == 1, (v3, crb, cra))
v3b = client.post("/api/pay/verify", json={"order_id": PO3, "razorpay_order_id": "rzp_o_w14",
                                            "razorpay_payment_id": "pay_w14_ok1",
                                            "razorpay_signature": _sig("rzp_o_w14", "pay_w14_ok1")}).json()
crc = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("I4 replay → duplicate, credit same", v3b.get("duplicate") is True and crc == cra, (v3b, crc))
o4 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_29"}).json()
PO4 = o4["pay_order"]["id"]
v4 = client.post("/api/pay/verify", json={"order_id": PO4, "razorpay_order_id": "rzp_o_w14",
                                           "razorpay_payment_id": "pay_w14_bad",
                                           "razorpay_signature": "deadbeef" * 8})
check("I5 tampered signature FAIL", v4.status_code == 400, v4.status_code)
crd = next(u for u in main.DB_USERS if u["tsap_id"] == GID).get("credits", 0)
check("I6 fail ayina credit add kadu", crd == crc, (crc, crd))
st4 = client.get(f"/api/pay/status/{PO4}").json()
check("I7 failed order stays created", st4["order"]["status"] == "created", st4["order"]["status"])
_PP14._rzp_create_order = _PPx
os.environ.pop("RAZORPAY_KEY_ID", None)
os.environ.pop("RAZORPAY_KEY_SECRET", None)

# ═══════════════════════════════════════════════════════════════════════════
section("J. OFFERS ADMIN")
# ═══════════════════════════════════════════════════════════════════════════
co = client.post("/api/admin/offers", json={"code": "W14FLAT", "title": "Wave14 flat",
                                             "flat_off": 30, "applies_to": "credits",
                                             "valid_from": "2020-01-01", "valid_to": "2030-12-31",
                                             "max_uses": 5}, headers=HDR_ADMIN).json()
check("J1 create flat offer", co.get("success") and co["offer"]["code"] == "W14FLAT", co)
dup = client.post("/api/admin/offers", json={"code": "W14FLAT", "flat_off": 10}, headers=HDR_ADMIN)
check("J2 duplicate code reject", dup.status_code == 400, dup.status_code)
of = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_99",
                                          "offer_code": "W14FLAT"}).json()
check("J3 flat 30 off 99 → 69", of.get("success") and of["pay_order"]["final_amount"] == 69, of)
tg = client.post("/api/admin/offers/W14FLAT/toggle", headers=HDR_ADMIN).json()
check("J4 toggle OFF", tg.get("success") and tg["offer"]["active"] is False, tg)
of2 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_99",
                                           "offer_code": "W14FLAT"})
check("J5 OFF offer reject", of2.status_code == 400, of2.status_code)
client.post("/api/admin/offers/W14FLAT/toggle", headers=HDR_ADMIN)
exp = client.post("/api/admin/offers", json={"code": "W14OLD", "pct_off": 50, "applies_to": "credits",
                                              "valid_from": "2020-01-01", "valid_to": "2020-02-01"},
                  headers=HDR_ADMIN).json()
check("J6 expired offer create ok (enforce at use)", exp.get("success"), exp)
exp2 = client.post("/api/pay/order", json={"tsap_id": GID, "purpose": "credits", "ref": "S_99",
                                            "offer_code": "W14OLD"})
check("J7 expired use reject", exp2.status_code == 400, exp2.status_code)
la = client.get("/api/admin/offers", headers=HDR_ADMIN).json()
check("J8 admin offers list", la.get("success") and la.get("count", 0) >= 6, la.get("count"))
pub = client.get("/api/offers/active").json()
check("J9 public active (expired ledu)", pub.get("success") and "W14OLD" not in [o["code"] for o in pub["offers"]]
      and "DIWALI25" in [o["code"] for o in pub["offers"]], [o["code"] for o in pub["offers"]])

# ═══════════════════════════════════════════════════════════════════════════
section("K. ADS UPDATE (dates/districts)")
# ═══════════════════════════════════════════════════════════════════════════
ADS.CAMPAIGNS.clear()
cc = ADS.create_campaign("V-W14", "Wave14 Test Ad", "district", 7, districts=["Hyderabad"],
                        slots=["home_hero"])
CID = cc["campaign"]["id"]
up = client.post(f"/api/admin/ads/{CID}/update",
                 json={"districts": ["Hyderabad", "Vijayawada"], "days": 10, "offer": "Diwali 20% off"},
                 headers=HDR_ADMIN).json()
check("K1 update districts+days+offer",
      up.get("success") and up["campaign"]["districts"] == ["Hyderabad", "Vijayawada"]
      and up["campaign"]["days"] == 10, up.get("campaign"))
ap = client.post(f"/api/admin/ads/{CID}/approve", json={"utr": "UTR-W14-AD", "days": 10},
                 headers=HDR_ADMIN).json()
check("K2 approve live", ap.get("success") and ap["campaign"]["status"] == "active", ap)
up2 = client.post(f"/api/admin/ads/{CID}/update", json={"days": 15}, headers=HDR_ADMIN).json()
check("K3 active extend → end recompute",
      up2.get("success") and up2["campaign"]["days"] == 15
      and up2["campaign"]["end"] > ap["campaign"]["end"],
      (ap["campaign"]["end"], up2["campaign"]["end"]))
sv = client.get("/api/ads?slot=home_hero&district=Vijayawada").json()
check("K4 Vijayawada scope serve", sv.get("ok") and CID in str(sv), str(sv)[:150])
badk = client.post(f"/api/admin/ads/{CID}/update", json={"start": "not-a-date"}, headers=HDR_ADMIN)
check("K5 bad date reject", badk.status_code == 400, badk.status_code)
_saved_fast = os.environ.pop("WA_TEST_FAST", None)
noa = client.post(f"/api/admin/ads/{CID}/update", json={"days": 5})
check("K6 no admin key 403", noa.status_code == 403, noa.status_code)
if _saved_fast is not None:
    os.environ["WA_TEST_FAST"] = _saved_fast

# ═══════════════════════════════════════════════════════════════════════════
section("L. BOT /matches")
# ═══════════════════════════════════════════════════════════════════════════
bot = client.get(f"/api/bot/matches?tsap_id={GID}").json()
check("L1 bot top-3", bot.get("success") and bot.get("count") == 3 and len(bot.get("matches", [])) == 3, bot)
check("L2 bot text telugu + /view", "top-3" in bot.get("text", "") and "/view" in bot.get("text", ""),
      bot.get("text", "")[:200])
check("L3 bot masked (no phone)", not PHONE_RE.findall(bot.get("text", "")))
check("L4 bot skips honest", bot.get("skipped", {}).get("age", 0) >= 1, bot.get("skipped"))
check("L5 blocked B1 not suggested", B1 not in [m.get("tsap_id") for m in bot.get("matches", [])])
bot404 = client.get("/api/bot/matches?tsap_id=BOGUS-ID")
check("L6 bogus ID 404", bot404.status_code == 404, bot404.status_code)

# ═══════════════════════════════════════════════════════════════════════════
section("M. META ENDPOINTS")
# ═══════════════════════════════════════════════════════════════════════════
mr = client.get("/api/meta/religions").json()
check("M1 religions 7", mr.get("success") and len(mr.get("religions", [])) == 7, mr)
mc = client.get("/api/meta/castes?religion=Muslim").json()
check("M2 muslim castes API", mc.get("success") and "Syed" in mc.get("castes", []), mc.get("castes", [])[:4])
mc2 = client.get("/api/meta/castes?religion=Hindu").json()
check("M3 hindu 43 API", mc2.get("success") and len(mc2.get("castes", [])) == 43, len(mc2.get("castes", [])))

# ═══════════════════════════════════════════════════════════════════════════
section("N. REGRESSION GUARDS (old waves intact)")
# ═══════════════════════════════════════════════════════════════════════════
check("N1 gothram+surname fields intact",
      "gothram_skipped" in tm and "surname_skipped" in tm and "gothram" in str(sc2), list(tm.keys()))
check("N2 score has surname+gothram+age",
      "surname" in sc2 and "gothram" in sc2 and "age_rule" in sc2, list(sc2.keys())[:12])
sg = client.get(f"/api/match/score?a={GID}&b={B1}").json()
check("N3 old verdict keys untouched", "score" in sg and "grade" in sg, list(sg.keys())[:8])

print(f"\n{'=' * 76}\nRESULT: {PASS} pass / {FAIL} fail")
if FAILED:
    print("FAILED:", FAILED)
    sys.exit(1)
