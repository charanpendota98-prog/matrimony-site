# 🔁 BOTS + WHATSAPP FAILOVER — ENNI KAVALI, ELA SET CHEYYALI (TELUGU)

> **Oke okka bot / oke okka WhatsApp number = risk.** Okati aagipoyina (ban / rate limit / bridge down / server restart) appudu posting **aagipothundi** — profile ki reach undadu. Andukane mana system lo **POOL + AUTO FAILOVER** pettamu: **okati fail aithe inkokati ventane pampistundi** — okka post kooda miss avvadu.

---

## 1️⃣ ENNI BOTS KAVALI? → **3 BOTS** (kakapote minimum 2)

| # | Bot | Purpose | Env variable | Enduku separate? |
|---|---|---|---|---|
| 1 | **Primary bot** (existing @telugumatrimony1_bot) | Channels lo **post** + users ki DM (register welcome, interest) | `BOT_TOKEN` | Idi main — 90% pani idi chestundi |
| 2 | **Backup bot** (kotha bot) | Channels lo **post** only — primary 429/401/down aithe | `BOT_TOKEN_BACKUP` | Telegram okka bot ki ~30 msg/sec limit; primary aagipote posts aagakudadu |
| 3 | **Alert bot** (kotha bot) | Admin alerts: kotha profile, interest, WhatsApp fail, monitoring | `BOT_TOKEN_ALERT` | User messages valla alert bot rate-limit avvakudadu |

**Enni channels ki add cheyyali?** — 3 bots ni **ANNI 52 channels** ki admin cheyyali (Channel → Administrators → Add → **Post + Edit + Pin + Change Info** ✅). Appude failover pani chestundi — primary aagipote backup bot **ade channel** lo post estundi.

### 🤖 Bots ela create cheyyali (2 nimushalu — @BotFather)
```
Telegram → @BotFather → /newbot
Name:      Mana Vivaha Backup
Username:  manavivaha_backup_bot        (chivari lo 'bot' undali)
→ token copy → .env lo BOT_TOKEN_BACKUP=123456:ABC...

Malli /newbot → Mana Vivaha Alerts → manavivaha_alerts_bot → BOT_TOKEN_ALERT=...
```
⚠️ Bot username **already taken** aithe numbers add cheyyandi (`manavivaha_backup1_bot`, `manavivaha_alert1_bot`).

---

## 2️⃣ ENNI WHATSAPP NUMBERS? → **3 NUMBERS** (2 posting + 1 requests/backup)

| # | Number | Lane | Daily cap | Env (`WA_INSTANCES` lo) | Enduku? |
|---|---|---|---|---|---|
| 1 | Number-1 (main) | `both` (post + requests) | 60 | `wa1` → `http://whatsapp-bridge:3000` | Primary — channels/groups post |
| 2 | Number-2 | `both` (post + requests) | 60 | `wa2` → `http://whatsapp-bridge2:3000` | Load split + ban risk half. wa1 fail aithe idi post estundi |
| 3 | Number-3 | `requests` | 40 | `wa3` → `http://whatsapp-bridge3:3000` | **Interest/request lane** ki dedicated + backup. Idi ban aina kooda channel posting aagadu |

**Total: rojuki 160 WhatsApp messages** (60+60+40) — anti-ban limits lo safe. Mari ekkuva kavali ante 4th number (`wa4`, cap 60) add cheyyandi — code lo em marchakunda, `.env` lo line add cheste chalu.

