"""
TSAP Matrimony — FastAPI Backend — Pin-to-Pin Perfect Advanced
All endpoints: Register, ID Search, Matches, Credits, Referral, Bureau, Admin, Payment, Channels auto-post
"""
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Any, Dict, Optional
import os, random, json, re
from datetime import datetime, timedelta

# Import our modules
from models import RegisterRequest, RegisterResponse, SearchResponse, MatchResult
from matching_engine import (
    calculate_match_score, generate_personalized_reasons, find_top_matches,
    generate_profile_highlights,
)
from card_generator import generate_id, create_profile_card
from credits import PLANS, can_view_number, deduct_credit, add_credits, can_search_id
from referral import (
    generate_referral_code, process_referral_payment, get_leaderboard, parse_referral_type,
    ensure_referrer_profile, validate_referral, attach_referral, referral_dashboard,
    share_kit as referral_share_kit,
    payout_request, payout_action, payout_queue, track_click, referral_terms_telugu,
    reverse_referral_payment, load_state as referral_load_state, stats_of as referral_stats_of,
    referrer_join_text, referrer_commission_text, referee_welcome_text,
    mask_payout as referral_mask_payout,
    tier_of as referral_tier_of, MILESTONES as REFERRAL_MILESTONES, TIERS as REFERRAL_TIERS,
)  # noqa: E402
import refpartners as RP19  # noqa: E402  # 🌊 WAVE 19 — referral partners
from vendors import (                                                        # 🏪 vendor ads + promotions
    register_vendor, activate_vendor, reject_vendor, expire_due_vendors, vendors_directory,
    ad_rotation, track_vendor_click, vendor_lead, promo_post, vendor_dashboard,
    vendor_queue, vendor_revenue, packages_public as vendor_packages_public,
    vendor_stats, public_vendor, category_label as vendor_category_label,
    CATEGORIES as VENDOR_CATEGORIES, PACKAGES as VENDOR_PACKAGES, SLOTS as VENDOR_SLOTS,
    load_state as vendors_load_state, save_state as vendors_save_state,
)
from channels_config import (
    CHANNELS, channel_stats, channels_by_tier, route_profile, build_caption,
    build_hashtags, live_channels, pending_channels, all_channels, resolve_caste_key,
    setup_plan as channels_config_setup_plan, caste_split_report, channel_health_report,
)
try:
    from card_pro import create_pro_card, has_telugu_font  # full-detail neat card
except Exception:  # fonts/PIL lekapoyina server padipodu
    create_pro_card = None
    def has_telugu_font():
        return False

import growth
from growth import (namaste_text, admin_new_profile_text, lead_followup_text,
                      track_visit, save_lead, lead_stats, leads_list, share_kit, inventory_status)
from publisher import (dead_letters, requeue_dead,
    enqueue, publish_profile, publish_status, read_log, start_worker, worker_running,
    build_whatsapp_text, build_share_text, config as publish_config,
    enqueue_whatsapp, wa_queue_stats, start_wa_worker, whatsapp_link, WA_QUEUE, WA_DEAD,
)
from wa_antiban import ENGINE as WA_ENGINE
# 🛡️ WAVE 9 — hardening layer (auth tokens, admin key, rate limit, validation, abuse ledger)
from hardening import (
    auth_enforced, require_owner, require_admin, rate_limit_hit, too_many,
    apply_security_headers, posture as security_posture, abuse_snapshot, abuse_log,
    sign_token, verify_token, token_from_request, is_admin, is_automation, clean, req_text,
    require_vendor, vendor_token,
    req_phone, req_int, req_choice, req_bool, validation_error, seen as idem_seen, abuse_count, clamp_int,
    ADMIN_KEY as TSAP_ADMIN_KEY, NAME_RE, PHONE_RE, dev_mode,
)
# ⭐ profiles quality + saved searches + consent ledger + templates
from quality import (
    profile_completeness, trust_score, templates as quality_templates, facets as search_facets,
    save_search, saved_for, delete_search, new_matches_for, mark_alerted, matches_filters,
    log_consent, consent_for, load_saved_searches, load_consent_ledger, CONSENT_LEDGER,
)
from interest import (
    PLANS as INTEREST_PLANS, plan_list, get_plan, plan_by_amount, apply_payment,
    can_send_interest, create_interest, respond_interest, expire_old,
    interest_to_owner_text, interest_accepted_text, interest_declined_text,
    interest_notify_text, inbox_for, sent_for, safe_user,
    MAX_PER_DAY as INTEREST_MAX_PER_DAY, EXPIRY_DAYS as INTEREST_EXPIRY_DAYS,
    mask_phone,
)
from card_generator import generate_id as _gen_id
from porutham import compute_porutham, porutham_line, norm_nakshatra, norm_rasi
import topmatch, safety, preview, bot_pool, wa_pool
import smart12 as S12  # 🔒 WAVE 12: masked captions + unlock/entitlement + ₹500 assisted
import astro as AST      # 🪐 WAVE 13: 36-guna + dosha + jathakam
import ads as ADS        # 📢 WAVE 13: vendor ad campaigns
import matchpro as MP      # 🌊 WAVE 14: age-rule + profession + NRI


def _is_nri(u: Dict) -> bool:  # 🌊 WAVE 14 adapter: stored flag + detect_nri fallback
    try:
        u = u or {}
        if u.get("is_nri"):
            return True
        return bool(MP.detect_nri(str(u.get("country", "")), str(u.get("work_location", "")),
                                   str(u.get("current_city", "")), str(u.get("state", ""))).get("is_nri"))
    except Exception:
        return False


def _prof_label(u: Dict) -> str:  # 🌊 WAVE 14 adapter: job_group → Telugu label
    try:
        return MP.GROUP_TE.get(MP.job_group(u or {}), "")
    except Exception:
        return ""
import paypro as PP        # 🌊 WAVE 14: safe-pay + festival offers
import cms as CMS            # 📝 WAVE 15: pages + stories + banners
import chanmap as CHAN         # 📡 WAVE 15: channel links + import + coverage
from interest import ADDONS, RENEWALS, is_addon, get_addon, get_renewal, plan_list_with_free, addon_list, renewal_offer
from photo_validate import validate_photo  # 🌊 WAVE 17 — photo validation pipeline
from otp_channels import send_otp as otp_channel_send, CHANNEL_TELUGU  # 🌊 WAVE 18 — free OTP
from channels_config import post_targets, caste_channel_links, channel_links, WA_OFFICIAL_LINK
# 🎁 WAVE 10 — register avvagane "3 profiles + caste channel links" WhatsApp ki
from welcome_pack import build_welcome_pack, pack_public, channels_count as wa_links_stats
# 🚀 WAVE 11 — ULTRA ADVANCED (gothram guard, stories, streak, push, voice, gamify, boost)
import advanced11 as A11

app = FastAPI(title="TSAP Matrimony API — Ultra Advanced", version="2.0")

# Card + photo files static ga serve — /cards/{id}.png browser lo direct open avutundi
try:
    from fastapi.staticfiles import StaticFiles
    os.makedirs("/tmp/cards", exist_ok=True)
    os.makedirs("/tmp/photos", exist_ok=True)
    app.mount("/cards", StaticFiles(directory="/tmp/cards"), name="cards")
    app.mount("/photos", StaticFiles(directory="/tmp/photos"), name="photos")
    os.makedirs("/tmp/voice", exist_ok=True)                                        # 🎙️ WAVE 11
    app.mount("/voice", StaticFiles(directory="/tmp/voice"), name="voice")          # 🎙️ WAVE 11
except Exception as _e:
    print("[STATIC] mount skip:", _e)

@app.on_event("startup")
async def _startup_publisher():
    ok = start_worker()
    st = publish_status()
    start_wa_worker()
    wa = st["whatsapp_queue"]["antiban"]
    print(f"[PUBLISHER] worker={ok} | telegram={'ready' if st['telegram']['configured'] else 'dry-run'} "
          f"| whatsapp={st['whatsapp']['mode']} | live_channels={st['telegram']['live_channels']}")
    print(f"[WHATSAPP-ANTIBAN] telegram mundu → whatsapp tarvata | gap={wa['random_gap']} | "
          f"cap={wa['daily_cap']}/day (today {wa['warmup_cap_today']}) | hour {wa['active_hours_ist'][0]}–{wa['active_hours_ist'][1]} IST")
    # demo/launch inventory: empty DB aithe (dev/preview lo) ventane profiles — site khali ga kanipinchadu
    if str(os.getenv("DEMO_SEED_ENABLED", "true")).lower() in ("1", "true", "yes", "on") and not DB_USERS:
        try:
            res = demo_seed()
            print("[DEMO] %d profiles ready: %s" % (len(res["created"]), ", ".join(x["tsap_id"] for x in res["created"])))
        except Exception as e:
            print("[DEMO] seed skip:", str(e)[:100])
        # launch inventory (360 profiles) — LAUNCH_SEED_COUNT env tho control (0 = bandh)
        try:
            n = int(os.getenv("LAUNCH_SEED_COUNT", "60"))
        except Exception:
            n = 60
        if n > 0:
            try:
                import seed_launch_db
                added = 0
                for sd in seed_launch_db.build_profiles(n):
                    phone = str(sd.get("phone", ""))
                    if phone and any(u.get("phone") == phone for u in DB_USERS):
                        continue
                    u = dict(sd)
                    u.setdefault("is_approved", True)
                    u.setdefault("photo_urls", [])
                    u.setdefault("referral_stats", {"total": 0, "earned": 0})
                    u.setdefault("credit_history", [])
                    u["card_url"] = "/cards/" + u["tsap_id"] + ".png"
                    u["phone_encrypted"] = encrypt_phone(phone) if phone else ""
                    DB_USERS.append(u)
                    added += 1
                print("[LAUNCH-DB] %d inventory profiles load ayyayi (total %d) — inventory_status=%.0f%%"
                      % (added, len(DB_USERS), inventory_status(len(DB_USERS))["percent"]))
            except Exception as e:
                print("[LAUNCH-DB] seed skip:", str(e)[:140])

    # 🏪 VENDOR ADS startup — state load + kalam ayyina listings expire + demo vendors
    try:
        _vl = vendors_load_state()
        print("[VENDORS] state load: %s (vendors=%s, leads=%s)"
              % ("ok" if _vl.get("ok") else "new", _vl.get("vendors", 0), _vl.get("leads", 0)))
        _ex = expire_due_vendors()
        if _ex.get("expired"):
            print("[VENDORS] %d listings expire ayyayi" % _ex["expired"])
        if str(os.getenv("DEMO_SEED_ENABLED", "true")).lower() in ("1", "true", "yes", "on") \
                and not [v for v in __import__("vendors").VENDORS if v.get("source") != "demo_seed"]:
            import vendors as _vmod
            _seed = _vmod.demo_seed()
            print("[VENDORS] %d demo vendors + %d leads ready (total %d)"
                  % (len(_seed["created"]), _seed["leads"], _seed["total"]))
    except Exception as e:
        print("[VENDORS] state load fail:", str(e)[:90])

    # 🤝 REFERRAL 2.0 startup: state file load (payouts/clicks restart lo kooda undali)
    try:
        _rl = referral_load_state()
        print("[REFERRAL] state load: %s (payouts=%s, clicks=%s)"
              % ("ok" if _rl.get("ok") else "new", _rl.get("payouts", 0), _rl.get("clicks", 0)))
    except Exception as e:
        print("[REFERRAL] state load fail:", str(e)[:90])
    # 🔑 Pranam prathi user ki UNIQUE referral code (seed data lo duplicates unnayi — 1042 shared by 2 users)
    try:
        for _u in DB_USERS:
            try:
                ensure_referrer_profile(_u, DB_USERS)
            except Exception:
                pass
        _codes = [u.get("referral_code") for u in DB_USERS if u.get("referral_code")]
        _dup = len(_codes) - len(set(_codes))
        print("[REFERRAL] %d users ki unique codes ready (duplicates: %d)" % (len(_codes), _dup))
        if _dup:
            seen, fixed = set(), 0
            for _u in DB_USERS:
                _c = str(_u.get("referral_code", "")).upper()
                if not _c:
                    continue
                if _c in seen:
                    _u["referral_code"] = ""
                    _new = ensure_referrer_profile(_u, DB_USERS)["code"]
                    print("[REFERRAL] duplicate fix: %s → %s" % (_c, _new))
                    _c = _new
                    fixed += 1
                seen.add(_c)
            print("[REFERRAL] duplicates fixed: %d" % fixed)
    except Exception as e:
        print("[REFERRAL] code assign fail:", str(e)[:90])

# ---------------------------------------------------------------------------
# VISIT TRACKING MIDDLEWARE — "site ki vachina vallu antha DB lo save avvali"
#    (page + API calls anni anonymous ga log: path, referrer, device, channel)
# ---------------------------------------------------------------------------
_SKIP_TRACK = ("/_next", "/static", "/favicon", "/cards/", "/photos/", "/health", "/robots", "/sitemap")


@app.middleware("http")
async def _track_visits_middleware(request: Request, call_next):
    try:
        path = request.url.path
        is_trackable = (request.method == "GET" and path not in ("", "/")
                        and not any(path.startswith(x) for x in _SKIP_TRACK))
        if is_trackable:
            fwd = request.headers.get("x-forwarded-for", "")
            ip = (fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else ""))
            ua = request.headers.get("user-agent", "")
            ref = request.headers.get("referer", "")
            utm = request.url.query if "utm_" in str(request.url.query) else ""
            track_visit(ip, ua, path, ref, utm)
    except Exception:
        pass  # tracking eppudu main request ni aapakudadu
    return await call_next(request)


@app.middleware("http")
async def _security_middleware(request: Request, call_next):
    """
    🛡️ rate limit (abuse) + security headers + docs lock + no-store (PII cache leak fix).

    🐞 FIX (S06): /docs + /openapi.json production lo open ga unnayi (anni endpoints + models
    bayata kanipisthunnayi). Ippudu: dev/test lo matrame open, prod lo admin key tho matrame —
    lekapote 404 (info disclosure closed).
    🐞 FIX (S07): private API responses ki Cache-Control: no-store (proxy/browser lo PII cache avvakunda).
    """
    _priv = (request.url.path.startswith(("/api/interest", "/api/credits", "/api/views", "/api/saved",
                                          "/api/blocks", "/api/referral", "/api/leads", "/api/admin",
                                          "/api/verification", "/api/consent", "/api/auth"))
             or bool(request.headers.get("x-tsap-token")) or bool(request.headers.get("x-admin-key")))
    try:
        if request.method == "POST":
            limited = rate_limit_hit(request)
            if limited:
                resp = too_many(limited)
                apply_security_headers(resp.headers)
                return resp
    except Exception:
        pass
    if request.url.path in ("/docs", "/redoc", "/openapi.json") and not dev_mode() and not is_admin(request):
        resp = JSONResponse(status_code=404, content={
            "success": False, "error": "docs_disabled",
            "message_telugu": "🔒 API docs public ga ledu — admin key (X-Admin-Key) tho matrame chudochu"})
        apply_security_headers(resp.headers)
        return resp
    response = await call_next(request)
    try:
        apply_security_headers(response.headers)
        if _priv and request.method == "GET":
            response.headers.setdefault("Cache-Control", "no-store, no-cache, must-revalidate, private")
        if (request.headers.get("x-forwarded-proto") or "").lower() == "https":
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    except Exception:
        pass
    return response


