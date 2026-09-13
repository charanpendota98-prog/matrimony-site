# ULTRA Advanced Startup Plan — Never Before Matrimony 🚀🔥
> Nee kotha ideas anni kalipi — Referral + Limit + Bureau + 2nd Marriage + Admin Control + Top-Level Advanced

## 0. Nuvvu Cheppina Kotha Points (Nenu Note Chesina) ✅

1.  **Limit System:** Vadiki pampina profiles ki limit pettadam, limit ayyaka malli money kattali
2.  **ID Search Always Open:** Limit ayina kuda, ID tho search chesthe profile open avvali (photos tho)
3.  **Personalized Match Reason:** "Nuvvu ilaga anukunnavu, ee ammai/abbai ilaga set avuthadu chusuko" ani reason tho pampali, vere random profiles vaddu
4.  **Main 4 Channels + Caste Channels:** Main 4 (TS/AP Bride/Groom) + caste-wise extra
5.  **Broker Referral:** Form lo "Miru evarivalla telisindi?" → valla number/code → vallu ₹99 kattagane refer chesina vallaki amount send
6.  **Referral Leaderboard:** Highest refer chesina valla list, top level
7.  **Marriage Bureau B2B:** Already bureau run chese vallaki subscription — vallu 25 members ni correct ga techchi payment cheyisthe, manam vallaki amount + mana profiles share chestham
8.  **Special Categories:** 2nd Marriage, Handicapped, Widow/Divorced ki separate
9.  **Admin Only Control:** Manaku matrame full access, vallu profile chuskuntaru kani payment cheyakapothe manam manual ga premium cheyochu
10. **More & More Advanced, Easy, Never Before**

**Idantha 100% possible, nenu ippude architecture ichesta.**

---

## 1. Credit / Limit System — Money Ravadam Ikkade 💰

Idi ne business ki heart. Limit lekapothe okkasari ₹99 kattesi lifetime profiles chustaru — loss.

### Plan & Credits:

| Plan | Price | Credits | Daily Auto | ID Search | Validity |
|---|---|---|---|---|---|
| **FREE** | ₹0 | 3 profiles (Numbers LOCK 🔒) | Week ki 1 (no numbers) | ✅ Yes, photos blur + details only | Lifetime |
| **Trial** | ₹99 | 10 Credits (10 numbers unlock) | Rojoo 2 profiles (numbers tho) | ✅ Full photos + details | 30 days |
| **Premium** | ₹299 | 50 Credits + Top Priority | Rojoo 5 profiles | ✅ Full + Voice intro kooda | 60 days |
| **VIP / Bureau** | ₹999 | Unlimited + Bureau Dashboard | Rojoo 10 + Bureau API | ✅ All + Contact direct | 90 days |

**Credit ante enti?**
- 1 Credit = 1 profile number chudadam
- User ki 10 credits unte, 10 mandi numbers chudochu
- 10 ayipogane → Bot: `⚠️ Me credits ayipoyayi! Malli ₹99 tho 10 credits pondandi or ₹299 ki upgrade avvandi — 50 profiles! [Pay Now]`
- **ID Search:** Credits ayina kuda `TSAP-1042` ani search chesthe profile open avuthundi, kani number chudali ante credit kavali or Pay. Photos: Free vallaki 1 photo blur, Paid vallaki 3 photos clear. **Idi ne adigina logic — perfect!**

**Backend Logic:**
```python
if user.credits > 0:
    show_number()
    user.credits -= 1
else:
    show_pay_wall()
# ID search always allowed
if search_by_id:
    show_profile_details() # but number = lock if credits==0
```

---

## 2. Personalized Match Reason — "Nuvvu Ilaga Anukunnavu..." 🧠❤️

Random profiles pampithe nammakam pothundi. Prati match ki **reason** cheppali — AI laaga.

**Example User Expectation:** "Naku Hyderabad lo Software chese Reddy ammai kavali, age 23-26, BTech"

