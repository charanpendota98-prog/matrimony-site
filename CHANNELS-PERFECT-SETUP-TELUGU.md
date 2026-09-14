# 📢 CHANNELS — PERFECT SETUP (4 Main + Caste × Bride/Groom) 🇮🇳

> **Status:** registry ready (83 channels) • kit + DP + automation ready • 4 main channels meere create chesaru (TSBRIDE, TSGROOM1) — AP + caste channels ippudu add cheyyali.
> Ee file `backend/setup_channels.py --plan` + `channels_config.py` nunchi auto-sync (drift undadu).

---

> 🔁 **Bots + WhatsApp numbers failover (enni kavali, ela set cheyyali):** **FAILOVER-BOTS-WHATSAPP-TELUGU.md**

---

## 1) Architecture — enduku idi best 🏆

```
📢 TSAP Matrimony Official (@TSAP_MATRIMONY)        ← brand hub (top-3/day + success + alerts)
│
├── 📍 MAIN 4 (volume — anni profiles ivi first)
│     👰 TS Brides  @TSBRIDE     ✅ LIVE
│     🤵 TS Grooms  @TSGROOM1    ✅ LIVE
│     👰 AP Brides  @APBRIDE     ⬜ create (wave 1)
│     🤵 AP Grooms  @APGROOM1    ⬜ create (wave 1)
│
├── 💍 CASTE PRAKARAM — top 18 castes ki **bride/groom separate** (36 channels)
│     👰 Reddy Brides  @manavivaha_reddy_bride   🤵 Reddy Grooms  @manavivaha_reddy_groom
│     👰 Kamma Brides  @manavivaha_kamma_bride   🤵 Kamma Grooms  @manavivaha_kamma_groom
│     … (Kapu, Velama, Vysya, Brahmin → wave 1 | Goud, Yadav, Mudiraj, Padmashali, Munnuru Kapu, Mala → wave 2
│        | Madiga, Lambada, Raju, Balija, Telaga, Viswakarma → wave 3)
│
├── 💍 migilina 25 castes — okate mixed channel (andulo #Bride / #Groom hashtag filter)
│     💍 Kummara Matrimony @manavivaha_kummara … (43 castes motham cover)
│
├── 🕊️ Religion — Hindu • Muslim • Christian • Other • Inter-faith/Love
└── ⭐ Special — 2nd marriage • differently-abled • govt jobs • software • doctors • teachers • 35+ • success stories • fraud alerts • bureau
```

**Enduku caste × bride/groom?** Telugu intlo vaallu **tama caste + bride/groom** channel ne follow avutaru (Reddy inti vaallu "Reddy Brides" chustaru). Anduke top castes ki separate — chinna castes ki okate channel (ekkada khali ga kanipinchadu, post volume maintain avutundi).

**Spam control:** okka profile **max 5 channels** lo matrame post avutundi (priority order lo) —
edaiana okkati miss avvali ante special channel (govt/software/doctors/35+/2nd marriage) priority penchutundi.

### Motham count
| Tier | Enti | Enni |
|---|---|---|
| L0 Official | brand hub | 1 |
| L1 Main 4 | TS/AP × Bride/Groom (+ NRI) | 5 |
| L3 Caste | 36 (18 castes × bride/groom) + 25 mixed | 61 |
| L2 Religion | Hindu, Muslim, Christian, Other, Inter-faith | 5 |
| L4 Special | 2nd marriage, able, govt, IT, doctors, teachers, 35+, love, success, alerts, bureau | 11 |
| **TOTAL** | | **83** |

---

## 2) 🌊 Wave plan (e order lo create cheyyali)

| Wave | Enni channels | Enti |
|---|---|---|
| **Wave 1** | **17** | Official + Main 4 (TS/AP × Bride/Groom) + **top 6 castes × bride/groom** (Reddy, Kamma, Kapu, Velama, Vysya, Brahmin) |
| Wave 2 | 18 | Goud, Yadav, Mudiraj, Padmashali, Munnuru Kapu, Mala (×2) + Religion 5 + 2nd marriage + govt |
| Wave 3 | 22 | Madiga, Lambada, Raju, Balija, Telaga, Viswakarma (×2) + doctors, software, 35+, success, alerts, bureau, other religion, interfaith |
| Wave 4 | 26 | migilina 25 castes (mixed) + teachers |

> Munda wave-1 (17 channels) perfect ga cheyyandi — vaati lo volume vastundi, appudu wave-2 ki vellandi.
> Telegram ki okkoka account ki channel creation ki silent limits untayi — "Too many attempts" vaste 24h aagi malli try cheyyandi.

---

## 3) ⚡ Setup — 3 nimushalalo prathi channel perfect

### Step A — Channel create (phone lo, 30 sec each)
1. Telegram → **New Channel** → Name paste (kit file nunchi) → **Public** → Username paste
   (username already taken ayithe → kit lo unna **fallback** okkati vadandi)
2. Description paste → Create

### Step B — Bot ni admin cheyyi (2 taps)
Channel → **Administrators** → **Add Admin** → `@telugumatrimony1_bot` → ✅ **Change Channel Info**, ✅ Post Messages, ✅ Edit Messages, ✅ Delete Messages, ✅ Pin Messages

### Step C — Okka command (title + desc + DP + 📌 pinned + invite link auto)
```bash
cd backend
export BOT_TOKEN=123456:ABC...            # @BotFather → /mybots → API Token
python setup_channels.py --check          # e channels ready unnayi chudu (admin ok na?)
python setup_channels.py --apply --wave 1  # wave-1 anni channels ni PERFECT ga set cheyyi
python setup_channels.py --apply --key c_reddy_bride   # okkate channel ki
python setup_channels.py --apply --wave 1 --mark-live  # + registry lo LIVE ani mark cheyyi
```

