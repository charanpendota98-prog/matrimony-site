# 🎁 WELCOME PACK — "Register avvagane WhatsApp ki 3 profiles + caste channel links"

**Status: MERGED ✅** (PR #2 → `main`, merge commit `73aa236`)

---

## 1. Mee adigindi (exact ga ela pani chestundi)

> "registration avvagane elaga vadi whatsapp ki 3 profiles vellai, mana channel links,
>  vadi caste channels — telegram and whatsapp channels — vadi caste related"

**Flow (ippudu live):**

```
User register chesadu (website / bot)
        │
        ├─ 1. Profile DB lo save + card generate
        ├─ 2. NAMASTE welcome (card + full details)  → WhatsApp queue (priority 0)
        ├─ 3. 🎁 WELCOME PACK  → WhatsApp queue (priority 0)
        │        • Mee 3 profiles  (peru, age, caste, district, education, job, ⭐ score, 🔗 link)
        │        • Mee caste channels (Telegram + WhatsApp links) — caste mundu, tarvata region → official
        │        • "Numbers 🔒 — interest accept = consent tho matrame exchange"
        └─ 4. Anti-ban order: Telegram mundu → WhatsApp tarvata (gap 120–170s, interest fast-lane 60–120s)
```

**Privacy (marchakoodadu — mana policy):**
- 🔒 Ee message lo **eppudu phone numbers undavu** (98••••••45 mask kooda message lo pettamu) — profile **links** matrame
- Number exchange = interest accept (mutual consent) → consent ledger lo record

---

## 2. Ee message ela untundi (live lo register ayina real output)

```
🎉 *Live Smoke Bride గారు — mee 3 FREE matches ready!* 🎉
🆔 *TSAP-F-2025-2065* | 💍 Reddy / Pakanati | 📍 Hyderabad, TS
━━━━━━━━━━━━━━━━

🔎 *Mee 3 profiles* (numbers 🔒 — interest accept = consent tho matrame exchange):
1️⃣ *Kiran Kumar Reddy* — 29 yrs
     Reddy, Nalgonda | MBBS • Doctor
     ⭐ 82% match • ✅ verified • 🌟 Mrigasira
     💡 Nuvvu TS kavali annavu → Groom kooda TS lone
     🔗 https://manavivaha.in/search/TSAP-M-2025-1042  (ID: TSAP-M-2025-1042)
2️⃣ ... 3️⃣ ...
✅ Interest pampali ante: mee TSAP ID + vaalla ID tho ee link open cheyyandi — 1 credit
   (modati 3 FREE), decline ayithe credit refund.

📢 *Mee caste channels — daily matches ikkada* 👇
• *👰 Reddy Brides | రెడ్డి వధువులు* — cluster=reddy + Bride
     ✈️ Telegram: https://t.me/manavivaha_reddy_bride | 🟢 WhatsApp: https://whatsapp.com/channel/...
• *👰 TS Brides ...*  ✈️ | 🟢
• *💻 Software Matrimony ...* ✈️ | 🟢
• *📢 TSAP Matrimony Official ...* ✈️ | 🟢

📱 WhatsApp channel links kooda pampistham — support ki 'CHANNEL' ani ping cheyyandi: https://wa.me/...
```

Live lo verify chesam: **3 profiles · 0 raw phone numbers · 3 Telegram + 3 WhatsApp channel links** (`TSAP-F-2025-2065`).

---

## 3. WhatsApp channel links configure ela cheyyali (server env)

Telegram links **automatic** (channel username nunchi). WhatsApp channel/community links ki real id kavali — 3 vidhanga ivvachu:

```bash
# (a) Oka channel ki okka link (recommended — real links unnappudu)
WA_CHANNEL_LINKS='{"c_reddy_bride":"https://whatsapp.com/channel/XXXX","official":"https://whatsapp.com/channel/YYYY"}'

# (b) Per-channel env (CI/scripts ki easy)
WA_CHANNEL_C_REDDY_BRIDE=https://whatsapp.com/channel/XXXX
WA_CHANNEL_OFFICIAL=https://whatsapp.com/channel/YYYY

# (c) Pattern — WhatsApp channel ids ready ayyaka generate cheyyali ante
WA_CHANNEL_PATTERN='https://whatsapp.com/channel/{key}'     # lekapote {username}

# WhatsApp messages pampadaniki bridge podu
WHATSAPP_MODE=bridge
WHATSAPP_BRIDGE_URL=http://localhost:3001
```

Configure avvakapote: Telegram link matrame veltundi + message lo **support note** ("WhatsApp channel links kooda pampistham — support ki ping cheyyandi") vastundi. Server crash avvadu.

---

## 4. Kotha endpoints (anni live + tested)

| Endpoint | Endi chestundi |
|---|---|
| `GET /api/welcome-pack/{tsap_id}` | Mee pack (3 profiles + channels + message preview) — **owner token** tho |
| `POST /api/welcome-pack/{tsap_id}/resend` | 🔁 Malli WhatsApp ki pampu (register page lo button undi) |
| `GET /api/channels/links?caste=Reddy&gender=Bride&state=TS` | Public — caste channel links (website/bot lo chupinchadaniki) |
| `POST /api/admin/vendors/{id}/token` | 🔐 Vendor token (vendor token pogottukunte support ivvadaniki) — admin key tho |

**Register response** lo kotha field: `welcome_pack` → `{profiles[3], channels[], message_text, message_preview, queue{queued, kind}, rules_telugu}`

---

## 5. Frontend (/register success screen)

- 📲 **"Mee WhatsApp ki pampinam — 3 profiles + mee caste channel links"** card
- 3 profile cards → click cheste `/search/{id}` ki veltundi (⭐ score, 🔒 number locked)
- Channel chips: **✈️ Telegram** + **🟢 WhatsApp** links
- **"📲 Malli WhatsApp ki pampu"** button (resend API)
- **"💬 WhatsApp channel link kavali? Support ki ping"**
- Privacy line: "Numbers eppudu message lo pettamu — consent tho matrame exchange"

---

## 6. Tests (anni green — ee feature ki 74 checks + full sweep)

```bash
cd backend
WA_TEST_FAST=1 /tmp/venv/bin/python test_wave10_welcome_pack.py     # 74 pass / 0 fail
WA_TEST_FAST=1 /tmp/venv/bin/python test_wave9_hardening.py         # 203 pass / 0 fail
ADMIN_KEY=... RAZORPAY_WEBHOOK_SECRET=... /tmp/venv/bin/python verify_live_flow.py --flow --vendor   # 69 pass / 0 fail
```

| Suite | Result |
|---|---|
| test_wave10_welcome_pack | **74 / 0** |
| test_wave9_hardening | **203 / 0** |
| test_privacy_contacts | 53 / 0 |
| test_interest_antiban | 84 / 0 |
| test_growth_namaste_leads | 138 / 0 |
| test_topmatch | 61 / 0 |
| test_safety_preview | 70 / 0 |
| test_redundancy | 53 / 0 |
| test_referral_advanced | 145 / 0 |
| test_vendors_ads | 130 / 0 |
| test_channels_setup | 84 / 0 |
| test_channels_router | 60 / 0 |
| verify_live_flow (live :8000) | **69 / 0** |

Frontend: `npx tsc --noEmit` clean · `npx next build` ✓ · 14 pages live lo 200.

---

## 7. Inka advanced ga em cheyyochu (next steps — cheppandi, chestham)

1. **WhatsApp channel real links** iste → pattern badulu real ids tho env set chesi, message lo exact group links (ippudu pattern tho generate avutunnai)
2. **Ee message telugu + English** rendu versions (elder parents ki telugu, NRI ki english) — user profile language batti
3. **Pack lo porutham score** (10 kootalu) + "mee jataka rasi ki ee profile best" line
4. **Resend limits** (spam taggadaniki 1/day) + "pack open ayyinda" tracking (link click = engaged lead)
5. **Caste channel auto-join**: user WhatsApp lo "JOIN" anagane bot aa caste group channel ki add chestundi (bridge tho)
6. **Vendor ads pack lo** — "pelli ki catering/photography" sponsor slot (₹149–₹3999 packages tho monetize)
7. **Weekly "kotha matches" digest** — ee week lo vachina kotha 3 profiles + caste channel top posts (saved-search alerts tho already ready)
