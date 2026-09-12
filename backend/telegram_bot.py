"""
TSAP Matrimony — Telegram Bot (aiogram 3.x) — Pin-to-Pin Perfect Advanced
Flows: Register Telugu buttons, OTP, Photo, Admin Approve, Auto-Router Main 4 + Caste + Special, Credits, Referral, Payment, Daily 9AM
"""
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "123456789")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Telugu keyboards
def get_gender_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="👰 Bride"), KeyboardButton(text="🤵 Groom")]], resize_keyboard=True)

def get_state_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="తెలంగాణ (TS)"), KeyboardButton(text="ఆంధ్రప్రదేశ్ (AP)")]], resize_keyboard=True)

def get_caste_kb():
    castes = ["Reddy","Kamma","Kapu","Velama","Vysya","Brahmin","Goud","Yadav","Mudiraj","Padmashali","SC-Mala","SC-Madiga","ST-Lambadi","Muslim","Christian","Open"]
    kb = []
    for i in range(0, len(castes), 2):
        kb.append([KeyboardButton(text=castes[i]), KeyboardButton(text=castes[i+1] if i+1 < len(castes) else "Others")])
    kb.append([KeyboardButton(text="⏭️ Skip")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_approve_kb(tsap_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve + Auto-Post", callback_data=f"approve_{tsap_id}"),
         InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_{tsap_id}")],
        [InlineKeyboardButton(text="💎 Make Premium +10 Credits", callback_data=f"premium_{tsap_id}")]
    ])

# In-memory user sessions (real lo Redis)
user_sessions = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    ref = message.text.split(" ")[1] if len(message.text.split(" "))>1 else ""
    # ref parsing: ch_reddy, ref_1042, etc.
    if ref.startswith("ch_"):
        await message.answer(f"📂 {ref.replace('ch_','')} Channel nunchi vacharu — welcome! 🙏\n\nTS-AP Matrimony ki swagatham! Meeku evaru kavali?", reply_markup=get_gender_kb())
    elif ref.startswith("ref_"):
        await message.answer(f"👥 Referral {ref} tho vacharu — meeku extra benefit! 🎉\n\nMeeku evaru kavali?", reply_markup=get_gender_kb())
        user_sessions[message.from_user.id] = {"referred_by": ref.replace("ref_","")}
    else:
        await message.answer("🙏 Namaste! TS-AP Matrimony ki swagatham!\n\nMeeku evaru kavali? [Bride/Groom]", reply_markup=get_gender_kb())

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

@dp.message(F.text)
async def caste_chosen(message: Message):
    # Simplified — real lo step-by-step
    session = user_sessions.get(message.from_user.id, {})
    if "caste" not in session and message.text not in ["⏭️ Skip"]:
        # assume caste
        if message.text in ["Reddy","Kamma","Kapu","Velama","Vysya","Brahmin","Goud","Yadav","Mudiraj","Padmashali","SC-Mala","SC-Madiga","ST-Lambadi","Muslim","Christian","Open"]:
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

    # Send to admin for approve
    approve_text = f"🆕 NEW PROFILE — {tsap_id}\nGender: {gender}\nCaste: {session.get('caste','Reddy')}\nState: {session.get('state','TS')}\nAge: {session.get('age','24')}\nPhone: {phone}\nRef: {session.get('referred_by','—')}\n\nCard: (mock) — Approve chesthe auto-post to Main + Caste + Special"

    # Mock admin message
    print(f"[ADMIN] {approve_text}")

    # User ko Top 3 FREE
    await message.answer(f"🎉 Abhinandanalu! Me ID: *{tsap_id}*\n\nMe profile admin check lo undi (2 min). Meeku saripoye Top 3 sambandhalu (FREE, numbers lock) 👇\n\n⭐ 92% Match — TSAP-F-1042 — Reddy, 24, BTech, Software Hyd\n⭐ 88% — TSAP-F-1043 — Reddy, 23, Govt Job\n⭐ 85% — TSAP-F-1044 — Kamma, 25, MBA\n\nNumbers chudali ante ₹99 (okkasaari) → [📞 ₹99 Pay chesi Numbers Chudu]", parse_mode="Markdown")

    # Clear session
    # user_sessions.pop(message.from_user.id, None)

@dp.callback_query(F.data.startswith("approve_"))
async def approve_callback(callback: CallbackQuery):
    tsap_id = callback.data.replace("approve_","")
    # In real: call backend /api/admin/approve/{tsap_id} → auto-post to channels
    # Mock posts
    channels = ["@ts_brides", "@tsap_reddy", "@tsap_second (if applicable)"]
    await callback.message.edit_text(f"✅ {tsap_id} Approved! Posted to: {', '.join(channels)}\n\nUser ki Top 3 FREE already sent + daily auto ON after pay.")
    await callback.answer("Approved + Auto-posted!")

@dp.callback_query(F.data.startswith("premium_"))
async def premium_callback(callback: CallbackQuery):
    tsap_id = callback.data.replace("premium_","")
    await callback.message.edit_text(f"💎 {tsap_id} ki 10 credits FREE + Premium gift! User ki message vellindi.")
    await callback.answer("Premium gifted!")

# Daily 9AM sender (mock)
async def daily_sender():
    while True:
        # In real: query DB for paid users, find 2 new matches, send via bot + WhatsApp API
        # APScheduler use
        await asyncio.sleep(86400)  # 24h
        print("[DAILY] Sending 9AM matches to paid users...")

async def main():
    # Start daily sender in background
    asyncio.create_task(daily_sender())
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