**Bot Pampedi:**
```
⭐ 92% BEST MATCH — Meeku Idhi Perfect! 👇

👰 TSAP-F-2025-1042 | Age 24 | Reddy | BTech | Software @ Hyd

✅ Nuvvu Adigina Daaniki 100% Set:
• Nuvvu Hyd kavali annavu → Ammai kooda Hyd lo ne (Gachibowli)
• Nuvvu Software annavu → Ammai kooda Software (Infosys, 60k)
• Nuvvu Reddy annavu → Ammai kooda Reddy, Gothram kooda same kaadhu (safe)
• Age: Nuvvu 27, Ammai 24 → 3 years gap, perfect
• Education: Iddaru BTech — understanding baguntundi

📍 Location: Mee intiki 15km dooram lone
💬 Ammai expectation: "Hyd lo unna abbai, Govt/Software, same caste"

[❤️ Interest Pampu] [📞 Number Chudu (1 Credit)] [⏭️ Next]
```

**Ela Generate Chestham?**
Backend lo simple template engine:
```python
reasons = []
if user.wanted_location == match.location: reasons.append(f"Nuvvu {location} kavali annavu → Ammai kooda {location} lone")
if user.wanted_job == match.job: reasons.append(...)
# ... 5 reasons max
final_text = "\n".join(reasons)
```
**Future AI:** User expectations ni full sentence lo rasina kuda AI (BERT) ardham cheskuni matching reason chepthundi. Ippudu template tho start, taruvata AI.

**Rule:** 70% kanna thakkuva unna profiles **asalu pampavaddu**. 3-5 high-quality matches = 100 random kanna best. **Quality > Quantity — idi top matrimony secret.**

---

## 3. Referral Program — 3 Levels (Nee Adigina Broker Idea Super!) 👥💸

### Level-1: Normal User Referral

- Prati user ki unique code: `TSAP-REF-1042` or link `t.me/tsap_bot?start=ref_1042`
- Form lo field: `👥 Meeku evaru chepparu? Referral Code / Phone (optional) [Skip]`
- Flow:
  - A (TSAP-1042) → B ki link share chesadu
  - B form fill + ₹99 pay → Webhook → A ki **₹20 cashback** or **2 Free Credits** (nee istam)
  - Bot A ki: `🎉 Congrats! Me friend TSAP-1050 pay chesadu. Meeku ₹20 vachindi / 2 credits vachayi!`
- Payout: RazorpayX auto or manual UPI (weekly once)

### Level-2: Broker Referral (Professional Brokers)

- Broker ki separate registration: `Broker Code: BROKER-RAJU-01`
- Broker Dashboard (simple web page):
  - Total refers: 45
  - Paid converts: 30
  - Earnings: ₹900 (30×₹30)
  - Link: `tsapmatrimony.com/r/BROKER-RAJU-01`
- Commission:
  - Per paid ₹99 → Broker ki **₹30** (30%)
  - 25 paid users in a month → **Extra Bonus ₹500**
  - 50 paid → Bonus ₹1200 + **Mana profiles share** (API / WhatsApp group lo daily 10 best profiles — vallu vallu clients ki pampukovachu, kani numbers manadaggare lock)

**Form lo broker number ela?**
User form lo `Referral Phone` field lo `98480xxxxx` kodithe → backend check → adi broker phone a? → Yes → broker ki commission.

### Level-3: Marriage Bureau B2B Subscription (Startup Level) 🏢

Already marriage bureau nadipisthunna vallu (Hyd lo 500+ unnaru) — vallaki oka offer:

| Bureau Plan | Price | Vallaki Emi Vasthundi | Manaki Emi Vasthundi |
|---|---|---|---|
| **Bureau Starter** | ₹999/mo | 100 profiles share (white-label card — vallu peru kooda card meeda), 25 credits, Bureau Dashboard | 25 new paid users guarantee (vallu techali), vallu clients nunchi extra charge cheskuntaru |
| **Bureau Pro** | ₹2999/mo | 500 profiles, Unlimited credits, API access, Vallu peru tho Telegram channel kooda manam create chesi istham | 100 paid users + 20% revenue share from their clients |

