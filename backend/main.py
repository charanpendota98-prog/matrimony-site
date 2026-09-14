"""
TSAP Matrimony — FastAPI Backend — Pin-to-Pin Perfect Advanced
All endpoints: Register, ID Search, Matches, Credits, Referral, Bureau, Admin, Payment, Channels auto-post
"""
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Any, Dict, Optional
import os, random, json
from datetime import datetime, timedelta

# Import our modules
from models import RegisterRequest, RegisterResponse, SearchResponse, MatchResult
from matching_engine import (
    calculate_match_score, generate_personalized_reasons, find_top_matches,
    generate_profile_highlights,
)
from card_generator import generate_id, create_profile_card
from credits import PLANS, can_view_number, deduct_credit, add_credits, can_search_id
from referral import generate_referral_code, process_referral_payment, get_leaderboard, parse_referral_type
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
from interest import (
    PLANS as INTEREST_PLANS, plan_list, get_plan, plan_by_amount,
    can_send_interest, create_interest, respond_interest, expire_old,
    interest_to_owner_text, interest_accepted_text, interest_declined_text,
    interest_notify_text, inbox_for, sent_for, safe_user,
    MAX_PER_DAY as INTEREST_MAX_PER_DAY, EXPIRY_DAYS as INTEREST_EXPIRY_DAYS,
)
from card_generator import generate_id as _gen_id
from porutham import compute_porutham, porutham_line, norm_nakshatra, norm_rasi
import topmatch, safety, preview, bot_pool, wa_pool
from interest import ADDONS, RENEWALS, is_addon, get_addon, get_renewal, plan_list_with_free, addon_list, renewal_offer
from channels_config import post_targets

app = FastAPI(title="TSAP Matrimony API — Ultra Advanced", version="2.0")

# Card + photo files static ga serve — /cards/{id}.png browser lo direct open avutundi
try:
    from fastapi.staticfiles import StaticFiles
    os.makedirs("/tmp/cards", exist_ok=True)
    os.makedirs("/tmp/photos", exist_ok=True)
    app.mount("/cards", StaticFiles(directory="/tmp/cards"), name="cards")
    app.mount("/photos", StaticFiles(directory="/tmp/photos"), name="photos")
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
    # 1. Validate
    if age < 18: raise HTTPException(400, "Age must be 18+ (Bride) / 21+ (Groom)")

    # 2. ID Gen
    tsap_id = unique_tsap_id(gender, 2025)
    # referral code — TSAP ID nunchi derive (unique, deterministic) [FIX: mundu undefined `seq` tho crash avutundi]
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
        "referral_code": my_ref_code,
        "referred_by": referral_code,
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

    # 5. Referral — if referred_by exists, update stats
    if referral_code:
        for u in DB_USERS:
            if u["referral_code"]==referral_code or u["phone"]==referral_code:
                u["referral_stats"]["total"] += 1

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
            w1 = enqueue_whatsapp([phone], namaste_text(user, tsap_id), image_path=card_path,
                                  priority=0, kind="namaste_welcome")
            welcome["queued"] = bool(w1.get("queued"))
            welcome["wa_result"] = w1
            admin_no = os.getenv("ADMIN_WHATSAPP_NUMBER", "").strip()
            if admin_no:
                w2 = enqueue_whatsapp([admin_no], admin_new_profile_text(user, tsap_id, source="website"),
                                      image_path=card_path, priority=1, kind="admin_new_profile")
                welcome["admin_alert"] = bool(w2.get("queued"))
        elif phone:
            welcome["manual_text"] = namaste_text(user, tsap_id)
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
    top_matches = []
    for cand in candidates[:20]:
        score = calculate_match_score(user, cand, user_wants_same_caste=True)
        if score>=70:
            reasons = generate_personalized_reasons(user, cand, score)
            top_matches.append(MatchResult(matched_user_id=cand["tsap_id"], score=score, reasons=reasons))
    top_matches = sorted(top_matches, key=lambda x: x.score, reverse=True)[:3]

    return RegisterResponse(
        tsap_id=tsap_id,
        card_url=user.get("card_url", card_url),
        credits=3,
        message_telugu=f"🎉 Congratulations! Me ID: {tsap_id}. Me profile admin approve lo undi (2 min). Top 3 FREE matches ready!",
        next_steps=["Admin approve (2 min)", "Top 3 FREE with reason", "₹99 pay → 10 numbers + daily auto", "Referral share → earn ₹30"],
        auto_post_queue=auto_queue,
        top_3_matches=top_matches,
        publish_queued=pub.get("queued", False),
        publish_targets=pub.get("targets", []),
        namaste_queued=bool(welcome.get("queued") or welcome.get("manual_text")),
        welcome_status=welcome,
        share_kit=share_kit(user, tsap_id),
        share_text=build_share_text(user, tsap_id),
    )

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
        # Mock for demo
        user = {
            "tsap_id": tsap_id,
            "gender": "Bride" if "-F-" in tsap_id else "Groom",
            "age": 24, "height":"5'4\"", "caste":"Reddy", "education":"BTech", "job":"Software", "salary":"60k",
            "state":"TS", "district":"Nalgonda", "mandal":"Gachibowli", "gothram":"Bharadwaj", "star":"Rohini",
            "marital_status":"Pelli Kaledu", "phone":"98480xxxxx", "credits":3, "plan":"FREE", "privacy_mode":"public"
        }

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

    return {
        "profile": user,
        "can_view_profile": True,
        "can_view_number": search_logic["can_view_number"],
        "can_view_number_reason": search_logic["message"],
        "is_photo_blur": viewer.get("plan","FREE")=="FREE" and user.get("privacy_mode")=="private",
        "reasons": reasons,
        "credits_needed": 1,
        "viewer_credits": viewer.get("credits",0)
    }

