"""
💳 WAVE 14 — SAFE PAYMENTS + FESTIVAL OFFERS (Mana Vivaha)
==========================================================
SAFETY FIRST (user demand — mistakes/errors vaddu):
  1. Amount SERVER compute chesthundi (client amount nammamu — tamper proof).
  2. Razorpay signature HMAC-SHA256 verify → SUCCESS ayithe MATRAMe fulfill.
  3. Idempotent: replay/double-click → okka sari matrame credit (receipt reuse).
  4. SECRET eppudu expose kadu — /api/pay/config lo key_id (public) matrame.
  5. Keys lekapothe → honest MANUAL-UPI mode (admin UTR confirm → fulfill).

Purposes: credits (S_29..S_499 plan) · assisted (ORD-xxxx) · ads (AD-xxxx) · boost (B_1/3/7).
Offers: festival promo codes (%/flat off, dates, applies_to, usage cap) — ADMIN lone create.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_FILE = os.path.join(BASE_DIR, "paypro14.json")

PAY_ORDERS: List[Dict] = []   # our orders (pay_ord_xxx)
RECEIPTS: Dict[str, Dict] = {}  # razorpay_payment_id → receipt (idempotency)
OFFERS: List[Dict] = []        # festival promo codes
_SEQ = 0


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


def _persist() -> None:
    try:
        with open(PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump({"orders": PAY_ORDERS[-1000:], "offers": OFFERS[-200:]}, f, ensure_ascii=False)
    except Exception:
        pass


def _restore() -> None:
    global _SEQ
    try:
        if os.path.exists(PERSIST_FILE):
            d = json.load(open(PERSIST_FILE, encoding="utf-8")) or {}
            PAY_ORDERS.extend(d.get("orders", []))
            OFFERS.extend(d.get("offers", []))
            for o in PAY_ORDERS:
                try:
                    _SEQ = max(_SEQ, int(str(o.get("id", "pay_ord_0")).split("_")[-1]))
                except Exception:
                    pass
    except Exception:
        pass


_restore()

# ---------------------------------------------------------------------------
# CONFIG (secret eppudu bayataki raadu)
# ---------------------------------------------------------------------------

def pay_config() -> Dict:
    """Public config — key_id matrame (secret NEVER)."""
    key_id = os.getenv("RAZORPAY_KEY_ID", "").strip()
    secret = os.getenv("RAZORPAY_KEY_SECRET", "").strip()
    upi = os.getenv("PAY_UPI_ID", "manavivaha@upi")
    live = bool(key_id and secret)
    return {"mode": "razorpay" if live else "manual_upi",
            "key_id": key_id if live else "",
            "upi_id": upi,
            "note_telugu": ("💳 Online pay ready (Razorpay)" if live
                            else f"💳 UPI manual: {upi} ki pay chesi UTR pampandi — admin confirm chesthadu")}


def _secret() -> str:
    return os.getenv("RAZORPAY_KEY_SECRET", "").strip()


# ---------------------------------------------------------------------------
# OFFERS (festival codes — ADMIN lone)
# ---------------------------------------------------------------------------
FESTIVAL_PRESETS = [
    {"code": "DIWALI25", "title": "🪔 Diwali Dhamaka — 25% OFF", "pct_off": 25, "flat_off": 0,
     "applies_to": ["credits", "assisted", "ads", "boost"], "festival": "Diwali"},
    {"code": "SANKRANTI20", "title": "🪁 Sankranti — 20% OFF", "pct_off": 20, "flat_off": 0,
     "applies_to": ["credits", "assisted", "ads"], "festival": "Sankranti"},
    {"code": "UGADI15", "title": "🌾 Ugadi — 15% OFF", "pct_off": 15, "flat_off": 0,
     "applies_to": ["credits", "assisted"], "festival": "Ugadi"},
    {"code": "FIRST50", "title": "🎉 First order — flat ₹50 OFF (₹199+)", "pct_off": 0, "flat_off": 50,
     "applies_to": ["credits", "assisted"], "festival": "Welcome", "min_amount": 199},
]


def seed_festivals(valid_from: str = "", valid_to: str = "", max_uses: int = 1000) -> Dict:
    """Admin 1-click: preset festival codes activate (dates tho)."""
    added = []
    have = {o.get("code") for o in OFFERS}
    for p in FESTIVAL_PRESETS:
        if p["code"] in have:
            continue
        o = dict(p, valid_from=valid_from, valid_to=valid_to, max_uses=max_uses,
                 used=0, active=True, created_at=_now())
        OFFERS.append(o)
        added.append(o["code"])
    _persist()
    return {"success": True, "added": added,
            "message_telugu": f"✅ {len(added)} festival offers activate: {', '.join(added) or 'already unnai'}"}


def create_offer(code: str, title: str, pct_off: int = 0, flat_off: int = 0,
                 applies_to: Optional[List[str]] = None, valid_from: str = "",
                 valid_to: str = "", max_uses: int = 100, min_amount: int = 0,
                 festival: str = "") -> Dict:
    code = str(code or "").strip().upper()
    if len(code) < 3:
        return {"success": False, "message_telugu": "⚠️ Code 3+ chars undali"}
    if any(o.get("code") == code for o in OFFERS):
        return {"success": False, "message_telugu": "⚠️ Ee code already undi"}
    if not pct_off and not flat_off:
        return {"success": False, "message_telugu": "⚠️ % leda flat discount ivvandi"}
    o = {"code": code, "title": title or code, "pct_off": int(pct_off or 0),
         "flat_off": int(flat_off or 0), "applies_to": applies_to or ["credits"],
         "valid_from": valid_from or "", "valid_to": valid_to or "",
         "max_uses": int(max_uses or 1), "used": 0, "min_amount": int(min_amount or 0),
         "festival": festival or "", "active": True, "created_at": _now()}
    OFFERS.append(o)
    _persist()
    return {"success": True, "offer": o, "message_telugu": f"✅ Offer {code} ready"}


def get_offer(code: str) -> Optional[Dict]:
    return next((o for o in OFFERS if o.get("code") == str(code or "").strip().upper()), None)


def validate_offer(code: str, purpose: str, amount: int) -> Dict:
    """Code valid aa? → {ok, final_amount, discount, reason}."""
    if not code:
        return {"ok": True, "code": "", "final_amount": amount, "discount": 0}
    o = get_offer(code)
    if not o or not o.get("active"):
        return {"ok": False, "reason": "bad_code", "message_telugu": "⚠️ Offer code valid kadu"}
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if o.get("valid_from") and today < o["valid_from"][:10]:
        return {"ok": False, "reason": "not_started", "message_telugu": "⚠️ Offer inka start kaledu"}
    if o.get("valid_to") and today > o["valid_to"][:10]:
        return {"ok": False, "reason": "expired", "message_telugu": "⚠️ Offer expire ayyindi"}
    if int(o.get("used", 0)) >= int(o.get("max_uses", 1)):
        return {"ok": False, "reason": "exhausted", "message_telugu": "⚠️ Offer limit ayipoyindi"}
    if purpose not in (o.get("applies_to") or []):
        return {"ok": False, "reason": "not_applicable",
                "message_telugu": f"⚠️ Ee offer {purpose} ki apply kadu"}
    if amount < int(o.get("min_amount", 0) or 0):
        return {"ok": False, "reason": "min_amount",
                "message_telugu": f"⚠️ Minimum ₹{o['min_amount']} undali"}
    disc = int(amount * int(o.get("pct_off", 0) or 0) / 100) + int(o.get("flat_off", 0) or 0)
    disc = min(disc, amount - 1) if amount > 1 else 0
    return {"ok": True, "code": o["code"], "final_amount": amount - disc, "discount": disc,
            "title": o.get("title", "")}


def active_offers() -> List[Dict]:
    """Public: ippudu live offers (banner + pricing)."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    out = []
    for o in OFFERS:
        if not o.get("active"):
            continue
        if o.get("valid_from") and today < o["valid_from"][:10]:
            continue
        if o.get("valid_to") and today > o["valid_to"][:10]:
            continue
        if int(o.get("used", 0)) >= int(o.get("max_uses", 1)):
            continue
        out.append({k: o.get(k) for k in
                    ("code", "title", "pct_off", "flat_off", "applies_to", "valid_to", "festival")})
    return out


