"""
MANA VIVAHA — WEDDING VENDOR ADS + PROMOTIONS 🏪
================================================
"Pelli sambandham aithey vendor lu kooda vuntaru — catering, photography, decorations...
 vaallaki promotions kooda cheyyali bestga." — advanced vendor ad network.

Enti idi chestundi:
  * 18 vendor categories (Telugu names tho) — catering, photography, decorations, hall, pandit...
  * 4 ad packages (₹499 → ₹3999) + spot ads (₹149/post, ₹499/status blast)
  * Vendor directory (searchable: category + district + rating + verified)
  * Ad rotation (paid-first, weighted, daypart impressions) + impression/click tracking
  * Lead capture → vendor ki instant WhatsApp (name, phone, district, requirement)
  * Telugu promo post generator (Telegram + WhatsApp channel post ready)
  * Promo poster PNG (1080×1080) with QR → wa.me deep link
  * Admin: queue → approve/activate (UTR) → reject → expire, leads, revenue summary

Ee module lo pricing SINGLE SOURCE — maarchi ante ikkade maarchandi (site + docs anni API nunchi).
"""
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

VENDORS_VERSION = "1.0"

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor_state.json")
INR = "₹"

# ---------------------------------------------------------------------------
# CATEGORIES — pelli sambandham related (Telugu + English)
# ---------------------------------------------------------------------------
CATEGORIES: List[Dict] = [
    {"key": "catering", "en": "Catering", "te": "విందు భోజనం (Catering)", "icon": "🍛", "kw": "catering, bojanam, vindu, cooks, tiffin"},
    {"key": "photography", "en": "Photography", "te": "ఫోటోగ్రఫీ", "icon": "📸", "kw": "photos, camera, album, candid, pre-wedding shoot"},
    {"key": "videography", "en": "Videography", "te": "వీడియోగ్రఫీ / Drone", "icon": "🎥", "kw": "video, drone, live streaming, cinematic"},
    {"key": "decorations", "en": "Decorations & Flowers", "te": "అలంకరణ (Decorations) & పూలు", "icon": "🌸", "kw": "mandap, flowers, stage, backdrop, lighting"},
    {"key": "banquet_hall", "en": "Function Hall / Banquet", "te": "ఫంక్షన్ హాల్ / కళ్యాణ మండపం", "icon": "🏛️", "kw": "hall, kalyana mandapam, convention, AC hall"},
    {"key": "tent_house", "en": "Tent House", "te": "టెంట్ హౌస్", "icon": "⛺", "kw": "tent, chairs, shamiana, sound, tables"},
    {"key": "pandit", "en": "Pandit / Priest", "te": "పండితులు (పురోహితులు)", "icon": "🕉️", "kw": "pandit, purohit, muhurtham, puja, homam"},
    {"key": "jewellery", "en": "Jewellery", "te": "బంగారు నగలు (Jewellery)", "icon": "💍", "kw": "gold, jewellery, rings, haram, vaddanam"},
    {"key": "bridal_wear", "en": "Bridal & Groom Wear", "te": "పెళ్లి దుస్తులు (Pattu cheera / Sherwani)", "icon": "👰", "kw": "saree, pattu, sherwani, lehenga, rentals"},
    {"key": "makeup", "en": "Makeup & Beautician", "te": "మేకప్ & బ్యూటీషియన్", "icon": "💄", "kw": "bridal makeup, hairstyle, saree draping"},
    {"key": "mehendi", "en": "Mehendi / Mehndi Artist", "te": "గోరింటాకు (Mehendi)", "icon": "🌿", "kw": "mehendi, henna, gorintaku, bridal mehendi"},
    {"key": "music_dj", "en": "DJ & Band (Melam / Band)", "te": "DJ, బ్యాండ్, మేళం", "icon": "🎶", "kw": "dj, band, melam, nadaswaram, sannai"},
    {"key": "invitations", "en": "Invitations & Printing", "te": "పిల్లి కార్డు / Printing", "icon": "✉️", "kw": "invitation, cards, printing, e-invite, video invite"},
    {"key": "cars_travel", "en": "Cars & Travel", "te": "కార్లు & ట్రావెల్స్", "icon": "🚗", "kw": "car, luxury car, travel, bus, airport pick"},
    {"key": "wedding_planner", "en": "Wedding Planner / Event", "te": "వెడ్డింగ్ ప్లానర్", "icon": "📋", "kw": "planner, event management, coordinator, complete package"},
    {"key": "bakery_cake", "en": "Bakery & Cake", "te": "కేక్ & బేకరీ", "icon": "🎂", "kw": "cake, bakery, sweets, laddu, ariselu"},
    {"key": "gifts_hampers", "en": "Gifts & Hampers", "te": "గిఫ్ట్‌లు & హ్యాంపర్స్", "icon": "🎁", "kw": "gifts, hampers, sai panam, dry fruits"},
    {"key": "honeymoon_travel", "en": "Honeymoon Packages", "te": "హనీమూన్ ప్యాకేజీలు", "icon": "✈️", "kw": "honeymoon, tour, package, resort, visa"},
]

CATEGORY_MAP = {c["key"]: c for c in CATEGORIES}


def category_label(key: str) -> Dict:
    return CATEGORY_MAP.get(key, {"key": key, "en": key.replace("_", " ").title(), "te": key, "icon": "🏪"})


