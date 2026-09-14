// AUTO-GENERATED from backend/channels_config.py — edit registry, run gen_frontend_channels.py
// Mana Vivaha | TSAP Matrimony — MASTER CHANNEL REGISTRY

export type Channel = {
  key: string;
  tier: string;
  name: string;
  username: string;
  link: string;
  deepLink: string;
  desc: string;
  hashtags: string[];
  wave: number;
  live: boolean;
  status: string;
  fallbacks: string[];
};

export const CHANNEL_STATS = {"total": 65, "live": 2, "to_create": 63, "by_tier": {"L0_OFFICIAL": 1, "L1_REGION": 5, "L2_RELIGION": 5, "L3_CASTE": 43, "L4_SPECIAL": 11}, "bot": "@telugumatrimony1_bot", "site": "https://manavivaha.in"} as const;

export const CHANNEL_TIERS = [
  {
    "key": "L0_OFFICIAL",
    "label": "Official Hub",
    "icon": "📢",
    "hint": "Top-3 daily, success stories, safety alerts",
    "count": 1
  },
  {
    "key": "L1_REGION",
    "label": "State Flagship",
    "icon": "📍",
    "hint": "TS / AP Bride & Groom + NRI",
    "count": 5
  },
  {
    "key": "L2_RELIGION",
    "label": "Religion",
    "icon": "🕊️",
    "hint": "Hindu, Muslim, Christian, Other, Inter-faith",
    "count": 5
  },
  {
    "key": "L3_CASTE",
    "label": "Caste-wise",
    "icon": "💍",
    "hint": "ONE channel per caste — 43 castes covered",
    "count": 43
  },
  {
    "key": "L4_SPECIAL",
    "label": "Special",
    "icon": "⭐",
    "hint": "2nd marriage, able, govt, IT, doctors, 35+, bureau",
    "count": 11
  }
] as const;

