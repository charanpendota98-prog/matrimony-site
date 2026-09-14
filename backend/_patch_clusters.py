"""
CHANNEL RESTRUCTURE (wave 8) — smart clusters.
  * Muslims  → 4 channels (TS/AP × bride/groom), no sub-division
  * Christians → 4 channels (TS/AP × bride/groom)
  * Hindus   → caste CLUSTERS (Viswabrahmana 5 sub-castes = 1 cluster laaga),
               pedda communities ki bride/groom separate, chinna vi single channel
  * 83 → 51 channels
"""
import pathlib
import re

p = pathlib.Path("channels_config.py")
s = p.read_text()

# ===========================================================================
# 1) L2 RELIGION — muslim/christian ni TS/AP × bride/groom ga
# ===========================================================================
old_rel = s[s.index('    "hindu": {'):s.index('    # ===================== LEVEL 3 — HINDU CASTE')]
new_rel = '''    "hindu": {
        "tier": "L2_RELIGION",
        "name": "🕉️ Hindu Matrimony Hub | హిందూ వివాహాలు",
        "username": "manavivaha_hindu",
        "fallbacks": ["manavivaha_hindus", "tsap_hindu"],
        "desc": ("Hindu Telugu matches — anni kulasthulu, anni districts.\\n"
                 "Caste-wise channels kooda undi — profile lo caste filter use cheyyandi.\\n"
                 "manavivaha.in/register • Bot: @telugumatrimony1_bot"),
        "hashtags": ["#Hindu", "#TeluguMatrimony"],
        "wave": 1,
        "live": False,
        "route": {"religion": "Hindu"},
    },
    # ---- MUSLIM (4 — TS/AP × bride/groom; Sheikh/Syed/Pathan antha same channel) ----
    "muslim_ts_bride": {
        "tier": "L2_RELIGION", "sub": "muslim", "state": "TS", "gender": "Bride",
        "religion": "Muslim", "name": "", "desc": "",
        "username": "manavivaha_muslim_ts_bride",
        "fallbacks": ["tsmuslimbride", "mv_muslim_ts_brd", "manavivaha_muslim_ts_brd"],
        "hashtags": ["#Muslim", "#Bride", "#Telangana", "#Nikah"],
        "wave": 1, "live": False, "route": {"religion": "Muslim", "state": "TS", "gender": "Bride"},
    },
    "muslim_ts_groom": {
        "tier": "L2_RELIGION", "sub": "muslim", "state": "TS", "gender": "Groom",
        "religion": "Muslim", "name": "", "desc": "",
        "username": "manavivaha_muslim_ts_groom",
        "fallbacks": ["tsmuslimgroom", "mv_muslim_ts_grm", "manavivaha_muslim_ts_grm"],
        "hashtags": ["#Muslim", "#Groom", "#Telangana", "#Nikah"],
        "wave": 1, "live": False, "route": {"religion": "Muslim", "state": "TS", "gender": "Groom"},
    },
    "muslim_ap_bride": {
        "tier": "L2_RELIGION", "sub": "muslim", "state": "AP", "gender": "Bride",
        "religion": "Muslim", "name": "", "desc": "",
        "username": "manavivaha_muslim_ap_bride",
        "fallbacks": ["apmuslimbride", "mv_muslim_ap_brd", "manavivaha_muslim_ap_brd"],
        "hashtags": ["#Muslim", "#Bride", "#AndhraPradesh", "#Nikah"],
        "wave": 1, "live": False, "route": {"religion": "Muslim", "state": "AP", "gender": "Bride"},
    },
    "muslim_ap_groom": {
        "tier": "L2_RELIGION", "sub": "muslim", "state": "AP", "gender": "Groom",
        "religion": "Muslim", "name": "", "desc": "",
        "username": "manavivaha_muslim_ap_groom",
        "fallbacks": ["apmuslimgroom", "mv_muslim_ap_grm", "manavivaha_muslim_ap_grm"],
        "hashtags": ["#Muslim", "#Groom", "#AndhraPradesh", "#Nikah"],
        "wave": 1, "live": False, "route": {"religion": "Muslim", "state": "AP", "gender": "Groom"},
    },
    # ---- CHRISTIAN (4 — TS/AP × bride/groom; Catholic/CSI/Baptist antha same channel) ----
    "christian_ts_bride": {
        "tier": "L2_RELIGION", "sub": "christian", "state": "TS", "gender": "Bride",
        "religion": "Christian", "name": "", "desc": "",
        "username": "manavivaha_christian_ts_bride",
        "fallbacks": ["tschristianbride", "mv_christ_ts_brd", "manavivaha_christ_ts_brd"],
        "hashtags": ["#Christian", "#Bride", "#Telangana", "#Wedding"],
        "wave": 1, "live": False, "route": {"religion": "Christian", "state": "TS", "gender": "Bride"},
    },
    "christian_ts_groom": {
        "tier": "L2_RELIGION", "sub": "christian", "state": "TS", "gender": "Groom",
        "religion": "Christian", "name": "", "desc": "",
        "username": "manavivaha_christian_ts_groom",
        "fallbacks": ["tschristiangroom", "mv_christ_ts_grm", "manavivaha_christ_ts_grm"],
        "hashtags": ["#Christian", "#Groom", "#Telangana", "#Wedding"],
        "wave": 1, "live": False, "route": {"religion": "Christian", "state": "TS", "gender": "Groom"},
    },
    "christian_ap_bride": {
        "tier": "L2_RELIGION", "sub": "christian", "state": "AP", "gender": "Bride",
        "religion": "Christian", "name": "", "desc": "",
        "username": "manavivaha_christian_ap_bride",
        "fallbacks": ["apchristianbride", "mv_christ_ap_brd", "manavivaha_christ_ap_brd"],
        "hashtags": ["#Christian", "#Bride", "#AndhraPradesh", "#Wedding"],
        "wave": 1, "live": False, "route": {"religion": "Christian", "state": "AP", "gender": "Bride"},
    },
    "christian_ap_groom": {
        "tier": "L2_RELIGION", "sub": "christian", "state": "AP", "gender": "Groom",
        "religion": "Christian", "name": "", "desc": "",
        "username": "manavivaha_christian_ap_groom",
        "fallbacks": ["apchristiangroom", "mv_christ_ap_grm", "manavivaha_christ_ap_grm"],
        "hashtags": ["#Christian", "#Groom", "#AndhraPradesh", "#Wedding"],
        "wave": 1, "live": False, "route": {"religion": "Christian", "state": "AP", "gender": "Groom"},
    },
    "other_religion": {
        "tier": "L2_RELIGION",
        "name": "🕊️ Other Religions | ఇతర మతాలు",
        "username": "manavivaha_other_religions",
        "fallbacks": ["manavivaha_others", "manavivaha_minority"],
        "desc": ("Sikh • Jain • Buddhist • Parsi • Jewish • No-caste/No-religion — Telugu matches.\\n"
                 "Respectful, private, verified. manavivaha.in/register"),
        "hashtags": ["#OtherReligions", "#Respect"],
        "wave": 2, "live": False, "route": {"religion": "Other"},
    },
    "interfaith": {
        "tier": "L2_RELIGION",
        "name": "💞 Inter-Caste & Inter-Faith | ప్రేమ వివాహం",
        "username": "manavivaha_interfaith",
        "fallbacks": ["manavivaha_intercaste", "manavivaha_mixedmarriage"],
        "desc": ("Inter-caste • Inter-religion • Love & Register marriage.\\n"
                 "No-caste filter • Full privacy • Couple corner.\\n"
                 "manavivaha.in/register • Height secret maintain chestham 🤝"),
        "hashtags": ["#Intercaste", "#LoveMarriage", "#RegisterMarriage"],
        "wave": 3, "live": False, "route": {"flag": "interfaith"},
    },

'''
s = s.replace(old_rel, new_rel, 1)

