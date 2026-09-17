# 🌊 WAVE 14 — PERFECT MATCH + ADMIN SUPREME (Telugu Summary)

> Branch: `arena/01a0aaf1-matrimony-site` • NO merge • Tests: **106/106** • Regression: **911/911** (W9–W14 + topmatch + safety + vendors)

## 1. 🎂 AGE RULE (Sampradayam — DOB-date accurate)
- Ammayi (bride) abbayi (groom) kanna **1 roju peddadi ayina → SKIP** — suggest cheyyamu, interest kooda block.
- **Same-date puttina → OK** 🎉 • **0–12 months younger brides FIRST** (priority tier).
- DOB lekapothe age-years fallback (equal allow, pedda block) • rendu lekapothe block kadu (honest unknown, rank thakkuva).
- Ekkada: `interest/send` block + `top-matches`/`match-send` auto-filter (`?include_age_block=1` tho chudochu) + `match/score` verdict.

## 2. 💼 PROFESSION AFFINITY (vala rangam vallake)
- Doctor→Doctor 🩺 • Software→Software 💻 • Govt→Govt 🏛️ • Teacher/Engineer/Police/Business/Accounts/Farmer/Private.
- **Score math marchaledu** — rank layer matrame (same-group block first, group lopala score order).
- Ekkada: `top-matches` + admin `match-send` (auto) + `/api/search?profession_first=true` (opt-in toggle "💼 Naa profession first").

## 3. ✈️ NRI (TS/AP abroad — separate)
- Register lo **Country** field (India/USA/UK/UAE…) — India kakapothe **NRI flag auto** (+ work_location/city keywords fallback).
- **✈️ NRI badge** (matches cards + profile page + country peru) • `?nri_only=1` filters (search + top-matches + admin match-send).
- NRI members: home-state channel **+ NRI Global Hub** ki kooda auto-post.

## 4. 🪔 RELIGION → CASTE (A–Z)
- Religion select → aa religion castes/groups **A–Z order**: Hindu **43** • Muslim 13 • Christian 10 • Sikh/Jain/Other.
- Register Step-2 caste list ippudu **backend nunchi dynamic** (`/api/meta/castes?religion=`) + count hint.

## 5. 💳 SAFE-PAY (Razorpay — mistakes vaddu)
- **Amount SERVER computes** (client amount nammamu) • **Signature HMAC verify → SUCCESS ayithe MATRAMe fulfill**.
- **Idempotent**: double-click/replay → okka sari matrame credit (receipt reuse) • **Secret eppudu expose kadu** (key_id matrame public).
- Keys lekapothe **manual-UPI mode** (honest): UPI ID + amount → admin UTR confirm → fulfill.
- Purposes: **credits** (S_29–S_499) • **assisted** (₹500 order) • **ads** (campaign live) • **boost** (B_1/3/7).
- Pricing page lo **PayBox** (offer code → order → Razorpay checkout.js / UPI) • verify fail aithe support msg (auto-refund note).

## 6. 🎉 FESTIVAL OFFERS (ADMIN only)
- Presets 1-click: **DIWALI25** (25%) • **SANKRANTI20** • **UGADI15** • **FIRST50** (₹50 flat, ₹199+) + custom create (%/flat, dates, applies_to, min, max-uses).
- **ON/OFF toggle** • dates/caps **server enforce** • homepage + pricing **auto-banner** 🪔.

## 7. 🔐 ADMIN SUPREME (anni admin lone)
- **💳 Payments tab**: orders + collected stats + pending UTR confirm→fulfill (double-credit impossible).
- **🎉 Offers tab**: seed + create + ON/OFF + used/max counts.
- **📢 Ads tab**: campaign **✏️ Edit** (title/offer/days/districts/state/slots/dates/link) — active extend aithe end auto-recompute.
- Bot **`/matches`**: personal top-3 Telugu text (age-rule + profession-first, numbers masked) — `GET /api/bot/matches?tsap_id=`.

## API cheatsheet
| Endpoint | Em chesthundi |
|---|---|
| `GET /api/meta/castes?religion=` | A–Z castes |
| `GET /api/pay/config` | mode + key_id + plans + offers (secret ledu) |
| `POST /api/pay/order` | server-amount order (+offer) |
| `POST /api/pay/verify` | HMAC → fulfill once |
| `GET /api/admin/payments` + `POST .../confirm` | UTR confirm → fulfill |
| `POST /api/admin/offers/seed` + CRUD + `toggle` | festival offers |
| `POST /api/admin/ads/{cid}/update` | dates/districts/days edit |
| `GET /api/bot/matches?tsap_id=` | top-3 text |

## Live proof (2026-09-16)
- `🚫 Ammayi abbayi kanna 1 roju peddadi — sampradayam prakaram suggest cheyyamu 🙏` (gap −1)
- Doctors (80/79) score-83 software paina — profession-first ✅
- NRI profile: `True USA` + badge ✅ • DIWALI25: ₹99→₹75 + UTR receipt ✅ • Bot top-3 (10 age-skips) ✅
