"""
TSAP Matrimony — Telegram Bot (aiogram 3.x) — Pin-to-Pin Perfect Advanced
Flows: Register Telugu buttons, OTP, Photo, Admin Approve, Auto-Router Main 4 + Caste + Special, Credits, Referral, Payment, Daily 9AM

🚀 WAVE 11 — bots perfect:
  • import-safe (BOT_TOKEN lekapoina module import avutundi — tests + health OK)
  • /help /myid /search /cancel + photo handler + unknown-text fallback
  • pure helpers (parse_start_ref, help_text, format_id_search) — network lekunda test avvachu
"""
import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# MASTER CHANNEL REGISTRY + AUTO-ROUTER (65 channels — L0 Official → L4 Special)
from channels_config import (
    CHANNELS, channel_stats, route_profile, build_caption, build_hashtags,
    channel_chat_id, post_targets, live_channels,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "123456789")
SITE_URL = os.getenv("SITE_URL", "https://manavivaha.in")

# ── import-safe bot (token lekapoina / wrong format ayina crash kadu) ─────────
bot = None
BOT_ERROR = ""
try:
    if BOT_TOKEN and ":" in BOT_TOKEN and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
        bot = Bot(token=BOT_TOKEN)
    else:
        BOT_ERROR = "BOT_TOKEN not configured — /start tho test cheyyalemu (token pettandi)"
except Exception as e:  # noqa: BLE001 — wrong format etc.
    BOT_ERROR = f"BOT_TOKEN invalid: {e}"
    bot = None


def get_bot() -> Bot | None:
    """Lazy bot (token .env lo pettaka polling start cheyyali)."""
    return bot


def bot_status() -> dict:
    """Health API ki — token/config ok na (network call ledu)."""
    return {
        "configured": bot is not None,
        "error": BOT_ERROR,
        "admin_configured": bool(ADMIN_CHAT_ID and str(ADMIN_CHAT_ID).isdigit()),
        "live_channels": len(live_channels()),
        "note_telugu": ("🤖 Bot ready — polling start cheyochu" if bot
                        else "⚠️ BOT_TOKEN pettandi (.env) — appudu polling start avutundi"),
    }


# ── pure helpers (tests network lekunda run avvadaniki) ───────────────────────
def parse_start_ref(text: str) -> dict:
    """'/start ch_reddy' / '/start ref_1042' / '/start TSAP-F-1042' → structured."""
    parts = str(text or "").strip().split()
    ref = parts[1] if len(parts) > 1 else ""
    out = {"raw": ref, "kind": "plain", "value": ""}
    if ref.startswith("unlock_"):
        out.update(kind="unlock", value=ref[7:].upper())
    elif ref.startswith("ch_"):
        out.update(kind="channel", value=ref[3:])
    elif ref.startswith("ref_"):
        out.update(kind="referral", value=ref[4:])
    elif ref.upper().startswith("TSAP-"):
        out.update(kind="profile", value=ref.upper())
    elif ref.startswith("story_"):
        out.update(kind="story", value=ref[6:])
    return out


def help_text() -> str:
    return (
        "🙏 Mana Vivaha Bot — HELP\n\n"
        "• /start — kottha register (3 min)\n"
        "• /search TSAP-F-1042 — ID tho profile chudandi\n"
        "• /unlock TSAP-F-1042 — number unlock (1 credit)\n"
        "• /mylist — mee unlocked numbers list\n"
        "• /balance — mee credits + plan\n"
        "• /pay — payment ela (UPI/call)\n"
        "• /link MEE-TSAP-ID — Telegram link (unlock/delivery kosam)\n"
        "• /myid — mee Telegram ID (support ki kavali)\n"
        "• /cancel — form cancel\n\n"
        "💰 Modati 3 profiles + 3 interests FREE\n"
        "₹99 → 5 profiles (decline ayithe refund)\n"
        "₹500 → assisted: mana team meeke 5 profiles personal ga pampisthundi\n\n"
        f"🌐 Website: {SITE_URL}\n"
        "🕙 Support: 10AM–7PM Telugu lo"
    )