# ===========================================================================
# 2) L3 — 43 caste channels ni CLUSTERS tho replace (smart grouping)
# ===========================================================================
start = s.index('    # ===================== LEVEL 3 — HINDU CASTE')
end = s.index('    # ===================== LEVEL 4 — SPECIAL')
l3_new = '''    # ===================== LEVEL 3 — HINDU CASTE CLUSTERS (smart groups) =====================
    # 🔑 IDEA: Telugu lo konni castes **okka kula group** laage untayi (ex: Viswabrahmana = 5 sub-castes).
    #         Anduke chinna sub-castes ni okate channel lo kalipamu — create cheyyadam suluvu,
    #         audience kooda oke chota vastundi. Pedda communities ki bride/groom **separate** channels.

'''
s = s[:start] + l3_new + s[end:]

# CASTE_SPLIT / SPLIT_MAP block → cluster generator
cs_start = s.index("# ---------------------------------------------------------------------------\n# ⭐ CASTE × GENDER CHANNELS")
cs_end = s.index("# ---------------------------------------------------------------------------\n# PERFECT CONTENT")
clusters_code = '''# ---------------------------------------------------------------------------
# ⭐ CASTE CLUSTERS — "caste prakaram" smart ga (bride/groom + grouped sub-castes)
# ---------------------------------------------------------------------------
# members       : ee channel lo cover ayye sub-castes (pinned post + description lo kanipisthundi)
# split         : True ayithe bride/groom separate channels, False ayithe single (both + hashtag filter)
# category      : OC / BC / SC / ST (coverage report ki)
CASTE_CLUSTERS: List[Dict] = [
    {"key": "reddy", "en": "Reddy", "te": "రెడ్డి", "category": "OC", "split": True, "wave": 1,
     "members": ["Reddy", "Pakanati Reddy", "Motati Reddy", "Gudati Reddy", "Deshathi Reddy"]},
    {"key": "kamma", "en": "Kamma", "te": "కమ్మ", "category": "OC", "split": True, "wave": 1,
     "members": ["Kamma", "Chowdary", "Choudary"]},
    {"key": "kapu", "en": "Kapu • Balija • Telaga", "te": "కాపు • బలిజ • తెలగ", "category": "OC", "split": True, "wave": 1,
     "members": ["Kapu", "Ontari", "Turupu Kapu", "Palli Kapu", "Balija", "Gajula Balija", "Setti Balija",
                 "Surya Balija", "Telaga", "Telagu"]},
    {"key": "velama", "en": "Velama", "te": "వెలమ", "category": "OC", "split": True, "wave": 2,
     "members": ["Velama", "Padma Velama", "Koppula Velama"]},
    {"key": "brahmin", "en": "Brahmin", "te": "బ్రాహ్మణ", "category": "OC", "split": True, "wave": 2,
     "members": ["Vaidiki Brahmin", "Niyogi Brahmin", "Sistla", "Dravida Brahmin", "Iyer"]},
    {"key": "vysya", "en": "Arya Vysya • Komati", "te": "వైశ్య • కోమటి", "category": "OC", "split": True, "wave": 2,
     "members": ["Arya Vysya", "Komati", "Komti", "Vaishya", "Sadhu Chetty"]},
    {"key": "yadava_goud", "en": "Yadava • Goud • Golla", "te": "యాదవ • గౌడ • గొల్ల", "category": "BC", "split": True,
     "wave": 2, "members": ["Yadav", "Yadava", "Golla", "Kuruma", "Kuruba", "Goud", "Gouda", "Ediga",
                            "Gamalla", "Idiga", "Settibalija"]},
    {"key": "mala", "en": "Mala", "te": "మాల", "category": "SC", "split": True, "wave": 2,
     "members": ["Mala", "Mala Ayawaru", "Mala Dasari"]},
    {"key": "madiga", "en": "Madiga", "te": "మాదిగ", "category": "SC", "split": True, "wave": 2,
     "members": ["Madiga", "Madiga Dasu", "Mashteen", "Madiga Dasari"]},
    {"key": "viswabrahmana", "en": "Viswabrahmana (Viswakarma)", "te": "విశ్వబ్రాహ్మణ", "category": "BC",
     "split": False, "wave": 2,
     "members": ["Viswakarma", "Viswabrahmin", "Viswabrahmana", "Kamsali", "Kammari", "Kanchari", "Vadla",
                 "Ausula", "Silpi", "Shilpi", "Vadrangi", "Achari"]},
    {"key": "munnuru_kapu", "en": "Munnuru Kapu", "te": "మున్నూరు కాపు", "category": "BC", "split": False,
     "wave": 2, "members": ["Munnuru Kapu", "Munnuru"]},
    {"key": "raju_kshatriya", "en": "Raju • Kshatriya", "te": "రాజు • క్షత్రియ", "category": "OC", "split": False,
     "wave": 3, "members": ["Raju", "Rajulu", "Kshatriya", "Vanniyar"]},
    {"key": "padmashali_weavers", "en": "Padmashali • Devanga (Weavers)", "te": "పద్మశాలి • దేవాంగ",
     "category": "BC", "split": False, "wave": 3,
     "members": ["Padmashali", "Padmasali", "Sali", "Pattusali", "Thogata", "Devanga", "Devanga Chettiar"]},
    {"key": "mudiraj", "en": "Mudiraj • Tenugollu", "te": "ముదిరాజ • తెనుగొల్ల", "category": "BC", "split": False,
     "wave": 3, "members": ["Mudiraj", "Mudiraju", "Mutrasi", "Tenugollu"]},
    {"key": "lambada_banjara", "en": "Lambada • Banjara (ST)", "te": "లంబాడ • బంజార", "category": "ST",
     "split": False, "wave": 3, "members": ["Lambada", "Lambadi", "Banjara", "Lambani", "Sugali"]},
    {"key": "others_bc", "en": "Other BC Communities", "te": "ఇతర BC కులాలు", "category": "BC", "split": False,
     "wave": 3, "members": ["Kummara", "Kulala", "Salivahana", "Gandla", "Telikula", "Uppara", "Sagara",
                            "Vaddera", "Odde", "Rajaka", "Chakali", "Mangali", "Nayi-Brahmin", "Boya", "Valmiki",
                            "Srisayana", "Segidi", "Gavara", "Bestha", "Gangaputra", "Jalari", "Vadabalija",
                            "Jangam", "Jogi", "Dasari", "Bhatraju", "Kalinga"]},
    {"key": "others_sc", "en": "Other SC Communities", "te": "ఇతర SC కులాలు", "category": "SC", "split": False,
     "wave": 3, "members": ["Adi Andhra", "Adi Dravida", "Arundhatiya", "Relli", "Arwa Mala", "Samban", "Dandasi"]},
    {"key": "others_st", "en": "Other ST Communities", "te": "ఇతర ST కులాలు", "category": "ST", "split": False,
     "wave": 3, "members": ["Koya", "Koitur", "Gond", "Rajgond", "Naikpod", "Chenchu", "Bagata", "Konda Reddi",
                            "Savara", "Andh"]},
]

SPLIT_MAP: Dict[str, Dict[str, str]] = {}      # cluster key -> {"Bride": key, "Groom": key}
CASTE_TO_CLUSTER: Dict[str, str] = {}          # alias/caste → cluster key

for _cl in CASTE_CLUSTERS:
    _ck, _en, _te = _cl["key"], _cl["en"], _cl["te"]
    _slug = _ck
    if _cl["split"]:
        _pair = {}
        for _gender, _suffix, _fb in (("Bride", "bride", "brd"), ("Groom", "groom", "grm")):
            _key = "c_%s_%s" % (_ck, _suffix)
            CHANNELS[_key] = {
                "tier": "L3_CASTE", "cluster": _ck, "cluster_en": _en, "cluster_te": _te,
                "category": _cl.get("category", ""), "members": list(_cl["members"]),
                "name": "", "desc": "",
                "username": ("manavivaha_%s_%s" % (_slug, _suffix))[:32],
                "fallbacks": ["tsap_%s_%s" % (_slug, _suffix), "mv_%s_%s" % (_slug, _fb)],
                "hashtags": ["#%s" % _slug.title().replace("_", ""), "#%s" % _suffix.title(), "#TS", "#AP"],
                "wave": _cl["wave"], "live": False,
                "route": {"caste": _en, "gender": _gender, "cluster": _ck},
            }
            _pair[_gender] = _key
        SPLIT_MAP[_ck] = _pair
    else:
        _key = "c_%s" % _ck
        CHANNELS[_key] = {
            "tier": "L3_CASTE", "cluster": _ck, "cluster_en": _en, "cluster_te": _te,
            "category": _cl.get("category", ""), "members": list(_cl["members"]),
            "name": "", "desc": "",
            "username": ("manavivaha_%s" % _slug)[:32],
            "fallbacks": ["tsap_%s" % _slug, "manavivaha_%s_community" % _slug],
            "hashtags": ["#%s" % _slug.title().replace("_", ""), "#Bride", "#Groom", "#TS", "#AP"],
            "wave": _cl["wave"], "live": False,
            "route": {"caste": _en, "cluster": _ck},
        }
        SPLIT_MAP[_ck] = {"Bride": _key, "Groom": _key}

# alias → cluster (sub-caste names antha okate channel ki)
for _cl in CASTE_CLUSTERS:
    CASTE_TO_CLUSTER[_cl["key"]] = _cl["key"]
    for _m in _cl["members"]:
        CASTE_TO_CLUSTER[_m.strip().lower()] = _cl["key"]

'''
s = s[:cs_start] + clusters_code + s[cs_end:]

