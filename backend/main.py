"""
TSAP Matrimony — FastAPI Backend — Pin-to-Pin Perfect Advanced
All endpoints: Register, ID Search, Matches, Credits, Referral, Bureau, Admin, Payment, Channels auto-post
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import os, random, json
from datetime import datetime

# Import our modules
from models import RegisterRequest, RegisterResponse, SearchResponse, MatchResult
from matching_engine import calculate_match_score, generate_personalized_reasons, find_top_matches
from card_generator import generate_id, create_profile_card
from credits import PLANS, can_view_number, deduct_credit, add_credits, can_search_id
from referral import generate_referral_code, process_referral_payment, get_leaderboard, parse_referral_type
from channels_config import (
    CHANNELS, channel_stats, channels_by_tier, route_profile, build_caption,
    build_hashtags, live_channels, pending_channels, all_channels, resolve_caste_key,
)
try:
    from card_pro import create_pro_card, has_telugu_font  # full-detail neat card
except Exception:  # fonts/PIL lekapoyina server padipodu
    create_pro_card = None
    def has_telugu_font():
        return False

from publisher import (
    enqueue, publish_profile, publish_status, read_log, start_worker, worker_running,
    build_whatsapp_text, build_share_text, config as publish_config,
)
from channels_config import post_targets

app = FastAPI(title="TSAP Matrimony API — Ultra Advanced", version="2.0")

@app.on_event("startup")
async def _startup_publisher():
    ok = start_worker()
    st = publish_status()
    print(f"[PUBLISHER] worker={ok} | telegram={'ready' if st['telegram']['configured'] else 'dry-run'} "
          f"| whatsapp={st['whatsapp']['mode']} | live_channels={st['telegram']['live_channels']}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DB (real lo Postgres)
DB_USERS = []
DB_PAYMENTS = []
DB_POSTS = []
DB_REFERRALS = []

# Helper
def encrypt_phone(phone: str) -> str:
    # Mock encrypt — real lo AES
    return f"enc_{phone[-4:]}"

@app.get("/")
def root():
    return {"message": "TSAP Matrimony API — Ultra Advanced, Deep, Never Before 🔥", "status": "LIVE", "version": "2.0", "endpoints": ["/api/register","/api/search/{id}","/api/matches/{id}","/api/payment/webhook","/api/admin/approve/{id}","/api/referral/leaderboard","/api/channels","/api/channels/route","/api/channels/live"]}

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
    seq = random.randint(1000, 9999)
    tsap_id = generate_id(gender, 2025, seq)
    my_ref_code = f"TSAP-REF-{seq}"

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
        "photo_urls": [f"/photos/{tsap_id}_1.jpg"],
        "card_url": f"/cards/{tsap_id}.png",
        "is_verified": False,
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
    DB_USERS.append(user)

    # 4. Card Gen — FULL DETAIL NEAT CARD (Pillow). Fail ayithe path matrame istundi.
    card_path = f"/tmp/cards/{tsap_id}.png"
    try:
        if create_pro_card:
            os.makedirs("/tmp/cards", exist_ok=True)
            create_pro_card(user, card_path)
            user["card_generated"] = True
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
        pub = enqueue(user, tsap_id, score=92,
                      photo_path=card_path if user.get("card_generated") else None)
        user["publish_targets"] = pub["targets"]

    # 7. Top 3 matches (from existing DB)
    opposite = "Bride" if gender=="Groom" else "Groom"
    candidates = [u for u in DB_USERS if u["gender"]==opposite and u["tsap_id"]!=tsap_id]
    top_matches = []
    for cand in candidates[:20]:
        score = calculate_match_score(user, cand, wants_same_caste=True)
        if score>=70:
            reasons = generate_personalized_reasons(user, cand, score)
            top_matches.append(MatchResult(matched_user_id=cand["tsap_id"], score=score, reasons=reasons))
    top_matches = sorted(top_matches, key=lambda x: x.score, reverse=True)[:3]

    return RegisterResponse(
        tsap_id=tsap_id,
        card_url=card_path,
        credits=3,
        message_telugu=f"🎉 Congratulations! Me ID: {tsap_id}. Me profile admin approve lo undi (2 min). Top 3 FREE matches ready!",
        next_steps=["Admin approve (2 min)", "Top 3 FREE with reason", "₹99 pay → 10 numbers + daily auto", "Referral share → earn ₹30"],
        auto_post_queue=auto_queue,
        top_3_matches=top_matches,
        publish_queued=pub.get("queued", False),
        publish_targets=pub.get("targets", []),
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
    """Registry channel → website-friendly JSON (join link, status, deep link, hashtags)."""
    user = ch["username"]
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
    }

@app.get("/api/channels")
def channels(tier: Optional[str] = None):
    """FULL master registry — 65 channels (L0 Official → L4 Special)."""
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
            "L1_REGION": "State + gender flagship — TS/AP Bride & Groom, NRI",
            "L2_RELIGION": "Hindu, Muslim, Christian, Other, Inter-faith",
            "L3_CASTE": "Hindu caste-wise — ONE channel per caste (43)",
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

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
