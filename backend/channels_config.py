"""
Mana Vivaha (TSAP Matrimony) — MASTER CHANNEL REGISTRY + AUTO-ROUTER
====================================================================
One profile post → automatic ga annni relevant channels lo ki vellali.
Idi single source of truth: backend, bot, website anni ikkada nunchi chaduvutayi.

LEVELS:
  L0 OFFICIAL   — 1  (brand hub, top-3/day, success stories)
  L1 REGION     — 5  (TS Bride/Groom, AP Bride/Groom, NRI/Other-States)
  L2 RELIGION   — 5  (Hindu, Muslim, Christian, Other, Inter-Faith)
  L3 CASTE      — 43 (Hindu caste-wise — ONE channel per caste, hashtag filter)
  L4 SPECIAL    — 11 (2nd marriage, differently-abled, govt job, IT, doctors...)
  ---------------------------------------------------------------
  TOTAL         — 65 channels

IMPORTANT RULES:
  * Username okkate Telegram lo unique — conflict ayithe FALLBACK list chudu.
  * LIVE channels (ts_bride, ts_groom) already create ayyayi — vaatini never break.
  * Max 5 channels per profile auto-post (spam taggadaniki) — priority order lo.
"""

from typing import Dict

BOT_USERNAME = "@telugumatrimony1_bot"
BRAND = "Mana Vivaha"
LEGAL_BRAND = "TSAP Matrimony"
SITE = "https://manavivaha.in"

# ---------------------------------------------------------------------------
# CHANNEL REGISTRY
# ---------------------------------------------------------------------------
# key: {
#   "name": Telugu+English display name,
#   "username": Telegram username (without @),
#   "fallbacks": [alternate usernames if taken],
#   "desc": channel description to paste in Telegram,
#   "hashtags": always-on hashtags for that channel,
#   "wave": launch wave,
#   "live": True if already created + bot admin,
# }
# ---------------------------------------------------------------------------