# ===========================================================================
# 3) CASTE_ALIASES — cluster keys ki rewrite
# ===========================================================================
a_start = s.index("CASTE_ALIASES = {")
a_end = s.index("RELIGION_ALIASES = {")
aliases = '''CASTE_ALIASES = {
    # ---- OC ----
    "reddy": "reddy", "reddi": "reddy", "pakanati": "reddy", "motati": "reddy",
    "gudati": "reddy", "deshathi": "reddy", "pakanati reddy": "reddy", "reddy(golla)": "reddy",
    "kamma": "kamma", "kammas": "kamma", "chowdary": "kamma", "choudary": "kamma", "kamma chowdary": "kamma",
    "kapu": "kapu", "ontari": "kapu", "turupu kapu": "kapu", "palli kapu": "kapu", "munnuru": "munnuru_kapu",
    "munnuru kapu": "munnuru_kapu", "munnurukapu": "munnuru_kapu",
    "balija": "kapu", "gajula balija": "kapu", "surya balija": "kapu", "setti balija": "kapu",
    "sadhu balija": "kapu", "telaga": "kapu", "telagu": "kapu",
    "velama": "velama", "vellama": "velama", "padma velama": "velama", "koppula velama": "velama",
    "koppula": "velama", "velama(kamma)": "velama",
    "vysya": "vysya", "arya vysya": "vysya", "aryavysya": "vysya", "komati": "vysya", "komti": "vysya",
    "vaishya": "vysya", "vaishya(arya)": "vysya", "sadhu chetty": "vysya",
    "brahmin": "brahmin", "telugu brahmin": "brahmin", "vaidiki": "brahmin", "vaidiki brahmin": "brahmin",
    "niyogi": "brahmin", "niyogi brahmin": "brahmin", "sistla": "brahmin", "dravida brahmin": "brahmin",
    "iyer": "brahmin", "iyengar": "brahmin", "smartha": "brahmin", "srivaishnava": "brahmin",
    "raju": "raju_kshatriya", "rajulu": "raju_kshatriya", "kshatriya": "raju_kshatriya",
    "vanniyar": "raju_kshatriya", "raju(kshatriya)": "raju_kshatriya",
    # ---- BC ----
    "goud": "yadava_goud", "gouda": "yadava_goud", "ediga": "yadava_goud", "gamalla": "yadava_goud",
    "idiga": "yadava_goud", "settibalija": "yadava_goud", "goundla": "yadava_goud", "kalalee": "yadava_goud",
    "yadav": "yadava_goud", "yadava": "yadava_goud", "golla": "yadava_goud", "golla(yadava)": "yadava_goud",
    "kuruma": "yadava_goud", "kuruba": "yadava_goud", "kuruba(golla)": "yadava_goud", "kuruva": "yadava_goud",
    "gorrela": "yadava_goud",
    "viswakarma": "viswabrahmana", "viswabrahmin": "viswabrahmana", "viswabrahmana": "viswabrahmana",
    "kamsali": "viswabrahmana", "kammari": "viswabrahmana", "kanchari": "viswabrahmana",
    "vadla": "viswabrahmana", "ausula": "viswabrahmana", "silpi": "viswabrahmana", "shilpi": "viswabrahmana",
    "vadrangi": "viswabrahmana", "achari": "viswabrahmana", "vishwakarma": "viswabrahmana",
    "padmashali": "padmashali_weavers", "padmasali": "padmashali_weavers", "sali": "padmashali_weavers",
    "pattusali": "padmashali_weavers", "thogata": "padmashali_weavers", "thogata sali": "padmashali_weavers",
    "devanga": "padmashali_weavers", "devanga chettiar": "padmashali_weavers",
    "mudiraj": "mudiraj", "mudiraju": "mudiraj", "mutrasi": "mudiraj", "tenugollu": "mudiraj",
    "kummara": "others_bc", "kulala": "others_bc", "salivahana": "others_bc", "kumbhara": "others_bc",
    "gandla": "others_bc", "telikula": "others_bc", "devathilakula": "others_bc",
    "uppara": "others_bc", "sagara": "others_bc", "sagari": "others_bc", "uppari": "others_bc",
    "vaddera": "others_bc", "vaddelu": "others_bc", "odde": "others_bc", "oddilu": "others_bc",
    "vadde": "others_bc", "rajaka": "others_bc", "chakali": "others_bc", "vannar": "others_bc",
    "agnikulakshatriya": "others_bc", "mangali": "others_bc", "mangala": "others_bc", "nayi": "others_bc",
    "nai": "others_bc", "nayi-brahmin": "others_bc", "bhajanthri": "others_bc",
    "boya": "others_bc", "valmiki": "others_bc", "boya bedar": "others_bc", "nishadi": "others_bc",
    "yellapu": "others_bc", "kirataka": "others_bc",
    "srisayana": "others_bc", "segidi": "others_bc", "jangam": "others_bc", "jangalu": "others_bc",
    "beda jangam": "others_bc", "jogi": "others_bc", "jogula": "others_bc", "dasari": "others_bc",
    "bhatraju": "others_bc", "bhatrajulu": "others_bc", "gavara": "others_bc",
    "kalinga": "others_bc", "kinthala kalinga": "others_bc", "buragam kalinga": "others_bc",
    "bestha": "others_bc", "gangaputra": "others_bc", "gangavar": "others_bc", "jalari": "others_bc",
    "vadabalija": "others_bc",
    # ---- SC ----
    "mala": "mala", "sc-mala": "mala", "sc mala": "mala", "mala ayawaru": "mala", "mala dasari": "mala",
    "madiga": "madiga", "sc-madiga": "madiga", "sc madiga": "madiga", "madiga dasu": "madiga",
    "mashteen": "madiga", "madiga dasari": "madiga",
    "adi andhra": "others_sc", "adi-andhra": "others_sc", "adi dravida": "others_sc",
    "arundhatiya": "others_sc", "sc-others": "others_sc", "sc others": "others_sc",
    "reli": "others_sc", "relli": "others_sc", "arwa mala": "others_sc", "samban": "others_sc",
    "dandasi": "others_sc",
    # ---- ST ----
    "lambada": "lambada_banjara", "lambadi": "lambada_banjara", "st-lambadi": "lambada_banjara",
    "st lambadi": "lambada_banjara", "banjara": "lambada_banjara", "lambani": "lambada_banjara",
    "sugali": "lambada_banjara",
    "koya": "others_st", "koitur": "others_st", "gond": "others_st", "rajgond": "others_st",
    "naikpod": "others_st", "st-others": "others_st", "st others": "others_st", "chenchu": "others_st",
    "andh": "others_st", "bagata": "others_st", "konda reddi": "others_st", "savara": "others_st",
    # ---- Open / no caste ----
    "open": None, "other": None, "others": None, "oc": None, "no caste": None, "caste no bar": None,
}

'''
s = s[:a_start] + aliases + s[a_end:]