### 📱 Numbers ela connect cheyyali (okka number ki ~3 nimushalu)
```bash
cd ~/matrimony-site   # server lo (VM)
docker-compose up -d whatsapp-bridge whatsapp-bridge2 whatsapp-bridge3

# browser lo QR open cheyyandi → phone nunchi scan (WhatsApp → Linked Devices)
http://140.245.216.16:3001/qr     # Number-1
http://140.245.216.16:3002/qr     # Number-2
http://140.245.216.16:3003/qr     # Number-3

# .env lo (single line, JSON):
WA_INSTANCES=[{"name":"wa1","url":"http://whatsapp-bridge:3000","lane":"both","daily_cap":60},
              {"name":"wa2","url":"http://whatsapp-bridge2:3000","lane":"both","daily_cap":60},
              {"name":"wa3","url":"http://whatsapp-bridge3:3000","lane":"requests","daily_cap":40}]
docker-compose restart backend
```
💡 **Phone requirement:** 3 numbers ki 3 SIM / 3 phones kavali (okka phone lo WhatsApp Business + normal WhatsApp — 2 varaku easy). Okkokati **separate WhatsApp account** (modati sari ee number tho WhatsApp open chesi verify cheyyali).
⚠️ **Ban risk thakkuva cheyyadaniki:** okkokka number ki rojuki 60 messages (gap 120–170 sec), groups lo target cap 8/day, 8–22 hours, 4 rojula warmup — ivi already code lo unnayi (`wa_antiban.py`).

---

## 3️⃣ OKATI FAIL AITHE INKOKATI PAMPELA — ILA PANI CHESTUNDI

```
Telegram post    →  primary bot  →(429 / 401 / timeout)→  backup bot  →(fail)→  alert bot  →(fail)→  queue retry (3x) + admin alert
WhatsApp post    →  wa1 (gap/cap ok na?)  →(fail)→  wa2  →(fail)→  wa3  →(fail)→  dead-letter + admin WhatsApp alert
Interest/request →  wa3 (requests lane)  →(fail)→  wa1  →(fail)→  wa2       (fast lane — 60–120 sec gap)
```

**Important rules (code lo implement ayyayi):**
- ❌ **Duplicate ledu** — okati success aithe aagipothundi (rendu numbers ki post avvadu)
- ⏱️ **429 rate-limit** → aa bot/number `retry_after` time cooldown lo, inkokati **ventane** pampistundi
- 🔐 **401 token tappu** → 1 hour cooldown (aa bot ni marchi .env lo kotha token pettali)
- 🚫 **403 'not enough rights'** → bot ni channel lo **admin cheyyaledu** → bot cooldown ledu, channel lo admin cheyyandi
- 📉 **Load balance** → thakkuva messages pampina number ki mundu chance (okate number meeda load padadu)
- 💀 **Anni fail** → 3 tries tarvata **dead-letter** lo save + admin ki alert → bridge fix chesi `POST /api/wa/dead/requeue` tho malli pampochu (message poye paristhithi ledu)

### 🧪 Health ela chudali (live)
```bash
curl localhost:8000/api/system/health      # 🩺 anni bots + numbers + queue + problems (Telugu lo chepthundi)
curl localhost:8000/api/bots/health        # 🤖 bots failover order
curl localhost:8000/api/wa/status          # 📱 per-number sent/cap/status
curl localhost:8000/api/wa/dead            # 💀 deliver kaani messages
curl -X POST localhost:8000/api/wa/dead/requeue   # bridge fix ayyaka malli pampu
```

---

## 4️⃣ CHANNELS — ANNI PERU (SMART DIVISION — **52 channels**, 83 kaadu)

**Total: 52 channels** · live: 2 · create cheyyalsinavi: 50

> 🧠 **Smart structure:** pedda communities ki **bride/groom separate**, chinna sub-castes (ex: Viswabrahmana 5-12) **okate channel**,
> **Muslim 4** (TS/AP × bride/groom) + **Christian 4** — malli division ledu. Full details: **CHANNELS-SMART-STRUCTURE-TELUGU.md**

### 🌊 Wave order — ila cheyyandi (okkesari anni vaddu!)
| Wave | Enni | Emi |
|---|---|---|
| **Wave 1** | 20 | Official + TS/AP bride/groom + **Muslim 4 + Christian 4** + top-3 caste clusters (Reddy/Kamma/Kapu × bride/groom) + Hindu hub |
| **Wave 2** | 17 | Velama, Brahmin, Vysya, Yadava-Goud, Mala, Madiga (×2), Viswabrahmana, Munnuru Kapu, NRI, Other religions, 2nd marriage |
| **Wave 3** | 15 | Padmashali-Devanga, Raju-Kshatriya, Mudiraj, Lambada-Banjara, Other BC/SC/ST, Inter-faith, + special (govt/IT/doctors/success/fraud/bureau/able) |

