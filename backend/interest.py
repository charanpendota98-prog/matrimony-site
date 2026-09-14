"""
Mana Vivaha — INTEREST / REQUEST ENGINE  💌  (CHATTING LEDU — anthe fix)
=======================================================================
Model (top matrimony sites la advanced, kani chatting tho kaadu):
  1. User profile chusi  →  "💌 Interest Pampu" press chesthadu  (1 credit)
  2. Mana side nunchi **WhatsApp** lo aa PROFILE OWNER ki message + profile card:
       "Oka person mee profile chusi interesting ga unnaru… valla profile idi 👇"
     (ante request pettina vadi profile owner ki WhatsApp lo share avutundi ✅)
  3. Owner "✅ Accept" chesthe → **rendu numbers WhatsApp lo automatic ga** (consent based)
  4. Owner "❌ Decline" chesthe → polite message + **mee credit refund** (trust!)

Enduku chatting ledu (mee decision — correct):
  • Chat = time waste + fake accounts + harassment risk + moderation cost (24/7 team kavali)
  • Request + consent = consent-led, safe, report-friendly — Bharat Matrimony "Express Interest" la
  • Chalu: accept ayithe direct WhatsApp/phone — anthe, manam middle lo undakkarledu

Credits (mee pricing final):
  FREE  → 3 requests   (modati 3 FREE — register cheyagane)
  ₹99   → 3 profiles
  ₹199  → 10 profiles
  ₹299  → 20 profiles   (₹15/profile — best value, "Most Popular")
  Referral ₹50 → friend pay chesinappudu (referral.py lo already undi)

Rules (anti-spam + trust):
  • Oka profile ki rendu sarlu request pampalevu (duplicate block)
  • Oka roju max 20 requests (spam/fraud block)
  • Request 7 days valid → auto expire (interest fresh ga untundi)
  • Same-gender / own profile / fake ID → block
  • Decline aithe credit refund (INTEREST_REFUND_ON_DECLINE=true default)
"""
from __future__ import annotations

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

SITE = os.getenv("SITE_URL", "https://manavivaha.in").rstrip("/")
SUPPORT = os.getenv("SUPPORT_WHATSAPP", "+91 98480 12345")
BOT_USERNAME = os.getenv("BOT_USERNAME", "@telugumatrimony1_bot")

# ------------------------------------------------------------------ PLANS
PLANS: Dict[str, Dict] = {
    "FREE":    {"code": "FREE",    "price": 0,   "profiles": 3,  "validity_days": 365, "label": "Free Start",
                "telugu": "Modati 3 requests FREE", "badge": "", "per_profile": 0},
    "S_99":    {"code": "S_99",    "price": 99,  "profiles": 3,  "validity_days": 30,  "label": "Sambandham",
                "telugu": "₹99 → 3 profiles", "badge": "Starter", "per_profile": 33},
    "S_199":   {"code": "S_199",   "price": 199, "profiles": 10, "validity_days": 45,  "label": "Family",
                "telugu": "₹199 → 10 profiles", "badge": "Best for families", "per_profile": 20},
    "S_299":   {"code": "S_299",   "price": 299, "profiles": 20, "validity_days": 60,  "label": "Premium",
                "telugu": "₹299 → 20 profiles", "badge": "Most Popular • ₹15/profile", "per_profile": 15},
    "BUREAU_999": {"code": "BUREAU_999", "price": 999, "profiles": 25, "validity_days": 30,
                   "label": "Bureau Starter", "telugu": "₹999 → 25 profiles (B2B)",
                   "badge": "Bureau/Agents", "per_profile": 40},
}

MAX_PER_DAY = int(os.getenv("INTEREST_MAX_PER_DAY", "20"))
EXPIRY_DAYS = int(os.getenv("INTEREST_EXPIRY_DAYS", "7"))
REFUND_ON_DECLINE = str(os.getenv("INTEREST_REFUND_ON_DECLINE", "true")).lower() in ("1", "true", "yes", "on")
AUTO_EXPIRE_CHECK = True


def plan_list() -> List[Dict]:
    return [PLANS["FREE"], PLANS["S_99"], PLANS["S_199"], PLANS["S_299"]]


def get_plan(code: str) -> Dict:
    return PLANS.get((code or "").upper(), PLANS["FREE"])


