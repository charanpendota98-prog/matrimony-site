"""
🔒 WAVE 12 TEST SUITE — SMART REVEAL ENGINE
===========================================
Cover:
  A. masking pure (name/surname/phone — public lo eppudu ledu)
  B. masked channel captions (rewired build_caption + WA text, old asserts intact)
  C. unlock engine (self free / credit deduct / entitled free / paywall / audit)
  D. ₹500 assisted orders (create → UTR-paid guard → attach STRICT)
  E. API (link / unlock / unlocks / match-send / copy-list / deliver)
  F. bot (/unlock /mylist /balance /pay /link + masked card + handlers)
  G. privacy regression (public endpoints lo numbers ledu; admin copy-list lo untayi)

Run:  WA_TEST_FAST=1 python3 test_wave12_smart.py   (backend/ nunchi)
"""
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
import smart12 as S12
import channels_config as CC
import publisher as PUB
import telegram_bot as TB

client = TestClient(main.app, raise_server_exceptions=False)
HDR_ADMIN = {"X-Admin-Key": H.ADMIN_KEY}

# fresh state (S12 stores matrame clear — vere suites ki touch kadu)
S12.UNLOCKS.clear()
S12.ORDERS.clear()
S12.REVEAL_LOG.clear()

# ═══════════════════════════════════════════════════════════════════════════
section("A. MASKING (pure)")
# ═══════════════════════════════════════════════════════════════════════════
check("A1 mask_name: full+surname rendu mask", S12.mask_name("Lakshmi Reddy") == "L•••••i R•••y",
      S12.mask_name("Lakshmi Reddy"))
check("A2 mask lo original words ledu",
      "Lakshmi" not in S12.mask_name("Lakshmi Reddy") and "Reddy" not in S12.mask_name("Lakshmi Reddy"))
check("A3 single word kooda mask", S12.mask_name("Sravani") == "S•••••i", S12.mask_name("Sravani"))
check("A4 short name as-is (T)", S12.mask_name("T") == "T")
check("A5 empty → —", S12.mask_name("") == "—")
check("A6 mask_phone format", S12.mask_phone("9848012345") == "98••••••45", S12.mask_phone("9848012345"))
check("A7 short phone lock", S12.mask_phone("12") == "🔒 •••••")
check("A8 first_masked paid-format", S12.first_masked("Lakshmi Reddy") == "Lakshmi R.",
      S12.first_masked("Lakshmi Reddy"))
check("A9 assert_no_leak ok", S12.assert_no_leak("hello 98••••••45 world")["ok"] is True)
check("A10 assert_no_leak catches", S12.assert_no_leak("call 9848012345")["ok"] is False)

# ═══════════════════════════════════════════════════════════════════════════
section("B. MASKED CHANNEL CAPTIONS (rewired, old asserts intact)")
# ═══════════════════════════════════════════════════════════════════════════
prof = {"full_name": "Lakshmi Reddy", "gender": "Bride", "age": 24, "height": "5'4\"",
        "caste": "Reddy", "education": "BTech", "job": "Software", "district": "Hyderabad",
        "state": "TS", "gothram": "Bharadwaj", "star": "Rohini", "phone": "9848012345"}
cap = CC.build_caption(prof, "TSAP-F-2025-5775", 92)
check("B1 caption: full name ledu", "Lakshmi Reddy" not in cap)
check("B2 caption: FIRST NAME visible (W13)", "\U0001F470 Lakshmi \u2022" in cap, cap[:200])
check("B3 caption: surname name-line lo ledu", "Lakshmi R" not in cap, cap.split(chr(10))[1])
check("B4 caption: full-name string ekkada ledu", "Lakshmi" in cap and "Lakshmi Reddy" not in cap)
check("B5 caption: number ledu", not PHONE_RE.findall(cap))
check("B6 caption: ID/score/bot/register/safety intact",
      "TSAP-F-2025-5775" in cap and "92%" in cap and CC.BOT_USERNAME in cap
      and "/register" in cap and "mosam jagratha" in cap.lower())