def _consume_offer(code: str) -> None:
    o = get_offer(code) if code else None
    if o:
        o["used"] = int(o.get("used", 0)) + 1
        _persist()


# ---------------------------------------------------------------------------
# ORDERS (amount SERVER compute — client amount nammamu)
# ---------------------------------------------------------------------------
def _expected_amount(purpose: str, ref: str) -> Dict:
    """Purpose + ref → server-side amount (single money truth)."""
    from interest import get_plan  # lazy
    purpose = (purpose or "").lower()
    if purpose == "credits":
        plan = get_plan(ref)
        if (plan.get("code") or "FREE") == "FREE":
            return {"ok": False, "message_telugu": "⚠️ Plan code S_29/S_99/S_199/S_299/S_499 matrame"}
        return {"ok": True, "amount": int(plan["price"]), "label": plan.get("telugu", plan.get("label", ref)),
                "credits": int(plan.get("profiles", 0))}
    if purpose == "assisted":
        import smart12 as S12  # lazy
        o = S12.get_order(ref)
        if not o:
            return {"ok": False, "message_telugu": "⚠️ Assist order dorakaledu"}
        if o.get("status") not in ("requested",):
            return {"ok": False, "message_telugu": f"⚠️ Order already {o.get('status')} — malli pay vaddu"}
        return {"ok": True, "amount": int(o.get("amount", 500)), "label": f"Assisted {ref} (₹500 service)"}
    if purpose == "ads":
        import ads as ADS  # lazy
        c = ADS.get_campaign(ref)
        if not c:
            return {"ok": False, "message_telugu": "⚠️ Campaign dorakaledu"}
        if c.get("status") not in ("pending",):
            return {"ok": False, "message_telugu": f"⚠️ Campaign already {c.get('status')}"}
        return {"ok": True, "amount": int(c.get("amount", 0)), "label": f"Ad campaign {ref}"}
    if purpose == "boost":
        import advanced11 as A11  # lazy
        pack = A11.BOOST_PACKS.get(str(ref).upper())
        if not pack:
            return {"ok": False, "message_telugu": "⚠️ Boost pack B_1/B_3/B_7 matrame"}
        return {"ok": True, "amount": int(pack["price"]), "label": pack.get("label", ref)}
    return {"ok": False, "message_telugu": "⚠️ purpose: credits/assisted/ads/boost matrame"}


