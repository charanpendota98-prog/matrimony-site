"""
🎁 WELCOME PACK — "register avvagane 3 profiles + caste channel links WhatsApp కి"
===============================================================================
User adigindi (Telugu):
  "registration avvagane elaga vadi whatsapp ki 3 profiles vellai, mana channel links
   vadi caste channels — telegram and whatsapp channels — vadi caste related"

Ee module lo:
  • top-3 matches ni user ki WhatsApp message ga marchadam (numbers 🔒 — links matrame)
  • caste / region / religion / official channel links (Telegram + WhatsApp) build cheyyadam
  • okate function: build_welcome_pack(user, tsap_id, matches) → dict (API + queue rendu vaadutayi)

RULES (user privacy policy — marchakoodadu):
  🔒 Phone numbers eppudu message lo pettamu (98••••••45 mask matrame)
  🔗 Profile link (manavivaha.in/search/TSAP-...) + channel links matrame
  🚫 Max 3 profiles (FREE policy), 5 channel links (spam taggadaniki)
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from channels_config import SITE, caste_channel_links, channel_links, CHANNELS


# --------------------------------------------------------------------------- #
# 1. PROFILE LINE (safe — phone/email lekunda)
# --------------------------------------------------------------------------- #
def safe_profile_summary(p: Dict[str, Any]) -> Dict[str, Any]:
    """Match profile నుంచి WhatsApp/website కి pani చేసే safe fields మాత్రమే."""
    p = p or {}
    tsap_id = str(p.get("tsap_id", ""))
    return {
        "tsap_id": tsap_id,
        "name": str(p.get("full_name", "") or "—"),
        "age": p.get("age", ""),
        "gender": p.get("gender", ""),
        "height": p.get("height", ""),
        "caste": p.get("caste", ""),
        "sub_caste": p.get("sub_caste", ""),
        "education": p.get("education", ""),
        "job": str(p.get("job", "") or ""),
        "company": str(p.get("company", "") or ""),
        "salary": str(p.get("salary", "") or ""),
        "district": p.get("district", ""),
        "state": p.get("state", ""),
        "star": p.get("star", ""),
        "rasi": p.get("rasi", ""),
        "verified": bool(p.get("is_verified")),
        "photo_private": bool(p.get("photo_private") or p.get("privacy_mode") == "private"),
        "phone_masked": str(p.get("phone_masked", "") or ""),
        "link": f"{SITE}/search/{tsap_id}" if tsap_id else SITE,
    }


def profile_line(idx: int, prof: Dict[str, Any], score: int = 0, reason: str = "") -> str:
    """WhatsApp లో ఒక్క profile line (Telugu, emoji, numbers లేదు)."""
    emoji = ["1️⃣", "2️⃣", "3️⃣"][idx] if idx < 3 else "•"
    bits = [f"{emoji} *{prof.get('name', '—')}* — {prof.get('age', '—')} yrs"]
    fam = ", ".join([x for x in [str(prof.get("caste", "")), str(prof.get("district", ""))] if x])
    if fam:
        bits.append(fam)
    work = " • ".join([x for x in [str(prof.get("education", "")), str(prof.get("job", ""))] if x])
    if work:
        bits.append(work)
    line = f"{bits[0]}\n     {(' | '.join(bits[1:]))}" if len(bits) > 1 else bits[0]
    extra = []
    if score:
        extra.append(f"⭐ {score}% match")
    if prof.get("verified"):
        extra.append("✅ verified")
    if prof.get("star"):
        extra.append(f"🌟 {prof['star']}")
    if extra:
        line += f"\n     {' • '.join(extra)}"
    if reason:
        line += f"\n     💡 {reason}"
    line += f"\n     🔗 {prof.get('link', SITE)}  (ID: {prof.get('tsap_id', '—')})"
    return line


# --------------------------------------------------------------------------- #
# 2. CHANNEL LINKS BLOCK (caste channels — telegram + whatsapp)
# --------------------------------------------------------------------------- #
def channel_line(link: Dict[str, Any], why: str = "") -> str:
    name = link.get("name", link.get("key", ""))
    tg = link.get("telegram", "")
    wa = link.get("whatsapp", "")
    out = f"• *{name}*"
    if why:
        out += f" — {why}"
    row = []
    if tg:
        row.append(f"✈️ Telegram: {tg}")
    if wa:
        row.append(f"🟢 WhatsApp: {wa}")
    if row:
        out += "\n     " + " | ".join(row)
    else:
        out += "\n     (link soon — support ki adagandi)"
    return out


def channels_text(links: List[Dict[str, Any]], why_map: Optional[Dict[str, str]] = None) -> str:
    why_map = why_map or {}
    if not links:
        return ""
    lines = [channel_line(l, why_map.get(l.get("key", ""), "")) for l in links]
    return "📢 *మీ caste channels — daily matches ఇక్కడ* 👇\n" + "\n".join(lines)


def support_note() -> str:
    """WhatsApp channel link configure అవ్వకపోతే — support కి ఎలా అడగాలి (Telugu)."""
    wa = os.getenv("SUPPORT_WHATSAPP_NUMBER", os.getenv("ADMIN_WHATSAPP_NUMBER", "")).strip()
    if wa:
        return f"📱 WhatsApp channel links కూడా pampistham — support కి 'CHANNEL' అని ping చెయ్యండి: https://wa.me/{wa}"
    return "📱 WhatsApp channel links configure avutunnayi — Telegram links ippude join అవ్వండి (daily matches)."


# --------------------------------------------------------------------------- #
# 3. MASTER BUILDER
# --------------------------------------------------------------------------- #
def build_welcome_pack(user: Dict[str, Any], tsap_id: str, matches: List[Dict[str, Any]],
                       max_profiles: int = 3, max_channels: int = 5) -> Dict[str, Any]:
    """
    🎁 Full welcome pack:
      profiles  : top-3 matches (safe summary — phone mask matrame)
      channels  : caste → region → (religion) → official (telegram + whatsapp links)
      message   : WhatsApp lo velle Telugu message (numbers ledu)
    """
    user = user or {}
    profs: List[Dict[str, Any]] = []
    for m in (matches or [])[:max_profiles]:
        row = dict(m or {})
        cand = row.get("profile") or row.get("user") or row
        s = safe_profile_summary(cand)
        s["score"] = int(row.get("score", 0) or 0)
        reasons = row.get("reasons") or []
        s["reason"] = str(reasons[0]) if reasons else ""
        profs.append(s)

    chans = caste_channel_links(user, limit=max_channels)
    why = {}
    try:
        from channels_config import route_profile
        why = {r.get("key"): r.get("telugu", "") for r in (route_profile(user, max_posts=6).get("reasons") or [])}
    except Exception:
        why = {}

    _n = len(profs)
    _n_te = {0: "మీ matches ready", 1: "మీ 1 FREE match ready", 2: "మీ 2 FREE matches ready"}.get(_n, "మీ 3 FREE matches ready")
    head = (
        f"🎉 *{user.get('full_name', 'గారు')} గారు — {_n_te}!* 🎉\n"
        f"🆔 *{tsap_id}* | 💍 {user.get('caste', '—')}"
        f"{(' / ' + str(user['sub_caste'])) if user.get('sub_caste') else ''}"
        f" | 📍 {user.get('district', '—')}, {user.get('state', 'TS')}\n"
        f"━━━━━━━━━━━━━━━━"
    )
    body_parts = [head]
    if profs:
        body_parts.append(f"🔎 *మీ {_n} profile{'s' if _n != 1 else ''}* (numbers 🔒 — interest accept = consent తో మాత్రమే exchange):\n" +
                          "\n".join(profile_line(i, p, p.get("score", 0), p.get("reason", ""))
                                    for i, p in enumerate(profs)))
    else:
        body_parts.append("🔎 మీ matches ఇంకా prepare avutunnai — konchem sepatlo WhatsApp లో vastayi.")
    body_parts.append("✅ Interest pampali అంటే: మీ TSAP ID + వాళ్ల ID తో ee link open చెయ్యండి — " +
                      "1 credit (మొదటి 3 FREE), decline అయితే credit refund.")
    if chans:
        body_parts.append(channels_text(chans, why))
    body_parts.append(support_note())
    message = "\n\n".join([p for p in body_parts if p])

    return {
        "tsap_id": tsap_id,
        "profiles": profs,
        "channels": chans,
        "message_text": message,
        "message_preview": message[:2600],   # channels block kooda preview lo kanipinchali
        "rules_telugu": [
            "🔒 Numbers ఎప్పుడు public గా ఇవ్వము — interest accept (consent) తో మాత్రమే exchange",
            "🆓 మొదటి 3 profiles + 3 requests FREE",
            "💰 ₹99 → 5 profiles + boost (మొదటి 3 FREE taruvata)",
            "📢 మీ caste Telegram + WhatsApp channels లో daily matches — join అవ్వండి",
        ],
        "has_numbers": False,
    }


def pack_public(pack: Dict[str, Any]) -> Dict[str, Any]:
    """API response కి — message text + profiles + channels (sensitive లేదు, number masked)."""
    if not pack:
        return {}
    return {k: v for k, v in pack.items() if k != "has_numbers"}


def channels_count() -> Dict[str, int]:
    """Debug/stats — enni channels కి telegram/whatsapp link configure అయ్యాయి."""
    tg = wa = 0
    for key in CHANNELS:
        l = channel_links(key)
        tg += 1 if l.get("telegram") else 0
        wa += 1 if l.get("whatsapp") else 0
    return {"channels": len(CHANNELS), "telegram_links": tg, "whatsapp_links": wa}