# ===========================================================================
# 4) ROUTER — religion × state × gender + clusters + L4 keys
# ===========================================================================
old_route = '''    elif religion == "Muslim":
        ordered.append(("muslim", "religion"))
    elif religion == "Christian":
        ordered.append(("christian", "religion"))
    else:
        ordered.append(("other_religion", "religion=Other"))'''
new_route = '''    elif religion in ("Muslim", "Christian"):
        # ☪️✝️ religion × state × gender = 4 channels (Sheikh/Syed/Catholic/CSI ante okate channel)
        _s = state if state in ("TS", "AP") else "TS"
        ordered.append(("%s_%s_%s" % (religion.lower(), _s.lower(), gender.lower()),
                        "religion=%s + %s + %s" % (religion, _s, gender)))
    else:
        ordered.append(("other_religion", "religion=Other"))'''
assert old_route in s
s = s.replace(old_route, new_route, 1)

# caste routing — cluster based
old_caste = '''            if caste_key in SPLIT_MAP:
                # ⭐ CASTE × GENDER channel (bride/groom separate) — exact reach
                ck = SPLIT_MAP[caste_key].get(gender, caste_key)
                ordered.append((ck, "caste=%s + %s" % (profile.get("caste"), gender)))
            else:
                ordered.append((caste_key, "caste=%s (mixed channel, #%s filter)" % (profile.get("caste"), gender)))'''