export const ALL_CHANNELS: Channel[] = [
  {
    "key": "official",
    "tier": "L0_OFFICIAL",
    "name": "📢 Mana Vivaha Official | TS-AP Matrimony",
    "username": "@manavivaha",
    "link": "https://t.me/manavivaha",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha",
    "desc": "Mana Vivaha — TS & AP No.1 Telugu Matrimony 🇮🇳 ₹99 ke Sambandham • Modati 3 FREE Daily Top-3 matches, success stories, mosam jagratha alerts. Website: manavivaha.in • Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#ManaVivaha",
      "#TSAPMatrimony",
      "#99keSambandham"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "manavivaha_official",
      "tsap_matrimony"
    ]
  },
  {
    "key": "ts_bride",
    "tier": "L1_REGION",
    "name": "👰 TS Brides | తెలంగాణ వధువులు",
    "username": "@TSBRIDE",
    "link": "https://t.me/TSBRIDE",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_tsbride",
    "desc": "Telangana ammayilu — anni kulasthulu. Daily 10+ kotha profiles • Photo verified • ID search. Register FREE: manavivaha.in/register • Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#TSBride",
      "#Telangana",
      "#Ammaayi"
    ],
    "wave": 1,
    "live": true,
    "status": "LIVE ✅ Bot Admin",
    "fallbacks": [
      "manavivaha_ts_bride"
    ]
  },
  {
    "key": "ts_groom",
    "tier": "L1_REGION",
    "name": "🤵 TS Grooms | తెలంగాణ వరులు",
    "username": "@TSGROOM1",
    "link": "https://t.me/TSGROOM1",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_tsgroom1",
    "desc": "Telangana abbayilu — anni kulasthulu. Daily 10+ kotha profiles • Photo verified • ID search. Register FREE: manavivaha.in/register • Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#TSGroom",
      "#Telangana",
      "#Abbaayi"
    ],
    "wave": 1,
    "live": true,
    "status": "LIVE ✅ Bot Admin",
    "fallbacks": [
      "manavivaha_ts_groom"
    ]
  },
  {
    "key": "ap_bride",
    "tier": "L1_REGION",
    "name": "👰 AP Brides | ఆంధ్రా వధువులు",
    "username": "@manavivaha_ap_bride",
    "link": "https://t.me/manavivaha_ap_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_ap_bride",
    "desc": "Andhra Pradesh ammayilu — 26 districts cover. Daily kotha profiles • Register FREE: manavivaha.in/register",
    "hashtags": [
      "#APBride",
      "#AndhraPradesh"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "ap_bride",
      "manavivaha_apbride"
    ]
  },
  {
    "key": "ap_groom",
    "tier": "L1_REGION",
    "name": "🤵 AP Grooms | ఆంధ్రా వరులు",
    "username": "@manavivaha_ap_groom",
    "link": "https://t.me/manavivaha_ap_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_ap_groom",
    "desc": "Andhra Pradesh abbayilu — 26 districts cover. Daily kotha profiles • Register FREE: manavivaha.in/register",
    "hashtags": [
      "#APGroom",
      "#AndhraPradesh"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "ap_groom",
      "apgroom1"
    ]
  },
  {
    "key": "nri_global",
    "tier": "L1_REGION",
    "name": "🌍 NRI & Other States | విదేశాల తెలుగు",
    "username": "@manavivaha_nri",
    "link": "https://t.me/manavivaha_nri",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_nri",
    "desc": "USA • UK • Canada • Australia • Gulf • Singapore — Telugu NRI matches. Visa/PR/job status mention cheyyandi. manavivaha.in • @telugumatrimony1_bot",
    "hashtags": [
      "#NRI",
      "#TeluguAbroad",
      "#GlobalTelugu"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "manavivaha_global",
      "manavivaha_usa"
    ]
  },
  {
    "key": "hindu",
    "tier": "L2_RELIGION",
    "name": "🕉️ Hindu Matrimony | హిందూ వివాహాలు",
    "username": "@manavivaha_hindu",
    "link": "https://t.me/manavivaha_hindu",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_hindu",
    "desc": "Hindu Telugu matches — anni kulasthulu, anni districts. Caste-wise channels kooda undi — profile search: caste filter use cheyyandi. manavivaha.in/register",
    "hashtags": [
      "#Hindu",
      "#TeluguMatrimony"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "manavivaha_hindus",
      "tsap_hindu"
    ]
  },
  {
    "key": "muslim",
    "tier": "L2_RELIGION",
    "name": "☪️ Muslim Matrimony | ముస్లిం వివాహాలు",
    "username": "@manavivaha_muslim",
    "link": "https://t.me/manavivaha_muslim",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_muslim",
    "desc": "Muslim Telugu matches — Sheikh, Syed, Pathan, Momin, Qureshi, Labbai... Bride & Groom rendu — hashtag tho filter: #Bride #Groom #Sheikh #Syed manavivaha.in/register • Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Muslim",
      "#Nikah",
      "#TeluguMuslim"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "manavivaha_muslims",
      "tsap_muslim"
    ]
  },
  {
    "key": "christian",
    "tier": "L2_RELIGION",
    "name": "✝️ Christian Matrimony | క్రైస్తవ వివాహాలు",
    "username": "@manavivaha_christian",
    "link": "https://t.me/manavivaha_christian",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_christian",
    "desc": "Christian Telugu matches — Catholic, CSI, Baptist, Pentecost, Born Again. Bride & Groom rendu — filter: #Catholic #CSI #Baptist manavivaha.in/register",
    "hashtags": [
      "#Christian",
      "#TeluguChristian",
      "#Wedding"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "manavivaha_christians",
      "tsap_christian"
    ]
  },
  {
    "key": "other_religion",
    "tier": "L2_RELIGION",
    "name": "🕊️ Other Religions | ఇతర మతాలు",
    "username": "@manavivaha_other_religions",
    "link": "https://t.me/manavivaha_other_religions",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_other_religions",
    "desc": "Sikh • Jain • Buddhist • Parsi • Jewish • No-caste/No-religion — Telugu matches. Respectful, private, verified. manavivaha.in/register",
    "hashtags": [
      "#OtherReligions",
      "#Respect"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "manavivaha_others",
      "manavivaha_minority"
    ]
  },
  {
    "key": "interfaith",
    "tier": "L2_RELIGION",
    "name": "💞 Inter-Caste & Inter-Faith | ప్రేమ వివాహం",
    "username": "@manavivaha_interfaith",
    "link": "https://t.me/manavivaha_interfaith",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_interfaith",
    "desc": "Inter-caste • Inter-religion • Love & Register marriage. No-caste filter • Full privacy • Couple corner. manavivaha.in/register • Height secret maintain chestham 🤝",
    "hashtags": [
      "#Intercaste",
      "#LoveMarriage",
      "#RegisterMarriage"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "manavivaha_intercaste",
      "manavivaha_mixedmarriage"
    ]
  },
  {
    "key": "reddy",
    "tier": "L3_CASTE",
    "name": "💍 Reddy Matrimony | TS-AP",
    "username": "@manavivaha_reddy",
    "link": "https://t.me/manavivaha_reddy",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_reddy",
    "desc": "Reddy brides & grooms — TS + AP anni districts. #Bride #Groom #Nalgonda #Hyderabad",
    "hashtags": [
      "#Reddy"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_reddy",
      "manavivaha_reddys"
    ]
  },
  {
    "key": "kamma",
    "tier": "L3_CASTE",
    "name": "💍 Kamma Matrimony | TS-AP",
    "username": "@manavivaha_kamma",
    "link": "https://t.me/manavivaha_kamma",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kamma",
    "desc": "Kamma brides & grooms — Guntur, Krishna, Prakasam, Khammam, Hyderabad.",
    "hashtags": [
      "#Kamma"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kamma",
      "manavivaha_kammas"
    ]
  },
  {
    "key": "kapu",
    "tier": "L3_CASTE",
    "name": "💍 Kapu Matrimony | TS-AP",
    "username": "@manavivaha_kapu",
    "link": "https://t.me/manavivaha_kapu",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kapu",
    "desc": "Kapu • Telaga • Balija • Ontari — united Kapu community matches.",
    "hashtags": [
      "#Kapu",
      "#Telaga",
      "#Balija"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kapu",
      "manavivaha_kapus"
    ]
  },
  {
    "key": "velama",
    "tier": "L3_CASTE",
    "name": "💍 Velama Matrimony | TS-AP",
    "username": "@manavivaha_velama",
    "link": "https://t.me/manavivaha_velama",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_velama",
    "desc": "Velama + Koppula Velama + Padma Velama matches — TS + AP.",
    "hashtags": [
      "#Velama"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_velama"
    ]
  },
  {
    "key": "vysya",
    "tier": "L3_CASTE",
    "name": "💍 Arya Vysya / Komati Matrimony",
    "username": "@manavivaha_vysya",
    "link": "https://t.me/manavivaha_vysya",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vysya",
    "desc": "Arya Vysya • Komati • Vaishya • Vysya — business families welcome.",
    "hashtags": [
      "#AryaVysya",
      "#Komati",
      "#Vysya"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_vysya",
      "manavivaha_aryavysya"
    ]
  },
  {
    "key": "brahmin",
    "tier": "L3_CASTE",
    "name": "💍 Brahmin Matrimony | TS-AP",
    "username": "@manavivaha_brahmin",
    "link": "https://t.me/manavivaha_brahmin",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_brahmin",
    "desc": "Vaidiki • Niyogi • Sistla • Dravida Brahmin — gothram + sutram matching.",
    "hashtags": [
      "#Brahmin",
      "#Gothram"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_brahmin",
      "manavivaha_brahmins"
    ]
  },
  {
    "key": "raju",
    "tier": "L3_CASTE",
    "name": "💍 Raju / Kshatriya Matrimony",
    "username": "@manavivaha_raju",
    "link": "https://t.me/manavivaha_raju",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_raju",
    "desc": "Raju • Kshatriya • Vanniyar • Rajulu matches.",
    "hashtags": [
      "#Raju",
      "#Kshatriya"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_raju",
      "manavivaha_kshatriya"
    ]
  },
  {
    "key": "goud",
    "tier": "L3_CASTE",
    "name": "💍 Goud Matrimony | TS-AP",
    "username": "@manavivaha_goud",
    "link": "https://t.me/manavivaha_goud",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_goud",
    "desc": "Goud • Gouda • Ediga • Gamalla • Idiga • Settibalija — today community.",
    "hashtags": [
      "#Goud",
      "#Ediga",
      "#Gamalla"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_goud",
      "manavivaha_gouda"
    ]
  },
  {
    "key": "yadav",
    "tier": "L3_CASTE",
    "name": "💍 Yadav / Golla Matrimony",
    "username": "@manavivaha_yadav",
    "link": "https://t.me/manavivaha_yadav",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_yadav",
    "desc": "Yadav • Golla • Kuruma • Yadava — cattle & farming families.",
    "hashtags": [
      "#Yadav",
      "#Golla",
      "#Kuruma"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_yadav",
      "manavivaha_golla"
    ]
  },
  {
    "key": "mudiraj",
    "tier": "L3_CASTE",
    "name": "💍 Mudiraj Matrimony | TS-AP",
    "username": "@manavivaha_mudiraj",
    "link": "https://t.me/manavivaha_mudiraj",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mudiraj",
    "desc": "Mudiraj • Mudiraju • Mutrasi • Tenugollu matches.",
    "hashtags": [
      "#Mudiraj",
      "#Tenugollu"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_mudiraj",
      "manavivaha_mutrasi"
    ]
  },
  {
    "key": "padmashali",
    "tier": "L3_CASTE",
    "name": "💍 Padmashali / Sali Matrimony",
    "username": "@manavivaha_padmashali",
    "link": "https://t.me/manavivaha_padmashali",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_padmashali",
    "desc": "Padmashali • Padmasali • Sali • Pattusali • Thogata — weaver community.",
    "hashtags": [
      "#Padmashali",
      "#Sali",
      "#Thogata"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_padmashali",
      "manavivaha_sali"
    ]
  },
  {
    "key": "munnuru_kapu",
    "tier": "L3_CASTE",
    "name": "💍 Munnuru Kapu Matrimony",
    "username": "@manavivaha_munnuru_kapu",
    "link": "https://t.me/manavivaha_munnuru_kapu",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_munnuru_kapu",
    "desc": "Munnuru Kapu — Telangana community matches.",
    "hashtags": [
      "#MunnuruKapu",
      "#Telangana"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "manavivaha_munnurukapu"
    ]
  },
  {
    "key": "balija",
    "tier": "L3_CASTE",
    "name": "💍 Balija Matrimony | TS-AP",
    "username": "@manavivaha_balija",
    "link": "https://t.me/manavivaha_balija",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_balija",
    "desc": "Balija • Gajula Balija • Setti Balija • Surya Balija matches.",
    "hashtags": [
      "#Balija"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_balija"
    ]
  },
  {
    "key": "telaga",
    "tier": "L3_CASTE",
    "name": "💍 Telaga Matrimony | TS-AP",
    "username": "@manavivaha_telaga",
    "link": "https://t.me/manavivaha_telaga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_telaga",
    "desc": "Telaga community matches — balija/telaga united channel.",
    "hashtags": [
      "#Telaga"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_telaga"
    ]
  },
  {
    "key": "koppula_velama",
    "tier": "L3_CASTE",
    "name": "💍 Koppula Velama Matrimony",
    "username": "@manavivaha_koppula_velama",
    "link": "https://t.me/manavivaha_koppula_velama",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_koppula_velama",
    "desc": "Koppula Velama — North Andhra + Godavari districts.",
    "hashtags": [
      "#KoppulaVelama"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_koppulavelama"
    ]
  },
  {
    "key": "kalinga",
    "tier": "L3_CASTE",
    "name": "💍 Kalinga Matrimony | TS-AP",
    "username": "@manavivaha_kalinga",
    "link": "https://t.me/manavivaha_kalinga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kalinga",
    "desc": "Kinthala • Buragana • Pandiri Kalinga — Srikakulam, Vizianagaram focus.",
    "hashtags": [
      "#Kalinga"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_kalinga"
    ]
  },
  {
    "key": "boya",
    "tier": "L3_CASTE",
    "name": "💍 Boya / Valmiki Matrimony",
    "username": "@manavivaha_boya",
    "link": "https://t.me/manavivaha_boya",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_boya",
    "desc": "Boya • Valmiki • Boya Bedar • Nishadi • Yellapu — Telangana BC matches.",
    "hashtags": [
      "#Boya",
      "#Valmiki"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "manavivaha_valmiki",
      "tsap_boya"
    ]
  },
  {
    "key": "kuruba",
    "tier": "L3_CASTE",
    "name": "💍 Kuruba / Kuruma Matrimony",
    "username": "@manavivaha_kuruba",
    "link": "https://t.me/manavivaha_kuruba",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kuruba",
    "desc": "Kuruba • Kuruma shepherds — Rayalaseema + Telangana.",
    "hashtags": [
      "#Kuruba"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_kuruba"
    ]
  },
  {
    "key": "uppara",
    "tier": "L3_CASTE",
    "name": "💍 Uppara / Sagara Matrimony",
    "username": "@manavivaha_uppara",
    "link": "https://t.me/manavivaha_uppara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_uppara",
    "desc": "Uppara • Sagara • Uppari — traditional stone/lime work families.",
    "hashtags": [
      "#Uppara",
      "#Sagara"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_sagara",
      "tsap_uppara"
    ]
  },
  {
    "key": "vaddera",
    "tier": "L3_CASTE",
    "name": "💍 Vaddera / Odde Matrimony",
    "username": "@manavivaha_vaddera",
    "link": "https://t.me/manavivaha_vaddera",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vaddera",
    "desc": "Vaddera • Vaddelu • Odde • Oddilu • Vadde — building work community.",
    "hashtags": [
      "#Vaddera",
      "#Odde"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_odde",
      "tsap_vaddera"
    ]
  },
  {
    "key": "rajaka",
    "tier": "L3_CASTE",
    "name": "💍 Rajaka / Chakali Matrimony",
    "username": "@manavivaha_rajaka",
    "link": "https://t.me/manavivaha_rajaka",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_rajaka",
    "desc": "Rajaka • Chakali • Vannar • Agnikulakshatriya matches.",
    "hashtags": [
      "#Rajaka",
      "#Chakali"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_chakali",
      "tsap_rajaka"
    ]
  },
  {
    "key": "mangali",
    "tier": "L3_CASTE",
    "name": "💍 Mangali / Nayi-Brahmin Matrimony",
    "username": "@manavivaha_mangali",
    "link": "https://t.me/manavivaha_mangali",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mangali",
    "desc": "Mangali • Mangala • Nayi-Brahmin • Bhajanthri matches.",
    "hashtags": [
      "#Mangali"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_nayi",
      "tsap_mangali"
    ]
  },
  {
    "key": "viswakarma",
    "tier": "L3_CASTE",
    "name": "💍 Viswabrahmin / Viswakarma Matrimony",
    "username": "@manavivaha_viswakarma",
    "link": "https://t.me/manavivaha_viswakarma",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_viswakarma",
    "desc": "Viswakarma • Kamsali • Kammari • Kanchari • Vadla • Ausula — 5 sub-castes.",
    "hashtags": [
      "#Viswakarma",
      "#Viswabrahmin",
      "#Kamsali"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "manavivaha_viswabrahmin",
      "tsap_viswakarma"
    ]
  },
  {
    "key": "kummara",
    "tier": "L3_CASTE",
    "name": "💍 Kummara / Kulala Matrimony",
    "username": "@manavivaha_kummara",
    "link": "https://t.me/manavivaha_kummara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kummara",
    "desc": "Kummara • Kulala • Salivahana — pottery community matches.",
    "hashtags": [
      "#Kummara",
      "#Kulala"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_kulala",
      "tsap_kummara"
    ]
  },
  {
    "key": "gandla",
    "tier": "L3_CASTE",
    "name": "💍 Gandla / Telikula Matrimony",
    "username": "@manavivaha_gandla",
    "link": "https://t.me/manavivaha_gandla",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gandla",
    "desc": "Gandla • Telikula • Devathilakula — oil presser community.",
    "hashtags": [
      "#Gandla",
      "#Telikula"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_telikula",
      "tsap_gandla"
    ]
  },
  {
    "key": "devanga",
    "tier": "L3_CASTE",
    "name": "💍 Devanga Matrimony | TS-AP",
    "username": "@manavivaha_devanga",
    "link": "https://t.me/manavivaha_devanga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_devanga",
    "desc": "Devanga • Devanga Chettiar — weaver community matches.",
    "hashtags": [
      "#Devanga"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_devanga"
    ]
  },
  {
    "key": "srisayana",
    "tier": "L3_CASTE",
    "name": "💍 Srisayana / Segidi Matrimony",
    "username": "@manavivaha_srisayana",
    "link": "https://t.me/manavivaha_srisayana",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_srisayana",
    "desc": "Srisayana • Segidi — North Andhra matches.",
    "hashtags": [
      "#Srisayana",
      "#Segidi"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_segidi",
      "tsap_srisayana"
    ]
  },
  {
    "key": "jangam",
    "tier": "L3_CASTE",
    "name": "💍 Jangam Matrimony | TS-AP",
    "username": "@manavivaha_jangam",
    "link": "https://t.me/manavivaha_jangam",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jangam",
    "desc": "Jangam • Jangalu • Beda Jangam community matches.",
    "hashtags": [
      "#Jangam"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_jangam"
    ]
  },
  {
    "key": "jogi",
    "tier": "L3_CASTE",
    "name": "💍 Jogi Matrimony | TS-AP",
    "username": "@manavivaha_jogi",
    "link": "https://t.me/manavivaha_jogi",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jogi",
    "desc": "Jogi • Jogula community matches.",
    "hashtags": [
      "#Jogi"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_jogi"
    ]
  },
  {
    "key": "dasari",
    "tier": "L3_CASTE",
    "name": "💍 Dasari Matrimony | TS-AP",
    "username": "@manavivaha_dasari",
    "link": "https://t.me/manavivaha_dasari",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_dasari",
    "desc": "Dasari • Dasari community matches — respectful space.",
    "hashtags": [
      "#Dasari"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_dasari"
    ]
  },
  {
    "key": "bhatraju",
    "tier": "L3_CASTE",
    "name": "💍 Bhatraju Matrimony | TS-AP",
    "username": "@manavivaha_bhatraju",
    "link": "https://t.me/manavivaha_bhatraju",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bhatraju",
    "desc": "Bhatraju • Bhatrajulu community matches.",
    "hashtags": [
      "#Bhatraju"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_bhatraju"
    ]
  },
  {
    "key": "gavara",
    "tier": "L3_CASTE",
    "name": "💍 Gavara Matrimony | TS-AP",
    "username": "@manavivaha_gavara",
    "link": "https://t.me/manavivaha_gavara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gavara",
    "desc": "Gavara community matches — North Andhra + Godavari.",
    "hashtags": [
      "#Gavara"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_gavara"
    ]
  },
  {
    "key": "bestha",
    "tier": "L3_CASTE",
    "name": "💍 Bestha / Gangaputra Matrimony",
    "username": "@manavivaha_bestha",
    "link": "https://t.me/manavivaha_bestha",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bestha",
    "desc": "Bestha • Gangaputra • Gangavar — fishing community matches.",
    "hashtags": [
      "#Bestha",
      "#Gangaputra"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_gangaputra",
      "tsap_bestha"
    ]
  },
  {
    "key": "jalari",
    "tier": "L3_CASTE",
    "name": "💍 Jalari Matrimony | TS-AP",
    "username": "@manavivaha_jalari",
    "link": "https://t.me/manavivaha_jalari",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jalari",
    "desc": "Jalari fishermen community matches — coastal AP focus.",
    "hashtags": [
      "#Jalari"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_jalari"
    ]
  },
  {
    "key": "vadabalija",
    "tier": "L3_CASTE",
    "name": "💍 Vadabalija Matrimony",
    "username": "@manavivaha_vadabalija",
    "link": "https://t.me/manavivaha_vadabalija",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vadabalija",
    "desc": "Vadabalija community matches — coastal districts.",
    "hashtags": [
      "#Vadabalija"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_vadabalija"
    ]
  },
  {
    "key": "mala",
    "tier": "L3_CASTE",
    "name": "💍 Mala Matrimony | TS-AP",
    "username": "@manavivaha_mala",
    "link": "https://t.me/manavivaha_mala",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mala",
    "desc": "Mala • Mala Ayawaru • Mala Dasari — SC community, full dignity + privacy.",
    "hashtags": [
      "#Mala",
      "#SC"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_mala",
      "manavivaha_sc_mala"
    ]
  },
  {
    "key": "madiga",
    "tier": "L3_CASTE",
    "name": "💍 Madiga Matrimony | TS-AP",
    "username": "@manavivaha_madiga",
    "link": "https://t.me/manavivaha_madiga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_madiga",
    "desc": "Madiga • Madiga Dasu • Mashteen — SC community, full dignity + privacy.",
    "hashtags": [
      "#Madiga",
      "#SC"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_madiga",
      "manavivaha_sc_madiga"
    ]
  },
  {
    "key": "adi_andhra",
    "tier": "L3_CASTE",
    "name": "💍 Adi Andhra Matrimony",
    "username": "@manavivaha_adi_andhra",
    "link": "https://t.me/manavivaha_adi_andhra",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_adi_andhra",
    "desc": "Adi Andhra • Adi Dravida • Arundhatiya — SC community matches.",
    "hashtags": [
      "#AdiAndhra",
      "#SC"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_adiandhra",
      "tsap_adi_andhra"
    ]
  },
  {
    "key": "sc_others",
    "tier": "L3_CASTE",
    "name": "💍 SC Other Communities Matrimony",
    "username": "@manavivaha_sc_others",
    "link": "https://t.me/manavivaha_sc_others",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_sc_others",
    "desc": "Relli • Mala Dasu • Arwa Mala • Samban • Dandasi — anni SC sub-castes okkate chota.",
    "hashtags": [
      "#SC",
      "#TeluguMatrimony"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_sccommunities"
    ]
  },
  {
    "key": "lambada",
    "tier": "L3_CASTE",
    "name": "💍 Lambada / Banjara Matrimony",
    "username": "@manavivaha_lambada",
    "link": "https://t.me/manavivaha_lambada",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_lambada",
    "desc": "Lambada • Banjara • Lambani — ST community, traditional + modern matches.",
    "hashtags": [
      "#Lambada",
      "#Banjara",
      "#ST"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "manavivaha_banjara",
      "tsap_lambada"
    ]
  },
  {
    "key": "koya",
    "tier": "L3_CASTE",
    "name": "💍 Koya Matrimony | Agency Areas",
    "username": "@manavivaha_koya",
    "link": "https://t.me/manavivaha_koya",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_koya",
    "desc": "Koya • Koitur • Bhine Koya — Godavari agency area ST matches.",
    "hashtags": [
      "#Koya",
      "#ST"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_koya"
    ]
  },
  {
    "key": "gond",
    "tier": "L3_CASTE",
    "name": "💍 Gond / Naikpod Matrimony",
    "username": "@manavivaha_gond",
    "link": "https://t.me/manavivaha_gond",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gond",
    "desc": "Gond • Rajgond • Naikpod • Koitur — Adilabad + agency ST matches.",
    "hashtags": [
      "#Gond",
      "#ST"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_naikpod",
      "tsap_gond"
    ]
  },
  {
    "key": "st_others",
    "tier": "L3_CASTE",
    "name": "💍 ST Other Communities Matrimony",
    "username": "@manavivaha_st_others",
    "link": "https://t.me/manavivaha_st_others",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_st_others",
    "desc": "Chenchu • Andh • Bagata • Konda Reddi • Savara — anni ST sub-castes okkate chota.",
    "hashtags": [
      "#ST",
      "#Adivasi",
      "#TeluguMatrimony"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "manavivaha_stcommunities"
    ]
  },
  {
    "key": "second_marriage",
    "tier": "L4_SPECIAL",
    "name": "💔 2nd Marriage | Divorcee & Widow",
    "username": "@manavivaha_second",
    "link": "https://t.me/manavivaha_second",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_second",
    "desc": "Divorcee • Widow • Widower — 2nd innings ki respect tho platform. 100% privacy • Judge cheyyaru • Serious matches matrame. manavivaha.in/register",
    "hashtags": [
      "#SecondMarriage",
      "#Remarriage",
      "#Respect"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_second",
      "manavivaha_remarriage"
    ]
  },
  {
    "key": "differently_abled",
    "tier": "L4_SPECIAL",
    "name": "♿ Differently Abled Matrimony",
    "username": "@manavivaha_able",
    "link": "https://t.me/manavivaha_able",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_able",
    "desc": "Differently abled brides & grooms — special care, special respect. Family support + verified profiles only. manavivaha.in/register",
    "hashtags": [
      "#DifferentlyAbled",
      "#SpecialCare"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_handicapped",
      "manavivaha_differentlyabled"
    ]
  },
  {
    "key": "govt_jobs",
    "tier": "L4_SPECIAL",
    "name": "👮 Govt Job Matches | ప్రభుత్వ ఉద్యోగం",
    "username": "@manavivaha_govt",
    "link": "https://t.me/manavivaha_govt",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_govt",
    "desc": "Teacher • Police • Bank • Railway • Group-1/2 • SI • Constable • Nurse — govt job profiles.",
    "hashtags": [
      "#GovtJob",
      "#SoftwarekaduGovt"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_govt",
      "manavivaha_govtjobs"
    ]
  },
  {
    "key": "software_it",
    "tier": "L4_SPECIAL",
    "name": "💻 Software / IT Matches",
    "username": "@manavivaha_software",
    "link": "https://t.me/manavivaha_software",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_software",
    "desc": "Software • IT • MNC • Product companies — HYD, BLR, PUNE, USA.",
    "hashtags": [
      "#Software",
      "#IT",
      "#Hyderabad"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_software",
      "manavivaha_it"
    ]
  },
  {
    "key": "doctors",
    "tier": "L4_SPECIAL",
    "name": "🩺 Doctors & Healthcare Matches",
    "username": "@manavivaha_doctors",
    "link": "https://t.me/manavivaha_doctors",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_doctors",
    "desc": "MBBS • MD • MS • BDS • Nursing • Pharma — medical professional matches.",
    "hashtags": [
      "#Doctors",
      "#Healthcare"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_doctors",
      "manavivaha_medical"
    ]
  },
  {
    "key": "teachers",
    "tier": "L4_SPECIAL",
    "name": "🎓 Teachers & Lecturers Matches",
    "username": "@manavivaha_teachers",
    "link": "https://t.me/manavivaha_teachers",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_teachers",
    "desc": "School Teacher • Lecturer • Professor • Anganwadi — education field matches.",
    "hashtags": [
      "#Teacher",
      "#Lecturer"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_teachers",
      "manavivaha_lecturers"
    ]
  },
  {
    "key": "above_35",
    "tier": "L4_SPECIAL",
    "name": "🕰️ 35+ Matches | Late Marriage",
    "username": "@manavivaha_35plus",
    "link": "https://t.me/manavivaha_35plus",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_35plus",
    "desc": "35+ brides & grooms — late marriage ki kooda best sambandham untundi. No age shaming • Serious profiles matrame. manavivaha.in/register",
    "hashtags": [
      "#35Plus",
      "#LateMarriage"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_35plus",
      "manavivaha_late"
    ]
  },
  {
    "key": "love_register",
    "tier": "L4_SPECIAL",
    "name": "💞 Love & Register Marriage",
    "username": "@manavivaha_love",
    "link": "https://t.me/manavivaha_love",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_love",
    "desc": "Love marriage • Register marriage • Parents oppuka kosam help.",
    "hashtags": [
      "#LoveMarriage",
      "#RegisterMarriage"
    ],
    "wave": 4,
    "live": false,
    "status": "Wave-4",
    "fallbacks": [
      "tsap_love"
    ]
  },
  {
    "key": "success_stories",
    "tier": "L4_SPECIAL",
    "name": "🎉 Success Stories & Reviews",
    "username": "@manavivaha_success",
    "link": "https://t.me/manavivaha_success",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_success",
    "desc": "Mana Vivaha tho pelli ayyina couples stories + photos (permission tho). Trust = Growth. Me story pampandi: manavivaha.in/success",
    "hashtags": [
      "#SuccessStory",
      "#ManaVivaha"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_success"
    ]
  },
  {
    "key": "fraud_alerts",
    "tier": "L4_SPECIAL",
    "name": "⚠️ Fraud Alert & Safety",
    "username": "@manavivaha_alerts",
    "link": "https://t.me/manavivaha_alerts",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_alerts",
    "desc": "Mosam jagratha! Fake profiles, advance money scams, photo theft alerts. Report: manavivaha.in/report • 24h lo action. Family safety first.",
    "hashtags": [
      "#FraudAlert",
      "#StaySafe"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_alerts"
    ]
  },
  {
    "key": "bureau_network",
    "tier": "L4_SPECIAL",
    "name": "🤝 Bureau & Broker Network (B2B)",
    "username": "@manavivaha_bureau",
    "link": "https://t.me/manavivaha_bureau",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bureau",
    "desc": "Marriage bureaus • Brokers • Influencers — referral ₹50/profile. Bulk upload • Dashboard • Leaderboard. manavivaha.in/bureau",
    "hashtags": [
      "#Bureau",
      "#Referral50"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_bureau",
      "manavivaha_brokers"
    ]
  }
];

// Register form dropdown — registry nunchi (43 castes + Muslim/Christian/Open)
export const CASTE_OPTIONS: string[] = [
  "Reddy",
  "Kamma",
  "Kapu",
  "Velama",
  "Vysya",
  "Brahmin",
  "Raju",
  "Goud",
  "Yadav",
  "Mudiraj",
  "Padmashali",
  "Munnuru Kapu",
  "Balija",
  "Telaga",
  "Koppula Velama",
  "Kalinga",
  "Boya",
  "Kuruba",
  "Uppara",
  "Vaddera",
  "Rajaka",
  "Mangali",
  "Viswakarma",
  "Kummara",
  "Gandla",
  "Devanga",
  "Srisayana",
  "Jangam",
  "Jogi",
  "Dasari",
  "Bhatraju",
  "Gavara",
  "Bestha",
  "Jalari",
  "Vadabalija",
  "Mala",
  "Madiga",
  "Adi Andhra",
  "SC-Others",
  "Lambada",
  "Koya",
  "Gond",
  "ST-Others",
  "Muslim",
  "Christian",
  "Open"
];
