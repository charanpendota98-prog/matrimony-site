"""
మన వివాహ — 10-PORUTHAM (KUNDLI MATCH) ENGINE 🔮
==================================================
Top matrimony sites (Bharat Matrimony, Shaadi) ee feature ni PAID ga ammutunnayi.
Manam free ga compute chesi, cards/requests lo chupistham — ee trust factor valla conversions perugutayi.

Ee module: Telugu traditional 10-porutham tables batti approximate match score.

10 PORUTHAMS (traditional order):
  1. Rasi Porutham        — 6/8 (shashtashtaka) dosham check
  2. Nakshatra Porutham   — nakshatra gana/distance rules
  3. Gana Porutham        — Deva / Manushya / Rakshasa matrix
  4. Yoni Porutham        — animal symbol compatibility (27 nakshatras)
  5. Rajju Porutham       — same rajju = dosham (⚠️ critical)
  6. Vedha Porutham       — vedha pairs (⚠️ critical)
  7. Mahendra Porutham    — count 4,7,10,13,16,19,22,25
  8. Stree Deergha        — groom nunchi bride count ≥ 13
  9. Vashya Porutham      — rasi vashya groups
 10. Rasi Adhipathi       — rasi lord relation

⚠️ Idi traditional tables batti *approximate* calculation (software estimate).
   Final ga purohit / panchangam tho confirm cheyyandi — mana site lo ala ne cheptham (honest).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# ------------------------------------------------------------------ 27 NAKSHATRAS
NAKSHATRAS = [
    "ashwini", "bharani", "krittika", "rohini", "mrigasira", "ardra", "punarvasu", "pushya",
    "ashlesha", "magha", "pubba", "uttara", "hasta", "chitra", "swati", "vishakha",
    "anuradha", "jyeshtha", "moola", "purvashadha", "uttarashadha", "shravana", "dhanishta",
    "shatabhisha", "purvabhadra", "uttarabhadra", "revati",
]
NAKSHATRA_TELUGU = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి",
    "ఆశ్లేష", "మఘ", "పూర్వ ఫల్గుణి", "ఉత్తర ఫల్గుణి", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ",
    "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ",
    "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి",
]
# spelling variants (users ala type chestharu)
NAK_ALIASES = {
    "aswini": 0, "aswani": 0, "pubbha": 10, "pubba": 10, "purvaphalguni": 10, "p phalguni": 10,
    "uttaraphalguni": 11, "u phalguni": 11, "utthara": 11, "uttara": 11, "hastha": 12,
    "chitta": 13, "swathi": 14, "visakha": 15, "vishaka": 15, "anooradha": 16, "anuraadha": 16,
    "jyeshta": 17, "jyesta": 17, "moola": 18, "mula": 18, "poorvashadha": 19, "purvashada": 19,
    "uttarashada": 20, "sravana": 21, "sravanam": 21, "sravan": 21, "dhanista": 22, "danishta": 22,
    "satabhisha": 23, "shatabhisa": 23, "sathabhisha": 23, "purvabhadra": 24, "uttarabhadra": 25,
    "revathi": 26, "rohini": 3, "krithika": 2, "karthika": 2, "mrugasira": 4, "mrigashira": 4,
    "arudra": 5, "punarvsu": 6, "pushyami": 7, "aslesha": 8, "magha": 9, "makha": 9,
}

# ------------------------------------------------------------------ 12 RASI
RASIS = ["mesha", "vrishabha", "mithuna", "karkataka", "simha", "kanya",
         "tula", "vrishchika", "dhanu", "makara", "kumbha", "meena"]
RASI_TELUGU = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య",
               "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]
RASI_LORDS = ["Mars (Kuja)", "Venus (Shukra)", "Mercury (Budha)", "Moon (Chandra)", "Sun (Surya)",
              "Mercury (Budha)", "Venus (Shukra)", "Mars (Kuja)", "Jupiter (Guru)", "Saturn (Shani)",
              "Saturn (Shani)", "Jupiter (Guru)"]
RASI_ALIASES = {"vrushabha": 1, "vruschika": 7, "vrischika": 7, "dhanussu": 8, "meenam": 11,
                "kumbham": 10, "makaram": 9, "mesham": 0, "karkatakam": 3, "simham": 4,
                "kanyam": 5, "tulam": 6, "mithunam": 2}

# nakshatra → rasi (moon sign): nakshatras 1-9 Bharani..? (Ashwini starts Mesha; 9 nakshatras per... )
# Traditional: each rasi has 2¼ nakshatras. Ashwini(1)-Bharani(2)+1/4 Krittika = Mesha ...
NAK_TO_RASI = ([0] * 2 + [1] * 3 + [1] + [2] * 2 + [3] * 3 + [4] * 2 + [5] * 2 +
               [6] * 2 + [7] * 3 + [8] * 3 + [9] * 2 + [10] * 2 + [11] * 2)  # 27 entries approx
NAK_TO_RASI = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 11]

# ------------------------------------------------------------------ GANA
GANA = {}
for i in [0, 4, 6, 7, 12, 14, 21, 26]:
    GANA[i] = "Deva"
for i in [1, 3, 5, 10, 11, 16, 20, 24]:
    GANA[i] = "Manushya"
for i in [2, 8, 9, 13, 15, 17, 18, 22, 23, 25]:
    GANA[i] = "Rakshasa"
# Gana matrix (bride→groom) standard: Deva-Manushya=good, same=good, Rakshasa mismatches = not good
GANA_MATRIX = {
    ("Deva", "Deva"): 2, ("Deva", "Manushya"): 2, ("Deva", "Rakshasa"): 0,
    ("Manushya", "Deva"): 1, ("Manushya", "Manushya"): 2, ("Manushya", "Rakshasa"): 1,
    ("Rakshasa", "Deva"): 0, ("Rakshasa", "Manushya"): 1, ("Rakshasa", "Rakshasa"): 2,
}

# ------------------------------------------------------------------ YONI
YONI = ["Horse", "Elephant", "Sheep", "Serpent", "Serpent", "Dog", "Cat", "Sheep", "Cat", "Rat",
        "Rat", "Cow", "Buffalo", "Tiger", "Buffalo", "Tiger", "Deer", "Deer", "Dog", "Monkey",
        "Mongoose", "Monkey", "Lion", "Horse", "Lion", "Cow", "Elephant"]
YONI_ENEMIES = {("Cow", "Tiger"), ("Elephant", "Lion"), ("Horse", "Buffalo"), ("Dog", "Deer"),
                ("Cat", "Rat"), ("Monkey", "Sheep"), ("Mongoose", "Serpent")}

# ------------------------------------------------------------------ RAJJU (⚠️ critical)
RAJJU_GROUPS = {
    "Pada": [0, 8, 9, 17, 18, 26],
    "Kati": [1, 7, 10, 16, 19, 25],
    "Nabhi": [2, 6, 11, 15, 20, 24],
    "Kantha": [3, 5, 12, 14, 21, 23],
    "Siro": [4, 13, 22],
}
RAJJU_TELUGU = {"Pada": "పాద రజ్జు", "Kati": "కటి రజ్జు", "Nabhi": "నాభి రజ్జు",
                "Kantha": "కంఠ రజ్జు", "Siro": "శిరో రజ్జు"}

# ------------------------------------------------------------------ VEDHA (⚠️ critical)
VEDHA_PAIRS = [(0, 17), (1, 16), (2, 15), (3, 14), (5, 21), (6, 20), (7, 19), (8, 18),
               (9, 26), (10, 25), (11, 24), (12, 23), (13, 22)]

# ------------------------------------------------------------------ VASHYA (rasi → primary group)
VASHYA_BY_RASI = {
    0: ["Chatuspada"],            # Mesha — ram (4 legs)
    1: ["Chatuspada"],            # Vrishabha — bull
    2: ["Manava"],                # Mithuna — human
    3: ["Jalachara"],             # Karkataka — crab (water)
    4: ["Vanachara"],             # Simha — lion (wild)
    5: ["Manava"],                # Kanya — maiden
    6: ["Manava"],                # Tula — human
    7: ["Keeta"],                 # Vrishchika — insect
    8: ["Manava", "Vanachara"],   # Dhanu — half man, half animal
    9: ["Chatuspada"],            # Makara — crocodile/4-leg (chatushpada per tradition)
    10: ["Manava"],               # Kumbha — human
    11: ["Jalachara"],            # Meena — fish
}
VASHYA_FRIENDS = {("Chatuspada", "Vanachara"), ("Manava", "Chatuspada")}

# ------------------------------------------------------------------ VEDHA (⚠️ critical)


def norm_nakshatra(value: str) -> Optional[int]:
    """Star name (English/Telugu/spelling variants) → 0-based index."""
    if not value:
        return None
    v = str(value).strip().lower().replace("  ", " ")
    if v in NAK_ALIASES:
        return NAK_ALIASES[v]
    for i, n in enumerate(NAKSHATRAS):
        if v == n or v in n or n in v:
            return i
    for i, t in enumerate(NAKSHATRA_TELUGU):
        if t and t in str(value):
            return i
    return None


def norm_rasi(value: str) -> Optional[int]:
    if not value:
        return None
    v = str(value).strip().lower().replace("  ", " ")
    if v in RASI_ALIASES:
        return RASI_ALIASES[v]
    for i, r in enumerate(RASIS):
        if v == r or v in r or r in v:
            return i
    for i, t in enumerate(RASI_TELUGU):
        if t and t in str(value):
            return i
    return None


def _count(a: int, b: int) -> int:
    """a nunchi b varaku count (1-based, 27 range)."""
    return ((b - a) % 27) + 1


def _rajju(idx: int) -> str:
    for name, group in RAJJU_GROUPS.items():
        if idx in group:
            return name
    return "?"


def _vedha(a: int, b: int) -> bool:
    return (a, b) in VEDHA_PAIRS or (b, a) in VEDHA_PAIRS


def compute_porutham(bride: Dict, groom: Dict) -> Dict:
    """
    Bride + groom (star/rasi fields unna profiles) → 10-porutham result.
    Returns: score (0-10), verdict, per-item list, dosha flags, Telugu summary.
    """
    b_star_raw, g_star_raw = bride.get("star") or bride.get("moola_nakshatram") or "", \
        groom.get("star") or groom.get("moola_nakshatram") or ""
    b_star, g_star = norm_nakshatra(b_star_raw), norm_nakshatra(g_star_raw)
    b_rasi_raw, g_rasi_raw = bride.get("rasi") or "", groom.get("rasi") or ""
    b_rasi, g_rasi = norm_rasi(b_rasi_raw), norm_rasi(g_rasi_raw)
    if b_rasi is None and b_star is not None:
        b_rasi = NAK_TO_RASI[b_star]
    if g_rasi is None and g_star is not None:
        g_rasi = NAK_TO_RASI[g_star]

    items: List[Dict] = []
    if b_star is None or g_star is None:
        return {
            "available": False,
            "reason": "Star (nakshatram) details రెండు profiles లో లేవు — పొరుతం calculate cheyyadam లేదు",
            "score": 0, "max_score": 10, "verdict": "Data saripoledu",
            "items": [], "doshas": [],
            "advice_telugu": "Register లో 'Star / Nakshatram' fill చెయ్యండి — appudu పొరుతం (10 points) automatic గా వస్తుంది.",
        }

    # 1. Rasi porutham (shashtashtaka 6/8 dosham)
    dist = ((b_rasi - g_rasi) % 12) + 1
    rasi_ok = dist not in (6, 8)
    items.append({"no": 1, "name": "రాశి పొరుతం", "telugu": "రాశి పొరుత్తం", "pass": rasi_ok,
                  "note": ("రాశి distances బాగున్నాయి" if rasi_ok else
                           f"రాశి {dist}వ స్థానం — షష్టాష్టక (6/8) దోషం, పరిహారం అవసరం")})

    # 2. Nakshatra porutham (vedha kakunda — general nakshatra distance)
    nak_count = _count(g_star, b_star)
    nak_ok = not _vedha(b_star, g_star)
    items.append({"no": 2, "name": "Nakshatra పొరుతం", "telugu": "నక్షత్ర పొరుత్తం", "pass": nak_ok,
                  "note": (f"Nakshatra count {nak_count} — ok" if nak_ok else "వేధ ఉంది (క్రింద చూడండి)")})

    # 3. Gana
    bg, gg = GANA.get(b_star, "Manushya"), GANA.get(g_star, "Manushya")
    gana_score = GANA_MATRIX.get((bg, gg), 1)
    items.append({"no": 3, "name": "Gana పొరుతం", "telugu": "గణ పొరుత్తం", "pass": gana_score >= 1,
                  "note": f"Bride {bg} • Groom {gg} — " + ("బాగుంది" if gana_score == 2 else
                                                            ("పర్వాలేదు" if gana_score == 1 else "రాక్షస గణం — సరిపోదు"))})

    # 4. Yoni
    by, gy = YONI[b_star], YONI[g_star]
    enemy = (by, gy) in YONI_ENEMIES or (gy, by) in YONI_ENEMIES
    yoni_ok = not enemy
    items.append({"no": 4, "name": "Yoni పొరుతం", "telugu": "యోని పొరుత్తం", "pass": yoni_ok,
                  "note": f"{by} ↔ {gy}" + (" — శత్రు యోనులు (కలహం రిస్క్)" if enemy else " — అనుకూలం")})

    # 5. Rajju (critical)
    br, gr = _rajju(b_star), _rajju(g_star)
    rajju_ok = br != gr
    items.append({"no": 5, "name": "Rajju పొరుతం", "telugu": "రజ్జు పొరుత్తం", "pass": rajju_ok,
                  "note": (f"{RAJJU_TELUGU.get(br, br)} ≠ {RAJJU_TELUGU.get(gr, gr)} — మంచిది" if rajju_ok
                           else f"ఇద్దరికీ {RAJJU_TELUGU.get(br, br)} — రజ్జు దోషం ⚠️ (పెద్దలను సంప్రదించండి)")})

    # 6. Vedha (critical)
    vedha = _vedha(b_star, g_star)
    items.append({"no": 6, "name": "Vedha పొరుతం", "telugu": "వేధ పొరుత్తం", "pass": not vedha,
                  "note": ("వేధ లేదు — మంచిది" if not vedha else
                           f"{NAKSHATRA_TELUGU[b_star]} ↔ {NAKSHATRA_TELUGU[g_star]} — వేధ ఉంది ⚠️")})

    # 7. Mahendra
    m_count = _count(b_star, g_star)
    mahendra_ok = m_count in (4, 7, 10, 13, 16, 19, 22, 25)
    items.append({"no": 7, "name": "Mahendra పొరుతం", "telugu": "మహేంద్ర పొరుత్తం", "pass": mahendra_ok,
                  "note": f"Count {m_count} — " + ("అనుకూలం" if mahendra_ok else "అనుకూలం కాదు (4,7,10,13,16,19,22,25 మంచివి)")})

    # 8. Stree Deergha
    sd_count = _count(g_star, b_star)
    sd_ok = sd_count >= 13
    items.append({"no": 8, "name": "Stree Deergha", "telugu": "స్త్రీ దీర్ఘ పొరుత్తం", "pass": sd_ok,
                  "note": f"Count {sd_count} — " + ("అనుకూలం (దీర్ఘ సుమంగళి)" if sd_ok else "13+ ఉండాలి — సరిపోదు")})

    # 9. Vashya
    bv = VASHYA_BY_RASI.get(b_rasi, [])
    gv = VASHYA_BY_RASI.get(g_rasi, [])
    vashya_ok = bool(set(bv) & set(gv)) or any((a, c) in VASHYA_FRIENDS or (c, a) in VASHYA_FRIENDS
                                              for a in bv for c in gv)
    items.append({"no": 9, "name": "Vashya పొరుతం", "telugu": "వశ్య పొరుత్తం", "pass": vashya_ok,
                  "note": f"{RASI_TELUGU[b_rasi]} ↔ {RASI_TELUGU[g_rasi]} ({'/'.join(bv) or '?'} ↔ {'/'.join(gv) or '?'}) — "
                          + ("అనుకూలం" if vashya_ok else "వశ్యం సరిపోదు — ఒకరు ఒకరిని ఆధీనం చేసుకోలేరు")})

    # 10. Rasi Adhipathi
    b_lord = RASI_LORDS[b_rasi] if b_rasi is not None else "?"
    g_lord = RASI_LORDS[g_rasi] if g_rasi is not None else "?"
    friends = {("Mars (Kuja)", "Sun (Surya)"), ("Sun (Surya)", "Mars (Kuja)"),
               ("Jupiter (Guru)", "Sun (Surya)"), ("Sun (Surya)", "Jupiter (Guru)"),
               ("Venus (Shukra)", "Saturn (Shani)"), ("Saturn (Shani)", "Venus (Shukra)"),
               ("Mercury (Budha)", "Venus (Shukra)"), ("Venus (Shukra)", "Mercury (Budha)"),
               ("Moon (Chandra)", "Sun (Surya)"), ("Sun (Surya)", "Moon (Chandra)")}
    lord_ok = b_lord == g_lord or (b_lord, g_lord) in friends
    items.append({"no": 10, "name": "రాశి Adhipathi", "telugu": "రాశి అధిపతి పొరుత్తం", "pass": lord_ok,
                  "note": f"{b_lord} ↔ {g_lord} — " + ("స్నేహితులు" if lord_ok else "సంబంధం బలహీనం")})

    score = len([i for i in items if i["pass"]])
    doshas = [i["name"] for i in items if not i["pass"] and i["no"] in (5, 6)]
    critical_miss = bool([i for i in items if not i["pass"] and i["no"] in (5, 6)])
    if score >= 8 and not critical_miss:
        verdict, stars = "⭐ అద్భుతం — ఈ పొరుత్తం చాలా మంచిది", 5
    elif score >= 6 and not critical_miss:
        verdict, stars = "✅ మంచిది — చాలా వరకు పొరుత్తాలు కలుస్తున్నాయి", 4
    elif critical_miss:
        verdict, stars = "⚠️ రజ్జు/వేధ దోషం — పెద్దలు + పురోహితులతో చర్చించండి", 2
    else:
        verdict, stars = "🟡 మధ్యస్థం — 5–6 పొరుత్తాలు మాత్రమే, పరిహారం చూడండి", 3

    return {
        "available": True,
        "bride_star": NAKSHATRA_TELUGU[b_star], "groom_star": NAKSHATRA_TELUGU[g_star],
        "bride_star_en": NAKSHATRAS[b_star].title(), "groom_star_en": NAKSHATRAS[g_star].title(),
        "bride_rasi": RASI_TELUGU[b_rasi], "groom_rasi": RASI_TELUGU[g_rasi],
        "score": score, "max_score": 10,
        "percent": int(score * 10),
        "stars": stars,
        "verdict": verdict,
        "items": items,
        "doshas": doshas,
        "advice_telugu": (
            "Idi traditional పొరుత్తం tables batti software estimate. Final గా పురోహితుడు / పంచాంగం తో confirm చెయ్యండి."
            + (" ⚠️ రజ్జు/వేధ దోషం ఉంది — పరిహారం (శాంతి) ఉంటేనే ముందుకు వెళ్ళండి." if critical_miss else "")
        ),
    }


def porutham_line(bride: Dict, groom: Dict) -> str:
    """WhatsApp/card message లో చూపించడానికి ఒక్క line (short)."""
    r = compute_porutham(bride, groom)
    if not r.get("available"):
        return "🔮 పొరుతం: star details లేవు (register లో fill చెయ్యండి)"
    return f"🔮 పొరుతం: {r['score']}/10 {r['verdict'].split('—')[0].strip()}"


if __name__ == "__main__":  # demo: python porutham.py
    b = {"star": "Rohini", "rasi": "Vrishabha"}
    g = {"star": "Mrigasira", "rasi": "Vrishabha"}
    import json
    print(json.dumps(compute_porutham(b, g), ensure_ascii=False, indent=2))