CHANNELS = {
    # ===================== LEVEL 0 — OFFICIAL =====================
    "official": {
        "tier": "L0_OFFICIAL",
        "name": "📢 Mana Vivaha Official | TS-AP Matrimony",
        "username": "TSAP_MATRIMONY",
        "fallbacks": ["manavivaha", "manavivaha_official", "manavivaha_hub"],
        "desc": ("Mana Vivaha — TS & AP No.1 Telugu Matrimony 🇮🇳\n"
                 "₹99 ke Sambandham • Modati 3 FREE\n"
                 "Daily Top-3 matches, success stories, mosam jagratha alerts.\n"
                 "Website: manavivaha.in • Bot: @telugumatrimony1_bot"),
        "hashtags": ["#ManaVivaha", "#TSAPMatrimony", "#99keSambandham"],
        "wave": 1,
        "live": False,
        "route": "digest",  # only top-3/day, not every profile
    },

    # ===================== LEVEL 1 — REGION =====================
    "ts_bride": {
        "tier": "L1_REGION",
        "name": "👰 TS Brides | తెలంగాణ వధువులు",
        "username": "TSBRIDE",
        "fallbacks": ["manavivaha_ts_bride", "tsbrides"],
        "desc": ("Telangana ammayilu — anni kulasthulu.\n"
                 "Daily 10+ kotha profiles • Photo verified • ID search.\n"
                 "Register FREE: manavivaha.in/register • Bot: @telugumatrimony1_bot"),
        "hashtags": ["#TSBride", "#Telangana", "#Ammaayi"],
        "wave": 1,
        "live": True,
        "route": {"state": "TS", "gender": "Bride"},
    },
    "ts_groom": {
        "tier": "L1_REGION",
        "name": "🤵 TS Grooms | తెలంగాణ వరులు",
        "username": "TSGROOM1",
        "fallbacks": ["manavivaha_ts_groom", "tsgroom"],
        "desc": ("Telangana abbayilu — anni kulasthulu.\n"
                 "Daily 10+ kotha profiles • Photo verified • ID search.\n"
                 "Register FREE: manavivaha.in/register • Bot: @telugumatrimony1_bot"),
        "hashtags": ["#TSGroom", "#Telangana", "#Abbaayi"],
        "wave": 1,
        "live": True,
        "route": {"state": "TS", "gender": "Groom"},
    },
    "ap_bride": {
        "tier": "L1_REGION",
        "name": "👰 AP Brides | ఆంధ్రా వధువులు",
        "username": "APBRIDE",
        "fallbacks": ["manavivaha_ap_bride", "apbride1", "manavivaha_apbride"],
        "desc": ("Andhra Pradesh ammayilu — 26 districts cover.\n"
                 "Daily kotha profiles • Register FREE: manavivaha.in/register"),
        "hashtags": ["#APBride", "#AndhraPradesh"],
        "wave": 1,
        "live": False,
        "route": {"state": "AP", "gender": "Bride"},
    },
    "ap_groom": {
        "tier": "L1_REGION",
        "name": "🤵 AP Grooms | ఆంధ్రా వరులు",
        "username": "APGROOM1",
        "fallbacks": ["manavivaha_ap_groom", "apgroom", "manavivaha_apgroom"],
        "desc": ("Andhra Pradesh abbayilu — 26 districts cover.\n"
                 "Daily kotha profiles • Register FREE: manavivaha.in/register"),
        "hashtags": ["#APGroom", "#AndhraPradesh"],
        "wave": 1,
        "live": False,
        "route": {"state": "AP", "gender": "Groom"},
    },
    "nri_global": {
        "tier": "L1_REGION",
        "name": "🌍 NRI & Other States | విదేశాల తెలుగు",
        "username": "manavivaha_nri",
        "fallbacks": ["manavivaha_global", "manavivaha_usa"],
        "desc": ("USA • UK • Canada • Australia • Gulf • Singapore — Telugu NRI matches.\n"
                 "Visa/PR/job status mention cheyyandi. manavivaha.in • @telugumatrimony1_bot"),
        "hashtags": ["#NRI", "#TeluguAbroad", "#GlobalTelugu"],
        "wave": 2,
        "live": False,
        "route": {"state": "Other"},
    },

    # ===================== LEVEL 2 — RELIGION =====================
    "hindu": {
        "tier": "L2_RELIGION",
        "name": "🕉️ Hindu Matrimony | హిందూ వివాహాలు",
        "username": "manavivaha_hindu",
        "fallbacks": ["manavivaha_hindus", "tsap_hindu"],
        "desc": ("Hindu Telugu matches — anni kulasthulu, anni districts.\n"
                 "Caste-wise channels kooda undi — profile search: caste filter use cheyyandi.\n"
                 "manavivaha.in/register"),
        "hashtags": ["#Hindu", "#TeluguMatrimony"],
        "wave": 2,
        "live": False,
        "route": {"religion": "Hindu"},
    },
    "muslim": {
        "tier": "L2_RELIGION",
        "name": "☪️ Muslim Matrimony | ముస్లిం వివాహాలు",
        "username": "manavivaha_muslim",
        "fallbacks": ["manavivaha_muslims", "tsap_muslim"],
        "desc": ("Muslim Telugu matches — Sheikh, Syed, Pathan, Momin, Qureshi, Labbai...\n"
                 "Bride & Groom rendu — hashtag tho filter: #Bride #Groom #Sheikh #Syed\n"
                 "manavivaha.in/register • Bot: @telugumatrimony1_bot"),
        "hashtags": ["#Muslim", "#Nikah", "#TeluguMuslim"],
        "wave": 2,
        "live": False,
        "route": {"religion": "Muslim"},
    },
    "christian": {
        "tier": "L2_RELIGION",
        "name": "✝️ Christian Matrimony | క్రైస్తవ వివాహాలు",
        "username": "manavivaha_christian",
        "fallbacks": ["manavivaha_christians", "tsap_christian"],
        "desc": ("Christian Telugu matches — Catholic, CSI, Baptist, Pentecost, Born Again.\n"
                 "Bride & Groom rendu — filter: #Catholic #CSI #Baptist\n"
                 "manavivaha.in/register"),
        "hashtags": ["#Christian", "#TeluguChristian", "#Wedding"],
        "wave": 2,
        "live": False,
        "route": {"religion": "Christian"},
    },
    "other_religion": {
        "tier": "L2_RELIGION",
        "name": "🕊️ Other Religions | ఇతర మతాలు",
        "username": "manavivaha_other_religions",
        "fallbacks": ["manavivaha_others", "manavivaha_minority"],
        "desc": ("Sikh • Jain • Buddhist • Parsi • Jewish • No-caste/No-religion — Telugu matches.\n"
                 "Respectful, private, verified. manavivaha.in/register"),
        "hashtags": ["#OtherReligions", "#Respect"],
        "wave": 3,
        "live": False,
        "route": {"religion": "Other"},
    },
    "interfaith": {
        "tier": "L2_RELIGION",
        "name": "💞 Inter-Caste & Inter-Faith | ప్రేమ వివాహం",
        "username": "manavivaha_interfaith",
        "fallbacks": ["manavivaha_intercaste", "manavivaha_mixedmarriage"],
        "desc": ("Inter-caste • Inter-religion • Love & Register marriage.\n"
                 "No-caste filter • Full privacy • Couple corner.\n"
                 "manavivaha.in/register • Height secret maintain chestham 🤝"),
        "hashtags": ["#Intercaste", "#LoveMarriage", "#RegisterMarriage"],
        "wave": 3,
        "live": False,
        "route": {"flag": "interfaith"},
    },

    # ===================== LEVEL 3 — HINDU CASTE (43) =====================
    # ---- OC / Forward (7) ----
    "reddy": {"tier": "L3_CASTE", "name": "💍 Reddy Matrimony | TS-AP",
              "username": "manavivaha_reddy", "fallbacks": ["tsap_reddy", "manavivaha_reddys"],
              "desc": "Reddy brides & grooms — TS + AP anni districts. #Bride #Groom #Nalgonda #Hyderabad",
              "hashtags": ["#Reddy"], "wave": 1, "live": False, "route": {"caste": "Reddy"}},
    "kamma": {"tier": "L3_CASTE", "name": "💍 Kamma Matrimony | TS-AP",
              "username": "manavivaha_kamma", "fallbacks": ["tsap_kamma", "manavivaha_kammas"],
              "desc": "Kamma brides & grooms — Guntur, Krishna, Prakasam, Khammam, Hyderabad.",
              "hashtags": ["#Kamma"], "wave": 1, "live": False, "route": {"caste": "Kamma"}},
    "kapu": {"tier": "L3_CASTE", "name": "💍 Kapu Matrimony | TS-AP",
             "username": "manavivaha_kapu", "fallbacks": ["tsap_kapu", "manavivaha_kapus"],
             "desc": "Kapu • Telaga • Balija • Ontari — united Kapu community matches.",
             "hashtags": ["#Kapu", "#Telaga", "#Balija"], "wave": 1, "live": False, "route": {"caste": "Kapu"}},
    "velama": {"tier": "L3_CASTE", "name": "💍 Velama Matrimony | TS-AP",
               "username": "manavivaha_velama", "fallbacks": ["tsap_velama"],
               "desc": "Velama + Koppula Velama + Padma Velama matches — TS + AP.",
               "hashtags": ["#Velama"], "wave": 1, "live": False, "route": {"caste": "Velama"}},
    "vysya": {"tier": "L3_CASTE", "name": "💍 Arya Vysya / Komati Matrimony",
              "username": "manavivaha_vysya", "fallbacks": ["tsap_vysya", "manavivaha_aryavysya"],
              "desc": "Arya Vysya • Komati • Vaishya • Vysya — business families welcome.",
              "hashtags": ["#AryaVysya", "#Komati", "#Vysya"], "wave": 2, "live": False, "route": {"caste": "Vysya"}},
    "brahmin": {"tier": "L3_CASTE", "name": "💍 Brahmin Matrimony | TS-AP",
                "username": "manavivaha_brahmin", "fallbacks": ["tsap_brahmin", "manavivaha_brahmins"],
                "desc": "Vaidiki • Niyogi • Sistla • Dravida Brahmin — gothram + sutram matching.",
                "hashtags": ["#Brahmin", "#Gothram"], "wave": 2, "live": False, "route": {"caste": "Brahmin"}},
    "raju": {"tier": "L3_CASTE", "name": "💍 Raju / Kshatriya Matrimony",
             "username": "manavivaha_raju", "fallbacks": ["tsap_raju", "manavivaha_kshatriya"],
             "desc": "Raju • Kshatriya • Vanniyar • Rajulu matches.",
             "hashtags": ["#Raju", "#Kshatriya"], "wave": 3, "live": False, "route": {"caste": "Raju"}},

    # ---- BC / Backward Classes (28) ----
    "goud": {"tier": "L3_CASTE", "name": "💍 Goud Matrimony | TS-AP",
             "username": "manavivaha_goud", "fallbacks": ["tsap_goud", "manavivaha_gouda"],
             "desc": "Goud • Gouda • Ediga • Gamalla • Idiga • Settibalija — today community.",
             "hashtags": ["#Goud", "#Ediga", "#Gamalla"], "wave": 2, "live": False, "route": {"caste": "Goud"}},
    "yadav": {"tier": "L3_CASTE", "name": "💍 Yadav / Golla Matrimony",
              "username": "manavivaha_yadav", "fallbacks": ["tsap_yadav", "manavivaha_golla"],
              "desc": "Yadav • Golla • Kuruma • Yadava — cattle & farming families.",
              "hashtags": ["#Yadav", "#Golla", "#Kuruma"], "wave": 2, "live": False, "route": {"caste": "Yadav"}},
    "mudiraj": {"tier": "L3_CASTE", "name": "💍 Mudiraj Matrimony | TS-AP",
                "username": "manavivaha_mudiraj", "fallbacks": ["tsap_mudiraj", "manavivaha_mutrasi"],
                "desc": "Mudiraj • Mudiraju • Mutrasi • Tenugollu matches.",
                "hashtags": ["#Mudiraj", "#Tenugollu"], "wave": 3, "live": False, "route": {"caste": "Mudiraj"}},
    "padmashali": {"tier": "L3_CASTE", "name": "💍 Padmashali / Sali Matrimony",
                   "username": "manavivaha_padmashali", "fallbacks": ["tsap_padmashali", "manavivaha_sali"],
                   "desc": "Padmashali • Padmasali • Sali • Pattusali • Thogata — weaver community.",
                   "hashtags": ["#Padmashali", "#Sali", "#Thogata"], "wave": 3, "live": False, "route": {"caste": "Padmashali"}},
    "munnuru_kapu": {"tier": "L3_CASTE", "name": "💍 Munnuru Kapu Matrimony",
                     "username": "manavivaha_munnuru_kapu", "fallbacks": ["manavivaha_munnurukapu"],
                     "desc": "Munnuru Kapu — Telangana community matches.",
                     "hashtags": ["#MunnuruKapu", "#Telangana"], "wave": 3, "live": False, "route": {"caste": "Munnuru Kapu"}},
    "balija": {"tier": "L3_CASTE", "name": "💍 Balija Matrimony | TS-AP",
               "username": "manavivaha_balija", "fallbacks": ["tsap_balija"],
               "desc": "Balija • Gajula Balija • Setti Balija • Surya Balija matches.",
               "hashtags": ["#Balija"], "wave": 3, "live": False, "route": {"caste": "Balija"}},
    "telaga": {"tier": "L3_CASTE", "name": "💍 Telaga Matrimony | TS-AP",
               "username": "manavivaha_telaga", "fallbacks": ["tsap_telaga"],
               "desc": "Telaga community matches — balija/telaga united channel.",
               "hashtags": ["#Telaga"], "wave": 3, "live": False, "route": {"caste": "Telaga"}},
    "koppula_velama": {"tier": "L3_CASTE", "name": "💍 Koppula Velama Matrimony",
                       "username": "manavivaha_koppula_velama", "fallbacks": ["manavivaha_koppulavelama"],
                       "desc": "Koppula Velama — North Andhra + Godavari districts.",
                       "hashtags": ["#KoppulaVelama"], "wave": 4, "live": False, "route": {"caste": "Koppula Velama"}},
    "kalinga": {"tier": "L3_CASTE", "name": "💍 Kalinga Matrimony | TS-AP",
                "username": "manavivaha_kalinga", "fallbacks": ["tsap_kalinga"],
                "desc": "Kinthala • Buragana • Pandiri Kalinga — Srikakulam, Vizianagaram focus.",
                "hashtags": ["#Kalinga"], "wave": 4, "live": False, "route": {"caste": "Kalinga"}},
    "boya": {"tier": "L3_CASTE", "name": "💍 Boya / Valmiki Matrimony",
             "username": "manavivaha_boya", "fallbacks": ["manavivaha_valmiki", "tsap_boya"],
             "desc": "Boya • Valmiki • Boya Bedar • Nishadi • Yellapu — Telangana BC matches.",
             "hashtags": ["#Boya", "#Valmiki"], "wave": 3, "live": False, "route": {"caste": "Boya"}},
    "kuruba": {"tier": "L3_CASTE", "name": "💍 Kuruba / Kuruma Matrimony",
               "username": "manavivaha_kuruba", "fallbacks": ["tsap_kuruba"],
               "desc": "Kuruba • Kuruma shepherds — Rayalaseema + Telangana.",
               "hashtags": ["#Kuruba"], "wave": 4, "live": False, "route": {"caste": "Kuruba"}},
    "uppara": {"tier": "L3_CASTE", "name": "💍 Uppara / Sagara Matrimony",
               "username": "manavivaha_uppara", "fallbacks": ["manavivaha_sagara", "tsap_uppara"],
               "desc": "Uppara • Sagara • Uppari — traditional stone/lime work families.",
               "hashtags": ["#Uppara", "#Sagara"], "wave": 4, "live": False, "route": {"caste": "Uppara"}},
    "vaddera": {"tier": "L3_CASTE", "name": "💍 Vaddera / Odde Matrimony",
                "username": "manavivaha_vaddera", "fallbacks": ["manavivaha_odde", "tsap_vaddera"],
                "desc": "Vaddera • Vaddelu • Odde • Oddilu • Vadde — building work community.",
                "hashtags": ["#Vaddera", "#Odde"], "wave": 4, "live": False, "route": {"caste": "Vaddera"}},
    "rajaka": {"tier": "L3_CASTE", "name": "💍 Rajaka / Chakali Matrimony",
               "username": "manavivaha_rajaka", "fallbacks": ["manavivaha_chakali", "tsap_rajaka"],
               "desc": "Rajaka • Chakali • Vannar • Agnikulakshatriya matches.",
               "hashtags": ["#Rajaka", "#Chakali"], "wave": 4, "live": False, "route": {"caste": "Rajaka"}},
    "mangali": {"tier": "L3_CASTE", "name": "💍 Mangali / Nayi-Brahmin Matrimony",
                "username": "manavivaha_mangali", "fallbacks": ["manavivaha_nayi", "tsap_mangali"],
                "desc": "Mangali • Mangala • Nayi-Brahmin • Bhajanthri matches.",
                "hashtags": ["#Mangali"], "wave": 4, "live": False, "route": {"caste": "Mangali"}},
    "viswakarma": {"tier": "L3_CASTE", "name": "💍 Viswabrahmin / Viswakarma Matrimony",
                   "username": "manavivaha_viswakarma", "fallbacks": ["manavivaha_viswabrahmin", "tsap_viswakarma"],
                   "desc": "Viswakarma • Kamsali • Kammari • Kanchari • Vadla • Ausula — 5 sub-castes.",
                   "hashtags": ["#Viswakarma", "#Viswabrahmin", "#Kamsali"], "wave": 3, "live": False, "route": {"caste": "Viswakarma"}},
    "kummara": {"tier": "L3_CASTE", "name": "💍 Kummara / Kulala Matrimony",
                "username": "manavivaha_kummara", "fallbacks": ["manavivaha_kulala", "tsap_kummara"],
                "desc": "Kummara • Kulala • Salivahana — pottery community matches.",
                "hashtags": ["#Kummara", "#Kulala"], "wave": 4, "live": False, "route": {"caste": "Kummara"}},
    "gandla": {"tier": "L3_CASTE", "name": "💍 Gandla / Telikula Matrimony",
               "username": "manavivaha_gandla", "fallbacks": ["manavivaha_telikula", "tsap_gandla"],
               "desc": "Gandla • Telikula • Devathilakula — oil presser community.",
               "hashtags": ["#Gandla", "#Telikula"], "wave": 4, "live": False, "route": {"caste": "Gandla"}},
    "devanga": {"tier": "L3_CASTE", "name": "💍 Devanga Matrimony | TS-AP",
                "username": "manavivaha_devanga", "fallbacks": ["tsap_devanga"],
                "desc": "Devanga • Devanga Chettiar — weaver community matches.",
                "hashtags": ["#Devanga"], "wave": 4, "live": False, "route": {"caste": "Devanga"}},
    "srisayana": {"tier": "L3_CASTE", "name": "💍 Srisayana / Segidi Matrimony",
                  "username": "manavivaha_srisayana", "fallbacks": ["manavivaha_segidi", "tsap_srisayana"],
                  "desc": "Srisayana • Segidi — North Andhra matches.",
                  "hashtags": ["#Srisayana", "#Segidi"], "wave": 4, "live": False, "route": {"caste": "Srisayana"}},
    "jangam": {"tier": "L3_CASTE", "name": "💍 Jangam Matrimony | TS-AP",
               "username": "manavivaha_jangam", "fallbacks": ["tsap_jangam"],
               "desc": "Jangam • Jangalu • Beda Jangam community matches.",
               "hashtags": ["#Jangam"], "wave": 4, "live": False, "route": {"caste": "Jangam"}},
    "jogi": {"tier": "L3_CASTE", "name": "💍 Jogi Matrimony | TS-AP",
             "username": "manavivaha_jogi", "fallbacks": ["tsap_jogi"],
             "desc": "Jogi • Jogula community matches.",
             "hashtags": ["#Jogi"], "wave": 4, "live": False, "route": {"caste": "Jogi"}},
    "dasari": {"tier": "L3_CASTE", "name": "💍 Dasari Matrimony | TS-AP",
               "username": "manavivaha_dasari", "fallbacks": ["tsap_dasari"],
               "desc": "Dasari • Dasari community matches — respectful space.",
               "hashtags": ["#Dasari"], "wave": 4, "live": False, "route": {"caste": "Dasari"}},
    "bhatraju": {"tier": "L3_CASTE", "name": "💍 Bhatraju Matrimony | TS-AP",
                 "username": "manavivaha_bhatraju", "fallbacks": ["tsap_bhatraju"],
                 "desc": "Bhatraju • Bhatrajulu community matches.",
                 "hashtags": ["#Bhatraju"], "wave": 4, "live": False, "route": {"caste": "Bhatraju"}},
    "gavara": {"tier": "L3_CASTE", "name": "💍 Gavara Matrimony | TS-AP",
               "username": "manavivaha_gavara", "fallbacks": ["tsap_gavara"],
               "desc": "Gavara community matches — North Andhra + Godavari.",
               "hashtags": ["#Gavara"], "wave": 4, "live": False, "route": {"caste": "Gavara"}},
    "bestha": {"tier": "L3_CASTE", "name": "💍 Bestha / Gangaputra Matrimony",
               "username": "manavivaha_bestha", "fallbacks": ["manavivaha_gangaputra", "tsap_bestha"],
               "desc": "Bestha • Gangaputra • Gangavar — fishing community matches.",
               "hashtags": ["#Bestha", "#Gangaputra"], "wave": 4, "live": False, "route": {"caste": "Bestha"}},
    "jalari": {"tier": "L3_CASTE", "name": "💍 Jalari Matrimony | TS-AP",
               "username": "manavivaha_jalari", "fallbacks": ["tsap_jalari"],
               "desc": "Jalari fishermen community matches — coastal AP focus.",
               "hashtags": ["#Jalari"], "wave": 4, "live": False, "route": {"caste": "Jalari"}},
    "vadabalija": {"tier": "L3_CASTE", "name": "💍 Vadabalija Matrimony",
                   "username": "manavivaha_vadabalija", "fallbacks": ["tsap_vadabalija"],
                   "desc": "Vadabalija community matches — coastal districts.",
                   "hashtags": ["#Vadabalija"], "wave": 4, "live": False, "route": {"caste": "Vadabalija"}},

    # ---- SC (4) ----
    "mala": {"tier": "L3_CASTE", "name": "💍 Mala Matrimony | TS-AP",
             "username": "manavivaha_mala", "fallbacks": ["tsap_mala", "manavivaha_sc_mala"],
             "desc": "Mala • Mala Ayawaru • Mala Dasari — SC community, full dignity + privacy.",
             "hashtags": ["#Mala", "#SC"], "wave": 2, "live": False, "route": {"caste": "Mala"}},
    "madiga": {"tier": "L3_CASTE", "name": "💍 Madiga Matrimony | TS-AP",
               "username": "manavivaha_madiga", "fallbacks": ["tsap_madiga", "manavivaha_sc_madiga"],
               "desc": "Madiga • Madiga Dasu • Mashteen — SC community, full dignity + privacy.",
               "hashtags": ["#Madiga", "#SC"], "wave": 2, "live": False, "route": {"caste": "Madiga"}},
    "adi_andhra": {"tier": "L3_CASTE", "name": "💍 Adi Andhra Matrimony",
                   "username": "manavivaha_adi_andhra", "fallbacks": ["manavivaha_adiandhra", "tsap_adi_andhra"],
                   "desc": "Adi Andhra • Adi Dravida • Arundhatiya — SC community matches.",
                   "hashtags": ["#AdiAndhra", "#SC"], "wave": 4, "live": False, "route": {"caste": "Adi Andhra"}},
    "sc_others": {"tier": "L3_CASTE", "name": "💍 SC Other Communities Matrimony",
                  "username": "manavivaha_sc_others", "fallbacks": ["manavivaha_sccommunities"],
                  "desc": "Relli • Mala Dasu • Arwa Mala • Samban • Dandasi — anni SC sub-castes okkate chota.",
                  "hashtags": ["#SC", "#TeluguMatrimony"], "wave": 4, "live": False, "route": {"caste": "SC-Others"}},

    # ---- ST (4) ----
    "lambada": {"tier": "L3_CASTE", "name": "💍 Lambada / Banjara Matrimony",
                "username": "manavivaha_lambada", "fallbacks": ["manavivaha_banjara", "tsap_lambada"],
                "desc": "Lambada • Banjara • Lambani — ST community, traditional + modern matches.",
                "hashtags": ["#Lambada", "#Banjara", "#ST"], "wave": 2, "live": False, "route": {"caste": "Lambada"}},
    "koya": {"tier": "L3_CASTE", "name": "💍 Koya Matrimony | Agency Areas",
             "username": "manavivaha_koya", "fallbacks": ["tsap_koya"],
             "desc": "Koya • Koitur • Bhine Koya — Godavari agency area ST matches.",
             "hashtags": ["#Koya", "#ST"], "wave": 4, "live": False, "route": {"caste": "Koya"}},
    "gond": {"tier": "L3_CASTE", "name": "💍 Gond / Naikpod Matrimony",
             "username": "manavivaha_gond", "fallbacks": ["manavivaha_naikpod", "tsap_gond"],
             "desc": "Gond • Rajgond • Naikpod • Koitur — Adilabad + agency ST matches.",
             "hashtags": ["#Gond", "#ST"], "wave": 4, "live": False, "route": {"caste": "Gond"}},
    "st_others": {"tier": "L3_CASTE", "name": "💍 ST Other Communities Matrimony",
                  "username": "manavivaha_st_others", "fallbacks": ["manavivaha_stcommunities"],
                  "desc": "Chenchu • Andh • Bagata • Konda Reddi • Savara — anni ST sub-castes okkate chota.",
                  "hashtags": ["#ST", "#Adivasi", "#TeluguMatrimony"], "wave": 4, "live": False, "route": {"caste": "ST-Others"}},

    # ===================== LEVEL 4 — SPECIAL (11) =====================
    "second_marriage": {"tier": "L4_SPECIAL", "name": "💔 2nd Marriage | Divorcee & Widow",
                        "username": "manavivaha_second", "fallbacks": ["tsap_second", "manavivaha_remarriage"],
                        "desc": ("Divorcee • Widow • Widower — 2nd innings ki respect tho platform.\n"
                                 "100% privacy • Judge cheyyaru • Serious matches matrame.\n"
                                 "manavivaha.in/register"),
                        "hashtags": ["#SecondMarriage", "#Remarriage", "#Respect"], "wave": 2, "live": False,
                        "route": {"flag": "second_marriage"}},
    "differently_abled": {"tier": "L4_SPECIAL", "name": "♿ Differently Abled Matrimony",
                          "username": "manavivaha_able", "fallbacks": ["tsap_handicapped", "manavivaha_differentlyabled"],
                          "desc": ("Differently abled brides & grooms — special care, special respect.\n"
                                   "Family support + verified profiles only. manavivaha.in/register"),
                          "hashtags": ["#DifferentlyAbled", "#SpecialCare"], "wave": 3, "live": False,
                          "route": {"flag": "differently_abled"}},
    "govt_jobs": {"tier": "L4_SPECIAL", "name": "👮 Govt Job Matches | ప్రభుత్వ ఉద్యోగం",
                  "username": "manavivaha_govt", "fallbacks": ["tsap_govt", "manavivaha_govtjobs"],
                  "desc": "Teacher • Police • Bank • Railway • Group-1/2 • SI • Constable • Nurse — govt job profiles.",
                  "hashtags": ["#GovtJob", "#SoftwarekaduGovt"], "wave": 2, "live": False,
                  "route": {"flag": "govt_job"}},
    "software_it": {"tier": "L4_SPECIAL", "name": "💻 Software / IT Matches",
                    "username": "manavivaha_software", "fallbacks": ["tsap_software", "manavivaha_it"],
                    "desc": "Software • IT • MNC • Product companies — HYD, BLR, PUNE, USA.",
                    "hashtags": ["#Software", "#IT", "#Hyderabad"], "wave": 3, "live": False,
                    "route": {"flag": "software"}},
    "doctors": {"tier": "L4_SPECIAL", "name": "🩺 Doctors & Healthcare Matches",
                "username": "manavivaha_doctors", "fallbacks": ["tsap_doctors", "manavivaha_medical"],
                "desc": "MBBS • MD • MS • BDS • Nursing • Pharma — medical professional matches.",
                "hashtags": ["#Doctors", "#Healthcare"], "wave": 3, "live": False,
                "route": {"flag": "doctor"}},
    "teachers": {"tier": "L4_SPECIAL", "name": "🎓 Teachers & Lecturers Matches",
                 "username": "manavivaha_teachers", "fallbacks": ["tsap_teachers", "manavivaha_lecturers"],
                 "desc": "School Teacher • Lecturer • Professor • Anganwadi — education field matches.",
                 "hashtags": ["#Teacher", "#Lecturer"], "wave": 4, "live": False,
                 "route": {"flag": "teacher"}},
    "above_35": {"tier": "L4_SPECIAL", "name": "🕰️ 35+ Matches | Late Marriage",
                 "username": "manavivaha_35plus", "fallbacks": ["tsap_35plus", "manavivaha_late"],
                 "desc": ("35+ brides & grooms — late marriage ki kooda best sambandham untundi.\n"
                          "No age shaming • Serious profiles matrame. manavivaha.in/register"),
                 "hashtags": ["#35Plus", "#LateMarriage"], "wave": 3, "live": False,
                 "route": {"flag": "above_35"}},
    "love_register": {"tier": "L4_SPECIAL", "name": "💞 Love & Register Marriage",
                      "username": "manavivaha_love", "fallbacks": ["tsap_love"],
                      "desc": "Love marriage • Register marriage • Parents oppuka kosam help.",
                      "hashtags": ["#LoveMarriage", "#RegisterMarriage"], "wave": 4, "live": False,
                      "route": {"flag": "love"}},
    "success_stories": {"tier": "L4_SPECIAL", "name": "🎉 Success Stories & Reviews",
                        "username": "manavivaha_success", "fallbacks": ["tsap_success"],
                        "desc": ("Mana Vivaha tho pelli ayyina couples stories + photos (permission tho).\n"
                                 "Trust = Growth. Me story pampandi: manavivaha.in/success"),
                        "hashtags": ["#SuccessStory", "#ManaVivaha"], "wave": 3, "live": False,
                        "route": "manual"},
    "fraud_alerts": {"tier": "L4_SPECIAL", "name": "⚠️ Fraud Alert & Safety",
                     "username": "manavivaha_alerts", "fallbacks": ["tsap_alerts"],
                     "desc": ("Mosam jagratha! Fake profiles, advance money scams, photo theft alerts.\n"
                              "Report: manavivaha.in/report • 24h lo action. Family safety first."),
                     "hashtags": ["#FraudAlert", "#StaySafe"], "wave": 3, "live": False,
                     "route": "manual"},
    "bureau_network": {"tier": "L4_SPECIAL", "name": "🤝 Bureau & Broker Network (B2B)",
                       "username": "manavivaha_bureau", "fallbacks": ["tsap_bureau", "manavivaha_brokers"],
                       "desc": ("Marriage bureaus • Brokers • Influencers — referral ₹50/profile.\n"
                                "Bulk upload • Dashboard • Leaderboard. manavivaha.in/bureau"),
                       "hashtags": ["#Bureau", "#Referral50"], "wave": 3, "live": False,
                       "route": "manual"},
}

