"""DP text polish — mid-word cuts fix (whole-word fit) + special overrides."""
import pathlib
import re

p = pathlib.Path("channel_content.py")
s = p.read_text()

old = s[s.index('def dp_text(key: str, ch: Dict | None = None) -> Dict[str, str]:'):s.index('def perfect_description(')]
new = '''DP_OVERRIDE: Dict[str, Dict[str, str]] = {
    "nri_global": {"big": "NRI", "mid": "TELUGU", "small": "USA • UK • GULF • CAN"},
    "hindu": {"big": "HINDU", "mid": "MATRIMONY", "small": "TS • AP TELUGU"},
    "other_religion": {"big": "OTHER", "mid": "RELIGIONS", "small": "TS • AP TELUGU"},
    "interfaith": {"big": "INTER", "mid": "CASTE • FAITH", "small": "LOVE & REGISTER"},
    "second_marriage": {"big": "2ND", "mid": "MARRIAGE", "small": "DIVORCEE • WIDOW"},
    "govt_jobs": {"big": "GOVT", "mid": "JOBS", "small": "TEACHER • POLICE • BANK"},
    "software_it": {"big": "SOFTWARE", "mid": "IT JOBS", "small": "HYD • BLR • USA"},
    "doctors_teachers": {"big": "DOCTORS", "mid": "TEACHERS", "small": "MEDICAL • EDU"},
    "success_stories": {"big": "SUCCESS", "mid": "STORIES", "small": "REAL COUPLES"},
    "fraud_alerts": {"big": "FRAUD", "mid": "ALERTS", "small": "STAY SAFE"},
    "bureau_network": {"big": "BUREAU", "mid": "BROKERS", "small": "REFERRAL ₹50"},
}


def _fit_words(text: str, limit: int) -> tuple:
    """Whole words tho fit — 'KAPU BALIJA TELA' la mid-word cut raakunda."""
    words, line, rest = text.split(), [], []
    for w in words:
        if sum(len(x) + 1 for x in line) + len(w) <= limit:
            line.append(w)
        else:
            rest.append(w)
    return " ".join(line), " ".join(rest)


def dp_text(key: str, ch: Dict | None = None) -> Dict[str, str]:
    """DP image lo render ayye text (English — server lo Telugu font ledu)."""
    ch = ch or {}
    if key == "official":
        return {"big": "TSAP", "mid": "MATRIMONY", "small": "TS • AP TELUGU"}
    if key in DP_OVERRIDE:
        return dict(DP_OVERRIDE[key])
    if ch.get("sub") in ("muslim", "christian"):
        st = {"TS": "TELANGANA", "AP": "AP"}.get(ch.get("state", "TS"), "TS")
        return {"big": ch["sub"].upper(),
                "mid": "%s %s" % (st, "BRIDES" if ch.get("gender") == "Bride" else "GROOMS"),
                "small": "TS • AP TELUGU"}
    if key.startswith("c_") and ch.get("cluster_en"):
        label = "BRIDES" if key.endswith("_bride") else ("GROOMS" if key.endswith("_groom") else "MATRIMONY")
        if ch.get("cluster", "").startswith("others_"):
            return {"big": "OTHER", "mid": "%s CASTES" % ch.get("category", ""), "small": "TS • AP TELUGU"}
        parts = [x.strip() for x in re.sub(r"\\([^)]*\\)", "", ch["cluster_en"]).split("•") if x.strip()]
        big, overflow = _fit_words(parts[0].upper(), 13)
        extra = " ".join([overflow] + [p.upper() for p in parts[1:]]).strip()
        small, _drop = _fit_words(extra, 20)
        return {"big": big or parts[0][:12].upper(), "mid": label,
                "small": small or "TS • AP TELUGU"}
    core = key
    for suf, label in (("_bride", "BRIDES"), ("_groom", "GROOMS")):
        if core.endswith(suf):
            core = core[: -len(suf)]
            name = core[2:] if core.startswith("c_") else core
            return {"big": name.replace("_", " ").upper(), "mid": label, "small": "TS • AP TELUGU"}
    if key in ("ts_bride",):
        return {"big": "TS", "mid": "BRIDES", "small": "తెలంగాణ"}
    return {"big": core.replace("_", " ").upper()[:14], "mid": "", "small": "TS • AP TELUGU"}


'''
s = s.replace(old, new, 1)
p.write_text(s)
print("dp_text polished")
