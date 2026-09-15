# 🧠 WAVE 5 — Match Score 2.0 • Trust & Safety • Porutham Report • PWA • OG Previews

**Status:** shipped (backend + frontend + tests) • `main` branch
**Goal:** top-matrimony sites (Shaadi/Bharat/Jeevansathi) kanna **better** — explainable scoring,
real safety layer, Telugu-first porutham report, installable app, WhatsApp-ready preview images.

---

## 1) 🧠 Match Score 2.0 (`backend/topmatch.py`)

Mundu unna v1 score "black box" (95/100 ani cheptham, enduku ani cheppaledu).
Ippudu **11 components + Telugu explanation + mutual (iddariki nachadam)**.

| Component | Weight | Enti chusthundi |
|---|---|---|
| Age match | 13 | Age gap + `exp_age_min/max` (register lo ichina partner preference) |
| Caste / community | 13 | Same caste → full points; different caste → honest note |
| Location | 12 | Same district > same state > different state (+ work location) |
| Education | 9 | Tier match (high/mid) + preference |
| Job / profession | 10 | Stable/premium profession + `exp_job` preference |
| Income | 8 | Salary band comparison (L/k → rupees parse) |
| Height | 5 | Groom > bride traditional check (flexible) |
| 10-Porutham | 10 | `porutham.py` engine (stars iddariki unte) — lekapote neutral |
| Family background | 8 | Family type/status/values |
| Lifestyle | 7 | Diet / habits / marital status |
| Verification / trust | 5 | Phone ✅ → photo ✅ → ID 🏅 (trust badge) |

**Features:**
- **Grade + Telugu verdict:** ≥85 అద్భుతం • ≥75 చాలా మంచిది • ≥65 మంచిది • ≥50 సాధారణం • తక్కువ
- **Breakdown rows:** prathi component ki `points / max + ratio + Telugu note` (UI lo bars ga chupistham)
- **Mutual bonus (+8%):** rendu sides score ≥65 → bonus + "💞 mutual match" note (iddariki nachindi ante)
- **Strengths / weak_points / how_to_improve** — user ki em improve cheyyalo cheptham (profile completion → score ↑)
- **find_top_matches_v2(user, profiles, limit, min_score)** — opposite gender + approved only + mutual ranking

**APIs:**
```
GET  /api/match/score?a=TSAP-M-..&b=TSAP-F-..   → score, grade, breakdown[11], mutual, Telugu verdict
POST /api/match/score                            → raw dicts tho (frontend preview/admin tools)
GET  /api/top-matches/{tsap_id}?limit=10&min_score=65 → ranked list + mutual_matches count
GET  /api/search?viewer_id=TSAP-..               → prathi row lo `score`, `match_v2`, `verification`
```

**UI:** `/matches` → prathi card lo **"🧠 Enduku ee score?"** expandable panel (bars, weak points,
"score penchadaniki" tips, 💞 mutual badge) + `🛡️ verification` chip + `🚩` report shortcut.

---

## 2) 🛡️ Trust & Safety (`backend/safety.py` + `/safety` page)

| Feature | Detail |
|---|---|
| 🚩 Report | 7 categories (నకిలీ ప్రొఫైల్, ముందు డబ్బు, వేధింపు, ఫోటో మార్పు, పెళ్లి అయ్యింది, స్పామ్, ఇతర) • severity high/medium/low • **duplicate reports update** (repeat_count) • reporter anonymity |
| 🚨 Auto-flag | 2+ high severity **or** 3 different reporters **or** 4+ open reports → profile **auto-hide** (`is_approved=False` + reason) — admin chudakamunde |
| 🚫 Block | 2 directions (block chesina vaallu meeku kanipinchadu, meeru vaallaki kanipinchadu) • search lo hide • interest send ki 400 • block list manage |
| ✅ Verification | phone (OTP) → photo (📸) → **ID (🏅 full trust badge)** • trust score 40/65/85/100 • level eppudu downgrade avvadu • profile + search lo badge |
| 👮 Moderation queue | Severity priority order • target profile info + verification • **suggested action** (ban/hide/warn) • actions: verify / warn / hide / ban / dismiss • audit (admin_note + timestamps) • same-target reports bulk close |
| 💡 Safety tips | 6 Telugu tips (advance money = 100% scam, video call verify, public kalthi, OTP ivvakandi, certificates, "chatting ledu") |
| 🔗 Interest respect | blocked/banned profile ki interest pampaleeru (400 + Telugu reason) |

**APIs:**
```
GET  /api/safety/tips                → tips + categories + verify levels (Telugu)
POST /api/report                     → report (auto-flag rules apply) + ack Telugu
GET  /api/moderation/queue           → admin queue (severity sorted + suggested action)
POST /api/moderation/resolve/{id}    → verify | warn | hide | ban | dismiss (+ audit)
POST /api/block · /api/unblock · GET /api/blocks/{id}
POST /api/verify/request             → phone/photo/id level penchadam
GET  /api/verification/{id}          → badge (level, Telugu text, trust score, next step)
```

**Pages:** `/safety` (report form + block list + verification + moderation preview + tips),
`/matches` card lo 🚩 shortcut, footer lo "Trust & Safety Center".

---

## 3) 💍 Porutham Full Report (`/porutham`)

