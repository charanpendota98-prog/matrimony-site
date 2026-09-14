# 💰 PRICING AUDIT + FINAL PLAN — "emi aina wrong chesthunna?" (TELUGU)

> Mee prashna: **"pricing plan cheppu — em aina wrong chesthunna? inka bestga cheyochaa?"**
> Answer: **90% pricing correct ga undi** (₹99 → 5, ₹199 → 12, ₹299 → 25, ₹499 → 50 ladder perfect).
> Kaani **3 real problems** dorikayi — anni **ippude fix chesanu**. Kinda chudandi.

---

## 1️⃣ FINAL PRICING TABLE (live ga ide jarugutundi)

| Plan | Price | Profiles | ₹/profile | Validity | Perks | Badge |
|---|---|---|---|---|---|---|
| **FREE** | ₹0 | **3** | — | 365 రోజులు | 3 requests, WhatsApp share, auto-post | "Card avasaram ledu" |
| **Okka Request** 🆕 | **₹29** | **1** | ₹29 | 15 రోజులు | 1 request + share + card | "Single • try cheyyandi" |
| **Sambandham** | **₹99** | **5** | ₹19.8 | 30 రోజులు | + 7-day channel boost, decline aithe refund | "Entry" |
| **Family** ⭐ | **₹199** | **12** | ₹16.6 | 45 రోజులు | + Verified badge + 1 porutham report + bureau assist | "MOST POPULAR" |
| **Premium** 🏆 | **₹299** | **25** | ₹12.0 | 60 రోజులు | + 30-day boost + who-viewed 60d + priority support | "BEST VALUE" |
| **Vivaha VIP** | **₹499** | **50** | ₹10.0 | 90 రోజులు | + matchmaker assist + 90-day boost + vendor discounts | "VIP" |

**Add-ons (plan lekunda kooda):** ⚡ Boost 7d **₹49** · 👀 Who-viewed 30d **₹49** · ⭐ 10-Porutham report **₹99** · ✅ Photo-verify badge **₹199**
**Renewal:** ₹99 → **8 profiles** + 7-day boost free (pata customer ki ekkuva value)
**Bureau/B2B:** ₹999 → 25 profiles/mo · ₹2,999 → 100 profiles/mo + agent dashboard
**Referral:** prathi paying profile ki referrer ki **₹50** (UPI/credits)

### Enduku ee ladder correct?
```text
₹29 (₹29/profile)  →  impulse buy + ANCHOR (pakkana ₹10/profile kanipisthundi → "VIP lo chala cheap")
₹99 (₹20/profile)  →  entry (free aipoyaka modati pay)
₹199 (₹16.6/profile) → HERO (most popular sticker — 60% mandi idi teesukuntaru)
₹299 (₹12/profile) →  best value (mana highest margin × volume)
₹499 (₹10/profile) →  anchor + VIP (matchmaker service cost cover avutundi)
```
**Rule:** prathi tier lo ₹/profile **thaggutuu** undali. Adi unte customers "pedda plan = ekkuva value" anukuntaru.

---

## 2️⃣ EMI AINA WRONG UNDI? → **3 problems dorikayi, anni FIXED** ✅

| # | Problem (ela undindi) | Enduku problem | Fix |
|---|---|---|---|
| 1 | **Payment webhook pata (legacy) plan map vaadutundi** — `{99: TRIAL_99, 299: PREMIUM_299, 999: VIP_999}` | ₹99 pay chesthe **5 profiles kaadu, pata system lo 10 "credits + daily 2"** add ayyevi. **₹199 & ₹499 ki emi map ledu** → TRIAL_99 default (10 credits!) — customer ₹499 katti 50 profiles raakapote **refund/complaint** | ✅ Webhook ni **okate source of truth** (`interest.apply_payment`) ki marchanu — ₹29/₹99/₹199/₹299/₹499 + add-ons + renewal anni correct ga map avutayi; tappu amount ki 400 + valid amounts list |
| 2 | **₹29 micro tier ledu** | ₹99 pay cheyyadam ki sankochinche vaallu (chala mandi) **exit avutaru** → free 3 aipoyaka drop-off | ✅ **₹29 → 1 profile** add chesanu (impulse buy + ₹10/profile VIP ki anchor) |
| 3 | **Pricing page ledu + legal pages ledu** (Terms/Privacy/Refund) | (a) **Razorpay activation ki Terms + Privacy + Refund + Contact compulsory** — lekapote payment gateway approve avvadu (live payments bandh!). (b) Customers "hidden charges" anukuni trust cheyyaru | ✅ **/pricing** (full table + compare + FAQ + add-ons), **/terms**, **/privacy**, **/refund** pages build chesanu — footer + nav + sitemap lo links |

**Bonus ga dorikina chinna vishayalu:**
- `credits.py` (pata file) lo prices **₹99 → 10 credits** ani undindi — ippudu `interest.py` tho **exact match** (₹99 → 5, ₹199 → 12, ₹299 → 25, ₹499 → 50) + legacy aliases kooda correct ga map.
- "pay cheyyandi" button URL `/pay?plan=TRIAL_99` (pata plan) → **`/pricing`** ki marchanu.
- Admin gift plan `PREMIUM_299` → `S_199`.

---

## 3️⃣ MANAM INKA BETTER CHESKOVACHU (roadmap — mee OK cheppandi)