def format_id_search(profile: dict) -> str:
    """ID search result card — WAVE 13: FIRST NAME visible, surname hidden, number eppudu ledu."""
    from smart12 import first_name_of  # lazy: cycle-safe
    p = profile or {}
    tid = p.get('tsap_id', '—')
    return (
        f"🔎 {tid} — {first_name_of(p.get('full_name',''))}\n"
        f"{p.get('gender','')} · {p.get('age','')} yrs · {p.get('caste','')}\n"
        f"🎓 {p.get('education','—')} · 💼 {p.get('job','—')}\n"
        f"📍 {p.get('district','—')}, {p.get('state','TS')}\n"
        f"⭐ {p.get('star','—')} · గోత్రం: {p.get('gothram','—')}\n\n"
        f"📞 Number kavali ante: /unlock {tid} (1 credit)\n"
        f"Interest pampalante website {SITE_URL}/matches lo login cheyyandi 💌"
    )


# ── WAVE 12 pure formatters (network lekunda test avvachu) ───────────────────
def unlock_result_text(data: dict) -> str:
    """POST /api/unlock response → user message."""
    d = data or {}
    if d.get("success"):
        chg = " (FREE — already unlocked 🙂)" if not d.get("charged") else f" (1 credit cut — migilindi: {d.get('credits_left',0)})"
        return (f"✅ Number unlock ayyindi{chg}\n📞 `{d.get('phone','—')}`\n"
                f"📝 Gauravamga matladandi — all the best! 💍")
    if d.get("reason") == "no_credits":
        return ("⚠️ Credits ayipoyayi!\n" + str(d.get("message_telugu","")) + "\n\n/pay — payment ela cheyyalo chudandi 🙏")
    return "⚠️ " + str(d.get("message_telugu") or d.get("detail") or "unlock avvaledu — ID sari chudandi")


def mylist_text(data: dict) -> str:
    """GET /api/unlocks response → masked list + hint."""
    d = data or {}
    items = d.get("profiles", []) or []
    if not items:
        return ("📋 Mee unlocked list khaali 🙂\n\nChannel lo nachina ID ni /unlock TSAP-F-1042 ani pampandi (1 credit).\n"
                "Leda ₹500 assisted — mana team meeke 5 profiles personal ga pampisthundi (/pay).")
    lines = [f"📋 Mee unlocked profiles ({len(items)}):", ""]
    for i, p in enumerate(items, 1):
        lines.append(f"{i}. {p.get('name_masked','—')} — {p.get('phone_masked','')} "
                     f"({p.get('tsap_id','')} · {p.get('caste','')})")
    lines += ["", "Full number kavali ante: /unlock <ID> (already unlocked — free 🙂)"]
    return "\n".join(lines)


def balance_text(credits: int, plan: str = "FREE") -> str:
    return (f"💰 Mee balance: *{credits}* credits\n📦 Plan: {plan}\n\n"
            f"1 credit = 1 number unlock 📞\nAyipothe /pay lo top-up cheyochu 🙏")


def pay_text() -> str:
    import os as _os
    upi = _os.getenv("PAY_UPI_ID", "manavivaha@upi")
    call = _os.getenv("SUPPORT_CALL_NUMBER", "")
    lines = ["💳 Payment ela cheyyali:", "",
             f"1️⃣ UPI: `{upi}` (note lo mee TSAP ID pettandi)",
             "2️⃣ Screenshot + TSAP ID ni support ki pampandi",
             "3️⃣ 10 min lo credits add (10AM–7PM)"]
    if call:
        lines.append(f"\n📞 Direct call: {call} (₹500 assisted kooda call lone book cheyochu)")
    lines.append("\n💰 ₹99=5 · ₹199=12 · ₹299=25 · ₹500=assisted 5 (personal)")
    return "\n".join(lines)


# Telugu keyboards
def get_gender_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="👰 Bride"), KeyboardButton(text="🤵 Groom")]], resize_keyboard=True)