# ---------------------------------------------------------------------------
# AD PACKAGES — SINGLE SOURCE (₹)
# ---------------------------------------------------------------------------
PACKAGES: List[Dict] = [
    {
        "code": "V_SINGLE_POST", "name": "Single Channel Post", "price": 149, "days": 1,
        "telugu": "ఒక్క channel post (₹149) — test cheyyadaniki",
        "perks": ["1 Telegram post (mirror channel)", "Mee city + category mention", "Report: views + enquiries"],
        "best_for": "Chinna offer / trial",
    },
    {
        "code": "V_BASIC", "name": "Basic Listing", "price": 499, "days": 30,
        "telugu": "డైరెక్టరీ లిస్టింగ్ — మీ category లో కనిపిస్తారు",
        "perks": ["1 category directory listing (30 days)", "Website lo verified-free badge",
                  "1 Telegram promo post (mee caste/region channel)", "Call/WhatsApp CTA on listing"],
        "best_for": "Kotha business — modati publicity",
    },
    {
        "code": "V_STATUS_BLAST", "name": "WhatsApp Status Blast", "price": 499, "days": 1,
        "telugu": "మా WhatsApp status/గ్రూప్‌లలో మీ promo (₹499)",
        "perks": ["Mana 3 status lanes lo promo (anti-ban safe order lo)", "1 Telegram post bonus",
                  "Enquiries direct mee WhatsApp ki"],
        "best_for": "Short notice / festival offer",
    },
    {
        "code": "V_SPOTLIGHT", "name": "Spotlight (7 days)", "price": 999, "days": 7,
        "telugu": "పెళ్లి సీజన్ spotlight — 7 రోజులు top banner + status",
        "perks": ["Top banner rotation (7 days, all pages)", "1 WhatsApp status blast (all our status lanes)",
                  "1 Telegram post (4 main channels)", "Urgent season offer ki best"],
        "best_for": "Fast season push (Padwa / Aashadam / Margashira)",
    },
    {
        "code": "V_STANDARD", "name": "Standard Promo", "price": 1499, "days": 90,
        "telugu": "3 categories + 3 posts + lead box (90 రోజులు)",
        "perks": ["3 category listings (90 days)", "3 Telegram + 2 WhatsApp channel posts",
                  "Lead box (site nunchi direct enquiries → mee WhatsApp)", "Priority placement in search",
                  "Monthly performance report (views/clicks/leads)"],
        "best_for": "Manchi name unna local vendor",
        "popular": True,
    },
    {
        "code": "V_PREMIUM", "name": "Premium Partner", "price": 3999, "days": 180,
        "telugu": "5 categories + weekly posts + top slot + badge (180 రోజులు)",
        "perks": ["5 category listings + 1 special channel (180 days)", "Weekly promo post (24+ posts)",
                  "Top slot rotation on home + /vendors page", "✅ Verified badge + rating badge",
                  "WhatsApp status blast (2 times/month, our groups)", "Dedicated account manager (call support)",
                  "Bride/groom matching season alert list"],
        "best_for": "Established vendors — full season visibility",
    },
]

PACKAGE_MAP = {p["code"]: p for p in PACKAGES}

ADDONS_VENDOR = [
    {"code": "V_ADD_PHOTO", "name": "Photo/Video gallery (10 items)", "price": 299},
    {"code": "V_ADD_REEL", "name": "Reel / short video (mana channels ki)", "price": 999},
    {"code": "V_ADD_INTERVIEW", "name": "Vendor interview video (trust build)", "price": 1499},
    {"code": "V_ADD_BRIDE_MAIL", "name": "Monthly mail to new brides/grooms (our DB)", "price": 799},
]

SLOTS = ["home_top_banner", "home_mid_strip", "vendors_top", "matches_sidebar", "requests_sidebar"]

# ---------------------------------------------------------------------------
# IN-MEMORY STATE (+ file persistence: vendors, leads, impressions)
# ---------------------------------------------------------------------------
VENDORS: List[Dict] = []
LEADS: List[Dict] = []
STATS_LOG: List[Dict] = []

PHONE_RE = None


def _now() -> str:
    return datetime.now().isoformat()


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _digits(text) -> str:
    return "".join(ch for ch in str(text or "") if ch.isdigit())


def _next_vendor_id() -> str:
    n = len([v for v in VENDORS if str(v.get("id", "")).startswith("MVV")]) + 1
    while any(v.get("id") == "MVV-%04d" % n for v in VENDORS):
        n += 1
    return "MVV-%04d" % n


def save_state() -> Dict:
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"at": _now(), "vendors": VENDORS[-800:], "leads": LEADS[-3000:],
                       "stats": STATS_LOG[-5000:]}, f, ensure_ascii=False, indent=1)
        return {"ok": True, "path": STATE_FILE, "vendors": len(VENDORS), "leads": len(LEADS)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:140]}


def load_state() -> Dict:
    global VENDORS, LEADS, STATS_LOG
    try:
        if not os.path.exists(STATE_FILE):
            return {"ok": True, "loaded": False}
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        VENDORS = list(data.get("vendors", []))
        LEADS = list(data.get("leads", []))
        STATS_LOG = list(data.get("stats", []))
        return {"ok": True, "loaded": True, "vendors": len(VENDORS), "leads": len(LEADS)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:140]}