### 📋 FULL LIST — 52 channels (copy-paste ready)

| # | Channel Name | Username | Wave | Status |
|---|---|---|---|---|
| 1 | 👰 AP Brides \| ఆంధ్రా వధువులు | @APBRIDE | 1 | ⬜ create |
| 2 | 🤵 AP Grooms \| ఆంధ్రా వరులు | @APGROOM1 | 1 | ⬜ create |
| 3 | 📢 TSAP Matrimony Official \| మన వివాహ — TS-AP | @TSAP_MATRIMONY | 1 | ⬜ create |
| 4 | 👰 TS Brides \| తెలంగాణ వధువులు | @TSBRIDE | 1 | ✅ LIVE |
| 5 | 🤵 TS Grooms \| తెలంగాణ వరులు | @TSGROOM1 | 1 | ✅ LIVE |
| 6 | ✝️ AP Christian Brides \| ఆంధ్రా క్రైస్తవ వధువులు | @manavivaha_christian_ap_bride | 1 | ⬜ create |
| 7 | ✝️ AP Christian Grooms \| ఆంధ్రా క్రైస్తవ వరులు | @manavivaha_christian_ap_groom | 1 | ⬜ create |
| 8 | ✝️ Telangana Christian Brides \| తెలంగాణ క్రైస్తవ వధువులు | @manavivaha_christian_ts_bride | 1 | ⬜ create |
| 9 | ✝️ Telangana Christian Grooms \| తెలంగాణ క్రైస్తవ వరులు | @manavivaha_christian_ts_groom | 1 | ⬜ create |
| 10 | 🕉️ Hindu Matrimony \| హిందూ వివాహాలు | @manavivaha_hindu | 1 | ⬜ create |
| 11 | 👰 Kamma Brides \| కమ్మ వధువులు | @manavivaha_kamma_bride | 1 | ⬜ create |
| 12 | 🤵 Kamma Grooms \| కమ్మ వరులు | @manavivaha_kamma_groom | 1 | ⬜ create |
| 13 | 👰 Kapu • Balija • Telaga Brides \| కాపు • బలిజ • తెలగ వధువులు | @manavivaha_kapu_bride | 1 | ⬜ create |
| 14 | 🤵 Kapu • Balija • Telaga Grooms \| కాపు • బలిజ • తెలగ వరులు | @manavivaha_kapu_groom | 1 | ⬜ create |
| 15 | ☪️ AP Muslim Brides \| ఆంధ్రా ముస్లిం వధువులు | @manavivaha_muslim_ap_bride | 1 | ⬜ create |
| 16 | ☪️ AP Muslim Grooms \| ఆంధ్రా ముస్లిం వరులు | @manavivaha_muslim_ap_groom | 1 | ⬜ create |
| 17 | ☪️ Telangana Muslim Brides \| తెలంగాణ ముస్లిం వధువులు | @manavivaha_muslim_ts_bride | 1 | ⬜ create |
| 18 | ☪️ Telangana Muslim Grooms \| తెలంగాణ ముస్లిం వరులు | @manavivaha_muslim_ts_groom | 1 | ⬜ create |
| 19 | 👰 Reddy Brides \| రెడ్డి వధువులు | @manavivaha_reddy_bride | 1 | ⬜ create |
| 20 | 🤵 Reddy Grooms \| రెడ్డి వరులు | @manavivaha_reddy_groom | 1 | ⬜ create |
| 21 | 👰 Brahmin Brides \| బ్రాహ్మణ వధువులు | @manavivaha_brahmin_bride | 2 | ⬜ create |
| 22 | 🤵 Brahmin Grooms \| బ్రాహ్మణ వరులు | @manavivaha_brahmin_groom | 2 | ⬜ create |
| 23 | 👰 Madiga Brides \| మాదిగ వధువులు | @manavivaha_madiga_bride | 2 | ⬜ create |
| 24 | 🤵 Madiga Grooms \| మాదిగ వరులు | @manavivaha_madiga_groom | 2 | ⬜ create |
| 25 | 👰 Mala Brides \| మాల వధువులు | @manavivaha_mala_bride | 2 | ⬜ create |
| 26 | 🤵 Mala Grooms \| మాల వరులు | @manavivaha_mala_groom | 2 | ⬜ create |
| 27 | 💍 Munnuru Kapu Matrimony \| మున్నూరు కాపు — వధువులు + వరులు | @manavivaha_munnuru_kapu | 2 | ⬜ create |
| 28 | 🌍 NRI Telugu Matrimony \| విదేశీ సంబంధాలు | @manavivaha_nri | 2 | ⬜ create |
| 29 | 🕊️ Other Religions \| ఇతర మత వివాహాలు | @manavivaha_other_religions | 2 | ⬜ create |
| 30 | 💍 Second Marriage \| రెండో పెళ్లి | @manavivaha_second | 2 | ⬜ create |
| 31 | 👰 Velama Brides \| వెలమ వధువులు | @manavivaha_velama_bride | 2 | ⬜ create |
| 32 | 🤵 Velama Grooms \| వెలమ వరులు | @manavivaha_velama_groom | 2 | ⬜ create |
| 33 | 💍 Viswabrahmana (Viswakarma) Matrimony \| విశ్వబ్రాహ్మణ — వధువులు + వరులు | @manavivaha_viswabrahmana | 2 | ⬜ create |
| 34 | 👰 Arya Vysya • Komati Brides \| వైశ్య • కోమటి వధువులు | @manavivaha_vysya_bride | 2 | ⬜ create |
| 35 | 🤵 Arya Vysya • Komati Grooms \| వైశ్య • కోమటి వరులు | @manavivaha_vysya_groom | 2 | ⬜ create |
| 36 | 👰 Yadava • Goud • Golla Brides \| యాదవ • గౌడ • గొల్ల వధువులు | @manavivaha_yadava_goud_bride | 2 | ⬜ create |
| 37 | 🤵 Yadava • Goud • Golla Grooms \| యాదవ • గౌడ • గొల్ల వరులు | @manavivaha_yadava_goud_groom | 2 | ⬜ create |
| 38 | ♿ Differently-Abled \| ప్రత్యేక సామర్థ్యం | @manavivaha_able | 3 | ⬜ create |
| 39 | 🚨 Fraud Alerts \| మోసం జాగ్రత్త | @manavivaha_alerts | 3 | ⬜ create |
| 40 | 🤝 Bureau / Broker Network \| బ్రోకర్ల నెట్‌వర్క్ | @manavivaha_bureau | 3 | ⬜ create |
| 41 | 🏛️ Govt Jobs Matrimony \| ప్రభుత్వ ఉద్యోగులు | @manavivaha_govt | 3 | ⬜ create |
| 42 | 💞 Inter-Faith & Love \| ప్రేమ వివాహాలు | @manavivaha_interfaith | 3 | ⬜ create |
| 43 | 💍 Lambada • Banjara (ST) Matrimony \| లంబాడ • బంజార — వధువులు + వరులు | @manavivaha_lambada_banjara | 3 | ⬜ create |
| 44 | 💍 Mudiraj • Tenugollu Matrimony \| ముదిరాజ • తెనుగొల్ల — వధువులు + వరులు | @manavivaha_mudiraj | 3 | ⬜ create |
| 45 | 💍 Other BC Communities Matrimony \| ఇతర BC కులాలు — వధువులు + వరులు | @manavivaha_others_bc | 3 | ⬜ create |
| 46 | 💍 Other SC Communities Matrimony \| ఇతర SC కులాలు — వధువులు + వరులు | @manavivaha_others_sc | 3 | ⬜ create |
| 47 | 💍 Other ST Communities Matrimony \| ఇతర ST కులాలు — వధువులు + వరులు | @manavivaha_others_st | 3 | ⬜ create |
| 48 | 💍 Padmashali • Devanga (Weavers) Matrimony \| పద్మశాలి • దేవాంగ — వధువులు + వరులు | @manavivaha_padmashali_weavers | 3 | ⬜ create |
| 49 | 🩺 Doctors & Teachers Matrimony \| వైద్యులు + ఉపాధ్యాయులు | @manavivaha_professionals | 3 | ⬜ create |
| 50 | 💍 Raju • Kshatriya Matrimony \| రాజు • క్షత్రియ — వధువులు + వరులు | @manavivaha_raju_kshatriya | 3 | ⬜ create |
| 51 | 💻 Software Matrimony \| సాఫ్ట్‌వేర్ ఉద్యోగులు | @manavivaha_software | 3 | ⬜ create |
| 52 | 🏆 Success Stories \| విజయ గాథలు | @manavivaha_success | 3 | ⬜ create |