def plan_by_amount(amount: int) -> Dict:
    for p in PLANS.values():
        if p["price"] == amount:
            return p
    return PLANS["FREE"]


# ------------------------------------------------------------------ helpers
def _now() -> datetime:
    return datetime.utcnow()


def _id(prefix: str = "REQ") -> str:
    return f"{prefix}-{datetime.utcnow().strftime('%y%m%d')}-{random.randint(1000, 9999)}"


def safe_user(u: Optional[Dict]) -> Dict:
    """Contact details teesesi (privacy first) — accept ayyaka matrame number istham."""
    if not u:
        return {}
    return {
        "tsap_id": u.get("tsap_id"),
        "full_name": u.get("full_name", "—"),
        "age": u.get("age", "—"),
        "gender": u.get("gender", "—"),
        "caste": u.get("caste", "—"),
        "sub_caste": u.get("sub_caste", ""),
        "education": u.get("education", "—"),
        "education_detail": u.get("education_detail", ""),
        "job": u.get("job", "—"),
        "company": u.get("company", ""),
        "salary": u.get("salary", "—"),
        "height": u.get("height", "—"),
        "district": u.get("district", "—"),
        "state": u.get("state", "TS"),
        "work_location": u.get("work_location", ""),
        "gothram": u.get("gothram", ""),
        "star": u.get("star", ""),
        "rasi": u.get("rasi", ""),
        "family_type": u.get("family_type", ""),
        "photo_url": u.get("photo_url", ""),
        "verified": bool(u.get("verified", False)),
    }


def daily_sent_count(interests: List[Dict], from_id: str) -> int:
    today = _now().strftime("%Y-%m-%d")
    return len([i for i in interests
                if i["from_id"] == from_id and str(i.get("created_at", "")).startswith(today)
                and i.get("status") != "withdrawn"])


def existing_request(interests: List[Dict], from_id: str, to_id: str) -> Optional[Dict]:
    for i in interests:
        if i["from_id"] == from_id and i["to_id"] == to_id and i.get("status") in ("pending", "accepted"):
            return i
    return None


def expire_old(interests: List[Dict]) -> int:
    """7 days nunchi pending lo unna requests auto expire (fresh interest only)."""
    if not AUTO_EXPIRE_CHECK:
        return 0
    n = 0
    limit = _now() - timedelta(days=EXPIRY_DAYS)
    for i in interests:
        if i.get("status") != "pending":
            continue
        try:
            if datetime.fromisoformat(i["created_at"]) < limit:
                i["status"] = "expired"
                i["status_at"] = _now().isoformat()
                n += 1
        except Exception:
            continue
    return n


# ------------------------------------------------------------------ core flow
def can_send_interest(frm: Dict, to: Dict, interests: List[Dict]) -> Tuple[bool, str]:
    if not frm or not to:
        return False, "TSAP ID correct ga ivvandi"
    if frm.get("tsap_id") == to.get("tsap_id"):
        return False, "Mee profile ki meeru request pampalervu 🙂"
    g1, g2 = (frm.get("gender") or "").lower(), (to.get("gender") or "").lower()
    if g1 and g2 and g1 == g2:
        return False, "Telugu matrimony lo opposite gender ki matrame interest pampali"
    if existing_request(interests, frm["tsap_id"], to["tsap_id"]):
        return False, "Ee profile ki already request pampincharu — reply kosam wait cheyyandi"
    if int(frm.get("credits", 0)) <= 0:
        return False, "credits_ledu"
    if daily_sent_count(interests, frm["tsap_id"]) >= MAX_PER_DAY:
        return False, f"Rojuki {MAX_PER_DAY} requests limit — repu malli try cheyyandi (spam block)"
    return True, "ok"


def create_interest(frm: Dict, to: Dict, note: str = "", score: int = 0,
                    reasons: Optional[List[str]] = None, channel: str = "website") -> Dict:
    rec = {
        "request_id": _id("REQ"),
        "from_id": frm["tsap_id"],
        "to_id": to["tsap_id"],
        "from_name": frm.get("full_name", ""),
        "to_name": to.get("full_name", ""),
        "note": (note or "").strip()[:280],
        "score": score,
        "reasons": (reasons or [])[:4],
        "status": "pending",           # pending | accepted | declined | expired | withdrawn
        "channel": channel,
        "credit_spent": 1,
        "credit_refunded": False,
        "contact_shared": False,
        "created_at": _now().isoformat(),
        "status_at": _now().isoformat(),
        "expires_at": (_now() + timedelta(days=EXPIRY_DAYS)).isoformat(),
    }
    return rec


