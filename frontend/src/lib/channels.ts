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

export const CHANNEL_STATS = {"total": 83, "live": 2, "to_create": 81, "by_tier": {"L0_OFFICIAL": 1, "L1_REGION": 5, "L2_RELIGION": 5, "L3_CASTE": 61, "L4_SPECIAL": 11}, "bot": "@telugumatrimony1_bot", "site": "https://manavivaha.in"} as const;

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
    "label": "Main 4 Channels",
    "icon": "📍",
    "hint": "TS Bride • TS Groom • AP Bride • AP Groom (+ NRI)",
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
    "hint": "Caste prakaram — top 18 castes ki bride/groom separate, migilina 25 castes ki mixed",
    "count": 61
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
    "name": "📢 TSAP Matrimony Official | మన వివాహ — TS-AP",
    "username": "@TSAP_MATRIMONY",
    "link": "https://t.me/TSAP_MATRIMONY",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_tsap_matrimony",
    "desc": "మన వివాహ — TS/AP నం.1 తెలుగు మ్యాట్రిమోని. రోజూ టాప్-3 సంబంధాలు, విజయ గాథలు, మోసం హెచ్చరికలు. 3 requests FREE, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#ManaVivaha",
      "#TSAPMatrimony",
      "#99keSambandham"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "manavivaha",
      "manavivaha_official",
      "manavivaha_hub"
    ]
  },
  {
    "key": "ts_bride",
    "tier": "L1_REGION",
    "name": "👰 TS Brides | తెలంగాణ వధువులు",
    "username": "@TSBRIDE",
    "link": "https://t.me/TSBRIDE",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_tsbride",
    "desc": "👰 TS Brides — తెలంగాణ వధువులు. అన్ని కులాలు, అన్ని జిల్లాలు, రోజూ కొత్త profiles + పొరుత్తం వివరాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#TSBride",
      "#Telangana",
      "#Ammaayi"
    ],
    "wave": 1,
    "live": true,
    "status": "LIVE ✅ Bot Admin",
    "fallbacks": [
      "manavivaha_ts_bride",
      "tsbrides"
    ]
  },
  {
    "key": "ts_groom",
    "tier": "L1_REGION",
    "name": "🤵 TS Grooms | తెలంగాణ వరులు",
    "username": "@TSGROOM1",
    "link": "https://t.me/TSGROOM1",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_tsgroom1",
    "desc": "🤵 TS Grooms — తెలంగాణ వరులు. అన్ని కులాలు, అన్ని జిల్లాలు, రోజూ కొత్త profiles + పొరుత్తం వివరాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#TSGroom",
      "#Telangana",
      "#Abbaayi"
    ],
    "wave": 1,
    "live": true,
    "status": "LIVE ✅ Bot Admin",
    "fallbacks": [
      "manavivaha_ts_groom",
      "tsgroom"
    ]
  },
  {
    "key": "ap_bride",
    "tier": "L1_REGION",
    "name": "👰 AP Brides | ఆంధ్రా వధువులు",
    "username": "@APBRIDE",
    "link": "https://t.me/APBRIDE",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_apbride",
    "desc": "👰 AP Brides — ఆంధ్రా వధువులు. అన్ని కులాలు, అన్ని జిల్లాలు, రోజూ కొత్త profiles + పొరుత్తం వివరాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#APBride",
      "#AndhraPradesh"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "manavivaha_ap_bride",
      "apbride1",
      "manavivaha_apbride"
    ]
  },
  {
    "key": "ap_groom",
    "tier": "L1_REGION",
    "name": "🤵 AP Grooms | ఆంధ్రా వరులు",
    "username": "@APGROOM1",
    "link": "https://t.me/APGROOM1",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_apgroom1",
    "desc": "🤵 AP Grooms — ఆంధ్రా వరులు. అన్ని కులాలు, అన్ని జిల్లాలు, రోజూ కొత్త profiles + పొరుత్తం వివరాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#APGroom",
      "#AndhraPradesh"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "manavivaha_ap_groom",
      "apgroom",
      "manavivaha_apgroom"
    ]
  },
  {
    "key": "nri_global",
    "tier": "L1_REGION",
    "name": "🌍 NRI Telugu Matrimony | విదేశీ సంబంధాలు",
    "username": "@manavivaha_nri",
    "link": "https://t.me/manavivaha_nri",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_nri",
    "desc": "🌍 NRI Telugu Matrimony — విదేశీ సంబంధాలు. అన్ని కులాలు, అన్ని జిల్లాలు, రోజూ కొత్త profiles + పొరుత్తం వివరాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "desc": "🕉️ Hindu Matrimony — హిందూ వివాహాలు. వధువులు + వరులు, అన్ని జిల్లాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "desc": "☪️ Muslim Matrimony — ముస్లిం వివాహాలు. వధువులు + వరులు, అన్ని జిల్లాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "desc": "✝️ Christian Matrimony — క్రైస్తవ వివాహాలు. వధువులు + వరులు, అన్ని జిల్లాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🕊️ Other Religions | ఇతర మత వివాహాలు",
    "username": "@manavivaha_other_religions",
    "link": "https://t.me/manavivaha_other_religions",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_other_religions",
    "desc": "🕊️ Other Religions — ఇతర మత వివాహాలు. వధువులు + వరులు, అన్ని జిల్లాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💞 Inter-Faith & Love | ప్రేమ వివాహాలు",
    "username": "@manavivaha_interfaith",
    "link": "https://t.me/manavivaha_interfaith",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_interfaith",
    "desc": "💞 Inter-Faith & Love — ప్రేమ వివాహాలు. వధువులు + వరులు, అన్ని జిల్లాలు. 3 FREE requests, ₹99లో 5. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "key": "koppula_velama",
    "tier": "L3_CASTE",
    "name": "💍 Koppula Velama Matrimony | కొప్పుల వెలమ వివాహాలు",
    "username": "@manavivaha_koppula_velama",
    "link": "https://t.me/manavivaha_koppula_velama",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_koppula_velama",
    "desc": "కొప్పుల వెలమ వివాహాలు — వధువులు + వరులు, TS + AP. #KoppulaVelama Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Kalinga Matrimony | కళింగ వివాహాలు",
    "username": "@manavivaha_kalinga",
    "link": "https://t.me/manavivaha_kalinga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kalinga",
    "desc": "కళింగ వివాహాలు — వధువులు + వరులు, TS + AP. #Kalinga Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Boya Matrimony | బోయ వివాహాలు",
    "username": "@manavivaha_boya",
    "link": "https://t.me/manavivaha_boya",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_boya",
    "desc": "బోయ వివాహాలు — వధువులు + వరులు, TS + AP. #Boya #Valmiki Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Kuruba Matrimony | కురుబ వివాహాలు",
    "username": "@manavivaha_kuruba",
    "link": "https://t.me/manavivaha_kuruba",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kuruba",
    "desc": "కురుబ వివాహాలు — వధువులు + వరులు, TS + AP. #Kuruba Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Uppara Matrimony | ఉప్పర వివాహాలు",
    "username": "@manavivaha_uppara",
    "link": "https://t.me/manavivaha_uppara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_uppara",
    "desc": "ఉప్పర వివాహాలు — వధువులు + వరులు, TS + AP. #Uppara #Sagara Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Vaddera Matrimony | వడ్డెర వివాహాలు",
    "username": "@manavivaha_vaddera",
    "link": "https://t.me/manavivaha_vaddera",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vaddera",
    "desc": "వడ్డెర వివాహాలు — వధువులు + వరులు, TS + AP. #Vaddera #Odde Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Rajaka Matrimony | రజక వివాహాలు",
    "username": "@manavivaha_rajaka",
    "link": "https://t.me/manavivaha_rajaka",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_rajaka",
    "desc": "రజక వివాహాలు — వధువులు + వరులు, TS + AP. #Rajaka #Chakali Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Mangali Matrimony | మంగలి వివాహాలు",
    "username": "@manavivaha_mangali",
    "link": "https://t.me/manavivaha_mangali",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mangali",
    "desc": "మంగలి వివాహాలు — వధువులు + వరులు, TS + AP. #Mangali Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "key": "kummara",
    "tier": "L3_CASTE",
    "name": "💍 Kummara Matrimony | కుమ్మరి వివాహాలు",
    "username": "@manavivaha_kummara",
    "link": "https://t.me/manavivaha_kummara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kummara",
    "desc": "కుమ్మరి వివాహాలు — వధువులు + వరులు, TS + AP. #Kummara #Kulala Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Gandla Matrimony | గండ్ల వివాహాలు",
    "username": "@manavivaha_gandla",
    "link": "https://t.me/manavivaha_gandla",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gandla",
    "desc": "గండ్ల వివాహాలు — వధువులు + వరులు, TS + AP. #Gandla #Telikula Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Devanga Matrimony | దేవాంగ వివాహాలు",
    "username": "@manavivaha_devanga",
    "link": "https://t.me/manavivaha_devanga",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_devanga",
    "desc": "దేవాంగ వివాహాలు — వధువులు + వరులు, TS + AP. #Devanga Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Srisayana Matrimony | శ్రీసాయన వివాహాలు",
    "username": "@manavivaha_srisayana",
    "link": "https://t.me/manavivaha_srisayana",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_srisayana",
    "desc": "శ్రీసాయన వివాహాలు — వధువులు + వరులు, TS + AP. #Srisayana #Segidi Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Jangam Matrimony | జంగం వివాహాలు",
    "username": "@manavivaha_jangam",
    "link": "https://t.me/manavivaha_jangam",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jangam",
    "desc": "జంగం వివాహాలు — వధువులు + వరులు, TS + AP. #Jangam Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Jogi Matrimony | జోగి వివాహాలు",
    "username": "@manavivaha_jogi",
    "link": "https://t.me/manavivaha_jogi",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jogi",
    "desc": "జోగి వివాహాలు — వధువులు + వరులు, TS + AP. #Jogi Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Dasari Matrimony | దాసరి వివాహాలు",
    "username": "@manavivaha_dasari",
    "link": "https://t.me/manavivaha_dasari",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_dasari",
    "desc": "దాసరి వివాహాలు — వధువులు + వరులు, TS + AP. #Dasari Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Bhatraju Matrimony | భట్రాజు వివాహాలు",
    "username": "@manavivaha_bhatraju",
    "link": "https://t.me/manavivaha_bhatraju",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bhatraju",
    "desc": "భట్రాజు వివాహాలు — వధువులు + వరులు, TS + AP. #Bhatraju Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Gavara Matrimony | గవర వివాహాలు",
    "username": "@manavivaha_gavara",
    "link": "https://t.me/manavivaha_gavara",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gavara",
    "desc": "గవర వివాహాలు — వధువులు + వరులు, TS + AP. #Gavara Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Bestha Matrimony | బెస్త వివాహాలు",
    "username": "@manavivaha_bestha",
    "link": "https://t.me/manavivaha_bestha",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bestha",
    "desc": "బెస్త వివాహాలు — వధువులు + వరులు, TS + AP. #Bestha #Gangaputra Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Jalari Matrimony | జలరి వివాహాలు",
    "username": "@manavivaha_jalari",
    "link": "https://t.me/manavivaha_jalari",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_jalari",
    "desc": "జలరి వివాహాలు — వధువులు + వరులు, TS + AP. #Jalari Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Vadabalija Matrimony | వడబలిజ వివాహాలు",
    "username": "@manavivaha_vadabalija",
    "link": "https://t.me/manavivaha_vadabalija",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vadabalija",
    "desc": "వడబలిజ వివాహాలు — వధువులు + వరులు, TS + AP. #Vadabalija Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "key": "adi_andhra",
    "tier": "L3_CASTE",
    "name": "💍 Adi Andhra Matrimony | ఆది ఆంధ్ర వివాహాలు",
    "username": "@manavivaha_adi_andhra",
    "link": "https://t.me/manavivaha_adi_andhra",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_adi_andhra",
    "desc": "ఆది ఆంధ్ర వివాహాలు — వధువులు + వరులు, TS + AP. #AdiAndhra #SC Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Sc Others Matrimony | SC ఇతరులు వివాహాలు",
    "username": "@manavivaha_sc_others",
    "link": "https://t.me/manavivaha_sc_others",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_sc_others",
    "desc": "SC ఇతరులు వివాహాలు — వధువులు + వరులు, TS + AP. #SC #TeluguMatrimony Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "key": "koya",
    "tier": "L3_CASTE",
    "name": "💍 Koya Matrimony | కోయ వివాహాలు",
    "username": "@manavivaha_koya",
    "link": "https://t.me/manavivaha_koya",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_koya",
    "desc": "కోయ వివాహాలు — వధువులు + వరులు, TS + AP. #Koya #ST Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Gond Matrimony | గోండ్ వివాహాలు",
    "username": "@manavivaha_gond",
    "link": "https://t.me/manavivaha_gond",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_gond",
    "desc": "గోండ్ వివాహాలు — వధువులు + వరులు, TS + AP. #Gond #ST Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 St Others Matrimony | ST ఇతరులు వివాహాలు",
    "username": "@manavivaha_st_others",
    "link": "https://t.me/manavivaha_st_others",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_st_others",
    "desc": "ST ఇతరులు వివాహాలు — వధువులు + వరులు, TS + AP. #ST #Adivasi #TeluguMatrimony Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💍 Second Marriage | రెండో పెళ్లి",
    "username": "@manavivaha_second",
    "link": "https://t.me/manavivaha_second",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_second",
    "desc": "💍 Second Marriage — రెండో పెళ్లి. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "♿ Differently-Abled | ప్రత్యేక సామర్థ్యం",
    "username": "@manavivaha_able",
    "link": "https://t.me/manavivaha_able",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_able",
    "desc": "♿ Differently-Abled — ప్రత్యేక సామర్థ్యం. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🏛️ Govt Jobs Matrimony | ప్రభుత్వ ఉద్యోగులు",
    "username": "@manavivaha_govt",
    "link": "https://t.me/manavivaha_govt",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_govt",
    "desc": "🏛️ Govt Jobs Matrimony — ప్రభుత్వ ఉద్యోగులు. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "💻 Software Matrimony | సాఫ్ట్‌వేర్ ఉద్యోగులు",
    "username": "@manavivaha_software",
    "link": "https://t.me/manavivaha_software",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_software",
    "desc": "💻 Software Matrimony — సాఫ్ట్‌వేర్ ఉద్యోగులు. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🩺 Doctors Matrimony | వైద్యులు",
    "username": "@manavivaha_doctors",
    "link": "https://t.me/manavivaha_doctors",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_doctors",
    "desc": "🩺 Doctors Matrimony — వైద్యులు. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "👩‍🏫 Teachers Matrimony | ఉపాధ్యాయులు",
    "username": "@manavivaha_teachers",
    "link": "https://t.me/manavivaha_teachers",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_teachers",
    "desc": "👩‍🏫 Teachers Matrimony — ఉపాధ్యాయులు. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🎂 35+ Matrimony | 35 ఏళ్ల పైన",
    "username": "@manavivaha_35plus",
    "link": "https://t.me/manavivaha_35plus",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_35plus",
    "desc": "🎂 35+ Matrimony — 35 ఏళ్ల పైన. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "❤️ Love & Register Marriage | ప్రేమ + రిజిస్టర్ పెళ్లి",
    "username": "@manavivaha_love",
    "link": "https://t.me/manavivaha_love",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_love",
    "desc": "❤️ Love & Register Marriage — ప్రేమ + రిజిస్టర్ పెళ్లి. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🏆 Success Stories | విజయ గాథలు",
    "username": "@manavivaha_success",
    "link": "https://t.me/manavivaha_success",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_success",
    "desc": "🏆 Success Stories — విజయ గాథలు. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🚨 Fraud Alerts | మోసం జాగ్రత్త",
    "username": "@manavivaha_alerts",
    "link": "https://t.me/manavivaha_alerts",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_alerts",
    "desc": "🚨 Fraud Alerts — మోసం జాగ్రత్త. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
    "name": "🤝 Bureau / Broker Network | బ్రోకర్ల నెట్‌వర్క్",
    "username": "@manavivaha_bureau",
    "link": "https://t.me/manavivaha_bureau",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_bureau",
    "desc": "🤝 Bureau / Broker Network — బ్రోకర్ల నెట్‌వర్క్. ఈ కేటగిరీ ప్రత్యేక profiles matrame — వేరే ఎక్కడా దొరకవు. Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
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
  },
  {
    "key": "c_reddy_bride",
    "tier": "L3_CASTE",
    "name": "👰 Reddy Brides | రెడ్డి వధువులు",
    "username": "@manavivaha_reddy_bride",
    "link": "https://t.me/manavivaha_reddy_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_reddy_bride",
    "desc": "రెడ్డి వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Reddy #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Reddy",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_reddy_bride",
      "mv_reddy_brd",
      "manavivaha_reddy_brd"
    ]
  },
  {
    "key": "c_reddy_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Reddy Grooms | రెడ్డి వరులు",
    "username": "@manavivaha_reddy_groom",
    "link": "https://t.me/manavivaha_reddy_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_reddy_groom",
    "desc": "రెడ్డి వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Reddy #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Reddy",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_reddy_groom",
      "mv_reddy_grm",
      "manavivaha_reddy_grm"
    ]
  },
  {
    "key": "c_kamma_bride",
    "tier": "L3_CASTE",
    "name": "👰 Kamma Brides | కమ్మ వధువులు",
    "username": "@manavivaha_kamma_bride",
    "link": "https://t.me/manavivaha_kamma_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kamma_bride",
    "desc": "కమ్మ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Kamma #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Kamma",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kamma_bride",
      "mv_kamma_brd",
      "manavivaha_kamma_brd"
    ]
  },
  {
    "key": "c_kamma_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Kamma Grooms | కమ్మ వరులు",
    "username": "@manavivaha_kamma_groom",
    "link": "https://t.me/manavivaha_kamma_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kamma_groom",
    "desc": "కమ్మ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Kamma #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Kamma",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kamma_groom",
      "mv_kamma_grm",
      "manavivaha_kamma_grm"
    ]
  },
  {
    "key": "c_kapu_bride",
    "tier": "L3_CASTE",
    "name": "👰 Kapu Brides | కాపు వధువులు",
    "username": "@manavivaha_kapu_bride",
    "link": "https://t.me/manavivaha_kapu_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kapu_bride",
    "desc": "కాపు వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Kapu #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Kapu",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kapu_bride",
      "mv_kapu_brd",
      "manavivaha_kapu_brd"
    ]
  },
  {
    "key": "c_kapu_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Kapu Grooms | కాపు వరులు",
    "username": "@manavivaha_kapu_groom",
    "link": "https://t.me/manavivaha_kapu_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_kapu_groom",
    "desc": "కాపు వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Kapu #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Kapu",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_kapu_groom",
      "mv_kapu_grm",
      "manavivaha_kapu_grm"
    ]
  },
  {
    "key": "c_velama_bride",
    "tier": "L3_CASTE",
    "name": "👰 Velama Brides | వెలమ వధువులు",
    "username": "@manavivaha_velama_bride",
    "link": "https://t.me/manavivaha_velama_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_velama_bride",
    "desc": "వెలమ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Velama #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Velama",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_velama_bride",
      "mv_velama_brd",
      "manavivaha_velama_brd"
    ]
  },
  {
    "key": "c_velama_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Velama Grooms | వెలమ వరులు",
    "username": "@manavivaha_velama_groom",
    "link": "https://t.me/manavivaha_velama_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_velama_groom",
    "desc": "వెలమ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Velama #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Velama",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_velama_groom",
      "mv_velama_grm",
      "manavivaha_velama_grm"
    ]
  },
  {
    "key": "c_vysya_bride",
    "tier": "L3_CASTE",
    "name": "👰 Vysya Brides | వైశ్య వధువులు",
    "username": "@manavivaha_vysya_bride",
    "link": "https://t.me/manavivaha_vysya_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vysya_bride",
    "desc": "వైశ్య వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Vysya #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Vysya",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_vysya_bride",
      "mv_vysya_brd",
      "manavivaha_vysya_brd"
    ]
  },
  {
    "key": "c_vysya_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Vysya Grooms | వైశ్య వరులు",
    "username": "@manavivaha_vysya_groom",
    "link": "https://t.me/manavivaha_vysya_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_vysya_groom",
    "desc": "వైశ్య వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Vysya #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Vysya",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_vysya_groom",
      "mv_vysya_grm",
      "manavivaha_vysya_grm"
    ]
  },
  {
    "key": "c_brahmin_bride",
    "tier": "L3_CASTE",
    "name": "👰 Brahmin Brides | బ్రాహ్మణ వధువులు",
    "username": "@manavivaha_brahmin_bride",
    "link": "https://t.me/manavivaha_brahmin_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_brahmin_bride",
    "desc": "బ్రాహ్మణ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Brahmin #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Brahmin",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_brahmin_bride",
      "mv_brahmin_brd",
      "manavivaha_brahmin_brd"
    ]
  },
  {
    "key": "c_brahmin_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Brahmin Grooms | బ్రాహ్మణ వరులు",
    "username": "@manavivaha_brahmin_groom",
    "link": "https://t.me/manavivaha_brahmin_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_brahmin_groom",
    "desc": "బ్రాహ్మణ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Brahmin #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Brahmin",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 1,
    "live": false,
    "status": "Wave-1",
    "fallbacks": [
      "tsap_brahmin_groom",
      "mv_brahmin_grm",
      "manavivaha_brahmin_grm"
    ]
  },
  {
    "key": "c_goud_bride",
    "tier": "L3_CASTE",
    "name": "👰 Goud Brides | గౌడ్ వధువులు",
    "username": "@manavivaha_goud_bride",
    "link": "https://t.me/manavivaha_goud_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_goud_bride",
    "desc": "గౌడ్ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Goud #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Goud",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_goud_bride",
      "mv_goud_brd",
      "manavivaha_goud_brd"
    ]
  },
  {
    "key": "c_goud_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Goud Grooms | గౌడ్ వరులు",
    "username": "@manavivaha_goud_groom",
    "link": "https://t.me/manavivaha_goud_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_goud_groom",
    "desc": "గౌడ్ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Goud #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Goud",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_goud_groom",
      "mv_goud_grm",
      "manavivaha_goud_grm"
    ]
  },
  {
    "key": "c_yadav_bride",
    "tier": "L3_CASTE",
    "name": "👰 Yadav Brides | యాదవ వధువులు",
    "username": "@manavivaha_yadav_bride",
    "link": "https://t.me/manavivaha_yadav_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_yadav_bride",
    "desc": "యాదవ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Yadav #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Yadav",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_yadav_bride",
      "mv_yadav_brd",
      "manavivaha_yadav_brd"
    ]
  },
  {
    "key": "c_yadav_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Yadav Grooms | యాదవ వరులు",
    "username": "@manavivaha_yadav_groom",
    "link": "https://t.me/manavivaha_yadav_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_yadav_groom",
    "desc": "యాదవ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Yadav #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Yadav",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_yadav_groom",
      "mv_yadav_grm",
      "manavivaha_yadav_grm"
    ]
  },
  {
    "key": "c_mudiraj_bride",
    "tier": "L3_CASTE",
    "name": "👰 Mudiraj Brides | ముదిరాజ్ వధువులు",
    "username": "@manavivaha_mudiraj_bride",
    "link": "https://t.me/manavivaha_mudiraj_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mudiraj_bride",
    "desc": "ముదిరాజ్ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Mudiraj #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Mudiraj",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_mudiraj_bride",
      "mv_mudiraj_brd",
      "manavivaha_mudiraj_brd"
    ]
  },
  {
    "key": "c_mudiraj_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Mudiraj Grooms | ముదిరాజ్ వరులు",
    "username": "@manavivaha_mudiraj_groom",
    "link": "https://t.me/manavivaha_mudiraj_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mudiraj_groom",
    "desc": "ముదిరాజ్ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Mudiraj #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Mudiraj",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_mudiraj_groom",
      "mv_mudiraj_grm",
      "manavivaha_mudiraj_grm"
    ]
  },
  {
    "key": "c_padmashali_bride",
    "tier": "L3_CASTE",
    "name": "👰 Padmashali Brides | పద్మశాలి వధువులు",
    "username": "@manavivaha_padmashali_bride",
    "link": "https://t.me/manavivaha_padmashali_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_padmashali_bride",
    "desc": "పద్మశాలి వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Padmashali #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Padmashali",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_padmashali_bride",
      "mv_padmashali_brd",
      "manavivaha_padmashali_brd"
    ]
  },
  {
    "key": "c_padmashali_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Padmashali Grooms | పద్మశాలి వరులు",
    "username": "@manavivaha_padmashali_groom",
    "link": "https://t.me/manavivaha_padmashali_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_padmashali_groom",
    "desc": "పద్మశాలి వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Padmashali #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Padmashali",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_padmashali_groom",
      "mv_padmashali_grm",
      "manavivaha_padmashali_grm"
    ]
  },
  {
    "key": "c_munnuru_kapu_bride",
    "tier": "L3_CASTE",
    "name": "👰 Munnuru Kapu Brides | మున్నూరు కాపు వధువులు",
    "username": "@manavivaha_munnurukapu_bride",
    "link": "https://t.me/manavivaha_munnurukapu_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_munnurukapu_bride",
    "desc": "మున్నూరు కాపు వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Munnurukapu #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Munnurukapu",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_munnurukapu_bride",
      "mv_munnurukapu_brd",
      "manavivaha_munnurukapu_brd"
    ]
  },
  {
    "key": "c_munnuru_kapu_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Munnuru Kapu Grooms | మున్నూరు కాపు వరులు",
    "username": "@manavivaha_munnurukapu_groom",
    "link": "https://t.me/manavivaha_munnurukapu_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_munnurukapu_groom",
    "desc": "మున్నూరు కాపు వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Munnurukapu #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Munnurukapu",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_munnurukapu_groom",
      "mv_munnurukapu_grm",
      "manavivaha_munnurukapu_grm"
    ]
  },
  {
    "key": "c_mala_bride",
    "tier": "L3_CASTE",
    "name": "👰 Mala Brides | మాల వధువులు",
    "username": "@manavivaha_mala_bride",
    "link": "https://t.me/manavivaha_mala_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mala_bride",
    "desc": "మాల వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Mala #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Mala",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_mala_bride",
      "mv_mala_brd",
      "manavivaha_mala_brd"
    ]
  },
  {
    "key": "c_mala_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Mala Grooms | మాల వరులు",
    "username": "@manavivaha_mala_groom",
    "link": "https://t.me/manavivaha_mala_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_mala_groom",
    "desc": "మాల వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Mala #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Mala",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 2,
    "live": false,
    "status": "Wave-2",
    "fallbacks": [
      "tsap_mala_groom",
      "mv_mala_grm",
      "manavivaha_mala_grm"
    ]
  },
  {
    "key": "c_madiga_bride",
    "tier": "L3_CASTE",
    "name": "👰 Madiga Brides | మాదిగ వధువులు",
    "username": "@manavivaha_madiga_bride",
    "link": "https://t.me/manavivaha_madiga_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_madiga_bride",
    "desc": "మాదిగ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Madiga #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Madiga",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_madiga_bride",
      "mv_madiga_brd",
      "manavivaha_madiga_brd"
    ]
  },
  {
    "key": "c_madiga_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Madiga Grooms | మాదిగ వరులు",
    "username": "@manavivaha_madiga_groom",
    "link": "https://t.me/manavivaha_madiga_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_madiga_groom",
    "desc": "మాదిగ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Madiga #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Madiga",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_madiga_groom",
      "mv_madiga_grm",
      "manavivaha_madiga_grm"
    ]
  },
  {
    "key": "c_lambada_bride",
    "tier": "L3_CASTE",
    "name": "👰 Lambada Brides | లంబాడ వధువులు",
    "username": "@manavivaha_lambada_bride",
    "link": "https://t.me/manavivaha_lambada_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_lambada_bride",
    "desc": "లంబాడ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Lambada #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Lambada",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_lambada_bride",
      "mv_lambada_brd",
      "manavivaha_lambada_brd"
    ]
  },
  {
    "key": "c_lambada_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Lambada Grooms | లంబాడ వరులు",
    "username": "@manavivaha_lambada_groom",
    "link": "https://t.me/manavivaha_lambada_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_lambada_groom",
    "desc": "లంబాడ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Lambada #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Lambada",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_lambada_groom",
      "mv_lambada_grm",
      "manavivaha_lambada_grm"
    ]
  },
  {
    "key": "c_raju_bride",
    "tier": "L3_CASTE",
    "name": "👰 Raju Brides | రాజు వధువులు",
    "username": "@manavivaha_raju_bride",
    "link": "https://t.me/manavivaha_raju_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_raju_bride",
    "desc": "రాజు వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Raju #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Raju",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_raju_bride",
      "mv_raju_brd",
      "manavivaha_raju_brd"
    ]
  },
  {
    "key": "c_raju_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Raju Grooms | రాజు వరులు",
    "username": "@manavivaha_raju_groom",
    "link": "https://t.me/manavivaha_raju_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_raju_groom",
    "desc": "రాజు వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Raju #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Raju",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_raju_groom",
      "mv_raju_grm",
      "manavivaha_raju_grm"
    ]
  },
  {
    "key": "c_balija_bride",
    "tier": "L3_CASTE",
    "name": "👰 Balija Brides | బలిజ వధువులు",
    "username": "@manavivaha_balija_bride",
    "link": "https://t.me/manavivaha_balija_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_balija_bride",
    "desc": "బలిజ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Balija #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Balija",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_balija_bride",
      "mv_balija_brd",
      "manavivaha_balija_brd"
    ]
  },
  {
    "key": "c_balija_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Balija Grooms | బలిజ వరులు",
    "username": "@manavivaha_balija_groom",
    "link": "https://t.me/manavivaha_balija_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_balija_groom",
    "desc": "బలిజ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Balija #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Balija",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_balija_groom",
      "mv_balija_grm",
      "manavivaha_balija_grm"
    ]
  },
  {
    "key": "c_telaga_bride",
    "tier": "L3_CASTE",
    "name": "👰 Telaga Brides | తెలగ వధువులు",
    "username": "@manavivaha_telaga_bride",
    "link": "https://t.me/manavivaha_telaga_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_telaga_bride",
    "desc": "తెలగ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Telaga #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Telaga",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_telaga_bride",
      "mv_telaga_brd",
      "manavivaha_telaga_brd"
    ]
  },
  {
    "key": "c_telaga_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Telaga Grooms | తెలగ వరులు",
    "username": "@manavivaha_telaga_groom",
    "link": "https://t.me/manavivaha_telaga_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_telaga_groom",
    "desc": "తెలగ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Telaga #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Telaga",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_telaga_groom",
      "mv_telaga_grm",
      "manavivaha_telaga_grm"
    ]
  },
  {
    "key": "c_viswakarma_bride",
    "tier": "L3_CASTE",
    "name": "👰 Viswakarma Brides | విశ్వకర్మ వధువులు",
    "username": "@manavivaha_viswakarma_bride",
    "link": "https://t.me/manavivaha_viswakarma_bride",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_viswakarma_bride",
    "desc": "విశ్వకర్మ వధువులు — TS + AP అన్ని జిల్లాలు. నిజమైన profiles, ఫోటో గోప్యం, 3 requests FREE, ₹99లో 5. #Viswakarma #Bride #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Viswakarma",
      "#Bride",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_viswakarma_bride",
      "mv_viswakarma_brd",
      "manavivaha_viswakarma_brd"
    ]
  },
  {
    "key": "c_viswakarma_groom",
    "tier": "L3_CASTE",
    "name": "🤵 Viswakarma Grooms | విశ్వకర్మ వరులు",
    "username": "@manavivaha_viswakarma_groom",
    "link": "https://t.me/manavivaha_viswakarma_groom",
    "deepLink": "https://t.me/telugumatrimony1_bot?start=ch_manavivaha_viswakarma_groom",
    "desc": "విశ్వకర్మ వరులు — TS + AP అన్ని జిల్లాలు. ఉద్యోగం/చదువు/జాతకం వివరాలతో profiles. 3 requests FREE. #Viswakarma #Groom #TS Register FREE: manavivaha.in | Bot: @telugumatrimony1_bot",
    "hashtags": [
      "#Viswakarma",
      "#Groom",
      "#TS",
      "#AP"
    ],
    "wave": 3,
    "live": false,
    "status": "Wave-3",
    "fallbacks": [
      "tsap_viswakarma_groom",
      "mv_viswakarma_grm",
      "manavivaha_viswakarma_grm"
    ]
  }
];

// Register form dropdown — registry nunchi (43 castes + Muslim/Christian/Open)
export const CASTE_OPTIONS: string[] = [
  "Koppula Velama",
  "Kalinga",
  "Boya",
  "Kuruba",
  "Uppara",
  "Vaddera",
  "Rajaka",
  "Mangali",
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
  "Adi Andhra",
  "SC-Others",
  "Koya",
  "Gond",
  "ST-Others",
  "Reddy",
  "Kamma",
  "Kapu",
  "Velama",
  "Vysya",
  "Brahmin",
  "Goud",
  "Yadav",
  "Mudiraj",
  "Padmashali",
  "Munnuru Kapu",
  "Mala",
  "Madiga",
  "Lambada",
  "Raju",
  "Balija",
  "Telaga",
  "Viswakarma",
  "Muslim",
  "Christian",
  "Open"
];