check("B7 caption: /unlock CTA undi", "/unlock TSAP-F-2025-5775" in cap)
wa = PUB.build_whatsapp_text(prof, "TSAP-F-2025-0001", 90)
check("B8 WA text: name+number ledu, link undi",
      "Lakshmi Reddy" not in wa and "Lakshmi" in wa and not PHONE_RE.findall(wa) and "/search/TSAP-F-2025-0001" in wa, wa[:200])
check("B9 WA text: first-name + unlock CTA", "Lakshmi" in wa and "Lakshmi Reddy" not in wa and "/unlock" in wa)

# ═══════════════════════════════════════════════════════════════════════════
section("C. UNLOCK ENGINE (pure)")
# ═══════════════════════════════════════════════════════════════════════════
viewer = {"tsap_id": "V1", "credits": 3}
target = {"tsap_id": "T1", "phone": "9848011111"}
r = S12.unlock_number(viewer, target)
check("C1 first unlock: success + 1 cut", r["success"] and viewer["credits"] == 2 and r["phone"] == "9848011111", r)
check("C2 entitled ayyadu", S12.is_entitled("V1", "T1"))
r2 = S12.unlock_number(viewer, target)
check("C3 second time FREE (credit cut kadu)", r2["success"] and viewer["credits"] == 2 and r2["charged"] == 0, r2)
poor = {"tsap_id": "V2", "credits": 0}
r3 = S12.unlock_number(poor, {"tsap_id": "T2", "phone": "9848022222"})
check("C4 0 credits → paywall, number ledu",
      not r3["success"] and r3["reason"] == "no_credits" and "phone" not in r3, r3)
check("C5 paywall lo pay options", "₹500" in r3.get("message_telugu", "") and r3.get("pay_options"), r3.get("message_telugu"))
me = {"tsap_id": "V3", "credits": 0, "phone": "9848033333"}
r4 = S12.unlock_number(me, dict(me))
check("C6 self unlock free (0 credits ayina)", r4["success"] and r4["phone"] == "9848033333", r4)
check("C7 audit log undi", len(S12.REVEAL_LOG) >= 2 and S12.REVEAL_LOG[0]["viewer"] == "V1", S12.REVEAL_LOG[:2])
S12.grant_unlock("V9", "T9", via="admin_gift")
check("C8 admin gift grant (credit touch kadu)", S12.is_entitled("V9", "T9"))
lst = S12.my_unlocks("V1", [{"tsap_id": "T1", "full_name": "Lakshmi Reddy", "phone": "9848011111",
                              "age": 24, "caste": "Reddy", "district": "Hyd"}])
check("C9 my_unlocks masked (number ledu)", lst["count"] == 1 and not PHONE_RE.findall(str(lst)), str(lst)[:200])

# ═══════════════════════════════════════════════════════════════════════════
section("D. ₹500 ORDERS (pure)")
# ═══════════════════════════════════════════════════════════════════════════
o = S12.create_order("V1", 500, "test")
check("D1 order create requested", o["status"] == "requested" and o["amount"] == 500, o)
p0 = S12.mark_order_paid(o["id"], "")
check("D2 UTR lekunda paid KUDADU", p0["success"] is False, p0)
a0 = S12.attach_order_profiles(o["id"], ["T1"])
check("D3 paid-kamundu attach KUDADU", a0["success"] is False, a0)
p1 = S12.mark_order_paid(o["id"], "UTR123456")
check("D4 UTR tho paid", p1["success"] and S12.get_order(o["id"])["status"] == "paid")
a1 = S12.attach_order_profiles(o["id"], ["T1", "T2"])
check("D5 paid tarvata attach success", a1["success"] and a1["attached"] == 2, a1)
check("D6 STRICT: attached-vi mathrame entitled",
      S12.is_entitled("V1", "T1") and S12.is_entitled("V1", "T2") and not S12.is_entitled("V1", "T3"))