new_caste = '''            # ⭐ CLUSTER channel — pedda community ayithe bride/groom separate, chinna vi single
            ck = SPLIT_MAP.get(caste_key, {}).get(gender, "c_%s" % caste_key if "c_" + caste_key in CHANNELS else None)
            if ck and ck in CHANNELS:
                split = bool(SPLIT_MAP.get(caste_key, {}).get("Bride") != SPLIT_MAP.get(caste_key, {}).get("Groom"))
                ordered.append((ck, "cluster=%s + %s%s" % (caste_key, gender,
                                                           "" if split else " (single channel — #%s filter)" % gender)))
            else:
                ordered.append(("c_others_bc", "caste=%s → Other communities channel" % profile.get("caste")))'''
assert old_caste in s
s = s.replace(old_caste, new_caste, 1)

# L4 flag keys — dropped channels → doctors_teachers / interfaith
s = s.replace('''    if physical and physical not in ("normal", "", "none"):
        ordered.append(("differently_abled", f"physical={profile.get('physical_status')}"))
''', "")
s = s.replace('''    if _flag_job(job + " " + education, BLOCK_DOCTOR):
        ordered.append(("doctors", "medical profession"))
    if _flag_job(job, BLOCK_TEACHER):
        ordered.append(("teachers", "teaching profession"))
    if age >= 35:
        ordered.append(("above_35", f"age={age}"))
''', '''    if _flag_job(job + " " + education, BLOCK_DOCTOR) or _flag_job(job, BLOCK_TEACHER):
        ordered.append(("doctors_teachers", "medical/teaching profession"))
''')
s = s.replace('''    # L2b — interfaith / love (optional flag)
    if profile.get("interfaith") or profile.get("love_marriage"):
        ordered.append(("interfaith", "inter-caste/love flag"))''',
'''    # L2b — interfaith / love / no-caste-bar (optional flag)
    if profile.get("interfaith") or profile.get("love_marriage") or profile.get("caste_no_bar"):
        ordered.append(("interfaith", "inter-caste / love / caste-no-bar flag"))''')
# hindu hub skip note la "hindu" key param — fine (key exists)

p.write_text(s)
print("channels_config.py restructured: L2 religion (8) + L3 clusters + aliases + router")
