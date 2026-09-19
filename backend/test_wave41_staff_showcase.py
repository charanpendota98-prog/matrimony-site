#!/usr/bin/env python3
"""
🌊 WAVE 41 — STAFF ROLES + WEEKLY CASTE SHOWCASE TEST SUITE
===========================================================
User: "admin manam mathrame · kinda pani chesevallaki separate limited access (full kakunda)
       · vivaha parichayam okko varam okko caste ki · vallaki mana profiles showcase"

A. STAFF ROLE (owner vs staff permissions):
   1. whoami: owner key → owner; staff key → staff; no key → 403
   2. staff CAN: profiles list, daily-matches candidates/set, showcase, match-send lookup, photos pending
   3. staff CANNOT: payouts queue, exports CSV, retention, leads, analytics (403 owner-only)
   4. no key at all → 403
B. WEEKLY SHOWCASE:
   5. public GET /api/showcase → success (empty ok)
   6. admin candidates?caste= → 400 without caste; ok with caste
   7. set showcase (2 same-caste profiles, no post) → success + public reflects
   8. cross-caste ID → 400; unknown ID → 404; >12 ids → capped
   9. rotation suggestion returned
"""
import os
import sys
from datetime import datetime

os.environ.setdefault("WA_TEST_FAST", "1")
# STAFF key set chesi test — production behaviour simulate
os.environ["STAFF_KEY"] = "staff-test-key-9876"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from fastapi.testclient import TestClient  # noqa: E402
import main as M  # noqa: E402
from hardening import ADMIN_KEY, STAFF_KEY  # noqa: E402

H_OWNER = {"x-admin-key": ADMIN_KEY}
H_STAFF = {"x-admin-key": STAFF_KEY}
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


# 🔒 enforcement ON — role tests kosam dev bypass off (dev_mode() env ni call-time lo chustundi)
for _f in ("WA_TEST_FAST", "TSAP_AUTH_MODE"):
    os.environ.pop(_f, None)

client = TestClient(M.app)

# deterministic test users (one caste — showcase kosam)
_now = datetime.utcnow().isoformat()
SC_CASTE = "Reddy"
seed = [{"tsap_id": "W41S01", "full_name": "Showcase One", "gender": "Bride", "age": 25, "caste": SC_CASTE,
         "district": "Nalgonda", "created_at": _now, "is_approved": True, "score": 91},
        {"tsap_id": "W41S02", "full_name": "Showcase Two", "gender": "Groom", "age": 28, "caste": SC_CASTE,
         "district": "Khammam", "created_at": _now, "is_approved": True, "score": 88},
        {"tsap_id": "W41K03", "full_name": "Other Caste", "gender": "Groom", "age": 30, "caste": "Kamma",
         "district": "Guntur", "created_at": _now, "is_approved": True}]
for _u in seed:
    if not any(x.get("tsap_id") == _u["tsap_id"] for x in M.DB_USERS):
        M.DB_USERS.append(_u)

# ---------------------------------------------------------------- A. STAFF ROLE
section("A. STAFF ROLE — owner full · staff limited · no key blocked")
r = client.get("/api/admin/whoami", headers=H_OWNER)
check("whoami: owner key → owner", r.status_code == 200 and r.json().get("role") == "owner")
r = client.get("/api/admin/whoami", headers=H_STAFF)
check("whoami: staff key → staff", r.status_code == 200 and r.json().get("role") == "staff")
r = client.get("/api/admin/whoami")
check("whoami: no key → 403", r.status_code == 403)

r = client.get("/api/admin/profiles?status=all&limit=5", headers=H_STAFF)
check("staff CAN: profiles list", r.status_code == 200)
r = client.get("/api/admin/daily-matches/candidates", headers=H_STAFF)
check("staff CAN: daily-matches candidates", r.status_code == 200)
r = client.get("/api/admin/match-send/W41S01", headers=H_STAFF)
check("staff CAN: match-send lookup", r.status_code == 200)
r = client.get("/api/admin/photos/pending", headers=H_STAFF)
check("staff CAN: photos pending", r.status_code == 200)