# ---------------------------------------------------------------------------
# REGISTER / ACTIVATE
# ---------------------------------------------------------------------------
def validate_vendor_form(form: Dict) -> Dict:
    problems = []
    name = str(form.get("business_name", "")).strip()
    if len(name) < 3:
        problems.append("business_name: business peru 3 aksharalu kanna ekkuva undali")
    if str(form.get("category", "")).strip() not in CATEGORY_MAP:
        problems.append("category: list lo unna category select cheyyandi")
    phone = _digits(form.get("phone"))
    if len(phone) != 10:
        problems.append("phone: 10 digit mobile number ivvandi")
    city = str(form.get("city", "")).strip()
    if len(city) < 2:
        problems.append("city: city/town peru ivvandi")
    pkg = str(form.get("package", "V_BASIC")).strip().upper()
    if pkg not in PACKAGE_MAP:
        problems.append("package: %s" % ", ".join(PACKAGE_MAP))
    return {"ok": not problems, "problems": problems}


def register_vendor(form: Dict, all_vendors: Optional[List[Dict]] = None) -> Dict:
    """Vendor signup → pending → admin approve → active (package days start)."""
    all_vendors = all_vendors if all_vendors is not None else VENDORS
    v = validate_vendor_form(form)
    if not v["ok"]:
        return {"ok": False, "reason": "invalid", "problems": v["problems"],
                "message_telugu": "⚠️ Ee details saricheyyali: " + " | ".join(v["problems"])}
    phone = _digits(form.get("phone"))
    cat = str(form.get("category")).strip()
    pkg = str(form.get("package", "V_BASIC")).strip().upper()
    dup = next((x for x in all_vendors if _digits(x.get("phone")) == phone
                and x.get("category") == cat and x.get("status") in ("pending", "active")), None)
    if dup:
        return {"ok": False, "reason": "duplicate", "vendor_id": dup.get("id"),
                "message_telugu": "ℹ️ Ee number tho ee category lo already listing undi (%s) — update cheyyali ante support ki cheppandi"
                                  % dup.get("id")}
    vendor = {
        "id": _next_vendor_id(),
        "business_name": str(form.get("business_name")).strip()[:80],
        "owner_name": str(form.get("owner_name", "")).strip()[:60],
        "category": cat,
        "category_te": category_label(cat)["te"],
        "icon": category_label(cat)["icon"],
        "phone": phone,
        "whatsapp": _digits(form.get("whatsapp")) or phone,
        "city": str(form.get("city", "")).strip()[:40],
        "district": str(form.get("district", "")).strip()[:40],
        "state": str(form.get("state", "TS")).strip()[:4],
        "service_areas": str(form.get("service_areas", "")).strip()[:160],
        "price_range": str(form.get("price_range", "")).strip()[:60],
        "about": str(form.get("about", "")).strip()[:600],
        "experience_years": str(form.get("experience_years", "")).strip()[:10],
        "photo_url": str(form.get("photo_url", "")).strip()[:200],
        "package": pkg,
        "package_price": PACKAGE_MAP[pkg]["price"],
        "package_days": PACKAGE_MAP[pkg]["days"],
        "status": "pending",
        "verified": False,
        "rating": 0.0,
        "reviews": 0,
        "impressions": 0,
        "clicks": 0,
        "leads": 0,
        "created_at": _now(),
        "activated_at": "",
        "expires_at": "",
        "payment_ref": "",
        "source": str(form.get("source", "website"))[:30],
    }
    all_vendors.append(vendor)
    save_state()
    return {"ok": True, "vendor_id": vendor["id"], "vendor": vendor,
            "package": PACKAGE_MAP[pkg], "amount": PACKAGE_MAP[pkg]["price"],
            "upi_id": os.getenv("VENDOR_UPI_ID", os.getenv("PAYMENT_UPI_ID", "")),
            "phonepe_link": "phonepe://pay?pa=%s&pn=ManaVivaha&am=%d&cu=INR&tn=%s"
                            % (os.getenv("VENDOR_UPI_ID", os.getenv("PAYMENT_UPI_ID", "manavivaha@upi")),
                               PACKAGE_MAP[pkg]["price"], vendor["id"]),
            "steps_telugu": [
                "1️⃣ ₹%d pay cheyyandi (UPI leda PhonePe link)" % PACKAGE_MAP[pkg]["price"],
                "2️⃣ Payment screenshot mana WhatsApp ki pampandi (reference: %s)" % vendor["id"],
                "3️⃣ 2 గంటల్లో admin verify chesi listing ACTIVE chestadu",
                "4️⃣ Mee promo post + poster ready — mana channels lo veltundi",
            ],
            "message_telugu": "🎉 %s — mee vendor request vachindi! Package: %s (₹%d / %d days). Payment tho ventane listing live avutundi."
                              % (vendor["business_name"], PACKAGE_MAP[pkg]["name"],
                                 PACKAGE_MAP[pkg]["price"], PACKAGE_MAP[pkg]["days"])}


def activate_vendor(vendor_id: str, package: str = "", utr: str = "",
                    all_vendors: Optional[List[Dict]] = None) -> Dict:
    all_vendors = all_vendors if all_vendors is not None else VENDORS
    v = next((x for x in all_vendors if x.get("id") == vendor_id), None)
    if not v:
        return {"ok": False, "reason": "not_found"}
    pkg_code = (package or v.get("package") or "V_BASIC").upper()
    if pkg_code not in PACKAGE_MAP:
        return {"ok": False, "reason": "bad_package"}
    pkg = PACKAGE_MAP[pkg_code]
    days = pkg["days"]
    v["package"] = pkg_code
    v["package_price"] = pkg["price"]
    v["package_days"] = days
    v["status"] = "active"
    v["verified"] = pkg_code in ("V_PREMIUM", "V_STANDARD") or bool(v.get("verified"))
    v["activated_at"] = _now()
    v["expires_at"] = (datetime.now() + timedelta(days=days)).isoformat()
    v["payment_ref"] = utr
    save_state()
    return {"ok": True, "vendor": v, "package": pkg, "days": days,
            "expires_at": v["expires_at"],
            "message_telugu": "✅ %s ACTIVE (%s, %d days). Promo post + poster pampadaniki ready 🚀"
                              % (v["business_name"], pkg["name"], days)}


