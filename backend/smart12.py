"""
🔒 WAVE 12 — SMART REVEAL ENGINE (Mana Vivaha)
==============================================
User demand (100% workable, top sites kanna advanced):

  1. Channel post lo NUMBER ❌ FULL-NAME ❌ SURNAME ❌ — masked teaser matrame.
     Number kosam → manalni contact / premium kattali.
  2. CREDITS model: credits tho number reveal; ayipothe malli pay.
  3. ₹500 assisted service: admin panel lo buyer ID → perfect matches load →
     filters → select → 📩 Telegram / 💬 WhatsApp personal send.
  4. STRICT entitlement: pampina profiles mathrame reveal — extra emi kadu.
  5. 📋 Copy-list: `NAME -- NUMBER` admin 1-click copy (manual paste kosam).

Design (emi break avvakunda):
  • Pure functions + in-memory stores (repo convention: DB_USERS lanti lists).
  • JSON persist (unlocks12.json) — restart ayina entitlements/orders potavu.
  • Public outputs (caption / bot card / copy-preview) lo number eppudu ledu —
    full number ONLY: POST /api/unlock (logged) + admin copy-list + paid DM.
"""
from __future__ import annotations

import json
import os
import re
import threading
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

# NOTE: channels_config import LAZY (cycle avoid) — functions lopala import.

PHONE_RE = re.compile(r"(?<![\d•])[6-9]\d{9}(?!\d)")

ASSISTED_PRICE = 500          # ₹500 assisted match service
ASSISTED_DEFAULT_COUNT = 5    # default ga 5 profiles personal ga
UNLOCK_CREDITS = 1            # self-service: 1 credit = 1 number reveal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_FILE = os.path.join(BASE_DIR, "unlocks12.json")

# ---------------------------------------------------------------------------
# STORES (in-memory + JSON persist)
# ---------------------------------------------------------------------------
# viewer_id -> {target_id: {"via": "credit"|"assisted"|"admin_gift"|"interest",
#                           "at": iso, "credits_charged": n, "order_id": str}}
UNLOCKS: Dict[str, Dict[str, Dict]] = {}
REVEAL_LOG: List[Dict] = []     # audit: evaru, e number, eppudu, ela
ORDERS: List[Dict] = []         # ₹500 assisted orders
_ORDER_SEQ = 0


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


def _persist() -> None:
    try:
        with open(PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump({"unlocks": UNLOCKS, "orders": ORDERS,
                       "reveal_log": REVEAL_LOG[-500:]}, f, ensure_ascii=False)
    except Exception:
        pass  # persist fail ayina memory flow aagadu


def _restore() -> None:
    global _ORDER_SEQ
    try:
        if not os.path.exists(PERSIST_FILE):
            return
        with open(PERSIST_FILE, encoding="utf-8") as f:
            data = json.load(f) or {}
        UNLOCKS.update(data.get("unlocks", {}))
        ORDERS.extend(data.get("orders", []))
        REVEAL_LOG.extend(data.get("reveal_log", []))
        for o in ORDERS:
            try:
                n = int(str(o.get("id", "ORD-0")).split("-")[-1])
                _ORDER_SEQ = max(_ORDER_SEQ, n)
            except Exception:
                pass
    except Exception:
        pass


_restore()

# ---------------------------------------------------------------------------
# 1. MASKING — name/surname/number public ga eppudu ledu
# ---------------------------------------------------------------------------

def mask_word(word: str) -> str:
    """Lakshmi → L•••••i · Raju → R•••u · T → T (too short, as-is)."""
    w = str(word or "").strip()
    if len(w) <= 2:
        return w
    return w[0] + "•" * (len(w) - 2) + w[-1]


def mask_name(full_name: str) -> str:
    """
    Full name + surname rendu mask:
      'Lakshmi Reddy' → 'L•••••i R•••y'
    Channel post / bot card / public search — anni chotla ide.
    """
    parts = str(full_name or "").strip().split()
    if not parts:
        return "—"
    return " ".join(mask_word(p) for p in parts)


def first_masked(full_name: str) -> str:
    """Copy-list personal DM kosam: 'Lakshmi R.' — admin/paid mathrame."""
    parts = str(full_name or "").strip().split()
    if not parts:
        return "—"
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} {parts[-1][0]}."