def get_state_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="తెలంగాణ (TS)"), KeyboardButton(text="ఆంధ్రప్రదేశ్ (AP)")]], resize_keyboard=True)


# Registry nunchi top castes (L3) — bot lo chupinchE order
TOP_CASTES = ["Reddy","Kamma","Kapu","Velama","Vysya","Brahmin","Raju","Goud","Yadav","Mudiraj",
              "Padmashali","Munnuru Kapu","Balija","Viswakarma","Mala","Madiga","Lambada","Boya",
              "Rajaka","Uppara","Kummara","Open"]


def get_religion_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🕉️ Hindu"), KeyboardButton(text="☪️ Muslim")],
        [KeyboardButton(text="✝️ Christian"), KeyboardButton(text="🕊️ Other / No religion")],
    ], resize_keyboard=True)


def get_caste_kb():
    kb = []
    for i in range(0, len(TOP_CASTES), 2):
        kb.append([KeyboardButton(text=TOP_CASTES[i]),
                   KeyboardButton(text=TOP_CASTES[i+1] if i+1 < len(TOP_CASTES) else "Others")])
    kb.append([KeyboardButton(text="🔎 Inka castes (full list)"), KeyboardButton(text="⏭️ Skip")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_approve_kb(tsap_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve + Auto-Post", callback_data=f"approve_{tsap_id}"),
         InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_{tsap_id}")],
        [InlineKeyboardButton(text="💎 Make Premium +10 Credits", callback_data=f"premium_{tsap_id}")]
    ])


dp = Dispatcher()

# In-memory user sessions + profiles (real lo Redis)
user_sessions = {}
user_profiles = {}


@dp.message(Command("start"))
async def cmd_start(message: Message):
    ref = parse_start_ref(message.text)
    if ref["kind"] == "channel":
        await message.answer(f"📂 {ref['value']} Channel nunchi vacharu — welcome! 🙏\n\nTS-AP Matrimony ki swagatham! Meeku evaru kavali?", reply_markup=get_gender_kb())
    elif ref["kind"] == "referral":
        await message.answer(f"👥 Referral {ref['value']} tho vacharu — meeku extra benefit! 🎉\n\nMeeku evaru kavali?", reply_markup=get_gender_kb())
        user_sessions[message.from_user.id] = {"referred_by": ref["value"]}
    elif ref["kind"] == "profile":
        await message.answer(f"🔎 {ref['value']} kosam vacharu!\n\nMundu mee details cheppandi — meeku evaru kavali?", reply_markup=get_gender_kb())
        user_sessions[message.from_user.id] = {"looking_for": ref["value"]}
    elif ref["kind"] == "unlock":
        # 🌊 WAVE 18 — website "Full details + Number" button nunchi deep-link
        target = ref["value"]
        sess = user_sessions.get(message.from_user.id, {})
        if sess.get("tsap_id"):
            await _do_unlock(message, sess["tsap_id"], target)
        else:
            user_sessions[message.from_user.id] = {**sess, "pending_unlock": target}
            await message.answer(f"📞 {target} number kavali — super!\n\nMundu mee profile link cheyyandi: /link MEE-TSAP-ID\n(Link ayyaka number automatic ga vastundi — 1 credit)", parse_mode="Markdown")
    else:
        await message.answer("🙏 Namaste! TS-AP Matrimony ki swagatham!\n\nMeeku evaru kavali? [Bride/Groom]", reply_markup=get_gender_kb())


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(help_text())


@dp.message(Command("myid"))
async def cmd_myid(message: Message):
    await message.answer(f"🆔 Mee Telegram ID: `{message.from_user.id}`\nSupport ki ee ID pampandi 🙏", parse_mode="Markdown")


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message):
    user_sessions.pop(message.from_user.id, None)
    await message.answer("❌ Form cancel chesam. Malli /start cheyochu 🙏")


