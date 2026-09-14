"""
MANA VIVAHA — VENDOR PROMO POSTER (PNG) 🖼️🏪
=============================================
Vendor listing ki promo poster: business peru, category (Telugu), city, rate range,
phone, QR (wa.me direct chat) — 1080×1080 square leda 1080×1920 status.

Run: from vendors import ... ; vendor_poster(vendor, style="square")
Pillow leda qrcode lekapote — crash avvadu (plain card / QR skip).
"""
import os
from typing import Dict, Optional

BRAND_MAROON = (122, 12, 46)
BRAND_GOLD = (212, 175, 55)
BRAND_CREAM = (255, 248, 231)
BRAND_NAVY = (15, 31, 60)

POSTER_DIR = os.getenv("VENDOR_POSTER_DIR", "/tmp/vendor_posters")


def _txt(text, fallback: str = "") -> str:
    """Strip emoji/Telugu (font lo glyphs levu → tofu boxes) — English part matrame print.
    Udaharanam: "విందు భోజనం (Catering)" → "Catering"."""
    s = str(text or "").replace("₹", "Rs.")   # rupee glyph font lo ledu → mundhe "Rs." ki marchali
    keep = []
    for ch in s:
        o = ord(ch)
        if o < 0x0250 or 0x1E00 <= o <= 0x1EFF:      # ASCII + Latin (emoji/Telugu skip)
            keep.append(ch)
    out = " ".join("".join(keep).split()).replace("  ", " ").strip(" .")
    out = out.replace("()", "").replace("|  |", "|").strip(" -|()")
    return out or fallback


def _safe(text: str) -> str:
    return "".join(ch for ch in str(text) if ch.isalnum() or ch in "-_")[:24] or "vendor"


def _font(size: int):
    from PIL import ImageFont
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _center(draw, y, text, font, fill, W):
    try:
        w = draw.textlength(text, font=font)
    except Exception:
        w = draw.textsize(text, font=font)[0]
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)
    return y + (font.size if hasattr(font, "size") else 18) + 8


def vendor_poster(vendor: Dict, style: str = "square", out_path: Optional[str] = None,
                  site: str = "manavivaha.in") -> str:
    """Vendor promo poster generate chesi path return chestundi."""
    from PIL import Image, ImageDraw
    code = _safe(vendor.get("id", "MVV"))
    out_path = out_path or os.path.join(POSTER_DIR, "%s_%s.png" % (code, style))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    W, H = (1080, 1080) if style != "status" else (1080, 1920)
    box_y = H - (400 if style != "status" else 460)
    box_guess = box_y - 10
    qr_ready = False
    img = Image.new("RGB", (W, H), BRAND_CREAM)
    d = ImageDraw.Draw(img)

    # header
    d.rectangle([0, 0, W, 190], fill=BRAND_MAROON)
    _center(d, 42, "MANA VIVAHA", _font(56), BRAND_GOLD, W)
    _center(d, 116, "Telugu Matrimony · Wedding Vendors", _font(30), (255, 255, 255), W)

    y = 230
    y = _center(d, y, _txt(vendor.get("business_name"), "Vendor")[:34], _font(56), BRAND_MAROON, W)
    y = _center(d, y, _txt(vendor.get("category_te"), _txt(vendor.get("category"))) [:40], _font(34), BRAND_NAVY, W)
    y += 10
    d.rectangle([100, y, W - 100, y + 4], fill=BRAND_GOLD)
    y += 30
    _city = _txt(vendor.get("city"))
    _dist = _txt(vendor.get("district"))
    _place = _city if (not _dist or _dist.lower() == _city.lower()) else "%s | %s" % (_city, _dist)
    y = _center(d, y, _place or "-",
                _font(34), BRAND_NAVY, W)
    if vendor.get("service_areas"):
        y = _center(d, y, _txt(vendor.get("service_areas"))[:46], _font(28), BRAND_NAVY, W)
    if vendor.get("price_range"):
        y = _center(d, y, _txt(vendor.get("price_range"))[:40], _font(32), BRAND_MAROON, W)
    if vendor.get("experience_years"):
        y = _center(d, y, "%s yrs experience" % _txt(vendor.get("experience_years")), _font(28), BRAND_NAVY, W)
    if vendor.get("verified"):
        y = _center(d, y, "MANA VIVAHA VERIFIED PARTNER", _font(30), (20, 120, 60), W)
    about = str(vendor.get("about") or "").strip()
    if about and (not qr_ready or y < box_guess):
        y += 6
        _ab = _txt(about)
        y = _center(d, y, _ab[:70], _font(24), (90, 90, 90), W)
        if len(_ab) > 70:
            y = _center(d, y, _ab[70:140], _font(24), (90, 90, 90), W)

    # QR + phone box
    phone = "".join(ch for ch in str(vendor.get("whatsapp") or vendor.get("phone") or "") if ch.isdigit())
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data("https://wa.me/91%s?text=%s" % (phone, "Namaste! Mana Vivaha listing chusanu"))
        qr.make()
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        size = 260 if style != "status" else 300
        qr_img = qr_img.resize((size, size))
        img.paste(qr_img, (W - size - 60, H - size - 150))
        qr_ready = True
    except Exception:
        qr_ready = False

    d.rounded_rectangle([60, box_y, W - 60, box_y + (300 if style != "status" else 340)],
                        radius=28, outline=BRAND_GOLD, width=4)
    d.text((100, box_y + 26), "BOOKING / ENQUIRY:", font=_font(30), fill=BRAND_MAROON)
    d.text((100, box_y + 76), "+91 %s" % phone, font=_font(52), fill=BRAND_NAVY)
    _qr_w = (260 if style != "status" else 300) + 60 if qr_ready else 0
    d.text((100, box_y + 152), "WhatsApp cheyyandi - Mana Vivaha\nmember ani cheppandi",
           font=_font(24), fill=(90, 90, 90), spacing=6)
    if not qr_ready:
        d.text((100, box_y + 190), "%s/vendors" % site, font=_font(26), fill=BRAND_NAVY)
    d.text((60, H - 96), "%s/vendors | Vendor ID %s" % (site, vendor.get("id", "")),
           font=_font(24), fill=(120, 120, 120))
    d.rectangle([0, H - 40, W, H], fill=BRAND_NAVY)

    img.save(out_path)
    return out_path
