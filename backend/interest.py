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

Credits (final ladder — ₹/profile prati tier lo thaggutundi):
  FREE  → 3 requests   (modati 3 FREE — register cheyagane)
  ₹99   → 5 profiles        (₹19.8/profile)
  ₹199  → 12 profiles       (₹16.6/profile, "Most popular")
  ₹299  → 25 profiles       (₹12/profile, "Best value")
  ₹499  → 50 profiles       (₹10/profile, VIP + matchmaker)
  Add-ons: ⚡ Boost ₹49 • 👀 Who-viewed ₹49 • 🔮 Porutham ₹99 • ✅ Verify ₹199
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
# 📊 PRICING LADDER (₹/profile thaggutuu pothundi → ₹299 ki "best value" ga kanipisthundi)
#    FREE 3  →  ₹99 = 5  →  ₹199 = 12  →  ₹299 = 25  →  ₹499 = 50
#    Enduku free 3, ₹99 ki 3 kadu? FREE ke 3 istham — ₹99 ki kooda 3 isthe evaru pay cheyyaru.
#    Enduku 5/12/25/50? Per-profile value 19.8 → 16.6 → 12 → 10 — clear upsell ladder (anchoring).
PLANS: Dict[str, Dict] = {
    "FREE": {
        "code": "FREE", "price": 0, "profiles": 3, "validity_days": 365,
        "label": "Free Start", "telugu": "Modati 3 requests FREE", "badge": "No card needed",
        "per_profile": 0, "perks": ["3 interest requests", "WhatsApp lo mee profile share", "Auto-post 65 channels"],
    },
    "S_29": {
        "code": "S_29", "price": 29, "profiles": 1, "validity_days": 15,
        "label": "Okka Request", "telugu": "₹29 → 1 profile (modati try ki)",
        "badge": "Single • ₹29/profile", "per_profile": 29, "micro": True,
        "perks": ["1 interest request", "WhatsApp lo mee profile share + 1 card",
                  "Ee request decline aithe credit refund"],
    },
    "S_99": {
        "code": "S_99", "price": 99, "profiles": 5, "validity_days": 30,
        "label": "Sambandham", "telugu": "₹99 → 5 profiles", "badge": "Entry • ₹19.8/profile",
        "per_profile": 20, "perks": ["5 interest requests", "⚡ 7-day profile boost (top of channel)", "Decline aithe refund"],
    },
    "S_199": {
        "code": "S_199", "price": 199, "profiles": 12, "validity_days": 45,
        "label": "Family", "telugu": "₹199 → 12 profiles", "badge": "Most popular • ₹16.6/profile",
        "per_profile": 17, "perks": ["12 interest requests", "✅ Photo-verified badge (trust boost)", "⭐ Free 10-porutham report (1)", "Family bureau assist"],
    },
    "S_299": {
        "code": "S_299", "price": 299, "profiles": 25, "validity_days": 60,
        "label": "Premium", "telugu": "₹299 → 25 profiles", "badge": "Best value • ₹12/profile",
        "per_profile": 12, "perks": ["25 interest requests", "⚡ 30-day boost (top of channel)", "✅ Photo-verified badge", "👀 Who-viewed-me 60 days", "Telugu support (dedicated)"],
    },
    "S_499": {
        "code": "S_499", "price": 499, "profiles": 50, "validity_days": 90,
        "label": "Vivaha VIP", "telugu": "₹499 → 50 profiles", "badge": "VIP • ₹10/profile",
        "per_profile": 10, "perks": ["50 interest requests", "🎯 Matchmaker assist (mana team call chesi matches chupisthundi)",
                                   "⚡ 90-day boost", "💍 Wedding vendor discounts", "Priority WhatsApp support"],
    },
    "BUREAU_999": {
        "code": "BUREAU_999", "price": 999, "profiles": 25, "validity_days": 30,
        "label": "Bureau Starter", "telugu": "₹999 → 25 profiles (B2B)", "badge": "Bureau/Agents",
        "per_profile": 40, "perks": ["25 profiles", "Monthly engaged report", "Bulk register"],
    },
    "BUREAU_2999": {
        "code": "BUREAU_2999", "price": 2999, "profiles": 100, "validity_days": 30,
        "label": "Bureau Pro", "telugu": "₹2999 → 100 profiles (B2B)", "badge": "Bureau Pro",
        "per_profile": 30, "perks": ["100 profiles", "Agent dashboard + client management", "Priority channel posting"],
    },
}

