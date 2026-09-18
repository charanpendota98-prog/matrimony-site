"""
MANA VIVAHA — TRUST & SAFETY ENGINE 🛡️
======================================
Top matrimony sites lo "report / block / verification" undi — manam kooda (inka better ga):

  1. 🚨 REPORT — fake profile, advance money scam, harassment, wrong photo, married, spam
     • 3 valid reports → profile **auto-hide** (admin chudakamunde)
     • severity level batti priority (scam/harassment = high)
  2. 🚫 BLOCK — user ni block (vaallu mee profile chudalenu, interest pampalenru, search lo kanipinchadu)
  3. ✅ VERIFICATION LEVELS — phone ✅ → photo ✅ → ID (KYC) ✅ (badge card lo + search lo)
  4. 👮 MODERATION QUEUE — admin oke chota chusi action teesukovachu
       (verify / warn / hide / ban / dismiss) — audit log tho
  5. 💡 SAFETY TIPS — Telugu lo (scam build-up, public meeting, video call verify)

Ee module pure logic — DB lists main.py nunchi istham (test lo in-memory).
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Tuple

DB_REPORTS: List[Dict] = []
DB_BLOCKS: List[Dict] = []          # {"owner": tsap, "blocked": tsap, "at": iso, "reason": ""}

REPORT_CATEGORIES = {
    "fake_profile": {"te": "నకిలీ ప్రొఫైల్", "severity": "high",
                     "desc": "Photo/పేరు/details నిజం kaavu (photos vere వాళ్ల vi)"},
    "advance_money": {"te": "ముందు డబ్బు అడిగారు", "severity": "high",
                      "desc": "Advance/registration/visa అని money adigaru (100% scam)"},
    "harassment": {"te": "వేధింపు / అసభ్య మాటలు", "severity": "high",
                   "desc": "Asabhyam గా matladaru, threat చేశారు, blackmail"},
    "wrong_photo": {"te": "ఫోటో మార్చేశారు", "severity": "medium",
                    "desc": "Photo వేరు, asalu vyakti వేరు (video call లో telisindi)"},
    "already_married": {"te": "ఇప్పటికే పెళ్లి అయ్యింది", "severity": "high",
                        "desc": "పెళ్లి అయింది కానీ profile లో లేదు అని cheppaledu"},
    "spam": {"te": "స్పామ్ / ప్రకటనలు", "severity": "low",
             "desc": "Interest కాదు — business/promo messages pampisthunnaru"},
    "other": {"te": "ఇతర", "severity": "medium", "desc": "Vere problem — detail లో రాయండి"},
}
ACTION_RULES = {"verify": "✅ Manually verify చేసి badge icharu",
                "warn": "⚠️ Warning pampincharu (audit log లో ఉంది)",
                "hide": "🙈 Profile hide అయ్యింది (admin review)",
                "ban": "⛔ Profile ban (permanent) — channels నుంచి teesestham",
                "dismiss": "❌ Report dismiss (evidence saripoledu)"}


def submit_report(reporter_id: str, target_id: str, category: str, detail: str = "",
                  reports: Optional[List[Dict]] = None, users: Optional[List[Dict]] = None) -> Tuple[bool, str, Dict]:
    """Report submit + auto-flag (3+ high/valid reports → auto hide)."""
    reports = DB_REPORTS if reports is None else reports
    users = users if users is not None else []
    cat = str(category or "").strip().lower()
    if cat not in REPORT_CATEGORIES:
        return False, "Category tappu — ఇవి మాత్రమే: " + ", ".join(REPORT_CATEGORIES), {}
    if not reporter_id or not target_id:
        return False, "reporter + target TSAP ID కావాలి", {}
    if str(reporter_id) == str(target_id):
        return False, "Meeru meeku report cheyyaleemu", {}
    dup = next((r for r in reports if r["reporter_id"] == reporter_id and r["target_id"] == target_id
                and r["category"] == cat and r["status"] == "open"), None)
    if dup:
        dup["detail"] = detail or dup.get("detail", "")
        dup["updated_at"] = datetime.utcnow().isoformat()
        dup["repeat_count"] = int(dup.get("repeat_count", 1)) + 1
        return True, "report_updated", dup

    rec = {
        "id": "REP-" + datetime.utcnow().strftime("%y%m%d") + "-" + str(len(reports) + 1).zfill(4),
        "reporter_id": reporter_id, "target_id": target_id, "category": cat,
        "category_telugu": REPORT_CATEGORIES[cat]["te"], "severity": REPORT_CATEGORIES[cat]["severity"],
        "detail": str(detail)[:500], "status": "open", "at": datetime.utcnow().isoformat(),
        "action": "", "auto_flagged": False, "repeat_count": 1,
    }
    reports.append(rec)
    # auto-flag rules
    open_mine = [r for r in reports if r["target_id"] == target_id and r["status"] == "open"]
    highs = [r for r in open_mine if r["severity"] == "high"]
    distinct_reporters = len({r["reporter_id"] for r in open_mine})
    if len(highs) >= 2 or distinct_reporters >= 3 or len(open_mine) >= 4:
        rec["auto_flagged"] = True
        rec["auto_action"] = "profile_hidden_for_review"
        tgt = next((u for u in users if u.get("tsap_id") == target_id), None)
        if tgt is not None:
            tgt["is_approved"] = False
            tgt["hidden_reason"] = "auto_flag: %d reports (severity high: %d)" % (len(open_mine), len(highs))
            tgt["hidden_at"] = datetime.utcnow().isoformat()
    return True, "new_report", rec


def report_stats(reports: Optional[List[Dict]] = None) -> Dict:
    reports = DB_REPORTS if reports is None else reports
    openr = [r for r in reports if r["status"] == "open"]
    by_cat: Dict[str, int] = {}
    for r in reports:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    return {"total": len(reports), "open": len(openr),
            "high": len([r for r in openr if r["severity"] == "high"]),
            "auto_flagged": len([r for r in reports if r.get("auto_flagged")]),
            "resolved": len([r for r in reports if r["status"] == "resolved"]),
            "by_category": by_cat,
            "message_telugu": "%d open reports (high priority: %d) — ముందు scam/harassment చూడండి"
                              % (len(openr), len([r for r in openr if r["severity"] == "high"]))}


def block_user(owner_id: str, blocked_id: str, reason: str = "",
               blocks: Optional[List[Dict]] = None) -> Tuple[bool, str, Dict]:
    blocks = DB_BLOCKS if blocks is None else blocks
    if not owner_id or not blocked_id or owner_id == blocked_id:
        return False, "Tappu IDs", {}
    existing = next((b for b in blocks if b["owner"] == owner_id and b["blocked"] == blocked_id), None)
    if existing:
        return True, "already_blocked", existing
    rec = {"owner": owner_id, "blocked": blocked_id, "reason": str(reason)[:200],
           "at": datetime.utcnow().isoformat()}
    blocks.append(rec)
    return True, "blocked", rec


def unblock_user(owner_id: str, blocked_id: str, blocks: Optional[List[Dict]] = None) -> Tuple[bool, str]:
    blocks = DB_BLOCKS if blocks is None else blocks
    before = len(blocks)
    blocks[:] = [b for b in blocks if not (b["owner"] == owner_id and b["blocked"] == blocked_id)]
    return (len(blocks) < before), ("unblocked" if len(blocks) < before else "not_blocked")


def is_blocked(a: str, b: str, blocks: Optional[List[Dict]] = None) -> bool:
    """Either side block చేసిన true (రెండు directions)."""
    blocks = DB_BLOCKS if blocks is None else blocks
    return any((x["owner"] == a and x["blocked"] == b) or (x["owner"] == b and x["blocked"] == a) for x in blocks)


def block_list(owner_id: str, blocks: Optional[List[Dict]] = None) -> List[Dict]:
    blocks = DB_BLOCKS if blocks is None else blocks
    return [b for b in blocks if b["owner"] == owner_id]


# --------------------------------------------------------------- verification
VERIFY_LEVELS = ["none", "phone", "photo", "id"]
VERIFY_TELUGU = {
    "none": "verify కాలేదు",
    "phone": "📱 Phone verified (OTP)",
    "photo": "📱✅ Phone + 📸 Photo verified",
    "id": "🏅 Aadhaar/ID verified (full trust badge)",
}


def set_verification(user: Dict, kind: str) -> Tuple[bool, str, Dict]:
    """phone / photo / id verification level set (level ఎప్పుడు penchadam మాత్రమే)."""
    kind = str(kind or "").strip().lower()
    if kind not in ("phone", "photo", "id"):
        return False, "kind: phone | photo | id మాత్రమే", {}
    cur = str((user or {}).get("verification_level", "none") or "none")
    if VERIFY_LEVELS.index(kind) > VERIFY_LEVELS.index(cur):
        user["verification_level"] = kind
    user["verification_" + kind] = True
    if kind == "photo":
        user["photo_verified"] = True
    if kind == "id":
        user["id_verified"] = True
    user["verified_at"] = datetime.utcnow().isoformat()
    return True, "level_%s" % user.get("verification_level", kind), user


def verification_badge(user: Dict) -> Dict:
    """Search/profile లో చూపించడానికి badge (text + level + next step)."""
    u = user or {}
    lvl = str(u.get("verification_level", "none") or "none")
    if lvl == "none" and (u.get("phone_verified") or u.get("is_verified")):
        lvl = "phone"
    next_step = {"none": "OTP తో phone verify చెయ్యండి (30 sec)",
                 "phone": "photo verify చెయ్యండి (selfie + photo)",
                 "photo": "ID verify చెయ్యండి (Aadhaar last 4 digits) — full trust badge",
                 "id": "అన్నీ verify అయ్యాయి — మీ profile top లో కనిపిస్తుంది"}[lvl]
    return {"level": lvl, "telugu": VERIFY_TELUGU[lvl], "stars": VERIFY_LEVELS.index(lvl),
            "trust_score": {"none": 40, "phone": 65, "photo": 85, "id": 100}[lvl],
            "next_step_telugu": next_step}


# --------------------------------------------------------------- moderation
def moderation_queue(reports: Optional[List[Dict]] = None, users: Optional[List[Dict]] = None,
                     limit: int = 50) -> Dict:
    reports = DB_REPORTS if reports is None else reports
    users = users or []
    order = {"high": 0, "medium": 1, "low": 2}
    openr = [r for r in reports if r["status"] == "open"]
    openr.sort(key=lambda r: (order.get(r["severity"], 3), r["at"]))
    items = []
    for r in openr[:limit]:
        tgt = next((u for u in users if u.get("tsap_id") == r["target_id"]), None)
        same_target = [x for x in openr if x["target_id"] == r["target_id"]]
        items.append({
            "report_id": r["id"], "category": r["category"], "category_telugu": r["category_telugu"],
            "severity": r["severity"], "detail": r["detail"], "at": r["at"],
            "reporter_id": r["reporter_id"], "target_id": r["target_id"],
            "reports_on_target": len(same_target),
            "target": ({"tsap_id": tgt.get("tsap_id"), "full_name": tgt.get("full_name"),
                        "phone_last4": tgt.get("phone_last4"), "district": tgt.get("district"),
                        "is_approved": tgt.get("is_approved", True),
                        "verification": verification_badge(tgt)["level"]} if tgt else None),
            "suggested_action": ("ban" if r["severity"] == "high" and len(same_target) >= 2 else
                                 "hide" if r["severity"] == "high" else "warn"),
        })
    return {"open": len(openr), "items": items, "actions": list(ACTION_RULES.keys()),
            "message_telugu": "High severity reports ముందు చూడండి — scam/harassment కి వెంటనే action teesukondi"}


def resolve_report(report_id: str, action: str, note: str = "",
                   reports: Optional[List[Dict]] = None, users: Optional[List[Dict]] = None) -> Tuple[bool, str, Dict]:
    reports = DB_REPORTS if reports is None else reports
    rec = next((r for r in reports if r["id"] == report_id), None)
    if not rec:
        return False, "Report దొరకలేదు: %s" % report_id, {}
    action = str(action or "").strip().lower()
    if action not in ACTION_RULES:
        return False, "action ఇవి మాత్రమే: " + ", ".join(ACTION_RULES), {}
    rec["status"] = "resolved"
    rec["action"] = action
    rec["action_telugu"] = ACTION_RULES[action]
    rec["resolved_at"] = datetime.utcnow().isoformat()
    rec["admin_note"] = str(note)[:300]
    tgt = next((u for u in (users or []) if u.get("tsap_id") == rec["target_id"]), None)
    if tgt is not None:
        if action == "hide":
            tgt["is_approved"] = False
            tgt["hidden_reason"] = "admin: " + note[:120]
        elif action == "ban":
            tgt["is_approved"] = False
            tgt["is_banned"] = True
            tgt["banned_at"] = datetime.utcnow().isoformat()
        elif action == "verify":
            set_verification(tgt, "photo")
        elif action == "warn":
            tgt["warnings"] = int(tgt.get("warnings", 0)) + 1
    # same target ki migilina open reports ni kooda close chey (oke action tho)
    for r in reports:
        if r["target_id"] == rec["target_id"] and r["status"] == "open":
            r["status"] = "resolved"
            r["action"] = action
            r["resolved_at"] = datetime.utcnow().isoformat()
            r["admin_note"] = "bulk resolve: " + rec["id"]
    return True, action, rec


# --------------------------------------------------------------- safety tips
def safety_tips() -> List[Dict]:
    """Telugu safety tips — /safety page + welcome message లో reuse."""
    return [
        {"icon": "💰", "title": "Advance money ఎప్పుడు వద్దు",
         "telugu": "Registration fee / visa / hospital / train ticket అని ఎవరు adigina — 100% scam. Ventane report చెయ్యండి: "
                   "మన team 24h లో action teesukuntundi."},
        {"icon": "📸", "title": "Photo ఎప్పుడు verify చెయ్యండి",
         "telugu": "Matrimony profile లో photos vere వాళ్ల vi కూడా undochu. WhatsApp video call (2 నిమిషాలు) చేసి confirm చెయ్యండి."},
        {"icon": "🏠", "title": "మొదటి kalthi public place లో",
         "telugu": "Pellichoopulu/temple/hotel lobby — ఇంట్లో కాదు, okkari తో కాదు. Inti peddavallani teesukondi."},
        {"icon": "📱", "title": "Number/OTP ఎవరికీ ivvakandi",
         "telugu": "మన site లో number interest accept అయ్యాక మాత్రమే share అవుతుంది. OTP అని ఎవరు adigina — ivvakandi."},
        {"icon": "📄", "title": "Certificates chusi confirm చెయ్యండి",
         "telugu": "Age/ID/education certificates original chusi, parents తో కలిసి మాత్రమే final చెయ్యండి."},
        {"icon": "🚫", "title": "Chatting లేదు — spam ఉండదు",
         "telugu": "మన site లో chatting లేదు. Interest accept అయితే — direct గా మీరు matladukovachu (మనం middle లో undamu)."},
    ]


def report_ack_text(target_name: str = "profile") -> str:
    return ("🙏 Report andinai ki dhanyavadalu!\n"
            "మన safety team 24 hours లో chusi action teesukuntundi.\n"
            "🔒 మీ పేరు report లో కనిపించదు — privacy 100%% protected.\n"
            "⚠️ ఈ madhya aa profile నుంచి money అడిగితే వెంటనే screenshots పంపండి.")
