# 🌟 WAVE 13 — FIRST-NAME + ASTRO + ADS (branch lone, merge cheyaledu)

> User demands: (1) first-name chupinchu + surname hide + same-surname backend block,
> (2) login eppudu undali + professional UI, (3) PEDDA astrology (dosham),
> (4) vendor ADS district/state target + days/media + revenue.

## ✅ 1. 👋 First-name display + surname guard
- Public anni chotla FIRST NAME: channel caption `👰 Lakshmi • 24y`, bot card, website cards.
- Surname + number eppudu hidden. Owner thana profile lo full name chusthadu.
- Backend same-surname auto-block (inti-peru okkate = pelli kudadhu):
  - interest/send → 400 `same_surname` (credit cut kadu)
  - top-matches + admin match-send → auto-skip + `surname_skipped` count (`?include_same_surname=1` tho chudochu)
  - match/score → `surname` verdict (gothram verdict tho paatu)
  - surname lekapothe (single-word peru) → block kadu + warning (gothram pattern)
- Demo seed grooms ki distinct inti-perlu (Verma/Nandan/Sharma) — patha tests green.

## ✅ 2. 🔐 Login persist + professional UI
- Token (30 days) + ID localStorage lone — refresh ayina login undi.
- Header lo session chip `👤 TSAP-… + logout` + `/api/auth/verify` auto-check prathi page load ki.
- Cards professional: first-name + badges + AdSlot (home hero + matches sidebar + mobile).

## ✅ 3. 🪐 PEDDA astrology system
- **36-guna Ashtakoota** (classical): Varna 1 · Vashya 2 · Tara 3 · Yoni 2 · Maitri 5 · Gana 6 · Bhakoot 7 · Nadi 8.
  - 27 nakshatras (gana/yoni/nadi tables) + 12 rasis (lord/varna/vashya) + spelling aliases (Aswini/Moola/Karkataka...).
  - Unknown star/rasi → honest "data ledu" (guess vaddu — mistakes vaddu).
  - Dosha detect: Nadi, Bhakoot (6-8/5-9/2-12), Yoni-vairam, Gana, Janma-tara, Graha-vairam.
- **Dosha screening** per profile: declared dosham (Kuja/Manglik), Moola/gandanta stars, kuja needs_chart.
- **Jathakam** upload (photo/PDF 8MB) → pandit queue → verify → 🪐 badge.
- Endpoints: `GET /api/astro/guna?bride_id=&groom_id=` (gender auto-swap), `GET /api/astro/dosha/{id}`,
  `POST /api/astro/jathakam/upload`, admin: `/api/admin/astro/queue|verify|stats`.
- Admin 🪐 tab: guna checker (8-koota breakdown card) + pandit queue + stats (dosha/moola/star).

## ✅ 4. 📢 Vendor ADS engine (revenue)
- Campaigns: title/offer + photo/banner + video + link + slots + scope + days.
- Scope: **district** (aa districts vallake) / **state** (TS/AP) / **all** — serve-time strict match.
- Pricing (public `/api/ads/rates` + quote): base ₹49/d + ₹19/district/d · state ₹299/d · all ₹499/d · video +₹30 · hero +₹99. Uda: 7d×2dist = ₹609.
- Flow: vendor create (pending) → UPI pay + UTR → admin approve → LIVE (start/end) → auto-expire.
- Serve rotation (least-impressions) + impressions/clicks/leads track.
- Slots: home_hero, matches_sidebar, profile_banner, search_top. Ad lekapothe house-promo (khaali vaddu).
- Pages: `/vendors/campaign` (quote + create + naa campaigns) · Admin 📢 tab (queue + pause/resume + revenue).
- Vendor auth: `X-Vendor-Token` (dev lo bypass, prod lo must).

## 🧪 Proof
- **Kotha `test_wave13_full.py`: 105/105** ✅ (surname/guna-known-answers/dosha/jathakam/ads-targeting/session)
- **Anni suites green** (~1400+ checks, 0 fail) ✅ · `npm run build` ✅
- Live: caption first-name + guna 24/36 + dosha clear + ads serve + surname-block — curl verify ✅

## 🔌 Kotha endpoints (13)
`GET /api/astro/guna` · `GET /api/astro/dosha/{id}` · `POST /api/astro/jathakam/upload` ·
`GET /api/admin/astro/queue` · `POST /api/admin/astro/verify/{jid}` · `GET /api/admin/astro/stats` ·
`GET /api/ads/rates` · `POST /api/ads/quote` · `GET /api/ads` · `POST /api/ads/{cid}/click` ·
`POST+GET /api/vendors/{vid}/campaigns` · `GET /api/admin/ads` · `POST /api/admin/ads/{cid}/approve|action` ·
`GET /api/admin/ads/stats`

## ⏳ Live ki (code ready)
Jathakam files: `/tmp/jathakam` (docker volume add). Ad images: URL-based (upload reuse optional).
Prod: vendor tokens + UPI verify + pandit login (admin key ne ippudu).

## 📁 Files
- NEW: `backend/astro.py`, `backend/ads.py`, `backend/test_wave13_full.py`,
  `frontend/src/lib/names.ts`, `components/AdSlot|AstroConsole|AdsConsole.tsx`, `app/vendors/campaign/page.tsx`
- EDIT: `smart12.py` (first-name + surname), `main.py` (guards + 13 routes + seeds),
  `telegram_bot.py` (first-name card), `test_wave12_smart.py` (display update),
  matches/ProfileView/header/home/admin UI