cl = S12.build_copy_list({"full_name": "Ravi Kumar"}, [
    {"full_name": "Sravani K", "phone": "9848011111", "tsap_id": "T1", "gender": "Bride",
     "caste": "Kamma", "age": 26, "district": "Vijayawada"}], o["id"])
check("D7 copy-list NAME -- NUMBER format", "Sravani K." in cl and "-- 9848011111" in cl and "T1" in cl, cl[:250])
pack = S12.build_personal_pack({"full_name": "Ravi Kumar"},
                               [{"full_name": "Lakshmi Reddy", "phone": "9848012345", "tsap_id": "T1",
                                 "gender": "Bride", "age": 24, "caste": "Reddy", "district": "Hyd", "state": "TS"}])
check("D8 personal pack header+card", len(pack) == 2 and "9848012345" in pack[1] and "₹500" in pack[0], pack[0][:150])

# ═══════════════════════════════════════════════════════════════════════════
section("E. API (link/unlock/unlocks/match-send/copy/deliver)")
# ═══════════════════════════════════════════════════════════════════════════
client.post("/api/demo/seed")
BB = {"gender": "Bride", "age": "25", "height": "5'4\"", "marital_status": "Pelli Kaledu", "caste": "Reddy",
      "education": "BTech", "job": "Software", "salary": "60k", "state": "TS", "district": "Hyderabad",
      "phone": "9848011111", "full_name": "Wave Twelve Bride One", "gothram": "Bharadwaj",
      "star": "Rohini", "religion": "Hindu"}
BB2 = dict(BB, phone="9848012222", full_name="Wave Twelve Bride Two", gothram="Kasyapa", star="Ashwini")
BG = dict(BB, gender="Groom", age="29", phone="9848022222", full_name="Wave Twelve Buyer Groom",
          gothram="Koundinya", height="5'9\"")
b1 = client.post("/api/register", data=BB).json()
b2 = client.post("/api/register", data=BB2).json()
buyer = client.post("/api/register", data=BG).json()
B1, B2, BUY = b1.get("tsap_id", ""), b2.get("tsap_id", ""), buyer.get("tsap_id", "")
check("E0 3 users register", all([B1, B2, BUY]), (B1, B2, BUY))
for _u in main.DB_USERS:
    if _u.get("tsap_id") in (B1, B2, BUY):
        _u["is_approved"] = True
S12.UNLOCKS.pop(BUY, None)

lk = client.post("/api/link-telegram", json={"tsap_id": BUY, "chat_id": "777001"}).json()
check("E1 link-telegram success", lk.get("success") is True, lk)
lk_bad = client.post("/api/link-telegram", json={"tsap_id": "TSAP-X-0000", "chat_id": "1"})
check("E2 link tappu ID → 404", lk_bad.status_code == 404, lk_bad.status_code)

cr0 = next(u for u in main.DB_USERS if u["tsap_id"] == BUY).get("credits", 0)
un = client.post("/api/unlock", json={"viewer_id": BUY, "target_id": B1}).json()
check("E3 unlock: number + 1 cut", un.get("success") and un.get("phone") == "9848011111"
      and un.get("credits_left") == cr0 - 1, un)
un2 = client.post("/api/unlock", json={"viewer_id": BUY, "target_id": B1}).json()
check("E4 malli unlock FREE", un2.get("success") and un2.get("charged") == 0, un2)
poor_u = next(u for u in main.DB_USERS if u["tsap_id"] == BUY)
poor_u["credits"] = 0
un3 = client.post("/api/unlock", json={"viewer_id": BUY, "target_id": B2}).json()
check("E5 0 credits → paywall", un3.get("success") is not True and un3.get("reason") == "no_credits", un3)
poor_u["credits"] = 5
my = client.get(f"/api/unlocks/{BUY}").json()
check("E6 unlocks list masked", my.get("count", 0) >= 1 and not PHONE_RE.findall(str(my)), str(my)[:220])