@app.get("/api/matches/{tsap_id}")
def get_matches(tsap_id: str, min_score: int = 70, limit: int = 20, caste_filter: Optional[str] = None):
    """
    Matches — Only 70%+ + personalized reasons
    Pin-to-Pin: Opposite gender, score, filter, reason
    """
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user:
        raise HTTPException(404, "User not found")

    all_profiles = DB_USERS
    if caste_filter:
        all_profiles = [p for p in all_profiles if p["caste"]==caste_filter]

    top = find_top_matches(user, all_profiles, limit=limit, min_score=min_score)

    return {"user_id": tsap_id, "total_found": len(top), "matches": top, "filter": caste_filter or "All", "min_score": min_score}

@app.post("/api/credits/deduct/{tsap_id}")
def deduct_credit_api(tsap_id: str, target_id: str):
    """1 credit = 1 number view"""
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user: raise HTTPException(404, "User not found")
    result = deduct_credit(user)
    if not result["success"]:
        return JSONResponse(status_code=402, content={"message_telugu": result["message_telugu"], "credits": 0, "pay_url": "/pay?plan=TRIAL_99"})
    # log
    return {"success": True, "credits_left": result["credits"], "target_number": "98480xxxxx", "message_telugu": result["message_telugu"]}

@app.post("/api/payment/webhook")
def payment_webhook(user_id: str, amount: int, razorpay_payment_id: str, referral_code: str = ""):
    """
    Razorpay webhook → verify → add credits → referral commission
    Pin-to-Pin:
    1. Verify payment (mock)
    2. Add credits based on plan
    3. If referral_code → process commission
    4. Daily scheduler ON
    5. Send numbers unlock
    """
    user = next((u for u in DB_USERS if u["tsap_id"]==user_id), None)
    if not user: raise HTTPException(404, "User not found")

    # Determine plan by amount
    plan_map = {99: "TRIAL_99", 299: "PREMIUM_299", 999: "VIP_999"}
    plan_key = plan_map.get(amount, "TRIAL_99")

    credit_result = add_credits(user, plan_key, payment_verified=True)

    # Referral commission
    referral_result = None
    if user.get("referred_by"):
        referral_result = process_referral_payment(user, user["referred_by"], amount, DB_USERS)

    return {
        "success": True,
        "user_id": user_id,
        "plan": plan_key,
        "credits_added": PLANS[plan_key]["credits"],
        "total_credits": user["credits"],
        "daily_quota": PLANS[plan_key]["daily"],
        "referral_commission": referral_result,
        "message_telugu": f"🎉 Payment success! {PLANS[plan_key]['credits']} credits add ayyayi. Rojoo {PLANS[plan_key]['daily']} matches vasthayi!"
    }

