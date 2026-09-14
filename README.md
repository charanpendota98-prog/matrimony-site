# 💍 Mana Vivaha (TSAP Matrimony)

**TS-AP No.1 Telugu Matrimony** — ₹99 ke Sambandham • Modati 3 FREE
Website: https://manavivaha.in • Bot: [@telugumatrimony1_bot](https://t.me/telugumatrimony1_bot)

Custom-built platform (Next.js 14 + FastAPI + Postgres + Redis + aiogram + Docker) —
**65 Telegram channels**, advanced 5-step register, full-detail profile card, Telegram + WhatsApp auto-post.

---

## ⚡ Quick start (local)

```bash
cp .env.example .env         # BOT_TOKEN, SITE_URL etc fill chey
export COMPOSE_HTTP_TIMEOUT=300
sudo -E docker-compose up -d --build postgres redis backend frontend bot

# Website   → http://localhost:3000
# API docs  → http://localhost:8000/docs
# Channels  → http://localhost:3000/channels
```

WhatsApp (optional, groups/community ki post):
```bash
docker-compose up -d whatsapp-bridge
# http://localhost:3001/qr → WhatsApp scan → .env: WHATSAPP_MODE=bridge
```

**Launch inventory (360 profiles + growth engine):**

```bash
cd backend
python seed_launch_db.py --count 360 --out launch_profiles.json     # generate
python seed_launch_db.py --count 360 --load http://localhost:8000   # API ki load
# .env: LAUNCH_SEED_COUNT=360 · ADMIN_WHATSAPP_NUMBER=91XXXXXXXXXX · LAUNCH_TARGET_PROFILES=360
# Dashboard: http://localhost:3000/growth   (visits → leads → profiles + anti-ban status)
```

## 🧪 Tests

```bash
python3 backend/
  wa_antiban.py           ← 🛡️ WhatsApp anti-ban engine (random 120–170s gap, caps, warmup, typing)
  interest.py             ← 💌 Interest/request engine (chatting LEDU) + credits + WhatsApp texts
  porutham.py             ← 🔮 10-porutham (kundli match) engine — Telugu verdict + dosha alerts
  test_interest_antiban.py← 83 tests (anti-ban + interest + porutham + views + add-ons)
  growth.py               ← 📈 Growth engine (namaste welcome, visitor/lead capture, share kit, inventory)
  test_growth_namaste_leads.py ← 109 tests (namaste + leads + share kit + launch inventory + anti-ban + 💰 pricing parity)
  topmatch.py             ← 🧠 Match Score 2.0 (11 weights, explainable breakdown, mutual +8% bonus, Telugu verdict)
  test_topmatch.py        ← 61 tests (weights, breakdown, mutual, top-matches, APIs, OG images)
  safety.py               ← 🛡️ Trust & Safety (report → auto-flag, block, verification levels, moderation queue, Telugu tips)
  preview.py              ← 🖼️ OG/social preview images (profile, porutham report, site) — WhatsApp reach booster
  test_safety_preview.py  ← 70 tests (reports, auto-hide, moderation, block, verify, tips, OG PNGs, APIs)
  seed_launch_db.py       ← 🚀 Launch inventory generator (360 realistic profiles: caste/star/district correct)
  test_channels_router.py     # 57/57 — registry + router
python3 backend/publisher.py                # dry-run post preview
cd frontend && npm run build                # 12/12 pages
```

## 📂 Structure

```
backend/
  channels_config.py      ← 65-channel registry + auto-router (SINGLE SOURCE OF TRUTH)
  create_channels.py      ← creation CLI (--wave / --key / --check / --mark-live)
  publisher.py            ← Telegram + WhatsApp auto-publisher (retry, queue, dry-run)
  card_pro.py             ← full-detail neat profile card (Pillow + QR + watermark)
  main.py                 ← FastAPI (register, search, matches, credits, channels, publish, otp, leads, growth)
  growth.py               ← 📈 Namaste welcome + visitor/lead capture + share kit + inventory gauge
  topmatch.py / safety.py / preview.py  ← 🧠 Match Score 2.0 • 🛡️ reports/block/verify • 🖼️ OG preview images
  telegram_bot.py         ← aiogram bot (approve → auto-post → deep links)
  gen_frontend_channels.py / gen_master_list.py   ← registry → frontend + docs (auto-gen)
frontend/
  src/lib/site-config.ts  ← ⭐ CUSTOMIZE IKKADE (brand, prices, features, contacts)
  src/components/         ← SiteHeader, SiteFooter, StickyCTA, Reveal, SectionHeading
  src/app/                ← home, register (smart wizard), channels, matches (score v2 panel), requests 💌, porutham 💍, safety 🛡️, castes (SEO), referral, bureau, admin, growth 📈, offline
  public/manifest.webmanifest + sw.js + icons/  ← 📲 PWA (installable, offline shell)
  src/lib/seo-pages.ts    ← 🔎 289 programmatic SEO pages (caste × role × district)
whatsapp-bridge/          ← optional Baileys service (groups/newsletter posting)
docker-compose.yml        ← postgres, redis, backend, frontend, bot, wa-bridge (+nginx profile)
nginx.conf                ← host nginx config (manavivaha.in, /api proxy, SSL via certbot)
```