def reject_vendor(vendor_id: str, reason: str = "") -> Dict:
    v = next((x for x in VENDORS if x.get("id") == vendor_id), None)
    if not v:
        return {"ok": False, "reason": "not_found"}
    v["status"] = "rejected"
    v["reject_reason"] = reason[:160]
    save_state()
    return {"ok": True, "vendor": v, "message_telugu": "❌ %s reject ayyindi — %s" % (v["business_name"], reason or "details verify avvaledu")}


def expire_due_vendors() -> Dict:
    """Kalam ayyina vendors ni auto-expire (worker/startup lo call)."""
    now = datetime.now()
    n = 0
    for v in VENDORS:
        if v.get("status") != "active":
            continue
        try:
            exp = datetime.fromisoformat(v.get("expires_at", ""))
        except Exception:
            continue
        if exp < now:
            v["status"] = "expired"
            n += 1
    if n:
        save_state()
    return {"ok": True, "expired": n}


# ---------------------------------------------------------------------------
# DIRECTORY + SEARCH
# ---------------------------------------------------------------------------
def vendors_directory(category: str = "", district: str = "", city: str = "", q: str = "",
                      include_inactive: bool = False, limit: int = 60) -> Dict:
    items = [v for v in VENDORS if include_inactive or v.get("status") == "active"]
    if category:
        cats = [c.strip() for c in category.split(",") if c.strip()]
        items = [v for v in items if v.get("category") in cats]
    if district:
        items = [v for v in items if district.lower() in str(v.get("district", "")).lower()
                 or district.lower() in str(v.get("city", "")).lower()
                 or district.lower() in str(v.get("service_areas", "")).lower()]
    if city:
        items = [v for v in items if city.lower() in str(v.get("city", "")).lower()
                 or city.lower() in str(v.get("service_areas", "")).lower()]
    if q:
        needle = q.lower()
        items = [v for v in items if needle in (str(v.get("business_name", "")) + " "
                                                + str(v.get("about", "")) + " "
                                                + str(v.get("city", "")) + " "
                                                + str(v.get("category", ""))).lower()]
    order = {"V_PREMIUM": 0, "V_STANDARD": 1, "V_SPOTLIGHT": 0, "V_BASIC": 2, "V_SINGLE_POST": 3, "V_STATUS_BLAST": 3}
    items.sort(key=lambda v: (order.get(v.get("package"), 4), -float(v.get("rating", 0) or 0)))
    counts: Dict[str, int] = {}
    for v in [x for x in VENDORS if include_inactive or x.get("status") == "active"]:
        counts[v["category"]] = counts.get(v["category"], 0) + 1
    return {"total": len(items), "counts": counts, "limit": limit,
            "vendors": [public_vendor(v) for v in items[:limit]],
            "categories": [{**c, "count": counts.get(c["key"], 0)} for c in CATEGORIES]}


def public_vendor(v: Dict, full_contact: bool = True) -> Dict:
    """Directory/listing ki vendor view (contact WhatsApp CTA tho)."""
    out = {
        "id": v.get("id"), "business_name": v.get("business_name"),
        "category": v.get("category"), "category_te": v.get("category_te"),
        "icon": v.get("icon") or category_label(v.get("category", ""))["icon"],
        "city": v.get("city"), "district": v.get("district"), "state": v.get("state"),
        "service_areas": v.get("service_areas"), "price_range": v.get("price_range"),
        "about": v.get("about"), "experience_years": v.get("experience_years"),
        "verified": bool(v.get("verified")), "rating": v.get("rating", 0),
        "reviews": v.get("reviews", 0), "package": v.get("package"),
        "photo_url": v.get("photo_url", ""), "status": v.get("status"),
    }
    wa = _digits(v.get("whatsapp")) or _digits(v.get("phone"))
    if full_contact and wa:
        out["whatsapp_link"] = "https://wa.me/91%s?text=%s" % (
            wa, "Namaste! Mana Vivaha (manavivaha.in) lo mee %s listing chusanu — details cheppandi"
                % (v.get("business_name", "")))
        out["call_link"] = "tel:+91%s" % wa
    return out


# ---------------------------------------------------------------------------
# AD ROTATION (paid-first, weighted, daily budget-ish)
# ---------------------------------------------------------------------------
def ad_rotation(slot: str = "home_top_banner", limit: int = 2, track: bool = True) -> Dict:
    if slot not in SLOTS:
        slot = "home_top_banner"
    active = [v for v in VENDORS if v.get("status") == "active"]
    weighted = []
    for v in active:
        pkg = v.get("package")
        w = {"V_PREMIUM": 5, "V_SPOTLIGHT": 6, "V_STANDARD": 3, "V_BASIC": 1}.get(pkg, 0)
        if w:
            weighted.extend([v] * w)
    random.shuffle(weighted)
    picked, seen = [], set()
    for v in weighted:
        if v["id"] in seen:
            continue
        seen.add(v["id"])
        picked.append(v)
        if len(picked) >= limit:
            break
    if track:
        for v in picked:
            v["impressions"] = int(v.get("impressions", 0)) + 1
            STATS_LOG.append({"at": _now(), "type": "impression", "slot": slot, "vendor_id": v["id"]})
        if picked:
            save_state()
    return {"slot": slot, "count": len(picked), "ads": [ad_card(v) for v in picked],
            "note_telugu": "Mee business kooda ikkada kanipinchali ante — /advertise chudandi (₹149 nunchi)"}