def respond_interest(rec: Dict, owner: Dict, requester: Dict, action: str) -> Dict:
    """Owner accept/decline. Contact exchange + refund logic."""
    action = (action or "").lower()
    if rec.get("status") != "pending":
        return {"success": False, "message": f"Ee request already {rec.get('status')} — inka action ledu"}
    rec["status_at"] = _now().isoformat()
    out = {"success": True, "request_id": rec["request_id"], "action": action}
    if action == "accept":
        rec["status"] = "accepted"
        rec["contact_shared"] = True
        out["owner_phone"] = owner.get("phone", "")
        out["requester_phone"] = requester.get("phone", "")
        out["message"] = "✅ Accept ayyindi — rendu numbers WhatsApp lo share ayyayi"
    elif action == "decline":
        rec["status"] = "declined"
        if REFUND_ON_DECLINE:
            rec["credit_refunded"] = True
            out["refund"] = 1
        out["message"] = "Request decline ayyindi" + (" — mee credit refund ayyindi ✅" if REFUND_ON_DECLINE else "")
    elif action == "withdraw":
        rec["status"] = "withdrawn"
        out["message"] = "Request withdraw ayyindi"
    else:
        return {"success": False, "message": "action = accept | decline | withdraw"}
    return out


# ------------------------------------------------------------------ WhatsApp texts
def interest_to_owner_text(requester: Dict, owner: Dict, rec: Dict) -> str:
    """Owner ki message — requester profile (idi user adigina 'profile share')."""
    r = safe_user(requester)
    reasons = "\n".join(f"  ✅ {x}" for x in (rec.get("reasons") or [])[:3])
    return (
        f"💌 *MANA VIVAHA — Mee profile ki INTEREST vachhindi!*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"Oka person mee profile chusi *\"interesting ga unnaru\"* ani request pettaru 👇\n\n"
        f"👤 *{r['full_name']}*  ({r['age']} yrs)\n"
        f"🆔 {r['tsap_id']}{'  ✅ Verified' if r['verified'] else ''}\n"
        f"🎓 {r['education']} {r['education_detail']}\n"
        f"💼 {r['job']} {r['company']}\n"
        f"💰 {r['salary']}  |  📏 {r['height']}\n"
        f"📍 {r['district']}, {r['state']}{'  •  💼 ' + r['work_location'] if r['work_location'] else ''}\n"
        f"💍 {r['caste']}{' / ' + r['sub_caste'] if r['sub_caste'] else ''}"
        f"{'  |  Gothram: ' + r['gothram'] if r['gothram'] else ''}\n"
        f"🌟 Star: {r['star'] or '—'}  |  Rasi: {r['rasi'] or '—'}\n"
        + (f"⭐ *{rec['score']}% match* — {', '.join((rec.get('reasons') or [])[:2])}\n" if rec.get("score") else "")
        + (f"📝 *Valla message:* \"{rec['note']}\"\n" if rec.get("note") else "")
        + f"━━━━━━━━━━━━━━━━\n"
        f"📸 Full profile + photo: {SITE}/search/{r['tsap_id']}\n"
        f"✅ *Accept* chesthe → valla number meeku WhatsApp lo vastundi\n"
        f"❌ *Decline* chesthe → polite ga no cheptham (and valla credit refund)\n"
        f"🚫 Chatting ledu — *direct contact exchange matrame* (safe, no time waste)\n"
        f"💻 Accept/Decline ikkada: {SITE}/requests?id={owner.get('tsap_id','')}\n"
        f"🆔 Request ID: {rec['request_id']}  •  ⏳ {EXPIRY_DAYS} days valid\n"
        f"⚠️ Mana Vivaha eppudu advance money adagadu • Report: {SUPPORT}"
    )


