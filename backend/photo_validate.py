"""
📸 WAVE 17 — PHOTO VALIDATION PIPELINE (top-matrimony standard, PIL-only, no numpy/cv2)
=======================================================================================
Top sites (BharatMatrimony/Shaadi) do TWO layers:
  1) AUTOMATIC technical checks  → instant reject with reason (resolution/blur/dark/glare/fake)
  2) HUMAN moderation queue      → admin approve/reject (photo-of-photo, wrong person, groups...)

Ee module = layer 1 (deterministic, explainable). Layer 2 = /api/admin/photos/* queue.

Checks (order):
  FORMAT → SIZE → DIMENSIONS → BRIGHTNESS → FLAT(fakeness) → BLUR → GLARE → FRAME(photo-of-photo)
Returns: {ok, reason, en, te, checks{...}} — reason codes stable for frontend i18n.
"""
from __future__ import annotations

import io

from PIL import Image, ImageFilter, ImageStat

MIN_SIDE = 350          # min(w,h) — kindaki ante LOW_RES (screenshot 5 standard)
MIN_BYTES = 4 * 1024
MAX_BYTES = 5 * 1024 * 1024
DARK_MEAN = 42          # kinda = TOO_DARK
BRIGHT_MEAN = 228       # paina = TOO_BRIGHT (white/overexposed)
FLAT_STD = 11           # kinda = FLAT (single-color / blank / fake)
BLUR_VAR = 250.0        # Laplacian variance (480px) kinda = BLURRY (sharp≈460+, blur≈230)
JPEG_DENSITY = 45.0     # JPEG bytes-per-kilo-pixel kinda = mush/heavy-blur (sharp≈150+, heavy-blur<35)
GLARE_PCT = 12.0        # % pixels >= 250 paina = GLARE (flash / screen reflection)
FRAME_BAND = 0.045      # top+bottom dark band >= 4.5% height each = PHOTO_OF_PHOTO frame
FRAME_DARK = 28         # band mean kinda + center paina → frame undi

REASONS = {
    "OK": ("Photo looks clear ✅", "ఫోటో క్లియర్‌గా ఉంది ✅ — admin approval ki vellindi"),
    "BAD_FORMAT": ("Not a valid photo file", "ఇది సరైన ఫోటో ఫైల్ కాదు — JPG/PNG/WebP pettandi"),
    "TOO_BIG": ("Photo larger than 5 MB", "ఫోటో 5MB కన్నా పెద్దది — చిన్న ఫోటో పంపండి"),
    "TOO_SMALL_FILE": ("Photo file is empty/corrupt", "ఫోటో ఖాళీ/పాడైంది — మళ్లీ upload చెయ్యండి"),
    "LOW_RES": ("Image resolution too low", "ఫోటో resolution చాలా తక్కువ — high-quality original photo pettandi (min 350px)"),
    "TOO_DARK": ("Photo is too dark", "ఫోటో చాలా చీకటిగా ఉంది — వెలుతురులో తీసిన ఫోటో పంపండి"),
    "TOO_BRIGHT": ("Photo is overexposed/blank", "ఫోటో తెల్లగా/మసకగా ఉంది — సరైన ఫోటో పంపండి"),
    "FLAT": ("Not a real photo", "ఇది నిజమైన ఫోటోలా లేదు — మీ original ఫోటో పంపండి"),
    "BLURRY": ("Photo is blurry", "ఫోటో blur గా ఉంది — clear/sharp ఫోటో పంపండి"),
    "GLARE": ("Flash/glare detected — photo of a photo?", "ఫోటోపై flash/glare ఉంది — screen/photo ని తీసినది కాకుండా ORIGINAL ఫోటో పంపండి"),
    "PHOTO_OF_PHOTO": ("Photo of a photo detected", "వేరే ఫోటోని తీసినట్లుంది (frame కనిపిస్తోంది) — ORIGINAL image upload చెయ్యండి"),
}