def ad_card(v: Dict) -> Dict:
    return {"vendor_id": v.get("id"), "business_name": v.get("business_name"),
            "category": v.get("category"), "category_te": v.get("category_te"),
            "icon": v.get("icon"), "city": v.get("city"), "price_range": v.get("price_range"),
            "verified": bool(v.get("verified")), "rating": v.get("rating", 0),
            "cta_telugu": "WhatsApp cheyyandi", "whatsapp_link": public_vendor(v).get("whatsapp_link", ""),
            "detail_url": "/vendors/%s" % v.get("id")}


def track_vendor_click(vendor_id: str, source: str = "") -> Dict:
    v = next((x for x in VENDORS if x.get("id") == vendor_id), None)
    if not v:
        return {"ok": False, "reason": "not_found"}
    v["clicks"] = int(v.get("clicks", 0)) + 1
    STATS_LOG.append({"at": _now(), "type": "click", "vendor_id": vendor_id, "source": source[:40]})
    save_state()
    return {"ok": True, "vendor_id": vendor_id, "clicks": v["clicks"]}


# ---------------------------------------------------------------------------
# LEADS (site nunchi enquiry → vendor WhatsApp + admin alert)
# ---------------------------------------------------------------------------
def vendor_lead(vendor_id: str, form: Dict) -> Dict:
    v = next((x for x in VENDORS if x.get("id") == vendor_id), None)
    if not v:
        return {"ok": False, "reason": "not_found"}
    name = str(form.get("name", "")).strip()
    phone = _digits(form.get("phone"))
    problems = []
    if len(name) < 2:
        problems.append("name")
    if len(phone) != 10:
        problems.append("phone (10 digits)")
    if problems:
        return {"ok": False, "reason": "invalid", "problems": problems,
                "message_telugu": "⚠️ Ee details saricheyyali: " + ", ".join(problems)}
    lead = {
        "id": "VL-%s-%04d" % (datetime.now().strftime("%y%m%d"), len(LEADS) + 1),
        "vendor_id": vendor_id, "vendor_name": v.get("business_name"),
        "name": name[:60], "phone": phone, "event_date": str(form.get("event_date", ""))[:20],
        "district": str(form.get("district", ""))[:40], "budget": str(form.get("budget", ""))[:30],
        "message": str(form.get("message", ""))[:400], "at": _now(), "status": "new",
        "source": str(form.get("source", "website"))[:30],
    }
    LEADS.append(lead)
    v["leads"] = int(v.get("leads", 0)) + 1
    save_state()
    return {"ok": True, "lead": lead, "vendor": public_vendor(v),
            "vendor_whatsapp_text": lead_to_vendor_text(v, lead),
            "customer_text_telugu": (
                "🙏 %s garu, mee enquiry %s ki vellindi. %s team mee number ki call/WhatsApp chestaru. "
                "Rate compare cheyyali ante mana side nunchi 3 more %s vendors pampistham (FREE)."
                % (lead["name"], v.get("business_name"), v.get("business_name"),
                   category_label(v.get("category", ""))["en"])),
            "message_telugu": "✅ Enquiry pampam — %s mee number ki contact chestaru (30 nimushalalo)" % v.get("business_name")}


def lead_to_vendor_text(vendor: Dict, lead: Dict) -> str:
    return ("🔔 *NEW ENQUIRY* — Mana Vivaha\n"
            "Business: %s (%s)\n"
            "Customer: %s\n📞 %s\n"
            "📍 %s | 📅 Event: %s | 💰 Budget: %s\n"
            "📝 %s\n\n"
            "Ventane call/WhatsApp cheyyandi — fast reply = ekkuva bookings ✅\n"
            "— Mana Vivaha (manavivaha.in)"
            % (vendor.get("business_name"), vendor.get("category_te") or vendor.get("category"),
               lead.get("name"), lead.get("phone"), lead.get("district") or "-",
               lead.get("event_date") or "-", lead.get("budget") or "-", lead.get("message") or "-"))


def leads_for(vendor_id: str, limit: int = 50) -> List[Dict]:
    return list(reversed([l for l in LEADS if l.get("vendor_id") == vendor_id]))[:limit]