## 📚 Docs
| Doc | Enti |
|---|---|
| [CHANNELS-MASTER-LIST-TELUGU.md](CHANNELS-MASTER-LIST-TELUGU.md) | 65 channels final list + waves + bot router rules |
| [WEBSITE-STRATEGY-AND-100-PERCENT-GAPS.md](WEBSITE-STRATEGY-AND-100-PERCENT-GAPS.md) | Custom vs WordPress + auto-post flow + 30 gaps (P0→P3) |
| [WEBSITE-CUSTOMIZATION-GUIDE.md](WEBSITE-CUSTOMIZATION-GUIDE.md) | Enti ekkada marchali — brand/pricing/features/colors + verify steps |
| [WHATSAPP-ANTIBAN-AND-REQUESTS.md](WHATSAPP-ANTIBAN-AND-REQUESTS.md) | 🛡️ Anti-ban playbook (120–170s random gap, caps, warmup, recovery) + 💌 requests model + APIs |
| [WAVE5-MATCH-SCORE-TRUST-PWA.md](WAVE5-MATCH-SCORE-TRUST-PWA.md) | 🧠 Match Score 2.0 (11 weights, explainable, mutual) • 🛡️ Trust & Safety (report/block/verify/moderation) • 💍 porutham report • 🖼️ OG preview images • 📲 PWA |
| [PLAN-ADVANCED-STRATEGY.md](PLAN-ADVANCED-STRATEGY.md) | 👑 Pricing ladder (₹99→5, ₹199→12, ₹299→25, ₹499→50 VIP), revenue math, 30-day plan, strategies, KPIs |
| [GROWTH-NAMASTE-LEADS-INVENTORY.md](GROWTH-NAMASTE-LEADS-INVENTORY.md) | 📈 Namaste welcome automation • lead capture funnel • 360-profile launch inventory • community networks playbook • pricing audit + parity guard |
| [ULTIMATE-TSAP-MASTER-PLAN-TELUGU.md](ULTIMATE-TSAP-MASTER-PLAN-TELUGU.md) | Master business plan |
| [REFERRAL-SHORT-CODE-BUREAU-OFFER.md](REFERRAL-SHORT-CODE-BUREAU-OFFER.md) | Referral ₹50 + bureau B2B |

## 🔑 API (main)
```
POST /api/register              → ID + card + top-3 matches + auto-post queue
GET  /api/channels              → 65 channels (tiers, live/pending, join + deep links)
POST /api/channels/route        → profile → ee channels ki post avutundi (preview)
POST /api/publish/preview       → caption + WhatsApp text + targets (post cheyyakunda)
GET  /api/publish/status        → Telegram/WhatsApp readiness + dry-run
GET  /api/publish/log           → publish audit log
POST /api/publish/now/{id}      → manual re-post (admin)
GET  /api/search/{id}           → ID search (always open)
POST /api/otp/send|verify       → phone verification (10 min, max 5 tries)
POST /api/photo/upload          → photo upload (real file, 5MB cap, phone lo compress)
GET  /api/search                → advanced filters (gender/caste/district/age/salary/porutham sort)
POST /api/interest/send         → 💌 request (1 credit → mana WhatsApp nunchi profile share)
GET  /api/interest/inbox|sent   → request dashboard (accept/decline)
POST /api/interest/respond      → accept (numbers exchange) / decline (credit refund)
GET  /api/porutham              → 10-porutham kundli match (Telugu verdict)
GET  /api/match/score?a=&b=     → 🧠 Match Score 2.0 (11 components breakdown + mutual + Telugu verdict)
GET  /api/top-matches/{id}      → top matches (mutual bonus tho ranked)
POST /api/report · GET /api/moderation/queue · POST /api/moderation/resolve/{id}  → 🛡️ trust & safety
POST /api/block · /api/unblock · GET /api/blocks/{id}                          → 🚫 block list
POST /api/verify/request · GET /api/verification/{id}                          → ✅ phone/photo/ID badge
GET  /api/og/profile/{id}.png · /api/og/porutham/{b}/{g}.png · /api/og/site.png → 🖼️ WhatsApp preview images
GET  /api/safety/tips           → 6 Telugu safety tips + categories + verify levels
POST /api/view · GET /api/views/{id}    → who-viewed-me (₹49 unlock)
POST /api/save · GET /api/saved/{id}    → shortlist ❤️
GET  /api/share/kit/{id}        → card + caption + hashtags (reach engine)
POST /api/track                 → visitor beacon (whole-site tracking)
POST /api/leads/quick           → 📱 phone-first lead (30-sec entry) + WhatsApp follow-up
GET  /api/leads · /api/leads/stats      → lead queue + traffic/conversion dashboard
POST /api/leads/followup/{id}   → follow-up WhatsApp pampu
GET  /api/inventory             → 300–400 profiles launch gauge
POST /api/admin/bulk-profiles   → launch inventory load ({generate: 360})
GET  /api/digest/preview        → daily digest text (9 AM post ki)
GET  /api/wa/status|pause|resume|reset_day → 🛡️ anti-ban control
```

## ⚠️ Safety
- `BOT_TOKEN` chala sari chat lo share ayyindi → **BotFather lo /revoke chesi** new token `.env` lo pettu (git lo commit cheyyaku — `.gitignore` lo undi).
- Number pay tarvata matrame chupinchali; photo-private → blur; card ki watermark + QR.
- WhatsApp: spam cheyyaku (roju 5–10 posts/group) — ban risk. Opt-in matrame.