def _fail(reason, checks):
    en, te = REASONS[reason]
    return {"ok": False, "reason": reason, "en": en, "te": te, "checks": checks}


def _pass(checks):
    en, te = REASONS["OK"]
    return {"ok": True, "reason": "OK", "en": en, "te": te, "checks": checks}


def _laplacian_var(gray: Image.Image) -> float:
    """Blur score — Laplacian variance @480px (ekkuva = sharp). ImageStat = C-speed (~5ms)."""
    g = gray.copy()
    g.thumbnail((480, 480), Image.BILINEAR)
    lap = g.filter(ImageFilter.Kernel((3, 3), (0, 1, 0, 1, -4, 1, 0, 1, 0), scale=1))
    return ImageStat.Stat(lap).var[0]


def validate_photo(data: bytes, filename: str = "", *, selfie: bool = False) -> dict:
    checks: dict = {"bytes": len(data or b"")}
    if not data or len(data) < MIN_BYTES:
        return _fail("TOO_SMALL_FILE", checks)
    if len(data) > MAX_BYTES:
        return _fail("TOO_BIG", checks)
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception:
        return _fail("BAD_FORMAT", checks)
    if img.format not in ("JPEG", "PNG", "WEBP", "MPO"):
        return _fail("BAD_FORMAT", checks)
    w, h = img.size
    checks.update({"format": img.format, "w": w, "h": h,
                   "kb": round(len(data) / 1024, 1)})
    if min(w, h) < (300 if selfie else MIN_SIDE):
        return _fail("LOW_RES", checks)
    gray = img.convert("L") if img.mode != "L" else img
    stat = ImageStat.Stat(gray)
    mean, std = stat.mean[0], stat.stddev[0]
    checks.update({"brightness": round(mean, 1), "contrast_std": round(std, 1)})
    if mean < DARK_MEAN:
        return _fail("TOO_DARK", checks)
    if mean > BRIGHT_MEAN:
        return _fail("TOO_BRIGHT", checks)
    if std < FLAT_STD:
        return _fail("FLAT", checks)
    # NOTE: brightness-structural checks (glare/frame) BEFORE texture (blur) —
    # photo-of-photo re-captures are often soft; report the TRUE reason first.
    # Glare: overexposed pixel share (flash / screen moiré-hotspots)
    small = gray.copy()
    small.thumbnail((200, 200), Image.BILINEAR)
    spx = list(small.getdata())
    hot = sum(1 for p in spx if p >= 250)
    glare_pct = hot * 100.0 / (len(spx) or 1)
    checks["glare_pct"] = round(glare_pct, 1)
    if glare_pct > GLARE_PCT:
        return _fail("GLARE", checks)
    # Frame: dark uniform bands top+bottom (photo-of-photo / screenshot frame)
    band_h = max(1, int(h * FRAME_BAND))
    top = ImageStat.Stat(gray.crop((0, 0, w, band_h)))
    bot = ImageStat.Stat(gray.crop((0, h - band_h, w, h)))
    center = ImageStat.Stat(gray.crop((int(w * 0.25), int(h * 0.35), int(w * 0.75), int(h * 0.65))))
    checks.update({"frame_top": round(top.mean[0], 1), "frame_bottom": round(bot.mean[0], 1),
                   "center": round(center.mean[0], 1)})
    if top.mean[0] < FRAME_DARK and bot.mean[0] < FRAME_DARK and center.mean[0] > 70:
        return _fail("PHOTO_OF_PHOTO", checks)
    blur = _laplacian_var(gray)
    checks["blur_score"] = round(blur, 1)
    if blur < BLUR_VAR:
        return _fail("BLURRY", checks)
    if img.format in ("JPEG", "MPO"):
        density = len(data) / ((w * h) / 1000.0)
        checks["jpeg_density"] = round(density, 1)
        if density < JPEG_DENSITY:
            return _fail("BLURRY", checks)
    return _pass(checks)