📄 **Ivi kooda chudandi:** `CHANNEL-CREATE-LIST-TELUGU.md` (phone lo copy-paste list) · `CHANNELS-SMART-STRUCTURE-TELUGU.md` (smart structure explanation + names) · `CHANNELS-SETUP-CHECKLIST.md` · `channel-kits/<key>.md` (prathi channel ki description + pinned welcome ready).

## 5️⃣ ONE-BY-ONE TO-DO (ee order lo cheyyandi)

### Step 0 — Bots ready (10 min)
1. Telegram → **@BotFather** → new bot (backup) → token copy → `.env` → `BOT_TOKEN_BACKUP=...`
2. Malli new bot (alert) → `BOT_TOKEN_ALERT=...` → `.env` (`ADMIN_CHAT_ID=` mee chat id kooda pettandi)
3. `docker-compose restart backend`
4. `curl localhost:8000/api/bots/health` → 3 bots configure ayinayi ani chupinchali

### Step 1 — Channels create (phone lo — wave 1 mundu)
1. `python setup_channels.py --create-list` → **CHANNEL-CREATE-LIST-TELUGU.md** open cheyyandi (phone lo)
2. Prathi channel: **New Channel** → name copy → Public → username copy → create
3. **Administrators → Add → @telugumatrimony1_bot + backup bot + alert bot** (3 ni add cheyyandi!)
4. `BOT_TOKEN=... python setup_channels.py --apply --key <key>` → title + description + DP + 📌 pinned auto set
5. Wave-1 antha ayyaka: `python setup_channels.py --apply --wave 1 --mark-live`
6. Verify: `python setup_channels.py --check` → `✅ ready: 17 | ⬜ missing: 0` ravachu

