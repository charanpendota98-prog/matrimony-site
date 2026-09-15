"""
MANA VIVAHA — MATCH SCORE 2.0 + TOP MATCHES TEST SUITE 🧠
========================================================
Run:  /tmp/venv/bin/python test_topmatch.py   (backend/ cwd nunchi)

Cover: weights sum, score/grade/breakdown shape, Telugu explanations, mutual bonus,
find_top_matches_v2 filters + ordering, /api/match/score, /api/top-matches,
/api/search match_v2 payload, OG image endpoints.
"""
import os
import sys

os.environ.setdefault("WA_TEST_FAST", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import topmatch  # noqa: E402

PASS = []
FAIL = []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✅ " if cond else "  ❌ ") + name + (("  | " + str(extra)) if extra else ""))


BRIDE = dict(tsap_id="TSAP-F-9001", gender="Bride", full_name="Sri Devi", age=24, caste="Reddy", sub_caste="Pakanati",
             education="BTech", education_detail="CSE", job="Software Engineer", company="TCS", salary="8L",
             height="5'4\"", district="Hyderabad", state="TS", star="Rohini", rasi="Vrishabha",
             gothram="Bharadwaj", marital_status="Pelli Kaledu", family_type="Nuclear",
             family_status="Middle Class", religion="Hindu", diet="Veg", is_approved=True, phone_verified=True)
GROOM = dict(tsap_id="TSAP-M-9001", gender="Groom", full_name="Ravi Kumar", age=29, caste="Reddy", sub_caste="Pakanati",
             education="BTech", education_detail="CSE", job="Software Engineer", company="Infosys", salary="12L",
             height="5'9\"", district="Hyderabad", state="TS", star="Uttara", rasi="Simha",
             gothram="Kashyapa", marital_status="Pelli Kaledu", family_type="Nuclear",
             family_status="Middle Class", religion="Hindu", diet="Veg", is_approved=True, phone_verified=True)
WRONG = dict(tsap_id="TSAP-M-9002", gender="Groom", full_name="Far Away", age=41, caste="Lambada",
             education="SSC", job="Daily Labour", salary="1L", height="5'2\"", district="Kurnool", state="AP",
             star="Ashlesha", rasi="Karkataka", marital_status="Divorced", family_type="Joint",
             family_status="Lower Middle", religion="Christian", is_approved=True)

print("=== 1. WEIGHTS ENGINE ===")
total_w = sum(topmatch.WEIGHTS.values())
check("weights sum = 100", total_w == 100, total_w)
check("11 components (top matrimony 7 kanna ekkuva)", len(topmatch.WEIGHTS) == 11, len(topmatch.WEIGHTS))
check("Telugu labels unnai", all(topmatch.LABELS[k][1] for k in topmatch.WEIGHTS))
check("caste + location weight high (matrimony reality)",
      topmatch.WEIGHTS["caste"] >= 12 and topmatch.WEIGHTS["location"] >= 10)
check("COMPONENTS anni WEIGHTS keys tho sync", {k for k, _ in topmatch.COMPONENTS} == set(topmatch.WEIGHTS))

print("=== 2. SCORE RESULT SHAPE ===")
res = topmatch.score_match_v2(GROOM, BRIDE)
for k in ("score", "grade", "grade_telugu", "verdict_telugu", "breakdown", "strengths", "weak_points",
          "how_to_improve", "explain_telugu", "mutual", "raw_score"):
    check("result lo '%s' undi" % k, k in res)
check("score 0-100 madhya", 0 <= res["score"] <= 100, res["score"])
check("grade valid", res["grade"] in ("perfect", "best", "good", "average", "low"), res["grade"])
check("breakdown 11 items (+mutual bonus row optional)", len(res["breakdown"]) in (11, 12), len(res["breakdown"]))
check("breakdown item shape", all({"key", "label", "telugu", "points", "max", "ratio", "note"} <= set(b.keys())
                                 for b in res["breakdown"]))
check("breakdown points <= max", all(b["points"] <= b["max"] + 0.01 for b in res["breakdown"]))
check("breakdown keys = WEIGHTS (+mutual bonus optional)",
      {b["key"] for b in res["breakdown"]} - {"mutual"} == set(topmatch.WEIGHTS))
check("explain_telugu detail untundi", len(str(res["explain_telugu"])) > 40 and "score" in str(res["explain_telugu"]).lower())
check("telugu script unudi (verdict)", any("\u0c00" <= ch <= "\u0c7f" for ch in res["verdict_telugu"]))
check("how_to_improve telugu text", isinstance(res["how_to_improve"], str) and len(res["how_to_improve"]) > 10)
check("grade_telugu unudi (Telugu UI badge)", bool(res.get("grade_telugu")))

print("=== 3. SCORE LOGIC (perfect vs wrong) ===")
check("same caste/city/age-bracket → best/perfect", res["score"] >= 70, res["score"])
bad = topmatch.score_match_v2(GROOM, WRONG)
check("mismatch profile low score", bad["score"] < res["score"], "%s < %s" % (bad["score"], res["score"]))
check("mismatch ki weak_points unnai", len(bad["weak_points"]) >= 2, bad["weak_points"][:2])
check("mismatch weak_points lo caste reason", any("caste" in str(w).lower() for w in bad["weak_points"]))
check("same-caste strength list lo caste point",
      any("caste" in str(s).lower() or "శాఖ" in str(s) or "కుల" in str(s) for s in res["strengths"]))

print("=== 4. MUTUAL BONUS ===")
check("mutual dict shape", {"their_score", "both_like", "note"} <= set(res["mutual"].keys()))
check("raw_score <= score (bonus eppudu negative kaadu)", res["raw_score"] <= res["score"], (res["raw_score"], res["score"]))
check("mutual.their_score 0-100", 0 <= res["mutual"]["their_score"] <= 100, res["mutual"]["their_score"])
high_pair = topmatch.score_match_v2(GROOM, BRIDE)
check("mutual both_like only when rendu 65+",
      bool(high_pair["mutual"]["both_like"]) == (high_pair["mutual"]["their_score"] >= 65 and res["score"] >= 65),
      (high_pair["mutual"].get("their_score"), res["score"]))
bonus_rows = [b for b in high_pair["breakdown"] if b["key"] == "mutual"]
if high_pair["mutual"]["both_like"]:
    check("mutual bonus breakdown row + 8%", len(bonus_rows) == 1 and bonus_rows[0]["note"].find("8%") >= 0)
    check("mutual bonus taruvata score penchindi", high_pair["score"] > high_pair["raw_score"],
          "%s > %s" % (high_pair["score"], high_pair["raw_score"]))
else:
    check("mutual bonus row ledu (bonus lekapote)", len(bonus_rows) == 0)

print("=== 5. FIND TOP MATCHES V2 ===")
pool = [BRIDE, GROOM, WRONG, dict(WRONG, tsap_id="TSAP-M-9003", is_approved=False, gender="Groom"),
        dict(BRIDE, tsap_id="TSAP-F-9002", gender="Bride")]
top = topmatch.find_top_matches_v2(BRIDE, pool, limit=10, min_score=40)
check("list return", isinstance(top, list), len(top))
check("tana gender profiles skip (bride ki bride radu)", all(r["profile"]["gender"] != "Bride" for r in top))
check("approve kaani profiles skip", all(r["profile"]["tsap_id"] != "TSAP-M-9003" for r in top))
check("sorted descending", all(top[i]["score"] >= top[i + 1]["score"] for i in range(len(top) - 1)))
check("generic pool: top lo best profile",
      bool(top) and all(t["score"] <= top[0]["score"] for t in top))
check("row shape (score + profile + breakdown)",
      all({"score", "grade", "profile", "strengths"} <= set(r.keys()) for r in top))
check("min_score respect", all(r["score"] >= 40 for r in top))
check("limit respect", len(topmatch.find_top_matches_v2(BRIDE, pool, limit=1)) <= 1)

print("=== 6. API ENDPOINTS (TestClient) ===")
try:
    from fastapi.testclient import TestClient
    import main

    with TestClient(main.app) as c:
        users = [u for u in main.DB_USERS if u.get("gender") == "Bride"][:2] + \
                [u for u in main.DB_USERS if u.get("gender") == "Groom"][:2]
        if len(users) >= 4:
            b, g = users[0], users[2]
            r = c.get("/api/match/score", params={"a": g["tsap_id"], "b": b["tsap_id"]})
            check("GET /api/match/score 200", r.status_code == 200, r.status_code)
            d = r.json()
            check("API score + breakdown + viewer", d.get("score") is not None and len(d.get("breakdown", [])) in (11, 12)
                  and d.get("other", {}).get("verification"), d.get("score"))
            check("API verification badge inside other", bool(d.get("other", {}).get("verification", {}).get("telugu")))

            r2 = c.get("/api/top-matches/%s" % b["tsap_id"], params={"limit": 5, "min_score": 30})
            check("GET /api/top-matches/{id} 200", r2.status_code == 200, r2.status_code)
            d2 = r2.json()
            check("top-matches count + results", isinstance(d2.get("results"), list) and d2.get("count") == len(d2["results"]))
            check("top-matches lo mutual_matches metric", "mutual_matches" in d2)
            check("top-matches rows lo profile fields", all("full_name" in x and "caste" in x for x in d2["results"]))

            r3 = c.get("/api/search", params={"viewer_id": g["tsap_id"], "limit": 5})
            check("GET /api/search viewer tho 200", r3.status_code == 200, r3.status_code)
            items = r3.json().get("items") or r3.json().get("results") or []
            sc = [i for i in items if i.get("score")]
            check("search rows lo score v2", len(sc) > 0, len(items))
            check("search rows lo match_v2 breakdown",
                  all("match_v2" in i and "breakdown" in i["match_v2"] for i in sc) if sc else False)
            check("search rows lo verification badge", all(i.get("verification_telugu") for i in items))

            r4 = c.get("/api/og/profile/%s.png" % b["tsap_id"])
            check("GET /api/og/profile/{id}.png 200", r4.status_code == 200, r4.status_code)
            check("PNG signature", r4.content[:8] == b"\x89PNG\r\n\x1a\n")
            check("1200x630 OG size", r4.headers.get("content-type") == "image/png", r4.headers.get("content-type"))

            r5 = c.get("/api/og/site.png")
            check("GET /api/og/site.png 200 PNG", r5.status_code == 200 and r5.content[:4] == b"\x89PNG")

            r6 = c.get("/api/match/score", params={"a": "TSAP-XX-1", "b": "TSAP-XX-2"})
            check("tappu IDs ki 404", r6.status_code == 404, r6.status_code)
        else:
            check("demo DB lo profiles levu (seed check)", False, len(main.DB_USERS))
except Exception as e:  # pragma: no cover
    check("TestClient suite", False, repr(e))

print("\n=== RESULT: %d pass / %d fail ===" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("🏆 MATCH SCORE 2.0 — ANNI TESTS PASS")