# 🛡️ CORS FIX: mundu "*" + credentials (browser security hole). Ippudu env allowlist + preview regex.
_CORS_ORIGINS = [o.strip() for o in (os.getenv("CORS_ORIGINS") or
                "https://manavivaha.in,https://www.manavivaha.in,http://localhost:3000,"
                "http://127.0.0.1:3000,http://localhost:8000").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_CORS_ORIGINS,
    allow_origin_regex=r"https://([a-z0-9-]+\.)?(e2b\.app|e2b\.dev|manavivaha\.in)$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# In-memory DB (real lo Postgres)
DB_USERS = []
DB_INTERESTS = []
DB_VIEWS = []          # {"tsap_id": who got viewed, "viewer_id": who viewed, "at": iso}
DB_SAVES = []          # shortlist: {"tsap_id": owner, "saved_id": saved profile, "at": iso}
DB_DIGEST = []         # daily digest log
DB_OTPS = {}           # {"98480xxxxx": {"code": "1234", "expires": iso, "tries": n}}
VERIFIED_PHONES = set()  # OTP verify ayyina numbers
DB_REPORTS = safety.DB_REPORTS      # safety reports (moderation queue)
DB_BLOCKS = safety.DB_BLOCKS        # block list (search/interest lo respect avutundi)
DB_PAYMENTS = []
DB_POSTS = []
DB_REFERRALS = []

# Helper — unique TSAP ID (same number rendu sarlu raakudadu)
def unique_tsap_id(gender: str, year: int = 2025) -> str:
    for _ in range(50):
        tid = generate_id(gender, year, random.randint(1000, 9999))
        if not any(u.get("tsap_id") == tid for u in DB_USERS):
            return tid
    return generate_id(gender, year, random.randint(10000, 99999))


def verify_webhook_signature(header_sig: str, secret: str, payload: str = "") -> bool:
    """
    🐞 FIX (B02): Razorpay webhook HMAC-SHA256 — **raw body** pai verify (timing-safe).
    Mundu `payload or header_sig` hash cheyyadam valla verification always fail/wrong ayye
    (+ main.py lo `request` param lekapote NameError silent ga swallow avvadam valla check dead code).
    """
    import hmac as _hmac, hashlib as _hashlib
    if not secret or not header_sig or payload in (None, "", b""):
        return False
    try:
        raw = payload.encode("utf-8") if isinstance(payload, str) else bytes(payload)
        if not raw:
            return False
        expected = _hmac.new(secret.encode("utf-8"), raw, _hashlib.sha256).hexdigest()
        return _hmac.compare_digest(str(header_sig).strip().lower(), expected.lower())
    except Exception:
        return False


def _mask_queue_result(res: Dict[str, Any], phone: str = "") -> Dict[str, Any]:
    """
    🔒 Queue result lo raw phone numbers vaddhu (owner endpoint/register response lo kooda mask).
    numbers policy: mask_phone('9848012345') → '98••••••45'
    """
    out = dict(res or {})
    if phone:
        out.pop("manual_text_phone", None)
    for key in ("targets",):
        if isinstance(out.get(key), list):
            out[key] = [mask_phone(str(x)) for x in out[key]]
    if out.get("target"):
        out["target"] = mask_phone(str(out["target"]))
    inner = out.get("wa_result")
    if isinstance(inner, dict):
        out["wa_result"] = _mask_queue_result(inner, phone)
    return out


def mask_pii(obj):
    """Public responses lo 10-digit numbers ni mask (values + dict KEYS + strings) — PII fix."""
    if isinstance(obj, dict):
        import re as _re
        out = {}
        for k, v in obj.items():
            _k = str(k)
            if _re.fullmatch(r"(?:\+?91)?[6-9]\d{9}", _k):
                _k = mask_phone(_k[-10:])
            out[_k] = mask_pii(v)
        return out
    if isinstance(obj, list):
        return [mask_pii(v) for v in obj]
    if isinstance(obj, str):
        import re as _re
        return _re.sub(r"(?<!\d)(?:\+?91[-\s]?)?([6-9]\d{9})(?!\d)", lambda m: mask_phone(m.group(1)), obj)
    return obj


def _score_pair(a: Dict, b: Dict) -> tuple:
    """Match score + Telugu reasons — missing fields unna safe ga (crash avvadu)."""
    def norm(u: Dict) -> Dict:
        d = dict(u or {})
        d.setdefault("gender", "Bride")
        d.setdefault("age", 25)
        d.setdefault("caste", "—")
        d.setdefault("education", "—")
        d.setdefault("job", "—")
        d.setdefault("height", '5\'5"')
        d.setdefault("star", "")
        d.setdefault("district", d.get("current_city", "—"))
        d.setdefault("state", "TS")
        d.setdefault("mandal", d.get("district", ""))
        d.setdefault("marital_status", "Pelli Kaledu")
        return d
    try:
        na, nb = norm(a), norm(b)
        sc = calculate_match_score(na, nb)
        rs = generate_personalized_reasons(na, nb, sc)
        return sc, rs
    except Exception as e:
        return 0, []


def encrypt_phone(phone: str) -> str:
    # Mock encrypt — real lo AES
    return f"enc_{phone[-4:]}"

@app.get("/")
def root():
    return {"message": "TSAP Matrimony API — Ultra Advanced, Deep, Never Before 🔥", "status": "LIVE", "version": "2.0", "chatting": False, "model": "Interest request + WhatsApp profile share",
            "endpoints": ["/api/register","/api/search/{id}","/api/matches/{id}","/api/plans","/api/credits/{id}",
                          "/api/credits/buy","/api/interest/send","/api/interest/inbox/{id}","/api/interest/sent/{id}",
                          "/api/interest/respond","/api/interest/status/{id}","/api/wa/status","/api/wa/pause","/api/wa/resume",
                          "/api/payment/webhook","/api/channels","/api/publish/status","/api/publish/log"]}

@app.post("/api/register", response_model=RegisterResponse)
async def register(
    gender: str = Form(...),
    age: int = Form(...),
    height: str = Form(...),
    marital_status: str = Form(...),
    children: str = Form("None"),
    caste: str = Form(...),
    sub_caste: str = Form(""),
    gothram: str = Form(""),
    star: str = Form(""),
    education: str = Form(...),
    job: str = Form(...),
    salary: str = Form(...),
    state: str = Form(...),
    district: str = Form(...),
    mandal: str = Form(""),
    phone: str = Form(...),
    password: str = Form(""),
    referral_code: str = Form(""),
    photo_private: bool = Form(False),
    expectations: str = Form(""),
    # Advanced fields - optional for backward compat
    full_name: str = Form(""),
    dob: str = Form(""),
    dob_correct: bool = Form(False),
    birth_time: str = Form(""),
    father_name: str = Form(""),
    mother_name: str = Form(""),
    father_occupation: str = Form(""),
    mother_occupation: str = Form(""),
    native_place: str = Form(""),
    education_detail: str = Form(""),
    work_location: str = Form(""),
    about_myself: str = Form(""),
    current_city: str = Form(""),
    email: str = Form(""),
    rasi: str = Form(""),
    dosham: str = Form("No"),
    family_type: str = Form("Nuclear"),
    company: str = Form(""),
    # Expectations builder
    exp_age_min: str = Form(""),
    exp_age_max: str = Form(""),
    exp_job: str = Form(""),
    exp_location: str = Form(""),
    exp_caste: str = Form(""),
    # Advanced optional — form anni fields API ki vellali (lekapothe card lo blank vasthundi)
    weight: str = Form(""),
    blood_group: str = Form(""),
    mother_tongue: str = Form("Telugu"),
    physical_status: str = Form("Normal"),
    body_type: str = Form("Average"),
    complexion: str = Form("Fair"),
    family_values: str = Form("Traditional"),
    family_status: str = Form("Middle Class"),
    brothers: str = Form(""),
    brothers_married: str = Form(""),
    sisters: str = Form(""),
    sisters_married: str = Form(""),
    moola_nakshatram: str = Form("No"),
    religion: str = Form("Hindu"),
    country: str = Form(""),
    college: str = Form(""),
    experience: str = Form(""),
    work_type: str = Form(""),
    pincode: str = Form(""),
    photo_url: str = Form(""),        # uploaded photo ka URL (S3/static)
    upload_token: str = Form(""),
    phone_verified: bool = Form(False),
):
    """
    Pin-to-Pin Register Flow:
    1. Validate OTP (mock)
    2. Generate ID: TSAP-M-2025-XXXX
    3. Encrypt phone, save DB
    4. Generate card (Pillow)
    5. Referral code generate for this user
    6. Auto-post queue: Main 4 + Caste + Special
    7. Find Top 3 FREE matches (score 70%+ + reasons)
    8. Return ID + card + matches
    """
    # 1. Validate — 🛡️ WAVE 9 strict (mundu age check tappa em ledu → 500s, XSS, junk rows)
    gender = req_choice(gender, "gender", ["Bride", "Groom", "Male", "Female"])
    gender = {"Male": "Groom", "Female": "Bride"}.get(gender, gender)
    age = req_int(age, "age", 21 if gender == "Groom" else 18, 70)
    phone = req_phone(phone, "phone")
    password = (password or "").strip()
    if password and len(password) < 6:   # 🌊 WAVE 18 — number+password login
        raise HTTPException(400, "🔑 Password minimum 6 characters (letters + number best)")
    if len(password) > 72:
        raise HTTPException(400, "🔑 Password maximum 72 characters")
    full_name = req_text(full_name, "full_name", 2, 60, required=True,
                         pattern=NAME_RE, pattern_msg="⚠️ Name lo letters matrame (2-60 chars)")
    marital_status = req_choice(marital_status, "marital_status",
                                # 🌊 WAVE 16 canonical + legacy (UI: Never married/Widow/Widower/Divorced/Awaiting Divorce)
                                ["Pelli Kaledu", "Widow", "Widower", "Divorced", "Awaiting Divorce",
                                 "Separated", "Vidakuulu", "Widow/Widower", "Handicapped"])
    children = req_choice(children, "children", ["None", "1", "2", "3", "4+"], required=False, default="None")
    if marital_status == "Pelli Kaledu":
        children = "None"                       # never-married → smart force (junk reject)
    caste = req_text(caste, "caste", 2, 40)
    height = req_text(height, "height", 1, 12)
    education = req_text(education, "education", 1, 60)
    job = req_text(job, "job", 1, 60)
    salary = req_text(salary, "salary", 1, 24)
    state = req_choice(state, "state", ["TS", "AP", "KA", "MH", "Other"])
    district = req_text(district, "district", 2, 40)
    family_status = req_choice(family_status, "family_status",
                               # 🌊 WAVE 17 canonical (screenshot) + legacy (old data/tests)
                               ["Middle Class", "Upper Middle Class", "Rich / Affluent (Elite)",
                                "Lower Middle", "Middle class", "Upper middle class", "Upper Middle",
                                "Rich", "Affluent"],
                               required=False, default="Middle Class")
    _fam_map = {"Lower Middle": "Middle Class", "Middle class": "Middle Class",
                "Upper middle class": "Upper Middle Class", "Upper Middle": "Upper Middle Class",
                "Rich": "Rich / Affluent (Elite)", "Affluent": "Rich / Affluent (Elite)"}
    family_status = _fam_map.get(family_status, family_status)
    _about = (about_myself or "").strip()
    # NOTE: empty allowed at API level (old clients/tests compat) — frontend form lo MANDATORY + counter.
    if _about and len(_about) < 50:
        raise HTTPException(400, "⚠️ About yourself — minimum 50 characters (మీ గురించి కనీసం 50 అక్షరాలు రాయండి)")
    if re.search(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)", _about) or ("@" in _about and "." in _about.split("@")[-1]):
        raise HTTPException(400, "🔒 About lo phone number / email pettakandi — privacy kosam numbers ivvamu (interest accept ayithe matrame exchange)")
    email = req_text(email, "email", 0, 80, required=False)
    country = req_text(country, "country", 0, 60, required=False) or "India"
    if age < 18: raise HTTPException(400, "Age must be 18+ (Bride) / 21+ (Groom)")

    # 2. ID Gen
    tsap_id = unique_tsap_id(gender, 2025)
    # referral code — TSAP ID nunchi derive (unique, deterministic) [FIX: mundu undefined `seq` tho crash avutundi]
    _dup_phone = any(u.get("phone") == phone for u in DB_USERS)
    if _dup_phone:
        abuse_log("duplicate_phone_register", tsap_id)
        abuse_count("duplicate_phone_registers")
    _ref_seq = "".join(ch for ch in tsap_id if ch.isdigit())[-5:] or str(random.randint(10000, 99999))
    my_ref_code = f"TSAP-REF-{_ref_seq}"

    # 3. Save DB - Advanced Full
    user = {
        "tsap_id": tsap_id,
        "full_name": full_name or f"{gender} User",
        "gender": gender,
        "dob": dob,
        "dob_correct": dob_correct,
        "birth_time": birth_time,
        "age": age,
        "height": height,
        "marital_status": marital_status,
        "children": children,
        "caste": caste,
        "sub_caste": sub_caste,
        "gothram": gothram,
        "star": star,
        "rasi": rasi,
        "dosham": dosham,
        "education": education,
        "education_detail": education_detail,
        "job": job,
        "company": company,
        "salary": salary,
        "work_location": work_location,
        "about_myself": about_myself,
        "father_name": father_name,
        "mother_name": mother_name,
        "father_occupation": father_occupation,
        "mother_occupation": mother_occupation,
        "family_type": family_type,
        "native_place": native_place,
        "weight": weight,
        "blood_group": blood_group,
        "mother_tongue": mother_tongue,
        "physical_status": physical_status,
        "body_type": body_type,
        "complexion": complexion,
        "family_values": family_values,
        "family_status": family_status,
        "brothers": brothers,
        "brothers_married": brothers_married,
        "sisters": sisters,
        "sisters_married": sisters_married,
        "moola_nakshatram": moola_nakshatram,
        "religion": religion,
        "country": country,
        "is_nri": _is_nri({"state": state, "country": country, "work_location": work_location, "current_city": current_city}),
        "college": college,
        "experience": experience,
        "work_type": work_type,
        "pincode": pincode,
        "state": state,
        "district": district,
        "mandal": mandal,
        "current_city": current_city,
        "email": email,
        "phone_encrypted": encrypt_phone(phone),
        "phone_last4": phone[-4:],
        "phone": phone,
        "password_hash": _hash_password(password) if password else "",
        "referral_code": my_ref_code,
        "referred_by": "",                    # attach_referral() validate chesi lock chestundi (kinda)
        "referred_by_raw": referral_code,     # form lo vachina code (audit)
        "photo_urls": ([photo_url] if photo_url else []),   # FIX: fake path valla photo_only filter ellappudu match ayyedi
        "card_url": f"/cards/{tsap_id}.png",   # web URL (card files static mount lo undi)
        "is_verified": False,
        "phone_verified": bool(phone_verified) or (phone in VERIFIED_PHONES),
        "is_approved": False,
        "privacy_mode": "private" if photo_private else "public",
        "credits": 3,
        "plan": "FREE",
        "created_at": datetime.utcnow().isoformat(),
        "wallet": 0,
        "referral_stats": {"total":0, "paid_count":0},
        "expectations": expectations,
        "exp_filters": {"ageMin": exp_age_min, "ageMax": exp_age_max, "job": exp_job, "location": exp_location, "caste": exp_caste},
    }
    # 3b. Card/caption lo chupinchE personalized highlights + completeness score
    user["reasons"] = generate_profile_highlights(user)
    filled = [k for k, v in user.items() if v not in ("", None, [], 0) and not k.startswith("_")]
    user["completeness"] = min(100, int(len(filled) * 100 / max(1, len(user))))
    user["score"] = max(70, min(99, 70 + int(user["completeness"] * 0.3)))
    DB_USERS.append(user)

    # 4. Card Gen — FULL DETAIL NEAT CARD (Pillow). Fail ayithe path matrame istundi.
    card_path = f"/tmp/cards/{tsap_id}.png"          # filesystem (internal use)
    card_url = f"/cards/{tsap_id}.png"               # web URL (browser/Telegram lo open avutundi)
    try:
        if create_pro_card:
            os.makedirs("/tmp/cards", exist_ok=True)
            # photo upload ayyindi unte card lo real photo (face crop) vestham
            if photo_url:
                user["photo_path"] = photo_url if os.path.isabs(photo_url) else photo_url.replace("/photos/", "/tmp/photos/")
            create_pro_card(user, card_path)
            user["card_generated"] = True
            user["card_url"] = card_url
    except Exception as e:
        user["card_generated"] = False
        user["card_error"] = str(e)[:160]

    # 5. 🤝 REFERRAL 2.0 — validate + lock + referee bonus credit (self-referral block kooda)
    referral_result = {"ok": False, "reason": "no_code"}
    if referral_code:
        try:
            referral_result = attach_referral(user, referral_code, DB_USERS)
        except Exception as e:
            referral_result = {"ok": False, "reason": "error", "error": str(e)[:120]}
    # ee user ki sontha referral code (share cheyyadaniki)
    my_referral = ensure_referrer_profile(user, DB_USERS)
    user["referred_by_final"] = user.get("referred_by") or referral_code

    # 5b. 🔔 Referrer ki instant WhatsApp update — "mee friend join ayyaru" (loop close)
    referral_notify = {"referrer_notified": False}
    if referral_result.get("ok"):
        try:
            _ref_user = next((u for u in DB_USERS
                              if str(u.get("referral_code", "")).upper() == str(referral_result.get("referrer_code", "")).upper()
                              or u.get("tsap_id") == referral_result.get("referrer_id")), None)
            if _ref_user:
                _ref_phone = str(_ref_user.get("phone") or "").strip()
                _txt = referrer_join_text(_ref_user, user)
                referral_notify["referrer_name"] = _ref_user.get("full_name", "")
                if _ref_phone and publish_config()["wa_mode"] != "off":
                    _q = enqueue_whatsapp([_ref_phone], _txt, priority=0, kind="referral_join")
                    referral_notify["referrer_notified"] = bool(_q.get("queued"))
                else:
                    referral_notify["manual_text"] = _txt
                    referral_notify["note"] = "WhatsApp bridge connect ayyaka automatic ga veltundi"
            referral_result["notify"] = referral_notify
        except Exception as e:
            referral_result["notify_error"] = str(e)[:120]

    # 6. Auto-post queue — ADVANCED ROUTER (region + religion + caste + specials)
    route = route_profile({
        "gender": gender, "state": state, "caste": caste, "age": age,
        "marital_status": marital_status, "job": job, "education": education,
        "district": district, "photo_private": photo_private,
    })
    auto_queue = route["usernames"]
    user["auto_post_channels"] = auto_queue
    user["auto_post_reasons"] = route["reasons"]
    user["post_hashtags"] = route["hashtags"]

    # 6b. AUTO-PUBLISH — Telegram + WhatsApp (queue, register response block avvadu)
    pub = {"queued": False, "targets": []}
    if publish_config()["auto_post_on_register"]:
        pub = enqueue(user, tsap_id, score=int(user.get("score", 92)),
                      photo_path=card_path if user.get("card_generated") else None)
        user["publish_targets"] = pub["targets"]

    # 6c. NAMASTE WELCOME AUTOMATION — MANA WhatsApp nunchi user ki card + full details
    #     (register avvagane pothundi — user ki "profile vellinda?" ani doubt undadu)
    welcome = {"queued": False, "admin_alert": False}
    try:
        cfg_wa = publish_config()
        if cfg_wa["wa_mode"] != "off" and phone:
            _welcome_msg = namaste_text(user, tsap_id)
            if referral_result.get("ok"):
                # referral tho vachina user ki extra line (friend peru + mee sontha code)
                _ref_user2 = next((u for u in DB_USERS if u.get("tsap_id") == referral_result.get("referrer_id")), None)
                if _ref_user2:
                    _welcome_msg = _welcome_msg + "\n\n" + referee_welcome_text(user, _ref_user2)
            w1 = enqueue_whatsapp([phone], _welcome_msg, image_path=card_path,
                                  priority=0, kind="namaste_welcome")
            welcome["queued"] = bool(w1.get("queued"))
            welcome["wa_result"] = w1
            admin_no = os.getenv("ADMIN_WHATSAPP_NUMBER", "").strip()
            if admin_no:
                w2 = enqueue_whatsapp([admin_no], admin_new_profile_text(user, tsap_id, source="website"),
                                      image_path=card_path, priority=1, kind="admin_new_profile")
                welcome["admin_alert"] = bool(w2.get("queued"))
        elif phone:
            _mt = namaste_text(user, tsap_id)
            if referral_result.get("ok"):
                _ref_user3 = next((u for u in DB_USERS if u.get("tsap_id") == referral_result.get("referrer_id")), None)
                if _ref_user3:
                    _mt = _mt + "\n\n" + referee_welcome_text(user, _ref_user3)
            welcome["manual_text"] = _mt
            welcome["note"] = "WHATSAPP_MODE=bridge chesi bridge connect cheyyandi — automatic ga veltundi"
        user["welcome_status"] = welcome
    except Exception as e:
        welcome["error"] = str(e)[:140]

    # 6d. VISITOR -> LEAD conversion (register chesinappudu lead ni close cheyyali)
    try:
        ok_lead, _kind, _lead = save_lead(user.get("full_name", ""), phone, gender=gender,
                                          district=district, caste=caste, age=str(age),
                                          source="register")
        if ok_lead and _lead:
            _lead["status"] = "converted"
            _lead["tsap_id"] = tsap_id
            user["lead_id"] = _lead["id"]
    except Exception:
        pass

    # 7. Top 3 matches (from existing DB)
    opposite = "Bride" if gender=="Groom" else "Groom"
    candidates = [u for u in DB_USERS if u["gender"]==opposite and u["tsap_id"]!=tsap_id]
    # 🐞 FIX (WAVE 10): mundu candidates[:20] + score>=70 filter valla konni sarlu 2 profiles
    #    matrame vachedi — kaani user ki **eppudu 3 profiles** vellali ("3 profiles FREE" promise).
    #    Ippudu: 60 candidates score chesi, top-3 theesukuntam (70+ lekapote best available tho fill).
    _scored = []
    for _idx, cand in enumerate(candidates[:60]):
        _sc = calculate_match_score(user, cand, user_wants_same_caste=True)
        _scored.append((_sc, _idx, cand))
    _scored.sort(key=lambda t: t[0], reverse=True)
    _picked = [t for t in _scored if t[0] >= 70][:3]
    if len(_picked) < 3:                      # fill — user ki 3 profiles eppudu chupinchali
        _seen_idx = {t[1] for t in _picked}
        _picked += [t for t in _scored if t[1] not in _seen_idx][:3 - len(_picked)]
    top_matches = []
    for _sc, _idx, cand in _picked:
        _reasons = generate_personalized_reasons(user, cand, _sc) or [
            f"Explore — {cand.get('district', '')} {opposite} profile, mee criteria ki daggaraga undi"]
        top_matches.append(MatchResult(matched_user_id=cand["tsap_id"], score=_sc, reasons=_reasons))

    # 7b. 🎁 WELCOME PACK — "register avvagane mee WhatsApp ki 3 profiles + caste channel links"
    #     (numbers 🔒 — profile links + caste Telegram/WhatsApp channel links matrame)
    _cand_map = {c["tsap_id"]: c for c in candidates}
    _pack_matches = [{"profile": _cand_map.get(m.matched_user_id, {}), "score": m.score, "reasons": m.reasons}
                     for m in top_matches]
    welcome_pack = build_welcome_pack(user, tsap_id, _pack_matches)
    pack_queue: Dict[str, Any] = {"queued": False, "kind": "welcome_pack_3profiles"}
    try:
        _cfg_wa3 = publish_config()
        if _cfg_wa3["wa_mode"] != "off" and phone:
            _wq = enqueue_whatsapp([phone], welcome_pack["message_text"], priority=0,
                                   kind="welcome_pack_3profiles")
            pack_queue["queued"] = bool(_wq.get("queued"))
            pack_queue["wa_result"] = _wq
            pack_queue["note_telugu"] = ("✅ Register ayina ventane mee WhatsApp ki 3 profiles + "
                                         "mee caste channel links (Telegram + WhatsApp) veltayi")
        else:
            pack_queue["note_telugu"] = ("WHATSAPP_MODE=bridge chesi bridge connect cheyyandi — appudu "
                                         "register ayina ventane 3 profiles + caste channel links veltayi")
            pack_queue["manual_text"] = welcome_pack["message_text"]
    except Exception as _e:
        pack_queue["error"] = str(_e)[:140]
    pack_queue = _mask_queue_result(pack_queue, phone)   # 🔒 response lo raw phone vaddhu (mask matrame)
    welcome_pack["queue"] = pack_queue
    user["welcome_pack_queue"] = pack_queue

    # 🛡️ sanitize free-text (XSS / control chars / huge payload fix)
    for _k, _n in (("full_name", 60), ("about_myself", 600), ("about_family", 400), ("expectations", 400),
                   ("father_name", 60), ("mother_name", 60), ("father_occupation", 60), ("mother_occupation", 60),
                   ("native_place", 60), ("college", 80), ("company", 80), ("education_detail", 120),
                   ("work_location", 60), ("current_city", 40), ("pincode", 6), ("blood_group", 8),
                   ("weight", 12), ("experience", 12), ("exp_job", 60), ("exp_location", 60), ("exp_caste", 40),
                   ("mandal", 40), ("gothram", 40), ("sub_caste", 40), ("star", 30), ("rasi", 30)):
        if _k in user:
            user[_k] = clean(user.get(_k), _n, "register:" + _k)
    user["duplicate_phone"] = bool(_dup_phone)      # policy (v2.1): same phone multi-account OK — flag matrame
    user["auth_token"] = sign_token(tsap_id)        # 🔐 private API ki login token
    user["quality"] = profile_completeness(user)
    _ref_bonus = int(referral_result.get("bonus_credits", 0)) if referral_result.get("ok") else 0
    _base_credits = 3 if user.get("credits", 3) == 3 else max(3, int(user.get("credits", 3)))
    _credits = _base_credits + (_ref_bonus if _ref_bonus and user.get("credits", 3) == 3 else 0)
    user["credits"] = max(int(user.get("credits", 3)), _credits)
    return RegisterResponse(
        tsap_id=tsap_id,
        auth_token=user.get("auth_token", ""),
        phone_masked=mask_phone(phone),
        duplicate_phone=bool(user.get("duplicate_phone")),
        quality=profile_completeness(user),
        message_plan_telugu=("🆓 FREE: 3 profiles + 3 requests · 🔒 Phone numbers ivvamu — interest accept "
                             "ayithe matrame numbers exchange (consent) · Paid: ₹99→5 profiles"),
        card_url=user.get("card_url", card_url),
        credits=user.get("credits", 3),
        message_telugu=("🎉 Congratulations! Me ID: %s. Me profile admin approve lo undi (2 min). Top 3 FREE matches ready!%s"
                        % (tsap_id, (" Mee friend code tho +%d FREE credit vachindi 🎁" % _ref_bonus) if _ref_bonus else "")),
        next_steps=["Admin approve (2 min)", "Top 3 FREE with reason",
                    "₹99 pay → 5 profiles + boost (modati 3 FREE)",
                    "🤝 Referral: friend pay chesthe meeku ₹50 — /referral lo mee link"],
        auto_post_queue=auto_queue,
        top_3_matches=top_matches,
        publish_queued=pub.get("queued", False),
        publish_targets=pub.get("targets", []),
        namaste_queued=bool(welcome.get("queued") or welcome.get("manual_text")),
        welcome_status=welcome,
        welcome_pack=pack_public(welcome_pack),
        share_kit=share_kit(user, tsap_id),
        share_text=build_share_text(user, tsap_id),
        referral={
            "my_code": user.get("referral_code", ""),
            "my_alias": user.get("referral_alias", ""),
            "my_link": user.get("referral_link", ""),
            "joined_with": referral_result,
            "commission_offer": 50,
            "earn_telugu": "🏆 Mee friend ₹99 pay chesthe meeku ₹50 wallet lo — prathi friend ki (limit ledu)!",
            "rule_telugu": ["Friend ee link tho register avvali", "Vaallu modati sari ₹99+ pay cheyyal",
                            "Meeku ventane ₹50 wallet lo + tier perigithe extra %"],
            "poster_url": "/api/referral/%s/poster.png" % tsap_id,
            "poster_status_url": "/api/referral/%s/poster.png?style=status" % tsap_id,
            "share_message": (
                "🙏 Namaste! Nenu %s — Mana Vivaha (TSAP) matrimony lo profile pettanu.\n"
                "Mee family/relatives/business circle lo pelli chusukune vaallaki ee link pampandi 👇\n%s\n"
                "Free registration + 3 matches FREE. Naa code: %s\n— Mana Vivaha · manavivaha.in"
                % (user.get("full_name") or tsap_id, user.get("referral_link", ""), user.get("referral_code", ""))),
            "dashboard": "/referral",
        },
    )

@app.get("/api/free-plan")
def free_plan_clarity():
    """
    🆓 FREE vs PAID — crystal clear (Telugu).
    "3 profiles istham kaani numbers ivvamu — vaallu pay chesaka numbers/contact"
    """
    free = plan_by_code("FREE") if "plan_by_code" in dir() else None
    return {
        "success": True,
        "headline_telugu": "Register 100% FREE — 3 profiles chudochu & 3 requests pampochu. **Numbers matram ivvamu** 🙅",
        "rule_telugu": "Numbers (phone) eppudu direct ga ivvamu. Interest pampinchi vaallu ACCEPT cheste — appudu rendu vaipula numbers WhatsApp lo exchange avutayi. Leda paid plan thisukoni ekkuva requests + priority thisukovachu.",
        "free": {
            "price": 0,
            "profiles": 3,
            "requests": 3,
            "numbers": "❌ ivvamu (locked)",
            "photo": "blur (privacy mode unna profiles)",
            "chat": "ledu (chatting ledu — requests matrame)",
            "validity": "365 days",
            "getting_started": ["Register (2 నిమిషాల form)", "Profile card free ga generate avutundi",
                                "3 profiles chudochu — 🔒 numbers locked",
                                "3 interests pampochu (vaallaki mana WhatsApp nunchi mee profile veltundi)",
                                "Vaallu accept cheste → numbers exchange (WhatsApp lo)"],
        },
        "paid": [
            {"code": "S_29", "price": 29, "profiles": 1, "telugu": "₹29 → 1 profile extra (trial)"},
            {"code": "S_99", "price": 99, "profiles": 5, "telugu": "₹99 → 5 profiles + boost (modati plan — ivide best seller)"},
            {"code": "S_199", "price": 199, "profiles": 12, "telugu": "₹199 → 12 profiles + per-profile ₹17"},
            {"code": "S_299", "price": 299, "profiles": 25, "telugu": "₹299 → 25 profiles + boost"},
            {"code": "S_499", "price": 499, "profiles": 50, "telugu": "₹499 → 50 profiles (VIP)"},
        ],
        "numbers_rule_telugu": [
            "🔒 Free lo numbers kanipinchavu — 'contact locked' ani matrame kanipisthundi (98••••••45 style)",
            "💌 Interest pampandi → vaallaki mana WhatsApp nunchi mee profile + photo veltundi",
            "✅ Vaallu accept cheste → mogudu/pellam vaipula numbers WhatsApp lo exchange (consent tho)",
            "❌ Chatting ledu — manam chat platform kaadu (spam undadu, complaint undadu)",
            "🔁 Decline ayithe mee credit refund avutundi (loss ledu)",
        ],
        "why_telugu": [
            "📵 Number public ga unte spam/broker calls vastayi — andukane lock",
            "🛡️ Rendu vaipula interest unte matrame contact — aa tarvata mee istam",
            "💯 Mee number DB lo encrypted ga untundi (phone_encrypted)",
        ],
        "faq_telugu": [
            {"q": "3 profiles FREE ante enti?", "a": "Register ayyaka 3 interest requests pampochu — prathi request ki oka profile. Numbers matram lock."},
            {"q": "Numbers eppudu vastayi?", "a": "Vaallu accept chesina tarvata (rendu vaipula ishtam) — leda paid plan tho ekkuva profiles chusi interest pampandi."},
            {"q": "₹99 enduku ivvali?", "a": "3 FREE taruvata ekkuva profiles + boost + priority. Decline ayithe credit refund — loss ledu."},
            {"q": "Mee number evariki telustundi?", "a": "Mee consent tho okka person ki matrame (accept chesina vaallaki). Admin ki audit purpose ki telustundi."},
        ],
        "cta": {"register": "/register", "pricing": "/pricing", "requests": "/requests", "demo": "/matches"},
        "instructions_telugu": "Mee profile lo number ivvakapoyina parvaledu — register FREE. Match ayye vaallaki mana WhatsApp nunchi pampistham.",
    }


@app.get("/api/search/{tsap_id}")
def search_profile(tsap_id: str, viewer_id: Optional[str] = None):
    """
    ID Search — Always Open (even if credits 0)
    Pin-to-Pin:
    - Search by TSAP-1042
    - Profile open, photo blur if FREE, clear if paid
    - Number needs credit
    - Reason generator
    """
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user:
        # 🐞 FIX: mundu tappu ID ki FAKE profile (phone tho) return ayyedi — ippudu honest 404
        raise HTTPException(404, f"TSAP ID dorakaledu: {tsap_id} — ID correct ga unda check cheyyandi")

    viewer = next((u for u in DB_USERS if u["tsap_id"]==viewer_id), {"credits":3, "plan":"FREE"}) if viewer_id else {"credits":3, "plan":"FREE"}

    search_logic = can_search_id(viewer, tsap_id)

    # Generate reasons if viewer exists
    reasons = []
    if viewer_id:
        v = next((u for u in DB_USERS if u["tsap_id"]==viewer_id), None)
        if v:
            score = calculate_match_score(v, user)
            reasons = generate_personalized_reasons(v, user, score)
    else:
        reasons = ["Nuvvu Hyd kavali annavu → profile kooda Hyd lone", "Software + Reddy perfect"]

    # 🔒 PRIVACY FIX: mundu ikkada FULL user dict (phone + email + encrypted) return ayyedi — leak!
    #    Ippudu contact details teesesi matrame (numbers ivvamu).
    pub = dict(safe_user(user))
    pub["is_nri"] = _is_nri(user)              # 🌊 WAVE 14 — NRI badge
    pub["country"] = user.get("country", "India")
    pub["profession_label"] = _prof_label(user)
    pub["radius"] = user.get("radius", "")
    pub["about_myself"] = user.get("about_myself", "")
    pub["family_details"] = user.get("family_details", "")
    pub["photo_urls"] = user.get("photo_urls", [])
    pub["photo_status"] = user.get("photo_status", "none")      # 🌊 WAVE 17
    pub["selfie_verified"] = bool(user.get("selfie_verified", False))
    return {
        "profile": pub,
        "can_view_profile": True,
        "can_view_number": False,          # 🔒 number eppudu direct ga ivvamu
        "can_view_number_reason": "🔒 Number ivvamu — interest pampandi (vaallu accept cheste matrame contact exchange). "
                                  "Free lo 3 requests unnayi; paid plan tho ekkuva requests + priority.",
        "contact_locked": True,
        "phone_masked": pub.get("phone_masked", ""),
        "unlock_telugu": ["1️⃣ Interest pampandi (FREE 3 requests) — vaallu accept cheste rendu numbers WhatsApp lo",
                          "2️⃣ Plan thisukondi (₹99 → 5 requests) — ekkuva profiles + boost",
                          "3️⃣ Number eppudu public ga kanipinchadu — consent tho matrame exchange"],
        "quality": profile_completeness(user),
        "trust": trust_score(user, DB_INTERESTS),
        "consent_note_telugu": "🔒 Mee number kooda protected — interest accept ayithe matrame exchange avutundi",
        "is_photo_blur": viewer.get("plan","FREE")=="FREE" and bool(user.get("privacy_mode")=="private" or user.get("photo_private")),
        "reasons": reasons,
        "credits_needed": 1,
        "viewer_credits": viewer.get("credits",0)
    }

@app.get("/api/matches/{tsap_id}")
def get_matches(tsap_id: str, min_score: int = 70, limit: int = 20, caste_filter: Optional[str] = None,
                education: Optional[str] = None, district: Optional[str] = None, salary_min: int = 0,
                salary_max: int = 0, verified_only: bool = False, photo_only: bool = False,
                marital_status: Optional[str] = None, dosham: Optional[str] = None, offset: int = 0):
    """
    Matches — Only 70%+ + personalized reasons
    Pin-to-Pin: Opposite gender, score, filter, reason
    """
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user:
        raise HTTPException(404, "User not found")

    # 🛡️ clamps (mundu limit=-1 → 75 rows; min_score=99999 → garbage)
    min_score = clamp_int(min_score, "min_score", 0, 100, 70)
    limit = clamp_int(limit, "limit", 1, 50, 20)
    offset = clamp_int(offset, "offset", 0, 10000, 0)

    all_profiles = [p for p in DB_USERS if not safety.is_blocked(tsap_id, p.get("tsap_id", ""), DB_BLOCKS)
                    and not p.get("is_banned") and p.get("tsap_id") != tsap_id]
    if caste_filter:
        all_profiles = [p for p in all_profiles if p.get("caste") == caste_filter]
    _f = {"education": education, "district": district, "marital_status": marital_status, "dosham": dosham,
          "salary_min": salary_min or None, "salary_max": salary_max or None,
          "verified_only": bool(verified_only), "photo_only": bool(photo_only)}
    if any(v for v in _f.values()):
        all_profiles = [p for p in all_profiles if matches_filters(p, _f)]

    top = find_top_matches(user, all_profiles, limit=limit + offset, min_score=min_score)[offset:]

    # 🔒 PRIVACY FIX: match dicts lo phone/email poyi (contact lock) — score + reasons matrame
    safe_top = []
    for m in top:
        row = dict(safe_user(m))
        row["score"] = m.get("score", 0)
        row["reasons"] = m.get("reasons", [])
        row["photo_urls"] = m.get("photo_urls", [])
        row["is_verified"] = bool(m.get("is_verified") or m.get("phone_verified"))
        row["quality_percent"] = profile_completeness(m).get("percent", 0)
        row["trust"] = trust_score(m, DB_INTERESTS)
        safe_top.append(row)

    return {"user_id": tsap_id, "total_found": len(safe_top), "matches": safe_top,
            "filter": caste_filter or "All", "min_score": min_score,
            "contact_locked": True,
            "contact_note_telugu": "🔒 Numbers ivvamu — interest pampandi (accept ayithe exchange) leda plan thisukondi"}

@app.post("/api/credits/deduct/{tsap_id}")
def deduct_credit_api(tsap_id: str, target_id: str = "", request: Request = None):
    """
    🐞 FIX (policy "numbers ivvavu"): mundu ee endpoint credit teesukuni **fake number "98480xxxxx"** ichedi.
    Ippudu numbers credit tho ammamu — credit kooda deduct avvadu.
    """
    require_owner(request, tsap_id)   # 🛡️ IDOR fix
    return JSONResponse(status_code=410, content={
        "success": False, "deprecated": True,
        "message_telugu": ("🔒 Numbers ippudu credit tho ivvamu — interest pampandi, vaallu accept cheste "
                           "rendu numbers WhatsApp lo exchange avutayi (FREE)."),
        "how_to_unlock": ["1️⃣ Interest pampandi (FREE 3 requests)", "2️⃣ Vaallu accept cheyyali (consent)",
                          "3️⃣ Appudu rendu numbers WhatsApp lo — manam madhyalo unnam"],
        "pay_url": "/pricing"})

@app.post("/api/payment/webhook")
async def payment_webhook(user_id: str = "", amount: int = 0, razorpay_payment_id: str = "",
                          referral_code: str = "", plan_code: str = "", signature_verified: bool = False,
                          request: Request = None):
    """
    💰 Razorpay webhook → **signature verify** → plan apply → referral commission.

    🛡️ WAVE 9 FIXES:
      • B01 `signature_verified=true` query bypass → ippudu admin/automation key tho matrame (free ₹499 plan hack closed)
      • B02 real HMAC-SHA256 **raw body** verification (mundu dead code — NameError silent swallow)
      • B03 prod lo RAZORPAY_WEBHOOK_SECRET lekapote unsigned webhook **reject** (fail-closed)
      • B04 Razorpay JSON webhook body support (payload.payment.entity → user_id/amount/payment_id notes nunchi)
      • B05 plan_code price != amount → 400 (₹1 + VIP plan mismatch hack)
    """
    raw_body = b""
    try:
        raw_body = await request.body()      # signature verify ki raw bytes kavali
    except Exception:
        raw_body = b""
    body: Dict[str, Any] = {}
    if raw_body:
        try:
            body = json.loads(raw_body.decode("utf-8")) or {}
        except Exception:
            body = {}
    entity = {}
    if isinstance(body, dict):
        entity = (((body.get("payload") or {}).get("payment") or {}).get("entity") or {}) or {}
    if entity:
        _notes = entity.get("notes") or {}
        user_id = user_id or str(_notes.get("user_id") or _notes.get("tsap_id") or "")
        if not amount:
            amount = int(int(entity.get("amount") or 0) // 100)      # paise → rupees
        razorpay_payment_id = razorpay_payment_id or str(entity.get("id") or "")
        referral_code = referral_code or str(_notes.get("referral_code") or "")
        plan_code = plan_code or str(_notes.get("plan_code") or "")

    user_id = req_text(user_id, "user_id", 3, 60)
    user = next((u for u in DB_USERS if u["tsap_id"] == user_id), None)
    if not user:
        raise HTTPException(404, "User not found")

    sig_header = ""
    try:
        sig_header = (request.headers.get("x-razorpay-signature") or "").strip()
    except Exception:
        sig_header = ""
    _wh_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").strip()
    _bridge = is_admin(request) or is_automation(request)          # internal bridge (x-api-key/admin key)
    _sig_ok = bool(_wh_secret) and verify_webhook_signature(sig_header, _wh_secret, raw_body)

    if _wh_secret and not _sig_ok:
        abuse_log("webhook_signature_fail", user_id)
        abuse_count("webhook_rejected")
        return JSONResponse(status_code=401, content={
            "success": False, "error": "signature_invalid",
            "message_telugu": "⚠️ Webhook signature verify kaledu — payment accept cheyyaledu (RAZORPAY_WEBHOOK_SECRET chusukondi)"})
    # 🛡️ fail-closed **gateway live** unnappudu matrame (Razorpay keys unte):
    #    keys unte kaani secret ledu ante → unsigned webhook reject (misconfiguration).
    #    Gateway inka configure avvakapote (keys ledu) → legacy/dev flow ki allow (abuse ledger lo log).
    _gateway_live = bool((os.getenv("RAZORPAY_KEY_ID") or "").strip()) or \
        str(os.getenv("PAYMENTS_LIVE", "")).strip().lower() in ("1", "true", "yes", "on")
    if not _wh_secret and not dev_mode() and _gateway_live:
        abuse_log("webhook_secret_missing", user_id)
        abuse_count("webhook_rejected")
        return JSONResponse(status_code=503, content={
            "success": False, "error": "webhook_secret_missing",
            "message_telugu": "⚠️ Payment gateway keys unnayi kaani webhook secret ledu — safe side reject chesam (RAZORPAY_WEBHOOK_SECRET set cheyyandi)"})
    if not _wh_secret and not _gateway_live:
        abuse_log("webhook_unsigned_no_gateway", user_id)
    if signature_verified and not _bridge:
        abuse_log("webhook_fake_signature_flag", user_id)
        abuse_count("admin_denied")
        return JSONResponse(status_code=403, content={
            "success": False, "error": "signature_verified_forbidden",
            "message_telugu": "🔒 signature_verified flag client nunchi ivvakoodadu — gateway signature matrame"})
    if not razorpay_payment_id and not _sig_ok and not (_bridge and signature_verified):
        return JSONResponse(status_code=400, content={
            "success": False, "error": "payment_proof_missing",
            "message_telugu": "⚠️ Payment proof ledu — order id + payment id pampandi"})

    amount = req_int(amount, "amount", 1, 1_000_000)
    razorpay_payment_id = clean(razorpay_payment_id, 60, "payment_id")
    _code_in = (plan_code or "").strip().upper()
    if _code_in:
        _known = next((_p for _p in (list(INTEREST_PLANS.values()) + list(ADDONS.values()) + list(RENEWALS.values()))
                       if str(_p.get("code", "")).upper() == _code_in), None)
        if _known and int(_known.get("price", 0)) != int(amount):
            abuse_log("webhook_amount_mismatch", f"{_code_in}:{amount}")
            abuse_count("webhook_rejected")
            return JSONResponse(status_code=400, content={
                "success": False, "error": "amount_mismatch",
                "expected_amount": _known.get("price"),
                "message_telugu": f"⚠️ {_code_in} price ₹{_known.get('price')} — meeku ₹{amount} vachindi. Match avvatledu."})
    if not dev_mode() and razorpay_payment_id and not razorpay_payment_id.startswith(("pay_", "order_", "upi_", "txn_")):
        abuse_log("webhook_bad_payment_id", user_id)
        return JSONResponse(status_code=400, content={
            "success": False, "error": "bad_payment_id",
            "message_telugu": "⚠️ Razorpay payment id format tappu (pay_xxxx laga undali)"})
    if razorpay_payment_id and idem_seen("pay:" + razorpay_payment_id):
        abuse_log("webhook_replay", razorpay_payment_id)
        abuse_count("webhook_replay")
        return {"success": True, "duplicate": True, "user_id": user_id, "payment_id": razorpay_payment_id,
                "message_telugu": "✅ Ee payment mundu already apply ayyindi — double credit ivvamu (idempotent)",
                "total_credits": user.get("credits", 0), "plan": user.get("plan", "FREE")}

    applied = apply_payment(user, amount, plan_code)
    if not applied["ok"]:
        return JSONResponse(status_code=400, content={
            "success": False, **applied,
            "message_telugu": "⚠️ Ee amount ki plan ledu — /api/pricing chusi correct amount pampandi",
            "valid_amounts": [p["price"] for p in plan_list()] + [a["price"] for a in addon_list()]})

    # 🧾 payment record (audit)
    DB_PAYMENTS.append({"at": datetime.utcnow().isoformat(), "tsap_id": user_id, "amount": amount,
                        "plan": applied["plan"]["code"], "kind": applied["kind"],
                        "payment_id": razorpay_payment_id, "referral_code": referral_code})

    # 🤝 referral commission (payment vachhina ventane) + referrer ki instant WhatsApp
    referral_result = None
    if user.get("referred_by"):
        referral_result = process_referral_payment(user, user["referred_by"], amount, DB_USERS)
        if referral_result.get("success"):
            try:
                _r = next((u for u in DB_USERS if u.get("tsap_id") == referral_result.get("referrer_id")), None)
                if _r:
                    _rtxt = referrer_commission_text(_r, user, referral_result)
                    _rphone = str(_r.get("phone") or "").strip()
                    if _rphone and publish_config()["wa_mode"] != "off":
                        _q = enqueue_whatsapp([_rphone], _rtxt, priority=0, kind="referral_commission")
                        referral_result["referrer_notified"] = bool(_q.get("queued"))
                    else:
                        referral_result["referrer_message"] = _rtxt
            except Exception as e:
                referral_result["notify_error"] = str(e)[:120]

    return {
        "success": True, "user_id": user_id, "amount": amount,
        "plan": applied["plan"]["code"], "kind": applied["kind"],
        "profiles_added": applied["profiles_added"], "total_credits": applied["credits"],
        "plan_expiry": applied["expiry"], "perks": applied["plan"].get("perks", []),
        "referral_commission": referral_result,
        "gst_note": "GST invoice kavali ante 24h lo support ki cheppandi (manavivaha.in/refund lo contact undi)",
        "message_telugu": applied["message_telugu"],
    }

@app.get("/api/referral/leaderboard")
def leaderboard(period: str = "all", limit: int = 10):
    """🏆 Top referrers — period: all | week | month | today (telugu labels tho)."""
    # 🐞 FIX (B08): period='JUNK' accept ayye (empty board) + limit=-5/1e9 unvalidated
    period = req_choice(period or "all", "period", ("all", "today", "week", "month"), required=False, default="all")
    limit = clamp_int(limit, "limit", 1, 50, 10)
    board = get_leaderboard(DB_USERS, limit=limit, period=period)
    return {"success": True, "period": period, "leaderboard": board, "total_users": len(DB_USERS),
            "prize_telugu": "Weekly top-1 ki ₹1000 + Elite badge (mana team WhatsApp lo contact chestundi)"}


# ═══════════════════ 🤝 REFERRAL 2.0 — DASHBOARD / SHARE / PAYOUT ═══════════════════

def _user_or_404(tsap_id: str) -> Dict:
    u = next((x for x in DB_USERS if x["tsap_id"] == tsap_id), None)
    if not u:
        raise HTTPException(404, "User not found — ID sari ga chusukondi")
    return u


@app.get("/api/referral/terms")
def referral_terms():
    """📜 Referral rules (Telugu) — andariki ₹50, tiers, payout, fraud rules."""
    return {"success": True, **referral_terms_telugu()}


@app.get("/api/referral/{tsap_id}")
def referral_home(tsap_id: str, request: Request = None):
    """
    📊 Mee referral dashboard — code, link, clicks, registrations, payments, wallet,
    tier, next milestone, ledger, payouts. (Tenant-safe: mee ID matrame chudochu.)
    """
    user = _user_or_404(tsap_id)                 # 🐞 FIX: tappu ID ki 401 kaadu — 404 (correct)
    require_owner(request, tsap_id)              # 🛡️ WAVE 9: IDOR fix — own data matrame
    d = referral_dashboard(user, DB_USERS)
    d["share_kit"] = referral_share_kit(user)
    return d


@app.get("/api/referral/{tsap_id}/share-kit")
def referral_share(tsap_id: str):
    """📲 5 ready WhatsApp messages + Telegram + SMS + poster text (Telugu)."""
    user = _user_or_404(tsap_id)
    kit = referral_share_kit(user)
    return {"success": True, **kit}


@app.get("/api/referral/{tsap_id}/poster.png")
def referral_poster(tsap_id: str, style: str = "square"):
    """🖼️ Referral poster (QR tho) — square (1080×1080) leda status (1080×1920)."""
    user = _user_or_404(tsap_id)
    ensure_referrer_profile(user, DB_USERS)
    try:
        import referral_kit
        path = referral_kit.poster_card(user, style=("status" if style == "status" else "square"))
        return FileResponse(path, media_type="image/png",
                            filename="manavivaha-referral-%s-%s.png" % (user.get("referral_code", "mv"), style))
    except Exception as e:
        raise HTTPException(500, "Poster generate avvaledu: %s" % str(e)[:120])


@app.post("/api/referral/click/{code}")
def referral_click(code: str, source: str = "link"):
    """/r/<code> link click — funnel tracking (clicks → registrations → payments)."""
    st = track_click(code, source)
    known = validate_referral(code, DB_USERS)
    return {"success": True, **st, "valid_code": known.get("ok", False),
            "referrer_name": known.get("referrer_name", ""),
            "bonus_credits": known.get("bonus_credits", 0)}


@app.get("/api/referral/validate/{code}")
def referral_validate(code: str):
    """Register form / landing page — 'ee code pani chestunda?' + bonus info."""
    return {"success": True, **validate_referral(code, DB_USERS)}


@app.post("/api/referral/payout")
def referral_payout(tsap_id: str, amount: int, method: str = "upi", upi_id: str = "",
                    account_no: str = "", ifsc: str = "", holder: str = "", request: Request = None):
    """
    💸 Payout request — wallet nunchi UPI/bank ki (min ₹100).
    Admin approve chesi UTR isthadu (3 working days SLA).
    """
    user = _user_or_404(tsap_id)
    require_owner(request, tsap_id)   # 🛡️ IDOR: mee payout matrame
    bank = {"account_no": account_no, "ifsc": ifsc, "holder": holder} if method == "bank" else None
    res = payout_request(user, amount, method=method, upi_id=upi_id, bank=bank)
    if not res.get("ok"):
        return JSONResponse(status_code=400, content={"success": False, **res})
    return {"success": True, **res}


@app.post("/api/referral/partner/register")
def referral_partner_register(payload: dict):
    """🤝🌊 WAVE 19 — Partner profile create (name/phone/phonepe/address/state/district) → ID + link + sheet."""
    d = payload or {}
    res = RP19.register_partner(str(d.get("name", "")), str(d.get("phone", "")),
                                str(d.get("phonepe", "")), str(d.get("address", "")),
                                str(d.get("state", "")), str(d.get("district", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    RP19.record_click(res["partner_id"])  # self-view counts as first touch (funnel start)
    return res


@app.get("/api/referral/partner/{pid}")
def referral_partner_public(pid: str):
    """🤝 Partner dashboard (public-safe): link + joins + earnings."""
    res = RP19.partner_public(pid, DB_USERS)
    if not res.get("success"):
        raise HTTPException(404, res.get("message_telugu"))
    return res


@app.post("/api/referral/partner/click/{pid}")
def referral_partner_click(pid: str):
    """🤝 Partner link click tracking."""
    RP19.record_click(pid)
    track_click(pid, "partner_link")
    return {"success": True, "partner_id": pid}


@app.post("/api/referral/partner/payout")
def referral_partner_payout(payload: dict):
    """🤝 Partner payout request (wallet → UPI/bank, min ₹100). No login — phone OTP verify."""
    d = payload or {}
    p = RP19.get_partner(str(d.get("partner_id", "")))
    if not p:
        raise HTTPException(404, "⚠️ Partner ID dorakaledu")
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    if phone != p.get("phone") or phone not in VERIFIED_PHONES:
        raise HTTPException(401, "🔒 Register chesina number tho OTP verify cheyyandi (mundu /api/otp/send + verify)")
    res = payout_request(p, int(d.get("amount", 0) or 0), method=str(d.get("method", "upi")),
                         upi_id=str(d.get("upi_id", "")), bank=d.get("bank"),
                         note="partner:" + p["partner_id"])
    if not res.get("ok"):
        raise HTTPException(400, res.get("message_telugu"))
    return {"success": True, **res}


@app.get("/api/admin/referrals/report")
def admin_referrals_report(request: Request):
    """🤝🌊 WAVE 19 ADMIN — evariki entha + evari referral lo evaru (partners + users, earning sort)."""
    require_admin(request)
    return RP19.admin_report(DB_USERS)


@app.get("/api/admin/referrals/partners.csv")
def admin_referrals_csv(request: Request):
    """🤝 ADMIN — partners SHEET download (Excel/Sheets-ready CSV)."""
    require_admin(request)
    from fastapi.responses import FileResponse
    if not os.path.exists(RP19.CSV_FILE):
        raise HTTPException(404, "Partners inka leru — sheet khali")
    return FileResponse(RP19.CSV_FILE, media_type="text/csv", filename="referral_partners.csv")


@app.get("/api/referral/{tsap_id}/payouts")
def referral_payouts(tsap_id: str, request: Request = None):
    """Mee payout history — request → paid/rejected + UTR."""
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    user = _user_or_404(tsap_id)
    st = referral_stats_of(user)
    mine = [p for p in payout_queue("")["items"] if p.get("tsap_id") == tsap_id]
    return {"success": True, "wallet": st.get("wallet", 0), "pending": st.get("pending_payout", 0),
            "paid_out": st.get("paid_out", 0), "min_payout": 100, "count": len(mine),
            "payouts": [referral_mask_payout(p) for p in list(reversed(mine))[:20]],
            "message_telugu": "💸 Min ₹100 — UPI/bank ki 3 working days lo (UTR tho confirm)"}




# ---------------------------------------------------------------------------
# 🔐 ADMIN GUARD — payout approve/reject lo MONEY move avutundi, kabatti token
#    ADMIN_TOKEN env set cheste aa token lekunda evaru kooda cheyyaledu.
#    (dev/preview lo env lekapote open — kaani response lo warning untundi)
# ---------------------------------------------------------------------------
def _admin_guard(token: str = ""):
    expected = os.getenv("ADMIN_TOKEN", "").strip()
    if expected and token.strip() != expected:
        return JSONResponse(status_code=401, content={
            "success": False, "reason": "unauthorized",
            "message_telugu": "🔐 Admin token avasaram — ADMIN_TOKEN header/query pampandi"})
    return None


@app.get("/api/admin/payouts")
def admin_payout_list(status: str = "requested", token: str = "", request: Request = None):
    """👮 Admin — payout queue (approve/reject). ADMIN_TOKEN set aithe token kavali."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    res = payout_queue(status)
    res["guard"] = "token_required" if os.getenv("ADMIN_TOKEN", "").strip() else "open_dev_mode"
    if not os.getenv("ADMIN_TOKEN", "").strip():
        res["warning_telugu"] = "⚠️ ADMIN_TOKEN env set cheyyandi — appudu admin endpoints lock avutayi"
    return {"success": True, **res}


@app.post("/api/admin/payouts/{request_id}/action")
def admin_payout_action(request_id: str, action: str, utr: str = "", reason: str = "", token: str = "", request: Request = None):
    """✅ Approve (UTR required) leda ❌ Reject (wallet ki malli credit)."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    res = payout_action(request_id, action, DB_USERS, utr=utr, reason=reason)
    if not res.get("ok"):
        return JSONResponse(status_code=400, content={"success": False, **res})
    return {"success": True, **res}


@app.post("/api/admin/refund/{tsap_id}")
def admin_refund(tsap_id: str, amount: int = 0, reason: str = "refund", token: str = "", request: Request = None):
    """
    ↩️ Refund → referral commission clawback (referrer wallet nunchi theesestham).
    Customer refund adigithe idi kooda cheyyali — lekapote referrer double profit.
    """
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    user = _user_or_404(tsap_id)
    if not user.get("referred_by"):
        return {"success": True, "reason": "no_referral", "message_telugu": "Ee user ki referral ledu"}
    res = reverse_referral_payment(user, amount, DB_USERS, reason=reason)
    return {"success": bool(res.get("success")), **res}


@app.get("/api/referral/{tsap_id}/fraud-check")
def referral_fraud_check(tsap_id: str, request: Request = None):
    """🕵️ Self-check: mee account lo emanna referral issue unda?"""
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    user = _user_or_404(tsap_id)
    st = referral_stats_of(user)
    issues = list(st.get("flags", []))
    if user.get("referred_by") and str(user.get("referral_code", "")).upper() == str(user.get("referred_by", "")).upper():
        issues.append("self_referral_locked")
    return {"success": True, "tsap_id": tsap_id, "issues": issues,
            "clean": not issues, "paid_count": st.get("paid_count", 0),
            "wallet": st.get("wallet", 0),
            "message_telugu": "✅ Clean — mee account lo em problem ledu" if not issues
            else "⚠️ Issues: %s" % ", ".join(issues)}




@app.post("/api/admin/approve/{tsap_id}")
def admin_approve(tsap_id: str):
    """Admin approve → auto-post to channels"""
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user: raise HTTPException(404, "Not found")
    user["is_approved"] = True
    user["is_verified"] = True

    # Auto-post queue — ADVANCED ROUTER (same logic as register)
    route = route_profile(user)
    queue = route["usernames"]
    user["posted_channels"] = queue
    user["post_hashtags"] = route["hashtags"]
    caption = build_caption(user, tsap_id, 92)

    # Save post log
    for ch in queue:
        DB_POSTS.append({"user_id": tsap_id, "channel": ch, "hashtags": route["hashtags"],
                         "posted_at": datetime.utcnow().isoformat()})

    return {"success": True, "tsap_id": tsap_id, "posted_to": queue,
            "count": len(queue), "hashtags": route["hashtags"],
            "caption_preview": caption,
            "message": f"Approved + posted to {len(queue)} channels"}

@app.post("/api/admin/make_premium/{tsap_id}")
def admin_make_premium(tsap_id: str, gift_credits: int = 10, request: Request = None):
    """Manual premium — admin gift"""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user: raise HTTPException(404, "Not found")
    user["credits"] += gift_credits
    user["plan"] = "S_199"
    return {"success": True, "tsap_id": tsap_id, "new_credits": user["credits"], "message_telugu": f"💎 Admin gift! {gift_credits} credits FREE + Premium!"}

def _channel_public(key: str, ch: dict) -> dict:
    """Registry channel → website-friendly JSON (join link, status, deep link, hashtags, DP)."""
    user = ch["username"]
    route = ch.get("route") if isinstance(ch.get("route"), dict) else {}
    return {
        "key": key,
        "tier": ch.get("tier"),
        "name": ch.get("name"),
        "username": "@" + user,
        "link": f"https://t.me/{user}",
        "deep_link": f"https://t.me/telugumatrimony1_bot?start=ch_{user.lower()}",
        "desc": ch.get("desc"),
        "hashtags": ch.get("hashtags", []),
        "wave": ch.get("wave"),
        "live": bool(ch.get("live")),
        "status": "LIVE ✅ Bot Admin" if ch.get("live") else f"Create — Wave-{ch.get('wave')}",
        "fallbacks": ch.get("fallbacks", []),
        "photo": f"/api/channels/photo/{key}.png",
        "caste": (route or {}).get("caste", ""),
        "gender": (route or {}).get("gender", ""),
    }

@app.get("/api/channels/photo/{key}.png")
def channel_photo(key: str):
    """Channel DP (512x512) — website lo channel card ki + Telegram setChatPhoto ki same file."""
    import setup_channels as SC
    path = os.path.join(SC.ASSET_DIR, "%s.png" % key)
    if not os.path.exists(path):
        if key not in CHANNELS:
            raise HTTPException(404, "Channel dorakaledu: %s" % key)
        path = SC.channel_dp_image(key, CHANNELS.get(key))
    if not path or not os.path.exists(path):
        raise HTTPException(500, "DP generate avvaledu")
    return FileResponse(path, media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})


@app.get("/api/channels/{key}/kit")
def channel_kit(key: str):
    """Okka channel ki full kit — description + 📌 pinned post + rules + share text (website nunchi copy)."""
    import channel_content as CC
    ch = CHANNELS.get(key)
    if not ch:
        raise HTTPException(404, "Channel dorakaledu: %s" % key)
    return {"key": key, "name": CC.perfect_title(key, ch), "desc": CC.perfect_description(key, ch),
            "pinned_post": CC.pinned_welcome(key, ch), "rules_post": CC.rules_post(key),
            "share_text": CC.share_text(key, ch), "dp_text": CC.dp_text(key),
            "hashtags": ch.get("hashtags", []), "username": "@" + ch["username"],
            "link": "https://t.me/" + ch["username"], "photo": f"/api/channels/photo/{key}.png",
            "live": bool(ch.get("live")), "wave": ch.get("wave"),
            "how_to_setup_telugu": [
                "1) Telegram → New Channel → Name paste → Username paste (taken ayithe fallback)",
                "2) Channel → Administrators → @telugumatrimony1_bot add → Change Info + Post + Pin ✅",
                "3) Description paste → 📌 pinned post paste+pin → DP upload (photo link)",
                "4) Taruvata: python setup_channels.py --apply --key %s" % key,
            ]}


@app.get("/api/channels/setup-plan")
def channels_setup_plan(wave: Optional[int] = None):
    """Channel create plan (wave order) + caste×gender coverage + health — launch/growth dashboard ki."""
    return {"plan": channels_config_setup_plan(wave), "caste_coverage": caste_split_report(),
            "config_problems": channel_health_report(), "stats": channel_stats(),
            "message_telugu": "Wave order lo create cheyyandi — wave 1 lo 4 main + top castes (bride/groom) "
                              "unnayi. Prathi channel ki kit + DP ready (website /channels lo)."}


@app.get("/api/channels")
def channels(tier: Optional[str] = None):
    """FULL master registry — 52 channels (L0 Official → L4 Special, caste clusters × bride/groom)."""
    tiers = channels_by_tier()
    out_tiers = {
        t: [_channel_public(c["key"], c) for c in items]
        for t, items in tiers.items()
    }
    if tier:
        items = out_tiers.get(tier, [])
        return {"tier": tier, "channels": items, "count": len(items), "stats": channel_stats()}
    return {
        "brand": "Mana Vivaha | TSAP Matrimony",
        "site": "https://manavivaha.in",
        "bot": "@telugumatrimony1_bot",
        "stats": channel_stats(),
        "tiers": {
            "L0_OFFICIAL": "Brand hub — daily Top-3, success stories, safety alerts",
            "L1_REGION": "Main 4 — TS Bride, TS Groom, AP Bride, AP Groom (+ NRI)",
            "L2_RELIGION": "Hindu, Muslim, Christian, Other, Inter-faith",
            "L3_CASTE": "Caste-wise — top castes ki bride/groom separate (caste prakaram), migilina castes ki mixed",
            "L4_SPECIAL": "2nd marriage, differently-abled, govt job, IT, doctors, 35+, bureau",
        },
        "channels_by_tier": out_tiers,
        "live": [_channel_public(c["key"], c) for c in live_channels()],
        "to_create": [_channel_public(c["key"], c) for c in pending_channels()],
        "total_live": channel_stats()["live"],
        "total_planned": channel_stats()["total"],
    }

@app.post("/api/channels/route")
def channels_route(payload: dict):
    """
    Profile → ee channels lo post avutundi (preview). Bot + website iddariki same logic.
    Body: {"gender":"Bride","state":"TS","caste":"Reddy","age":24,"job":"Software Engineer", ...}
    """
    r = route_profile(payload)
    return {
        "success": True,
        "channels": r["usernames"],
        "keys": r["keys"],
        "reasons": r["reasons"],
        "hashtags": r["hashtags"],
        "count": r["count"],
        "notes": r["notes"],
        "preview_caption": build_caption(payload, payload.get("tsap_id", "TSAP-F-2025-XXXX"), int(payload.get("score", 92))),
    }

@app.get("/api/publish/status")
def publish_status_endpoint(request: Request = None):
    """Telegram + WhatsApp auto-publish status (dry-run? tokens unnai? enni targets?).

    🔒 WAVE 9: mundu ee endpoint lo anti-ban event details lo FULL phone numbers vachedi (public leak).
    Ippudu public ki mask (98••••••45), admin key unte full details.
    """
    st = {"success": True, **publish_status(), "worker_running": worker_running()}
    if not is_admin(request):
        st = mask_pii(st)
        st["pii_masked"] = True
        st["note_telugu"] = "🔒 Numbers mask chesam — admin key tho full queue details (X-Admin-Key)"
    return st

@app.get("/api/publish/log")
def publish_log_endpoint(limit: int = 20, request: Request = None):
    """Ee varaku publish ayyina profiles log (audit). 🔒 WAVE 9: public ki PII mask."""
    limit = clamp_int(limit, "limit", 1, 200, 20)
    out = {"success": True, "count": limit, "log": read_log(limit)}
    if not is_admin(request):
        out = mask_pii(out)
        out["pii_masked"] = True
    return out

@app.post("/api/publish/now/{tsap_id}")
async def publish_now(tsap_id: str, score: int = 92, request: Request = None):
    """Manual re-post (admin) — already register ayyina profile ni malli channels ki pampu."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    user = next((u for u in DB_USERS if u["tsap_id"] == tsap_id), None)
    if not user:
        raise HTTPException(404, "Profile not found")
    res = await publish_profile(user, tsap_id, score)
    return {"success": True, **res}

@app.post("/api/publish/preview")
def publish_preview(payload: dict):
    """Post avvakunda — caption + WhatsApp text + targets chudu."""
    profile = payload or {}
    tsap_id = profile.get("tsap_id", "TSAP-F-2025-XXXX")
    score = int(profile.get("score", 92))
    return {
        "success": True,
        "telegram_caption": build_caption(profile, tsap_id, score),
        "whatsapp_text": build_whatsapp_text(profile, tsap_id, score),
        "share_text": build_share_text(profile, tsap_id),
        "targets": post_targets(profile),
    }

@app.get("/api/channels/live")
def channels_live():
    return {"live": [_channel_public(c["key"], c) for c in live_channels()],
            "count": channel_stats()["live"], "bot": "@telugumatrimony1_bot"}


# ===========================================================================
# 💌 INTEREST / REQUEST + 💳 CREDITS + 🛡️ WHATSAPP ANTI-BAN CONTROL
# ===========================================================================
def _find_user(tsap_id: str):
    return next((u for u in DB_USERS if u["tsap_id"] == tsap_id), None)


@app.get("/api/plans")
def plans_endpoint():
    """Pricing ladder: FREE 3 → ₹99=5 → ₹199=12 → ₹299=25 → ₹499=50 (VIP) + add-ons."""
    return {
        "currency": "INR",
        "chatting": False,
        "model": "Interest request + WhatsApp lo profile share (chatting ledu)",
        "free_first": 3,
        "plans": plan_list_with_free(),
        "addons": addon_list(),
        "renewal": renewal_offer(),
        "value_ladder": [f"₹{p['price']} → {p['profiles']} profiles (₹{p['per_profile']}/profile)" for p in plan_list()],
        "note_telugu": "Request pampinappudu 1 credit. Accept aithe numbers automatic ga WhatsApp lo. Decline aithe credit refund. "
                       "₹/profile prati tier lo thaggutundi — ₹299 best value, ₹499 VIP.",
    }


@app.get("/api/credits/{tsap_id}")
def credits_endpoint(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found")
    sent = [i for i in DB_INTERESTS if i["from_id"] == tsap_id]
    return {
        "tsap_id": tsap_id,
        "credits": u.get("credits", 0),
        "plan": u.get("plan", "FREE"),
        "plan_label": get_plan(u.get("plan", "FREE"))["label"],
        "requests_sent": len(sent),
        "pending": len([i for i in sent if i["status"] == "pending"]),
        "accepted": len([i for i in sent if i["status"] == "accepted"]),
        "refunded": len([i for i in sent if i.get("credit_refunded")]),
        "plans": plan_list(),
        "message_telugu": ("✅ Mee daggara %d credits unnayi" % u.get("credits", 0)) if u.get("credits", 0) > 0
                          else "⚠️ Credits ayipoyayi — ₹99 tho 3 profiles pondandi",
    }


@app.post("/api/credits/buy")
def credits_buy(payload: dict, request: Request = None):
    """
    Plan buy — Razorpay live ayyaka ee endpoint webhook tho kalisipothundi.
    Ippudu: PAYMENT_AUTO_APPROVE=true (dev/demo) ayithe ventane credits add; leda order create chesi
    UPI/Razorpay link istundi (manual verify).
    """
    tsap_id = (payload or {}).get("tsap_id", "")
    require_owner(request, tsap_id)   # 🛡️ IDOR: mee plan matrame meeru konagalaru
    plan_code = (payload or {}).get("plan", "S_99")
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found — mundu register cheyyandi")
    plan = get_plan(plan_code)
    addon = get_addon(plan_code)
    order_id = "ORD-" + datetime.utcnow().strftime("%y%m%d%H%M%S") + str(len(DB_PAYMENTS) + 1).zfill(3)
    order = {"order_id": order_id, "tsap_id": tsap_id, "plan": plan["code"], "amount": plan["price"],
             "profiles": plan.get("profiles", 0), "at": datetime.utcnow().isoformat(), "status": "created",
             "kind": "addon" if addon else "plan"}
    # 🐞 FIX (money): mundu default "true" → evaraina POST chesthe FREE credits (production lo disaster).
    #    Ippudu: default OFF; dev/demo lo matrame auto (lekapote webhook payment proof adigutundi).
    _auto_env = str(os.getenv("PAYMENT_AUTO_APPROVE", "false")).lower() in ("1", "true", "yes", "on")
    _demo_pay = str(os.getenv("ALLOW_DEMO_PAYMENTS", "0")).lower() in ("1", "true", "yes", "on")
    # prod: default OFF (webhook proof kavali) | dev/test/demo: auto (suites + preview)
    auto = dev_mode() or (_auto_env and _demo_pay)
    if not auto:
        order["payment_required"] = True
        order["next_step_telugu"] = ("💳 ₹%d pay cheyyandi — payment vachhaka credits automatic ga add avutayi "
                                     "(webhook). UPI: manavivaha@upi | Razorpay link soon."
                                     % int(plan["price"]))
    if auto and plan["price"] > 0:
        u["credits"] = int(u.get("credits", 0)) + int(plan.get("profiles", 0) or 0)
        u["plan"] = plan["code"]
        order["status"] = "paid"
        order["credits_added"] = int(plan.get("profiles", 0) or 0)
        # 🎁 ADD-ON effects (boost / whoviewed / verify / porutham)
        if addon:
            days = int(addon.get("days", 30))
            until = (datetime.utcnow() + timedelta(days=days)).isoformat()
            if addon["kind"] == "boost":
                u["boost_until"] = until
                order["effect"] = f"⚡ Boost {days} days active"
            elif addon["kind"] == "whoviewed":
                u["whoviewed_until"] = until
                order["effect"] = f"👀 Who-viewed-me {days} days unlock"
            elif addon["kind"] == "verify":
                u["is_verified"] = True
                u["verified_until"] = until
                order["effect"] = "✅ Verified badge ON"
            elif addon["kind"] == "porutham":
                u["porutham_unlocked"] = True
                order["effect"] = "🔮 Full porutham report unlock"
        elif plan["code"].startswith("S_") or plan["code"].startswith("PREMIUM"):
            # premium plans lo perks automatic ga
            if plan["code"] in ("S_199", "S_299", "S_499", "PREMIUM_299", "VIP_999"):
                u["is_verified"] = True
            if plan["code"] in ("S_299", "S_499", "VIP_999"):
                u["boost_until"] = (datetime.utcnow() + timedelta(days=30)).isoformat()
                u["whoviewed_until"] = (datetime.utcnow() + timedelta(days=60)).isoformat()
        # referral commission (friend pay chesadu → referrer ki ₹50; referral.py logic)
        if u.get("referred_by"):
            try:
                order["referral"] = process_referral_payment(u, u["referred_by"], plan["price"], DB_USERS)
            except Exception as e:
                order["referral"] = {"error": str(e)[:120]}
    DB_PAYMENTS.append(order)
    upi = f"upi://pay?pa=manavivaha@upi&pn=ManaVivaha&am={plan['price']}&cu=INR&tn={order_id}"
    _rec = _item_note = (f"🎁 {addon['label']} active!" if addon else
                         f"🎉 ₹{plan['price']} → {plan.get('profiles', 0)} profiles add ayyayi! Total credits: {u.get('credits', 0)}")
    return {
        "success": True,
        "order": order,
        "credits_now": u.get("credits", 0),
        "plan": plan,
        "upi_link": upi if plan["price"] else "",
        "message_telugu": _item_note if order["status"] == "paid"
                          else f"Order {order_id} create ayyindi — ₹{plan['price']} pay cheyyandi (UPI/Razorpay)",
        "note": "Razorpay live ayyaka idhe endpoint auto-verify chestundi (webhook /api/payment/webhook)",
    }


@app.post("/api/interest/send")
async def interest_send(payload: dict, request: Request = None):
    """
    💌 Interest pampu — 1 credit. Owner ki WhatsApp lo REQUESTER PROFILE + card veltundi.
    (idi user adigina core flow: chatting ledu, WhatsApp lo profile share matrame)
    """
    d = payload or {}
    from_id = d.get("from_id", "").strip()
    to_id = d.get("to_id", "").strip()
    note = d.get("note", "")
    require_owner(request, from_id)   # 🛡️ IDOR: mee ID tarvupuna matrame interest pampali
    note = clean(note, 300, "interest_note", allow_newlines=True)

    frm, to = _find_user(from_id), _find_user(to_id)
    if not frm:
        raise HTTPException(404, f"Mee TSAP ID dorakaledu: {from_id} — mundu register cheyyandi")
    if not to:
        raise HTTPException(404, f"Profile dorakaledu: {to_id}")

    if safety.is_blocked(from_id, to_id, DB_BLOCKS):
        # 🐞 FIX: mundu block unna kooda "gender tappu" error vachedi (misleading message)
        abuse_log("blocked_interest_attempt", f"{from_id}→{to_id}")
        abuse_count("blocked_interest")
        return JSONResponse(status_code=400, content={
            "success": False, "reason": "blocked_user", "blocked": True,
            "message_telugu": "🚫 Ee profile tho contact block ayyindi — vere profiles chudandi (safety first)"})
    if to.get("is_banned"):
        raise HTTPException(400, "Ee profile moderation lo teesesaru — interest pampaleeru")

    # 🛡️ WAVE 11: same gothram → interest auto-block (pelli kudadhu — sampradayam)
    #    (self-interest/gender/duplicate ni core can_send_interest handle chestundi)
    g11 = {"blocked": False} if from_id == to_id else A11.gothram_check(frm, to)
    if g11.get("blocked"):
        abuse_log("same_gothram_interest_block", f"{from_id}→{to_id} ({g11.get('a_gothram')})")
        return JSONResponse(status_code=400, content={
            "success": False, "reason": "same_gothram", "gothram": g11,
            "message_telugu": g11["verdict_telugu"]})

    # 🛡️ WAVE 13: same surname (inti-peru) → interest auto-block (okka inti — pelli kudadhu)
    s13 = {"blocked": False} if from_id == to_id else S12.same_surname_check(frm, to)
    if s13.get("blocked"):
        abuse_log("same_surname_interest_block", f"{from_id}→{to_id}")
        return JSONResponse(status_code=400, content={
            "success": False, "reason": "same_surname", "surname": s13,
            "message_telugu": s13["verdict_telugu"]})

    # 🌊 WAVE 14: AGE RULE — groom kante bride 1-day pedda ayina interest block.
    a14 = {"blocked": False} if from_id == to_id else MP.age_rule_check(frm, to)
    if a14.get("blocked"):
        abuse_log("age_rule_interest_block", f"{from_id}→{to_id}")
        return JSONResponse(status_code=400, content={
            "success": False, "reason": "age_rule", "age_rule": a14,
            "message_telugu": "🙏 " + a14.get("verdict_telugu", "")})

    expire_old(DB_INTERESTS)
    # 💬 ready-made Telugu template (optional)
    _tpl = str(d.get("template_id", "")).strip()
    if _tpl and not note:
        note = next((t["text"] for t in quality_templates() if t["id"] == _tpl), "")
    ok, reason = can_send_interest(frm, to, DB_INTERESTS)
    if not ok:
        if reason == "credits_ledu":
            return JSONResponse(status_code=402, content={
                "success": False, "reason": "credits_ledu", "credits": frm.get("credits", 0),
                "plans": plan_list(), "pay_url": "/requests#plans",
                "message_telugu": "⚠️ Credits ayipoyayi — ₹99 tho 3 profiles, ₹199 tho 10, ₹299 tho 20 pondandi",
            })
        return JSONResponse(status_code=400, content={"success": False, "reason": reason,
                                                      "message_telugu": reason})

    try:
        v2 = topmatch.score_match_v2(frm, to)
        score, reasons = v2["score"], (v2["strengths"] + [v2["verdict_telugu"]])
    except Exception:
        score, reasons = _score_pair(frm, to)

    rec = create_interest(frm, to, note=note, score=score, reasons=reasons,
                          channel=d.get("channel", "website"))
    deduct = deduct_credit(frm)
    if not deduct.get("success"):
        return JSONResponse(status_code=402, content={"success": False, "plans": plan_list(),
                                                      "message_telugu": deduct.get("message_telugu", "Credits ledu")})
    DB_INTERESTS.append(rec)

    # ── WhatsApp: owner ki requester profile (+ card image) | requester ki confirmation ──
    owner_text = interest_to_owner_text(frm, to, rec)
    # 🔮 porutham line (star details unte) — owner message + response rendu chotla
    try:
        p_line = porutham_line(to, frm) if (frm.get("gender") == "Groom") else porutham_line(frm, to)
        por = compute_porutham(frm, to) if frm.get("gender") == "Groom" else compute_porutham(to, frm)
        if por.get("available"):
            owner_text += f"\n{porutham_line(to, frm) if frm.get('gender')=='Groom' else porutham_line(frm, to)}"
            rec["porutham_score"] = por["score"]
            rec["porutham_verdict"] = por["verdict"]
    except Exception:
        pass
    notify_text = interest_notify_text(frm, to, rec)
    owner_phone = to.get("phone", "")
    frm_phone = frm.get("phone", "")
    wa_plan = enqueue_whatsapp([owner_phone], owner_text, image_id=from_id, priority=0,
                               kind="interest_to_owner")
    wa_plan2 = enqueue_whatsapp([frm_phone], notify_text, image_id=to_id, priority=0,
                                kind="interest_confirm")
    if not wa_plan.get("queued"):
        start_wa_worker()

    return {
        "success": True,
        "request_id": rec["request_id"],
        "status": rec["status"],
        "expires_in_days": INTEREST_EXPIRY_DAYS,
        "score": score,
        "reasons": reasons,
        "credits_left": frm.get("credits", 0),
        "sent_to": safe_user(to),
        "whatsapp": {
            "mode": publish_config()["wa_mode"],
            "owner_queued": wa_plan.get("queued", False),
            "requester_queued": wa_plan2.get("queued", False),
            "owner_link_manual": whatsapp_link(owner_phone, owner_text) if not wa_plan.get("queued") else "",
            "anti_ban": f"{int(WA_ENGINE.cfg()['min_gap_interest'])}–{int(WA_ENGINE.cfg()['max_gap_interest'])}s random gap (fast lane)",
        },
        "owner_message_preview": owner_text,
        "message_telugu": (f"💌 Interest pampincharu! {safe_user(to)['full_name']} ki WhatsApp lo "
                           f"mee profile veltundi. Accept aithe numbers automatic ga exchange avutayi. "
                           f"Credits migilayi: {frm.get('credits', 0)}"),
    }


@app.get("/api/interest/inbox/{tsap_id}")
def interest_inbox(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found")
    expire_old(DB_INTERESTS)
    data = inbox_for(u, DB_USERS, DB_INTERESTS)
    data["credits"] = u.get("credits", 0)
    data["model"] = "accept → number exchange (chatting ledu)"
    return data


@app.get("/api/interest/sent/{tsap_id}")
def interest_sent(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found")
    expire_old(DB_INTERESTS)
    data = sent_for(u, DB_USERS, DB_INTERESTS)
    data["credits"] = u.get("credits", 0)
    return data


@app.post("/api/interest/respond")
async def interest_respond(payload: dict, request: Request = None):
    """Owner accept/decline. Accept → rendu numbers WhatsApp lo (consent based). Decline → credit refund."""
    d = payload or {}
    tsap_id = d.get("tsap_id", "")
    request_id = d.get("request_id", "")
    action = (d.get("action", "") or "").lower()
    require_owner(request, tsap_id)   # 🛡️ IDOR: ee request owner ki matrame
    owner = _find_user(tsap_id)
    if not owner:
        raise HTTPException(404, "User not found")
    rec = next((i for i in DB_INTERESTS if i["request_id"] == request_id), None)
    if not rec:
        raise HTTPException(404, f"Request dorakaledu: {request_id}")
    if rec["to_id"] != tsap_id:
        raise HTTPException(403, "Ee request meeku kaadu")
    requester = _find_user(rec["from_id"])
    res = respond_interest(rec, owner, requester or {}, action)
    if not res.get("success"):
        return JSONResponse(status_code=400, content=res)

    wa = {}
    if action == "accept" and requester:
        txt = interest_accepted_text(requester, owner, rec)
        wa = enqueue_whatsapp([requester.get("phone", "")], txt, image_id=owner["tsap_id"],
                              priority=0, kind="interest_accepted")
        enqueue_whatsapp([owner.get("phone", "")], txt, image_id=requester["tsap_id"],
                         priority=0, kind="interest_accepted_owner")
        res["contact"] = {"name": requester.get("full_name"), "phone": requester.get("phone", "")}
        # 📜 consent ledger (audit trail — numbers eppudu exchange ayyayo)
        log_consent("interest_accepted", owner.get("tsap_id", ""), requester.get("tsap_id", ""),
                    request_id=request_id, exchanged=True, note="rendu numbers WhatsApp lo exchange")
        res["consent_record_telugu"] = "📜 Ee exchange consent ledger lo record ayyindi (mee profile lo chudochu)"
    elif action == "decline":
        log_consent("interest_declined", owner.get("tsap_id", ""), (requester or {}).get("tsap_id", ""),
                    request_id=request_id, exchanged=False, note="number share cheyyaledu")
        if rec.get("credit_refunded"):
            requester and requester.update({"credits": int(requester.get("credits", 0)) + 1})
        if requester:
            txt = interest_declined_text(requester, owner, rec)
            wa = enqueue_whatsapp([requester.get("phone", "")], txt, priority=0, kind="interest_declined")
    elif action == "withdraw":
        rec["credit_refunded"] = True
        if requester:
            requester.update({"credits": int(requester.get("credits", 0)) + 1})

    return {"success": True, "request": rec, "whatsapp": wa, "result": res,
            "message_telugu": res.get("message"), "credits": owner.get("credits", 0)}


@app.get("/api/interest/status/{request_id}")
def interest_status(request_id: str):
    rec = next((i for i in DB_INTERESTS if i["request_id"] == request_id), None)
    if not rec:
        raise HTTPException(404, "Request not found")
    return {"request": rec,
            "steps": [
                {"step": "Request pampincharu", "done": True},
                {"step": "Owner ki WhatsApp lo mee profile vellindi", "done": True},
                {"step": "Owner reply (accept/decline)", "done": rec["status"] in ("accepted", "declined")},
                {"step": "Numbers exchange (WhatsApp)", "done": rec.get("contact_shared", False)},
            ]}


# ---------------------------------------------------------------- WhatsApp control
@app.get("/api/wa/status")
def wa_status():
    """Anti-ban live status: gap, caps, queue, quiet hours, cooldown + per-number instances."""
    return {"ok": True, **wa_queue_stats(),
            "instances": wa_pool.wa_health(),
            "per_number": {i["name"]: {"sent_today": i["sent_today"], "cap": i["daily_cap"],
                                       "status": i["status"], "available": i["available"]}
                           for i in wa_pool.wa_health()["instances"]}}


@app.get("/api/system/health")
def system_health():
    """
    🩺 FULL SYSTEM HEALTH — bots (failover order) + WhatsApp numbers + queue + dead-letters.
    Dashboard lo idi chudandi: okati down ayithe pakkadi automatic ga pani chestundi.
    """
    bt = bot_pool.bot_health()
    wa = wa_pool.wa_health()
    dead = dead_letters(5)
    problems = []
    if bt["configured"] == 0:
        problems.append("Telegram bots configure cheyyaledu (BOT_TOKEN)")
    elif bt["available"] == 0:
        problems.append("Anni Telegram bots cooldown/dead lo unnayi")
    if wa["configured"] == 0:
        problems.append("WhatsApp instances ledu (WA_INSTANCES / WHATSAPP_BRIDGE_URL)")
    elif wa["available"] == 0:
        problems.append("Anni WhatsApp numbers unavailable (QR/caps/cooldown)")
    return {"ok": not problems, "problems": problems,
            "bots": bt, "whatsapp": wa,
            "queue": {"pending": len(WA_QUEUE), "dead": len(WA_DEAD)},
            "dead_letters_preview": dead["items"],
            "message_telugu": ("Anni healthy ✅ — okati fail aina pakkadi ventane pampistundi"
                               if not problems else " ⚠️ ".join(problems))}


@app.get("/api/wa/dead")
def wa_dead(limit: int = 50, request: Request = None):
    """💀 Dead-letter list — 3 tries ayyaka kooda deliver kaani messages (bridge problem)."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return dead_letters(limit)


@app.post("/api/wa/dead/requeue")
def wa_dead_requeue(limit: int = 20, request: Request = None):
    """Bridge fix ayyaka dead-letters ni malli queue lo vey."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return requeue_dead(limit)


@app.get("/api/bots/health")
def bots_health(request: Request = None):
    """🤖 Telegram bots health + failover order (primary → backup → alert)."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return {"ok": True, **bot_pool.bot_health()}


@app.post("/api/wa/pause")
def wa_pause(reason: str = "manual", request: Request = None):
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return {"ok": True, **WA_ENGINE.pause(reason)}


@app.post("/api/wa/resume")
def wa_resume(request: Request = None):
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return {"ok": True, **WA_ENGINE.resume()}


@app.post("/api/wa/reset_day")
def wa_reset_day(request: Request = None):
    """Test tip: ee roju counters reset (caps fresh). Production lo vaddu."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return {"ok": True, **WA_ENGINE.reset_today()}


@app.get("/api/admin/wa/numbers")
def admin_wa_numbers(request: Request):
    """📱🌊 WAVE 19 ADMIN — 3 numbers health (otp/channels/personal lanes + orders + caps)."""
    require_admin(request)
    h = wa_pool.wa_health()
    return {"success": True, **h,
            "lanes_telugu": {"otp": "🔑 OTP number (OTP lu matrame, fast 25–60s)",
                             "channels": "📢 Channels number (posts, 120–170s gaps)",
                             "personal": "💬 Personal number (interest/referral DMs, 60–120s)",
                             "both": "🛟 Backup (purpose number down ayithe)"}}


@app.post("/api/admin/wa/numbers")
def admin_wa_number_add(payload: dict, request: Request):
    """📱 ADMIN — number add (name, bridge url, lane, cap, token, number)."""
    require_admin(request)
    d = payload or {}
    if not str(d.get("url", "")).strip():
        raise HTTPException(400, "Bridge URL ivvandi (http://wa-otp:3000 lanti)")
    return wa_pool.get_pool().add_instance(
        str(d.get("name", "")), str(d.get("url", "")), str(d.get("lane", "both")),
        int(d.get("daily_cap", 60) or 60), str(d.get("token", "")), str(d.get("number", "")))


@app.post("/api/admin/wa/numbers/{name}")
def admin_wa_number_update(name: str, payload: dict, request: Request):
    """📱 ADMIN — number update/pause/resume (url/lane/cap/token/number/paused)."""
    require_admin(request)
    d = payload or {}
    kw = {k: d[k] for k in ("url", "lane", "daily_cap", "token", "number", "paused") if k in d}
    res = wa_pool.get_pool().update_instance(name, **kw)
    if not res.get("success"):
        raise HTTPException(404, res.get("message_telugu"))
    return res


@app.delete("/api/admin/wa/numbers/{name}")
def admin_wa_number_delete(name: str, request: Request):
    """📱 ADMIN — number remove."""
    require_admin(request)
    res = wa_pool.get_pool().remove_instance(name)
    if not res.get("success"):
        raise HTTPException(404, res.get("message_telugu"))
    return res


@app.post("/api/demo/seed")
def demo_seed(request: Request = None):
    """
    Demo profiles create (frontend test cheyyadaniki) — idempotent, dev convenience.
    DEMO_SEED_ENABLED=false chesthe bandh.
    """
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    if str(os.getenv("DEMO_SEED_ENABLED", "true")).lower() not in ("1", "true", "yes", "on"):
        raise HTTPException(403, "Demo seed bandh chesaru")
    seeds = [
        # ---- 4 base profiles (fixed IDs — /matches, /search demo IDs tho match avvali) ----
        dict(prefer_id="TSAP-F-2025-1042", gender="Bride", full_name="Lakshmi Reddy", age=24, caste="Reddy",
             sub_caste="Pakanati", education="BTech", education_detail="CSE", job="Software Engineer",
             company="TCS", salary="8L", height="5'4\"", weight="54kg", district="Hyderabad", state="TS",
             gothram="Bharadwaj", star="Rohini", rasi="Vrishabha", phone="9848011111", family_type="Nuclear",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=True),
        dict(prefer_id="TSAP-F-2025-2042", gender="Bride", full_name="Sravani Chowdary", age=26, caste="Kamma",
             sub_caste="", education="MSc", education_detail="Data Science", job="Data Analyst",
             company="Deloitte", salary="10L", height="5'5\"", weight="56kg", district="Vijayawada", state="AP",
             gothram="Kasyapa", star="Ashwini", rasi="Mesha", phone="9848022222", family_type="Joint",
             family_status="Upper Middle", marital_status="Pelli Kaledu", is_verified=True),
        dict(prefer_id="TSAP-M-2025-1042", gender="Groom", full_name="Kiran Kumar Verma", age=29, caste="Reddy",
             sub_caste="Deshathi", education="MBBS", education_detail="MD", job="Doctor", company="Apollo",
             salary="2L+/mo", height="5'10\"", weight="74kg", district="Nalgonda", state="TS", gothram="Vasishta",
             star="Mrigasira", rasi="Dhanu", phone="9848033333", family_type="Nuclear",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=True),
        dict(prefer_id="TSAP-M-2025-4042", gender="Groom", full_name="Arjun Nandan", age=31, caste="Kamma",
             sub_caste="", education="MS", education_detail="USA", job="Product Manager", company="Amazon",
             salary="40L", height="5'11\"", weight="78kg", district="Guntur", state="AP", gothram="Kaundinya",
             star="Bharani", rasi="Simha", phone="9848044444", family_type="Nuclear",
             family_status="Upper Middle", marital_status="Pelli Kaledu", is_verified=True),
        # ---- 6 more brides ----
        dict(gender="Bride", full_name="Divya Kapu", age=23, caste="Kapu", sub_caste="Telaga",
             education="BCom", education_detail="Computers", job="Bank Employee", company="SBI", salary="5L",
             height="5'2\"", weight="50kg", district="Visakhapatnam", state="AP", gothram="Kashyapa",
             star="Hasta", rasi="Kanya", phone="9848055555", family_type="Joint", family_status="Middle Class",
             marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Bride", full_name="Anusha Velama", age=27, caste="Velama", sub_caste="Koppula",
             education="MCom", education_detail="", job="Lecturer", company="Degree College", salary="6L",
             height="5'6\"", weight="58kg", district="Warangal", state="TS", gothram="Srivatsa", star="Swati",
             rasi="Tula", phone="9848066666", family_type="Nuclear", family_status="Middle Class",
             marital_status="Pelli Kaledu", is_verified=False),
        dict(gender="Bride", full_name="Meghana Vysya", age=25, caste="Vysya", sub_caste="Arya Vysya",
             education="BPharm", education_detail="", job="Pharmacist", company="MedPlus", salary="4.5L",
             height="5'3\"", weight="52kg", district="Hyderabad", state="TS", gothram="Kaushika", star="Chitra",
             rasi="Kanya", phone="9848077777", family_type="Joint", family_status="Middle Class",
             marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Bride", full_name="Sandhya Mala", age=24, caste="Mala", sub_caste="",
             education="BSc", education_detail="Nursing", job="Staff Nurse", company="Yashoda", salary="4L",
             height="5'4\"", weight="55kg", district="Nalgonda", state="TS", gothram="Vasishta", star="Revati",
             rasi="Meena", phone="9848088888", family_type="Nuclear", family_status="Middle Class",
             marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Bride", full_name="Swathi Madiga", age=28, caste="Madiga", sub_caste="",
             education="MA", education_detail="Telugu", job="Teacher", company="ZP High School", salary="3.5L",
             height="5'5\"", weight="57kg", district="Karimnagar", state="TS", gothram="Bharadwaj",
             star="Anuradha", rasi="Vrishchika", phone="9848099999", family_type="Joint",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=False),
        dict(gender="Bride", full_name="Gayatri Brahmin", age=26, caste="Brahmin", sub_caste="Vaidiki",
             education="MCA", education_detail="", job="Software Engineer", company="Infosys", salary="9L",
             height="5'4\"", weight="54kg", district="Guntur", state="AP", gothram="Sankhyayana", star="Punarvasu",
             rasi="Mithuna", phone="9848010101", family_type="Nuclear", family_status="Upper Middle",
             marital_status="Pelli Kaledu", is_verified=True),
        # ---- 6 more grooms ----
        dict(gender="Groom", full_name="Rakesh Yadav", age=30, caste="Yadav", sub_caste="Golla",
             education="BTech", education_detail="Mech", job="Govt Job", company="TS Genco", salary="9L",
             height="5'9\"", weight="76kg", district="Hyderabad", state="TS", gothram="Koundinya",
             star="Uttara", rasi="Simha", phone="9848020202", family_type="Joint", family_status="Middle Class",
             marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Groom", full_name="Naveen Padmashali", age=27, caste="Padmashali", sub_caste="",
             education="BCom", education_detail="CA Inter", job="Business", company="Own Textiles",
             salary="12L", height="5'8\"", weight="72kg", district="Warangal", state="TS", gothram="Kashyapa",
             star="Rohini", rasi="Vrishabha", phone="9848030303", family_type="Joint",
             family_status="Upper Middle", marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Groom", full_name="Suresh Lambada", age=33, caste="Lambada", sub_caste="Banjara",
             education="MSc", education_detail="Agriculture", job="Agriculture Officer", company="Govt of TS",
             salary="7L", height="5'7\"", weight="70kg", district="Khammam", state="TS", gothram="Srivatsa",
             star="Dhanishta", rasi="Makara", phone="9848040404", family_type="Nuclear",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=False),
        dict(gender="Groom", full_name="Vijay Goud", age=32, caste="Goud", sub_caste="",
             education="BBA", education_detail="", job="Business", company="Wine & Retail", salary="15L",
             height="5'9\"", weight="80kg", district="Hyderabad", state="TS", gothram="Kaundinya",
             star="Magha", rasi="Simha", phone="9848050505", family_type="Joint", family_status="Rich",
             marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Groom", full_name="Sai Krishna Sharma", age=28, caste="Brahmin", sub_caste="Niyogi",
             education="MBA", education_detail="Finance", job="Software Engineer", company="Microsoft",
             salary="45L", height="5'10\"", weight="75kg", district="Tirupati", state="AP",
             gothram="Bharadwaj", star="Shravana", rasi="Makara", phone="9848060606", family_type="Nuclear",
             family_status="Upper Middle", marital_status="Pelli Kaledu", is_verified=True),
        dict(gender="Groom", full_name="Mahesh SC Others", age=29, caste="SC Others", sub_caste="",
             education="BTech", education_detail="EEE", job="Private Job", company="L&T", salary="8L",
             height="5'8\"", weight="73kg", district="Kurnool", state="AP", gothram="Vasishta",
             star="Ashlesha", rasi="Karkataka", phone="9848070707", family_type="Nuclear",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=False),
    ]
    created = []
    for sd in seeds:
        sd["demo"] = True          # 🎬 demo profile — demo-login allowed (real users ki phone OTP)
        existing = next((u for u in DB_USERS
                         if u.get("full_name") == sd["full_name"] and u.get("district") == sd["district"]), None)
        if existing:
            created.append({"tsap_id": existing["tsap_id"], "name": sd["full_name"],
                            "role": sd["gender"], "existing": True})
            continue
        prefer = sd.pop("prefer_id", None)
        tsap_id = prefer if (prefer and not any(u.get("tsap_id") == prefer for u in DB_USERS)) else unique_tsap_id(sd["gender"])
        user = {**sd, "tsap_id": tsap_id, "credits": 3, "plan": "FREE", "wallet": 0,
                "marital_status": sd.get("marital_status", "Pelli Kaledu"),
                "mandal": sd.get("district", ""), "religion": sd.get("religion", "Hindu"),
                "mother_tongue": "Telugu", "dosham": "No", "moola_nakshatram": "No",
                "blood_group": "", "family_values": "Traditional", "phone_verified": sd.get("is_verified", False),
                "about_myself": f"{sd['full_name']} — {sd.get('job','')} ({sd.get('district','')}). "
                                f"Simple family, traditional values, sambandham kosam chusthunnam.",
                "phone_encrypted": encrypt_phone(sd["phone"]), "phone_last4": sd["phone"][-4:],
                "photo_urls": [], "card_url": f"/cards/{tsap_id}.png",
                "is_verified": bool(sd.get("is_verified", False)),
                "is_approved": True, "privacy_mode": "public", "referral_code": "",       # ensure_referrer_profile() unique code isthundi (duplicate fix)
                "referral_stats": {"total": 0, "paid_count": 0},
                "created_at": datetime.utcnow().isoformat(), "completeness": 88, "score": 92,
                "profile_note": "TSAP demo profile"}
        user["reasons"] = generate_profile_highlights(user)
        DB_USERS.append(user)
        # demo card generate (WhatsApp image test ki) — fail aithe skip
        try:
            if create_pro_card:
                os.makedirs("/tmp/cards", exist_ok=True)
                create_pro_card(user, f"/tmp/cards/{tsap_id}.png")
        except Exception as _e:
            print("[DEMO] card skip:", str(_e)[:80])
        created.append({"tsap_id": tsap_id, "name": sd["full_name"], "role": sd["gender"]})
    return {"success": True, "created": created, "total_users": len(DB_USERS),
            "hint": "Maa ID tho /requests lo interest pampinchu (user adigina flow test)"}



# ===========================================================================
# 🔮 10-PORUTHAM (kundli match) + 👀 WHO VIEWED ME + ❤️ SHORTLIST + 🎁 ADD-ONS
# ===========================================================================
@app.get("/api/porutham")
def porutham_by_id(bride: str = "", groom: str = ""):
    """
    TSAP IDs tho 10-porutham (kundli match) — score /10 + Telugu verdict + per-item notes.
    Udaharanam: /api/porutham?bride=TSAP-F-2025-1042&groom=TSAP-M-2025-1042
    """
    b = _find_user(bride)
    g = _find_user(groom)
    if not b or not g:
        raise HTTPException(404, "Bride/Groom TSAP ID correct ga ivvandi")
    res = compute_porutham(b, g)
    return {"bride": safe_user(b), "groom": safe_user(g), **res}


@app.post("/api/porutham")
def porutham_raw(payload: dict):
    """Star/rasi direct ga isthe kooda calculate chestundi (register cheyyakunda test ki)."""
    d = payload or {}
    b = {"star": d.get("bride_star", ""), "rasi": d.get("bride_rasi", "")}
    g = {"star": d.get("groom_star", ""), "rasi": d.get("groom_rasi", "")}
    return {"bride": b, "groom": g, **compute_porutham(b, g)}


@app.post("/api/view")
def record_view(payload: dict, request: Request = None):
    """
    Profile view record — "evaru chusaru" feature (top matrimony sites lo idi paid).
    Same viewer 6 గంటల్లో malli chuste duplicate ga count avvadu.
    """
    d = payload or {}
    tsap_id = (d.get("tsap_id") or "").strip()
    viewer_id = (d.get("viewer_id") or "").strip()
    require_owner(request, viewer_id)   # 🛡️ IDOR: view mee peru tarvupuna
    if not tsap_id:
        raise HTTPException(400, "tsap_id kavali")
    if viewer_id and viewer_id == tsap_id:
        return {"success": True, "self_view": True, "counted": False}
    # duplicate debounce (6h)
    now = datetime.utcnow()
    for v in reversed(DB_VIEWS[-500:]):
        if v["tsap_id"] == tsap_id and v.get("viewer_id") == viewer_id:
            try:
                if (now - datetime.fromisoformat(v["at"])).total_seconds() < 6 * 3600:
                    return {"success": True, "counted": False, "note": "6h lo duplicate view skip"}
            except Exception:
                pass
    if not _find_user(tsap_id):
        raise HTTPException(404, "Ee profile dorakaledu (view record cheyyaledu)")
    DB_VIEWS.append({"tsap_id": tsap_id, "viewer_id": viewer_id, "at": now.isoformat()})
    total = len([v for v in DB_VIEWS if v["tsap_id"] == tsap_id])
    # 🐞 FIX: mundu key mismatch (`total_views` vs `views_total`) — frontend lo 0 kanipinchedu. Ippudu rendu keys.
    return {"success": True, "counted": True, "total_views": total, "views_total": total,
            "unique_viewers": len({v.get("viewer_id") for v in DB_VIEWS if v["tsap_id"] == tsap_id and v.get("viewer_id")})}


@app.get("/api/views/{tsap_id}")
def views_for(tsap_id: str, request: Request = None):
    """
    Views summary. FREE users ki count + city/caste level info;
    paid (credits/plan) unte **names tho** full list (whoviewed add-on leda ₹299+ plan).
    """
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    u = _find_user(tsap_id)
    mine = [v for v in DB_VIEWS if v["tsap_id"] == tsap_id]
    unique_viewers = []
    for v in mine:
        vid = v.get("viewer_id")
        if vid and vid not in [x["tsap_id"] for x in unique_viewers]:
            vu = _find_user(vid)
            if vu:
                unique_viewers.append(vu)
    plan = (u or {}).get("plan", "FREE")
    whoviewed = bool((u or {}).get("whoviewed_until")) or plan in ("S_199", "S_299", "S_499", "PREMIUM_299", "VIP_999")
    return {
        "tsap_id": tsap_id,
        "total_views": len(mine),
        "views_total": len(mine),                    # 🐞 FIX: frontend ee key expect chestundi (alias)
        "unique_viewers": len(unique_viewers),
        "today": len([v for v in mine if str(v["at"]).startswith(datetime.utcnow().strftime("%Y-%m-%d"))]),
        "whoviewed_unlocked": whoviewed,
        "viewers": [safe_user(v) for v in unique_viewers[-20:]] if whoviewed else [],
        "viewers_masked": [{"caste": v.get("caste", "—"), "district": v.get("district", "—"),
                            "age": v.get("age", "—")} for v in unique_viewers[-20:]] if not whoviewed else [],
        "unlock_addon": ADDONS["WHOVIEWED_49"],
        "message_telugu": (f"👀 Mee profile ni {len(mine)} sarlu chusaru ({len(unique_viewers)} mandi)"
                           + ("" if whoviewed else " — evaru chusaro telusukovali ante ₹49 (30 days)")),
    }


@app.post("/api/save")
def toggle_save(payload: dict, request: Request = None):
    """❤️ Shortlist — profile save/remove (top matrimony sites lo idi must feature)."""
    d = payload or {}
    tsap_id = clean(d.get("tsap_id"), 30, "tsap_id")
    saved_id = clean(d.get("saved_id") or d.get("target_id"), 30, "saved_id")   # 🐞 FIX: target_id alias
    require_owner(request, tsap_id)   # 🛡️ IDOR: mee shortlist matrame
    if not tsap_id or not saved_id:
        raise HTTPException(400, "tsap_id + saved_id (leda target_id) kavali")
    if tsap_id == saved_id:
        raise HTTPException(400, "Mee profile ni meeru save cheyyakkarledu 🙂")
    if not _find_user(saved_id):
        raise HTTPException(404, "Save cheyyalsina profile dorakaledu")
    if safety.is_blocked(tsap_id, saved_id, DB_BLOCKS):
        raise HTTPException(403, "🚫 Blocked profile ni shortlist cheyyaleeru")
    existing = next((x for x in DB_SAVES if x["tsap_id"] == tsap_id and x["saved_id"] == saved_id), None)
    if existing:
        DB_SAVES.remove(existing)
        return {"success": True, "saved": False, "message_telugu": "Shortlist nunchi teesesaaru",
                "total_saved": len([x for x in DB_SAVES if x["tsap_id"] == tsap_id])}
    DB_SAVES.append({"tsap_id": tsap_id, "saved_id": saved_id, "at": datetime.utcnow().isoformat()})
    return {"success": True, "saved": True, "message_telugu": "❤️ Shortlist lo save ayyindi",
            "total_saved": len([x for x in DB_SAVES if x["tsap_id"] == tsap_id])}


@app.get("/api/saved/{tsap_id}")
def saved_list(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    rows = [x for x in DB_SAVES if x["tsap_id"] == tsap_id]
    out = []
    for r in rows:
        u = _find_user(r["saved_id"])
        if u:
            out.append({"saved_at": r["at"], "profile": safe_user(u),
                        "porutham": None})
    # porutham with me (star unte)
    me = _find_user(tsap_id)
    if me:
        for o in out:
            pu = _find_user(o["profile"]["tsap_id"])
            r = compute_porutham(me, pu) if (pu and me.get("gender") == "Groom") else (
                compute_porutham(pu or {}, me) if pu else {"available": False})
            o["porutham"] = {"score": r.get("score"), "max": r.get("max_score"),
                             "verdict": r.get("verdict")} if r.get("available") else None
    return {"tsap_id": tsap_id, "count": len(out), "saved": out[::-1],
            "message_telugu": f"❤️ {len(out)} profiles shortlist lo unnayi"}




# ===========================================================================
# 📱 OTP VERIFY (phone) + 🔎 ADVANCED SEARCH FILTERS
# ===========================================================================
@app.post("/api/photo/upload")
async def photo_upload(file: UploadFile = File(...), tsap_id: str = Form("")):
    """
    📸 Real photo upload — phone lo camera/gallery nunchi.
    Validation: JPG/PNG/WebP, max 5 MB. Storage: /tmp/photos (docker volume) → /photos/{name} URL.
    (P0 gap fill — mundu photo preview matrame undi, real upload ledu)
    """
    data = await file.read()
    # 🌊 WAVE 17 — Layer-1 automatic validation (thappu photo iste asalu thisukovaddu)
    verdict = validate_photo(data, file.filename or "")
    if not verdict["ok"]:
        raise HTTPException(422, {"reason": verdict["reason"], "en": verdict["en"],
                                  "te": verdict["te"],
                                  "message_telugu": f"📸 {verdict['te']}",
                                  "checks": verdict["checks"]})
    ext = (file.filename or "").split(".")[-1].lower()
    if ext not in {"jpg", "jpeg", "png", "webp"}:
        ext = {"heic": "jpg", "heif": "jpg"}.get(ext, "jpg")
    os.makedirs("/tmp/photos", exist_ok=True)
    token = (tsap_id.strip() or "tmp") + "-" + datetime.utcnow().strftime("%y%m%d%H%M%S") + "-" + str(random.randint(100, 999))
    name = f"{token}.{ 'jpg' if ext in ('heic','heif') else ext }"
    path = f"/tmp/photos/{name}"
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise HTTPException(500, f"Photo save avvaledu: {str(e)[:80]}")
    _u = next((u for u in DB_USERS if u.get("tsap_id") == tsap_id.strip()), None) if tsap_id else None
    if _u is not None:
        _u["photo_url"] = f"/photos/{name}"
        _u["photo_status"] = "pending"          # Layer-2: admin human review (top-site standard)
        _u["photo_checks"] = verdict["checks"]
        _u["photo_uploaded_at"] = datetime.utcnow().isoformat()
    return {"success": True, "url": f"/photos/{name}", "bytes": len(data),
            "kb": round(len(data) / 1024, 1), "path": path,
            "status": "pending", "checks": verdict["checks"],
            "message_telugu": f"📸 Photo clear ga undi ({round(len(data)/1024)} KB) — admin approval ki vellindi ✅"}


@app.get("/api/photo/status/{tsap_id}")
def photo_status(tsap_id: str):
    """📸 Photo + selfie verification status (frontend screens: validating/approved/not-approved)."""
    u = next((x for x in DB_USERS if x.get("tsap_id") == tsap_id), None)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    return {"success": True, "tsap_id": tsap_id,
            "photo_url": u.get("photo_url", ""), "photo_status": u.get("photo_status", "none"),
            "photo_reason": u.get("photo_reason", ""), "photo_reason_te": u.get("photo_reason_te", ""),
            "selfie_status": u.get("selfie_status", "none"),
            "selfie_verified": bool(u.get("selfie_verified", False))}


@app.post("/api/verify/selfie")
async def verify_selfie(file: UploadFile = File(...), tsap_id: str = Form("")):
    """🤳 Live-selfie verification upload — technical checks + admin review → trust badge."""
    u = next((x for x in DB_USERS if x.get("tsap_id") == (tsap_id or "").strip()), None)
    if not u:
        raise HTTPException(404, "Profile dorakaledu — mundu register avvandi")
    data = await file.read()
    verdict = validate_photo(data, file.filename or "", selfie=True)
    if not verdict["ok"]:
        raise HTTPException(422, {"reason": verdict["reason"], "en": verdict["en"],
                                  "te": verdict["te"],
                                  "message_telugu": f"🤳 {verdict['te']}",
                                  "checks": verdict["checks"]})
    os.makedirs("/tmp/photos", exist_ok=True)
    name = f"{u['tsap_id']}-selfie-" + datetime.utcnow().strftime("%y%m%d%H%M%S") + ".jpg"
    with open(f"/tmp/photos/{name}", "wb") as f:
        f.write(data)
    u["selfie_url"] = f"/photos/{name}"
    u["selfie_status"] = "pending"
    u["selfie_checks"] = verdict["checks"]
    return {"success": True, "url": u["selfie_url"], "status": "pending", "checks": verdict["checks"],
            "message_telugu": "🤳 Selfie clear ga undi — verification ki vellindi ✅ (admin approve cheyagane badge vastundi)"}


@app.get("/api/admin/photos/pending")
def admin_photos_pending(request: Request):
    """📸 ADMIN — photo + selfie moderation queue (Layer-2 human review)."""
    require_admin(request)
    q = []
    for u in DB_USERS:
        _first = str(u.get("full_name", "")).split()[0] if str(u.get("full_name", "")).split() else ""
        if u.get("photo_status") == "pending":
            q.append({"kind": "photo", "tsap_id": u.get("tsap_id"), "name": _first,
                      "url": u.get("photo_url", ""), "checks": u.get("photo_checks", {}),
                      "at": u.get("photo_uploaded_at", "")})
        if u.get("selfie_status") == "pending":
            q.append({"kind": "selfie", "tsap_id": u.get("tsap_id"), "name": _first,
                      "url": u.get("selfie_url", ""), "checks": u.get("selfie_checks", {}), "at": ""})
    return {"success": True, "count": len(q), "queue": q}


@app.post("/api/admin/photos/review")
def admin_photos_review(payload: dict, request: Request):
    """📸 ADMIN — approve/reject photo or selfie (wrong-person/group/celebrity → reject)."""
    require_admin(request)
    d = payload or {}
    u = next((x for x in DB_USERS if x.get("tsap_id") == str(d.get("tsap_id", ""))), None)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    kind = str(d.get("kind", "photo"))
    decision = str(d.get("decision", ""))
    if kind not in ("photo", "selfie") or decision not in ("approved", "rejected"):
        raise HTTPException(400, "kind=photo/selfie, decision=approved/rejected ivvandi")
    te_reason = str(d.get("reason_te", "") or d.get("reason", "")).strip()
    if kind == "photo":
        u["photo_status"] = decision
        if decision == "approved":
            u["has_photo"] = True
            u["photo_urls"] = [u.get("photo_url", "")] if u.get("photo_url") else []
            u["photo_reason"] = ""
            u["photo_reason_te"] = ""
        else:
            u["has_photo"] = False
            u["photo_reason"] = str(d.get("reason", "Photo not approved") or "Photo not approved")
            u["photo_reason_te"] = te_reason or "ఈ ఫోటో approve kaledu — మీ clear original ఫోటో మళ్లీ పంపండి"
    else:
        u["selfie_status"] = decision
        u["selfie_verified"] = (decision == "approved")
    return {"success": True, "tsap_id": u["tsap_id"], "kind": kind, "decision": decision,
            "message_telugu": ("✅ Approve ayyindi" if decision == "approved" else "❌ Reject ayyindi — user ki reason vellindi")}


# ---------------------------------------------------------------------------
# 🌊 WAVE 18 — PASSWORD AUTH (number + password login, forgot/reset via OTP)
# pbkdf2_hmac-sha256 + random salt (stdlib only — bcrypt dependency vaddu).
# ---------------------------------------------------------------------------
import hashlib as _hashlib
import secrets as _secrets

PW_LOCKS: Dict[str, Dict[str, Any]] = {}   # phone → {fails, locked_until}


def _hash_password(pw: str) -> str:
    salt = _secrets.token_hex(16)
    h = _hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(salt), 120_000)
    return f"pbkdf2${salt}${h.hex()}"


def _check_password(pw: str, stored: str) -> bool:
    try:
        algo, salt, hexh = (stored or "").split("$")
        if algo != "pbkdf2":
            return False
        h = _hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(salt), 120_000)
        return _secrets.compare_digest(h.hex(), hexh)
    except Exception:
        return False


def _pw_locked(phone: str) -> str:
    rec = PW_LOCKS.get(phone) or {}
    try:
        if rec.get("locked_until") and datetime.fromisoformat(rec["locked_until"]) > datetime.utcnow():
            return rec["locked_until"]
    except Exception:
        pass
    return ""


def _pw_fail(phone: str) -> int:
    rec = PW_LOCKS.get(phone) or {"fails": 0}
    rec["fails"] = int(rec.get("fails", 0)) + 1
    if rec["fails"] >= 5:
        rec["locked_until"] = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
        rec["fails"] = 0
        abuse_log("pw_locked", phone[-4:])
    PW_LOCKS[phone] = rec
    return rec["fails"]


@app.post("/api/auth/login-password")
def auth_login_password(payload: dict):
    """🔑 Number + password login (OTP alternative). 5 wrong → 15 min lock."""
    d = payload or {}
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    pw = str(d.get("password", ""))
    if len(phone) != 10 or not pw:
        raise HTTPException(400, "10-digit number + password ivvandi")
    if _pw_locked(phone):
        raise HTTPException(429, "🔒 5 sarlu tappu — 15 nimushalalo malli try cheyyandi (leda OTP tho login)")
    u = next((x for x in DB_USERS if x.get("phone") == phone), None)
    if not u or not u.get("password_hash") or not _check_password(pw, u["password_hash"]):
        left = 5 - _pw_fail(phone)
        raise HTTPException(401, f"❌ Number/Password tappu (migilindi: {max(left, 0)} tries) — leda OTP tho login cheyyandi")
    PW_LOCKS.pop(phone, None)
    return {"success": True, "tsap_id": u["tsap_id"], "auth_token": sign_token(u["tsap_id"]),
            "has_account": True, "profile": safe_user(u),
            "message_telugu": f"✅ Welcome back, {str(u.get('full_name', '')).split()[0] if str(u.get('full_name', '')).split() else ''}! 🙏"}


@app.post("/api/auth/forgot")
def auth_forgot(payload: dict):
    """🔑 Forgot password — reset OTP (purpose=reset) pampistham."""
    d = dict(payload or {})
    d["purpose"] = "reset"
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    if len(phone) != 10:
        raise HTTPException(400, "10 digit mobile number ivvandi")
    return otp_send(d)


@app.post("/api/auth/reset")
def auth_reset(payload: dict):
    """🔑 Reset password — OTP verify + kotha password set."""
    d = payload or {}
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    code = str(d.get("code", "")).strip()
    new_pw = str(d.get("new_password", "")).strip()
    if len(phone) != 10 or not code:
        raise HTTPException(400, "Number + OTP ivvandi")
    if len(new_pw) < 6 or len(new_pw) > 72:
        raise HTTPException(400, "🔑 Kotha password 6–72 characters undali")
    rec = DB_OTPS.get(phone)
    if not rec or rec.get("purpose") not in ("reset", "login"):
        raise HTTPException(400, "Mundu reset OTP pampandi (/api/auth/forgot)")
    try:
        if datetime.fromisoformat(rec["expires"]) < datetime.utcnow():
            DB_OTPS.pop(phone, None)
            raise HTTPException(400, "OTP expire ayyindi — malli pampandi")
    except HTTPException:
        raise
    except Exception:
        pass
    if code != rec.get("code"):
        raise HTTPException(400, "❌ OTP tappu — malli try cheyyandi")
    u = next((x for x in DB_USERS if x.get("phone") == phone), None)
    if not u:
        raise HTTPException(404, "Ee number tho account ledu — mundu register avvandi")
    u["password_hash"] = _hash_password(new_pw)
    u["phone_verified"] = True
    DB_OTPS.pop(phone, None)
    PW_LOCKS.pop(phone, None)
    return {"success": True, "tsap_id": u["tsap_id"], "auth_token": sign_token(u["tsap_id"]),
            "message_telugu": "✅ Password marchindi — ippudu number + password tho login cheyyandi 🔑"}


@app.post("/api/otp/send")
def otp_send(payload: dict):
    """
    Phone OTP — 4 digit. Dev mode (OTP_DEV_MODE=true) lo code response lo vasthundi (SMS provider ledu).
    Production: SMS provider (MSG91 / Fast2SMS) configure chesi, code ni akkada pampali.
    """
    d = payload or {}
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    if len(phone) != 10:
        raise HTTPException(400, "10 digit mobile number ivvandi")
    # 🛡️ WAVE 9 — OTP abuse fix: 60s cooldown + 5/hour per phone (SMS cost + brute force)
    _prev = DB_OTPS.get(phone) or {}
    if _prev.get("sent_at"):
        try:
            _age = (datetime.utcnow() - datetime.fromisoformat(_prev["sent_at"])).total_seconds()
            if _age < 60:
                return JSONResponse(status_code=429, content={
                    "success": False, "retry_after": int(60 - _age),
                    "message_telugu": f"⏳ {int(60 - _age)} sec tarvata malli OTP pampistham (cooldown)"})
        except Exception:
            pass
    _hour = [t for t in _prev.get("history", []) if t > (datetime.utcnow() - timedelta(hours=1)).isoformat()]
    if len(_hour) >= 5:
        abuse_log("otp_hour_limit", phone[-4:])
        return JSONResponse(status_code=429, content={
            "success": False, "message_telugu": "⚠️ Ganta lo 5 OTP limit — 1 hour tarvata try cheyyandi (abuse protection)"})
    code = f"{random.randint(1000, 9999)}"
    purpose = str(d.get("purpose", "login")).strip()[:16] or "login"
    DB_OTPS[phone] = {"code": code, "expires": (datetime.utcnow() + timedelta(minutes=10)).isoformat(),
                      "tries": 0, "sent_at": datetime.utcnow().isoformat(), "purpose": purpose,
                      "history": (_hour + [datetime.utcnow().isoformat()])[-10:]}
    # 🌊 WAVE 18 — FREE channels first (WA bridge → Telegram → SMS), dev fallback
    ch = otp_channel_send(phone, code, DB_USERS)
    DB_OTPS[phone]["channel"] = ch.get("channel", "dev")
    dev = str(os.getenv("OTP_DEV_MODE", "true")).lower() in ("1", "true", "yes", "on")
    out = {"success": True, "phone": f"XXXXXX{phone[-4:]}", "expires_in_min": 10,
           "channel": ch.get("channel", "dev"), "purpose": purpose,
           "message_telugu": f"{CHANNEL_TELUGU.get(ch.get('channel', 'dev'), '')} (+91 XXXXXX{phone[-4:]}). 10 nimushalalo enter cheyyandi."}
    if dev:
        out["dev_code"] = code
        out["message_telugu"] += f" [DEV — code: {code}]"
        out["note"] = "Production: WHATSAPP_MODE=bridge (FREE) leda MSG91_KEY pettandi — appudu code response lo raadu."
    return out


@app.post("/api/otp/verify")
def otp_verify(payload: dict):
    d = payload or {}
    phone = "".join(ch for ch in str(d.get("phone", "")) if ch.isdigit())
    code = str(d.get("code", "")).strip()
    rec = DB_OTPS.get(phone)
    if not rec:
        raise HTTPException(400, "Mundu OTP pampandi")
    try:
        if datetime.fromisoformat(rec["expires"]) < datetime.utcnow():
            DB_OTPS.pop(phone, None)
            raise HTTPException(400, "OTP expire ayyindi — malli pampandi")
    except HTTPException:
        raise
    except Exception:
        pass
    rec["tries"] = int(rec.get("tries", 0)) + 1
    if rec["tries"] > 5:
        DB_OTPS.pop(phone, None)
        abuse_log("otp_locked", phone[-4:])
        abuse_count("otp_locked")
        raise HTTPException(429, "Chala sarlu try chesaru — kotha OTP teesukondi (15 min lock)")
    if code != rec["code"]:
        return JSONResponse(status_code=400, content={"success": False, "message_telugu": "❌ OTP tappu — malli try cheyyandi",
                                                      "tries_left": max(0, 5 - rec["tries"])})
    VERIFIED_PHONES.add(phone)
    DB_OTPS.pop(phone, None)
    u = next((x for x in DB_USERS if x.get("phone") == phone), None)
    if u:
        u["phone_verified"] = True
    # 🔐 WAVE 9 — login: OTP verify ayyaka auth token (private API ki)
    _tid = (u or {}).get("tsap_id", "")
    return {"success": True, "phone_verified": True,
            "tsap_id": _tid, "auth_token": sign_token(_tid) if _tid else "",
            "has_account": bool(u),
            "profile": safe_user(u) if u else None,
            "quality": profile_completeness(u) if u else None,
            "message_telugu": ("✅ Number verify ayyindi — mee profile ki verified badge vasthundi"
                               if u else "✅ Number verify ayyindi — ippudu 3 nimushalalo register cheyyandi (FREE 3 profiles)")}


@app.get("/api/home/teasers")
def home_teasers(limit: int = 8):
    """🏠 Homepage teaser profiles — RANDOM approved, safe_user only (blur+lock frontend lo).
    Register/login ki push cheyyadaniki — numbers/photos-full evvamu."""
    pool = [u for u in DB_USERS if u.get("is_approved")]
    random.shuffle(pool)
    rows = []
    for u in pool[:max(1, min(int(limit or 8), 12))]:
        r = safe_user(u)
        r["blur"] = True
        r["photo_url"] = ""          # teaser lo clear photo vaddu — attract kosam blur tile
        rows.append(r)
    return {"success": True, "count": len(rows), "teasers": rows,
            "cta_telugu": "🔒 Full details + photo chudali ante REGISTER (FREE) — 3 nimishalalo!"}


@app.get("/api/search")
def advanced_search(
    gender: Optional[str] = None, caste: Optional[str] = None, district: Optional[str] = None,
    state: Optional[str] = None, job: Optional[str] = None, education: Optional[str] = None,
    age_min: int = 18, age_max: int = 60, salary_min: int = 0,
    marital_status: Optional[str] = None, children: Optional[str] = None,
    verified_only: bool = False, photo_only: bool = False,
    religion: Optional[str] = None, q: Optional[str] = None,
    sort: str = "score", viewer_id: Optional[str] = None, limit: int = 30, offset: int = 0,
    nri_only: bool = False, profession_first: bool = False,
    salary_max: int = 0, height_min: str = "", height_max: str = "", dosham: Optional[str] = None,
    star: Optional[str] = None, min_completeness: int = 0, exclude_viewed: bool = False,
    exclude_interested: bool = False, with_facets: bool = False,
):
    """
    🔎 Advanced filters — caste / district / age range / salary / job / verified / photo / search text.
    Frontend /matches page idi use chestundi (fallback: demo data).
    """
    # 🛡️ WAVE 9 — clamp + sanitize (mundu limit=-1 → 75 rows; age_min>age_max silently 0 results)
    limit = clamp_int(limit, "limit", 1, 100, 30)
    offset = clamp_int(offset, "offset", 0, 100000, 0)
    for _b in (verified_only, photo_only, exclude_viewed, exclude_interested, with_facets):
        pass  # bool params — FastAPI coerce chestundi
    age_min = clamp_int(age_min, "age_min", 18, 70, 18)
    age_max = clamp_int(age_max, "age_max", 18, 70, 60)
    if age_min > age_max:
        validation_error("age_min", "⚠️ age_min < age_max undali (age range tappu)")
    salary_min = clamp_int(salary_min, "salary_min", 0, 100_000_000, 0)
    if sort not in ("score", "new", "age", "porutham", "boosted", "trust", "completeness"):
        validation_error("sort", "⚠️ sort ki valid values: score | new | age | porutham | boosted | trust | completeness")
    q = clean(q, 60, "q") if q else None
    for _f in (gender, caste, district, state, job, education, marital_status, religion):
        if _f and len(str(_f)) > 60:
            validation_error("filter", "⚠️ Filter value chala peddadi (60 chars max)")
    if min_completeness:
        min_completeness = req_int(min_completeness, "min_completeness", 0, 100, default=0)

    items = [u for u in DB_USERS if u.get("is_approved", True)]
    if viewer_id:
        items = [u for u in items if not safety.is_blocked(viewer_id, u.get("tsap_id", ""), DB_BLOCKS)]
    else:
        items = [u for u in items if not u.get("is_banned")]
    if gender:
        items = [u for u in items if str(u.get("gender", "")).lower() == gender.lower()]
    if caste:
        cl = caste.lower()
        items = [u for u in items if cl in str(u.get("caste", "")).lower() or cl in str(u.get("sub_caste", "")).lower()]
    if district:
        dl = district.lower()
        items = [u for u in items if dl in str(u.get("district", "")).lower() or dl in str(u.get("current_city", "")).lower()]
    if state:
        items = [u for u in items if str(u.get("state", "")).upper() == state.upper()]
    if job:
        jl = job.lower()
        items = [u for u in items if jl in str(u.get("job", "")).lower() or jl in str(u.get("work_type", "")).lower()]
    if education:
        el = education.lower()
        items = [u for u in items if el in str(u.get("education", "")).lower()]
    if marital_status:
        items = [u for u in items if str(u.get("marital_status", "")).lower() == marital_status.lower()]
    if children:
        items = [u for u in items if str(u.get("children", "None")) == children]
    if religion:
        items = [u for u in items if str(u.get("religion", "Hindu")).lower() == religion.lower()]
    if nri_only:                                    # 🌊 WAVE 14 — NRI-only browse
        items = [u for u in items if _is_nri(u)]
    if verified_only:
        items = [u for u in items if u.get("is_verified") or u.get("phone_verified")]
    if photo_only:
        items = [u for u in items if u.get("photo_urls")]
    items = [u for u in items if age_min <= int(u.get("age", 0) or 0) <= age_max]
    if salary_max:
        def _sal_max(u):
            raw = str(u.get("salary", "")).lower().replace("l", "00000").replace("k", "000")
            digits = "".join(ch for ch in raw if ch.isdigit())
            return int(digits) if digits else 0
        items = [u for u in items if 0 < _sal_max(u) <= salary_max]
    if height_min or height_max:
        from quality import _height_cm
        lo_cm, hi_cm = _height_cm(height_min) if height_min else 0, _height_cm(height_max) if height_max else 999
        items = [u for u in items if _height_cm(u.get("height")) and lo_cm <= _height_cm(u.get("height")) <= hi_cm]
    if dosham:
        items = [u for u in items if str(u.get("dosham", "No")).lower() == dosham.lower()]
    if star:
        items = [u for u in items if star.lower() in str(u.get("star", "")).lower()]
    if min_completeness:
        items = [u for u in items if profile_completeness(u)["percent"] >= min_completeness]
    if exclude_viewed and viewer_id:
        viewed = {v.get("tsap_id") for v in DB_VIEWS if v.get("viewer_id") == viewer_id}
        items = [u for u in items if u.get("tsap_id") not in viewed]
    if exclude_interested and viewer_id:
        touched = {i.get("to_id") for i in DB_INTERESTS if i.get("from_id") == viewer_id}
        touched |= {i.get("from_id") for i in DB_INTERESTS if i.get("to_id") == viewer_id}
        items = [u for u in items if u.get("tsap_id") not in touched]
    if salary_min:
        def _sal(u):
            raw = str(u.get("salary", "")).lower().replace("l", "00000").replace("k", "000")
            digits = "".join(ch for ch in raw if ch.isdigit())
            return int(digits) if digits else 0
        items = [u for u in items if _sal(u) >= salary_min]
    if q:
        ql = q.lower()
        items = [u for u in items
                 if ql in str(u.get("full_name", "")).lower() or ql in str(u.get("district", "")).lower()
                 or ql in str(u.get("caste", "")).lower() or ql in str(u.get("job", "")).lower()]

    viewer = _find_user(viewer_id) if viewer_id else None
    out = []
    for u in items:
        row = safe_user(u)
        row["phone_verified"] = bool(u.get("phone_verified") or u.get("is_verified"))
        row["has_photo"] = bool(u.get("photo_urls"))
        row["boosted"] = bool(u.get("boost_until"))
        row["marital_status"] = u.get("marital_status", "—")
        row["salary"] = u.get("salary", "—")
        row["company"] = u.get("company", "")
        row["sub_caste"] = u.get("sub_caste", "")
        row["moola_nakshatram"] = u.get("moola_nakshatram", "No")
        row["is_nri"] = _is_nri(u)
        row["profession_label"] = _prof_label(u)
        row["country"] = u.get("country", "India")
        badge = safety.verification_badge(u)
        row["verification"] = badge["level"]
        row["verification_telugu"] = badge["telugu"]
        row["trust_score"] = badge["trust_score"]
        if viewer and viewer.get("gender") != u.get("gender"):
            try:
                v2 = topmatch.score_match_v2(viewer, u)          # 🧠 Match Score 2.0 (explainable)
                row["score"] = v2["score"]
                row["reasons"] = v2["strengths"] + ([v2["mutual"]["note"]] if v2.get("mutual", {}).get("both_like") else [])
                row["match_v2"] = {"grade": v2["grade"], "verdict": v2["verdict_telugu"],
                                   "mutual": v2.get("mutual", {}), "breakdown": v2["breakdown"][:6],
                                   "weak_points": v2["weak_points"], "how_to_improve": v2["how_to_improve"]}
            except Exception:
                row["score"], row["reasons"] = _score_pair(viewer, u)
            src = compute_porutham(u, viewer) if viewer.get("gender") == "Groom" else compute_porutham(viewer, u)
            row["porutham"] = {"score": src.get("score"), "max": src.get("max_score"),
                               "verdict": src.get("verdict")} if src.get("available") else None
        out.append(row)

    if sort == "trust":
        out.sort(key=lambda x: -int((x.get("trust") or {}).get("score", 0) if isinstance(x.get("trust"), dict)
                                    else (x.get("trust_score") or 0)))
    elif sort == "completeness":
        out.sort(key=lambda x: -int(x.get("quality_percent", 0) or 0))
    elif sort == "score" and viewer:
        out.sort(key=lambda x: -int(x.get("score", 0) or 0))
    elif sort == "new":
        out.sort(key=lambda x: str(x.get("tsap_id", "")), reverse=True)
    elif sort == "age":
        out.sort(key=lambda x: int(x.get("age", 99) or 99))
    elif sort == "porutham":
        out.sort(key=lambda x: -int(((x.get("porutham") or {}).get("score") or 0)))
    elif sort == "boosted":
        out.sort(key=lambda x: (not x.get("boosted"), -int(x.get("score", 0) or 0)))
    if profession_first and viewer:                 # 🌊 WAVE 14 — profession affinity first
        out = MP.rerank_profession(viewer, out)

    return {
        "total": len(out), "count": len(out[offset:offset + limit]), "offset": offset, "limit": limit,
        "sort": sort,
        "filters": {"gender": gender, "caste": caste, "district": district, "state": state, "job": job,
                    "education": education, "age": [age_min, age_max], "salary_min": salary_min,
                    "marital_status": marital_status, "verified_only": verified_only, "photo_only": photo_only,
                    "religion": religion, "q": q},
        "results": out[offset:offset + limit],
        "facets": search_facets(out, 10) if with_facets else {},
        "message_telugu": f"🔎 {len(out)} profiles dorikayi (filters: caste={caste or 'Any'}, district={district or 'Any'}, age={age_min}-{age_max})",
    }


@app.get("/api/digest/preview")
def digest_preview():
    """
    📅 Daily 9AM digest — Telegram + WhatsApp ki pampadaniki ready text.
    (Cron/scheduler ee endpoint ni pilichi post cheyyali — anti-ban queue lo veltundi)
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")
    brides = [u for u in DB_USERS if u.get("gender") == "Bride"]
    grooms = [u for u in DB_USERS if u.get("gender") == "Groom"]
    by_caste: Dict[str, int] = {}
    for u in DB_USERS:
        c = u.get("caste") or "Other"
        by_caste[c] = by_caste.get(c, 0) + 1
    top = sorted(by_caste.items(), key=lambda x: -x[1])[:6]
    text = (
        f"🌅 *MANA VIVAHA — Nedu Kotha Profiles* ({today})\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👰 Brides: *{len(brides)}*   🤵 Grooms: *{len(grooms)}*\n"
        f"🔥 Top castes: " + ", ".join(f"{c} ({n})" for c, n in top) + "\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💌 Interest pampu → WhatsApp lo mee profile share\n"
        f"🎁 Modati 3 requests FREE • ₹99 → 5 profiles\n"
        f"📝 FREE register: {os.getenv('SITE_URL', 'https://manavivaha.in')}/register"
    )
    entry = {"at": datetime.utcnow().isoformat(), "brides": len(brides), "grooms": len(grooms)}
    DB_DIGEST.append(entry)
    return {"success": True, "text": text, "brides": len(brides), "grooms": len(grooms),
            "top_castes": top,
            "how_to_post": "POST /api/publish/digest cheyyandi → Telegram + WhatsApp (anti-ban gap tho) veltundi",
            "history": DB_DIGEST[-7:]}


@app.post("/api/publish/digest")
async def publish_digest(request: Request = None):
    """Digest ni Telegram live channels + WhatsApp queue ki (anti-ban gap tho) pampu."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    prev = digest_preview()
    text = prev["text"].replace("*", "*")  # WhatsApp formatting ki same
    targets = cfg_live = [c["chat_id"] for c in live_channels() if c.get("chat_id")]
    res = enqueue_whatsapp(publish_config()["wa_bridge_targets"], text, priority=1, kind="digest")
    tg = []
    for chat in targets:
        tg.append(await _send_telegram_public(chat, text))
    return {"success": True, "telegram": tg, "whatsapp": res, "text": text}


async def _send_telegram_public(chat: str, text: str):
    try:
        from publisher import _send_telegram as _st  # type: ignore
        return await _st(chat, text, None, publish_config())
    except Exception as e:
        return {"ok": False, "channel": chat, "error": str(e)[:120]}






# ============================================================================
#  VISITOR + LEAD CAPTURE  ("chusina vallu antha DB lo save")
# ============================================================================
@app.post("/api/track")
def api_track(payload: dict):
    """
    Frontend beacon — client-side info (screen, time on page, utm) tho visit ni enrich chestundi.
    Server middleware kooda prathi request ni track chestundi (double safety).
    """
    p = payload or {}
    rec = track_visit(str(p.get("ip", "")), str(p.get("ua", "")), str(p.get("path", "/")),
                      str(p.get("ref", "")), str(p.get("utm", "")), str(p.get("device", "")),
                      extra={"screen": p.get("screen", ""), "lang": p.get("lang", ""),
                             "seconds": p.get("seconds", ""), "visitor_id": p.get("visitor_id", "")})
    return {"success": True, "visitor_id": rec["vid"], "channel": rec["channel"],
            "visits_total": len(growth.DB_VISITORS)}


@app.post("/api/leads/quick")
def api_lead_quick(payload: dict):
    """
    Phone-first quick start: "number pettu — mana team mee profile complete chestundi" (FREE).
    3-minute register form ki mundu 30-second entry point (phone lo chala easy).
    """
    p = payload or {}
    # 🛡️ validation: phone 10-digit, name sanitize (mundu "x" phone tho junk leads vachevi)
    _pname = clean(p.get("name", ""), 60, "lead_name")
    _pphone = req_phone(p.get("phone", ""), "phone")
    ok, kind, lead = save_lead(_pname, _pphone,
                               gender=str(p.get("gender", "")), district=str(p.get("district", "")),
                               caste=str(p.get("caste", "")), age=str(p.get("age", "")),
                               source=str(p.get("source", "quick_form")), notes=str(p.get("notes", "")))
    if not ok:
        raise HTTPException(400, kind)
    cfg = publish_config()
    queued = {"queued": False}
    if cfg["wa_mode"] != "off" and kind == "new_lead":
        queued = enqueue_whatsapp([lead["phone"]], lead_followup_text(lead), priority=0, kind="lead_followup")
    return {"success": True, "lead_id": lead["id"], "kind": kind, "lead_status": lead.get("status"),
            "followup_queued": bool(queued.get("queued")), "wa_mode": cfg["wa_mode"],
            "next": "/register?phone=" + lead["phone"],
            "message_telugu": ("Number save ayyindi! Mana team 10 nimushalalo call chesi mee profile FREE ga "
                               "complete chestundi. Leda meeru ippude 3 nimushalalo register cheyyochu."),
            "whatsapp_link": "https://wa.me/91" + lead["phone"]}


@app.get("/api/leads")
def api_leads(status: str = "", limit: int = 100, request: Request = None):
    """Admin — leads list (follow-up ki). Deploy lo ADMIN_TOKEN env tho protect cheyyali."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return leads_list(status, limit)


@app.get("/api/leads/stats")
def api_lead_stats(request: Request = None):
    """Traffic + conversion dashboard: visits, channels, top pages, lead sources, inventory."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    st = lead_stats()
    st["inventory"] = inventory_status(len(DB_USERS))
    st["whatsapp"] = wa_queue_stats()
    # 🐞 FIX: mundu ee endpoint lo user/lead phone numbers (10-digit) public ga vachedi → mask
    if not is_admin(request):
        st = mask_pii(st)
        st["pii_masked"] = True
    return st


@app.post("/api/leads/followup/{lead_id}")
def api_lead_followup(lead_id: str, request: Request = None):
    """Lead ki WhatsApp follow-up pampu (mana side nunchi)."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    lead = next((l for l in growth.DB_LEADS if l["id"] == lead_id), None)
    if not lead:
        raise HTTPException(404, "Lead dorakaledu")
    cfg = publish_config()
    res = {"queued": False}
    if cfg["wa_mode"] != "off":
        res = enqueue_whatsapp([lead["phone"]], lead_followup_text(lead), priority=0, kind="lead_followup")
    lead["status"] = "contacted"
    lead["touches"] = int(lead.get("touches", 1)) + 1
    lead["contacted_at"] = datetime.utcnow().isoformat()
    return {"success": True, "lead": lead, "whatsapp": res, "wa_mode": cfg["wa_mode"],
            "message_telugu": "Follow-up WhatsApp queue lo pettam (anti-ban gap tho pothundi)"}


# ============================================================================
#  SHARE KIT — reach engine ("oka profile chala mandi chudalanukune la")
# ============================================================================
@app.get("/api/share/kit/{tsap_id}")
def api_share_kit(tsap_id: str):
    u = _find_user(tsap_id) or _find_user(tsap_id.upper())
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    return share_kit(u, u["tsap_id"], hashtags=u.get("post_hashtags"))


@app.get("/api/inventory")
def api_inventory():
    """Launch readiness — '300-400 profiles chalu' gauge + ela fill cheyyalo."""
    inv = inventory_status(len(DB_USERS))
    brides = len([u for u in DB_USERS if u.get("gender") == "Bride"])
    return dict(inv, brides=brides, grooms=len(DB_USERS) - brides,
                castes_covered=len({u.get("caste") for u in DB_USERS if u.get("caste")}),
                districts_covered=len({u.get("district") for u in DB_USERS if u.get("district")}),
                verified=len([u for u in DB_USERS if u.get("phone_verified") or u.get("is_verified")]),
                photos=len([u for u in DB_USERS if u.get("photo_urls")]))


# ============================================================================
#  LAUNCH INVENTORY LOAD (300-400 profiles — channels khali ga kanipinchavu)
# ============================================================================
@app.post("/api/admin/bulk-profiles")
def api_bulk_profiles(payload: dict, request: Request = None):
    """
    Launch inventory load — realistic profiles (seed_launch_db.py nunchi).
    body: {"profiles": [ ... ]}  leda  {"generate": 360}
    """
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    import seed_launch_db
    # 🐞 FIX: mundu {"profiles": "notalist"} / [1,2,3] ki 500 vachedi
    profiles = (payload or {}).get("profiles") or []
    if profiles and not isinstance(profiles, list):
        validation_error("profiles", "⚠️ profiles ki LIST pampandi (leda {'generate': 360})")
    bad = [i for i, p in enumerate(profiles[:500]) if not isinstance(p, dict)]
    if bad:
        validation_error("profiles", f"⚠️ Profiles lo {len(bad)} items dict kaadu (index {bad[:3]}) — check cheyyandi")
    profiles = [p for p in profiles[:500] if isinstance(p, dict)]
    if not profiles:
        gen = int((payload or {}).get("generate", 0) or 0)
        if not gen:
            raise HTTPException(400, "profiles list ivvandi leda {generate: 360} pampandi")
        profiles = seed_launch_db.build_profiles(gen, int((payload or {}).get("seed", 42)))
    added, skipped = 0, 0
    for sd in profiles:
        phone = str(sd.get("phone", ""))
        if phone and any(u.get("phone") == phone for u in DB_USERS):
            skipped += 1
            continue
        u = dict(sd)
        u["demo"] = True                       # 🎬 seed/inventory profile — demo login allowed (real users ki OTP)
        u.setdefault("tsap_id", unique_tsap_id(sd.get("gender", "Bride"), 2025))
        u.setdefault("religion", "Hindu")
        u.setdefault("mother_tongue", "Telugu")
        u.setdefault("gothram", "-")
        u.setdefault("credit_history", [])
        u.setdefault("referral_stats", {"total": 0, "earned": 0})
        u.setdefault("is_approved", True)
        u.setdefault("photo_urls", [])
        u.setdefault("card_url", "/cards/" + u["tsap_id"] + ".png")
        u["credits"] = int(u.get("credits", 3) or 3)
        u["plan"] = u.get("plan", "FREE")
        if phone:
            u["phone_last4"] = phone[-4:]
            u["phone_encrypted"] = encrypt_phone(phone)
        DB_USERS.append(u)
        added += 1
    return {"success": True, "added": added, "skipped": skipped, "total_users": len(DB_USERS),
            "inventory": inventory_status(len(DB_USERS)),
            "message_telugu": "%d profiles load ayyayi (total %d) — channels ippudu rich ga kanipistayi"
                              % (added, len(DB_USERS))}


@app.post("/api/admin/seed-launch")
def api_seed_launch(payload: dict = None, request: Request = None):
    """Shortcut: demo profiles ventane load (dev/preview ki). DEMO_SEED_ENABLED=false chesthe bandh."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    if str(os.getenv("DEMO_SEED_ENABLED", "true")).lower() not in ("1", "true", "yes", "on"):
        raise HTTPException(403, "Demo seed bandh (DEMO_SEED_ENABLED=false)")
    return api_bulk_profiles({"generate": int((payload or {}).get("count", 60)),
                              "seed": int((payload or {}).get("seed", 42))})




# ============================================================================
#  MATCH SCORE 2.0 — explainable + mutual (why ee score? Telugu lo cheptham)
# ============================================================================
@app.get("/api/match/score")
def api_match_score(a: str, b: str):
    me, other = _find_user(a), _find_user(b)
    if not me or not other:
        raise HTTPException(404, "Rendu TSAP IDs correct ga ivvandi")
    if safety.is_blocked(a, b, DB_BLOCKS):
        raise HTTPException(400, "Ee profile block ayyindi")
    res = topmatch.score_match_v2(me, other)
    res["viewer"] = a
    res["other"] = {"tsap_id": other.get("tsap_id"), "full_name": other.get("full_name"),
                    "verification": safety.verification_badge(other)}
    res["gothram"] = A11.gothram_check(me, other)   # 🛡️ WAVE 11: score tho paatu gothram verdict
    res["surname"] = S12.same_surname_check(me, other)   # 🛡️ WAVE 13: surname verdict kooda
    res["age_rule"] = MP.age_rule_check(me, other)            # 🌊 WAVE 14: vayasu verdict kooda
    return res


@app.post("/api/match/score")
def api_match_score_raw(payload: dict):
    """Raw dicts tho score (frontend preview / admin tools ki)."""
    d = payload or {}
    a, b = d.get("a") or {}, d.get("b") or {}
    if not a or not b:
        raise HTTPException(400, "a + b (profile dicts) kavali")
    return topmatch.score_match_v2(a, b)


@app.get("/api/top-matches/{tsap_id}")
def api_top_matches(tsap_id: str, limit: int = 10, min_score: int = 65, include_same_gothram: int = 0,
                      include_same_surname: int = 0, include_age_block: int = 0, nri_only: int = 0):
    """Top matches 2.0 — mutual bonus tho rank, blocked/banned/same-gothram teesestham, boosted first."""
    me = _find_user(tsap_id)
    if not me:
        raise HTTPException(404, "Mee profile dorakaledu")
    pool = [u for u in DB_USERS if not safety.is_blocked(tsap_id, u.get("tsap_id", ""), DB_BLOCKS)
            and not u.get("is_banned")]
    # 🛡️ WAVE 11: same-gothram auto-filter (?include_same_gothram=1 tho chudochu)
    g11skip = []
    if not include_same_gothram:
        gf = A11.filter_same_gothram(me, pool)
        pool, g11skip = gf["kept"], gf["skipped_ids"]
    # 🛡️ WAVE 13: same-surname auto-filter (?include_same_surname=1 tho chudochu)
    s13skip = []
    if not include_same_surname:
        sf = S12.filter_same_surname(me, pool)
        pool, s13skip = sf["kept"], sf["skipped_ids"]
    # 🌊 WAVE 14: AGE RULE auto-filter (?include_age_block=1) + NRI-only (?nri_only=1)
    a14skip = []
    if not include_age_block:
        af = MP.filter_age_ok(me, pool)
        pool, a14skip = af["kept"], af["skipped_ids"]
    if nri_only:
        pool = [c for c in pool if _is_nri(c)]
    rows = topmatch.find_top_matches_v2(me, pool, limit=limit, min_score=min_score)
    # ⚡ WAVE 11: boosted profiles first (pay chesinavallaki value)
    rows.sort(key=lambda r: (A11.boost_rank_key(r.get("profile", {})), r.get("score", 0)), reverse=True)
    rows = MP.rerank_profession(me, rows)     # 🌊 WAVE 14: profession affinity first
    out = []
    for r in rows:
        prof = r.pop("profile")
        r["full_name"] = prof.get("full_name")
        r["age"] = prof.get("age")
        r["caste"] = prof.get("caste")
        r["district"] = prof.get("district")
        r["state"] = prof.get("state")
        r["education"] = prof.get("education")
        r["job"] = prof.get("job")
        r["star"] = prof.get("star")
        r["verification"] = safety.verification_badge(prof)["level"]
        r["boosted"] = A11.is_boosted(prof)
        r["voice_url"] = prof.get("voice_url", "")
        r["has_voice"] = bool(prof.get("voice_url"))
        r["gothram_ok"] = not A11.gothram_check(me, prof).get("same", False)
        r["children"] = prof.get("children", "None")
        r["is_nri"] = _is_nri(prof)
        r["profession_label"] = _prof_label(prof)
        out.append(r)
    return {"tsap_id": tsap_id, "count": len(out), "mutual_matches": len([x for x in out if x.get("mutual", {}).get("both_like")]),
            "gothram_skipped": len(g11skip), "gothram_skipped_ids": g11skip[:10],
            "surname_skipped": len(s13skip), "surname_skipped_ids": s13skip[:10],
            "age_skipped": len(a14skip), "age_skipped_ids": a14skip[:10],
            "nri_only": bool(nri_only),
            "results": out,
            "message_telugu": "%d top matches — mutthu (mutual) matches: %d%s%s%s%s" % (
                len(out), len([x for x in out if x.get("mutual", {}).get("both_like")]),
                f" · 🚫 same-gothram {len(g11skip)} skip" if g11skip else "",
                f" · 🚫 same-surname {len(s13skip)} skip" if s13skip else "",
                f" · 🚫 age-rule {len(a14skip)} skip" if a14skip else "",
                " · ✈️ NRI-only" if nri_only else "")}


# ============================================================================
#  TRUST & SAFETY — report / block / verify / moderation
# ============================================================================
@app.get("/api/safety/tips")
def api_safety_tips():
    return {"tips": safety.safety_tips(),
            "verify_levels": [{"level": k, "telugu": v} for k, v in safety.VERIFY_TELUGU.items()],
            "report_categories": [{"key": k, **v} for k, v in safety.REPORT_CATEGORIES.items()],
            "message_telugu": "Safety first: advance money vaddu, public lo kalthi, video call tho verify 🙏"}


@app.post("/api/report")
def api_report(payload: dict, request: Request = None):
    d = payload or {}
    require_owner(request, str(d.get("reporter_id", "")))   # 🛡️ IDOR: report mee peru tarvupuna
    _reporter = clean(d.get("reporter_id"), 30, "reporter_id")
    _target = clean(d.get("target_id"), 30, "target_id")
    if _reporter and _target and _reporter == _target:
        validation_error("target_id", "⚠️ Mee profile ni meeru report cheyyakkarledu")
    _detail = clean(d.get("detail", ""), 500, "detail", allow_newlines=True)
    _cat = clean(d.get("category", ""), 40, "category")
    dup = next((r for r in DB_REPORTS if r.get("reporter_id") == _reporter and r.get("target_id") == _target
                and str(r.get("category", "")) == _cat and r.get("status", "open") == "open"), None)
    if dup:
        return {"success": True, "kind": "already_reported", "report": dup,
                "message_telugu": "ℹ️ Ee profile ni meeru mundu report chesaru — mana team chustundi (48h lo action)"}
    ok, kind, rec = safety.submit_report(_reporter, _target, _cat, _detail,
                                         reports=DB_REPORTS, users=DB_USERS)
    if not ok:
        raise HTTPException(400, kind)
    return {"success": True, "kind": kind, "report": rec,
            "auto_hidden": bool(rec.get("auto_flagged")),
            "ack_telugu": safety.report_ack_text(),
            "stats": safety.report_stats(DB_REPORTS)}


@app.get("/api/moderation/queue")
def api_moderation_queue(limit: int = 50, request: Request = None):
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    return safety.moderation_queue(DB_REPORTS, DB_USERS, limit)


@app.post("/api/moderation/resolve/{report_id}")
def api_moderation_resolve(report_id: str, payload: dict = None, request: Request = None):
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    d = payload or {}
    ok, msg, rec = safety.resolve_report(report_id, str(d.get("action", "")), str(d.get("note", "")),
                                         reports=DB_REPORTS, users=DB_USERS)
    if not ok:
        raise HTTPException(400, msg)
    return {"success": True, "action": msg, "report": rec, "queue": safety.report_stats(DB_REPORTS)}


@app.post("/api/block")
def api_block(payload: dict, request: Request = None):
    """🚫 Block — safety first (blocked valla profile/interest rendu vaipula hide avutayi)."""
    d = payload or {}
    me = clean(d.get("tsap_id") or d.get("owner"), 30, "tsap_id")
    you = clean(d.get("block_id") or d.get("blocked") or d.get("target_id"), 30, "block_id")
    require_owner(request, me)                     # 🛡️ WAVE 9: IDOR fix
    if not me or not you:
        validation_error("block_id", "⚠️ tsap_id + block_id (leda owner + blocked) pampandi")
    if me == you:
        validation_error("block_id", "⚠️ Meere meeku block enduku 🙂")
    if not _find_user(me) or not _find_user(you):
        raise HTTPException(404, "Profile dorakaledu — TSAP ID check cheyyandi")
    _already = next((b for b in DB_BLOCKS
                     if (b.get("tsap_id") or b.get("owner")) == me
                     and (b.get("block_id") or b.get("blocked")) == you), None)
    if _already:
        return {"success": True, "already_blocked": True, "block": _already,
                "total_blocks": len(safety.block_list(me, DB_BLOCKS)),
                "message_telugu": "🚫 Ee profile mundu nunche block lo undi"}
    ok, kind, rec = safety.block_user(me, you, clean(d.get("reason", ""), 120, "reason"), DB_BLOCKS)
    if not ok:
        raise HTTPException(400, kind)
    rec.setdefault("block_id", you)                 # safety module 'blocked' key vadachu — rendu unchey
    return {"success": True, "kind": kind, "block": rec,
            "total_blocks": len(safety.block_list(me, DB_BLOCKS)),
            "message_telugu": "🚫 Block chesaru — vaallu mee profile chudalenu, interest kooda pampalenru"}


@app.post("/api/unblock")
def api_unblock(payload: dict, request: Request = None):
    d = payload or {}
    me = clean(d.get("tsap_id") or d.get("owner"), 30, "tsap_id")
    you = clean(d.get("block_id") or d.get("blocked"), 30, "block_id")
    require_owner(request, me)                     # 🛡️ WAVE 9: IDOR fix
    ok, msg = safety.unblock_user(me, you, DB_BLOCKS)
    return {"success": ok, "kind": msg, "total_blocks": len(safety.block_list(me, DB_BLOCKS)),
            "message_telugu": "✅ Unblock ayyindi — ippudu interest kooda pampochu" if ok else "Ee user block list lo ledu"}


@app.get("/api/blocks/{tsap_id}")
def api_blocks(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    rows = safety.block_list(tsap_id, DB_BLOCKS)
    return {"tsap_id": tsap_id, "count": len(rows), "items": rows}


@app.post("/api/verify/request")
def api_verify_request(payload: dict):
    """Phone / Photo / ID verification level penchadam (photo/ID ki admin approve kavali — dev lo auto)."""
    d = payload or {}
    u = _find_user(str(d.get("tsap_id", "")))
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    kind = str(d.get("kind", "")).lower()
    ok, msg, _ = safety.set_verification(u, kind)
    if not ok:
        raise HTTPException(400, msg)
    badge = safety.verification_badge(u)
    return {"success": True, "kind": msg, "verification": badge,
            "message_telugu": "✅ %s — %s" % (badge["telugu"], badge["next_step_telugu"])}


@app.get("/api/verification/{tsap_id}")
def api_verification(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)   # 🛡️ WAVE 9: IDOR fix — own data matrame
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    b = safety.verification_badge(u)
    return {"tsap_id": tsap_id, **b}


# ============================================================================
#  SOCIAL PREVIEW IMAGES (WhatsApp/Telegram link preview — reach booster)
# ============================================================================
@app.get("/api/og/profile/{tsap_id}.png")
def api_og_profile(tsap_id: str):
    u = _find_user(tsap_id) or next((x for x in DB_USERS if x["tsap_id"].upper() == tsap_id.upper()), None)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    path = preview.og_profile_png(u)
    if not path or not os.path.exists(path):
        raise HTTPException(500, "Preview generate avvaledu (Pillow/font check cheyyandi)")
    return FileResponse(path, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"})


@app.get("/api/og/porutham/{bride}/{groom}.png")
def api_og_porutham(bride: str, groom: str):
    b, g = _find_user(bride), _find_user(groom)
    if not b or not g:
        raise HTTPException(404, "Rendu profiles kavali")
    res = compute_porutham(b, g)
    path = preview.og_porutham_png(b, g, res)
    if not path or not os.path.exists(path):
        raise HTTPException(500, "Preview generate avvaledu")
    return FileResponse(path, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"})


@app.get("/api/og/site.png")
def api_og_site(title: str = "Mana Vivaha — Telugu Matrimony", subtitle: str = "65 channels • 43 castes • TS + AP"):
    path = preview.og_generic_png(title, subtitle, name="site")
    if not path or not os.path.exists(path):
        raise HTTPException(500, "Preview generate avvaledu")
    return FileResponse(path, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"})



# ---------------------------------------------------------------------------
# 🏪 VENDOR ADS + PROMOTIONS — catering / photography / decorations / halls...
#    "Pelli sambandham related vaallaki promotions kooda cheyyali bestga"
# ---------------------------------------------------------------------------
# ============================================================================
# 🛡️ WAVE 9 — HARDENING / TRUST / ADVANCED ENDPOINTS
# ============================================================================
@app.get("/api/security/posture")
def security_posture_endpoint():
    """Public security posture (trust page ki): auth, headers, rate limit, numbers policy."""
    p = security_posture()
    p["numbers_policy_telugu"] = ("🔒 Phone numbers public API lo eppudu ledu (98••••••45 mask) — "
                                  "interest accept (consent) tho matrame exchange")
    p["data_practices_telugu"] = [
        "Mee number DB lo encrypted column lo — public responses lo asalu radu",
        "Consent ledger: numbers eppudu evariki exchange ayyayo record untundi (dispute ki proof)",
        "Rate limit + OTP lock: broker/spam calls aapadaniki",
        "Admin endpoints ki key — PII leaks block chesam",
    ]
    return p


@app.get("/api/auth/verify")
def auth_verify(request: Request = None):
    """Token valid aa? Frontend login state ki (evariki token undo cheptundi, PII ledu)."""
    ident = token_from_request(request)
    if not ident:
        return JSONResponse(status_code=401, content={"success": False, "valid": False,
                                                      "message_telugu": "🔒 Token ledu/expire — OTP login cheyyandi"})
    u = _find_user(ident["tsap_id"])
    return {"success": True, "valid": True, "tsap_id": ident["tsap_id"],
            "expires_in_hours": int((ident["exp"] - datetime.utcnow().timestamp()) // 3600),
            "user": safe_user(u) if u else None,
            "admin_key_ok": is_admin(request)}


@app.post("/api/auth/demo-token")
def auth_demo_token(payload: dict = Body(default={}), request: Request = None):
    """
    🎬 Demo/seed profiles ki token (preview/demo lo browsing ki). **Real users ki kaadu** —
    vaallu OTP (login) use cheyyali. DEMO_LOGIN=0 tho off cheyyachu.
    """
    if str(os.getenv("DEMO_LOGIN", "1")).lower() in ("0", "false", "no", "off"):
        raise HTTPException(403, "🔒 Demo login off lo undi — OTP tho login cheyyandi")
    tid = clean((payload or {}).get("tsap_id"), 30, "tsap_id")
    u = _find_user(tid)
    if not u:
        raise HTTPException(404, "Demo profile dorakaledu")
    is_seed = bool(u.get("demo") or u.get("is_demo") or u.get("inventory_status") or u.get("seed"))
    if not is_seed and not dev_mode():
        raise HTTPException(403, "🔒 Idi demo profile kaadu — OTP (phone) tho login cheyyandi")
    return {"success": True, "tsap_id": tid, "auth_token": sign_token(tid), "demo": True,
            "user": safe_user(u), "message_telugu": "🎬 Demo login — real users ki OTP login (phone) undi"}


@app.get("/api/profile/{tsap_id}/quality")
def profile_quality(tsap_id: str):
    """⭐ Profile completeness % + trust score + Telugu next steps (register/profile improve ki)."""
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    mine = [i for i in DB_INTERESTS if tsap_id in (i.get("from_id"), i.get("to_id"))]
    comp = profile_completeness(u)
    trust = trust_score(u, mine)
    return {"tsap_id": tsap_id, "completeness": comp, "trust": trust,
            "grade_telugu": ("🏆 Superb profile — top matches lo kanipisthundi" if comp["percent"] >= 85
                             else "👍 Manchi profile — konchem add chesthe inka best" if comp["percent"] >= 60
                             else "✍️ Inka fill cheyyalsindi chala undi — ippude complete cheyyandi"),
            "photo_tip_telugu": "📸 Clear photo (face) unna profiles ki 5x views — privacy mode kooda undi (blur option)",
            "badge_preview_telugu": trust["badge_telugu"]}


@app.get("/api/facets")
def search_facets_endpoint(gender: Optional[str] = None, limit: int = 12):
    """🔎 Search UI chips ki counts (caste/district/education/job) — advanced filter UX."""
    limit = clamp_int(limit, "limit", 1, 30, 12)
    items = [u for u in DB_USERS if not u.get("is_banned") and u.get("is_approved", True)]
    if gender:
        items = [u for u in items if str(u.get("gender", "")).lower() == clean(gender, 10).lower()]
    return {"total": len(items), "facets": search_facets(items, limit),
            "note_telugu": "Ee counts ippudu unna profiles batti — filter click chesi chudandi"}


@app.get("/api/templates/interest")
def interest_template_list():
    """💬 Ready-made Telugu interest messages (spam takkuva, response ekkuva)."""
    return {"templates": quality_templates(),
            "tip_telugu": "Short + family mention + city/job reference unte replies ekkuva vasthayi",
            "rule_telugu": "Copy chesi mee style lo edit cheskovachu — numbers ee stage lo ivvamu (consent tho tarvata)"}


@app.post("/api/saved-searches")
def saved_search_create(payload: dict = Body(default={}), request: Request = None):
    """🔔 Search save cheyyandi — kotha profiles vaste WhatsApp alert (advanced feature)."""
    d = payload or {}
    tsap_id = clean(d.get("tsap_id"), 30, "tsap_id")
    require_owner(request, tsap_id)
    if not _find_user(tsap_id):
        raise HTTPException(404, "Mee profile dorakaledu")
    rec = save_search(tsap_id, d.get("name", ""), d.get("filters") or {}, alert=req_bool(d.get("alert", True)))
    return {"success": True, "search": rec, "total": len(saved_for(tsap_id)),
            "message_telugu": "🔔 Search save ayyindi — kotha matches vaste meeku WhatsApp alert vastundi"}


@app.get("/api/saved-searches/{tsap_id}")
def saved_search_list(tsap_id: str, request: Request = None):
    require_owner(request, tsap_id)
    rows = saved_for(tsap_id)
    out = []
    for r in rows:
        fresh = new_matches_for(r, DB_USERS, exclude=[tsap_id], limit=5)
        out.append({**r, "new_matches": len(fresh), "sample": [safe_user(x) for x in fresh[:3]]})
    return {"tsap_id": tsap_id, "count": len(out), "searches": out}


@app.delete("/api/saved-searches/{tsap_id}/{search_id}")
def saved_search_delete(tsap_id: str, search_id: str, request: Request = None):
    require_owner(request, tsap_id)
    ok = delete_search(tsap_id, search_id)
    if not ok:
        raise HTTPException(404, "Ee search dorakaledu")
    return {"success": True, "message_telugu": "🗑️ Search delete ayyindi"}


@app.post("/api/saved-searches/{tsap_id}/alerts")
def saved_search_alerts(tsap_id: str, request: Request = None):
    """Kotha matches ni WhatsApp ki pampu (anti-ban gap tho) — 'saved search alert'."""
    require_owner(request, tsap_id)
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Mee profile dorakaledu")
    total = 0
    details = []
    for r in saved_for(tsap_id):
        fresh = new_matches_for(r, DB_USERS, exclude=[tsap_id], limit=5)
        if not fresh:
            continue
        total += len(fresh)
        names = ", ".join(x.get("full_name", x.get("tsap_id", "")) for x in fresh[:3])
        txt = (f"🔔 {r['name']} — mee saved search ki {len(fresh)} kotha profiles dorikayi!\n{names}\n"
               f"Chudataniki: manavivaha.in/matches?search={r['search_id']}")
        q = {"queued": False}
        if publish_config()["wa_mode"] != "off":
            q = enqueue_whatsapp([u.get("phone", "")], txt, priority=1, kind="saved_search_alert")
        mark_alerted(r, [x["tsap_id"] for x in fresh])
        details.append({"search_id": r["search_id"], "new_matches": len(fresh), "queued": bool(q.get("queued")),
                        "text": txt})
    return {"success": True, "alerts_sent": len(details), "new_matches_total": total, "details": details,
            "message_telugu": (f"🔔 {total} kotha matches (saved searches) — WhatsApp queue lo pettam"
                               if total else "ℹ️ Ippudu kotha matches levu — filters mariste inka dorukutayi")}


@app.get("/api/consent/log/{tsap_id}")
def consent_log_endpoint(tsap_id: str, request: Request = None):
    """
    📜 Consent ledger — numbers eppudu evariki exchange ayyayo (audit; dispute ki proof).
    Numbers ikkada kooda masked — proof matrame (full number eppudu API lo radu).
    """
    require_owner(request, tsap_id)
    rows = consent_for(tsap_id)
    safe_rows = [{"at": r.get("at"), "action": r.get("action"),
                  "with": mask_phone(str(r.get("other_id", ""))[-10:]) if str(r.get("other_id", "")).isdigit() else r.get("other_id"),
                  "request_id": r.get("request_id"), "numbers_exchanged": r.get("numbers_exchanged"),
                  "lawful_basis": r.get("lawful_basis"), "retention_days": r.get("retention_days")} for r in rows]
    return {"tsap_id": tsap_id, "count": len(safe_rows), "consents": safe_rows,
            "policy_telugu": "🔐 Numbers consent tho matrame exchange — ee ledger lo record untundi (3 years retention)",
            "your_rights_telugu": ["Mee data delete cheyyali ante support ki cheppandi",
                                   "Block chesina profiles ki mee data kanipinchadu",
                                   "Number eppudu public ga (search/Google) kanipinchadu"]}


@app.get("/api/admin/abuse")
def admin_abuse(request: Request = None):
    """🚨 Abuse dashboard — rate limits, OTP locks, webhook attacks, validation errors."""
    require_admin(request)
    snap = abuse_snapshot()
    snap["otp_active"] = len(DB_OTPS)
    snap["verified_phones"] = len(VERIFIED_PHONES)
    snap["duplicate_phone_accounts"] = len([u for u in DB_USERS if u.get("duplicate_phone")])
    snap["consent_events"] = len(CONSENT_LEDGER)
    snap["message_telugu"] = "🚨 Ee numbers periguthunte attack/spam — rate limit tight cheyyandi (TSAP_RATE_LIMIT)"
    return snap


@app.get("/api/trust/board")
def trust_board(limit: int = 10):
    """🏅 Public trust leaderboard — complete + verified profiles (encourages form fill)."""
    limit = clamp_int(limit, "limit", 1, 50, 10)
    rows = []
    for u in DB_USERS:
        if u.get("is_banned"):
            continue
        t = trust_score(u, DB_INTERESTS)
        c = profile_completeness(u)
        rows.append({"tsap_id": u.get("tsap_id"), "gender": u.get("gender"), "district": u.get("district"),
                     "trust_score": t["score"], "badge_telugu": t["badge_telugu"],
                     "completeness": c["percent"], "verified": bool(u.get("phone_verified") or u.get("is_verified")),
                     "has_photo": bool(u.get("photo_urls"))})
    rows.sort(key=lambda r: (-r["trust_score"], -r["completeness"]))
    avg = round(sum(r["trust_score"] for r in rows) / max(1, len(rows)), 1)
    return {"count": len(rows), "average_trust": avg, "board": rows[:limit],
            "message_telugu": "🏅 Complete + verified profiles ki trust score ekkuva — matches kooda ekkuva vasthayi"}


@app.get("/api/vendors/categories")
def vendor_categories():
    """18 vendor categories (Telugu names tho) + active counts."""
    return {"success": True, "count": len(VENDOR_CATEGORIES), "categories": VENDOR_CATEGORIES,
            "headline": "Pelli sambandham related anni services — okate chota"}


@app.get("/api/vendors/stats")
def vendor_stats_api():
    return {"success": True, **vendor_stats()}


@app.get("/api/vendors/packages")
def vendor_packages():
    """🏷️ Ad packages (₹149 nunchi ₹3999) + add-ons + slots."""
    return {"success": True, **vendor_packages_public()}


@app.get("/api/vendors/ads")
def vendor_ads(slot: str = "home_top_banner", limit: int = 2, track: bool = True):
    """📢 Ad rotation (paid-first weighted). Site home/strips lo vaadutunnam."""
    return {"success": True, **ad_rotation(slot, limit=min(max(limit, 1), 6), track=track)}


@app.get("/api/vendors")
def vendor_list(category: str = "", district: str = "", city: str = "", q: str = "",
                limit: int = 60, include_inactive: bool = False):
    """🏪 Vendor directory — category/district/city/search filters (paid-first order)."""
    return {"success": True, **vendors_directory(category=category, district=district, city=city,
                                                 q=q, limit=min(max(limit, 1), 200),
                                                 include_inactive=include_inactive)}


@app.post("/api/vendors/register")
def vendor_register(payload: Dict[str, Any] = Body(default={})):
    """
    🏪 Vendor signup (catering/photography/decoration/hall...) → pending → admin approve.
    Body: {business_name, category, phone, city, district, state, package, about, price_range...}
    """
    res = register_vendor(payload or {})
    if res.get("ok"):
        # 🔐 WAVE 9 — vendor dashboard token (X-Vendor-Token) — own data matrame chudochu
        # 🐞 FIX: register_vendor() "vendor_id" ni **top-level** lo isthundi (res["vendor"] lo kaadu)
        _vid = (res.get("vendor_id") or (res.get("vendor") or {}).get("vendor_id")
                or (res.get("vendor") or {}).get("id") or "")
        if _vid:
            res["vendor_token"] = vendor_token(_vid)
            res.setdefault("note_telugu", "🔐 Ee vendor_token save cheyyandi — mee dashboard (impressions/clicks/leads) ki kavali")
    if not res.get("ok"):
        return JSONResponse(status_code=400, content={"success": False, **res})
    # Admin ki instant alert (WhatsApp) + vendor ki confirmation text
    try:
        admin_no = os.getenv("ADMIN_WHATSAPP_NUMBER", "").strip()
        v = res["vendor"]
        _txt = ("🏪 *NEW VENDOR REQUEST*\n%s (%s)\n📍 %s, %s\n📞 %s\n💼 Package: %s = ₹%d\n"
                "Vendor ID: %s\n\nPayment verify chesi /api/admin/vendors/%s/action?action=approve&utr=... "
                "tho activate cheyyandi" % (v["business_name"], v["category_te"], v["city"], v["district"],
                                            v["phone"], res["package"]["name"], res["amount"], v["id"], v["id"]))
        if admin_no and publish_config()["wa_mode"] != "off":
            enqueue_whatsapp([admin_no], _txt, priority=0, kind="vendor_request")
            res["admin_notified"] = True
        else:
            res["admin_alert_text"] = _txt
    except Exception as e:
        res["notify_error"] = str(e)[:100]
    return {"success": True, **res}


@app.get("/api/vendors/{vendor_id}")
def vendor_detail(vendor_id: str, track: bool = False):
    """🏪 Vendor public detail (contact WhatsApp CTA tho)."""
    v = next((x for x in __import__("vendors").VENDORS if x.get("id") == vendor_id), None)
    if not v:
        raise HTTPException(404, "Vendor dorakaledi")
    if v.get("status") == "pending" and str(v.get("phone")) != (os.getenv("ADMIN_PHONE", "") or "___"):
        pass  # pending listing public ki kanipinchadu (kaani owner/demo ki chudataniki allow)
    if track:
        track_vendor_click(vendor_id, source="detail")
    same_cat = [x for x in __import__("vendors").VENDORS
                if x.get("category") == v.get("category") and x.get("status") == "active" and x.get("id") != vendor_id][:4]
    return {"success": True, "vendor": public_vendor(v), "package": VENDOR_PACKAGES and
            {p["code"]: p for p in VENDOR_PACKAGES}.get(v.get("package"), {}),
            "similar": [public_vendor(x) for x in same_cat],
            "review_note_telugu": "Mee experience share cheyyandi — mana team verify chesi rating update chestundi"}


@app.get("/api/vendors/{vendor_id}/dashboard")
def vendor_dash(vendor_id: str, request: Request = None):
    """📊 Vendor performance: impressions, clicks, enquiries, days left, upsell."""
    require_vendor(request, vendor_id)   # 🛡️ WAVE 9: vendor token lekunda 401 (vendor data leak fix)
    d = vendor_dashboard(vendor_id)
    if not d.get("ok"):
        raise HTTPException(404, "Vendor dorakaledi")
    return {"success": True, **d}


@app.get("/api/vendors/{vendor_id}/promo")
def vendor_promo(vendor_id: str, variant: int = 0):
    """📝 Telugu promo post (Telegram + WhatsApp ready) + poster text."""
    v = next((x for x in __import__("vendors").VENDORS if x.get("id") == vendor_id), None)
    if not v:
        raise HTTPException(404, "Vendor dorakaledi")
    return {"success": True, **promo_post(v, variant=variant),
            "poster_square": "/api/vendors/%s/poster.png?style=square" % vendor_id,
            "poster_status": "/api/vendors/%s/poster.png?style=status" % vendor_id}


@app.get("/api/vendors/{vendor_id}/poster.png")
def vendor_poster_png(vendor_id: str, style: str = "square"):
    """🖼️ Vendor promo poster (QR tho) — square / status."""
    v = next((x for x in __import__("vendors").VENDORS if x.get("id") == vendor_id), None)
    if not v:
        raise HTTPException(404, "Vendor dorakaledi")
    try:
        import vendor_kit
        path = vendor_kit.vendor_poster(v, style=("status" if style == "status" else "square"))
        return FileResponse(path, media_type="image/png",
                            filename="manavivaha-vendor-%s-%s.png" % (v.get("id"), style))
    except Exception as e:
        raise HTTPException(500, "Poster generate avvaledu: %s" % str(e)[:120])


@app.post("/api/vendors/{vendor_id}/lead")
def vendor_lead_api(vendor_id: str, payload: Dict[str, Any] = Body(default={})):
    """📩 Enquiry → vendor ki instant WhatsApp + admin alert (+ customer ko 3 more options)."""
    res = vendor_lead(vendor_id, payload or {})
    if not res.get("ok"):
        return JSONResponse(status_code=400, content={"success": False, **res})
    try:
        v = res["vendor"]
        _to_vendor = res["vendor_whatsapp_text"]
        _phone = "".join(ch for ch in str(v.get("whatsapp_link", "")) if ch.isdigit())[2:12]
        vnum = ""
        _vend = next((x for x in __import__("vendors").VENDORS if x.get("id") == vendor_id), None)
        vnum = str((_vend or {}).get("whatsapp") or (_vend or {}).get("phone") or "")
        if vnum and publish_config()["wa_mode"] != "off":
            enqueue_whatsapp([vnum], _to_vendor, priority=0, kind="vendor_lead")
            res["vendor_notified"] = True
        else:
            res["vendor_alert_text"] = _to_vendor
        admin_no = os.getenv("ADMIN_WHATSAPP_NUMBER", "").strip()
        if admin_no and publish_config()["wa_mode"] != "off":
            enqueue_whatsapp([admin_no], "📩 Vendor enquiry: %s ← %s (%s)"
                             % (v.get("business_name"), payload.get("name"), payload.get("phone")),
                             priority=1, kind="vendor_lead_admin")
            res["admin_notified"] = True
    except Exception as e:
        res["notify_error"] = str(e)[:100]
    # 🎯 Mana side advantage: category lo inka 3 options (customer ni mana daggarane unchadam)
    try:
        import vendors as _vmod
        _v = next((x for x in _vmod.VENDORS if x.get("id") == vendor_id), None)
        if _v:
            _more = [public_vendor(x) for x in _vmod.VENDORS
                     if x.get("category") == _v.get("category") and x.get("status") == "active"
                     and x.get("id") != vendor_id][:3]
            res["more_options"] = _more
            if _more:
                res["compare_telugu"] = "Rate compare cheyyandi — %s category lo inka %d vendors unnaru mana side" % (
                    _v.get("category_te"), len(_more))
    except Exception:
        pass
    return {"success": True, **res}


@app.post("/api/vendors/{vendor_id}/click")
def vendor_click(vendor_id: str, source: str = ""):
    res = track_vendor_click(vendor_id, source)
    if not res.get("ok"):
        raise HTTPException(404, "Vendor dorakaledi")
    return {"success": True, **res}


@app.get("/api/admin/vendors")
def admin_vendor_list(status: str = "pending", token: str = "", request: Request = None):
    """👮 Admin — vendor requests queue (approve/reject)."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    return {"success": True, **vendor_queue(status)}


@app.post("/api/admin/vendors/{vendor_id}/action")
def admin_vendor_action(vendor_id: str, action: str, package: str = "", utr: str = "",
                        reason: str = "", token: str = "", request: Request = None):
    """✅ approve (package + UTR) · ❌ reject · ⏳ expire."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    if action == "approve":
        res = activate_vendor(vendor_id, package=package, utr=utr)
    elif action == "reject":
        res = reject_vendor(vendor_id, reason)
    elif action == "expire":
        v = next((x for x in __import__("vendors").VENDORS if x.get("id") == vendor_id), None)
        if not v:
            raise HTTPException(404, "Vendor dorakaledi")
        v["status"] = "expired"
        vendors_save_state()
        res = {"ok": True, "vendor": v, "message_telugu": "⏳ %s listing expire chesam" % v.get("business_name")}
    else:
        return JSONResponse(status_code=400, content={"success": False, "reason": "bad_action"})
    if not res.get("ok"):
        return JSONResponse(status_code=400, content={"success": False, **res})
    return {"success": True, **res}


@app.get("/api/admin/vendors/revenue/summary")
def admin_vendor_revenue(token: str = "", request: Request = None):
    """💰 Vendor revenue: active, pipeline, MRR, leads, renewals due."""
    require_admin(request)   # 🛡️ WAVE 9: admin key lekunda 403 (PII/money/)
    _g = _admin_guard(token)
    if _g:
        return _g
    return {"success": True, **vendor_revenue()}


@app.get("/api/welcome-pack/{tsap_id}")
def welcome_pack_get(tsap_id: str, request: Request = None):
    """
    🎁 Mee welcome pack — 3 profiles + caste channel links (Telegram + WhatsApp).
    Owner-only (mee token tho). WhatsApp tho pampina message kooda ikkada chudochu.
    """
    user = _user_or_404(tsap_id)
    require_owner(request, tsap_id)
    opposite = "Bride" if user.get("gender") == "Groom" else "Groom"
    cands = [u for u in DB_USERS if u.get("gender") == opposite and u["tsap_id"] != tsap_id][:20]
    rows = []
    for c in cands:
        sc = calculate_match_score(user, c, user_wants_same_caste=True)
        rows.append({"profile": c, "score": sc,
                     "reasons": generate_personalized_reasons(user, c, sc)})
    rows = sorted(rows, key=lambda r: r["score"], reverse=True)[:3]
    pack = build_welcome_pack(user, tsap_id, rows)
    pack["queue"] = user.get("welcome_pack_queue", {"queued": False,
                                                    "note_telugu": "Register lo queue avvaledu — resend cheyyandi"})
    return {"success": True, **pack_public(pack)}


@app.post("/api/welcome-pack/{tsap_id}/resend")
def welcome_pack_resend(tsap_id: str, request: Request = None):
    """🔁 3 profiles + caste channel links ni malli mee WhatsApp ki pampu (owner-only)."""
    user = _user_or_404(tsap_id)
    require_owner(request, tsap_id)
    opposite = "Bride" if user.get("gender") == "Groom" else "Groom"
    cands = [u for u in DB_USERS if u.get("gender") == opposite and u["tsap_id"] != tsap_id][:20]
    rows = []
    for c in cands:
        sc = calculate_match_score(user, c, user_wants_same_caste=True)
        rows.append({"profile": c, "score": sc, "reasons": generate_personalized_reasons(user, c, sc)})
    rows = sorted(rows, key=lambda r: r["score"], reverse=True)[:3]
    pack = build_welcome_pack(user, tsap_id, rows)
    phone = str(user.get("phone") or "").strip()
    res: Dict[str, Any] = {"queued": False}
    try:
        if phone and publish_config()["wa_mode"] != "off":
            res = enqueue_whatsapp([phone], pack["message_text"], priority=0, kind="welcome_pack_resend")
        else:
            res = {"queued": False, "reason": "whatsapp_mode_off" if phone else "phone_ledu",
                   "message_telugu": "WHATSAPP_MODE=bridge chesi bridge connect cheyyandi — appudu resend pani chestundi"}
    except Exception as e:
        res = {"queued": False, "error": str(e)[:140]}
    res = _mask_queue_result(res, phone)
    user["welcome_pack_queue"] = res
    return {"success": True, "tsap_id": tsap_id, "queued": bool(res.get("queued")), "wa_result": res,
            "profiles": pack["profiles"], "channels": pack["channels"],
            "message_preview": pack["message_preview"],
            "message_telugu": ("✅ 3 profiles + caste channel links malli pampisthunnam"
                               if res.get("queued") else "⚠️ WhatsApp queue off — message ikkada chudochu")}


@app.post("/api/admin/vendors/{vendor_id}/token")
def admin_vendor_token(vendor_id: str, request: Request = None):
    """
    🔐 Admin → vendor dashboard token (vendor token pogottukunte support ivvadaniki).
    Admin key tho matrame (X-Admin-Key). Vendor ki WhatsApp/phone tho pampistham.
    """
    require_admin(request)
    import vendors as _vmod_tok
    vendor = next((v for v in _vmod_tok.VENDORS if v.get("vendor_id") == vendor_id or v.get("id") == vendor_id), None)
    if not vendor:
        raise HTTPException(404, f"Vendor dorakaledu: {vendor_id}")
    _vid = vendor.get("vendor_id") or vendor.get("id")
    return {"success": True, "vendor_id": _vid, "vendor_token": vendor_token(_vid),
            "note_telugu": "🔐 Ee token vendor ki pampandi — vaallu /vendors/" + str(_vid) + " lo dashboard chudochu (token evariki ivvakoodadu)"}


@app.get("/api/channels/links")
def channels_links(caste: str = "", gender: str = "", state: str = "", district: str = "",
                   religion: str = "Hindu", limit: int = 5):
    """📢 Caste-based channel links (Telegram + WhatsApp) — website lo chupinchadaniki (public, PII ledu)."""
    prof = {"caste": clean(caste, 40, "caste"), "gender": clean(gender, 20, "gender"),
            "state": clean(state, 10, "state"), "district": clean(district, 40, "district"),
            "religion": clean(religion, 20, "religion")}
    links = caste_channel_links(prof, limit=clamp_int(limit, "limit", 1, 10, 5))
    if not str(caste or "").strip():
        note = "Caste pampandi (?caste=Reddy&gender=Bride) — mee caste channels (Telegram + WhatsApp) chupistham"
    else:
        note = "📢 Mee caste channel lo daily matches — Telegram + WhatsApp rendu join avvandi"
    return {"success": True, "channels": links, "stats": wa_links_stats(), "note_telugu": note}


# ============================================================================
#  🚀 WAVE 11 — ULTRA ADVANCED (gothram guard · stories · streak · push ·
#              voice · gamify · boost · support)
# ============================================================================
@app.get("/api/gothram/check")
def gothram_check(a: str, b: str):
    """🛡️ Rendu IDs madhya gothram check — same ayithe pelli kudadhu (block)."""
    me, other = _find_user(a), _find_user(b)
    if not me or not other:
        raise HTTPException(404, "Rendu TSAP IDs correct ga ivvandi")
    return {"success": True, "a": a, "b": b, **A11.gothram_check(me, other)}


@app.post("/api/stories/submit")
def story_submit(payload: dict, request: Request = None):
    """💑 Pelli ayina janta success story pampu (admin approve tarvata public)."""
    d = payload or {}
    require_owner(request, str(d.get("tsap_id", "")))
    u = _find_user(str(d.get("tsap_id", "")))
    if not u:
        raise HTTPException(404, "Mee profile dorakaledu — mundu register cheyyandi")
    rec = A11.submit_story(str(d.get("tsap_id", "")), str(d.get("text", "")),
                           partner_id=str(d.get("partner_id", "")),
                           couple_names=str(d.get("couple_names", "")) or str(u.get("full_name", "")),
                           photo_url=str(d.get("photo_url", "")),
                           district=str(d.get("district", "")) or str(u.get("district", "")))
    return {"success": True, "story": rec,
            "message_telugu": "💑 Story vachindi! Admin approve (24h) ayyaka /stories page + channels lo kanipistundi 🎉"}


@app.get("/api/stories")
def stories_list(limit: int = 20):
    """💑 Approved success stories (public — trust + viral, numbers ledu)."""
    rows = A11.approved_stories(clamp_int(limit, "limit", 1, 50, 20))
    return {"success": True, "count": len(rows), "stories": rows,
            "share_note_telugu": "💑 Pelli ayinda? Mee story pampandi — janta photo + 2 lines chalu!"}


@app.post("/api/stories/{story_id}/like")
def story_like(story_id: str):
    return {"success": True, **A11.like_story(story_id)}


@app.post("/api/admin/stories/{story_id}/action")
def admin_story_action(story_id: str, payload: dict = None, request: Request = None):
    """💑 Admin: story approve/reject (approve → share text ready)."""
    require_admin(request)
    d = payload or {}
    rec = A11.review_story(story_id, str(d.get("action", "")), str(d.get("note", "")))
    out = {"success": True, "story": rec}
    if rec.get("status") == "approved":
        out["share_text"] = A11.story_share_text(rec)
        out["share_note_telugu"] = "📢 Ee text official channel + WhatsApp lo forward cheyyandi"
    return out


@app.get("/api/support/faq")
def support_faq(q: str = "", limit: int = 5):
    """💬 Telugu support Q&A — ?q=price ani search (widget + bot common)."""
    rows = A11.search_faq(q, clamp_int(limit, "limit", 1, 12, 5))
    return {"success": True, "count": len(rows), "faqs": rows,
            "human_telugu": "Manishitho matladali ante bot lo /help — 10AM–7PM Telugu support 🙏"}


@app.get("/api/streak/{tsap_id}")
def streak_get(tsap_id: str, request: Request = None):
    """🔥 Streak status (count, best, repu bonus)."""
    require_owner(request, tsap_id)
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Mee profile dorakaledu")
    return {"success": True, "tsap_id": tsap_id, **A11.streak_status(u)}


@app.post("/api/streak/claim")
def streak_claim(payload: dict, request: Request = None):
    """🔥 Daily bonus claim — rojoo okasari (streak penchithe bonus ekkuva)."""
    tsap_id = str((payload or {}).get("tsap_id", ""))
    require_owner(request, tsap_id)
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Mee profile dorakaledu")
    return {"success": True, "tsap_id": tsap_id, **A11.claim_daily(u)}


@app.get("/api/push/vapid")
def push_vapid():
    """🔔 VAPID public key (browser subscribe ki) — keys lekapothe preview mode."""
    key = A11.vapid_public_key()
    return {"success": True, "vapid_public_key": key,
            "mode": "live-ready" if key else "preview",
            "note_telugu": "🔔 Alerts ON cheyyandi — kotha matches vaste notification" if key
                           else "ℹ️ VAPID keys set cheyyagane live push (ippudu queue-preview mode)"}


@app.post("/api/push/subscribe")
def push_subscribe(payload: dict, request: Request = None):
    """🔔 Browser push subscribe (matches page 🔔 button nunchi)."""
    d = payload or {}
    tsap_id = str(d.get("tsap_id", ""))
    require_owner(request, tsap_id)
    if not _find_user(tsap_id):
        raise HTTPException(404, "Mee profile dorakaledu")
    return A11.push_subscribe(tsap_id, str(d.get("endpoint", "")),
                              d.get("keys") or {}, ua=str(d.get("ua", "")))


@app.post("/api/push/unsubscribe")
def push_unsubscribe(payload: dict, request: Request = None):
    d = payload or {}
    tsap_id = str(d.get("tsap_id", ""))
    if tsap_id:
        require_owner(request, tsap_id)
    return A11.push_unsubscribe(tsap_id=tsap_id, endpoint=str(d.get("endpoint", "")))


@app.post("/api/push/notify/{tsap_id}")
def push_notify(tsap_id: str, payload: dict, request: Request = None):
    """🔔 Notify pampu — owner (self digest) leda admin (broadcast)."""
    if not is_admin(request):
        require_owner(request, tsap_id)
    if not _find_user(tsap_id):
        raise HTTPException(404, "Profile dorakaledu")
    d = payload or {}
    return {"tsap_id": tsap_id, **A11.push_notify(
        tsap_id, str(d.get("title", "💍 Mana Vivaha — kotha matches!")),
        str(d.get("body", "Meeku 2 kotha matches vachayi — chudandi!")),
        str(d.get("url", "/matches")))}


@app.get("/api/admin/push/queue")
def admin_push_queue(request: Request = None):
    require_admin(request)
    return {"success": True, "subs": len(A11.PUSH_SUBS),
            "queue": A11.PUSH_QUEUE[-30:][::-1],
            "vapid_ready": bool(A11.vapid_public_key())}


@app.post("/api/voice/upload")
async def voice_upload(file: UploadFile = File(...), tsap_id: str = Form("")):
    """
    🎙️ Voice intro upload (30 sec) — phone recorder nunchi.
    MP3/WAV/OGG/M4A, max 2MB. Matches lo ▶️ play avutundi.
    """
    tid = (tsap_id or "").strip()
    u = _find_user(tid) if tid else None
    data = await file.read()
    chk = A11.voice_validate(file.filename or "", len(data))
    if not chk.get("ok"):
        raise HTTPException(400, chk["error_telugu"])
    os.makedirs("/tmp/voice", exist_ok=True)
    token = (tid.strip() or "tmp") + "-" + datetime.utcnow().strftime("%y%m%d%H%M%S")
    name = f"{token}.{chk['ext']}"
    path = f"/tmp/voice/{name}"
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise HTTPException(500, f"Voice save avvaledu: {str(e)[:80]}")
    url = f"/voice/{name}"
    if u is not None:
        u["voice_url"] = url
        u["voice_at"] = datetime.utcnow().isoformat()
    return {"success": True, "url": url, "tsap_id": tid, "bytes": len(data),
            "message_telugu": f"🎙️ Voice intro upload ayyindi! Matches lo mee voice vintaru ({round(len(data)/1024)} KB)"}


@app.get("/api/voice/{tsap_id}")
def voice_get(tsap_id: str):
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    url = str(u.get("voice_url", "") or "")
    return {"success": True, "tsap_id": tsap_id, "voice_url": url, "has_voice": bool(url),
            "uploaded_at": str(u.get("voice_at", "") or ""),
            "note_telugu": "🎙️ Voice unna profiles ki 3x response (mana survey)" if url
                           else "ℹ️ Voice intro ledu — 30 sec record chesi pampandi"}


@app.post("/api/profile/complete-bonus/{tsap_id}")
def complete_bonus(tsap_id: str, request: Request = None):
    """🎮 Profile 90%+ → 2 credits FREE (okasari matrame — gamification)."""
    require_owner(request, tsap_id)
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "Mee profile dorakaledu")
    pct = profile_completeness(u)["percent"]
    res = A11.claim_complete_bonus(u, pct)
    return {"success": res.get("success", False), "tsap_id": tsap_id,
            "completeness": pct, **res}


@app.get("/api/boost/packs")
def boost_packs():
    """⚡ Boost packs list (B_1/B_3/B_7) + mee boost status kosam ?tsap_id=."""
    return {"success": True, "packs": list(A11.BOOST_PACKS.values()),
            "note_telugu": "⚡ Boost active ayithe matches + postings lo mee profile TOP lo"}


@app.post("/api/boost/buy")
def boost_buy(payload: dict, request: Request = None):
    """
    ⚡ Boost konadam — dev/demo lo ventane active, production lo payment tarvata
    (credits/buy pattern — webhook verify ayyaka active).
    """
    d = payload or {}
    tsap_id = str(d.get("tsap_id", ""))
    require_owner(request, tsap_id)
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found — mundu register cheyyandi")
    pack_code = str(d.get("pack", "B_1")).upper()
    if pack_code not in A11.BOOST_PACKS:
        raise HTTPException(400, "Boost pack B_1 / B_3 / B_7 matrame")
    pack = A11.BOOST_PACKS[pack_code]
    order_id = "BST-" + datetime.utcnow().strftime("%y%m%d%H%M%S") + str(len(DB_PAYMENTS) + 1).zfill(3)
    order = {"order_id": order_id, "tsap_id": tsap_id, "plan": pack_code, "kind": "boost",
             "amount": pack["price"], "at": datetime.utcnow().isoformat(), "status": "created"}
    if dev_mode():
        eff = A11.apply_boost(u, pack_code)
        order["status"] = "paid"
        order["effect"] = eff["message_telugu"]
    else:
        order["payment_required"] = True
        order["next_step_telugu"] = (f"💳 ₹{pack['price']} pay cheyyandi — payment vachhaka boost automatic ON. UPI: manavivaha@upi")
    DB_PAYMENTS.append(order)
    return {"success": True, "order": order, "boost_until": str(u.get("boost_until", "") or ""),
            "boosted": A11.is_boosted(u),
            "message_telugu": (f"{pack['label']} active! ⚡" if order["status"] == "paid"
                               else f"Order {order_id} — ₹{pack['price']} pay cheyyandi")}


# ============================================================================
# 🔒 WAVE 12 — SMART REVEAL (masked channels + unlock + ₹500 assisted console)
# ============================================================================
@app.post("/api/link-telegram")
def api_link_telegram(payload: dict):
    """🔗 Bot /link — Telegram chat_id ni profile tho link (personal delivery kosam)."""
    d = payload or {}
    u = _find_user(str(d.get("tsap_id", "")).upper())
    if not u:
        raise HTTPException(404, "ID dorakaledu — website login lo mee TSAP ID chudandi")
    u["telegram_chat_id"] = str(d.get("chat_id", ""))
    u["telegram_linked_at"] = datetime.utcnow().isoformat()
    return {"success": True, "tsap_id": u["tsap_id"],
            "message_telugu": f"✅ Link ayyindi! {u['tsap_id']} — ippudu /unlock, /mylist vadachu"}


@app.post("/api/unlock")
def api_unlock(payload: dict):
    """
    🔓 Number unlock — entitled ayithe FREE, lekapothe 1 credit cut.
    Credits 0 ayithe paywall (₹99 top-up / ₹500 assisted).
    """
    d = payload or {}
    viewer = _find_user(str(d.get("viewer_id", "")).upper())
    target = _find_user(str(d.get("target_id", "")).upper())
    if not viewer:
        raise HTTPException(404, "Mee profile dorakaledu — /link tho link cheyyandi")
    if not target:
        raise HTTPException(404, f"ID dorakaledu: {d.get('target_id', '')}")
    res = S12.unlock_number(viewer, target)
    if res.get("success"):
        res["target"] = {"tsap_id": target["tsap_id"],
                         "name": S12.first_masked(target.get("full_name", "")),
                         "age": target.get("age"), "caste": target.get("caste")}
    return res


@app.get("/api/unlocks/{viewer_id}")
def api_my_unlocks(viewer_id: str):
    """📋 Naa unlocked list — MASKED (full number per-unlock matrame, logged)."""
    me = _find_user(viewer_id.upper())
    if not me:
        raise HTTPException(404, "Profile dorakaledu")
    out = S12.my_unlocks(me["tsap_id"], DB_USERS)
    out["credits"] = me.get("credits", 0)
    return out


# --- ₹500 assisted orders (admin) --------------------------------------------
@app.post("/api/admin/assist-orders")
def api_assist_create(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    buyer = _find_user(str(d.get("buyer_id", "")).upper())
    if not buyer:
        raise HTTPException(404, f"Buyer ID dorakaledu: {d.get('buyer_id', '')}")
    order = S12.create_order(buyer["tsap_id"], int(d.get("amount", S12.ASSISTED_PRICE) or S12.ASSISTED_PRICE),
                             str(d.get("note", "")))
    return {"success": True, "order": order,
            "message_telugu": f"✅ Order {order['id']} — ₹{order['amount']} (UTR vachhaka paid cheyyandi)"}


@app.get("/api/admin/assist-orders")
def api_assist_list(request: Request, status: str = ""):
    require_admin(request)
    items = [o for o in S12.ORDERS if not status or o.get("status") == status]
    return {"success": True, "count": len(items), "orders": list(reversed(items))}


@app.post("/api/admin/assist-orders/{order_id}/paid")
def api_assist_paid(order_id: str, payload: dict, request: Request):
    require_admin(request)
    res = S12.mark_order_paid(order_id, str((payload or {}).get("utr", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/assist-orders/{order_id}/profiles")
def api_assist_attach(order_id: str, payload: dict, request: Request):
    require_admin(request)
    ids = [str(x).upper() for x in (payload or {}).get("profile_ids", [])]
    missing = [i for i in ids if not _find_user(i)]
    if missing:
        raise HTTPException(404, f"IDs dorakalevu: {', '.join(missing)}")
    res = S12.attach_order_profiles(order_id, ids)
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


# --- 🎯 Match & Send console (admin) ------------------------------------------
@app.get("/api/admin/match-send/copy-list")
def api_copy_list(request: Request, buyer: str = "", ids: str = "", order_id: str = ""):
    """📋 Admin 1-click copy — `NAME -- NUMBER` lines (manual paste kosam). ADMIN-ONLY."""
    require_admin(request)
    b = _find_user(buyer.upper())
    if not b:
        raise HTTPException(404, f"Buyer ID dorakaledu: {buyer}")
    wanted = [x.strip().upper() for x in (ids or "").split(",") if x.strip()]
    targets = [_find_user(i) for i in wanted]
    if not targets or any(t is None for t in targets):
        raise HTTPException(404, "Konni IDs dorakalevu — list sari chudandi")
    text = S12.build_copy_list(b, targets, order_id)
    return {"success": True, "count": len(targets), "text": text}


@app.get("/api/admin/match-send/{buyer_id}")
def api_match_send(buyer_id: str, request: Request, limit: int = 20, min_score: int = 0,
                     include_same_surname: int = 0, include_age_block: int = 0, nri_only: int = 0,
                     age_min: int = 0, age_max: int = 0, castes: str = "", districts: str = "",
                     state: str = "", religion: str = "", education: str = "", jobs: str = "",
                     salary_min: int = 0, marital: str = "", children: str = "",
                     photo_only: int = 0, verified_only: int = 0, nri_exclude: int = 0):
    """
    🎯 Buyer ID → perfect matches (score sort) + delivery readiness.
    ADMIN-ONLY (full phones untayi — copy-list/verify kosam).
    🌊 WAVE 19: advanced server filters — anni pass ayina suitable matches matrame.
    """
    require_admin(request)
    me = _find_user(buyer_id.upper())
    if not me:
        raise HTTPException(404, f"Buyer ID dorakaledu: {buyer_id}")
    pool = [u for u in DB_USERS if u.get("tsap_id") != me["tsap_id"]
            and not safety.is_blocked(me["tsap_id"], u.get("tsap_id", ""), DB_BLOCKS)
            and not u.get("is_banned")]
    gf = A11.filter_same_gothram(me, pool)
    sf = S12.filter_same_surname(me, gf["kept"])
    if not include_same_surname:
        kept = sf["kept"]
    else:
        kept = gf["kept"]
    # 🌊 WAVE 14: AGE RULE auto-filter (?include_age_block=1) + NRI-only (?nri_only=1)
    a14skip = []
    if not include_age_block:
        af = MP.filter_age_ok(me, kept)
        kept, a14skip = af["kept"], af["skipped_ids"]
    if nri_only:
        kept = [c for c in kept if _is_nri(c)]
    if nri_exclude:
        kept = [c for c in kept if not _is_nri(c)]
    # 🌊 WAVE 19 — ADVANCED FILTERS (strict: anni match ayithe matrame suitable)
    _fstate = (state or "").strip()
    _frel = (religion or "").strip()
    _fmari = [x.strip() for x in (marital or "").split(",") if x.strip()]
    _fkids = (children or "").strip()
    _fcastes = [x.strip().lower() for x in (castes or "").split(",") if x.strip()]
    _fdists = [x.strip().lower() for x in (districts or "").split(",") if x.strip()]
    _fedu = [x.strip().lower() for x in (education or "").split(",") if x.strip()]
    _fjobs = [x.strip().lower() for x in (jobs or "").split(",") if x.strip()]

    def _sal_num(v):
        try:
            return float(str(v).replace(",", "").strip().split()[0])
        except Exception:
            return 0.0

    _f19skip = 0

    def _f19_ok(c):
        try:
            _age = int(c.get("age", 0) or 0)
        except Exception:
            _age = 0
        if age_min and _age and _age < age_min:
            return False
        if age_max and _age and _age > age_max:
            return False
        if _fcastes and str(c.get("caste", "")).lower() not in _fcastes:
            return False
        if _fdists and str(c.get("district", "")).lower() not in _fdists:
            return False
        if _fstate and str(c.get("state", "")) != _fstate:
            return False
        if _frel and str(c.get("religion", "")) != _frel:
            return False
        if _fedu and str(c.get("education", "")).lower() not in _fedu:
            return False
        if _fjobs and str(c.get("job", "")).lower() not in _fjobs:
            return False
        if salary_min and _sal_num(c.get("salary", 0)) < salary_min:
            return False
        if _fmari and str(c.get("marital_status", "")) not in _fmari:
            return False
        if _fkids and str(c.get("children", "None")) != _fkids:
            return False
        if photo_only and not (c.get("has_photo") or c.get("photo_url")):
            return False
        if verified_only and not (c.get("phone_verified") or c.get("is_verified")):
            return False
        return True

    _before = len(kept)
    kept = [c for c in kept if _f19_ok(c)]
    _f19skip = _before - len(kept)
    rows = topmatch.find_top_matches_v2(me, kept, limit=min(limit, 100), min_score=min_score)
    rows.sort(key=lambda r: (A11.boost_rank_key(r.get("profile", {})), r.get("score", 0)), reverse=True)
    rows = MP.rerank_profession(me, rows)     # 🌊 WAVE 14: profession affinity first
    out = []
    for r in rows:
        prof = r.pop("profile")
        r.update({"full_name": prof.get("full_name"), "phone": prof.get("phone", ""),
                  "age": prof.get("age"), "gender": prof.get("gender"), "caste": prof.get("caste"),
                  "sub_caste": prof.get("sub_caste", ""), "district": prof.get("district"),
                  "state": prof.get("state"), "education": prof.get("education"),
                  "job": prof.get("job"), "salary": prof.get("salary", ""),
                  "marital_status": prof.get("marital_status", ""), "children": prof.get("children", "None"),
                  "star": prof.get("star", ""),
                  "height": prof.get("height", ""),
                  "verification": safety.verification_badge(prof)["level"],
                  "phone_verified": bool(prof.get("phone_verified") or prof.get("is_verified")),
                  "has_photo": bool(prof.get("photo_urls")),
                  "is_nri": _is_nri(prof),
                  "profession_label": _prof_label(prof)})
        out.append(r)
    return {"buyer": {"tsap_id": me["tsap_id"], "name": me.get("full_name"),
                      "phone": me.get("phone", ""), "credits": me.get("credits", 0),
                      "telegram_chat_id": me.get("telegram_chat_id", ""),
                      "telegram_linked": bool(me.get("telegram_chat_id"))},
            "count": len(out), "gothram_skipped": len(gf["skipped_ids"]),
            "surname_skipped": len(sf["skipped_ids"]), "surname_skipped_ids": sf["skipped_ids"][:10],
            "age_skipped": len(a14skip), "age_skipped_ids": a14skip[:10],
            "nri_only": bool(nri_only), "nri_excluded": bool(nri_exclude),
            "filters_skipped": _f19skip,
            "results": out,
            "message_telugu": f"🎯 {len(out)} perfect matches — select chesi Telegram/WhatsApp ki pampandi" + (" · ✈️ NRI-only" if nri_only else "") + (f" · 🔍 filters {_f19skip} skip" if _f19skip else "")}


@app.post("/api/admin/match-send/deliver")
async def api_match_deliver(payload: dict, request: Request):
    """
    📩 1-click personal delivery — buyer Telegram DM + WhatsApp.
    Grant (STRICT: ee profiles mathrame) + send + copy-list — anni okesari.
    """
    require_admin(request)
    d = payload or {}
    buyer = _find_user(str(d.get("buyer_id", "")).upper())
    if not buyer:
        raise HTTPException(404, f"Buyer ID dorakaledu: {d.get('buyer_id', '')}")
    ids = [str(x).upper() for x in d.get("profile_ids", [])]
    targets = [_find_user(i) for i in ids]
    if not targets or any(t is None for t in targets):
        raise HTTPException(404, "Konni profile IDs dorakalevu")
    order_id = str(d.get("order_id", "") or "")
    via = str(d.get("via", "both") or "both").lower()
    if order_id:
        o = S12.get_order(order_id)
        if not o:
            raise HTTPException(404, f"Order dorakaledu: {order_id}")
        if o["status"] not in ("paid", "delivered"):
            raise HTTPException(400, "⚠️ Order paid kakapothe deliver cheyyakoodadu — mundhu UTR confirm")
        o["profile_ids"] = ids
        o["via"] = [via]
    for pid in ids:
        S12.grant_unlock(buyer["tsap_id"], pid,
                         via=("assisted" if order_id else "admin_gift"), order_id=order_id)
    res = await S12.deliver_personal(buyer, targets, via=via, order_id=order_id)
    if order_id and res.get("ok"):
        S12.get_order(order_id)["status"] = "delivered"
        S12.get_order(order_id)["delivered_at"] = S12._now_iso()
        S12._persist()
    res.update({"success": True, "buyer_id": buyer["tsap_id"], "delivered": len(ids),
                "order_id": order_id})
    return res


@app.post("/api/admin/link-telegram")
def api_admin_link_tg(payload: dict, request: Request):
    """🔗 Admin manual link — buyer /myid chepthe ikkada link (DM delivery kosam)."""
    require_admin(request)
    d = payload or {}
    u = _find_user(str(d.get("buyer_id", "")).upper())
    if not u:
        raise HTTPException(404, "Buyer ID dorakaledu")
    u["telegram_chat_id"] = str(d.get("chat_id", ""))
    u["telegram_linked_at"] = datetime.utcnow().isoformat()
    return {"success": True, "tsap_id": u["tsap_id"], "telegram_chat_id": u["telegram_chat_id"],
            "message_telugu": "✅ Telegram link ayyindi — personal DM ready"}


# ============================================================================
# 🪐 WAVE 13 — ASTROLOGY (36-guna + dosha + jathakam/pandit)
# ============================================================================
@app.get("/api/astro/guna")
def api_guna(bride_id: str = "", groom_id: str = ""):
    """🪐 36-guna jathakam porutham — 2 profile IDs (gender auto-detect + swap)."""
    a = _find_user(bride_id.upper()) if bride_id else None
    b = _find_user(groom_id.upper()) if groom_id else None
    if not a or not b:
        raise HTTPException(404, "Rendu profile IDs ivvandi (bride_id + groom_id)")
    bride, groom = a, b
    if a.get("gender") == "Groom" and b.get("gender") == "Bride":
        bride, groom = b, a
    elif a.get("gender") == b.get("gender"):
        raise HTTPException(400, "Bride + Groom rendu veru genders ayi undali")
    res = AST.guna_milan(bride.get("star", ""), bride.get("rasi", ""),
                          groom.get("star", ""), groom.get("rasi", ""))
    res["bride_id"] = bride.get("tsap_id")
    res["groom_id"] = groom.get("tsap_id")
    return res


@app.get("/api/astro/dosha/{tsap_id}")
def api_dosha(tsap_id: str):
    """🔍 Dosha screening — profile ki dosham unda/leda (honest flags)."""
    u = _find_user(tsap_id.upper())
    if not u:
        raise HTTPException(404, "Profile dorakaledu")
    res = AST.dosha_screening(u)
    res["tsap_id"] = u["tsap_id"]
    return res


@app.post("/api/astro/jathakam/upload")
async def api_jathakam_upload(file: UploadFile = File(...), tsap_id: str = Form("")):
    """📜 Jathakam upload (photo/PDF, max 8MB) → pandit queue."""
    u = _find_user(tsap_id.strip().upper())
    if not u:
        raise HTTPException(404, "TSAP ID dorakaledu — mundu register")
    ext = (file.filename or "").split(".")[-1].lower()
    if ext not in {"jpg", "jpeg", "png", "webp", "pdf"}:
        raise HTTPException(400, "Jathakam photo (JPG/PNG) leda PDF matrame")
    data = await file.read()
    if len(data) > 8 * 1024 * 1024:
        raise HTTPException(413, "File 8MB kanna ekkuva — compress chesi pampandi")
    if len(data) < 1024:
        raise HTTPException(400, "File khaali — malli upload cheyyandi")
    os.makedirs("/tmp/jathakam", exist_ok=True)
    name = f"{u['tsap_id']}-{datetime.utcnow().strftime('%y%m%d%H%M%S')}.{ext}"
    with open(f"/tmp/jathakam/{name}", "wb") as f:
        f.write(data)
    j = AST.submit_jathakam(u["tsap_id"], name, "pdf" if ext == "pdf" else "photo")
    return {"success": True, "jathakam_id": j["id"],
            "message_telugu": f"✅ Jathakam vachindi ({j['id']}) — pandit verify chesaka 🪐 badge vastundi 🙏"}


@app.get("/api/admin/astro/queue")
def api_astro_queue(request: Request, status: str = ""):
    require_admin(request)
    items = [j for j in AST.JATHAKAMS if not status or j.get("status") == status]
    return {"success": True, "count": len(items), "items": list(reversed(items))}


@app.post("/api/admin/astro/verify/{jid}")
def api_astro_verify(jid: str, payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = AST.verify_jathakam(jid, bool(d.get("ok", True)), str(d.get("note", "")))
    if not res.get("success"):
        raise HTTPException(404, res.get("message_telugu"))
    j = res["jathakam"]
    u = _find_user(j["tsap_id"])
    if u and j["status"] == "verified":
        u["jathakam_verified"] = True
    elif u:
        u["jathakam_verified"] = False
    return res


@app.get("/api/admin/astro/stats")
def api_astro_stats(request: Request):
    require_admin(request)
    return {"success": True, **AST.astro_stats(DB_USERS)}


# ============================================================================
# 📢 WAVE 13 — VENDOR ADS (campaigns + targeting + slots)
# ============================================================================
@app.get("/api/ads/rates")
def api_ads_rates():
    """💰 Public ad rates (vendor ki mundhe telustundi)."""
    return {"success": True, "rates": ADS.RATES, "slots": ADS.SLOTS, "slot_telugu": ADS.SLOT_TE}


@app.post("/api/ads/quote")
def api_ads_quote(payload: dict):
    d = payload or {}
    q = ADS.quote(str(d.get("level", "")), int(d.get("days", 0) or 0),
                  d.get("districts") or [], d.get("slots") or [], bool(d.get("video_url")))
    if not q.get("ok"):
        raise HTTPException(400, q.get("message_telugu"))
    return {"success": True, **q}


@app.get("/api/ads")
def api_ads_serve(slot: str = "matches_sidebar", district: str = "", state: str = ""):
    """🎯 Targeted ad serve (slot + user district/state). No ad → house promo signal."""
    return ADS.serve(slot, district, state)


@app.post("/api/ads/{cid}/click")
def api_ads_click(cid: str):
    return ADS.track_click(cid)


@app.post("/api/vendors/{vendor_id}/campaigns")
def api_vendor_campaign_create(vendor_id: str, payload: dict, request: Request):
    """📢 Vendor campaign request (payment + admin approve tarvata live)."""
    require_vendor(request, vendor_id)
    import vendors as VND
    v = next((x for x in VND.VENDORS if x.get("id") == vendor_id), None)
    if not v:
        raise HTTPException(404, "Vendor dorakaledu")
    d = payload or {}
    res = ADS.create_campaign(vendor_id, str(d.get("title", "")), str(d.get("level", "")),
                              int(d.get("days", 0) or 0), d.get("districts") or [],
                              str(d.get("state", "")), d.get("slots") or [],
                              str(d.get("image_url", "")), str(d.get("banner_url", "")),
                              str(d.get("video_url", "")), str(d.get("offer", "")),
                              str(d.get("link", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.get("/api/vendors/{vendor_id}/campaigns")
def api_vendor_campaigns(vendor_id: str, request: Request):
    require_vendor(request, vendor_id)
    items = ADS.vendor_campaigns(vendor_id)
    return {"success": True, "count": len(items),
            "campaigns": list(reversed(items)),
            "totals": {"impressions": sum(int(c.get("impressions", 0) or 0) for c in items),
                       "clicks": sum(int(c.get("clicks", 0) or 0) for c in items),
                       "spent": sum(int(c.get("amount", 0) or 0) for c in items if c.get("utr"))}}


@app.get("/api/admin/ads")
def api_admin_ads(request: Request, status: str = ""):
    require_admin(request)
    items = [c for c in ADS.CAMPAIGNS if not status or c.get("status") == status]
    return {"success": True, "count": len(items), "campaigns": list(reversed(items))}


@app.post("/api/admin/ads/{cid}/approve")
def api_admin_ads_approve(cid: str, payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = ADS.approve_campaign(cid, str(d.get("utr", "")), int(d.get("days", 0) or 0))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/ads/{cid}/action")
def api_admin_ads_action(cid: str, payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = ADS.campaign_action(cid, str(d.get("action", "")), str(d.get("reason", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.get("/api/admin/ads/stats")
def api_admin_ads_stats(request: Request):
    require_admin(request)
    return {"success": True, **ADS.ads_stats()}


# ============================================================================
#  🌊 WAVE 14 — META (religion→caste) + SAFE-PAY (Razorpay) + FESTIVAL OFFERS
# ============================================================================
@app.get("/api/meta/religions")
def api_meta_religions():
    return {"success": True, "religions": MP.RELIGIONS}


@app.get("/api/meta/castes")
def api_meta_castes(religion: str = "Hindu"):
    info = MP.castes_for(religion)
    return {"success": True, **info,
            "message_telugu": f"🙏 {info['religion']} — {len(info['castes'])} kulalu/groups (A–Z)"}


@app.get("/api/pay/config")
def api_pay_config():
    """Public: Razorpay key_id (publishable) + plans + active offers. Secret NEVER."""
    return {"success": True, **PP.pay_config(), "plans": plan_list_with_free(),
            "offers": PP.active_offers()}


@app.post("/api/pay/order")
def api_pay_order(payload: dict):
    """Create pay order — amount SERVER computes (client amount trust cheyyam)."""
    d = payload or {}
    res = PP.create_pay_order(str(d.get("tsap_id", "")).upper(), str(d.get("purpose", "credits")),
                              str(d.get("ref", "")), str(d.get("offer_code", "") or ""))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/pay/verify")
def api_pay_verify(payload: dict):
    """Razorpay verify → signature OK ayithe ONLY fulfill. Idempotent."""
    d = payload or {}
    res = PP.verify_payment(str(d.get("order_id", "") or d.get("pay_order_id", "")),
                            str(d.get("razorpay_order_id", "")), str(d.get("razorpay_payment_id", "")),
                            str(d.get("razorpay_signature", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.get("/api/pay/status/{order_id}")
def api_pay_status(order_id: str):
    po = PP.get_pay_order(order_id)
    if not po:
        raise HTTPException(404, "Order dorakaledu")
    safe = {k: v for k, v in po.items() if k not in ("signature", "payment_id")}
    return {"success": True, "order": safe}


@app.get("/api/admin/payments")
def api_admin_payments(request: Request, status: str = ""):
    require_admin(request)
    items = [o for o in PP.PAY_ORDERS if not status or o.get("status") == status]
    return {"success": True, "count": len(items), "orders": list(reversed(items)),
            "stats": PP.pay_stats()}


@app.post("/api/admin/payments/{order_id}/confirm")
def api_admin_pay_confirm(order_id: str, payload: dict, request: Request):
    """Manual-UPI fallback: admin UTR verify chesi confirm → fulfill."""
    require_admin(request)
    res = PP.confirm_manual(order_id, str((payload or {}).get("utr", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.get("/api/offers/active")
def api_offers_active():
    """Public: live festival offers (homepage banner ki)."""
    offers = PP.active_offers()
    return {"success": True, "offers": offers,
            "message_telugu": f"🎉 {len(offers)} festival offers live!"}


@app.post("/api/admin/offers")
def api_admin_offer_create(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    applies = d.get("applies_to") or ["credits"]
    if isinstance(applies, str):
        applies = [a.strip() for a in applies.split(",") if a.strip()]
    res = PP.create_offer(str(d.get("code", "")), str(d.get("title", "")),
                          pct_off=int(d.get("pct_off", 0) or 0), flat_off=int(d.get("flat_off", 0) or 0),
                          applies_to=applies, valid_from=str(d.get("valid_from", "") or ""),
                          valid_to=str(d.get("valid_to", "") or ""),
                          max_uses=int(d.get("max_uses", 100) or 100),
                          min_amount=int(d.get("min_amount", 0) or 0),
                          festival=str(d.get("festival", "") or ""))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/offers/seed")
def api_admin_offers_seed(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    return PP.seed_festivals(str(d.get("valid_from", "") or ""), str(d.get("valid_to", "") or ""),
                             int(d.get("max_uses", 1000) or 1000))


@app.get("/api/promo/apply")
def api_promo_apply(code: str = "", purpose: str = "credits", plan: str = "S_99", user: str = ""):
    """🎟️ Promo preview — pay ki mundu discount chudu (public, no charge)."""
    from interest import get_plan
    try:
        amount = int(get_plan(plan).get("price", 0))
    except Exception:
        amount = 0
    if amount <= 0:
        raise HTTPException(400, "Plan sari ledhu")
    res = PP.validate_offer((code or "").strip(), purpose.strip().lower() or "credits", amount, user)
    if not res.get("ok"):
        raise HTTPException(400, res.get("message_telugu"))
    return {"success": True, **res, "plan": plan, "amount": amount,
            "message_telugu": f"🎉 {res.get('code')}: ₹{amount} → ₹{res['final_amount']} (−₹{res['discount']})"}


@app.delete("/api/admin/offers/{code}")
def api_admin_offer_delete(code: str, request: Request):
    """🎟️ ADMIN — promo/offer delete."""
    require_admin(request)
    res = PP.delete_offer(code)
    if not res.get("success"):
        raise HTTPException(404, res.get("message_telugu"))
    return res


@app.post("/api/admin/offers/{code}/toggle")
def api_admin_offer_toggle(code: str, request: Request):
    require_admin(request)
    o = PP.get_offer(code)
    if not o:
        raise HTTPException(404, "Offer dorakaledu")
    o["active"] = not o.get("active", True)
    PP._persist()
    return {"success": True, "offer": o,
            "message_telugu": f"✅ {o['code']} {'ON' if o['active'] else 'OFF'}"}


@app.post("/api/admin/ads/{cid}/update")
def api_admin_ads_update(cid: str, payload: dict, request: Request):
    """ADMIN: campaign dates/districts/days/content edit."""
    require_admin(request)
    res = ADS.update_campaign(cid, payload or {})
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


# ============================================================================
#  🌊 WAVE 14 — BOT /matches (personal top-3, Telugu text + structured)
# ============================================================================
@app.get("/api/bot/matches")
def api_bot_matches(tsap_id: str, limit: int = 3):
    """Telegram bot /matches command ki: age-rule + profession-first top-3."""
    me = _find_user(tsap_id.upper())
    if not me:
        raise HTTPException(404, "TSAP ID dorakaledu — /register tho link cheyyandi")
    pool = [u for u in DB_USERS if u.get("tsap_id") != me["tsap_id"] and not u.get("is_banned")
            and not safety.is_blocked(tsap_id.upper(), u.get("tsap_id", ""), DB_BLOCKS)]
    gf = A11.filter_same_gothram(me, pool)
    sf = S12.filter_same_surname(me, gf["kept"])
    af = MP.filter_age_ok(me, sf["kept"])
    rows = topmatch.find_top_matches_v2(me, af["kept"], limit=10, min_score=60)
    rows = MP.rerank_profession(me, rows)[:max(1, min(int(limit or 3), 5))]
    lines = [f"💘 <b>Mee top-{len(rows)} matches</b> (vayasu custom + profession-first)"]
    cards = []
    for i, r in enumerate(rows, 1):
        prof = r.get("profile", {})
        nm = str(prof.get("full_name", "?")).split()[0]
        job = _prof_label(prof)
        nri = " ✈️NRI" if _is_nri(prof) else ""
        lines.append(f"{i}. <b>{nm}</b> • {prof.get('age')}y • {prof.get('caste', '')} • {prof.get('district', '')}{nri}")
        lines.append(f"   {job} • score {r.get('score')} — /view {prof.get('tsap_id', '')}")
        cards.append({"tsap_id": prof.get("tsap_id"), "name": nm, "age": prof.get("age"),
                      "caste": prof.get("caste"), "district": prof.get("district"),
                      "profession": job, "is_nri": _is_nri(prof),
                      "score": r.get("score"), "phone_hidden": True})
    lines.append("📞 Number kavali — premium tho unlock cheyyandi 🙏")
    return {"success": True, "for": tsap_id.upper(), "count": len(cards),
            "text": "\n".join(lines), "matches": cards,
            "skipped": {"gothram": len(gf["skipped_ids"]), "surname": len(sf["skipped_ids"]),
                        "age": len(af["skipped_ids"])},
            "message_telugu": f"💘 Mee top-{len(cards)} matches ready!"}


@app.get("/api/admin/offers")
def api_admin_offers_list(request: Request):
    require_admin(request)
    return {"success": True, "count": len(PP.OFFERS), "offers": list(reversed(PP.OFFERS))}


# ============================================================================
#  📝 WAVE 15 — CMS (public read + admin CRUD)
# ============================================================================
@app.get("/api/cms/pages")
def api_cms_pages():
    return {"success": True, "pages": CMS.list_pages(True)}


@app.get("/api/cms/pages/{slug}")
def api_cms_page(slug: str):
    p = CMS.get_page(slug)
    if not p or not p.get("published"):
        raise HTTPException(404, "Page dorakaledu")
    return {"success": True, "page": p}


@app.get("/api/cms/stories")
def api_cms_stories(tag: str = "", limit: int = 20):
    return {"success": True, "stories": CMS.list_stories(tag, True, limit),
            "tags": CMS.all_tags()}


@app.get("/api/cms/banners")
def api_cms_banners(page: str = ""):
    return {"success": True, "banners": CMS.list_banners(page, False)}


@app.get("/api/cms/tags")
def api_cms_tags():
    return {"success": True, "tags": CMS.all_tags()}


@app.get("/api/admin/cms")
def api_admin_cms(request: Request):
    require_admin(request)
    return {"success": True, "stats": CMS.cms_stats(),
            "pages": CMS.list_pages(False), "stories": CMS.list_stories("", False, 100),
            "banners": CMS.list_banners("", True)}


@app.post("/api/admin/cms/pages")
def api_admin_cms_page(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = CMS.upsert_page(str(d.get("slug", "")), str(d.get("title_en", "")), str(d.get("title_te", "")),
                          str(d.get("body_en", "") or ""), str(d.get("body_te", "") or ""),
                          d.get("photos"), d.get("tags"), d.get("published", True),
                          int(d.get("order", 0) or 0))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/cms/stories")
def api_admin_cms_story(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = CMS.upsert_story(str(d.get("id", "") or ""), str(d.get("groom", "")), str(d.get("bride", "")),
                           str(d.get("photo", "") or ""), str(d.get("story_en", "") or ""),
                           str(d.get("story_te", "") or ""), str(d.get("district", "") or ""),
                           str(d.get("wedding_date", "") or ""), d.get("tags"),
                           d.get("published", True))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/cms/banners")
def api_admin_cms_banner(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = CMS.upsert_banner(str(d.get("id", "") or ""), str(d.get("text_en", "")), str(d.get("text_te", "") or ""),
                            str(d.get("link", "") or ""), d.get("pages", "all"),
                            d.get("active", True), int(d.get("order", 0) or 0))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/cms/delete")
def api_admin_cms_delete(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = CMS.delete_item(str(d.get("kind", "")), str(d.get("id", "") or d.get("slug", "")))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/cms/seed")
def api_admin_cms_seed(request: Request):
    require_admin(request)
    return CMS.seed_cms()


# ============================================================================
#  📡 WAVE 15 — CHANNEL MAPPER + SMART POSTER
# ============================================================================
@app.get("/api/channels/join")
def api_channels_join():
    """Public: Join buttons ki admin-mapped telegram/whatsapp links (active vi matrame)."""
    return {"success": True, "links": CHAN.public_links()}


@app.get("/api/admin/channels/map")
def api_admin_chan_map(request: Request, tier: str = "", q: str = ""):
    require_admin(request)
    items = CHAN.effective()
    if tier:
        items = [e for e in items if e.get("tier") == tier]
    if q:
        ql = q.lower()
        items = [e for e in items if ql in e.get("key", "").lower() or ql in e.get("name", "").lower()]
    return {"success": True, "count": len(items), "channels": items}


@app.post("/api/admin/channels/link")
def api_admin_chan_link(payload: dict, request: Request):
    require_admin(request)
    d = payload or {}
    res = CHAN.set_link(str(d.get("key", "")), str(d.get("telegram", "") or ""),
                        str(d.get("whatsapp", "") or ""), d.get("active", True),
                        str(d.get("note", "") or ""))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.post("/api/admin/channels/import")
def api_admin_chan_import(payload: dict, request: Request):
    """Bulk paste (`Label | tg-link | wa-link`) → fuzzy match → apply."""
    require_admin(request)
    d = payload or {}
    res = CHAN.import_bulk(str(d.get("text", "") or ""), bool(d.get("auto_apply", False)))
    if not res.get("success"):
        raise HTTPException(400, res.get("message_telugu"))
    return res


@app.get("/api/admin/channels/coverage")
def api_admin_chan_coverage(request: Request):
    require_admin(request)
    return CHAN.coverage()


@app.get("/api/admin/poster")
def api_admin_poster(request: Request):
    """Smart poster: queue + random-gap config + pause state (1 screen)."""
    require_admin(request)
    st = wa_queue_stats()
    cfg = dict(WA_ENGINE.cfg())
    return {"success": True,
            "paused": bool(WA_ENGINE.state.get("paused", False)),
            "queue": st.get("queue", st),
            "antiban": st.get("antiban", {}),
            "gaps": {"min_gap": cfg.get("min_gap"), "max_gap": cfg.get("max_gap"),
                     "min_gap_interest": cfg.get("min_gap_interest"),
                     "max_gap_interest": cfg.get("max_gap_interest")},
            "message_telugu": "📮 Smart poster — prati message ki random gap + jitter + coffee-breaks"}


@app.post("/api/admin/poster/gaps")
def api_admin_poster_gaps(payload: dict, request: Request):
    """Jitter range tune (seconds). Safe bounds enforce."""
    require_admin(request)
    d = payload or {}
    try:
        mn = max(30, min(int(d.get("min_gap", 120)), 600))
        mx = max(mn + 10, min(int(d.get("max_gap", 170)), 1800))
    except (ValueError, TypeError):
        raise HTTPException(400, "⚠️ gaps numbers ivvandi (seconds)")
    os.environ["WA_MIN_GAP"] = str(mn)
    os.environ["WA_MAX_GAP"] = str(mx)
    return {"success": True, "gaps": {"min_gap": mn, "max_gap": mx},
            "message_telugu": f"✅ Random gap {mn}–{mx} sec set ayyindi (server restart varaku; permanent ki env lo pettandi)"}


if __name__ == "__main__":
    import sys
    import uvicorn
    _port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=_port)