# >>> LIVE_KEYS_EXTRA (setup_channels.py --mark-live idi auto-manage chestundi)
LIVE_KEYS_EXTRA = [
]
# <<< LIVE_KEYS_EXTRA

# ---------------------------------------------------------------------------
# ⭐ CASTE × GENDER CHANNELS — "caste prakaram" proper ga (bride/groom separate)
# ---------------------------------------------------------------------------
# Telugu matrimony lo inti vaallu **tama caste + bride/groom** channel ne follow avutaru.
# Anduke top castes ki bride/groom separate channels; chinna castes ki okate mixed channel
# (andulo #Bride/#Groom hashtag filter).
CASTE_SPLIT: Dict[str, int] = {
    # wave 1 — highest volume (TS + AP)
    "reddy": 1, "kamma": 1, "kapu": 1, "velama": 1, "vysya": 1, "brahmin": 1,
    # wave 2
    "goud": 2, "yadav": 2, "mudiraj": 2, "padmashali": 2, "munnuru_kapu": 2, "mala": 2,
    # wave 3
    "madiga": 3, "lambada": 3, "raju": 3, "balija": 3, "telaga": 3, "viswakarma": 3,
}
SPLIT_MAP: Dict[str, Dict[str, str]] = {}      # caste_key -> {"Bride": key, "Groom": key}

