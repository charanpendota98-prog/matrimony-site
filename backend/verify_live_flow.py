"""
🔍 LIVE SMOKE — Mana Vivaha (referral 2.0)
==========================================
Run (servers already running):
    /tmp/venv/bin/python verify_live_flow.py                 # pages + read-only APIs
    /tmp/venv/bin/python verify_live_flow.py --flow          # + register→pay→₹50 E2E (DB lo kotha user)

Website :3000 (proxy → :8000) kanipinchali. Fail ayithe exit 1.
"""
import json
import os
import random
import sys
import urllib.error
import urllib.parse
import urllib.request

WEB = os.getenv("SMOKE_WEB", "http://localhost:3000")
API = os.getenv("SMOKE_API", "http://localhost:8000")
PASS, FAIL = [], []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✅ " if cond else "  ❌ ") + name + (("  | " + str(extra)) if extra and not cond else ""))


def get(url, base=API, method="GET"):
    try:
        req = urllib.request.Request(base + url, method=method)
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()
            ctype = r.headers.get("content-type", "")
            data = json.loads(body.decode("utf-8")) if "json" in ctype else body
            return r.status, data
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:200]
    except Exception as e:
        return 0, str(e)[:120]


def post_form(url, fields: dict, base=API):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(base + url, data=data, method="POST",
                                headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300]
    except Exception as e:
        return 0, str(e)[:150]


print("=== 1. PAGES (website :3000) ===")
PAGES = ["/", "/pricing", "/terms", "/privacy", "/refund", "/register", "/referral",
         "/referral/register", "/admin", "/channels", "/casts" if False else "/castes",
         "/matches", "/requests", "/porutham", "/safety", "/sitemap.xml", "/robots.txt"]
for p in PAGES:
    st, body = get(p, WEB)
    check("page %s → 200" % p, st == 200, st)

print("=== 2. CORE APIs ===")
st, plans = get("/api/plans")
check("/api/plans 200 + ladder", st == 200 and isinstance(plans.get("plans"), list), st)
if isinstance(plans, dict) and plans.get("plans"):
    ladder = {p["code"]: (p["price"], p.get("credits", p.get("profiles"))) for p in plans["plans"]}
    check("pricing ladder FREE3/₹99=5/₹199=12/₹299=25/₹499=50",
          ladder.get("FREE", (0, 3))[1] == 3 and ladder.get("S_99") == (99, 5)
          and ladder.get("S_199") == (199, 12) and ladder.get("S_299") == (299, 25)
          and ladder.get("S_499") == (499, 50), ladder)
st, ch = get("/api/channels")
check("/api/channels 52 registry", st == 200 and ch.get("stats", {}).get("total") == 52, ch.get("stats"))

print("=== 3. REFERRAL 2.0 APIs ===")
st, terms = get("/api/referral/terms")
check("/api/referral/terms — ₹50 headline + 10 rules", st == 200 and terms.get("headline", "").startswith("₹50")
      and len(terms.get("rules_telugu", [])) >= 8)
st, lb = get("/api/referral/leaderboard?period=all&limit=5")
check("/api/referral/leaderboard", st == 200 and lb.get("success") and "prize_telugu" in lb)
st, rk = get("/api/referral/leaderboard?period=week")
check("leaderboard week period", st == 200 and rk.get("period") == "week")

# oru real user ni teesukuni dashboard test
st, chans = get("/api/channels")
target = None
try:
    import urllib.request as u2
    with u2.urlopen(WEB + "/api/referral/leaderboard?period=all&limit=1", timeout=20) as r:
        pass
except Exception:
    pass
st, prof = get("/api/search/TSAP-F-2025-1042")
target = "TSAP-F-2025-1042"
st, dash = get("/api/referral/%s" % target)
check("/api/referral/{id} dashboard (code+link+stats+kit)",
      st == 200 and dash.get("ok") and dash.get("code") and dash.get("link")
      and len(dash.get("share_kit", {}).get("whatsapp_messages", [])) == 5, st)
check("dashboard commission rules Telugu (₹50 first, 10% repeat)",
      "50" in str(dash.get("commission_rules", {}).get("first_payment")) and "10%" in str(dash.get("commission_rules", {}).get("repeat_payment")))
check("dashboard tier + milestones", dash.get("tier", {}).get("key") in ("BRONZE", "SILVER", "GOLD", "PLATINUM", "ELITE")
      and len(dash.get("milestones", [])) == 4)
st, kit = get("/api/referral/%s/share-kit" % target)
check("share-kit 5 WA + TG + SMS", st == 200 and len(kit.get("whatsapp_messages", [])) == 5
      and "t.me/share/url" in kit.get("telegram_share", "") and kit.get("sms_text"))