def mask_phone(phone: str) -> str:
    """9848012345 → 98••••••45 (interest.py tho same format)."""
    d = "".join(ch for ch in str(phone or "") if ch.isdigit())
    if len(d) < 4:
        return "🔒 •••••"
    return d[:2] + "•" * max(0, len(d) - 4) + d[-2:]


def assert_no_leak(text: str) -> Dict:
    """Public text lo number leak check (tests + safety net)."""
    found = PHONE_RE.findall(text or "")
    return {"ok": not found, "leaked": found[:3]}


# ---------------------------------------------------------------------------
# 2. MASKED CHANNEL CAPTIONS (number ❌ name ❌ surname ❌)
# ---------------------------------------------------------------------------

def build_masked_caption(profile: Dict, tsap_id: str = "TSAP-F-2025-XXXX",
                         score: int = 92) -> str:
    """📢 Telegram channel post v2 — teaser matrame + unlock CTA."""
    from channels_config import route_profile, BOT_USERNAME, SITE  # lazy: cycle safe
    r = route_profile(profile or {})
    reasons = "\n".join(f"• {x['telugu']}" for x in r["reasons"][:4])
    g = profile.get("gender", "")
    icon = "👰" if g == "Bride" else ("🤵" if g == "Groom" else "💍")
    return (
        f"🆔 {tsap_id} | ⭐ {score}% BEST MATCH\n"
        f"{icon} {first_name_of(profile.get('full_name', ''))} • {profile.get('age', '—')}y • "
        f"{profile.get('height', '—')} • {profile.get('caste', '—')}\n"
        f"🎓 {profile.get('education', '—')} • 💼 {profile.get('job', '—')} • "
        f"📍 {profile.get('district', '—')}\n"
        f"🌟 {profile.get('gothram', '—')} gothram • {profile.get('star', '—')} nakshatram\n"
        f"\n✅ Enduku set avutharu:\n{reasons}\n"
        f"\n{r['hashtags']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔒 Number lock lo undi — unlock cheyyandi:\n"
        f"🤖 Bot: {BOT_USERNAME} → /unlock {tsap_id} (1 credit)\n"
        f"🔍 Full profile: {SITE}/search/{tsap_id}\n"
        f"📝 Register 3 min lo: {SITE}/register\n"
        f"⚠️ Mosam jagratha — advance money evariki ivvakandi!"
    )


def build_masked_whatsapp(profile: Dict, tsap_id: str = "TSAP-F-2025-XXXX",
                          score: int = 92) -> str:
    """💬 WhatsApp channel/group post v2 (*bold* format, masked)."""
    from channels_config import route_profile, BOT_USERNAME, SITE  # lazy
    r = route_profile(profile or {})
    reasons = "\n".join(f"✅ {x['telugu']}" for x in r["reasons"][:3])
    return (
        f"💍 *MANA VIVAHA* — TS-AP Telugu Matrimony\n"
        f"🆔 *{tsap_id}*  |  ⭐ *{score}% BEST MATCH*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 *{first_name_of(profile.get('full_name', ''))}* ({profile.get('age', '—')} yrs)\n"
        f"📍 {profile.get('district', '—')}, {profile.get('state', 'TS')}\n"
        f"💍 Caste: {profile.get('caste', '—')}  |  Gothram: {profile.get('gothram', '—')}\n"
        f"🎓 {profile.get('education', '—')}  |  💼 {profile.get('job', '—')}\n"
        f"🌟 Star: {profile.get('star', '—')}  |  Rasi: {profile.get('rasi', '—')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"*Enduku best match:*\n{reasons}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"{r['hashtags']}\n"
        f"🔒 Number lock — bot lo /unlock {tsap_id} (1 credit)\n"
        f"🔍 Profile: {SITE}/search/{tsap_id}\n"
        f"🤖 Bot: {BOT_USERNAME}  •  ⚠️ Advance money adigithe report cheyyandi"
    )