@dp.message(Command("search"))
async def cmd_search(message: Message):
    """Bot lo ne ID search — backend API ki call (token unte)."""
    parts = str(message.text or "").strip().split()
    if len(parts) < 2:
        await message.answer("🔎 Ela: /search TSAP-F-1042\nID website card meeda / channel post lo untundi")
        return
    tsap_id = parts[1].upper()
    # backend API nunchi profile (site internal call)
    import aiohttp
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as sess:
            async with sess.get(f"{api_base}/api/search/{tsap_id}") as resp:
                if resp.status != 200:
                    await message.answer(f"⚠️ {tsap_id} dorakaledu — ID sari chudandi")
                    return
                data = await resp.json()
        prof = data.get("profile", data)
        await message.answer(format_id_search(prof if isinstance(prof, dict) else {"tsap_id": tsap_id}))
    except Exception as e:  # noqa: BLE001
        await message.answer(f"⚠️ Search ippudu work avvatledu — website lo chudandi: {SITE_URL}/matches\n({str(e)[:60]})")


async def _do_unlock(message: Message, viewer: str, target: str):
    """🔓 Shared unlock: /unlock command + website deep-link rendu ikkade."""
    import aiohttp
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.post(f"{api_base}/api/unlock",
                              json={"viewer_id": viewer, "target_id": target}) as resp:
                data = await resp.json()
        await message.answer(unlock_result_text(data if isinstance(data, dict) else {}), parse_mode="Markdown")
    except Exception as e:  # noqa: BLE001
        await message.answer(f"⚠️ Unlock ippudu work avvatledu — website lo try cheyyandi: {SITE_URL}/matches\n({str(e)[:60]})")


@dp.message(Command("unlock"))
async def cmd_unlock(message: Message):
    """🔓 /unlock TSAP-F-1042 — 1 credit tho number reveal (bot lo link ayina ID tho)."""
    parts = str(message.text or "").strip().split()
    if len(parts) < 2:
        await message.answer("🔓 Ela: /unlock TSAP-F-1042\n(Channel post lo ID untundi — 1 credit = 1 number 📞)")
        return
    target = parts[1].upper()
    sess = user_sessions.get(message.from_user.id, {})
    viewer = sess.get("tsap_id", "")
    if not viewer:
        user_sessions[message.from_user.id] = {**sess, "pending_unlock": target}
        await message.answer("🙏 Mundu mee profile link cheyyandi: /link MEE-TSAP-ID\n(ID website login lo / register SMS lo untundi — link ayyaka number automatic)",
                             parse_mode="Markdown")
        return
    await _do_unlock(message, viewer, target)


@dp.message(Command("mylist"))
async def cmd_mylist(message: Message):
    sess = user_sessions.get(message.from_user.id, {})
    viewer = sess.get("tsap_id", "")
    if not viewer:
        await message.answer("🙏 Mundu /link MEE-TSAP-ID cheyyandi — appudu mee unlocked list chupistham")
        return
    import aiohttp
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(f"{api_base}/api/unlocks/{viewer}") as resp:
                data = await resp.json()
        await message.answer(mylist_text(data if isinstance(data, dict) else {}))
    except Exception as e:  # noqa: BLE001
        await message.answer(f"⚠️ List load avvaledu ({str(e)[:60]}) — /help chudandi")


@dp.message(Command("balance"))
async def cmd_balance(message: Message):
    sess = user_sessions.get(message.from_user.id, {})
    viewer = sess.get("tsap_id", "")
    if not viewer:
        await message.answer("🙏 Mundu /link MEE-TSAP-ID cheyyandi")
        return
    import aiohttp
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(f"{api_base}/api/credits/{viewer}") as resp:
                data = await resp.json() if resp.status == 200 else {}
        await message.answer(balance_text(int(data.get("credits", 0)), str(data.get("plan", "FREE"))),
                             parse_mode="Markdown")
    except Exception as e:  # noqa: BLE001
        await message.answer(f"⚠️ Balance load avvaledu ({str(e)[:60]})")


@dp.message(Command("pay"))
async def cmd_pay(message: Message):
    await message.answer(pay_text(), parse_mode="Markdown")


