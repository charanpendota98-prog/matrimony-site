"""
🤝🌊 WAVE 19 — REFERRAL PARTNERS (agents/brokers with own ID + link + sheet)
===============================================================================
Website → Refer → profile create (name, phone, PhonePe number, address, state, district)
 → ID generate (ex: charan108) + link (/r/charan108 — short, click-tracked)
 → link tho open chesthe register daggara referral code AUTO-FILL (existing ?ref= flow)
 → join + payment commissions vallaki (same ₹50 rule, wallet + payouts)
 → anni data manaki: JSON + **referral_partners.csv SHEET** + admin report.

Partner dict = referrer-compatible (referral_code/stats/wallet) → find_referrer/
attach_referral/process_referral_payment anni automatic ga pani chestayi.
"""
from __future__ import annotations

import csv
import json
import os
import random
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE, "refpartners19.json")
CSV_FILE = os.path.join(BASE, "referral_partners.csv")
CSV_HEADER = ["partner_id", "name", "phone", "phonepe", "address", "state", "district",
              "link", "created_at", "registrations", "paid_count", "wallet", "paid_out"]

PARTNERS: List[Dict[str, Any]] = []
_STATES = {"TS", "AP", "KA", "MH", "Other"}


def _now() -> str:
    return datetime.utcnow().isoformat()


def _load() -> None:
    global PARTNERS
    try:
        if os.path.exists(JSON_FILE):
            PARTNERS = json.load(open(JSON_FILE, encoding="utf-8")) or []
    except Exception:
        PARTNERS = []