# ---------------------------------------------------------------------------
# PROMO CONTENT (Telugu posts + poster text) — channels ki ready
# ---------------------------------------------------------------------------
def promo_post(vendor: Dict, variant: int = 0, channel: str = "") -> Dict:
    name = vendor.get("business_name", "")
    cat = vendor.get("category_te") or category_label(vendor.get("category", ""))["en"]
    icon = vendor.get("icon") or "🏪"
    city = vendor.get("city", "")
    areas = vendor.get("service_areas") or city
    price = vendor.get("price_range") or ""
    phone = _digits(vendor.get("whatsapp")) or _digits(vendor.get("phone"))
    about = (vendor.get("about") or "").strip()
    exp = vendor.get("experience_years", "")
    verified = "✅ Verified" if vendor.get("verified") else ""
    tg = [
        ("%s *%s* — %s\n\n%s\n\n📍 %s%s%s%s\n%s\n💰 %s\n📞 %s\n\n"
         "Mana Vivaha lo %s — pelli sambandham chusukune vaallaki recommend chestunnam 🙏"
         % (icon, name.upper(), cat,
            (about[:220] + ("..." if len(about) > 220 else "")) if about else "Mana Vivaha partner vendor.",
            city, (" | " + areas) if areas and areas != city else "",
            (" | " + exp + " yrs experience") if exp else "",
            (" | " + verified) if verified else "",
            "🔗 Listing: manavivaha.in/vendors", price or "Best rates — direct ga adagandi", phone,
            cat)),
        ("🎊 %s %s — %s\n\nMee pelli ki kavalsina %s ikkade!\n%s\n📍 %s\n📞 %s (WhatsApp)\n\n"
         "Mana Vivaha members ki *special rate* — ee post chupinchandi 😊\n#ManaVivaha #%s #%s"
         % (icon, cat, name, cat,
            ("⭐ " + about[:160]) if about else "Trusted local vendor",
            areas or city, phone,
            name.replace(" ", ""), city.replace(" ", "") or "Telugu")),
        ("💍 *Pelli season special* 💍\n\n%s *%s*\n%s\n\n%s\n📍 %s\n💰 %s\n📞 %s\n\n"
         "Booking fast ga avutunnayi — mundhe confirm chesukondi ✅\nMana Vivaha partner (verified) 🏪"
         % (icon, name, cat, about[:200] or "Quality service, manchi rates.",
            areas or city, price or "Rates call lo cheptam", phone)),
    ]
    wa = [
        ("🙏 Namaste! *%s* — %s (Mana Vivaha partner)\n\n%s\n📍 %s\n💰 %s\n📞 %s\n\n"
         "Pelli sambandham chusukuntunnara? Ee vendor ni manam verify chesam ✅ — direct ga contact cheyyandi."
         % (name, cat, about[:200] or "Manchi service + reasonable rates",
            areas or city, price or "Call chesi adagandi", phone)),
        ("%s %s — %s\n%s\n📍 %s | 📞 %s\nMana Vivaha verified partner 🏪 (manavivaha.in/vendors)"
         % (icon, cat, city, ("⭐ " + about[:150]) if about else "Trusted vendor", areas or city, phone)),
    ]
    return {
        "vendor_id": vendor.get("id"), "variant": variant % max(1, len(tg)),
        "telegram_post": tg[variant % len(tg)],
        "whatsapp_messages": wa,
        "poster_text": "%s %s\n%s | %s\n📞 %s\nmanavivaha.in/vendors" % (icon, name, cat, city, phone),
        "channel_hint": channel or "Mee city/caste channel + 4 main channels",
        "share_me": "https://wa.me/91%s?text=%s" % (phone, "Namaste! Mana Vivaha listing chusanu — rates cheppandi"),
    }


# ---------------------------------------------------------------------------
# DASHBOARD (vendor ki performance report)
# ---------------------------------------------------------------------------
def vendor_dashboard(vendor_id: str) -> Dict:
    v = next((x for x in VENDORS if x.get("id") == vendor_id), None)
    if not v:
        return {"ok": False, "reason": "not_found"}
    my_leads = leads_for(vendor_id, limit=20)
    days_left = 0
    try:
        exp = datetime.fromisoformat(v.get("expires_at", ""))
        days_left = max(0, (exp - datetime.now()).days)
    except Exception:
        days_left = 0
    cat_peers = [x for x in VENDORS if x.get("category") == v.get("category") and x.get("status") == "active"]
    return {
        "ok": True, "vendor": public_vendor(v), "package": PACKAGE_MAP.get(v.get("package"), {}),
        "days_left": days_left,
        "stats": {"impressions": v.get("impressions", 0), "clicks": v.get("clicks", 0),
                  "leads": v.get("leads", 0), "reviews": v.get("reviews", 0),
                  "ctr_pct": round((int(v.get("clicks", 0)) / int(v.get("impressions", 1)) * 100), 1)
                  if v.get("impressions") else 0.0,
                  "lead_rate_pct": round((int(v.get("leads", 0)) / int(v.get("clicks", 1)) * 100), 1)
                  if v.get("clicks") else 0.0},
        "recent_leads": my_leads,
        "competition": {"same_category_active": len(cat_peers),
                        "message_telugu": "Mee category lo %d active vendors unnaru — top slot ki Premium thisukondi" % len(cat_peers)},
        "upsell_telugu": ("⏳ %d days migilayi — renew cheyyandi (₹%d / %d days)"
                          % (days_left, PACKAGE_MAP.get(v.get("package"), PACKAGE_MAP["V_BASIC"])["price"],
                             PACKAGE_MAP.get(v.get("package"), PACKAGE_MAP["V_BASIC"])["days"]))
        if v.get("status") == "active" else "Listing active ledu — admin approve cheyyali",
        "message_telugu": "📊 Impressions %s · Clicks %s · Enquiries %s — %s"
                          % (v.get("impressions", 0), v.get("clicks", 0), v.get("leads", 0),
                             "manchi ga nadusthundi 👍" if int(v.get("leads", 0)) > 0 else "promo post pettandi, leads perugutayi"),
    }


# ---------------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------------
def vendor_queue(status: str = "pending") -> Dict:
    items = [v for v in VENDORS if (not status or v.get("status") == status)]
    items = list(reversed(items))
    return {"count": len(items), "total_amount": sum(int(v.get("package_price", 0)) for v in items),
            "items": [dict(v) for v in items[:100]],
            "slots": SLOTS}


