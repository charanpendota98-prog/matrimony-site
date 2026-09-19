"""
REFERRAL KIT 🎨 — poster card (QR tho) + share texts
====================================================
Referrer ki WhatsApp status / group lo veyyadaniki ready **poster image**:
  * Mee peru + code (LAK42) + link (manavivaha.in/r/LAK42)
  * **QR code** — scan cheste direct register (ref auto-lock)
  * "₹50 per paying referral" offer line + 3 FREE requests
  * Square (1080×1080 — WhatsApp post) + Status (1080×1920 — status/story)

Fonts: server lo Telugu font lekapote English matrame (crash ledu) — DejaVu fallback tho.
"""
from __future__ import annotations

import os
from typing import Dict, Optional

BRAND_MAROON = (122, 12, 46)
BRAND_GOLD = (212, 175, 55)
BRAND_CREAM = (255, 248, 231)
NAVY = (15, 31, 60)

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "channel_assets")
# 🖼️ Referral posters: runtime lo generate avutayi — repo lo pettakoodadu (gitignored folder + /tmp fallback)
POSTER_DIR = os.getenv("REFERRAL_POSTER_DIR", "/tmp/referral_posters")
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _font(size: int, bold: bool = True):
    from PIL import ImageFont
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _qr_image(data: str, size: int):
    """QR generate (qrcode lib ఉంటే). Lekapote None — card లో link text వస్తుంది."""
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        return img.resize((size, size))
    except Exception:
        return None


def _safe(text: str) -> str:
    """Filename safe (code లో weird chars వస్తే bhi path break అవ్వదు)."""
    return "".join(ch for ch in str(text) if ch.isalnum() or ch in "-_")[:24] or "ref"


def poster_card(user: Dict, code: str = "", link: str = "", out_path: Optional[str] = None,
                style: str = "square", site: str = "manavivaha.in") -> str:
    """
    Referral poster card (PNG). style: "square" (1080×1080) | "status" (1080×1920).
    Pillow lekapote — fail avvadu, simple text card ivvadu (path return chestundi).
    """
    from PIL import Image, ImageDraw

    code = (code or user.get("referral_code") or "MV100").upper()
    link = link or user.get("referral_link") or ("https://%s/r/%s" % (site, code))
    name = (user.get("full_name") or user.get("name") or "మన వివాహ Member").strip()[:28]
    W, H = (1080, 1080) if style != "status" else (1080, 1920)
    out_path = out_path or os.path.join(POSTER_DIR, "%s_%s.png" % (_safe(code.lower()), style))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (W, H), BRAND_CREAM)
    d = ImageDraw.Draw(img)

    # top bar — 💍 R13: kotha marriage logo + మన వివాహ
    d.rectangle([0, 0, W, 150], fill=BRAND_MAROON)
    _tx = 48
    try:
        from PIL import Image as _PILImage
        _lp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand", "logo-square-256.png")
        if os.path.exists(_lp):
            _lg = _PILImage.open(_lp).convert("RGBA").resize((104, 104), _PILImage.LANCZOS)
            img.paste(_lg, (48, 23), _lg.split()[3])
            _tx = 180
    except Exception:
        _tx = 48
    d.text((_tx, 36), "మన వివాహ", font=_font(56), fill=BRAND_GOLD)
    d.text((_tx, 106), "TS - AP TELUGU MATRIMONY  |  " + site, font=_font(26, False), fill=BRAND_CREAM)

    y = 200
    d.text((48, y), "REFERRAL BONUS  -  Rs.50", font=_font(66), fill=BRAND_MAROON)
    y += 86
    d.text((48, y), "per paying referral  (everyone)", font=_font(34, False), fill=NAVY)
    y += 70

    # name plate
    d.rounded_rectangle([48, y, W - 48, y + 150], radius=24, fill=(255, 255, 255), outline=BRAND_GOLD, width=3)
    d.text((72, y + 22), "REFERRED BY", font=_font(26, False), fill=(120, 120, 120))
    d.text((72, y + 58), name, font=_font(48), fill=BRAND_MAROON)
    y += 190

    # code plate
    d.rounded_rectangle([48, y, W - 48, y + 170], radius=24, fill=BRAND_MAROON)
    d.text((72, y + 22), "USE MY CODE", font=_font(26, False), fill=BRAND_GOLD)
    d.text((72, y + 58), code, font=_font(84), fill=BRAND_CREAM)
    d.text((W - 460, y + 62), "+1 FREE credit", font=_font(38), fill=BRAND_GOLD)
    d.text((W - 460, y + 112), "for your registration", font=_font(26, False), fill=BRAND_CREAM)
    y += 210

    # QR
    qr_size = 300 if style != "status" else 360
    qr = _qr_image(link, qr_size)
    if qr:
        img.paste(qr, (48, y))
        d.rectangle([46, y - 2, 48 + qr_size + 2, y + qr_size + 2], outline=NAVY, width=3)
        ty = y + 20
    else:
        ty = y
    tx = (48 + qr_size + 40) if qr else 48
    d.text((tx, ty), "SCAN  ->  REGISTER", font=_font(40), fill=NAVY)
    d.text((tx, ty + 62), "or open the link:", font=_font(30, False), fill=(90, 90, 90))
    d.text((tx, ty + 104), link.replace("https://", ""), font=_font(32), fill=BRAND_MAROON)
    d.text((tx, ty + 160), "3 requests FREE", font=_font(34), fill=(0, 128, 96))
    d.text((tx, ty + 205), "Rs.99 = 5 profiles", font=_font(30, False), fill=NAVY)
    d.text((tx, ty + 248), "52 Telegram channels", font=_font(28, False), fill=NAVY)
    y += qr_size + 40

    # bullets
    for line in ["Real profiles  |  Photo private  |  Chatting లేదు",
                 "Numbers share only after both sides agree",
                 "Fraud alerts + verified badges + Telugu support"]:
        d.text((48, y), "• " + line, font=_font(30, False), fill=NAVY)
        y += 46

    # footer
    d.rectangle([0, H - 120, W, H], fill=NAVY)
    d.text((48, H - 90), "Register: %s/r/%s" % (site, code), font=_font(32), fill=BRAND_GOLD)
    d.text((48, H - 48), "Bot: @telugumatrimony1_bot  |  care@manavivaha.in", font=_font(26, False), fill=BRAND_CREAM)

    img.save(out_path, "PNG")
    return out_path


def referral_kit(user: Dict, share_kit: Dict) -> Dict:
    """Share kit + poster cards (square + status) → download links."""
    code = share_kit.get("code") or user.get("referral_code", "")
    link = share_kit.get("link") or user.get("referral_link", "")
    out = {"square": "", "status": "", "errors": []}
    for style in ("square", "status"):
        try:
            path = poster_card(user, code=code, link=link, style=style)
            out[style] = "/api/referral/%s/poster.png?style=%s" % (user.get("tsap_id") or code, style)
            out[style + "_path"] = path
        except Exception as e:
            out["errors"].append("%s: %s" % (style, str(e)[:80]))
    out["message_telugu"] = ("🖼️ Poster ready (square = WhatsApp post, status = story). "
                             "Download చేసి share చెయ్యండి — QR scan చేస్తే direct register!")
    return out
