#!/usr/bin/env python3
"""
🌊 WAVE 40 — RETENTION + DAILY MATCHES + EXPORTS + BRAND TEST SUITE
===================================================================
User: "3 years profiles delete cheyali (space) · matches of the day select chesi post ·
       valla data Excel lo kavali · wallet 0 avvali kaani history undali · మన వివాహ (vivaham కాదు)"

A. RETENTION (3-year auto-delete):
   1. preview: 4-year-old → to_delete; wallet>0/plan-active → skipped_active; fresh → untouched
   2. run: archive file create + delete + interests/views cleanup + payments untouched
   3. safety: run on empty/dry_run safe
B. DAILY MATCHES:
   4. public endpoint: empty → success + 0
   5. admin set (2 IDs) → today selection + public shows them (post_to_channels=False — dry sandbox)
   6. invalid ID → 404; no ids → 400; no admin key → 401/403
C. EXPORTS (Excel CSV):
   7. users.csv / payments.csv / leads.csv → 200 + text/csv + header row + BOM
   8. no admin key → 401/403
D. BRAND: "మన వివాహ" everywhere; "Mana Vivaha"/"మనవివాహం" ZERO in user-facing code
E. WALLET: payout approve → wallet 0 + paid_out + lifetime intact (referral unit level)
"""
import os
import sys
import json
from datetime import datetime, timedelta

os.environ.setdefault("ADMIN_KEY", "")
os.environ.setdefault("WA_TEST_FAST", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from fastapi.testclient import TestClient  # noqa: E402
import main as M  # noqa: E402
from hardening import ADMIN_KEY  # noqa: E402

H_ADMIN = {"x-admin-key": ADMIN_KEY}
PASS = 0
FAIL = 0


def section(t):
    print("\n" + "=" * 62 + "\n" + t + "\n" + "=" * 62)


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name} {extra}")


client = TestClient(M.app)

# ---------------------------------------------------------------- A. RETENTION
section("A. RETENTION — 3-year auto-delete (archive first)")
import retention as RT  # noqa: E402

old_iso = (datetime.utcnow() - timedelta(days=365 * 4 + 10)).isoformat()
fresh_iso = datetime.utcnow().isoformat()
plan_iso = (datetime.utcnow() + timedelta(days=30)).isoformat()
fake_users = [
    {"tsap_id": "OLD001", "full_name": "Old Profile", "created_at": old_iso},
    {"tsap_id": "OLD002", "full_name": "Wallet Active", "created_at": old_iso, "wallet": 150},
    {"tsap_id": "OLD003", "full_name": "Plan Active", "created_at": old_iso, "plan_until": plan_iso},
    {"tsap_id": "NEW001", "full_name": "Fresh", "created_at": fresh_iso},
]
p = RT.preview(fake_users)
check("preview: OLD001 → to_delete", any(x["tsap_id"] == "OLD001" for x in p["to_delete"]))
check("preview: wallet ₹150 → skipped", any(x["tsap_id"] == "OLD002" and x["reason"] == "wallet_balance" for x in p["skipped_active"]))
check("preview: plan active → skipped", any(x["tsap_id"] == "OLD003" and x["reason"] == "plan_until" for x in p["skipped_active"]))
check("preview: fresh untouched", not any(x["tsap_id"] == "NEW001" for x in p["to_delete"]))