for _caste, _wave in CASTE_SPLIT.items():
    _head = _caste.replace("_", "")
    _pair = {}
    for _gender, _suffix, _fb in (("Bride", "bride", "brd"), ("Groom", "groom", "grm")):
        _key = "c_%s_%s" % (_caste, _suffix)
        CHANNELS[_key] = {
            "tier": "L3_CASTE",
            "name": "",                       # fill avutundi (channel_content nunchi)
            "username": ("manavivaha_%s_%s" % (_head, _suffix))[:32],
            "fallbacks": ["tsap_%s_%s" % (_head, _suffix),
                          "mv_%s_%s" % (_head, _fb),
                          "manavivaha_%s_%s" % (_head, _fb)],
            "desc": "",
            "hashtags": ["#%s" % _caste.replace("_", "").title(), "#%s" % _suffix.title(),
                         "#TS", "#AP"],
            "wave": _wave,
            "live": False,
            "route": {"caste": _caste.replace("_", " ").title(), "gender": _gender},
        }
        _pair[_gender] = _key
    SPLIT_MAP[_caste] = _pair
    # split caste ki mixed channel vaddu (duplicate + empty channel avvakunda)
    CHANNELS.pop(_caste, None)

# ---------------------------------------------------------------------------
# PERFECT CONTENT — title/description anni channel ki (Telugu-first, search-optimised)
# ---------------------------------------------------------------------------
from channel_content import perfect_title as _pt, perfect_description as _pd  # noqa: E402