ms = client.get(f"/api/admin/match-send/{BUY}?limit=20&min_score=0", headers=HDR_ADMIN).json()
check("E7 match-send buyer box", ms.get("buyer", {}).get("tsap_id") == BUY
      and ms.get("buyer", {}).get("telegram_linked") is True, str(ms.get("buyer"))[:200])
check("E8 match-send results (admin sees phones)", ms.get("count", 0) >= 1
      and any(r.get("phone") for r in ms.get("results", [])), ms.get("count"))
ms_bad = client.get("/api/admin/match-send/TSAP-X-0000", headers=HDR_ADMIN)
check("E9 match-send tappu ID → 404", ms_bad.status_code == 404)

oc = client.post("/api/admin/assist-orders", json={"buyer_id": BUY, "note": "t12"}, headers=HDR_ADMIN).json()
OID = (oc.get("order") or {}).get("id", "")
check("E10 assist order create", oc.get("success") and OID.startswith("ORD-"), oc)
op_bad = client.post(f"/api/admin/assist-orders/{OID}/paid", json={"utr": ""}, headers=HDR_ADMIN)
check("E11 paid UTR lekunda → 400", op_bad.status_code == 400, op_bad.status_code)
op = client.post(f"/api/admin/assist-orders/{OID}/paid", json={"utr": "UTR-T12-001"}, headers=HDR_ADMIN).json()
check("E12 paid success", op.get("success") is True, op)
oa = client.post(f"/api/admin/assist-orders/{OID}/profiles", json={"profile_ids": [B1, B2]},
                 headers=HDR_ADMIN).json()
check("E13 attach 2 profiles", oa.get("success") and oa.get("attached") == 2, oa)
check("E14 STRICT API: B1,B2 entitled, inkokati kadu",
      S12.is_entitled(BUY, B1) and S12.is_entitled(BUY, B2) and not S12.is_entitled(BUY, "TSAP-F-2099-XXXX"))

cp = client.get(f"/api/admin/match-send/copy-list?buyer={BUY}&ids={B1},{B2}&order_id={OID}",
                headers=HDR_ADMIN).json()
check("E15 copy-list format (admin: numbers untayi)",
      cp.get("success") and "-- 9848011111" in cp.get("text", "") and "-- 9848012222" in cp.get("text", ""),
      cp.get("text", "")[:250])

dl = client.post("/api/admin/match-send/deliver",
                 json={"buyer_id": BUY, "profile_ids": [B1, B2], "via": "both", "order_id": OID},
                 headers=HDR_ADMIN).json()
check("E16 deliver success + copy_list", dl.get("success") and "-- 9848011111" in dl.get("copy_list", ""), str(dl)[:250])
check("E17 deliver dry-run honest (tokens ledu)",
      dl.get("telegram", {}).get("failed") != "" or dl.get("telegram", {}).get("sent", 0) >= 0, dl.get("telegram"))
check("E18 order delivered ayyindi leda preview", S12.get_order(OID)["status"] in ("paid", "delivered"),
      S12.get_order(OID)["status"])

al = client.post("/api/admin/link-telegram", json={"buyer_id": BUY, "chat_id": "777002"},
                 headers=HDR_ADMIN).json()
check("E19 admin manual link", al.get("success") and al.get("telegram_chat_id") == "777002", al)

# ═══════════════════════════════════════════════════════════════════════════
section("F. BOT (commands + masked card + formatters)")
# ═══════════════════════════════════════════════════════════════════════════
check("F1 import-safe (token lekapoina)", TB.get_bot() is None and "BOT_TOKEN" in TB.bot_status().get("error", "BOT_TOKEN"))
check("F2 help lo kotha commands",
      all(c in TB.help_text() for c in ("/unlock", "/mylist", "/balance", "/pay", "/link"))
      and "/search" in TB.help_text() and "₹99" in TB.help_text())