# ---------------------------------------------------------------------------
# 3. ENTITLEMENTS — evariki, e profiles, eppudu (STRICT: sent-vi mathrame)
# ---------------------------------------------------------------------------

def is_entitled(viewer_id: str, target_id: str) -> bool:
    return target_id in UNLOCKS.get(viewer_id or "", {})


def grant_unlock(viewer_id: str, target_id: str, via: str = "admin_gift",
                 order_id: str = "", credits_charged: int = 0) -> Dict:
    """Admin/assisted grant — credit cut ledu, entitlement matrame."""
    box = UNLOCKS.setdefault(viewer_id, {})
    first = target_id not in box
    box[target_id] = {"via": via, "at": _now_iso(), "order_id": order_id,
                      "credits_charged": credits_charged}
    _persist()
    return {"viewer_id": viewer_id, "target_id": target_id, "via": via,
            "first_time": first}


_UNLOCK_LOCKS: Dict[str, threading.Lock] = defaultdict(threading.Lock)


def unlock_number(viewer: Dict, target: Dict) -> Dict:
    """
    Self-service reveal:
      entitled ayithe → FREE reveal (already paid/granted)
      kakapothe credits > 0 → 1 cut → reveal + entitlement record
      0 credits → paywall
    Full number + audit log — ee function nunchi matrame bayataki vastundi.
    """
    viewer_id = (viewer or {}).get("tsap_id", "")
    target_id = (target or {}).get("tsap_id", "")
    if not viewer_id or not target_id:
        return {"success": False, "reason": "bad_ids",
                "message_telugu": "⚠️ ID sari ledu"}
    if viewer_id == target_id:
        phone = str(target.get("phone", ""))
        return {"success": True, "phone": phone, "phone_masked": mask_phone(phone),
                "charged": 0, "credits_left": viewer.get("credits", 0),
                "via": "self", "message_telugu": "✅ Mee number ye idi 🙂"}
    if is_entitled(viewer_id, target_id):
        phone = str(target.get("phone", ""))
        REVEAL_LOG.append({"viewer": viewer_id, "target": target_id, "via": "entitled",
                           "charged": 0, "at": _now_iso()})
        _persist()
        return {"success": True, "phone": phone, "phone_masked": mask_phone(phone),
                "charged": 0, "credits_left": viewer.get("credits", 0), "via": "entitled",
                "message_telugu": "✅ Already unlocked — malli free ga chupisthunnam"}
    # WAVE 24 DOUBLE-SPEND LOCK: concurrent unlocks same credit ni rendu sarlu kharchu cheyyakudadu.
    with _UNLOCK_LOCKS[viewer_id]:
        credits = int(viewer.get("credits", 0) or 0)
        if credits < UNLOCK_CREDITS:
            return {"success": False, "reason": "no_credits",
                    "phone_masked": mask_phone(target.get("phone", "")),
                    "credits_left": 0,
                    "message_telugu": "⚠️ Credits ayipoyayi! ₹99 = 5 credits (leda ₹500 assisted — mana team meeke perfect 5 profiles pampisthundi). Pay chesi malli try cheyyandi 🙏",
                    "pay_options": [{"label": "₹99 — 5 credits", "credits": 5},
                                    {"label": "₹500 — assisted 5 profiles (personal)", "credits": 0,
                                     "note": "admin pathavi"}]}
        viewer["credits"] = credits - UNLOCK_CREDITS
        grant_unlock(viewer_id, target_id, via="credit", credits_charged=UNLOCK_CREDITS)
        phone = str(target.get("phone", ""))
        REVEAL_LOG.append({"viewer": viewer_id, "target": target_id, "via": "credit",
                           "charged": UNLOCK_CREDITS, "at": _now_iso()})
        _persist()
        return {"success": True, "phone": phone, "phone_masked": mask_phone(phone),
                "charged": UNLOCK_CREDITS, "credits_left": viewer["credits"], "via": "credit",
                "message_telugu": f"✅ Number unlock ayyindi! (1 credit cut — migilindi: {viewer['credits']})"}