**Bureau Flow:**
1. Bureau manadaggara subscribe → manam `BUREAU-SRI-01` code istham
2. Bureau valla clients ni mana form link (with bureau code) tho register cheyistharu
3. Client pay cheste → Bureau ki 30% + manaki 70%
4. Bureau correct profiles (fake kaakunda) isthe → manam "Verified Bureau ✅" badge istham → vallaki inka ekkuva clients vastharu
5. **Fraud control:** Bureau pampina profile kooda mana admin approve cheyyali

**Leaderboard (Top Referrers):**
- Weekly Bot lo + Website lo: `🏆 Top 5 Referrers This Week: 1. Raju (32 refers) — ₹960 earned`
- Competition valla inka ekkuva referrals vasthayi — **viral loop**.

---

## 4. Channel Structure — Main 4 + Caste + Special (Final) 📢

**Nee maata prakaram — Main 4 + Caste wise + Special separate — idi perfect:**

### LEVEL-1: Main 4 (Must — Day-1 nundi)

| Channel | Username | Content |
|---|---|---|
| 👰 TS Brides | `@ts_brides` | TS ammayilu — anni castes, anni categories |
| 🤵 TS Grooms | `@ts_grooms` | TS abbayilu |
| 👰 AP Brides | `@ap_brides` | AP ammayilu |
| 🤵 AP Grooms | `@ap_grooms` | AP abbayilu |

### LEVEL-2: Caste Wise (20 — Waves lo)

`@tsap_reddy`, `@tsap_kamma`, `@tsap_kapu`, `@tsap_velama`, `@tsap_vysya`, `@tsap_brahmin`, `@tsap_goud`, `@tsap_yadav`, `@tsap_mudiraj`, `@tsap_padmashali`, `@tsap_raju`, `@tsap_lingayat`, `@tsap_sc_mala`, `@tsap_sc_madiga`, `@tsap_st_lambadi`, `@tsap_muslim`, `@tsap_christian`, `@tsap_open` (intercaste), etc.

**Bot Auto-Router:** Profile approve ayyagane → Main 4 lo okadantlo + Caste channel lo + Special aithe special lo kooda — **one post = 3 channels lo auto**.

### LEVEL-3: Special Categories (Separate — Chala Important) ✨

| Special Channel/Tag | Enduku Separate? | Bot Tag |
|---|---|---|
| 💔 2nd Marriage / Divorced / Widow | 1st marriage vallatho kalipithe uncomfortable | `#SecondMarriage` |
| ♿ Handicapped / Special Needs | Vallaki separate respect + matching | `#Special` |
| 🌍 NRI / Abroad | USA, Gulf vallaki separate demand | `#NRI` |
| 👮 Govt Jobs Only | Chala mandi Govt job ne kavali antaru — hot category | `#GovtJob` |
| 🩺 Doctors / Engineers / Software | Profession wise kooda | `#Doctor` |

**Implementation:** Form lo `Marital Status` = Divorced aithe → auto tag `#SecondMarriage` → Main 4 + Caste + Special channel lo kooda post. User filter lo "2nd marriage chupinchu/vaddu" option.

**Launch Waves (Empty channel death kabatti):**
- **Wave-1 Day-1:** Main 4 + Reddy, Kamma, Kapu, Velama + 2nd Marriage = **9 channels** (min 20 profiles each)
- **Wave-2 Week-2:** +6 caste + Handicapped + Govt Jobs = **17**
- **Wave-3 Week-4:** Migilina caste + NRI + etc = **25+**

---

## 5. Admin Only Control — Nee Chethilo Full Power 🔐

**Nuvvu adigavu: "Manaku matrame access undali, vallu profile chuskuntaru kani payment cheyakapothe manual premium" — 100% correct, idi pettali:**

### Admin Panel (Web + Telegram Bot):