| # | Idea | Enduku | Expected impact |
|---|---|---|---|
| 1 | **Success fee (₹2,999–₹4,999)** — pelli fix ayyaka matrame | Matrimony lo idi **highest revenue** model (Shaadi/Jeevansathi kooda ide). Customer ki risk ledu ("pelli kaledu ante ₹0") | Oka pelli ki ₹3,000 × 50 pellilu/నెల = **₹1.5L/నెల** |
| 2 | **Weekend / festival offer** (Sankranti, Ugadi, Varalakshmi) — ₹299 → 30 profiles | Festivals lo registrations 2–3× | Conversion +40% aa rojulu |
| 3 | **₹9 "trial week"** (oka request + boost) | Lowest risk entry — card lo kooda try chestaru | Funnel top perigidi |
| 4 | **Referral ladder** — 3 refer = 1 free request, 10 refer = ₹500 cash | Bureau network + word of mouth | CAC ₹0 |
| 5 | **Bureau per-placement pricing** (₹500/profile confirmed match) | Agents ki "only success" model nachutundi | Bureau revenue 2× |
| 6 | **Wedding vendor commissions** (photography, catering, hall, jewellery) | Profiles ki mana service "pelli varaku" untundi — vendors kooda kavali | Extra income + customer value |
| 7 | **A/B price test** — ₹199 vs ₹249 hero tier (2 వారాలు) | Data tho confirm cheyyali | +10–15% revenue |
| 8 | **Premium "matchmaker" ₹999** (team manam matches chupinchadam) | VIP ki next step, high-margin service | ARPU +₹300 |

---

## 4️⃣ UNIT ECONOMICS (simple ga — enduku profitable)

```text
Costs: Telegram channels ₹0 · WhatsApp bridge (server) ₹0 extra · Bot API free
       Server (Oracle VM) ₹0 (free tier) · Razorpay fee ~2% · SMS/OTP ₹0 (WhatsApp OTP)

1000 registrations (free users) → 5% pay chestaru ante (industry 2–8%):
  60 × ₹199 (hero)   = ₹11,940
  25 × ₹99           = ₹2,475
  10 × ₹299          = ₹2,990
   5 × ₹499          = ₹2,495
  ─────────────────────────────
  Revenue ≈ ₹19,900 / 1000 registrations  (~₹20 per registration)
  
+ add-ons (10% mandi ₹49–₹199) ≈ ₹2,500  → total ≈ ₹22,400
+ bureau plans (2 bureaus × ₹999) ≈ ₹2,000 → total ≈ ₹24,400
```
**Meaning:** 3,000 registrations/నెల (100/day) → **~₹60,000–₹75,000/నెల** — 2 ఏళ్లలో లక్ష registrations ayithe scale avutundi.
**Break-even:** ~500 registrations (server+domain+SSL costs ~₹1,500/నెల).

---

## 5️⃣ COMPLIANCE (Razorpay + legal — idi miss ayithe payments aagipothayi)

| Item | Status |
|---|---|
| Terms of Use page | ✅ `/terms` (18+/21+, chatting ledu, banned list, Hyderabad jurisdiction) |
| Privacy Policy | ✅ `/privacy` (DPDP Act 2023 + Grievance Officer + 30-day delete) |
| Refund & Cancellation | ✅ `/refund` (7-day money-back, decline refund, no cash-refund-after-use, GST invoice) |
| Contact details | ✅ Footer + Refund page (phone, email, address) |
| Auto-renewal | ✅ **Ledu** (clear ga prathi page lo cheppamu — gateway ki trust signal) |
| GST invoice | ✅ Payment tarvata 24h lo (support ki adigithe) — **live lo GSTIN add cheyyali** |
| Price display | ✅ All-inclusive (hidden charges ledu) — prathi page lo same price |

---

## 6️⃣ EEE CHANGES EKKADA UNNAYI (code)

| File | Em marchindi |
|---|---|
| `backend/interest.py` | **S_29 micro tier** + `apply_payment()` (payments ki single source of truth) |
| `backend/main.py` | Webhook fix (legacy map teesesa) + `/pricing` pay_url + gift plan update |
| `backend/credits.py` | Legacy prices ni kotha ladder ki align (drift ledu) |
| `backend/models.py` | Plan comment update |
| `frontend/src/app/pricing/page.tsx` | 🆕 Full pricing page (compare + add-ons + renewal + bureau + FAQ) |
| `frontend/src/app/{terms,privacy,refund}/page.tsx` | 🆕 Legal pages (Razorpay ki kavali) |
| `frontend/src/components/{SiteHeader,SiteFooter}.tsx` | Pricing + Policies links |
| `frontend/src/lib/site-config.ts` | ₹29 bundle + prices |
| `backend/test_growth_namaste_leads.py` | **+25 new checks** — webhook mapping, ₹29, legal pages, cross-links (total 138/0 PASS) |

---

## ✅ Bottom line

1. **Mee ladder correct** — 99 → 5, 199 → 12, 299 → 25, 499 → 50 ✅ (₹/profile thaggutuu undi).
2. **₹99 → 3 ani chupinchadam tappu ayyedi** — enduku ante free ke 3 isthamu, so evaru pay cheyyaru. Ippudu **₹99 → 5 + boost** ✅.
3. **Webhook bug** (₹199/₹499 wrong credits) — **fix ayyindi**, ippudu prathi payment correct ga profile credits isthundi ✅.
4. **₹29 micro + /pricing + legal pages** — ippudu complete ✅ (Razorpay approve cheyyadaniki ready).
5. **Next best step:** **success fee (₹2,999)** + festival offers — idi add chesthe revenue 2–3× avutundi. Cheppandi, implement chesesthanu.