for _k, _ch in CHANNELS.items():
    _ch["name"] = _pt(_k, _ch)
    _ch["desc"] = _pd(_k, _ch)
    if _k in LIVE_KEYS_EXTRA:          # setup_channels.py --mark-live tho verify ayyavi
        _ch["live"] = True

# ---------------------------------------------------------------------------
# CASTE ALIASES — user free-text ni channel key ki map chesthundi
# ---------------------------------------------------------------------------
CASTE_ALIASES = {
    # OC
    "reddy": "reddy", "reddi": "reddy", "pakanati": "reddy", "motati": "reddy",
    "gudati": "reddy", "deshathi": "reddy", "reddy(golla)": "reddy",
    "kamma": "kamma", "kammas": "kamma", "chowdary": "kamma", "choudary": "kamma",
    "kapu": "kapu", "ontari": "kapu", "turupu kapu": "kapu", "palli kapu": "kapu",
    "velama": "velama", "padma velama": "velama", "vellama": "velama",
    "vysya": "vysya", "arya vysya": "vysya", "komati": "vysya", "komti": "vysya",
    "vaishya": "vysya", "vaishya(arya)": "vysya", "sadhu chetty": "vysya",
    "brahmin": "brahmin", "telugu brahmin": "brahmin", "vaidiki": "brahmin",
    "niyogi": "brahmin", "sistla": "brahmin", "dravida brahmin": "brahmin", "iyer": "brahmin",
    "raju": "raju", "kshatriya": "raju", "rajulu": "raju", "vanniyar": "raju",
    # BC
    "goud": "goud", "gouda": "goud", "ediga": "goud", "gamalla": "goud", "idiga": "goud",
    "settibalija": "goud", "goundla": "goud", "kalalee": "goud",
    "yadav": "yadav", "yadava": "yadav", "golla": "yadav", "golla(yadava)": "yadav",
    "kuruma": "yadav", "gorrela": "yadav",
    "mudiraj": "mudiraj", "mudiraju": "mudiraj", "mutrasi": "mudiraj", "tenugollu": "mudiraj",
    "padmashali": "padmashali", "padmasali": "padmashali", "sali": "padmashali",
    "pattusali": "padmashali", "thogata": "padmashali", "thogata sali": "padmashali",
    "munnuru kapu": "munnuru_kapu", "munnuru": "munnuru_kapu",
    "balija": "balija", "gajula balija": "balija", "surya balija": "balija",
    "setti balija": "balija", "sadhu balija": "balija",
    "telaga": "telaga", "telagu": "telaga",
    "koppula velama": "koppula_velama", "koppula": "koppula_velama",
    "kalinga": "kalinga", "kinthala kalinga": "kalinga", "buragam kalinga": "kalinga",
    "boya": "boya", "valmiki": "boya", "boya bedar": "boya", "nishadi": "boya",
    "yellapu": "boya", "kirataka": "boya",
    "kuruba": "kuruba", "kuruba(golla)": "kuruba", "kuruva": "kuruba",
    "uppara": "uppara", "sagara": "uppara", "sagari": "uppara", "uppari": "uppara",
    "vaddera": "vaddera", "vaddelu": "vaddera", "odde": "vaddera", "oddilu": "vaddera", "vadde": "vaddera",
    "rajaka": "rajaka", "chakali": "rajaka", "vannar": "rajaka", "agnikulakshatriya": "rajaka",
    "mangali": "mangali", "mangala": "mangali", "nayi": "mangali", "nai": "mangali",
    "nayi-brahmin": "mangali", "bhajanthri": "mangali",
    "viswakarma": "viswakarma", "viswabrahmin": "viswakarma", "viswabrahmana": "viswakarma",
    "kamsali": "viswakarma", "kammari": "viswakarma", "kanchari": "viswakarma",
    "vadla": "viswakarma", "ausula": "viswakarma", "silpi": "viswakarma", "vadrangi": "viswakarma",
    "kummara": "kummara", "kulala": "kummara", "salivahana": "kummara", "kumbhara": "kummara",
    "gandla": "gandla", "telikula": "gandla", "devathilakula": "gandla",
    "devanga": "devanga", "devanga chettiar": "devanga",
    "srisayana": "srisayana", "segidi": "srisayana",
    "jangam": "jangam", "jangalu": "jangam", "beda jangam": "jangam",
    "jogi": "jogi", "jogula": "jogi",
    "dasari": "dasari", "dasari(formerly)": "dasari",
    "bhatraju": "bhatraju", "bhatrajulu": "bhatraju",
    "gavara": "gavara",
    "bestha": "bestha", "gangaputra": "bestha", "gangavar": "bestha",
    "jalari": "jalari", "jalari(fishermen)": "jalari",
    "vadabalija": "vadabalija",
    # SC
    "mala": "mala", "sc-mala": "mala", "sc mala": "mala", "mala ayawaru": "mala",
    "mala dasari": "mala",
    "madiga": "madiga", "sc-madiga": "madiga", "sc madiga": "madiga", "madiga dasu": "madiga",
    "mashteen": "madiga", "madiga dasari": "madiga",
    "adi andhra": "adi_andhra", "adi-andhra": "adi_andhra", "adi dravida": "adi_andhra",
    "arundhatiya": "adi_andhra",
    "sc-others": "sc_others", "sc others": "sc_others", "reli": "sc_others", "relli": "sc_others",
    "arwa mala": "sc_others", "samban": "sc_others", "dandasi": "sc_others",
    # ST
    "lambada": "lambada", "lambadi": "lambada", "st-lambadi": "lambada", "st lambadi": "lambada",
    "banjara": "lambada", "lambani": "lambada", "sugali": "lambada",
    "koya": "koya", "koitur": "koya", "bhine koya": "koya",
    "gond": "gond", "rajgond": "gond", "naikpod": "gond",
    "st-others": "st_others", "st others": "st_others", "chenchu": "st_others",
    "andh": "st_others", "bagata": "st_others", "konda reddi": "st_others", "savara": "st_others",
    # Open / no caste
    "open": None, "other": None, "others": None, "oc": None, "no caste": None, "caste no bar": None,
}

