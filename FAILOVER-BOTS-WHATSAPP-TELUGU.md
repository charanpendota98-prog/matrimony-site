# 🔁 BOTS + WHATSAPP FAILOVER — ENNI KAVALI, ELA SET CHEYYALI (TELUGU)

> **Oke okka bot / oke okka WhatsApp number = risk.** Okati aagipoyina (ban / rate limit / bridge down / server restart) appudu posting **aagipothundi** — profile ki reach undadu. Andukane mana system lo **POOL + AUTO FAILOVER** pettamu: **okati fail aithe inkokati ventane pampistundi** — okka post kooda miss avvadu.

---

## 1️⃣ ENNI BOTS KAVALI? → **3 BOTS** (kakapote minimum 2)

| # | Bot | Purpose | Env variable | Enduku separate? |
|---|---|---|---|---|
| 1 | **Primary bot** (existing @telugumatrimony1_bot) | Channels lo **post** + users ki DM (register welcome, interest) | `BOT_TOKEN` | Idi main — 90% pani idi chestundi |
| 2 | **Backup bot** (kotha bot) | Channels lo **post** only — primary 429/401/down aithe | `BOT_TOKEN_BACKUP` | Telegram okka bot ki ~30 msg/sec limit; primary aagipote posts aagakudadu |
| 3 | **Alert bot** (kotha bot) | Admin alerts: kotha profile, interest, WhatsApp fail, monitoring | `BOT_TOKEN_ALERT` | User messages valla alert bot rate-limit avvakudadu |

**Enni channels ki add cheyyali?** — 3 bots ni **ANNI 83 channels** ki admin cheyyali (Channel → Administrators → Add → **Post + Edit + Pin + Change Info** ✅). Appude failover pani chestundi — primary aagipote backup bot **ade channel** lo post estundi.

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

## 4️⃣ CHANNELS — ANNI PERU + EEM CHESTUNTAYO (WAVE ORDER LO)

**Total: 83 channels** · live: 2 · create cheyyalsinavi: 81

### 🌊 Wave order — ila cheyyandi (okkesari anni vaddu!)
| Wave | Enni | Emi |
|---|---|---|
| **Wave 1** | 17 | Official + TS/AP bride/groom + NRI + top-6 castes × bride/groom |
| **Wave 2** | 18 | Goud, Yadav, Mudiraj, Padmashali, Munnuru Kapu, Mala (+religion/special) |
| **Wave 3** | 22 | Madiga, Lambada, Raju, Balija, Telaga, Viswakarma + migilinavi |
| **Wave 4** | 26 | Mixed-caste + region + special + utility channels |

### 📋 FULL LIST — 83 channels (copy-paste ready)