def my_unlocks(viewer_id: str, users: List[Dict]) -> Dict:
    """Mee unlocked profiles — MASKED list (full number per-unlock matrame)."""
    box = UNLOCKS.get(viewer_id or "", {})
    by_id = {u.get("tsap_id"): u for u in (users or [])}
    items = []
    for tid, meta in box.items():
        u = by_id.get(tid, {})
        items.append({"tsap_id": tid, "name_masked": first_name_of(u.get("full_name", "")),
                      "age": u.get("age", "—"), "caste": u.get("caste", "—"),
                      "district": u.get("district", "—"),
                      "phone_masked": mask_phone(u.get("phone", "")),
                      "via": meta.get("via"), "unlocked_at": meta.get("at")})
    return {"viewer_id": viewer_id, "count": len(items), "profiles": items}


# ---------------------------------------------------------------------------
# 4. ₹500 ASSISTED ORDERS — pay → attach → personal send
# ---------------------------------------------------------------------------

def create_order(buyer_id: str, amount: int = ASSISTED_PRICE, note: str = "") -> Dict:
    global _ORDER_SEQ
    _ORDER_SEQ += 1
    order = {"id": f"ORD-{_ORDER_SEQ:04d}", "buyer_id": buyer_id, "amount": amount,
             "status": "requested", "utr": "", "profile_ids": [],
             "via": [], "created_at": _now_iso(), "paid_at": "", "delivered_at": "",
             "note": note}
    ORDERS.append(order)
    _persist()
    return order


def get_order(order_id: str) -> Optional[Dict]:
    return next((o for o in ORDERS if o.get("id") == order_id), None)


def mark_order_paid(order_id: str, utr: str) -> Dict:
    o = get_order(order_id)
    if not o:
        return {"success": False, "message_telugu": "⚠️ Order dorakaledu"}
    if not (utr or "").strip():
        return {"success": False,
                "message_telugu": "⚠️ UTR/reference lekunda paid cheyyakoodadu (audit ki)"}
    o["status"] = "paid"
    o["utr"] = utr.strip()
    o["paid_at"] = _now_iso()
    _persist()
    return {"success": True, "order": o,
            "message_telugu": f"✅ {order_id} paid (₹{o['amount']}) — ippudu profiles attach + send cheyochu"}


def attach_order_profiles(order_id: str, profile_ids: List[str]) -> Dict:
    """Paid order ki profiles attach → buyer ki entitlements (STRICT: ivi mathrame)."""
    o = get_order(order_id)
    if not o:
        return {"success": False, "message_telugu": "⚠️ Order dorakaledu"}
    if o["status"] not in ("paid", "delivered"):
        return {"success": False,
                "message_telugu": "⚠️ Mundhu payment (UTR) confirm cheyyandi — appude profiles attach"}
    clean = [p for p in dict.fromkeys(profile_ids or []) if p]
    o["profile_ids"] = clean
    for pid in clean:
        grant_unlock(o["buyer_id"], pid, via="assisted", order_id=order_id)
    _persist()
    return {"success": True, "order_id": order_id, "buyer_id": o["buyer_id"],
            "attached": len(clean),
            "message_telugu": f"✅ {len(clean)} profiles {o['buyer_id']} ki unlock ayyayi (ivi mathrame — extra ledu)"}


# ---------------------------------------------------------------------------
# 5. PERSONAL PACK + COPY-LIST (paid buyer ke — full numbers)
# ---------------------------------------------------------------------------