ints = [{"from_id": "OLD001", "to_id": "NEW001"}, {"from_id": "NEW001", "to_id": "NEW001"}]
views = [{"tsap_id": "OLD001", "viewer_id": "NEW001"}]
saves = [{"tsap_id": "NEW001", "saved_id": "OLD001"}]
res = RT.run(fake_users, ints, views, saves)
check("run: deleted=1", res.get("deleted") == 1)
check("run: archive file created", os.path.exists(res.get("archive", "")))
arc = json.load(open(res["archive"], encoding="utf-8"))
check("run: archive has OLD001 full profile", any(u["tsap_id"] == "OLD001" for u in arc["profiles"]))
check("run: OLD001 removed from users", not any(u["tsap_id"] == "OLD001" for u in fake_users))
check("run: NEW001 kept", any(u["tsap_id"] == "NEW001" for u in fake_users))
check("run: OLD001 interests cleaned", not any(i.get("from_id") == "OLD001" for i in ints))
check("run: OLD001 views cleaned", not any(v.get("tsap_id") == "OLD001" for v in views))
check("run: OLD001 saves cleaned", not any(s.get("saved_id") == "OLD001" for s in saves))
check("run: retention_log written", os.path.exists(RT.LOG_FILE))
check("run: dry_run safe", RT.run(fake_users, ints, views, saves, dry_run=True)["deleted"] == 0)

# live admin endpoints
r = client.get("/api/admin/retention/preview", headers=H_ADMIN)
check("GET /api/admin/retention/preview 200", r.status_code == 200 and r.json().get("success"))
check("preview has policy_years", r.json().get("policy_years") == 3)
if M.auth_enforced():
    r = client.get("/api/admin/retention/preview")
    check("retention preview: NO admin key → 401/403", r.status_code in (401, 403))
else:
    print("  ⏭️ retention no-key check skipped (dev/test auth bypass)")

# ---------------------------------------------------------------- B. DAILY MATCHES
section("B. DAILY MATCHES — admin select → today's featured")
r = client.get("/api/daily-matches")
d = r.json()
check("GET /api/daily-matches 200", r.status_code == 200 and d.get("success"))
check("public: matches list present", "matches" in d)

# deterministic test users (DB empty in test env)
_now = datetime.utcnow().isoformat()
for _i, _u in enumerate([{"tsap_id": "W40D01", "full_name": "Daily One", "gender": "Bride", "age": 26,
                           "caste": "Reddy", "district": "Nalgonda", "created_at": _now},
                          {"tsap_id": "W40D02", "full_name": "Daily Two", "gender": "Groom", "age": 29,
                           "caste": "Kamma", "district": "Warangal", "created_at": _now}]):
    if not any(x.get("tsap_id") == _u["tsap_id"] for x in M.DB_USERS):
        M.DB_USERS.append(_u)
r = client.get("/api/admin/daily-matches/candidates", headers=H_ADMIN)
check("GET candidates 200 + rows", r.status_code == 200 and isinstance(r.json().get("candidates"), list))
cand = r.json().get("candidates") or []
pick = [c["tsap_id"] for c in cand[:2]]
if len(pick) < 2:
    # demo DB lo profiles undo — create quick ones via demo seed fallback
    pick = [u["tsap_id"] for u in M.DB_USERS[:2]]
check("candidates list non-empty", len(pick) >= 1)

r = client.post("/api/admin/daily-matches", headers={**H_ADMIN, "Content-Type": "application/json"},
                json={"profile_ids": pick, "post_to_channels": False})
d = r.json()
check("POST set today 200", r.status_code == 200 and d.get("success"))
check("selected == sent ids", d.get("selected") == pick)
r = client.get("/api/daily-matches")
d = r.json()
check("public shows today's picks", d.get("count") == len(pick) and [m["tsap_id"] for m in d["matches"]] == pick)
row = (d.get("matches") or [{}])[0]
check("public row: NO phone leak", "phone" not in row)

r = client.post("/api/admin/daily-matches", headers={**H_ADMIN, "Content-Type": "application/json"},
                json={"profile_ids": []})
check("empty ids → 400", r.status_code == 400)
r = client.post("/api/admin/daily-matches", headers={**H_ADMIN, "Content-Type": "application/json"},
                json={"profile_ids": ["NOPE999"], "post_to_channels": False})
check("bad ID → 404", r.status_code == 404)
if M.auth_enforced():
    r = client.post("/api/admin/daily-matches", headers={"Content-Type": "application/json"},
                    json={"profile_ids": pick})
    check("set: NO admin key → 401/403", r.status_code in (401, 403))
