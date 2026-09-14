"""channel_content.py → cluster + religion (Muslim/Christian) aware content."""
import pathlib

p = pathlib.Path("channel_content.py")
s = p.read_text()

# ---------------------------------------------------------------- title helpers
s = s.replace('''def perfect_title(key: str, ch: Dict | None = None) -> str:''',
'''RELIGION_STATE_TE = {"TS": "తెలంగాణ", "AP": "ఆంధ్రా"}
RELIGION_STATE_EN = {"TS": "Telangana", "AP": "AP"}


def religion_title(key: str, ch: Dict) -> str:
    """☪️ Muslim / ✝️ Christian — state × gender channels ki title."""
    sub = ch.get("sub", "")
    st, g = ch.get("state", "TS"), ch.get("gender", "Bride")
    icon = {"muslim": "☪️", "christian": "✝️"}.get(sub, "💍")
    en = "%s %s %s" % (RELIGION_STATE_EN.get(st, st), sub.title(), ("Brides" if g == "Bride" else "Grooms"))
    te = "%s %s %s" % (RELIGION_STATE_TE.get(st, st), ("ముస్లిం" if sub == "muslim" else "క్రైస్తవ"),
                       ("వధువులు" if g == "Bride" else "వరులు"))
    return "%s %s | %s" % (icon, en, te)


def cluster_title(key: str, ch: Dict) -> str:
    """Caste cluster — pedda community (bride/groom separate) + grouped sub-castes."""
    en = ch.get("cluster_en", "")
    te = ch.get("cluster_te", "")
    if key.endswith("_bride"):
        return "👰 %s Brides | %s వధువులు" % (en, te)
    if key.endswith("_groom"):
        return "🤵 %s Grooms | %s వరులు" % (en, te)
    return "💍 %s Matrimony | %s — వధువులు + వరులు" % (en, te)


def perfect_title(key: str, ch: Dict | None = None) -> str:''', 1)

s = s.replace('''    if key in SPECIAL_TITLE:
        return "%s | %s" % SPECIAL_TITLE[key]
    caste = _caste_key_from_channel(key)''',
'''    if key in SPECIAL_TITLE:
        return "%s | %s" % SPECIAL_TITLE[key]
    ch = ch or {}
    if ch.get("sub") in ("muslim", "christian"):
        return religion_title(key, ch)
    if key.startswith("c_") and ch.get("cluster_en"):
        return cluster_title(key, ch)
    caste = _caste_key_from_channel(key)''', 1)

# ---------------------------------------------------------------- dp text
s = s.replace('''    core = key
    for suf, label in (("_bride", "BRIDES"), ("_groom", "GROOMS")):''',
'''    core = key
    ch = {} if False else None
    for suf, label in (("_bride", "BRIDES"), ("_groom", "GROOMS")):''', 1)

s = s.replace('''def dp_text(key: str) -> Dict[str, str]:
    """DP image lo render ayye text (English — server lo Telugu font ledu)."""
    if key == "official":
        return {"big": "TSAP", "mid": "MATRIMONY", "small": "TS • AP TELUGU"}''',
'''def dp_text(key: str, ch: Dict | None = None) -> Dict[str, str]:
    """DP image lo render ayye text (English — server lo Telugu font ledu)."""
    ch = ch or {}
    if key == "official":
        return {"big": "TSAP", "mid": "MATRIMONY", "small": "TS • AP TELUGU"}
    if ch.get("sub") in ("muslim", "christian"):
        st = {"TS": "TELANGANA", "AP": "AP"}[ch.get("state", "TS")]
        return {"big": ch["sub"].upper(), "mid": "%s %s" % (st, "BRIDES" if ch.get("gender") == "Bride" else "GROOMS"),
                "small": "TS • AP TELUGU"}
    if key.startswith("c_") and ch.get("cluster_en"):
        en = ch["cluster_en"].replace("(", "").replace(")", "").replace("•", " ")
        words = [w for w in en.split() if w]
        if len(word_words := " ".join(words)) > 16:      # noqa: F841  (readability)
            pass
        label = "BRIDES" if key.endswith("_bride") else ("GROOMS" if key.endswith("_groom") else "MATRIMONY")
        return {"big": " ".join(words)[:16].upper(), "mid": label, "small": "TS • AP TELUGU"}''', 1)