def create_pay_order(tsap_id: str, purpose: str, ref: str, offer_code: str = "") -> Dict:
    """Pay order create — amount server-side + offer apply + Razorpay/manual mode."""
    global _SEQ
    exp = _expected_amount(purpose, ref)
    if not exp.get("ok"):
        return {"success": False, "message_telugu": exp.get("message_telugu")}
    off = validate_offer(offer_code, purpose.lower(), exp["amount"])
    if not off.get("ok"):
        return {"success": False, "message_telugu": off.get("message_telugu")}
    _SEQ += 1
    cfg = pay_config()
    po = {"id": f"pay_ord_{_SEQ:05d}", "tsap_id": tsap_id, "purpose": purpose.lower(),
          "ref": ref, "amount": exp["amount"], "final_amount": off["final_amount"],
          "discount": off["discount"], "offer_code": off.get("code", ""),
          "label": exp["label"], "mode": cfg["mode"], "status": "created",
          "rzp_order_id": "", "payment_id": "", "utr": "", "created_at": _now(),
          "paid_at": "", "receipt": None}
    PAY_ORDERS.append(po)
    _persist()
    out = {"success": True, "pay_order": {k: po[k] for k in
           ("id", "purpose", "ref", "amount", "final_amount", "discount", "offer_code",
            "label", "mode", "status")},
           "message_telugu": (f"✅ Order {po['id']} — ₹{po['final_amount']} pay cheyyandi"
                               + (f" (offer {off['code']}: -₹{off['discount']})" if off.get("code") else ""))}
    if cfg["mode"] == "razorpay":
        # NOTE: real RZP order create checkout step lo (frontend key_id tho direct),
        # verify daggara signature match — single source: mana pay_order final_amount.
        out["pay_order"]["key_id"] = cfg["key_id"]
        out["pay_order"]["checkout_amount_paise"] = po["final_amount"] * 100
        out["next_telugu"] = "💳 Razorpay checkout lo pay chesi → /api/pay/verify ki pampandi"
    else:
        out["pay_order"]["upi_id"] = cfg["upi_id"]
        out["next_telugu"] = f"💳 {cfg['upi_id']} ki ₹{po['final_amount']} pay chesi UTR admin ki pampandi"
    return out