def vendor_revenue() -> Dict:
    active = [v for v in VENDORS if v.get("status") == "active"]
    pending = [v for v in VENDORS if v.get("status") == "pending"]
    by_pkg: Dict[str, Dict] = {}
    for v in VENDORS:
        if v.get("status") not in ("active", "expired"):
            continue
        p = by_pkg.setdefault(v.get("package", "V_BASIC"),
                              {"count": 0, "revenue": 0, "name": PACKAGE_MAP.get(v.get("package"), {}).get("name", v.get("package"))})
        p["count"] += 1
        p["revenue"] += int(v.get("package_price", 0) or 0)
    return {
        "vendors_total": len(VENDORS), "active": len(active), "pending": len(pending),
        "mrr": sum(int(v.get("package_price", 0) or 0) for v in active),
        "collected": sum(int(v.get("package_price", 0) or 0) for v in VENDORS if v.get("status") in ("active", "expired")),
        "pipeline": sum(int(v.get("package_price", 0) or 0) for v in pending),
        "by_package": by_pkg,
        "leads_total": len(LEADS),
        "leads_today": len([l for l in LEADS if str(l.get("at", "")).startswith(_today())]),
        "impressions": sum(int(v.get("impressions", 0)) for v in VENDORS),
        "clicks": sum(int(v.get("clicks", 0)) for v in VENDORS),
        "top_vendors": [{"id": v["id"], "name": v.get("business_name"), "leads": v.get("leads", 0),
                         "clicks": v.get("clicks", 0), "package": v.get("package")}
                        for v in sorted(VENDORS, key=lambda x: -int(x.get("leads", 0)))[:5]],
        "renewals_due": [{"id": v["id"], "name": v.get("business_name"), "expires_at": v.get("expires_at")}
                         for v in active if _days_left(v) <= 7],
        "message_telugu": "🏪 %d active vendors · ₹%d collected · %d leads · %d enquiries ee roju"
                          % (len(active), sum(int(v.get("package_price", 0) or 0) for v in VENDORS
                                              if v.get("status") in ("active", "expired")),
                             len(LEADS), len([l for l in LEADS if str(l.get("at", "")).startswith(_today())])),
    }


def _days_left(v: Dict) -> int:
    try:
        return max(0, (datetime.fromisoformat(v.get("expires_at", "")) - datetime.now()).days)
    except Exception:
        return 0


def packages_public() -> Dict:
    return {
        "currency": "INR",
        "headline": "Mee business ni Mana Vivaha lo promote cheyyandi — ₹149 nunchi",
        "packages": PACKAGES, "addons": ADDONS_VENDOR, "slots": SLOTS, "categories": CATEGORIES,
        "how_it_works_telugu": [
            "1️⃣ Package select chesi register cheyyandi (2 nimushalu)",
            "2️⃣ Payment (UPI/PhonePe) + screenshot mana WhatsApp ki",
            "3️⃣ 2 గంటల్లో admin verify → listing ACTIVE + verified badge",
            "4️⃣ Promo post + poster mana Telegram/WhatsApp channels lo (52 channels)",
            "5️⃣ Enquiries direct mee WhatsApp ki — dashboard lo performance report",
        ],
        "why_telugu": [
            "🎯 Telugu pelli market — bride/groom families + relatives (manchi intent)",
            "📢 52 channels + WhatsApp lanes (anti-ban safe order lo posts)",
            "📊 Impressions/clicks/enquiries — edi pani chesindo kanipistundi",
            "🏅 Verified badge + rating — trust build avutundi",
            "🔁 Renewal ki discount + season offers (Aashadam, Margashira, Padwa)",
        ],
        "renewal_discount_pct": 15,
        "contact_whatsapp": os.getenv("VENDOR_SALES_WHATSAPP", os.getenv("SUPPORT_PHONE", "")),
    }


def vendor_stats() -> Dict:
    active = [v for v in VENDORS if v.get("status") == "active"]
    counts: Dict[str, int] = {}
    for v in active:
        counts[v["category"]] = counts.get(v["category"], 0) + 1
    return {"total": len(VENDORS), "active": len(active),
            "pending": len([v for v in VENDORS if v.get("status") == "pending"]),
            "categories": len(CATEGORIES), "by_category": counts, "leads": len(LEADS),
            "impressions": sum(int(v.get("impressions", 0)) for v in VENDORS),
            "clicks": sum(int(v.get("clicks", 0)) for v in VENDORS)}