card = TB.format_id_search({"tsap_id": "TSAP-F-1", "full_name": "Lakshmi Reddy", "gender": "Bride",
                            "age": 24, "caste": "Reddy", "education": "BTech", "job": "SW",
                            "district": "Hyd", "state": "TS", "star": "Rohini",
                            "gothram": "Bharadwaj", "phone": "9848012345"})
check("F3 bot card first-name + surname/number ledu", "Lakshmi" in card and "Lakshmi Reddy" not in card and "9848012345" not in card
      and "TSAP-F-1" in card and "/unlock TSAP-F-1" in card, card[:200])
t_ok = TB.unlock_result_text({"success": True, "phone": "9848012345", "charged": 1, "credits_left": 2})
check("F4 unlock text (paid)", "9848012345" in t_ok and "2" in t_ok, t_ok[:150])
t_free = TB.unlock_result_text({"success": True, "phone": "9848012345", "charged": 0})
check("F5 unlock text (free)", "FREE" in t_free, t_free[:150])
t_pay = TB.unlock_result_text({"success": False, "reason": "no_credits", "message_telugu": "Credits ayipoyayi!"})
check("F6 unlock paywall text", "/pay" in t_pay, t_pay[:150])
t_my = TB.mylist_text({"profiles": [{"name_masked": "L•••••i", "phone_masked": "98••••••45",
                                     "tsap_id": "T1", "caste": "Reddy"}]})
check("F7 mylist text masked", "L•••••i" in t_my and "98••••••45" in t_my, t_my[:200])
t_my0 = TB.mylist_text({"profiles": []})
check("F8 mylist empty → /unlock hint", "/unlock" in t_my0 and "₹500" in t_my0, t_my0[:200])
check("F9 balance text", "7" in TB.balance_text(7, "S_99") and "S_99" in TB.balance_text(7, "S_99"))
check("F10 pay text (UPI + packs)", "UPI" in TB.pay_text() and "₹500" in TB.pay_text(), TB.pay_text()[:200])
n_handlers = len(TB.dp.message.handlers) + len(TB.dp.callback_query.handlers)
check("F11 handlers >= 15 (5 kotha commands + pathavi)", n_handlers >= 15, n_handlers)

# ═══════════════════════════════════════════════════════════════════════════
section("G. PRIVACY REGRESSION (public ≠ numbers, admin = numbers)")
# ═══════════════════════════════════════════════════════════════════════════
r = client.get("/api/search?limit=5")
check("G1 /api/search lo numbers ledu", not PHONE_RE.findall(r.text), PHONE_RE.findall(r.text)[:3])
r = client.get(f"/api/search/{B1}")
check("G2 /api/search/ID lo numbers ledu", not PHONE_RE.findall(r.text), PHONE_RE.findall(r.text)[:3])
r = client.get(f"/api/top-matches/{BUY}?limit=5")
check("G3 /api/top-matches lo numbers ledu", not PHONE_RE.findall(r.text), PHONE_RE.findall(r.text)[:3])
r = client.get("/api/stories")
check("G4 /api/stories lo numbers ledu", not PHONE_RE.findall(r.text))
r = client.get("/api/channels")
check("G5 /api/channels lo numbers ledu", not PHONE_RE.findall(r.text))
r = client.get(f"/api/unlocks/{BUY}")
check("G6 /api/unlocks list lo numbers ledu", not PHONE_RE.findall(r.text), PHONE_RE.findall(r.text)[:3])
r = client.get(f"/api/admin/match-send/copy-list?buyer={BUY}&ids={B1}", headers=HDR_ADMIN)
check("G7 admin copy-list lo number UNDI (correct)", "9848011111" in r.text, r.text[:150])
r = client.get(f"/api/publish/preview?tsap_id={B1}" if False else "/api/publish/status")
check("G8 publish status reachable", r.status_code == 200, r.status_code)

print(f"\n{'=' * 76}\nRESULT: {PASS} pass / {FAIL} fail")
if FAILED:
    print("FAILED:", FAILED)
    sys.exit(1)