def _save() -> None:
    try:
        json.dump(PARTNERS, open(JSON_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception:
        pass


def _csv_append(p: Dict[str, Any]) -> None:
    try:
        new = not os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(CSV_HEADER)
            st = p.get("referral_stats", {})
            w.writerow([p.get("partner_id", ""), p.get("name", ""), p.get("phone", ""),
                        p.get("phonepe", ""), p.get("address", ""), p.get("state", ""),
                        p.get("district", ""), p.get("link", ""), p.get("created_at", ""),
                        st.get("registrations", 0), st.get("paid_count", 0),
                        st.get("wallet", 0), st.get("paid_out", 0)])
    except Exception:
        pass


def _gen_id(name: str) -> str:
    base = re.sub(r"[^a-z]", "", (name or "").strip().lower().split()[0] if (name or "").strip() else "ref")[:10] or "ref"
    for _ in range(50):
        pid = f"{base}{random.randint(100, 999)}"
        if not any(p.get("partner_id", "").lower() == pid for p in PARTNERS):
            return pid
    return f"{base}{random.randint(1000, 9999)}"


def get_partner(pid: str) -> Optional[Dict[str, Any]]:
    p = (pid or "").strip().lower()
    return next((x for x in PARTNERS if str(x.get("partner_id", "")).lower() == p), None)


def find_partner_by_code(code: str) -> Optional[Dict[str, Any]]:
    """referral.find_referrer fallback — partner ID/code tho match."""
    if not code:
        return None
    return get_partner(code)


def register_partner(name: str, phone: str, phonepe: str = "", address: str = "",
                     state: str = "", district: str = "", site: str = "") -> Dict[str, Any]:
    name = re.sub(r"\s+", " ", (name or "").strip())[:60]
    if len(name) < 2:
        return {"success": False, "reason": "bad_name",
                "message_telugu": "⚠️ Name ivvandi (min 2 letters)"}
    phone = "".join(ch for ch in str(phone or "") if ch.isdigit())
    if len(phone) != 10 or phone[0] not in "6789":
        return {"success": False, "reason": "bad_phone",
                "message_telugu": "⚠️ 10-digit mobile number ivvandi (6/7/8/9 tho start)"}
    if any(p.get("phone") == phone for p in PARTNERS):
        ex = next(p for p in PARTNERS if p.get("phone") == phone)
        return {"success": True, "already": True, "partner_id": ex["partner_id"],
                "link": ex.get("link", ""),
                "message_telugu": f"ℹ️ Ee number tho already partner ID undi: {ex['partner_id']}"}
    phonepe_d = "".join(ch for ch in str(phonepe or "") if ch.isdigit())
    if phonepe_d and (len(phonepe_d) != 10 or phonepe_d[0] not in "6789"):
        return {"success": False, "reason": "bad_phonepe",
                "message_telugu": "⚠️ PhonePe number 10 digits undali (ledante khali vadileyandi)"}
    state = (state or "").strip()
    if state not in _STATES:
        return {"success": False, "reason": "bad_state",
                "message_telugu": "⚠️ State select cheyyandi (TS/AP/KA/MH/Other)"}
    district = re.sub(r"\s+", " ", (district or "").strip())[:40]
    if len(district) < 2:
        return {"success": False, "reason": "bad_district",
                "message_telugu": "⚠️ District select/type cheyyandi"}
    pid = _gen_id(name)
    base_url = (site or os.getenv("SITE_URL", "https://manavivaha.in")).rstrip("/")
    p = {"partner_id": pid, "name": name, "full_name": name, "phone": phone,
         "phonepe": phonepe_d or phone, "address": (address or "").strip()[:200],
         "state": state, "district": district,
         "referral_code": pid, "link": f"{base_url}/r/{pid}",
         "created_at": _now(), "clicks": 0, "wallet": 0,
         "referral_stats": {"clicks": 0, "registrations": 0, "total": 0, "paid_count": 0,
                            "wallet": 0, "lifetime_earned": 0, "pending_payout": 0,
                            "paid_out": 0, "ledger": [], "flags": []}}
    PARTNERS.append(p)
    _save()
    _csv_append(p)
    return {"success": True, "partner_id": pid, "link": p["link"],
            "message_telugu": f"🎉 Partner ID ready: {pid} — ee link share cheyyandi, prathi payment ki ₹50!"}


def record_click(pid: str) -> None:
    p = get_partner(pid)
    if p:
        p["clicks"] = int(p.get("clicks", 0)) + 1
        p.get("referral_stats", {})["clicks"] = p["clicks"]
        _save()


def partner_public(pid: str, users: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """Partner dashboard: link + joins + earnings (masked phones)."""
    p = get_partner(pid)
    if not p:
        return {"success": False, "reason": "not_found",
                "message_telugu": "⚠️ Partner ID dorakaledu"}
    st = p.get("referral_stats", {})
    _ledger = st.get("ledger", []) or []
    _paid_ids = {l.get("from") for l in _ledger if l.get("type") == "commission" and l.get("from")}
    joins = []
    if users is not None:
        for u in users:
            if str(u.get("referred_by", "")).lower() == p["partner_id"].lower():
                _comm = round(sum(float(l.get("amount", 0) or 0) for l in _ledger
                                  if l.get("type") == "commission" and l.get("from") == u.get("tsap_id")), 2)
                joins.append({"tsap_id": u.get("tsap_id", ""),
                              "name": u.get("full_name") or u.get("name", ""),
                              "at": u.get("referred_at", ""),
                              # has_paid flag + ledger fallback (pata data ki kuda correct)
                              "paid": bool(u.get("has_paid", False)) or u.get("tsap_id") in _paid_ids,
                              "commission": _comm})
    return {"success": True, "partner_id": p["partner_id"], "name": p["name"],
            "link": p.get("link", ""), "clicks": p.get("clicks", 0),
            "registrations": st.get("registrations", 0), "paid_count": st.get("paid_count", 0),
            "wallet": st.get("wallet", 0), "lifetime_earned": st.get("lifetime_earned", 0),
            "pending_payout": st.get("pending_payout", 0), "paid_out": st.get("paid_out", 0),
            "joins": joins[-50:]}


def admin_report(users: List[Dict]) -> Dict[str, Any]:
    """Admin: evariki entha ravali + evari referral lo evaru (partners + users)."""
    rows = []
    for p in PARTNERS:
        st = p.get("referral_stats", {})
        who = [u.get("tsap_id", "") for u in users
               if str(u.get("referred_by", "")).lower() == p["partner_id"].lower()]
        rows.append({"kind": "partner", "id": p["partner_id"], "name": p["name"],
                     "phone_masked": (p.get("phone", "")[:2] + "••••••" + p.get("phone", "")[-2:]) if p.get("phone") else "",
                     "phonepe": p.get("phonepe", ""), "state": p.get("state", ""),
                     "district": p.get("district", ""), "registrations": st.get("registrations", 0),
                     "paid_count": st.get("paid_count", 0), "wallet": st.get("wallet", 0),
                     "lifetime_earned": st.get("lifetime_earned", 0),
                     "pending_payout": st.get("pending_payout", 0), "paid_out": st.get("paid_out", 0),
                     "joined_ids": who})
    for u in (users or []):
        st = u.get("referral_stats") or {}
        if st.get("registrations", 0) or st.get("wallet", 0):
            who = [x.get("tsap_id", "") for x in users
                   if str(x.get("referred_by", "")).upper() == str(u.get("referral_code", "")).upper()]
            rows.append({"kind": "user", "id": u.get("tsap_id", ""), "name": u.get("full_name", ""),
                         "phone_masked": "", "phonepe": "", "state": u.get("state", ""),
                         "district": u.get("district", ""), "registrations": st.get("registrations", 0),
                         "paid_count": st.get("paid_count", 0), "wallet": st.get("wallet", 0),
                         "lifetime_earned": st.get("lifetime_earned", 0),
                         "pending_payout": st.get("pending_payout", 0), "paid_out": st.get("paid_out", 0),
                         "joined_ids": who})
    rows.sort(key=lambda r: (r["lifetime_earned"], r["registrations"]), reverse=True)
    return {"success": True, "count": len(rows), "rows": rows,
            "total_wallet": round(sum(float(r["wallet"] or 0) for r in rows), 2),
            "total_earned": round(sum(float(r["lifetime_earned"] or 0) for r in rows), 2)}


_load()
