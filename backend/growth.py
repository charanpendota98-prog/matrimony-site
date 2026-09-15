"""
MANA VIVAHA — GROWTH ENGINE
===========================
1) 🙏 NAMASTE WELCOME AUTOMATION — register avvagane MANA WhatsApp nunchi:
   • user ki: "Namaste <name> garu! 🙏" + profile card + full details + next steps
   • admin/matcher ki: kotha registration alert (follow-up cheyyadaniki)
2) 📊 VISITOR + LEAD CAPTURE — "site ki vachina vallu, chusina vallu antha DB lo save avvali"
   • prathi visit (path, referrer, utm, device, city guess) DB_VISITORS lo
   • number isthe → DB_LEADS (hot lead) + WhatsApp follow-up queue
   • profile views DB_VIEWS lo (already main.py lo) — ikkada who-viewed summary
3) 🎴 SHARE KIT — "oka profile chala mandi chudalanukune la" — status-ready image + text + hashtags

Chatting ledu — interest request + WhatsApp profile share model ki todu.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib
import os
import random

SITE = os.getenv("PUBLIC_SITE_URL", "https://manavivaha.in").rstrip("/")
BOT_USERNAME = os.getenv("BOT_USERNAME", "@telugumatrimony1_bot")
SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "9100000000")

DB_VISITORS: List[Dict] = []   # {vid, at, path, ref, utm, device, ua}
DB_LEADS: List[Dict] = []      # {id, at, name, phone, gender, age, district, caste, source, status, notes}


# ---------------------------------------------------------------------------
# 1) 🙏 NAMASTE WELCOME + ADMIN ALERT
# ---------------------------------------------------------------------------
def namaste_text(user: Dict, tsap_id: str) -> str:
    """
    Register ayina ventane user ki velle NAMASTE message —
    card + full details + next steps (chatting ledu ani clear ga).
    """
    u = user or {}
    return (
        f"🙏 *నమస్తే {u.get('full_name', 'గారు')} గారు!* 🙏\n"
        f"*Mana Vivaha* kutumbam lo meeku swagatham 💐\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"✅ Mee profile ready: *{tsap_id}*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 {u.get('full_name', '—')} ({u.get('age', '—')} yrs)\n"
        f"💍 {u.get('caste', '—')}{(' / ' + u['sub_caste']) if u.get('sub_caste') else ''} | Gothram: {u.get('gothram', '—')}\n"
        f"🌟 Star: {u.get('star', '—')} | Rasi: {u.get('rasi', '—')}\n"
        f"📏 Height: {u.get('height', '—')} | 🩸 {u.get('blood_group', '—') or '—'}\n"
        f"🎓 {u.get('education', '—')} {u.get('education_detail', '')}\n"
        f"💼 {u.get('job', '—')} {u.get('company', '')} | 💰 {u.get('salary', '—')}\n"
        f"📍 {u.get('district', '—')}, {u.get('state', 'TS')}\n"
        f"👨‍👩‍👧 {u.get('family_type', '—')} • {u.get('family_status', '—')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📢 Mee profile ippude mana *65 channels* + WhatsApp groups lo post avutundi "
        f"(anti-ban rules tho — konni nimushalalo live).\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"*Ippudu em cheyyali?*\n"
        f"1️⃣ Mee profile card kindha pampisthunnam — WhatsApp status lo pettandi (reach double!)\n"
        f"2️⃣ Matches chusi 💌 *Interest request* pampandi — modati 3 FREE\n"
        f"3️⃣ Mee ID share cheyyandi: {tsap_id}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🔒 Mee number evariki kanipinchadu. Interest accept ayyaka matrame exchange avutundi.\n"
        f"🚫 Chatting ledu — spam/loose talk undadu.\n"
        f"🤖 Bot: {BOT_USERNAME} | 🔍 Mee profile: {SITE}/search/{tsap_id}\n"
        f"⚠️ Advance money adigithe ventane report cheyyandi: {SUPPORT_PHONE}"
    )


def admin_new_profile_text(user: Dict, tsap_id: str, source: str = "website") -> str:
    """Admin/matcher ki kotha registration alert — 2 nimushalalo verify + follow-up cheyyadaniki."""
    u = user or {}
    return (
        f"🆕 *NEW REGISTRATION* ({source})\n"
        f"🆔 {tsap_id} — {u.get('gender', '—')}\n"
        f"👤 {u.get('full_name', '—')} • {u.get('age', '—')}y • {u.get('caste', '—')}\n"
        f"📍 {u.get('district', '—')}, {u.get('state', 'TS')} • 🎓 {u.get('education', '—')} • 💼 {u.get('job', '—')}\n"
        f"📞 {u.get('phone', '—')} {'✅ verified' if u.get('phone_verified') else '⚠️ verify pending'}\n"
        f"📸 photo: {'undi' if u.get('photo_urls') else 'ledu — adagandi'}\n"
        f"🎴 Card: {SITE}/cards/{tsap_id}.png\n"
        f"👉 Follow-up: welcome call + photo adagandi + channels confirm"
    )


def lead_followup_text(lead: Dict) -> str:
    """Number ichi aagipoyina lead ki polite follow-up (mana WhatsApp nunchi)."""
    l = lead or {}
    return (
        f"🙏 Namaste {l.get('name', 'గారు')} గారు!\n"
        f"Mana Vivaha nunchi matladutunnam 💐\n"
        f"Meeru {l.get('district', 'mee oorlo')} nunchi — {l.get('gender', '')} profile ki interest chupincharu.\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"Mee profile *FREE* ga complete cheyyadaniki 3 nimushalu chalu:\n"
        f"1️⃣ Peru + photo (optional)\n2️⃣ Caste + star details\n3️⃣ Education + job\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🔗 Ikkada complete cheyyandi: {SITE}/register?phone={l.get('phone', '')}\n"
        f"లేదా ee number ki 'YES' ani reply cheyyandi — mana team call chesi 5 nimushalalo profile ready chestundi.\n"
        f"🔒 Mee number safe — evariki share avvadu.🚫 Chatting ledu.\n"
        f"❓ Help: {SUPPORT_PHONE}"
    )


# ---------------------------------------------------------------------------
# 2) 📊 VISITOR + LEAD CAPTURE
# ---------------------------------------------------------------------------
def _vid(ip: str, ua: str) -> str:
    """Anonymous visitor id (IP+UA hash — cookie ledu, GDPR-friendly)."""
    return "V" + hashlib.sha256((str(ip) + "|" + str(ua)[:120]).encode()).hexdigest()[:14]


def track_visit(ip: str, ua: str, path: str, ref: str = "", utm: str = "",
                device: str = "", extra: Optional[Dict] = None) -> Dict:
    """Prathi visit DB_VISITORS lo — 'chusina vallu antha save' requirement."""
    d = "mobile" if device == "mobile" else ("desktop" if device == "desktop" else ("mobile" if _is_mobile(ua) else "desktop"))
    rec = {
        "vid": _vid(ip, ua), "at": datetime.utcnow().isoformat(), "path": path[:160],
        "ref": (ref or "")[:160], "utm": (utm or "")[:160], "device": d,
        "channel": _channel_of(ref, utm),
    }
    if extra:
        rec.update({k: str(v)[:120] for k, v in extra.items()})
    DB_VISITORS.append(rec)
    return rec


def _is_mobile(ua: str) -> bool:
    ua = (ua or "").lower()
    return any(k in ua for k in ("android", "iphone", "ipad", "mobile", "oppo", "vivo", "redmi", "samsung"))


def _channel_of(ref: str, utm: str) -> str:
    s = (str(ref) + " " + str(utm)).lower()
    if "whatsapp" in s or "wa.me" in s:
        return "whatsapp"
    if "t.me" in s or "telegram" in s:
        return "telegram"
    if "google" in s:
        return "google"
    if "facebook" in s or "fb." in s:
        return "facebook"
    if "instagram" in s:
        return "instagram"
    if "youtube" in s:
        return "youtube"
    if "share" in s:
        return "share_link"
    return "direct"


def save_lead(name: str, phone: str, gender: str = "", district: str = "", caste: str = "",
              age: str = "", source: str = "website", notes: str = "") -> Tuple[bool, str, Dict]:
    """
    Half-filled visitor ni lead ga save chey (hot lead — mana team follow-up chestundi).
    Same phone malli isthe duplicate update avutundi (fresh ga untundi).
    """
    phone = "".join(ch for ch in str(phone) if ch.isdigit())[-10:]
    if len(phone) != 10:
        return False, "10 digit mobile number ivvandi", {}
    existing = next((l for l in DB_LEADS if l["phone"] == phone), None)
    if existing:
        existing.update({"name": name or existing.get("name", ""), "gender": gender or existing.get("gender", ""),
                         "district": district or existing.get("district", ""), "caste": caste or existing.get("caste", ""),
                         "age": str(age) if age else existing.get("age", ""),
                         "source": source or existing.get("source", ""),
                         "notes": notes or existing.get("notes", ""),
                         "updated_at": datetime.utcnow().isoformat(), "touches": int(existing.get("touches", 1)) + 1})
        return True, "already_lead", existing
    lead = {
        "id": "LEAD-" + datetime.utcnow().strftime("%y%m%d") + "-" + str(len(DB_LEADS) + 1).zfill(4),
        "at": datetime.utcnow().isoformat(), "name": name, "phone": phone, "gender": gender,
        "district": district, "caste": caste, "age": str(age), "source": source, "notes": notes,
        "status": "new", "touches": 1,
        "followup": "WhatsApp follow-up queued (mana side nunchi)",
    }
    DB_LEADS.append(lead)
    return True, "new_lead", lead


def lead_stats() -> Dict:
    by_source: Dict[str, int] = {}
    by_day: Dict[str, int] = {}
    by_channel: Dict[str, int] = {}
    by_path: Dict[str, int] = {}
    for v in DB_VISITORS:
        by_source[v.get("source", "website") if v.get("source") else "website"] = by_source.get(
            v.get("source", "website") if v.get("source") else "website", 0) + 1
        by_day[v["at"][:10]] = by_day.get(v["at"][:10], 0) + 1
        by_channel[v.get("channel", "direct")] = by_channel.get(v.get("channel", "direct"), 0) + 1
        by_path[v.get("path", "/")] = by_path.get(v.get("path", "/"), 0) + 1
    top_paths = sorted(by_path.items(), key=lambda x: -x[1])[:10]
    new_leads = [l for l in DB_LEADS if l.get("status") == "new"]
    return {
        "visits_total": len(DB_VISITORS),
        "visitors_unique": len({v["vid"] for v in DB_VISITORS}),
        "visits_today": len([v for v in DB_VISITORS if v["at"][:10] == datetime.utcnow().strftime("%Y-%m-%d")]),
        "by_channel": by_channel, "by_day": by_day,
        "top_paths": [{"path": p, "visits": n} for p, n in top_paths],
        "leads_total": len(DB_LEADS), "leads_new": len(new_leads),
        "leads_by_source": _count_by(DB_LEADS, "source"), "leads_by_district": _count_by(DB_LEADS, "district"),
        "conversion": (round(len(DB_LEADS) / max(1, len({v['vid'] for v in DB_VISITORS})) * 100, 1)),
        "message_telugu": "%d visits (%d unique) • %d leads • %s" % (
            len(DB_VISITORS), len({v["vid"] for v in DB_VISITORS}), len(DB_LEADS),
            "ee roju kotha leads: %d" % len([l for l in DB_LEADS if l["at"][:10] == datetime.utcnow().strftime("%Y-%m-%d")])),
    }


def _count_by(rows: List[Dict], key: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in rows:
        k = r.get(key) or "—"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda x: -x[1])[:12])


def leads_list(status: str = "", limit: int = 100) -> Dict:
    rows = DB_LEADS if not status else [l for l in DB_LEADS if l.get("status") == status]
    hot = sorted(rows, key=lambda x: (-int(x.get("touches", 1)), x["at"]), reverse=False)[:limit]
    return {"total": len(rows), "items": hot,
            "message_telugu": "Kotha leads mundu follow-up cheyyandi — first 24 hours lo response rate 3x ekkuva"}


# ---------------------------------------------------------------------------
# 3) 🎴 SHARE KIT (profile reach penchadaniki)
# ---------------------------------------------------------------------------
def share_kit(user: Dict, tsap_id: str, hashtags: Optional[List[str]] = None) -> Dict:
    """
    WhatsApp status / groups ki ready kit: card image + Telugu text + hashtags + TG/WA share links.
    'Oka profile chala mandi chudalanukune la' — idi aa reach engine.
    """
    u = user or {}
    name = u.get("full_name", "Profile")
    tags = hashtags or ["#ManaVivaha", "#TeluguMatrimony", "#" + str(u.get("caste", "Telugu")).replace(" ", ""),
                        "#" + str(u.get("district", "TS")).replace(" ", ""), "#PelliChoopulu"]
    caption = (
        f"💍 *{name}* — {u.get('age', '—')} yrs | {u.get('caste', '—')} | {u.get('district', '—')}, {u.get('state', 'TS')}\n"
        f"🎓 {u.get('education', '—')} {u.get('job', '')} | 💰 {u.get('salary', '—')}\n"
        f"🌟 {u.get('star', '—')} / {u.get('rasi', '—')} | 🕉️ {u.get('gothram', '—')}\n"
        f"🆔 *{tsap_id}*\n"
        f"🔍 Details: {SITE}/search/{tsap_id}\n"
        f"📝 Mee profile FREE ga pettu: {SITE}/register\n"
        f"{' '.join(tags)}"
    )
    return {
        "tsap_id": tsap_id,
        "card_image": f"{SITE}/cards/{tsap_id}.png",
        "caption": caption,
        "caption_short": f"💍 {name} | {u.get('age', '—')}y | {u.get('caste', '—')} | {u.get('district', '—')}\n🆔 {tsap_id} | {SITE}/search/{tsap_id}",
        "hashtags": tags,
        "whatsapp_share": "https://wa.me/?text=" + _url(caption),
        "telegram_share": "https://t.me/share/url?url=" + _url(f"{SITE}/search/{tsap_id}") + "&text=" + _url(caption),
        "best_time_to_post": "Ratri 8–10 IST (WhatsApp status views ekkuva)",
        "tips_telugu": [
            "Card image ni WhatsApp status lo 24h pettandi — local reach 3x avutundi",
            "Family WhatsApp groups lo caption + link pampandi",
            "Caste + district group admin ki direct ga pampandi (mana channels cover chestayi)",
        ],
    }


def _url(s: str) -> str:
    from urllib.parse import quote
    return quote(s, safe="")


# ---------------------------------------------------------------------------
# 4) 🚀 LAUNCH INVENTORY HELPER (300–400 profiles chalu — annav)
# ---------------------------------------------------------------------------
def inventory_status(total_users: int) -> Dict:
    """
    'Chala mandi undalsina avasaram ledu — 300–400 profiles chalu' → ee gauge.
    """
    target = int(os.getenv("LAUNCH_TARGET_PROFILES", "360"))
    pct = round(total_users / max(1, target) * 100, 1)
    return {
        "total_profiles": total_users, "launch_target": target, "percent": pct,
        "ready": total_users >= target,
        "message_telugu": ("✅ Launch inventory ready (%d/%d profiles) — channels khali ga kanipinchavu"
                           % (total_users, target)) if total_users >= target else
                          ("⚠️ Inka %d profiles kavali launch ki (%d/%d). Growth engine leads ni profiles ga marchutundi."
                           % (target - total_users, total_users, target)),
        "how_to_fill": ["POST /api/demo/seed-launch (demo inventory)",
                        "Community heads nunchi bulk upload",
                        "Lead follow-up → profile completion (conversion 40%+)",
                        "Referral link (prathi user 3 profiles techukostadu)"],
    }


def expire_old_requests(requests: List[Dict], days: int = 7) -> int:
    """7 days lo reply lekapothe request expire (credits user ke migilipothayi ani notify)."""
    now = datetime.utcnow()
    n = 0
    for r in requests:
        if r.get("status") != "pending":
            continue
        try:
            created = datetime.fromisoformat(r.get("at") or r.get("created_at"))
        except Exception:
            continue
        if now - created > timedelta(days=days):
            r["status"] = "expired"
            r["expired_at"] = now.isoformat()
            n += 1
    return n