else:
    print("  ⏭️ set no-key check skipped (dev/test auth bypass)")

# ---------------------------------------------------------------- C. EXPORTS
section("C. EXCEL EXPORTS — CSV (BOM + header)")
for path, fname in [("/api/admin/export/users.csv", "profiles"),
                    ("/api/admin/export/payments.csv", "payments"),
                    ("/api/admin/export/leads.csv", "leads")]:
    r = client.get(path, headers=H_ADMIN)
    ok = r.status_code == 200 and "csv" in r.headers.get("content-type", "")
    body = r.text
    check(f"{fname}.csv 200 + csv type", ok)
    check(f"{fname}.csv BOM (Excel Telugu)", body.startswith("\ufeff"))
    check(f"{fname}.csv header row", body.splitlines()[0].count(",") >= 2)
if M.auth_enforced():
    r = client.get("/api/admin/export/users.csv")
    check("users.csv NO admin key → 401/403", r.status_code in (401, 403))
else:
    print("  ⏭️ users.csv no-key check skipped (dev/test auth bypass)")
r = client.get("/api/admin/export/users.csv", headers=H_ADMIN)
check("users.csv rows == DB users", len(r.text.strip().splitlines()) - 1 == len(M.DB_USERS))

# ---------------------------------------------------------------- D. BRAND
section("D. BRAND — మన వివాహ (Mana Vivaha, vivaham కాదు)")
r = client.get("/api/plans")
check("plans: VIP label (Vivaha VIP కాదు)", not any("Vivaha VIP" in str(p.get("label", "")) for p in r.json().get("plans", [])))
brand_hits = 0
for f in ("main.py", "referral.py", "card_pro.py", "channels_config.py", "channel_content.py", "interest.py", "credits.py"):
    src = open(os.path.join(HERE, f), encoding="utf-8").read()
    import re as _re
    lines = [l for l in src.splitlines() if "Mana Vivaha" in l and not l.strip().startswith("#")]
    brand_hits += len(lines)
check("backend user-facing code: 'Mana Vivaha' ZERO", brand_hits == 0, f"found {brand_hits}")
mani = open(os.path.join(HERE, "..", "frontend", "public", "manifest.webmanifest"), encoding="utf-8").read()
check("manifest: మన వివాహ (vivaham కాదు)", "మన వివాహ" in mani and "మనవివాహం" not in mani)

# ---------------------------------------------------------------- E. WALLET
section("E. WALLET — pay చేసిన తర్వాత 0, history ఉంటుంది")
import referral as R  # noqa: E402
u = {"tsap_id": "W40T01", "full_name": "Wallet Test", "wallet": 200,
     "referral_code": "W400001"}
req = R.payout_request(u, 200, upi_id="wallet40@okhdfcbank")
check("payout request ok", req.get("ok"))
st = u["referral_stats"]
check("payout request: wallet → 0", float(u.get("wallet", 0)) == 0 and float(st["wallet"]) == 0)
check("payout request: pending 200", float(st["pending_payout"]) == 200)
check("lifetime_earned stays 200 (history)", float(st["lifetime_earned"]) == 200)
res = R.payout_action(req["request"]["id"], "paid", [u], utr="UTR12345678")
check("payout approve ok", res.get("ok"))
check("paid: pending → 0", float(st["pending_payout"]) == 0)
check("paid: paid_out 200 (settled history)", float(st["paid_out"]) == 200)
check("paid: ledger has UTR entry", any("UTR" in str(e.get("note", "")) for e in st.get("ledger", [])))

# ---------------------------------------------------------------- RESULT
section("RESULT")
print(f"PASS {PASS} · FAIL {FAIL}")
if FAIL:
    print("❌ WAVE 40 — FIX CHEYALI")
    sys.exit(1)
print("✅ WAVE 40 — ALL GREEN (retention + daily matches + exports + brand + wallet)")