def interest_accepted_text(requester: Dict, owner: Dict, rec: Dict) -> str:
    o = safe_user(owner)
    phone = str(owner.get("phone", "") or "").strip()
    phone_line = f"📞 *{phone}*" if phone else f"📞 Number: {SITE}/requests?id={requester.get('tsap_id','')}"
    return (
        f"🎉 *INTEREST ACCEPT AYYINDI!*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 *{o['full_name']}* ({o['tsap_id']}) mee request ni *accept* chesaru ✅\n\n"
        f"📞 Contact: {phone_line}  (+ WhatsApp)\n"
        f"📍 {o['district']}, {o['state']}  |  💍 {o['caste']}\n"
        f"🎓 {o['education']}  |  💼 {o['job']}\n\n"
        f"✅ Mee number kuda vallaki share ayyindi — ippudu direct matladukovachu\n"
        f"💐 All the best! Mana Vivaha parivaaram nunchi shubhakankshalu\n"
        f"❓ Emaina help kavali ante: {SUPPORT}\n"
        f"⚠️ Advance money / gold adigite ventane report cheyyandi — safety first"
    )


def interest_declined_text(requester: Dict, owner: Dict, rec: Dict) -> str:
    o = safe_user(owner)
    refund = "✅ Mee credit refund ayyindi (mana trust policy)" if rec.get("credit_refunded") else ""
    return (
        f"🙏 *MANA VIVAHA — Response vachhindi*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 {o['full_name']} ({o['tsap_id']}) ee sari interest ki yes analedu.\n"
        f"{refund}\n\n"
        f"💚 Niraasa padakandi — {SITE}/matches lo mee {o['caste']} "
        f"{o['district']} matches chudandi, rojuki kotha profiles vasthayi.\n"
        f"💡 Tip: photo + gothram + star add chesthe 3x ekkuva acceptances vasthayi\n"
        f"🆔 {rec['request_id']}"
    )


def interest_notify_text(requester: Dict, owner: Dict, rec: Dict) -> str:
    """Requester ki confirmation (mana WhatsApp nunchi)."""
    o = safe_user(owner)
    return (
        f"✅ *Interest pampincharu — {rec['request_id']}*\n"
        f"👤 {o['full_name']} ({o['tsap_id']}) — {o['district']}, {o['caste']}\n"
        f"⏳ {EXPIRY_DAYS} days lo reply vasthundi (accept/decline)\n"
        f"📊 Mee credits: {requester.get('credits', 0)} migilayi\n"
        f"📸 Valla profile: {SITE}/search/{o['tsap_id']}\n"
        f"💡 Advance money adigite ventane report cheyyandi — {SUPPORT}"
    )


# ------------------------------------------------------------------ inbox views
def inbox_for(user: Dict, users: List[Dict], interests: List[Dict]) -> Dict:
    """Received requests — contact owner accept chesina tarvata matrame kanipisthundi."""
    me = user["tsap_id"]
    recv = [i for i in interests if i["to_id"] == me]
    recv.sort(key=lambda x: (x.get("status") != "pending", x.get("created_at", "")), reverse=False)
    out = []
    for i in recv:
        req_user = next((u for u in users if u["tsap_id"] == i["from_id"]), None)
        item = dict(i)
        item["requester"] = safe_user(req_user)
        item["requester_phone"] = (req_user or {}).get("phone", "") if i.get("contact_shared") else "🔒 accept cheyyandi"
        item["actions"] = ["accept", "decline"] if i.get("status") == "pending" else []
        out.append(item)
    return {
        "tsap_id": me,
        "pending": len([x for x in out if x["status"] == "pending"]),
        "accepted": len([x for x in out if x["status"] == "accepted"]),
        "declined": len([x for x in out if x["status"] == "declined"]),
        "expired": len([x for x in out if x["status"] == "expired"]),
        "received": out,
    }


def sent_for(user: Dict, users: List[Dict], interests: List[Dict]) -> Dict:
    me = user["tsap_id"]
    sent = [i for i in interests if i["from_id"] == me]
    sent.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    out = []
    for i in sent:
        to_user = next((u for u in users if u["tsap_id"] == i["to_id"]), None)
        item = dict(i)
        item["profile"] = safe_user(to_user)
        item["contact"] = (to_user or {}).get("phone", "") if i.get("status") == "accepted" else "🔒 accept ayyaka"
        out.append(item)
    return {
        "tsap_id": me,
        "pending": len([x for x in out if x["status"] == "pending"]),
        "accepted": len([x for x in out if x["status"] == "accepted"]),
        "sent": out,
    }