RELIGION_ALIASES = {
    "hindu": "Hindu", "hindhu": "Hindu",
    "muslim": "Muslim", "muslims": "Muslim", "musalman": "Muslim", "islam": "Muslim",
    "sheikh": "Muslim", "shaik": "Muslim", "syed": "Muslim", "pathan": "Muslim",
    "khan": "Muslim", "momin": "Muslim", "qureshi": "Muslim", "labbai": "Muslim",
    "dudekula": "Muslim", "pinjari": "Muslim", "noorbash": "Muslim", "asraf": "Muslim",
    "christian": "Christian", "christians": "Christian", "catholic": "Christian",
    "roman catholic": "Christian", "csi": "Christian", "baptist": "Christian",
    "pentecost": "Christian", "born again": "Christian", "methodist": "Christian",
    "salvation army": "Christian", "lutheran": "Christian",
    "sikh": "Other", "jain": "Other", "buddhist": "Other", "parsi": "Other",
    "jewish": "Other", "atheist": "Other", "no religion": "Other",
}

STATE_ALIASES = {
    "ts": "TS", "telangana": "TS", "తెలంగాణ": "TS", "telengana": "TS",
    "ap": "AP", "andhra": "AP", "andhra pradesh": "AP", "ఆంధ్ర": "AP",
    "ఆంధ్రప్రదేశ్": "AP", "ap-2": "AP",
    "usa": "Other", "uk": "Other", "gulf": "Other", "dubai": "Other",
    "canada": "Other", "australia": "Other", "singapore": "Other", "nri": "Other",
    "other": "Other", "others": "Other", "bangalore": "Other", "bengaluru": "Other",
    "chennai": "Other", "pune": "Other", "mumbai": "Other",
}

BLOCK_SOFTWARE = ("software", "it ", " it", "developer", "engineer", "programmer", "devops",
                  "data scientist", "testing", "qa", "product manager", "cloud")
BLOCK_GOVT = ("govt", "government", "teacher", "police", "bank", "railway", "group", "si ",
              "constable", "nurse", "postal", "defence", "army", "navy", "air force", "psu", "sachivalayam")
BLOCK_DOCTOR = ("doctor", "mbbs", "md ", "ms ", "surgeon", "dental", "bds", "nursing", "pharmacy",
                "physio", "veterinary", "bams", "bhms")
BLOCK_TEACHER = ("teacher", "lecturer", "professor", "principal", "anganwadi", "guruji", "trainer")


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def get_channel(key: str) -> dict:
    return CHANNELS.get(key, {})


def all_channels(tier: str | None = None) -> list:
    """Returns list of (key, channel_dict) — tier filter optional."""
    out = []
    for key, ch in CHANNELS.items():
        if tier and ch.get("tier") != tier:
            continue
        out.append({"key": key, **ch})
    return out


def channels_by_tier() -> dict:
    tiers = {}
    for key, ch in CHANNELS.items():
        tiers.setdefault(ch.get("tier", "OTHER"), []).append({"key": key, **ch})
    return tiers


def live_channels() -> list:
    return [{"key": k, **v} for k, v in CHANNELS.items() if v.get("live")]