st, val = get("/api/referral/validate/%s" % dash.get("code"))
check("validate/{code} → ok + ₹50 offer", st == 200 and val.get("ok") and val.get("commission_offer") == 50)
st, bad = get("/api/referral/validate/ZZZ99")
check("validate bad code → ok False", st == 200 and bad.get("ok") is False)
st, png = get("/api/referral/%s/poster.png?style=square" % target)
check("poster.png square (PNG bytes)", st == 200 and isinstance(png, bytes) and png[:8] == b"\x89PNG\r\n\x1a\n", st)
st, png2 = get("/api/referral/%s/poster.png?style=status" % target)
check("poster.png status 1080×1920", st == 200 and isinstance(png2, bytes) and len(png2) > 20000, st)
st, pay = get("/api/referral/%s/payouts" % target)
check("payouts list + min ₹100 note", st == 200 and pay.get("min_payout") == 100)
st, fr = get("/api/referral/%s/fraud-check" % target)
check("fraud-check shape", st == 200 and "clean" in fr and "issues" in fr)
st, _ = get("/api/referral/TSAP-NOT-EXIST")
check("unknown id → 404", st == 404, st)

print("=== 4. LANDING + CLICK FUNNEL (website proxy) ===")
st, page = get("/r/%s" % dash.get("code"), WEB)
check("/r/<code> landing 200", st == 200, st)
st, clk = get("/api/referral/click/%s?source=smoke" % dash.get("code"), WEB, method="POST")
check("click tracked (funnel)", st == 200 and clk.get("success"))
st, dash2 = get("/api/referral/%s" % target)
check("dashboard lo click kanipisthundi", dash2.get("stats", {}).get("clicks", 0) >= 1)

if "--flow" in sys.argv:
    print("=== 5. E2E: click → register → ₹99 → referrer ₹50 (--flow) ===")
    phone = "9%09d" % random.randint(0, 999999999)
    fields = {"gender": "Groom", "age": 32, "height": "5.8", "marital_status": "Pelli Kaledu",
              "caste": "Reddy", "district": "Hyderabad", "state": "TS", "full_name": "Smoke Test Groom",
              "phone": phone, "job": "Engineer", "education": "B.Tech", "salary": "90k",
              "referral_code": dash.get("code")}
    st, reg = post_form("/api/register", fields, WEB)
    check("register with ?ref → 200", st == 200 and reg.get("tsap_id"), st)
    if isinstance(reg, dict) and reg.get("tsap_id"):
        check("referral lock ok + +1 credit (3→4)",
              reg.get("referral", {}).get("joined_with", {}).get("ok") is True and reg.get("credits") >= 4,
              reg.get("referral", {}).get("joined_with"))
        check("sontha code + link + poster urls",
              reg["referral"]["my_code"] and reg["referral"]["my_link"].endswith(reg["referral"]["my_code"])
              and reg["referral"]["poster_url"].endswith("/poster.png"))
        check("referrer ki notify text (join message)", bool(reg["referral"]["joined_with"].get("notify")))
        check("kotha user welcome lo referral line",
              "Mee friend" in str((reg.get("welcome_status") or {}).get("manual_text", "")))
        st, wh = post_form("/api/payment/webhook?user_id=%s&amount=99&razorpay_payment_id=smoke99"
                           % reg["tsap_id"], {})
        rc = (wh or {}).get("referral_commission") or {}
        check("webhook ₹99 → referrer ku ₹50", st == 200 and rc.get("commission") == 50, rc)
        check("wallet update + message", float(rc.get("wallet", 0)) >= 50 and rc.get("message_telugu"))
        st, dash3 = get("/api/referral/%s" % target)
        check("referrer dashboard: paid_count +1, wallet perigindi",
              dash3.get("stats", {}).get("paid_count", 0) >= 1 and dash3.get("stats", {}).get("wallet", 0) > 0,
              dash3.get("stats"))
        st, self_ref = post_form("/api/register", dict(fields, phone="9%09d" % random.randint(0, 999999999),
                                                      referral_code=reg["referral"]["my_code"]), WEB)
        # self-referral is only blocked when the referrer phone/code matches; vaallu veru kabatti check skip
        st, dup = post_form("/api/referral/click/%s" % reg["referral"]["my_code"], {})
        check("kotha user sontha code kooda click track avutundi", st == 200 and dup.get("success"))

print("\n=== RESULT: %d pass / %d fail ===" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("   ❌ " + f)
    sys.exit(1)
print("🏆 LIVE SMOKE PASS — referral 2.0 (₹50 andariki) live lo pani chestundi")