**Automation em chestundi (prathi channel ki):**
1. `getChat` → channel unda? username ok na? (fallback tho try chestundi)
2. **Bot admin check** → admin kaakapote clear Telugu error isthundi (em cheyyalo chepthundi)
3. `setChatTitle` → perfect Telugu title (`👰 Reddy Brides | రెడ్డి వధువులు`)
4. `setChatDescription` → 255-char Telugu description (keywords + ₹99 + site + bot)
5. `setChatPhoto` → 512×512 DP image (`backend/channel_assets/<key>.png`)
6. `createChatInviteLink` → permanent invite link (state file lo save)
7. `sendMessage` + `pinChatMessage` → **📌 pinned welcome post** (rules + 3-step flow + pricing)
8. State file (`channel_setup_state.json`) → malli run chesthe duplicate welcome pampadu, patch avvadu

### Step D — Website nunchi copy-paste (bot automation vadakapoyina)
`/channels` page lo prathi channel card ki:
- 🖼️ DP image (download button tho) • 📋 **Kit** button → description / 📌 pinned post / rules / WhatsApp share text — anni **copy** buttons tho

---

## 4) 🛠️ Commands reference

```bash
python setup_channels.py --plan              # anni 83 channels plan + CHANNELS-SETUP-CHECKLIST.md
python setup_channels.py --plan --wave 1     # wave-1 matrame (17)
python setup_channels.py --kit --wave 1      # channel-kits/*.md (prathi channel ki 6-step kit)
python setup_channels.py --photos            # 83 DP images generate (backend/channel_assets/)
python setup_channels.py --check             # Telegram status: exists / admin / desc / members
python setup_channels.py --apply --wave 1    # auto: title + desc + DP + pinned + invite link
python setup_channels.py --apply --key ap_bride --force-photo
python setup_channels.py --mark-live         # verified channels ni registry lo LIVE
python setup_channels.py --self-test         # fake bot tho full flow test (token ledu, CI ki)
```

**Mukhyam:** Telegram **Bot API lo channel create cheyyadam ledu** (bot create cheyyaleedu) — anduke Step A manual (30 sec), taruvata antha automation. Idi Telegram rule; bypass ledu.

---

## 5) ✍️ Content standards (prathi channel ki same quality)

| Item | Ela untundi |
|---|---|
| **Title** | keyword-first + Telugu + emoji: `👰 Reddy Brides \| రెడ్డి వధువులు` (≤128 chars, Telegram search lo top) |
| **Description** | 60–255 chars: Telugu line + `3 FREE requests, ₹99లో 5` + `manavivaha.in` + `@telugumatrimony1_bot` |
| **📌 Pinned post** | welcome + "idi ela work avutundi" + **3 steps** + 🆓 pricing + ⚠️ rules (advance money = 100% scam, no chatting, report) + links + hashtags (≤4096 chars) |
| **Rules post** | 7 rules (no spam, no money, no numbers in channel, respect, report link) |
| **DP image** | 512×512 maroon+gold, caste name English (server lo Telugu font ledu — image ki English, channel text lo Telugu) |
| **Daily posts** | 7:30 AM • 12:30 PM • 6:00 PM • 9:00 PM (ratri 8–10 highest views) + Sunday 10 AM weekly digest |
| **Hashtags** | `#Reddy #Bride #TS #AP #Hyderabad` — filter ki + Telegram search ki |

---

## 6) 🚀 First 100 members (channel growth playbook)

1. **Mana WhatsApp groups/status** — `share_text()` (kit lo undi) copy → status/story + 5 groups (anti-ban gaps tho: 120–170 sec)
2. **Existing channel nunchi** — TSBRIDE/TSGROOM1 lo new channel announce post + invite link pin
3. **Register flow lo entry** — register ayyaka user ki tama caste channels join links (deep link: `t.me/telugumatrimony1_bot?start=ch_<username>`)
4. **Invite contest** — ekkuva members teesukochina 5 mandiki FREE 1 credit (growth dashboard lo track)
5. **Local network** — function halls, photocopy shops, marriage bureaus (bureau channel lo B2B offer ₹50/profile)
   Target: per caste channel **50–100 members** = 1,500–3,000 reach. Adi matrimony ki chalu (300–400 profiles tho start).

---

## 7) ✅ Verification (anni run ayyayi)

```bash
cd backend
WA_TEST_FAST=1 /tmp/venv/bin/python test_channels_setup.py   # 78 pass / 0 fail
WA_TEST_FAST=1 /tmp/venv/bin/python test_channels_router.py  # 61 pass / 0 fail
python setup_channels.py --self-test                          # fake bot flow PASS
```
- 83 channels • usernames unique + Telegram-valid • titles ≤128 • descriptions 60–255 • config problems **0**
- 18 castes × bride/groom = 36 channels • mixed 25 • 43 castes Telugu names
- `/api/channels`, `/api/channels/photo/{key}.png`, `/api/channels/{key}/kit`, `/api/channels/setup-plan` — anni 200 (website proxy tho kooda)

---

## 8) 📌 Pending (meeru cheyyalsindi)

1. **BOT_TOKEN** — @BotFather lo `/revoke` (purathana token chat lo share ayyindi) → kotha token `.env` lo
2. **AP channels** create cheyyandi — `@APBRIDE`, `@APGROOM1` (wave-1) → bot admin
3. **Wave-1 caste channels** — 12 channels (Reddy/Kamma/Kapu/Velama/Vysya/Brahmin × bride/groom)
4. Taruvata: `python setup_channels.py --apply --wave 1 --mark-live` → anni perfect ga set avutayi
5. `/growth` dashboard lo channel progress chudandi (live/pending count + wave)