r = client.get("/api/admin/payouts", headers=H_STAFF)
check("staff CANNOT: payouts (owner-only)", r.status_code == 403, f"got {r.status_code}")
r = client.get("/api/admin/export/users.csv", headers=H_STAFF)
check("staff CANNOT: users export", r.status_code == 403, f"got {r.status_code}")
r = client.get("/api/admin/export/payments.csv", headers=H_STAFF)
check("staff CANNOT: payments export", r.status_code == 403, f"got {r.status_code}")
r = client.get("/api/admin/retention/preview", headers=H_STAFF)
check("staff CANNOT: retention", r.status_code == 403, f"got {r.status_code}")
r = client.get("/api/leads", headers=H_STAFF)
check("staff CANNOT: leads (PII)", r.status_code == 403, f"got {r.status_code}")

r = client.get("/api/admin/export/users.csv")
check("no key: export → 403", r.status_code == 403)
r = client.get("/api/admin/profiles")
check("no key: profiles → 403", r.status_code == 403)
r = client.get("/api/admin/profiles?status=all&limit=5", headers=H_OWNER)
check("owner CAN: everything (profiles)", r.status_code == 200)

# ---------------------------------------------------------------- B. SHOWCASE
section("B. WEEKLY CASTE SHOWCASE — వారానికి ఒక కులం")
r = client.get("/api/showcase")
check("public showcase 200", r.status_code == 200 and r.json().get("success"))

r = client.get("/api/admin/showcase/candidates", headers=H_OWNER)
check("candidates: no caste → 400", r.status_code == 400)
r = client.get(f"/api/admin/showcase/candidates?caste={SC_CASTE}", headers=H_STAFF)
d = r.json()
check("candidates: staff CAN load (caste ok)", r.status_code == 200 and d.get("success"))
ids = [c["tsap_id"] for c in d.get("candidates", []) if c["tsap_id"].startswith("W41S")]
check("candidates: our 2 Reddy profiles listed", len(ids) >= 2)
check("candidates: rotation suggestion present", bool(d.get("next_caste_suggestion")))

r = client.post("/api/admin/showcase", headers={**H_STAFF, "Content-Type": "application/json"},
                json={"caste": SC_CASTE, "profile_ids": ids[:2], "post_to_channels": False})
d = r.json()
check("set showcase (staff): success", r.status_code == 200 and d.get("success"))
check("set: selected ids", d.get("selected") == ids[:2])
r = client.get("/api/showcase")
d = r.json()
check("public: caste reflected", d.get("caste") == SC_CASTE)
got = [m["tsap_id"] for m in d.get("matches", [])]
check("public: both profiles shown", all(i in got for i in ids[:2]))
check("public: NO phone leak", all("phone" not in m for m in d.get("matches", [])))

r = client.post("/api/admin/showcase", headers={**H_OWNER, "Content-Type": "application/json"},
                json={"caste": SC_CASTE, "profile_ids": ["W41K03"], "post_to_channels": False})
check("cross-caste ID → 400", r.status_code == 400)
r = client.post("/api/admin/showcase", headers={**H_OWNER, "Content-Type": "application/json"},
                json={"caste": SC_CASTE, "profile_ids": ["NOPE123"], "post_to_channels": False})
check("unknown ID → 404", r.status_code == 404)
big = ids[:2] * 8  # 16 ids → cap 12
r = client.post("/api/admin/showcase", headers={**H_OWNER, "Content-Type": "application/json"},
                json={"caste": SC_CASTE, "profile_ids": big, "post_to_channels": False})
check(">12 ids → capped to 12", r.status_code == 200 and len(r.json().get("selected", [])) <= 12)
r = client.post("/api/admin/showcase", headers={"Content-Type": "application/json"},
                json={"caste": SC_CASTE, "profile_ids": ids[:1]})
check("showcase set: no key → 403", r.status_code == 403)

# ---------------------------------------------------------------- RESULT
section("RESULT")
print(f"PASS {PASS} · FAIL {FAIL}")
if FAIL:
    print("❌ WAVE 41 — FIX CHEYALI")
    sys.exit(1)
print("✅ WAVE 41 — ALL GREEN (staff roles + weekly caste showcase)")