# 🎁 ADD-ONS (credits kanna — per-item revenue. Ivi "cheap ga" kanipisthayi, margin 100%)
ADDONS: Dict[str, Dict] = {
    "BOOST_49": {"code": "BOOST_49", "price": 49, "label": "Profile Boost 7 days",
                 "telugu": "Mee card 7 days channel top lo", "kind": "boost", "days": 7},
    "WHOVIEWED_49": {"code": "WHOVIEWED_49", "price": 49, "label": "Who viewed me (30 days)",
                     "telugu": "Mee profile ni evaru chusaru — names tho", "kind": "whoviewed", "days": 30},
    "PORUTHAM_99": {"code": "PORUTHAM_99", "price": 99, "label": "10-Porutham report",
                    "telugu": "Full kundli match report (Telugu)", "kind": "porutham", "days": 365},
    "VERIFY_199": {"code": "VERIFY_199", "price": 199, "label": "Photo verification badge",
                   "telugu": "✅ Verified badge — 3x ekkuva acceptances", "kind": "verify", "days": 365},
}

# 🔁 RENEWAL OFFER — pata customer ki ekkuva value (loyalty + repeat revenue)
RENEWALS: Dict[str, Dict] = {
    "RENEW_99": {"code": "RENEW_99", "price": 99, "profiles": 8, "validity_days": 30,
                 "label": "Renewal Bonus", "telugu": "₹99 → 8 profiles (pata customer special)",
                 "badge": "Renewal • ₹12.4/profile", "per_profile": 12,
                 "perks": ["8 interest requests", "⚡ 7-day boost free"]},
}

MAX_PER_DAY = int(os.getenv("INTEREST_MAX_PER_DAY", "20"))
EXPIRY_DAYS = int(os.getenv("INTEREST_EXPIRY_DAYS", "7"))
REFUND_ON_DECLINE = str(os.getenv("INTEREST_REFUND_ON_DECLINE", "true")).lower() in ("1", "true", "yes", "on")
AUTO_EXPIRE_CHECK = True


def plan_list() -> List[Dict]:
    """Purchasable plans (FREE separate ga chupistham)."""
    return [PLANS["S_29"], PLANS["S_99"], PLANS["S_199"], PLANS["S_299"], PLANS["S_499"]]


def plan_list_with_free() -> List[Dict]:
    return [PLANS["FREE"]] + plan_list()


def addon_list() -> List[Dict]:
    return list(ADDONS.values())


def renewal_offer() -> Dict:
    return RENEWALS["RENEW_99"]


def get_plan(code: str) -> Dict:
    key = (code or "").upper()
    return PLANS.get(key) or ADDONS.get(key) or RENEWALS.get(key) or PLANS["FREE"]


def get_addon(code: str) -> Optional[Dict]:
    return ADDONS.get((code or "").upper())


def is_addon(code: str) -> bool:
    return (code or "").upper() in ADDONS


def get_renewal(code: str = "RENEW_99") -> Optional[Dict]:
    return RENEWALS.get((code or "").upper())


def plan_by_amount(amount: int) -> Dict:
    for p in PLANS.values():
        if p["price"] == amount:
            return p
    return PLANS["FREE"]


def apply_payment(user: Dict, amount: int, plan_code: str = "") -> Dict:
    """
    💰 Payment vachhaka **okka chota** nunchi plan apply (profile credits + expiry).
    plan_code ichithe adi; lekapote amount batti plan/addon/renewal kantey.
    Single source of truth = PLANS / ADDONS / RENEWALS (legacy credits.py kaadu).
    """
    code = (plan_code or "").upper()
    plan = None
    kind = "plan"
    if code:
        plan = PLANS.get(code)
        if not plan and code in ADDONS:
            plan, kind = ADDONS[code], "addon"
        if not plan and code in RENEWALS:
            plan, kind = RENEWALS[code], "renewal"
    if not plan:                                # amount batti (gateway amount matrame isthundi)
        matches = [p for p in PLANS.values() if p["price"] == amount and p["price"] > 0]
        if matches:
            plan = matches[0]
        else:
            matches = [a for a in ADDONS.values() if a["price"] == amount]
            if matches:
                plan, kind = matches[0], "addon"
    if not plan:
        return {"ok": False, "error": "amount/plan match avvaledu", "amount": amount, "code": code}
    profiles = int(plan.get("profiles", 0) or 0)
    if profiles:                                # profile/request credits add
        user["credits"] = int(user.get("credits", 0)) + profiles
    user["plan"] = plan["code"]
    if kind in ("plan", "renewal"):
        user["plan_expiry"] = datetime.utcnow() + timedelta(days=int(plan.get("validity_days", 30)))
    user["last_payment"] = {"amount": amount, "plan": plan["code"], "kind": kind,
                            "at": datetime.utcnow().isoformat()}
    return {"ok": True, "kind": kind, "plan": plan,
            "profiles_added": profiles, "credits": user.get("credits", 0),
            "expiry": user.get("plan_expiry").isoformat() if user.get("plan_expiry") else "",
            "message_telugu": ("🎉 ₹%d payment success — %s" % (amount, plan.get("telugu", plan.get("label", ""))))
                              + (" • Mee daggara ippudu %d profiles" % user.get("credits", 0) if profiles else "")}


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