| Feature | Ela Panichestundi |
|---|---|
| **Approve/Reject** | Kotha profile vasthe Admin Bot lo Card + 2 buttons: [✅ Approve] [❌ Reject + Reason]. Approve chesthe ne channels lo post |
| **Manual Premium** | Admin Panel lo ID search `TSAP-1042` → [💎 Make Premium - 10 Credits Free] → user ki instant unlock. Payment rakapoyina, manchi profile aithe manam free ga ivvochu (marketing) |
| **Credit Control** | `TSAP-1042 ki 5 credits add cheyyi / minus cheyyi` |
| **Number View** | Phone numbers DB lo encrypted, admin kooda "View Number" button nokkithe ne kanipistundi + log avuthundi (misuse aapadaniki) |
| **Fake Block** | Report 2 vasthe auto-hide + admin ki alert. Admin block chesthe — profile delete + phone blacklist |
| **Bureau Control** | Bureau dashboard lo vallu pampina profiles list, vallu earnings, vallu fake chesthe ban |
| **Analytics** | E roju entha mandi register, entha mandi pay, e caste lo demand, e channel nunchi ekkuva users — motham graph tho |

**Security:**
- Admin login = OTP + Password (2-factor)
- Photos direct link tho open kaavu — only via bot/backend (hotlink block)
- Backup daily 2AM

---

## 6. Never Before Features — Top Matrimony kante Advanced ga (Nuvvu Adigina) 🌟

Ivi pedithe **"Intha advanced matrimony eppudu chudaledu"** antaru:

### A) Trust & Safety (Ammayilu Safe ga Feel Avvali — Ledante Business Ledu)
1.  **Photo-Private Mode:** Ammayi "Na photo only paid members ki chupinchu" ante — public channels lo silhouette + details only. Interest accept/pay ayyaka ne photo. **Female registrations 2x avuthayi.**
2.  **Selfie Verification (AI):** Profile photo + selfie match → ✅ Verified badge. Fake photos 90% tagguthayi.
3.  **Family Group Auto-Create:** Interest accept ayyaka — Bot automatic ga private Telegram group create chesthundi: `TSAP-F-1042 ❤️ TSAP-M-1030 Family Group` — iddaru families matladukovali. **Idi Shaadi.com lo kooda ledu!**
4.  **Fraud AI:** Same phone tho 3 profiles, Google nunchi donga photo, 18 years kanna thakkuva — auto reject.

### B) Easy & Advanced UX
5.  **Voice Intro 30 sec:** "Na peru Raju, nenu Hyd lo software..." — photo kanna 10x trust.
6.  **Natural Language Search:** Bot lo `Naku Hyd lo 5'5" paina unna Reddy ammai, BTech, 24-27` ani Telugu lo type cheste — AI ardham cheskuni profiles isthundi.
7.  **Daily Auto Status:** User ki roju 9AM ki WhatsApp/Telegram lo "Good Morning! Meeku 2 kotha profiles vachayi (91%, 88%) — chudandi"
8.  **One-Tap Interest:** Profile kinda [❤️ Interest Pampu] → Avatali vallaki "TSAP-1042 ki mee profile nachindi, Accept?" → Accept → Iddariki numbers + Family group auto.
9.  **Success Story Auto Maker:** Pelli ayyaka couple photo + 2 lines isthe — Bot auto ga beautiful success card chesi Official channel lo post + referral bonus ₹500 gift.

### C) Business Growth
10. **Referral Leaderboard + Weekly Contest:** Top referrer ki ₹1000 prize — viral.
11. **Bureau White-Label:** Bureau vallaki card meeda `Powered by TSAP | Via Sri Sai Bureau` ani — vallaki branding, manaki marketing.
12. **Smart Renewal:** Plan ayipovadaniki 3 roju mundhu "Me plan ayipothundi, renew cheste 5 extra credits FREE" — retention 3x.

---

## 7. Full Tech Stack — Oracle VM lo (Final) 💻

| Part | Tech | Work |
|---|---|---|
| Frontend Form + Website | Next.js + Tailwind + Framer Motion | Neat form, referral field, ID search, filters, admin panel |
| Backend | FastAPI (Python) | Register, ID gen, Card gen, Matching, Credits, Referral, Payment webhook |
| Telegram Bot | aiogram 3.x | Register flow Telugu, Approve bot, Auto-router, Daily sender |
| Database | Postgres | Users, Payments, Credits, Referrals, Bureaus, Posts |
| Queue | Redis + Celery | Daily matches, WhatsApp queue, Referral payouts |
| Card Gen | Pillow + rembg + qrcode | Template + ID + watermark + hashtags |
| Payment | Razorpay + RazorpayX (for payouts) | ₹99/₹299/₹999 + referral payouts auto |
| Hosting | Oracle VM + Docker + Nginx + SSL | FREE |
| WhatsApp | WhatsApp Cloud API (later) + Baileys (starting semi-auto) | Auto matches, broadcast |
| AI (Phase-2) | Sentence-BERT + Face Verify lib | Reason generator, Natural search, Photo verify |