- **10 porutham lu okate page lo:** Rasi • Nakshatra • Gana • Yoni • Rajju • Vedha • Mahendra • Stree Deergha • Vashya • Rasi Adhipathi — prathi daaniki ✓/✗ + Telugu note
- **Score /10 + stars + Telugu verdict** + Rajju/Vedha **dosha alert** (purohitulu/pedda vaallatho matladandi)
- **Star tho calculate** (register avvakunda) or **TSAP IDs tho** (profiles nunchi)
- **🖨️ Print / PDF** (purohitulu ki chupinchadaniki) + WhatsApp share + **report image** (Pillow)
- **110 glossary:** prathi porutham enduku chustaru (Telugu lo) + 🎁 detailed report add-on ₹49

**API:** `GET /api/porutham?bride=..&groom=..` • `POST /api/porutham` (star/rasi direct)

---

## 4) 🖼️ Social Preview / OG Images (`backend/preview.py`)

WhatsApp/Telegram lo link pampinappudu **photo preview** → click rate 2–3x (matrimony lo idi reach booster).

```
GET /api/og/profile/{tsap_id}.png              → 1200x630 profile preview (name, ID, age, caste, edu, job, district, star, VERIFIED badge)
GET /api/og/porutham/{bride}/{groom}.png       → porutham report image (score circle + 10 items + verdict + dosha)
GET /api/og/site.png?title=..&subtitle=..      → site/caste/SEO page preview
```
Files `PREVIEW_DIR` (default `/tmp/previews`) lo cache → `Cache-Control: public, max-age=3600`.

**Per-profile SEO/OG (server-side):** `/search/[id]` ippudu **server component wrapper**
(`page.tsx` → `ProfileView.tsx`):
- `generateMetadata` → per-profile **title** (`Lakshmi Reddy (TSAP-F-2025-1042) — 24 yrs • Reddy • BTech • …`), description, canonical, `og:type=profile`, `twitter:summary_large_image`, `og:image=/api/og/profile/{id}.png`
- **JSON-LD `Person`** schema (Google lo profile rich results)
- **Host-aware absolute URLs** (`headers()` → staging/preview/prod lo kooda OG pani chestundi; `SITE_URL` set unte adi vaduthundi)
- Profile dorakapoyina page 200 + fallback metadata (SEO safe)

---

## 5) 📲 PWA (installable app)

- `public/manifest.webmanifest` — name/short_name, `start_url=/?utm_source=pwa`, theme `#7A0C2E`,
  background `#FFF8E7`, 3 icons (192/512/maskable), **4 shortcuts** (Matches, Porutham, Requests, Register)
- `public/sw.js` (**mv-v5-2026-09**) — app-shell cache; **`/api/*`, `/cards/*`, `/photos/*` NEVER cache**
  (privacy + fresh data); static assets cache-first; pages network-first; offline aithe `/offline`
- Icons: `public/icons/icon-192 · icon-512 · icon-maskable-512 · apple-touch-icon` (maroon + gold "MV" monogram)
- `components/PWA.tsx` — SW register + **"📲 Install cheyyandi"** card (`beforeinstallprompt`, `tsap_pwa_dismissed` remember)
- `/offline` page — offline lo kooda matches/porutham/safety links
- `layout.tsx` — manifest + icons + `appleWebApp` metadata

---

## 6) ✅ Verification (anni run chesi proof)

```bash
cd backend
WA_TEST_FAST=1 /tmp/venv/bin/python test_topmatch.py         # 61 pass / 0 fail
WA_TEST_FAST=1 /tmp/venv/bin/python test_safety_preview.py   # 70 pass / 0 fail
WA_TEST_FAST=1 /tmp/venv/bin/python test_growth_namaste_leads.py  # 109 / 0
WA_TEST_FAST=1 /tmp/venv/bin/python test_interest_antiban.py      # 83 / 0
WA_TEST_FAST=1 /tmp/venv/bin/python test_channels_router.py       # 57 / 0
```

**E2E (browser path, `:3000` website proxy → `:8000` API):**
- `/tmp/verify_wave5.py` → **46/46** (match score, top-matches, safety report→queue→resolve, block→search hide→interest 400, verify badge, OG PNGs, per-profile metadata, PWA assets, pages)
- `/tmp/verify_flow.py` → **31/31** (register → namaste → leads → interest → accept → refund → anti-ban → pricing)
- Routes sweep: **17/17** = `/`, `/register`, `/matches`, `/requests`, `/safety`, `/porutham`, `/offline`,
  `/growth`, `/castes/reddy-bride-hyderabad`, `/channels`, `/search/TSAP-F-2025-1042`, `/search/TSAP-M-2025-1042`,
  `/sitemap.xml`, `/manifest.webmanifest`, `/sw.js`, `/icons/icon-192.png`, `/api/og/site.png`

**Server lo restart tarvata:**
```bash
pkill -9 -f "next-server"; cd frontend && npm run build && BACKEND_URL=http://localhost:8000 npx next start -H 0.0.0.0 -p 3000
```
(Git lo build output ledu — `.next` sandbox snapshot nunchi teesestham.)

---

## 7) ⚙️ Ops notes / gaps

- **Telugu font server lo ledu** → OG **images** lo English text (site pages lo Telugu 100% perfect).
  Image lo Telugu kavali ante: `apt-get install -y fonts-noto-telugu` (appudu `preview.py` Telugu lines kooda render avutayi).
- `SITE_URL` production lo `https://manavivaha.in` set cheyyandi (canonical/OG ki); lekapote request host vaduthundi.
- Report/block/verification data ippudu **in-memory** (demo). Postgres wiring (`reports`, `blocks`, `verification`)
  next step — API shapes same untaayi, frontend marchanavasaram ledu.
- Moderation queue admin auth kavali production lo (`/growth`/`/admin` ki password + rate limit).