@app.get("/api/referral/leaderboard")
def leaderboard():
    board = get_leaderboard(DB_USERS, limit=10)
    return {"leaderboard": board, "total_users": len(DB_USERS)}

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
def admin_make_premium(tsap_id: str, gift_credits: int = 10):
    """Manual premium — admin gift"""
    user = next((u for u in DB_USERS if u["tsap_id"]==tsap_id), None)
    if not user: raise HTTPException(404, "Not found")
    user["credits"] += gift_credits
    user["plan"] = "PREMIUM_299"
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
    """FULL master registry — 83 channels (L0 Official → L4 Special, caste × bride/groom)."""
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
def publish_status_endpoint():
    """Telegram + WhatsApp auto-publish status (dry-run? tokens unnai? enni targets?)"""
    return {"success": True, **publish_status(), "worker_running": worker_running()}

@app.get("/api/publish/log")
def publish_log_endpoint(limit: int = 20):
    """Ee varaku publish ayyina profiles log (audit)."""
    return {"success": True, "count": limit, "log": read_log(limit)}

@app.post("/api/publish/now/{tsap_id}")
async def publish_now(tsap_id: str, score: int = 92):
    """Manual re-post (admin) — already register ayyina profile ni malli channels ki pampu."""
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
def credits_endpoint(tsap_id: str):
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
def credits_buy(payload: dict):
    """
    Plan buy — Razorpay live ayyaka ee endpoint webhook tho kalisipothundi.
    Ippudu: PAYMENT_AUTO_APPROVE=true (dev/demo) ayithe ventane credits add; leda order create chesi
    UPI/Razorpay link istundi (manual verify).
    """
    tsap_id = (payload or {}).get("tsap_id", "")
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
    auto = str(os.getenv("PAYMENT_AUTO_APPROVE", "true")).lower() in ("1", "true", "yes", "on")
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
async def interest_send(payload: dict):
    """
    💌 Interest pampu — 1 credit. Owner ki WhatsApp lo REQUESTER PROFILE + card veltundi.
    (idi user adigina core flow: chatting ledu, WhatsApp lo profile share matrame)
    """
    d = payload or {}
    from_id = d.get("from_id", "").strip()
    to_id = d.get("to_id", "").strip()
    note = d.get("note", "")

    frm, to = _find_user(from_id), _find_user(to_id)
    if not frm:
        raise HTTPException(404, f"Mee TSAP ID dorakaledu: {from_id} — mundu register cheyyandi")
    if not to:
        raise HTTPException(404, f"Profile dorakaledu: {to_id}")

    if safety.is_blocked(from_id, to_id, DB_BLOCKS):
        raise HTTPException(400, "Ee profile tho contact block ayyindi — vere profiles chudandi")
    if to.get("is_banned"):
        raise HTTPException(400, "Ee profile moderation lo teesesaru — interest pampaleeru")

    expire_old(DB_INTERESTS)
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
def interest_inbox(tsap_id: str):
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found")
    expire_old(DB_INTERESTS)
    data = inbox_for(u, DB_USERS, DB_INTERESTS)
    data["credits"] = u.get("credits", 0)
    data["model"] = "accept → number exchange (chatting ledu)"
    return data


@app.get("/api/interest/sent/{tsap_id}")
def interest_sent(tsap_id: str):
    u = _find_user(tsap_id)
    if not u:
        raise HTTPException(404, "User not found")
    expire_old(DB_INTERESTS)
    data = sent_for(u, DB_USERS, DB_INTERESTS)
    data["credits"] = u.get("credits", 0)
    return data


@app.post("/api/interest/respond")
async def interest_respond(payload: dict):
    """Owner accept/decline. Accept → rendu numbers WhatsApp lo (consent based). Decline → credit refund."""
    d = payload or {}
    tsap_id = d.get("tsap_id", "")
    request_id = d.get("request_id", "")
    action = (d.get("action", "") or "").lower()
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
    elif action == "decline":
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
def wa_dead(limit: int = 50):
    """💀 Dead-letter list — 3 tries ayyaka kooda deliver kaani messages (bridge problem)."""
    return dead_letters(limit)


@app.post("/api/wa/dead/requeue")
def wa_dead_requeue(limit: int = 20):
    """Bridge fix ayyaka dead-letters ni malli queue lo vey."""
    return requeue_dead(limit)


@app.get("/api/bots/health")
def bots_health():
    """🤖 Telegram bots health + failover order (primary → backup → alert)."""
    return {"ok": True, **bot_pool.bot_health()}


@app.post("/api/wa/pause")
def wa_pause(reason: str = "manual"):
    return {"ok": True, **WA_ENGINE.pause(reason)}


@app.post("/api/wa/resume")
def wa_resume():
    return {"ok": True, **WA_ENGINE.resume()}