# ---------------------------------------------------------------- description
s = s.replace('''    elif key.endswith("_bride") and key.startswith("c_"):
        caste = _caste_key_from_channel(key)
        body = ("%s వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, "
                "3 requests FREE, ₹99లో 5. %s" % (CASTE_TELUGU.get(caste, caste), tags))
    elif key.endswith("_groom") and key.startswith("c_"):
        caste = _caste_key_from_channel(key)
        body = ("%s వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. "
                "3 requests FREE. %s" % (CASTE_TELUGU.get(caste, caste), tags))''',
'''    elif ch.get("sub") in ("muslim", "christian"):
        sub_te = "ముస్లిం" if ch["sub"] == "muslim" else "క్రైస్తవ"
        st_te = RELIGION_STATE_TE.get(ch.get("state", "TS"), "తెలంగాణ")
        st_en = RELIGION_STATE_EN.get(ch.get("state", "TS"), "TS")
        who = "వధువులు" if ch.get("gender") == "Bride" else "వరులు"
        body = ("%s %s %s — %s. ఫోటో గోప్యం, నిజమైన profiles, 3 requests FREE, ₹99లో 5. %s"
                % (st_te, sub_te, who, st_en, tags))
    elif key.startswith("c_") and ch.get("cluster_en"):
        en, te = ch["cluster_en"], ch["cluster_te"]
        mem = " • ".join((ch.get("members") or [])[:5])
        who = ("Brides" if key.endswith("_bride") else "Grooms" if key.endswith("_groom") else "Brides + Grooms")
        body = ("%s — %s (%s). Sub-castes: %s. నిజమైన profiles, 3 requests FREE, ₹99లో 5."
                % (te, en, who, mem))''', 1)

# ---------------------------------------------------------------- pinned welcome (members line)
s = s.replace('''    caste_or_type = ""
    if key.startswith("c_"):
        caste_or_type = CASTE_TELUGU.get(_caste_key_from_channel(key), "")''',
'''    caste_or_type = ""
    if key.startswith("c_"):
        caste_or_type = ch.get("cluster_te") or CASTE_TELUGU.get(_caste_key_from_channel(key), "")
    members_line = ""
    if ch.get("members"):
        members_line = ("👥 ఈ channel లో: *%s*\\n\\n" % " • ".join(ch["members"][:14]))
    if ch.get("sub"):   # Muslim / Christian
        members_line = ("👥 %s %s — %s\\n\\n"
                        % (RELIGION_STATE_EN.get(ch.get("state", "TS"), ""), ch["sub"].title(),
                           ("Catholic • CSI • Baptist • Pentecost • Born Again" if ch["sub"] == "christian"
                            else "Sheikh • Syed • Pathan • Momin • Qureshi • Labbai — antha okate channel")))''', 1)
s = s.replace('''        "%s\\n\\n"
        "ఇక్కడ ఏం దొరుకుతుంది:\\n"''', '''        "%s\\n"
        "%s"
        "ఇక్కడ ఏం దొరుకుతుంది:\\n"''', 1)
s = s.replace('''        % (title, ("*%s*" % caste_or_type) if caste_or_type else "Telugu Matrimony — TS + AP",
           BOT, SITE, SITE, tags, "")''',
'''        % (title, ("*%s*" % caste_or_type) if caste_or_type else "Telugu Matrimony — TS + AP",
           members_line, BOT, SITE, SITE, tags, "")''', 1)

# ---------------------------------------------------------------- CASTE_TELUGU: cluster keys add
s = s.replace('''    "st_others": "ST ఇతరులు",
}''',
'''    "st_others": "ST ఇతరులు",
    # ---- clusters (wave 8 restructure) ----
    "kapu_family": "కాపు • బలిజ • తెలగ", "yadava_goud": "యాదవ • గౌడ • గొల్ల",
    "viswabrahmana": "విశ్వబ్రహ్మణ", "raju_kshatriya": "రాజు • క్షత్రియ",
    "padmashali_weavers": "పద్మశాలి • దేవాంగ", "mudiraj": "ముదిరాజ • తెనుగొల్ల",
    "lambada_banjara": "లంబాడ • బంజార", "others_bc": "ఇతర BC కులాలు",
    "others_sc": "ఇతర SC కులాలు", "others_st": "ఇతర ST కులాలు",
}''', 1)

# ---------------------------------------------------------------- special titles: merged keys
s = s.replace('''    "doctors": ("🩺 Doctors Matrimony", "వైద్యులు"),
    "teachers": ("👩‍🏫 Teachers Matrimony", "ఉపాధ్యాయులు"),''',
'''    "doctors": ("🩺 Doctors Matrimony", "వైద్యులు"),
    "teachers": ("👩‍🏫 Teachers Matrimony", "ఉపాధ్యాయులు"),
    "doctors_teachers": ("🩺 Doctors & Teachers Matrimony", "వైద్యులు + ఉపాధ్యాయులు"),''', 1)

p.write_text(s)
print("channel_content.py → clusters + muslim/christian titles")