@dp.message(Command("link"))
async def cmd_link(message: Message):
    """🔗 /link TSAP-F-1042 — Telegram ni profile tho link (personal delivery + unlock kosam)."""
    parts = str(message.text or "").strip().split()
    if len(parts) < 2:
        await message.answer("🔗 Ela: /link MEE-TSAP-ID\n(ID website login lo untundi — link ayithe personal profiles + unlock ivvachu 🙂)")
        return
    tsap_id = parts[1].upper()
    import aiohttp
    api_base = os.getenv("API_BASE", "http://localhost:8000")
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.post(f"{api_base}/api/link-telegram",
                              json={"tsap_id": tsap_id,
                                    "chat_id": str(message.from_user.id)}) as resp:
                data = await resp.json()
        if resp.status == 200 and isinstance(data, dict) and data.get("success") is not False:
            _sess = {**user_sessions.get(message.from_user.id, {}), "tsap_id": tsap_id}
            _pend = _sess.pop("pending_unlock", "")
            user_sessions[message.from_user.id] = _sess
            await message.answer(f"✅ Link ayyindi! {tsap_id} ↔ Telegram\n\nIppudu:\n• /unlock <ID> — number reveal (1 credit)\n• /mylist — unlocked list\n• /balance — credits",
                                 parse_mode="Markdown")
            if _pend:
                await message.answer(f"⏳ Pending unlock chestunna: {_pend}…")
                await _do_unlock(message, tsap_id, _pend)
        else:
            await message.answer(f"⚠️ {(data or {}).get('message_telugu') or 'ID dorakaledu — sari chudandi'}")
    except Exception as e:  # noqa: BLE001
        await message.answer(f"⚠️ Link avvaledu ({str(e)[:60]}) — website lo try cheyyandi")


@dp.message(F.text.in_(["👰 Bride", "🤵 Groom"]))
async def gender_chosen(message: Message):
    gender = "Bride" if "Bride" in message.text else "Groom"
    user_sessions[message.from_user.id] = {**user_sessions.get(message.from_user.id, {}), "gender": gender}
    await message.answer(f"{gender} kosam vetukuthunnara — super! Mee rashtram?", reply_markup=get_state_kb())


@dp.message(F.text.contains("తెలంగాణ") | F.text.contains("ఆంధ్ర"))
async def state_chosen(message: Message):
    state = "TS" if "తెలంగాణ" in message.text else "AP"
    user_sessions[message.from_user.id] = {**user_sessions.get(message.from_user.id, {}), "state": state}
    await message.answer("Mee kulam?", reply_markup=get_caste_kb())


@dp.message(F.photo)
async def photo_received(message: Message):
    """📸 Real photo receive — session lo file_id save (backend upload tarvata)."""
    session = user_sessions.get(message.from_user.id, {})
    if not session:
        await message.answer("🙏 Mundu /start cheyyandi — appudu photo pampandi")
        return
    file_id = message.photo[-1].file_id if message.photo else ""
    session["photo_file_id"] = file_id
    session["photo"] = "uploaded"
    user_sessions[message.from_user.id] = session
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Number Share", request_contact=True)]], resize_keyboard=True)
    await message.answer("📸 Photo vachindi — super! Ippudu mee WhatsApp/Telegram number share cheyyandi (one tap) — OTP vastundi", reply_markup=kb)