@app.post("/api/wa/reset_day")
def wa_reset_day():
    """Test tip: ee roju counters reset (caps fresh). Production lo vaddu."""
    return {"ok": True, **WA_ENGINE.reset_today()}


@app.post("/api/demo/seed")
def demo_seed():
    """
    Demo profiles create (frontend test cheyyadaniki) — idempotent, dev convenience.
    DEMO_SEED_ENABLED=false chesthe bandh.
    """
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
        dict(prefer_id="TSAP-M-2025-1042", gender="Groom", full_name="Kiran Kumar Reddy", age=29, caste="Reddy",
             sub_caste="Deshathi", education="MBBS", education_detail="MD", job="Doctor", company="Apollo",
             salary="2L+/mo", height="5'10\"", weight="74kg", district="Nalgonda", state="TS", gothram="Vasishta",
             star="Mrigasira", rasi="Dhanu", phone="9848033333", family_type="Nuclear",
             family_status="Middle Class", marital_status="Pelli Kaledu", is_verified=True),
        dict(prefer_id="TSAP-M-2025-4042", gender="Groom", full_name="Arjun Chowdary", age=31, caste="Kamma",
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
        dict(gender="Groom", full_name="Sai Krishna Brahmin", age=28, caste="Brahmin", sub_caste="Niyogi",
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
                "is_approved": True, "privacy_mode": "public", "referral_code": f"MV{tsap_id[-4:]}",
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
def record_view(payload: dict):
    """
    Profile view record — "evaru chusaru" feature (top matrimony sites lo idi paid).
    Same viewer 6 గంటల్లో malli chuste duplicate ga count avvadu.
    """
    d = payload or {}
    tsap_id = (d.get("tsap_id") or "").strip()
    viewer_id = (d.get("viewer_id") or "").strip()
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
    DB_VIEWS.append({"tsap_id": tsap_id, "viewer_id": viewer_id, "at": now.isoformat()})
    total = len([v for v in DB_VIEWS if v["tsap_id"] == tsap_id])
    return {"success": True, "counted": True, "total_views": total}


@app.get("/api/views/{tsap_id}")
def views_for(tsap_id: str):
    """
    Views summary. FREE users ki count + city/caste level info;
    paid (credits/plan) unte **names tho** full list (whoviewed add-on leda ₹299+ plan).
    """
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
def toggle_save(payload: dict):
    """❤️ Shortlist — profile save/remove (top matrimony sites lo idi must feature)."""
    d = payload or {}
    tsap_id = (d.get("tsap_id") or "").strip()
    saved_id = (d.get("saved_id") or "").strip()
    if not tsap_id or not saved_id:
        raise HTTPException(400, "tsap_id + saved_id kavali")
    if tsap_id == saved_id:
        raise HTTPException(400, "Mee profile ni meeru save cheyyakkarledu 🙂")
    existing = next((x for x in DB_SAVES if x["tsap_id"] == tsap_id and x["saved_id"] == saved_id), None)
    if existing:
        DB_SAVES.remove(existing)
        return {"success": True, "saved": False, "message_telugu": "Shortlist nunchi teesesaaru",
                "total_saved": len([x for x in DB_SAVES if x["tsap_id"] == tsap_id])}
    DB_SAVES.append({"tsap_id": tsap_id, "saved_id": saved_id, "at": datetime.utcnow().isoformat()})
    return {"success": True, "saved": True, "message_telugu": "❤️ Shortlist lo save ayyindi",
            "total_saved": len([x for x in DB_SAVES if x["tsap_id"] == tsap_id])}


@app.get("/api/saved/{tsap_id}")
def saved_list(tsap_id: str):
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
    ext = (file.filename or "").split(".")[-1].lower()
    allowed = {"jpg", "jpeg", "png", "webp", "heic", "heif"}
    if ext not in allowed:
        raise HTTPException(400, "Photo format JPG/PNG/WebP matrame — malli try cheyyandi")
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(413, "Photo 5MB kanna peddadi undi — chinna photo pettandi (app lo ne compress avutundi)")
    if len(data) < 1024:
        raise HTTPException(400, "Photo khali ga undi — malli upload cheyyandi")
    os.makedirs("/tmp/photos", exist_ok=True)
    token = (tsap_id.strip() or "tmp") + "-" + datetime.utcnow().strftime("%y%m%d%H%M%S") + "-" + str(random.randint(100, 999))
    name = f"{token}.{ 'jpg' if ext in ('heic','heif') else ext }"
    path = f"/tmp/photos/{name}"
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise HTTPException(500, f"Photo save avvaledu: {str(e)[:80]}")
    return {"success": True, "url": f"/photos/{name}", "bytes": len(data),
            "kb": round(len(data) / 1024, 1), "path": path,
            "message_telugu": f"📸 Photo upload ayyindi ({round(len(data)/1024)} KB)"}


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
    code = f"{random.randint(1000, 9999)}"
    DB_OTPS[phone] = {"code": code, "expires": (datetime.utcnow() + timedelta(minutes=10)).isoformat(),
                      "tries": 0}
    dev = str(os.getenv("OTP_DEV_MODE", "true")).lower() in ("1", "true", "yes", "on")
    out = {"success": True, "phone": f"XXXXXX{phone[-4:]}", "expires_in_min": 10,
           "message_telugu": f"📱 OTP pampinchaam (+91 XXXXXX{phone[-4:]}). 10 nimushalalo enter cheyyandi."}
    if dev:
        out["dev_code"] = code
        out["message_telugu"] += f" [DEV MODE — code: {code}]"
        out["note"] = "Production lo SMS provider (MSG91/Fast2SMS) configure cheyyandi — appudu ee code response lo raadu."
    else:
        out["message_telugu"] += " SMS provider configure cheyyaledu — support ki cheppandi."
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
        raise HTTPException(429, "Chala sarlu try chesaru — kotha OTP teesukondi")
    if code != rec["code"]:
        return JSONResponse(status_code=400, content={"success": False, "message_telugu": "❌ OTP tappu — malli try cheyyandi",
                                                      "tries_left": max(0, 5 - rec["tries"])})
    VERIFIED_PHONES.add(phone)
    DB_OTPS.pop(phone, None)
    u = next((x for x in DB_USERS if x.get("phone") == phone), None)
    if u:
        u["phone_verified"] = True
    return {"success": True, "phone_verified": True, "message_telugu": "✅ Number verify ayyindi — mee profile ki verified badge vasthundi"}


@app.get("/api/search")
def advanced_search(
    gender: Optional[str] = None, caste: Optional[str] = None, district: Optional[str] = None,
    state: Optional[str] = None, job: Optional[str] = None, education: Optional[str] = None,
    age_min: int = 18, age_max: int = 60, salary_min: int = 0,
    marital_status: Optional[str] = None, verified_only: bool = False, photo_only: bool = False,
    religion: Optional[str] = None, q: Optional[str] = None,
    sort: str = "score", viewer_id: Optional[str] = None, limit: int = 30, offset: int = 0,
):
    """
    🔎 Advanced filters — caste / district / age range / salary / job / verified / photo / search text.
    Frontend /matches page idi use chestundi (fallback: demo data).
    """
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
    if religion:
        items = [u for u in items if str(u.get("religion", "Hindu")).lower() == religion.lower()]
    if verified_only:
        items = [u for u in items if u.get("is_verified") or u.get("phone_verified")]
    if photo_only:
        items = [u for u in items if u.get("photo_urls")]
    items = [u for u in items if age_min <= int(u.get("age", 0) or 0) <= age_max]
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

    if sort == "score" and viewer:
        out.sort(key=lambda x: -int(x.get("score", 0) or 0))
    elif sort == "new":
        out.sort(key=lambda x: str(x.get("tsap_id", "")), reverse=True)
    elif sort == "age":
        out.sort(key=lambda x: int(x.get("age", 99) or 99))
    elif sort == "porutham":
        out.sort(key=lambda x: -int(((x.get("porutham") or {}).get("score") or 0)))
    elif sort == "boosted":
        out.sort(key=lambda x: (not x.get("boosted"), -int(x.get("score", 0) or 0)))

    return {
        "total": len(out), "count": len(out[offset:offset + limit]), "offset": offset, "limit": limit,
        "sort": sort,
        "filters": {"gender": gender, "caste": caste, "district": district, "state": state, "job": job,
                    "education": education, "age": [age_min, age_max], "salary_min": salary_min,
                    "marital_status": marital_status, "verified_only": verified_only, "photo_only": photo_only,
                    "religion": religion, "q": q},
        "results": out[offset:offset + limit],
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
async def publish_digest():
    """Digest ni Telegram live channels + WhatsApp queue ki (anti-ban gap tho) pampu."""
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
    ok, kind, lead = save_lead(str(p.get("name", "")), str(p.get("phone", "")),
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
def api_leads(status: str = "", limit: int = 100):
    """Admin — leads list (follow-up ki). Deploy lo ADMIN_TOKEN env tho protect cheyyali."""
    return leads_list(status, limit)


@app.get("/api/leads/stats")
def api_lead_stats():
    """Traffic + conversion dashboard: visits, channels, top pages, lead sources, inventory."""
    st = lead_stats()
    st["inventory"] = inventory_status(len(DB_USERS))
    st["whatsapp"] = wa_queue_stats()
    return st


@app.post("/api/leads/followup/{lead_id}")
def api_lead_followup(lead_id: str):
    """Lead ki WhatsApp follow-up pampu (mana side nunchi)."""
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
def api_bulk_profiles(payload: dict):
    """
    Launch inventory load — realistic profiles (seed_launch_db.py nunchi).
    body: {"profiles": [ ... ]}  leda  {"generate": 360}
    """
    import seed_launch_db
    profiles = (payload or {}).get("profiles") or []
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
def api_seed_launch(payload: dict = None):
    """Shortcut: demo profiles ventane load (dev/preview ki). DEMO_SEED_ENABLED=false chesthe bandh."""
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
def api_top_matches(tsap_id: str, limit: int = 10, min_score: int = 65):
    """Top matches 2.0 — mutual bonus tho rank, blocked/banned profiles teesestham."""
    me = _find_user(tsap_id)
    if not me:
        raise HTTPException(404, "Mee profile dorakaledu")
    pool = [u for u in DB_USERS if not safety.is_blocked(tsap_id, u.get("tsap_id", ""), DB_BLOCKS)
            and not u.get("is_banned")]
    rows = topmatch.find_top_matches_v2(me, pool, limit=limit, min_score=min_score)
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
        out.append(r)
    return {"tsap_id": tsap_id, "count": len(out), "mutual_matches": len([x for x in out if x.get("mutual", {}).get("both_like")]),
            "results": out,
            "message_telugu": "%d top matches — mutthu (mutual) matches: %d" % (len(out), len([x for x in out if x.get("mutual", {}).get("both_like")]))}


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
def api_report(payload: dict):
    d = payload or {}
    ok, kind, rec = safety.submit_report(str(d.get("reporter_id", "")), str(d.get("target_id", "")),
                                         str(d.get("category", "")), str(d.get("detail", "")),
                                         reports=DB_REPORTS, users=DB_USERS)
    if not ok:
        raise HTTPException(400, kind)
    return {"success": True, "kind": kind, "report": rec,
            "auto_hidden": bool(rec.get("auto_flagged")),
            "ack_telugu": safety.report_ack_text(),
            "stats": safety.report_stats(DB_REPORTS)}


@app.get("/api/moderation/queue")
def api_moderation_queue(limit: int = 50):
    return safety.moderation_queue(DB_REPORTS, DB_USERS, limit)


@app.post("/api/moderation/resolve/{report_id}")
def api_moderation_resolve(report_id: str, payload: dict = None):
    d = payload or {}
    ok, msg, rec = safety.resolve_report(report_id, str(d.get("action", "")), str(d.get("note", "")),
                                         reports=DB_REPORTS, users=DB_USERS)
    if not ok:
        raise HTTPException(400, msg)
    return {"success": True, "action": msg, "report": rec, "queue": safety.report_stats(DB_REPORTS)}


@app.post("/api/block")
def api_block(payload: dict):
    d = payload or {}
    ok, kind, rec = safety.block_user(str(d.get("owner", "")), str(d.get("blocked", "")),
                                      str(d.get("reason", "")), DB_BLOCKS)
    if not ok:
        raise HTTPException(400, kind)
    return {"success": True, "kind": kind, "block": rec, "total_blocks": len(safety.block_list(d.get("owner", ""), DB_BLOCKS)),
            "message_telugu": "🚫 Block chesaru — vaallu mee profile chudalenu, interest kooda pampalenru"}


@app.post("/api/unblock")
def api_unblock(payload: dict):
    d = payload or {}
    ok, msg = safety.unblock_user(str(d.get("owner", "")), str(d.get("blocked", "")), DB_BLOCKS)
    return {"success": ok, "kind": msg,
            "message_telugu": "Unblock ayyindi" if ok else "Ee user block list lo ledu"}


@app.get("/api/blocks/{tsap_id}")
def api_blocks(tsap_id: str):
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
def api_verification(tsap_id: str):
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



if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