def build_copy_list(buyer: Dict, targets: List[Dict], order_id: str = "") -> str:
    """
    📋 Admin 1-click copy — `NAME -- NUMBER` lines (manual paste kosam):
      👰 Mee kosam 5 profiles (₹500 paid ✅):
      1. Sravani K. -- 9848012345 (TSAP-F-2042 · Kamma · 26)
    """
    bname = first_masked((buyer or {}).get("full_name", ""))
    lines = [f"💍 Mana Vivaha — {bname} garu, mee kosam {len(targets)} profiles "
             f"(₹{ASSISTED_PRICE} paid ✅{f' · {order_id}' if order_id else ''}):", ""]
    for i, t in enumerate(targets or [], 1):
        icon = "👰" if t.get("gender") == "Bride" else ("🤵" if t.get("gender") == "Groom" else "💍")
        lines.append(f"{i}. {icon} {first_masked(t.get('full_name', ''))} -- "
                     f"{t.get('phone', '—')} ({t.get('tsap_id', '—')} · "
                     f"{t.get('caste', '—')} · {t.get('age', '—')}y · "
                     f"{t.get('district', '—')})")
    lines += ["", "🙏 Nachina vallaki interest pampandi — leda memu matladistham (10AM–7PM).",
              "⚠️ Ee numbers vere vallaki forward cheyyakandi — meekosame unlock chesam."]
    return "\n".join(lines)


def build_personal_card(target: Dict, buyer_name: str = "") -> str:
    """Paid buyer DM card (Telegram/WhatsApp) — full number tho (consent-paid)."""
    t = target or {}
    icon = "👰" if t.get("gender") == "Bride" else ("🤵" if t.get("gender") == "Groom" else "💍")
    g = "Ammayi" if t.get("gender") == "Bride" else ("Abbayi" if t.get("gender") == "Groom" else "")
    return (
        f"{icon} {t.get('tsap_id', '—')} — {first_masked(t.get('full_name', ''))} ({g} {t.get('age', '—')}y)\n"
        f"💍 {t.get('caste', '—')} · {t.get('gothram', '—')} gothram · 🌟 {t.get('star', '—')}\n"
        f"🎓 {t.get('education', '—')} · 💼 {t.get('job', '—')} · 💰 {t.get('salary', '—')}\n"
        f"📍 {t.get('district', '—')}, {t.get('state', 'TS')}\n"
        f"📞 Number: {t.get('phone', '—')}\n"
        f"🔍 Full: /search {t.get('tsap_id', '')}"
    )


def build_personal_pack(buyer: Dict, targets: List[Dict], order_id: str = "") -> List[str]:
    """DM sequence: header + 1 msg per profile (Telegram limit-safe chunks)."""
    bname = first_masked((buyer or {}).get("full_name", ""))
    header = (f"💍 Mana Vivaha — {bname} garu, Namaste! 🙏\n"
              f"₹{ASSISTED_PRICE} payment vachindi ✅ — meekosam handpicked "
              f"{len(targets)} profiles 👇 (numbers meekosame unlock){f' · {order_id}' if order_id else ''}")
    return [header] + [build_personal_card(t, bname) for t in (targets or [])]


# ---------------------------------------------------------------------------
# 6. PERSONAL DELIVERY — Telegram DM + WhatsApp (dry-run safe)
# ---------------------------------------------------------------------------

async def deliver_personal(buyer: Dict, targets: List[Dict], via: str = "both",
                           order_id: str = "") -> Dict:
    """
    Buyer personal Telegram DM + WhatsApp ki profiles.
    Tokens/links lekapothe → dry-run preview (crash ledu, admin copy-list tho pampachu).
    Returns per-target status + copy_list (admin fallback).
    """
    import bot_pool  # lazy
    msgs = build_personal_pack(buyer, targets, order_id)
    copy_list = build_copy_list(buyer, targets, order_id)
    via = (via or "both").lower()
    want_tg = via in ("telegram", "both")
    want_wa = via in ("whatsapp", "both")

    tg = {"wanted": want_tg, "sent": 0, "failed": "", "chat_id": str((buyer or {}).get("telegram_chat_id", "") or "")}
    if want_tg:
        if tg["chat_id"]:
            try:
                pool = bot_pool.get_pool()
                for m in msgs:
                    r = await pool.post(tg["chat_id"], m)
                    if isinstance(r, dict) and (r.get("ok") or r.get("dry_run")):
                        tg["sent"] += 1
                    else:
                        tg["failed"] = str((r or {}).get("error") or r)[:120]
                        break
                if not tg["sent"] and not tg["failed"]:
                    tg["failed"] = "dry_run_no_token"
            except Exception as e:  # noqa: BLE001
                tg["failed"] = type(e).__name__ + ": " + str(e)[:100]
        else:
            tg["failed"] = "no_telegram_chat_id"

    wa = {"wanted": want_wa, "queued": 0, "failed": "",
          "phone": str((buyer or {}).get("phone", "") or "")}
    if want_wa:
        if wa["phone"]:
            try:
                import publisher  # lazy
                cfg = publisher.config()
                if cfg.get("whatsapp_mode", "off") == "off":
                    wa["failed"] = "dry_run_whatsapp_off"
                else:
                    for m in msgs:
                        publisher.enqueue_whatsapp([wa["phone"]], m)
                        wa["queued"] += 1
            except Exception as e:  # noqa: BLE001
                wa["failed"] = type(e).__name__ + ": " + str(e)[:100]
        else:
            wa["failed"] = "no_phone"

    ok = (not want_tg or tg["sent"] == len(msgs)) and (not want_wa or wa["queued"] == len(msgs))
    return {"ok": ok, "via": via, "messages": len(msgs), "telegram": tg, "whatsapp": wa,
            "copy_list": copy_list,
            "message_telugu": ("✅ Personal delivery success" if ok else
                               "🧪 Dry-run/preview — tokens/link ledu, kindi copy-list tho manual ga pampandi")}