def pending_channels() -> list:
    return [{"key": k, **v} for k, v in CHANNELS.items() if not v.get("live")]


def channel_chat_id(key: str, only_live: bool = True) -> str | None:
    """Bot post cheyyadaniki chat id/username. only_live=True ayithe created channels matrame."""
    ch = CHANNELS.get(key)
    if not ch:
        return None
    if only_live and not ch.get("live"):
        return None
    return "@" + ch["username"]


def post_targets(profile: dict, only_live: bool = True) -> list:
    """
    Router + live filter → bot e channels lo actually post cheyyali.
    Create kaani channels ni skip chestundi (429/400 error raakunda) + pending list istundi.
    """
    r = route_profile(profile)
    ready, pending = [], []
    for key in r["keys"]:
        if channel_chat_id(key, only_live=True):
            ready.append("@" + CHANNELS[key]["username"])
        else:
            pending.append(key)
    return {"ready": ready, "pending": pending, "keys": r["keys"],
            "hashtags": r["hashtags"], "reasons": r["reasons"], "notes": r["notes"]}


# ---------------------------------------------------------------------------
# SETUP PLAN — "e channels create cheyyali, e order lo" (setup_channels.py idi use chestundi)
# ---------------------------------------------------------------------------
TIER_PRIORITY = {"L0_OFFICIAL": 0, "L1_REGION": 1, "L3_CASTE": 2, "L2_RELIGION": 3, "L4_SPECIAL": 4}


def setup_plan(wave: int | None = None) -> list:
    """Wave → tier → caste order lo channels (create cheyyadaniki)."""
    rows = []
    for key, ch in CHANNELS.items():
        if wave and ch.get("wave") != wave:
            continue
        rows.append({"key": key, "tier": ch.get("tier"), "wave": ch.get("wave"),
                     "name": ch.get("name"), "username": ch.get("username"),
                     "fallbacks": ch.get("fallbacks", []), "live": bool(ch.get("live")),
                     "hashtags": ch.get("hashtags", []), "desc": ch.get("desc")})
    rows.sort(key=lambda r: (r["wave"], TIER_PRIORITY.get(r["tier"], 9), r["key"]))
    return rows


def caste_split_report() -> dict:
    """Caste × gender coverage report (enni castes ki bride/groom separate unnai)."""
    by_wave: Dict[int, list] = {}
    for caste, wave in sorted(CASTE_SPLIT.items(), key=lambda x: (x[1], x[0])):
        by_wave.setdefault(wave, []).append({
            "caste": caste.replace("_", " ").title(),
            "bride": "@" + CHANNELS[SPLIT_MAP[caste]["Bride"]]["username"],
            "groom": "@" + CHANNELS[SPLIT_MAP[caste]["Groom"]]["username"],
        })
    mixed = [k for k, v in CHANNELS.items() if v.get("tier") == "L3_CASTE" and k not in SPLIT_MAP.values()]
    mixed_keys = set()
    for pair in SPLIT_MAP.values():
        mixed_keys.update(pair.values())
    mixed = [k for k, v in CHANNELS.items() if v.get("tier") == "L3_CASTE" and k not in mixed_keys]
    return {"split_castes": len(CASTE_SPLIT), "caste_gender_channels": len(CASTE_SPLIT) * 2,
            "mixed_caste_channels": len(mixed), "by_wave": by_wave}


def channel_health_report() -> list:
    """Emanna channel config lo problem unda (setup mundu)."""
    from channel_content import channel_health
    out = []
    for key, ch in CHANNELS.items():
        probs = channel_health(key, ch)
        if probs:
            out.append({"key": key, "problems": probs})
    return out

def channel_stats() -> dict:
    tiers = channels_by_tier()
    return {
        "total": len(CHANNELS),
        "live": len(live_channels()),
        "to_create": len(pending_channels()),
        "by_tier": {t: len(v) for t, v in tiers.items()},
        "bot": BOT_USERNAME,
        "site": SITE,
    }


def resolve_religion(raw: str) -> str:
    if not raw:
        return "Hindu"
    return RELIGION_ALIASES.get(str(raw).strip().lower(), "Hindu")


def resolve_state(raw: str) -> str:
    if not raw:
        return "TS"
    return STATE_ALIASES.get(str(raw).strip().lower(), "TS")


def resolve_caste_key(raw: str) -> str | None:
    """Caste free-text / dropdown value → channel key (or None if Open/Others)."""
    if not raw:
        return None
    text = str(raw).strip().lower().replace("_", " ").replace("-", " ")
    text = " ".join(text.split())
    text_dash = str(raw).strip().lower()
    for probe in (text_dash, text):
        if probe in CASTE_ALIASES:
            return CASTE_ALIASES[probe]
    # partial match — "reddy (pakanati)" etc.
    for alias, key in CASTE_ALIASES.items():
        if alias and alias in text:
            return key
    return None


def _flag_job(text: str, words: tuple) -> bool:
    t = f" {str(text).lower()} "
    return any(w in t for w in words)


def why_telugu(key: str, profile: dict) -> str:
    """Channel key → caption lo chupinchE Telugu reason (personalized)."""
    gender_word = "Ammai" if str(profile.get("gender", "Bride")).lower().startswith("b") else "Abbai"
    state = resolve_state(profile.get("state", "TS"))
    state_word = {"TS": "Telangana", "AP": "Andhra", "Other": "NRI/Abroad"}[state]
    dist = profile.get("district", "")
    caste = profile.get("caste", "")
    age = str(profile.get("age", "")).split("-")[0]
    reasons = {
        "ts_bride": f"{state_word} {gender_word} — TS Brides channel lo daily chusevallaki reach",
        "ts_groom": f"{state_word} {gender_word} — TS Grooms channel lo direct reach",
        "ap_bride": f"{state_word} {gender_word} — AP Brides channel lo first page",
        "ap_groom": f"{state_word} {gender_word} — AP Grooms channel lo direct reach",
        "nri_global": "NRI/Abroad matches korukune families ki idi first choice",
        "hindu": "Hindu community matches — caste channel kooda kalipi reach",
        "muslim": "Muslim community — Sheikh/Syed/Pathan/Momin anni sub-sects ki reach",
        "christian": "Christian community — Catholic/CSI/Baptist anni denominations ki reach",
        "other_religion": "Other religions — respectful + private matches",
        "interfaith": "Inter-caste / Love marriage korukune couples ki safe space",
        "second_marriage": "2nd innings — divorcee/widow ki respect tho matches",
        "differently_abled": "Differently abled — special care + special respect channel",
        "govt_jobs": "Govt job profile — ee channel lo demand chala ekkuva 🔥",
        "software_it": "Software/IT job — HYD, BLR, USA matches ki best",
        "doctors": "Medical profession — doctor matches ki separate channel",
        "teachers": "Teacher/Lecturer matches — education field families ki",
        "above_35": f"Age {age} — 35+ channel lo late marriage ki kooda best sambandham",
        "love_register": "Love/Register marriage support — parents oppuka tho",
    }
    if key in reasons:
        return reasons[key]
    ch = CHANNELS.get(key, {})
    if ch.get("tier") == "L3_CASTE":
        return f"{caste} caste channel — {dist or state_word} lo {caste} sambandhalu okkate chota"
    return ch.get("desc", key)[:90]


# ---------------------------------------------------------------------------
# THE ROUTER — one profile → all relevant channels
# ---------------------------------------------------------------------------
MAX_POSTS = 5  # spam control — max 5 channels per profile


