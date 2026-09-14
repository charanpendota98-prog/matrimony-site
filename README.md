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

## 🧪 Tests

```bash
python3 backend/
  wa_antiban.py           ← 🛡️ WhatsApp anti-ban engine (random 120–170s gap, caps, warmup, typing)
  interest.py             ← 💌 Interest/request engine (chatting LEDU) + credits + WhatsApp texts
  test_interest_antiban.py← 54 tests (anti-ban + interest flow)test_channels_router.py     # 57/57 — registry + router
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
  main.py                 ← FastAPI (register, search, matches, credits, channels, publish)
  telegram_bot.py         ← aiogram bot (approve → auto-post → deep links)
  gen_frontend_channels.py / gen_master_list.py   ← registry → frontend + docs (auto-gen)
frontend/
  src/lib/site-config.ts  ← ⭐ CUSTOMIZE IKKADE (brand, prices, features, contacts)
  src/components/         ← SiteHeader, SiteFooter, StickyCTA, Reveal, SectionHeading
  src/app/                ← home, register (55 fields), channels, matches, referral, bureau, admin
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
| [PLAN-ADVANCED-STRATEGY.md](PLAN-ADVANCED-STRATEGY.md) | 👑 Pricing ladder (₹99→3, ₹199→10, ₹299→20), revenue math, 30-day plan, 15 advanced strategies, KPIs |
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
```

## ⚠️ Safety
- `BOT_TOKEN` chala sari chat lo share ayyindi → **BotFather lo /revoke chesi** new token `.env` lo pettu (git lo commit cheyyaku — `.gitignore` lo undi).
- Number pay tarvata matrame chupinchali; photo-private → blur; card ki watermark + QR.
- WhatsApp: spam cheyyaku (roju 5–10 posts/group) — ban risk. Opt-in matrame.