| # | Channel Name | Username | Wave | Status |
|---|---|---|---|---|
| 1 |  | @APBRIDE | 1 | ⬜ create |
| 2 |  | @APGROOM1 | 1 | ⬜ create |
| 3 |  | @TSAP_MATRIMONY | 1 | ⬜ create |
| 4 |  | @TSBRIDE | 1 | ✅ LIVE |
| 5 |  | @TSGROOM1 | 1 | ✅ LIVE |
| 6 |  | @manavivaha_brahmin_bride | 1 | ⬜ create |
| 7 |  | @manavivaha_brahmin_groom | 1 | ⬜ create |
| 8 |  | @manavivaha_kamma_bride | 1 | ⬜ create |
| 9 |  | @manavivaha_kamma_groom | 1 | ⬜ create |
| 10 |  | @manavivaha_kapu_bride | 1 | ⬜ create |
| 11 |  | @manavivaha_kapu_groom | 1 | ⬜ create |
| 12 |  | @manavivaha_reddy_bride | 1 | ⬜ create |
| 13 |  | @manavivaha_reddy_groom | 1 | ⬜ create |
| 14 |  | @manavivaha_velama_bride | 1 | ⬜ create |
| 15 |  | @manavivaha_velama_groom | 1 | ⬜ create |
| 16 |  | @manavivaha_vysya_bride | 1 | ⬜ create |
| 17 |  | @manavivaha_vysya_groom | 1 | ⬜ create |
| 18 |  | @manavivaha_christian | 2 | ⬜ create |
| 19 |  | @manavivaha_goud_bride | 2 | ⬜ create |
| 20 |  | @manavivaha_goud_groom | 2 | ⬜ create |
| 21 |  | @manavivaha_govt | 2 | ⬜ create |
| 22 |  | @manavivaha_hindu | 2 | ⬜ create |
| 23 |  | @manavivaha_mala_bride | 2 | ⬜ create |
| 24 |  | @manavivaha_mala_groom | 2 | ⬜ create |
| 25 |  | @manavivaha_mudiraj_bride | 2 | ⬜ create |
| 26 |  | @manavivaha_mudiraj_groom | 2 | ⬜ create |
| 27 |  | @manavivaha_munnurukapu_bride | 2 | ⬜ create |
| 28 |  | @manavivaha_munnurukapu_groom | 2 | ⬜ create |
| 29 |  | @manavivaha_muslim | 2 | ⬜ create |
| 30 |  | @manavivaha_nri | 2 | ⬜ create |
| 31 |  | @manavivaha_padmashali_bride | 2 | ⬜ create |
| 32 |  | @manavivaha_padmashali_groom | 2 | ⬜ create |
| 33 |  | @manavivaha_second | 2 | ⬜ create |
| 34 |  | @manavivaha_yadav_bride | 2 | ⬜ create |
| 35 |  | @manavivaha_yadav_groom | 2 | ⬜ create |
| 36 |  | @manavivaha_35plus | 3 | ⬜ create |
| 37 |  | @manavivaha_able | 3 | ⬜ create |
| 38 |  | @manavivaha_alerts | 3 | ⬜ create |
| 39 |  | @manavivaha_balija_bride | 3 | ⬜ create |
| 40 |  | @manavivaha_balija_groom | 3 | ⬜ create |
| 41 |  | @manavivaha_boya | 3 | ⬜ create |
| 42 |  | @manavivaha_bureau | 3 | ⬜ create |
| 43 |  | @manavivaha_doctors | 3 | ⬜ create |
| 44 |  | @manavivaha_interfaith | 3 | ⬜ create |
| 45 |  | @manavivaha_lambada_bride | 3 | ⬜ create |
| 46 |  | @manavivaha_lambada_groom | 3 | ⬜ create |
| 47 |  | @manavivaha_madiga_bride | 3 | ⬜ create |
| 48 |  | @manavivaha_madiga_groom | 3 | ⬜ create |
| 49 |  | @manavivaha_other_religions | 3 | ⬜ create |
| 50 |  | @manavivaha_raju_bride | 3 | ⬜ create |
| 51 |  | @manavivaha_raju_groom | 3 | ⬜ create |
| 52 |  | @manavivaha_software | 3 | ⬜ create |
| 53 |  | @manavivaha_success | 3 | ⬜ create |
| 54 |  | @manavivaha_telaga_bride | 3 | ⬜ create |
| 55 |  | @manavivaha_telaga_groom | 3 | ⬜ create |
| 56 |  | @manavivaha_viswakarma_bride | 3 | ⬜ create |
| 57 |  | @manavivaha_viswakarma_groom | 3 | ⬜ create |
| 58 |  | @manavivaha_adi_andhra | 4 | ⬜ create |
| 59 |  | @manavivaha_bestha | 4 | ⬜ create |
| 60 |  | @manavivaha_bhatraju | 4 | ⬜ create |
| 61 |  | @manavivaha_dasari | 4 | ⬜ create |
| 62 |  | @manavivaha_devanga | 4 | ⬜ create |
| 63 |  | @manavivaha_gandla | 4 | ⬜ create |
| 64 |  | @manavivaha_gavara | 4 | ⬜ create |
| 65 |  | @manavivaha_gond | 4 | ⬜ create |
| 66 |  | @manavivaha_jalari | 4 | ⬜ create |
| 67 |  | @manavivaha_jangam | 4 | ⬜ create |
| 68 |  | @manavivaha_jogi | 4 | ⬜ create |
| 69 |  | @manavivaha_kalinga | 4 | ⬜ create |
| 70 |  | @manavivaha_koppula_velama | 4 | ⬜ create |
| 71 |  | @manavivaha_koya | 4 | ⬜ create |
| 72 |  | @manavivaha_kummara | 4 | ⬜ create |
| 73 |  | @manavivaha_kuruba | 4 | ⬜ create |
| 74 |  | @manavivaha_love | 4 | ⬜ create |
| 75 |  | @manavivaha_mangali | 4 | ⬜ create |
| 76 |  | @manavivaha_rajaka | 4 | ⬜ create |
| 77 |  | @manavivaha_sc_others | 4 | ⬜ create |
| 78 |  | @manavivaha_srisayana | 4 | ⬜ create |
| 79 |  | @manavivaha_st_others | 4 | ⬜ create |
| 80 |  | @manavivaha_teachers | 4 | ⬜ create |
| 81 |  | @manavivaha_uppara | 4 | ⬜ create |
| 82 |  | @manavivaha_vadabalija | 4 | ⬜ create |
| 83 |  | @manavivaha_vaddera | 4 | ⬜ create |

📄 **Ivi kooda chudandi:** `CHANNEL-CREATE-LIST-TELUGU.md` (phone lo copy-paste list) · `CHANNELS-SETUP-CHECKLIST.md` (full plan) · `channel-kits/<key>.md` (prathi channel ki description + pinned welcome ready).

---

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
| Channels | 83 | **₹0** | Wave-1 17 → ~1 గంట (phone lo) |
| Bot API rate limit | — | — | 30 msg/sec/bot, ~20 msg/min/channel |
| WhatsApp safety | — | — | 60/day/number, 120–170 sec gap, target cap 8 |

✅ **Bottom line:** 3 bots + 3 numbers + 83 channels = okka post kooda miss avvadu, ban risk chala thakkuva, mari ekkuva profiles ki reach.