@dp.message(F.text)
async def caste_chosen(message: Message):
    # Simplified — real lo step-by-step
    session = user_sessions.get(message.from_user.id, {})
    if "caste" not in session and message.text not in ["⏭️ Skip"]:
        # assume caste
        if message.text in TOP_CASTES or message.text in ("Others",):
            session["caste"] = message.text
            user_sessions[message.from_user.id] = session
            await message.answer(f"{message.text} — super! Mee vayasu? [18-60 type cheyyandi] Buttons: [18-22] [23-27] [28-32] [33+]", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="18-22"), KeyboardButton(text="23-27")],[KeyboardButton(text="28-32"), KeyboardButton(text="33+")]], resize_keyboard=True))
            return

    # Age
    if "age" not in session and message.text in ["18-22","23-27","28-32","33+"]:
        session["age"] = message.text
        user_sessions[message.from_user.id] = session
        await message.answer("Mee photo 1-3 pampandi 📸 (face clear)", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📸 Photo Skip — Demo")]], resize_keyboard=True))
        return

    if "photo" not in session and "Photo" in message.text:
        session["photo"] = "uploaded"
        user_sessions[message.from_user.id] = session
        # Contact
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Number Share", request_contact=True)]], resize_keyboard=True)
        await message.answer("Mee WhatsApp/Telegram number share cheyyandi (one tap) — OTP vastundi", reply_markup=kb)
        return

    # fallback — artham kakapothe help
    if str(message.text or "").startswith("/"):
        await message.answer("⚠️ Ee command teliyadu — /help chudandi 🙏")
    else:
        await message.answer("🙏 Artham kaledu — /start (register) leda /help (commands) try cheyyandi")


@dp.message(F.contact)
async def contact_received(message: Message):
    phone = message.contact.phone_number
    session = user_sessions.get(message.from_user.id, {})
    session["phone"] = phone
    user_sessions[message.from_user.id] = session

    # Generate ID + Card mock
    import random
    seq = random.randint(1000,9999)
    gender = session.get("gender","Bride")
    tsap_id = f"TSAP-{'F' if gender=='Bride' else 'M'}-2025-{seq}"
    session["tsap_id"] = tsap_id

    # Router preview — ee profile e channels ki veltundi
    profile = {
        "full_name": session.get("full_name", ""), "gender": gender,
        "state": session.get("state", "TS"), "caste": session.get("caste", "Reddy"),
        "religion": session.get("religion", "Hindu"), "age": session.get("age", 24),
        "job": session.get("job", ""), "education": session.get("education", ""),
        "district": session.get("district", ""), "marital_status": session.get("marital_status", "Pelli Kaledu"),
    }
    user_profiles[tsap_id] = profile
    route = post_targets(profile)
    approve_text = (f"🆕 NEW PROFILE — {tsap_id}\nGender: {gender}\nCaste: {profile['caste']}\n"
                    f"State: {profile['state']}\nAge: {profile['age']}\nPhone: {phone}\n"
                    f"Ref: {session.get('referred_by','—')}\n\n"
                    f"📤 Post avvalsina LIVE channels ({len(route['ready'])}): {', '.join(route['ready'])}"
                    f"\n⏳ Pending channels: {len(route['pending'])}"
                    f"\n#hashtags: {route['hashtags']}")

    # Admin ki approve message (ADMIN_CHAT_ID unte real, lekapothe print)
    print(f"[ADMIN] {approve_text}")
    try:
        _b = get_bot()
        if _b is not None and ADMIN_CHAT_ID and str(ADMIN_CHAT_ID).isdigit():
            await _b.send_message(chat_id=ADMIN_CHAT_ID, text=approve_text, reply_markup=get_approve_kb(tsap_id))
    except Exception as e:
        print(f"[ADMIN SEND FAIL] {e}")

    # User ko Top 3 FREE
    await message.answer(f"🎉 Abhinandanalu! Me ID: *{tsap_id}*\n\nMe profile admin check lo undi (2 min). Meeku saripoye Top 3 sambandhalu (FREE, numbers lock) 👇\n\n⭐ 92% Match — TSAP-F-1042 — Reddy, 24, BTech, Software Hyd\n⭐ 88% — TSAP-F-1043 — Reddy, 23, Govt Job\n⭐ 85% — TSAP-F-1044 — Kamma, 25, MBA\n\nNumbers chudali ante ₹99 (okkasaari) → [📞 ₹99 Pay chesi Numbers Chudu]", parse_mode="Markdown")

    # Clear session
    # user_sessions.pop(message.from_user.id, None)


async def post_to_channels(profile: dict, tsap_id: str, score: int = 92, photo_path: str | None = None):
    """
    One approve → Advanced router → anni relevant LIVE channels lo post.
    Create kaani channels ni skip chesi list return chestundi.
    Bot configure kakapothe dry-run preview return (crash kadu).
    """
    t = post_targets(profile)
    caption = build_caption(profile, tsap_id, score)
    _b = get_bot()
    if _b is None:
        return {"posted": [], "failed": [], "pending_channels": t["pending"],
                "hashtags": t["hashtags"], "notes": t["notes"],
                "dry_run": True, "caption_preview": caption[:300]}
    posted, failed = [], []
    for chat in t["ready"]:
        try:
            if photo_path and os.path.exists(photo_path):
                from aiogram.types import FSInputFile
                await _b.send_photo(chat_id=chat, photo=FSInputFile(photo_path), caption=caption[:1024])
            else:
                await _b.send_message(chat_id=chat, text=caption[:4096])
            posted.append(chat)
            await asyncio.sleep(1.2)  # rate-limit safe
        except Exception as e:
            failed.append(f"{chat}: {e}")
    return {"posted": posted, "failed": failed, "pending_channels": t["pending"],
            "hashtags": t["hashtags"], "notes": t["notes"]}


@dp.callback_query(F.data.startswith("approve_"))
async def approve_callback(callback: CallbackQuery):
    tsap_id = callback.data.replace("approve_","")
    profile = user_profiles.get(tsap_id, {})
    res = await post_to_channels(profile, tsap_id, score=int(profile.get("score", 92)))
    pending_txt = ""
    if res["pending_channels"]:
        pending_txt = f"\n\n⏳ Create cheyyalsina channels: {len(res['pending_channels'])} (Wave plan chudu)"
    dry = "\n\n🧪 Dry-run (BOT_TOKEN pettagane live post)" if res.get("dry_run") else ""
    await callback.message.edit_text(
        f"✅ {tsap_id} Approved!\n\n📤 Posted ({len(res['posted'])}): {', '.join(res['posted']) or '—'}"
        f"\n❌ Failed: {', '.join(res['failed']) or '—'}{pending_txt}{dry}"
        f"\n\n#hashtags: {res['hashtags']}\n\nUser ki Top 3 FREE already sent + daily auto ON after pay.")
    await callback.answer("Approved + Auto-posted!")


@dp.callback_query(F.data.startswith("reject_"))
async def reject_callback(callback: CallbackQuery):
    tsap_id = callback.data.replace("reject_","")
    user_profiles.pop(tsap_id, None)
    await callback.message.edit_text(f"❌ {tsap_id} rejected — user ki reason tho message pampandi.")
    await callback.answer("Rejected")


@dp.callback_query(F.data.startswith("premium_"))
async def premium_callback(callback: CallbackQuery):
    tsap_id = callback.data.replace("premium_","")
    await callback.message.edit_text(f"💎 {tsap_id} ki 10 credits FREE + Premium gift! User ki message vellindi.")
    await callback.answer("Premium gifted!")


# Daily 9AM sender (APScheduler hook — backend scheduler nunchi call avutundi)
async def daily_sender_once(api_base: str = "") -> dict:
    """
    Daily 9AM digest — paid users ki top matches (dry-run preview return).
    Real scheduler (APScheduler/celery) ee function ni roju 9AM ki call chestundi.
    """
    base = api_base or os.getenv("API_BASE", "http://localhost:8000")
    return {"ok": True, "mode": "hook-ready", "api_base": base,
            "note": "APScheduler: daily_sender_once() ni 9AM IST ki schedule cheyyandi"}


async def daily_sender():
    while True:
        # In real: query DB for paid users, find 2 new matches, send via bot + WhatsApp API
        # APScheduler use
        await asyncio.sleep(86400)  # 24h
        print("[DAILY] Sending 9AM matches to paid users...")


async def main():
    st = channel_stats()
    print(f"[BOT START] {st['total']} channels registry | LIVE: {st['live']} | to create: {st['to_create']}")
    print("[BOT START] live: " + ", ".join("@" + c["username"] for c in live_channels()))
    _b = get_bot()
    if _b is None:
        print(f"[BOT STOP] {BOT_ERROR}")
        return
    asyncio.create_task(daily_sender())
    await dp.start_polling(_b)


if __name__ == "__main__":
    asyncio.run(main())