def route_profile(profile: dict, max_posts: int = MAX_POSTS) -> dict:
    """
    profile keys (all optional, sane defaults):
      gender: "Bride" | "Groom"
      state: "TS" | "AP" | "Other"
      religion: "Hindu" | "Muslim" | "Christian" | "Other"
      caste: "Reddy" | "SC-Mala" | ...   (free text ok)
      age: int or "24"
      marital_status: "Pelli Kaledu" | "Divorcee" | "Widow" | ...
      physical_status: "Normal" | "Handicapped" | ...
      job: "Software Engineer" / "Govt Teacher"
      education: "MBBS" / "BTech"
      interfaith: bool  (couple opted for inter-caste channel)
      wants_nri: bool   (profile is NRI / abroad)

    returns: {"keys": [...], "usernames": [...], "hashtags": "...", "notes": [...]}
    """
    gender = profile.get("gender", "Bride")
    if str(gender).lower().startswith("g"):
        gender = "Groom"
    else:
        gender = "Bride"
    state = resolve_state(profile.get("state", "TS"))
    religion = resolve_religion(profile.get("religion") or profile.get("caste", ""))
    caste_key = resolve_caste_key(profile.get("caste", ""))

    try:
        age = int(str(profile.get("age", "0")).split("-")[0] or 0)
    except Exception:
        age = 0

    marital = str(profile.get("marital_status", "Pelli Kaledu")).lower()
    physical = str(profile.get("physical_status", "Normal")).lower()
    job = f"{profile.get('job','')} {profile.get('occupation','')}"
    education = str(profile.get("education", "")) + " " + str(profile.get("education_detail", ""))

    ordered = []   # (key, reason)
    notes = []

    # L1 — region (always)
    if state == "TS":
        ordered.append(("ts_bride" if gender == "Bride" else "ts_groom", "region+gender"))
    elif state == "AP":
        ordered.append(("ap_bride" if gender == "Bride" else "ap_groom", "region+gender"))
    else:
        ordered.append(("nri_global", "region=Other/NRI"))

    # L2 — religion + L3 caste
    if religion == "Hindu":
        if caste_key:
            # Caste channel already covers the community → general Hindu channel ki
            # duplicate pettaku. Slot save chesi specialty channel ki vadukuntam.
            # Exception: TOP MATCH (score>=90) ayithe Hindu hub lo kooda vestham (digest value).
            if profile.get("top_match"):
                ordered.append(("hindu", "top-match digest"))
            else:
                notes.append("Caste channel undi → general Hindu hub skip (duplication avoid, slot save)")
            if caste_key in SPLIT_MAP:
                # ⭐ CASTE × GENDER channel (bride/groom separate) — exact reach
                ck = SPLIT_MAP[caste_key].get(gender, caste_key)
                ordered.append((ck, "caste=%s + %s" % (profile.get("caste"), gender)))
            else:
                ordered.append((caste_key, "caste=%s (mixed channel, #%s filter)" % (profile.get("caste"), gender)))
        else:
            ordered.append(("hindu", "religion (caste Open/Others)"))
            notes.append("Caste 'Open/Others' — caste channel skip (hashtag #Open)")
    elif religion == "Muslim":
        ordered.append(("muslim", "religion"))
    elif religion == "Christian":
        ordered.append(("christian", "religion"))
    else:
        ordered.append(("other_religion", "religion=Other"))

    # L2b — interfaith / love (optional flag)
    if profile.get("interfaith") or profile.get("love_marriage"):
        ordered.append(("interfaith", "inter-caste/love flag"))

    # L4 — special flags
    if marital and marital not in ("pelli kaledu", "never married", "first marriage", "", "unmarried"):
        ordered.append(("second_marriage", f"marital={profile.get('marital_status')}"))
    if physical and physical not in ("normal", "", "none"):
        ordered.append(("differently_abled", f"physical={profile.get('physical_status')}"))
    if _flag_job(job, BLOCK_GOVT):
        ordered.append(("govt_jobs", "govt job"))
    if _flag_job(job, BLOCK_SOFTWARE):
        ordered.append(("software_it", "software/IT job"))
    if _flag_job(job + " " + education, BLOCK_DOCTOR):
        ordered.append(("doctors", "medical profession"))
    if _flag_job(job, BLOCK_TEACHER):
        ordered.append(("teachers", "teaching profession"))
    if age >= 35:
        ordered.append(("above_35", f"age={age}"))
    if profile.get("wants_nri") or state == "Other":
        ordered.append(("nri_global", "NRI/abroad"))

    # de-dupe, keep order, apply cap
    seen, keys, reasons = set(), [], []
    for key, why in ordered:
        if key in seen or key not in CHANNELS:
            continue
        if len(keys) >= max_posts:
            notes.append(f"cap {max_posts} reach — '{key}' skipped (priority taggindi)")
            continue
        seen.add(key)
        keys.append(key)
        reasons.append({"key": key, "why": why, "telugu": why_telugu(key, profile),
                        "username": "@" + CHANNELS[key]["username"]})

    usernames = ["@" + CHANNELS[k]["username"] for k in keys]
    hashtags = build_hashtags(profile, keys)
    return {"keys": keys, "usernames": usernames, "reasons": reasons,
            "hashtags": hashtags, "notes": notes, "count": len(keys)}


def build_hashtags(profile: dict, keys: list | None = None) -> str:
    """Advanced hashtag builder — channel + caste + state + gender + age + district + job."""
    tags = []
    for k in (keys or []):
        tags += CHANNELS.get(k, {}).get("hashtags", [])[:1]
    caste = str(profile.get("caste", "")).strip().replace(" ", "").replace("-", "")
    if caste and caste.lower() not in ("open", "others", "other", "oc"):
        tags.append("#" + caste)
    state = resolve_state(profile.get("state", "TS"))
    tags.append({"TS": "#Telangana", "AP": "#AndhraPradesh", "Other": "#NRI"}[state])
    gender = "Bride" if str(profile.get("gender", "Bride")).lower().startswith("b") else "Groom"
    tags.append("#" + gender)
    dist = str(profile.get("district", "")).strip().replace(" ", "")
    if dist:
        tags.append("#" + dist)
    age = str(profile.get("age", "")).split("-")[0].strip()
    if age.isdigit():
        tags.append(f"#Age{age}")
    edu = str(profile.get("education", "")).strip().replace(" ", "")
    if edu:
        tags.append("#" + edu)
    if profile.get("photo_private"):
        tags.append("#PhotoPrivate")
    # de-dupe preserve order
    seen, out = set(), []
    for t in tags:
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return " ".join(out)


def build_caption(profile: dict, tsap_id: str = "TSAP-F-2025-XXXX", score: int = 92) -> str:
    """Ready-to-post Telegram caption (photo card + footer + CTA)."""
    r = route_profile(profile)
    reasons = "\n".join(f"• {x['telugu']}" for x in r["reasons"][:4])
    return (
        f"🆔 {tsap_id} | ⭐ {score}% BEST MATCH\n"
        f"👤 {profile.get('full_name','—')} • {profile.get('age','—')}y • {profile.get('height','—')} • {profile.get('caste','—')}\n"
        f"🎓 {profile.get('education','—')} • 💼 {profile.get('job','—')} • 📍 {profile.get('district','—')}, {resolve_state(profile.get('state','TS'))}\n"
        f"🌟 {profile.get('gothram','—')} gothram • {profile.get('star','—')} nakshatram\n"
        f"\n✅ Enduku set avutharu:\n{reasons}\n"
        f"\n{r['hashtags']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🤖 Bot: {BOT_USERNAME} (Modati 3 FREE)\n"
        f"🔍 ID Search: {SITE}/search/{tsap_id}\n"
        f"📝 Register 3 min lo: {SITE}/register\n"
        f"⚠️ Number bot lo pay tarvata matrame — mosam jagratha!"
    )