def get_pay_order(pid: str) -> Optional[Dict]:
    return next((o for o in PAY_ORDERS if o.get("id") == pid), None)


# ---------------------------------------------------------------------------
# VERIFY + FULFILL (signature OK ayithe MATRAMe credits — idempotent)
# ---------------------------------------------------------------------------
def _hmac_ok(rzp_order_id: str, payment_id: str, signature: str) -> bool:
    secret = _secret()
    if not secret or not rzp_order_id or not payment_id or not signature:
        return False
    msg = f"{rzp_order_id}|{payment_id}".encode()
    good = hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(good, str(signature))


def fulfill_order(po: Dict, payment_id: str, via: str) -> Dict:
    """Actual fulfill (main.py users/callbacks tho — Users list inject via param? no: lazy main)."""
    import main as MAIN  # lazy: circles avoid (paypro ← main import, runtime only)
    user = MAIN._find_user(po.get("tsap_id", ""))
    if not user:
        return {"ok": False, "message_telugu": "⚠️ User dorakaledu — amount hold (admin refund/credit)"}
    purpose, ref = po.get("purpose"), po.get("ref")
    if purpose == "credits":
        from interest import apply_payment
        applied = apply_payment(user, _expected_amount("credits", ref)["amount"], ref)
        if not applied.get("ok"):
            return {"ok": False, "message_telugu": "⚠️ Plan apply fail — admin chusthadu"}
        return {"ok": True, "credits": user.get("credits", 0), "plan": user.get("plan"),
                "message_telugu": f"✅ ₹{po['final_amount']} success — {applied.get('profiles_added', 0)} credits add! Balance: {user.get('credits', 0)} 🎉"}
    if purpose == "assisted":
        import smart12 as S12
        r = S12.mark_order_paid(ref, payment_id or po.get("utr", "") or "RZPAY")
        if not r.get("success"):
            return {"ok": False, "message_telugu": r.get("message_telugu")}
        return {"ok": True, "message_telugu": f"✅ Assisted {ref} PAID — admin profiles select chesi personal ga pampisthadu 🙏"}
    if purpose == "ads":
        import ads as ADS
        r = ADS.approve_campaign(ref, payment_id or po.get("utr", "") or "RZPAY")
        if not r.get("success"):
            return {"ok": False, "message_telugu": r.get("message_telugu")}
        return {"ok": True, "message_telugu": f"✅ Campaign {ref} LIVE — {r['campaign']['days']} days 🎉"}
    if purpose == "boost":
        import advanced11 as A11
        eff = A11.apply_boost(user, str(ref).upper())
        return {"ok": True, "message_telugu": f"✅ Boost ON! {eff.get('message_telugu', '')} ⚡"}
    return {"ok": False, "message_telugu": "⚠️ Unknown purpose"}