# ---------------------------------------------------------------------------
# 7. FIRST-NAME DISPLAY + SAME-SURNAME GUARD (WAVE 13)
# ---------------------------------------------------------------------------
# Public chotla FIRST NAME kanipisthundi (nammakam + privacy balance),
# surname eppudu hidden. Kani backend lo SAME SURNAME ayithe match vaddu
# (okka inti-peru — pelli kudadhu, sampradayam). Gothram guard lanti logic.

def first_name_of(full_name: str) -> str:
    """'Lakshmi Reddy' → 'Lakshmi' — public display (surname hidden)."""
    parts = str(full_name or "").strip().split()
    return parts[0] if parts else "—"


def surname_of(full_name: str) -> str:
    """'Lakshmi Reddy' → 'Reddy' · single-word peru → '' (surname teliyadu)."""
    parts = str(full_name or "").strip().split()
    return parts[-1] if len(parts) >= 2 else ""


def norm_surname(s: str) -> str:
    """Case/space/dot proof: ' Reddy.' → 'reddy'."""
    return "".join(ch for ch in str(s or "").lower() if ch.isalnum())


def same_surname_check(a: Dict, b: Dict) -> Dict:
    """
    Same-surname → blocked (pelli kudadhu).
    Okariki surname lekapothe → block kadu + unknown_side warning (gothram pattern).
    """
    sa = norm_surname(surname_of((a or {}).get("full_name", "")))
    sb = norm_surname(surname_of((b or {}).get("full_name", "")))
    if not sa or not sb:
        missing = "a" if not sa else ("b" if not sb else "both")
        return {"same": False, "blocked": False, "unknown_side": True, "missing": missing,
                "reason": "surname_unknown",
                "verdict_telugu": "⚠️ Okariki inti-peru (surname) ledu — admin/pandit confirm cheyyandi"}
    same = (sa == sb)
    nm = surname_of(a.get("full_name", ""))
    return {"same": same, "blocked": same, "a_surname": nm,
            "b_surname": surname_of(b.get("full_name", "")),
            "reason": "same_surname" if same else "surname_ok",
            "verdict_telugu": ("🚫 Okka inti-peru (%s) — pelli kudadhu (sampradayam). Vere profiles chudandi 🙏" % nm
                               if same else "✅ Inti-peru veru — surname paranga OK")}


def filter_same_surname(me: Dict, pool: list) -> Dict:
    """Pool nunchi same-surname profiles teesey (suggestions/matches kosam)."""
    kept, skipped = [], []
    for u in (pool or []):
        if (u or {}).get("tsap_id") == (me or {}).get("tsap_id"):
            kept.append(u)
            continue
        c = same_surname_check(me, u)
        (skipped if c.get("blocked") else kept).append(u)
    ids = [u.get("tsap_id") for u in skipped]
    return {"kept": kept, "skipped_ids": ids, "skipped_count": len(ids)}