---

## 8. Project Structure — Code Ekkada Pedathamo 📁

```
matrimony-site/
├── frontend/ (Next.js)
│   ├── app/register/page.tsx (Form + Referral field + OTP)
│   ├── app/search/[id]/page.tsx (ID search — credits logic)
│   ├── app/admin/page.tsx (Admin panel — Approve, Credits, Bureau)
│   └── app/bureau/page.tsx (Bureau Dashboard)
├── backend/
│   ├── main.py (FastAPI)
│   ├── models.py (User, Credit, Referral, Bureau)
│   ├── card_gen.py (ID + Template)
│   ├── matching.py (Score 0-100 + Reason Generator)
│   ├── referral.py (Code gen, Commission, Leaderboard)
│   ├── credits.py (Limit logic)
│   ├── telegram_router.py (Main 4 + Caste + Special auto-post)
│   └── payment.py (Razorpay webhook + payout)
├── bot/
│   └── bot.py (Telegram bot full flow)
└── docker-compose.yml
```

---

## 9. Money Flow — Ippudu Inka Clear 💸

**Normal User:**
1000 registers → 200 pay ₹99 (₹19,800) → 50 upgrade ₹299 (₹14,950) = ₹35k
Referral valla: 200 paid users × avg 2 refers = 400 extra registers → 80 extra paid = +₹8k → Total ₹43k

**Bureau:**
10 bureaus × ₹999 = ₹9,990 + vallu tecchina 10×25=250 paid users × ₹99 × 70% = ₹17,325
**Grand Total (1000 users + 10 bureaus): ~₹70k/month**

Kharchu: Domain ₹1000/yr + Razorpay 2% (~₹1400) + WhatsApp API later ₹2500 = **Profit ~₹65k**

**Scale:** 10k users + 50 bureaus → ₹6-7 Lakhs/month possible — **startup level!**

---

## 10. Next Steps — Nenu Ippude Build Cheyala? 🚀

Ne ideas anni 100% clear. Naa suggestion order:

**Phase-1 (7 days — MVP):**
1.  **B) Web Form + Card + ID + Credits + Referral Field** — Neat form with "Evarivalla telisindi?" + ID + template + backend + ID search page
2.  **A) Telegram Bot + Main 4 Channels Auto-Router + Special Tags**
3.  **C) Matching + Reason Generator + Limit + Payment**

**Phase-2 (Week-2):**
4.  Bureau Dashboard + Leaderboard + Admin Manual Premium
5.  WhatsApp auto sender + Daily 9AM

**Nenu ippude start chestha — edi mundhu?**

**OPTION 1: 📝 Advanced Web Form (Referral + Credits + ID Search) — LIVE PREVIEW tho**
Form fill → ID + Card generate → Credits logic → ID search → Reason tho matches — motham website lo live chupistha

**OPTION 2: 🤖 Telegram Bot + Auto-Router (Main 4 + Caste + 2nd Marriage separate)**

**OPTION 3: 💸 Referral + Bureau System (Full Commission + Leaderboard)**

**Neeku edi mundhu kavali? Nenu cheppedi: OPTION 1 — Form nunchi start cheste, migilina automation easy. Form ready ayyaka Telegram/WhatsApp ki connect cheyochu.**

Brand name final enti? `TSAP Matrimony` ne continue cheddama? Ledante kotha peru? (ID, usernames, referral codes anni danimeeda)

Cheppu anna, **OPTION 1 Form + Card + Credits + Referral** nunchi code start cheddama? 2-3 gantalalo LIVE preview istha! 👌🔥