# ---------------------------------------------------------------------------
# DEMO SEED — site khali ga kanipinchadu (launch lo real vendors tho replace avutayi)
# ---------------------------------------------------------------------------
DEMO_VENDORS = [
    {"business_name": "Sri Lakshmi Catering", "category": "catering", "city": "Warangal", "district": "Warangal",
     "phone": "9848011101", "package": "V_STANDARD", "price_range": "₹250-450 per plate", "experience_years": "25",
     "about": "Traditional Telugu vindu — 200 nunchi 2000 members varaku. Veg + non-veg counters, live dosa counter.",
     "service_areas": "Warangal, Hanamkonda, Kazipet, Jangaon"},
    {"business_name": "Sri Balaji Photography", "category": "photography", "city": "Hyderabad", "district": "Rangareddy",
     "phone": "9848011102", "package": "V_PREMIUM", "price_range": "₹40,000 - 1,20,000", "experience_years": "12",
     "about": "Candid + traditional + drone. Pre-wedding shoot, full album design, same-day edit.",
     "service_areas": "Hyderabad, Secunderabad, TS + AP"},
    {"business_name": "Vasavi Decorations", "category": "decorations", "city": "Vijayawada", "district": "Krishna",
     "phone": "9848011103", "package": "V_STANDARD", "price_range": "₹35,000 - 2,00,000", "experience_years": "15",
     "about": "Mandap, stage backdrop, flower decoration, lighting. Pelli, half-saree, seemantham anni functions.",
     "service_areas": "Vijayawada, Guntur, Tenali, Eluru"},
    {"business_name": "Sai Kalyana Mandapam", "category": "banquet_hall", "city": "Karimnagar", "district": "Karimnagar",
     "phone": "9848011104", "package": "V_BASIC", "price_range": "₹45,000 - 1,50,000/day", "experience_years": "20",
     "about": "AC function hall — 800 members seating, 200 car parking, dining hall + rooms, generator backup.",
     "service_areas": "Karimnagar, Peddapalli, Jagtial"},
    {"business_name": "Srinivasa Tent House", "category": "tent_house", "city": "Nalgonda", "district": "Nalgonda",
     "phone": "9848011105", "package": "V_BASIC", "price_range": "₹25,000 - 90,000", "experience_years": "18",
     "about": "Tents, chairs, sound system, shamiana, dining tables — ee area lo 18 years nunchi.",
     "service_areas": "Nalgonda, Miryalaguda, Suryapet, Bhongir"},
    {"business_name": "Pandit Sri Sharma", "category": "pandit", "city": "Hyderabad", "district": "Hyderabad",
     "phone": "9848011106", "package": "V_BASIC", "price_range": "₹8,000 - 35,000", "experience_years": "22",
     "about": "Muhurtham, pelli, seemantham, satyanarayana vratam — Telugu + Sanskritlo pooja chepistham.",
     "service_areas": "Hyderabad, Ranga Reddy, Medchal"},
    {"business_name": "Sri Padmavathi Jewellers", "category": "jewellery", "city": "Guntur", "district": "Guntur",
     "phone": "9848011107", "package": "V_BASIC", "price_range": "Pelli haram ₹2L nunchi", "experience_years": "35",
     "about": "916 gold, vaddanam, haram, bangles — custom pelli jewellery designs, hall-mark certified.",
     "service_areas": "Guntur, Tenali, Chilakaluripet"},
    {"business_name": "Lakshmi Bridal Makeup Studio", "category": "makeup", "city": "Nizamabad", "district": "Nizamabad",
     "phone": "9848011108", "package": "V_STANDARD", "price_range": "₹12,000 - 60,000", "experience_years": "10",
     "about": "Bridal makeup, hairstyle, saree draping, HD + airbrush. Reception + pelli packages.",
     "service_areas": "Nizamabad, Armoor, Kamareddy, Adilabad"},
    {"business_name": "Vijaya Wedding Planners", "category": "wedding_planner", "city": "Visakhapatnam", "district": "Visakhapatnam",
     "phone": "9848011109", "package": "V_PREMIUM", "price_range": "₹1,50,000 nunchi (complete package)", "experience_years": "8",
     "about": "Complete pelli planning — hall, catering, decoration, photography, makeup, invitation, travel. End-to-end.",
     "service_areas": "Visakhapatnam, Vizianagaram, Srikakulam, Kakinada"},
    {"business_name": "Ravi DJ & Melam Band", "category": "music_dj", "city": "Khammam", "district": "Khammam",
     "phone": "9848011110", "package": "V_BASIC", "price_range": "₹15,000 - 75,000", "experience_years": "14",
     "about": "DJ + nadaswaram + melam band. Baraat, reception, sangeet ki full sound + lighting.",
     "service_areas": "Khammam, Kothagudem, Bhadrachalam"},
]

DEMO_LEADS = [
    {"vendor": "Sri Lakshmi Catering", "name": "Ravi Kumar", "phone": "9848090001", "district": "Warangal",
     "event_date": "2026-11-22", "budget": "₹1,20,000", "message": "300 members ki lunch + dinner, veg only"},
    {"vendor": "Sri Balaji Photography", "name": "Sneha Reddy", "phone": "9848090002", "district": "Hyderabad",
     "event_date": "2026-12-05", "budget": "₹75,000", "message": "Candid + traditional, 2 days function"},
]


def demo_seed() -> Dict:
    """Demo vendors + leads (site khali ga kanipinchadu). Idempotent — duplicates add avvavu."""
    created = []
    for w in DEMO_VENDORS:
        if any(x.get("business_name") == w["business_name"] for x in VENDORS):
            continue
        form = {"business_name": w["business_name"], "category": w["category"], "phone": w["phone"],
                "city": w["city"], "district": w["district"], "state": "TS", "package": w["package"],
                "about": w["about"], "price_range": w["price_range"], "experience_years": w["experience_years"],
                "service_areas": w["service_areas"], "owner_name": "", "source": "demo_seed"}
        res = register_vendor(form)
        if res.get("ok"):
            activate_vendor(res["vendor_id"], utr="DEMO")
            created.append(res["vendor_id"])
    # leads demo (dashboard lo performance kanipinchadaniki)
    for dl in DEMO_LEADS:
        v = next((x for x in VENDORS if x.get("business_name") == dl["vendor"]), None)
        if v and not [l for l in LEADS if l.get("vendor_id") == v["id"]]:
            vendor_lead(v["id"], {"name": dl["name"], "phone": dl["phone"], "district": dl["district"],
                                  "event_date": dl["event_date"], "budget": dl["budget"],
                                  "message": dl["message"], "source": "demo_seed"})
    # kొంత impressions/clicks (rotation demo)
    for v in VENDORS[:4]:
        v["impressions"] = int(v.get("impressions", 0)) + random.randint(40, 160)
        v["clicks"] = int(v.get("clicks", 0)) + random.randint(5, 25)
    save_state()
    return {"ok": True, "created": created, "total": len(VENDORS), "leads": len(LEADS)}