### Step 2 — WhatsApp numbers connect (30 min)
1. 3 SIM ready (leda 2 — modati sari 2 tho start cheyyandi, tarvata 3rd add cheyyandi)
2. `docker-compose up -d whatsapp-bridge whatsapp-bridge2 whatsapp-bridge3`
3. Prathi QR scan: `:3001/qr`, `:3002/qr`, `:3003/qr`
4. `.env` → `WA_INSTANCES=[...]` (paina unna JSON) → `docker-compose restart backend`
5. `curl localhost:8000/api/wa/status` → 3 instances `connected` ani chupinchali

### Step 3 — Failover test (5 min)
1. `curl localhost:8000/api/system/health` → `ok: true` vasthe anni ready
2. Oka bridge ni aapesi test: `docker-compose stop whatsapp-bridge` → profile register cheyyandi → wa2/wa3 nunchi post vellali (`/api/publish/log` lo instance peru kanipisthundi)
3. `docker-compose start whatsapp-bridge`
4. Telegram: `/api/system/health` lo bots `post_order` lo backup kanipisthundi

---

## 6️⃣ COST / EFFORT SUMMARY

| Item | Enni | Cost | Effort |
|---|---|---|---|
| Telegram bots | 3 | **₹0** (free) | 10 min |
| WhatsApp numbers | 3 | SIM charges (₹0–₹200/నెల) | 30 min (QR scan) |
| Channels | 52 | **₹0** | Wave-1 20 → ~2 గంటలు (phone lo) |
| Bot API rate limit | — | — | 30 msg/sec/bot, ~20 msg/min/channel |
| WhatsApp safety | — | — | 60/day/number, 120–170 sec gap, target cap 8 |

✅ **Bottom line:** 3 bots + 3 numbers + 52 channels = okka post kooda miss avvadu, ban risk chala thakkuva, mari ekkuva profiles ki reach.