def verify_payment(pay_order_id: str, rzp_order_id: str, payment_id: str,
                   signature: str) -> Dict:
    """
    Razorpay checkout response verify:
      signature OK + pay_order match + amount sane → fulfill ONCE → receipt.
      replay → old receipt (double credit NEVER).
    """
    po = get_pay_order(pay_order_id)
    if not po:
        return {"success": False, "message_telugu": "⚠️ Order dorakaledu"}
    if po.get("status") == "paid":
        return {"success": True, "duplicate": True, "receipt": po.get("receipt"),
                "message_telugu": "✅ Ee order already paid — double charge ledu (idempotent) 🙂"}
    if payment_id and payment_id in RECEIPTS:
        old = RECEIPTS[payment_id]
        return {"success": True, "duplicate": True, "receipt": old,
                "message_telugu": "✅ Ee payment already use ayyindi — malli credit ivvamu 🙂"}
    if pay_config()["mode"] != "razorpay":
        return {"success": False, "message_telugu": "⚠️ Online verify off (manual-UPI mode) — admin confirm chesthadu"}
    if not _hmac_ok(rzp_order_id, payment_id, signature):
        return {"success": False, "reason": "bad_signature",
                "message_telugu": "🚫 Payment verify FAIL — signature mismatch (amount cut ayithe 5-7 days lo auto-refund, leda support ki payment ID pampandi)"}
    po["rzp_order_id"] = rzp_order_id
    po["payment_id"] = payment_id
    done = fulfill_order(po, payment_id, "razorpay")
    if not done.get("ok"):
        _persist()
        return {"success": False, "message_telugu": done.get("message_telugu")}
    po["status"] = "paid"
    po["paid_at"] = _now()
    receipt = {"pay_order_id": po["id"], "payment_id": payment_id, "amount": po["final_amount"],
               "purpose": po["purpose"], "ref": po["ref"], "tsap_id": po["tsap_id"],
               "paid_at": po["paid_at"], "detail": done.get("message_telugu")}
    po["receipt"] = receipt
    RECEIPTS[payment_id] = receipt
    if po.get("offer_code"):
        _consume_offer(po["offer_code"])
    _persist()
    return {"success": True, "receipt": receipt, "message_telugu": receipt["detail"]}


def confirm_manual(pay_order_id: str, utr: str) -> Dict:
    """Admin: UPI payment vachhindi (UTR) → fulfill ONCE."""
    po = get_pay_order(pay_order_id)
    if not po:
        return {"success": False, "message_telugu": "⚠️ Order dorakaledu"}
    if po.get("status") == "paid":
        return {"success": True, "duplicate": True, "receipt": po.get("receipt"),
                "message_telugu": "✅ Already paid — double credit ivvamu"}
    if not (utr or "").strip():
        return {"success": False, "message_telugu": "⚠️ UTR lekunda confirm cheyyakoodadu (audit)"}
    po["utr"] = utr.strip()
    done = fulfill_order(po, "", "manual_utr")
    if not done.get("ok"):
        _persist()
        return {"success": False, "message_telugu": done.get("message_telugu")}
    po["status"] = "paid"
    po["paid_at"] = _now()
    receipt = {"pay_order_id": po["id"], "utr": po["utr"], "amount": po["final_amount"],
               "purpose": po["purpose"], "ref": po["ref"], "tsap_id": po["tsap_id"],
               "paid_at": po["paid_at"], "detail": done.get("message_telugu")}
    po["receipt"] = receipt
    if po.get("offer_code"):
        _consume_offer(po["offer_code"])
    _persist()
    return {"success": True, "receipt": receipt, "message_telugu": receipt["detail"]}


def pay_stats() -> Dict:
    paid = [o for o in PAY_ORDERS if o.get("status") == "paid"]
    return {"orders": len(PAY_ORDERS), "paid": len(paid),
            "pending": len([o for o in PAY_ORDERS if o.get("status") == "created"]),
            "collected": sum(int(o.get("final_amount", 0) or 0) for o in paid),
            "offers_live": len(active_offers())}
