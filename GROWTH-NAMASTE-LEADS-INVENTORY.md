# 📈 MANA VIVAHA — GROWTH ENGINE (Namaste Welcome • Leads • Launch Inventory • Community Networks)

> Mee maata ki 1:1 — **"mana site ki vachina vallu, chusina vallu antha database lo save avvali"**,
> **"register avvagane manam namaste msg pettali (card + details tho)"**,
> **"300–400 profiles unte chalu — chala mandi avasaram ledu"**, **"community networks vastayi"**.

Ee document lo aa 4 requirements ki **code + strategy + numbers** unnayi. Anni already implement ayyayi
(`backend/growth.py`, `backend/seed_launch_db.py`, `main.py` endpoints, `/growth` dashboard) — 109 automated
checks tho verify ayyayi (`backend/test_growth_namaste_leads.py`).

---

## 1) 🙏 NAMASTE WELCOME AUTOMATION (register avvagane)

**Flow (register button nokkagane, automatic):**

```
User register complete
   │
   ├─ 1. Profile + card generate (Pillow)                          → /cards/TSAP-....png
   ├─ 2. Telegram channels ki post (65-channel network)             → @TSBRIDE / @TSGROOM1 / caste channels
   ├─ 3. WhatsApp queue: mana side nunchi NAMASTE msg + card image  → anti-ban gap (120–170s random)
   ├─ 4. Admin/matcher ki "NEW REGISTRATION" alert                  → ADMIN_WHATSAPP_NUMBER
   ├─ 5. Top 3 FREE matches (score + reasons)                       → register response lo
   └─ 6. Lead "converted" ga mark                                   → /growth dashboard lo kanipisthundi
```

**Namaste message lo em untundi (Telugu):** peru + garu, profile ID, caste/gothram/star/rasi, height,
education, job, salary, district, family type, "65 channels lo post ayyindi", **3 next steps**,
"number evariki kanipinchadu", "🚫 Chatting ledu", support number, bot handle.

**Enduku idi strong:** user ki "naa profile vellinda?" ani doubt undadu → trust perugutundi → share chestadu
(status lo pettadaniki ready caption + card kindha ne pampistham). Idi **retention + referral engine**.

Endpoints/env:

| Env | Default | Endi chestundi |
|---|---|---|
| `ADMIN_WHATSAPP_NUMBER` | *(khali)* | kotha registration alert + matcher follow-up ki |
| `SUPPORT_PHONE` | `9100000000` | profiles lo trust line + scam report |
| `WHATSAPP_MODE` | `off` | `bridge` (Baileys) leda `cloud_api` chesi pettandi — appude automatic ga veltundi |

`WA_MODE=off` lo kooda nasta ledu: register response lo `welcome_status.manual_text` vasthundi —
support team copy chesi pampochu (register success screen lo "📋 Namaste message copy" button undi).

---

## 2) 📊 LEAD CAPTURE — "chusina vallu antha DB lo save"

**3 layers (evvaru miss avvaru):**

| Layer | Em capture avutundi | Ekkada |
|---|---|---|
| **1. Server middleware** | prathi GET (path, referrer, device, channel: whatsapp/telegram/google/fb/insta/youtube/direct) | `DB_VISITORS` |
| **2. Frontend beacon** | screen size, lang, time-on-page, utm, visitor_id | `POST /api/track` |
| **3. QuickLead form (30 sec)** | **number** + name + gender + district | `POST /api/leads/quick` → `DB_LEADS` |

**Funnel:** `visit → profile chudu → number isthe lead → register aithe converted`

**Why "phone-first" works for masses:** 55-field form ani bhaya padakunda, "number pettu — mana team call chesi
profile FREE ga complete chestundi" ani 30 seconds lo entry. Number isthe ventane **WhatsApp follow-up**
(anti-ban fast lane 60–120s) pothundi + register link (`/register?phone=…`) tho profile complete avutundi.

**Endpoints:**

| Method | Endpoint | Pani |
|---|---|---|
| POST | `/api/track` | visit beacon (client info enrich) |
| POST | `/api/leads/quick` | phone-first lead + auto WhatsApp follow-up |
| GET | `/api/leads` | leads list (follow-up queue) |
| GET | `/api/leads/stats` | visits, unique, channels, top pages, lead sources, conversion %, inventory |
| POST | `/api/leads/followup/{lead_id}` | malli follow-up pampu (status → `contacted`) |
| POST | `/api/interest/send` | 1 credit → target ki mana WhatsApp nunchi profile share |
| POST | `/api/view`, GET `/api/views/{id}` | who-viewed-me (paid unlock ₹49) |
| POST | `/api/save`, GET `/api/saved/{id}` | shortlist ❤️ (free — engagement loop) |
| GET | `/api/porutham` | 10-porutham kundli match (Telugu verdict) |
| GET | `/api/share/kit/{id}` | card + caption + hashtags + WA/TG links + best time to post |
| GET | `/api/inventory` | 300–400 profiles gauge + ela fill cheyyalo |
| GET | `/api/plans` | pricing ladder + add-ons + renewal |
| POST | `/api/admin/bulk-profiles` | launch inventory load (`{generate: 360}` leda profiles list) |
| POST | `/api/admin/seed-launch` | demo inventory shortcut (dev) |

**Ops dashboard: `/growth`** — visits today, unique, leads, conversion %, inventory gauge, channel bars,
top pages, lead table (WhatsApp follow-up button), anti-ban status + pause/resume/reset.

---

## 3) 🚀 LAUNCH INVENTORY — "300–400 profiles chalu"

`backend/seed_launch_db.py` → **realistic Telugu profiles** (caste-faithful surnames, district-wise mandals,
star ↔ rasi correct, DOB ↔ age match, salary ↔ job coherence):

```bash
# Local / VM lo 360 profiles generate + JSON dump
python backend/seed_launch_db.py --count 360 --out launch_profiles.json

# Running backend ki direct load (API)
python backend/seed_launch_db.py --count 360 --load http://localhost:8000
# leda
curl -X POST localhost:8000/api/admin/bulk-profiles -H 'Content-Type: application/json' -d '{"generate":360}'
```

* Default startup: `LAUNCH_SEED_COUNT=60` (dev/preview ki — site khali ga kanipinchadu).
* **Oracle VM lo:** `.env` → `LAUNCH_SEED_COUNT=360` + `LAUNCH_TARGET_PROFILES=360`.
* Production lo real users vachaka `LAUNCH_SEED_COUNT=0` pettandi (demo profiles clean).

Quality checks (automated): 43 castes cover, 49 districts cover, TS+AP mix, unique TSAP IDs + phones,
27 nakshatras valid, bride 22–30 / groom 26–36 age bands, `about_myself` + `expectations` filled.

---

## 4) 🤝 COMMUNITY NETWORKS PLAYBOOK (360 profiles ela fill cheyyali — 30 rojulu)

**Target: 360 profiles = 180 brides + 180 grooms** (caste-proportional). Idi "chala mandi" kanna better —
**quality + caste coverage** unnayi kabatti matches dorukutayi.

| Vaaram | Community / channel | Ela approach cheyyali | Target |
|---|---|---|---|
| W1 | **Caste association heads** (Reddy/Kamma/Kapu/Vysya/Mala/Madiga/Lambada sanghams) | Vyaktiga kalisi — "mee caste channel free, profiles free ga register cheyistham" | 60 |
| W2 | **WhatsApp group admins** (district × caste groups) | Group ki mana channel link + "news kaadu, sambandham" message; admin ki ₹50/referral | 80 |
| W3 | **Bureau / broker network** (pelli brokers, photo studios, tailors, gold shops) | Bureau ₹999/mo → 25 profiles + dashboard; commission model | 80 |
| W4 | **Women self-help groups (SHG) / Anganwadi / teachers** | Oorlo trust undi — free registration camp (phone tho 3 nimushalu) | 60 |
| W4+ | **Students / influencers / YouTubers (Telugu)** | Reels: "chatting ledu, direct WhatsApp" USP + referral ₹50 | 60 |
| Continuous | **Lead follow-up** (already captured!) | ప్రతి lead ki call + WhatsApp follow-up → 40%+ profile conversion | ∞ |

**Community head incentives (motivation):** unique referral code (`?ref=NAME`), ₹50 per paid user,
free VIP plan (₹499) chesthe chaalu, "Mana Vivaha Community Partner" badge + village/district leaderboard
(`/referral` page lo leaderboard already undi), monthly payout UPI tho (min ₹150).

**KPI (ee 30 rojulalo):**
* 360 profiles • 43 castes × 24 districts cover
* 5,000+ visits • 300+ leads • 40% lead → profile conversion
* 60+ paid users (₹99 nunchi) • avg 2 add-ons/user (boost + verify)

---

## 5) 💰 PRICING — mee numbers lo unna 2 problems + final fix

**Mee numbers:** FREE 3 → ₹99 = 3 → ₹199 = 10 → ₹299 = 20
**Problem 1 (pedda problem):** **₹99 = 3 profiles kani FREE kooda 3 istham** → first paid step ki *reason ledu*
→ evaru ₹99 kooda pay cheyyaru. Idi conversion killer.
**Problem 2:** ₹299 = ₹15/profile kani ₹199 = ₹19.9/profile — ladder clear ga ledu (pedda tier lo thaggali).

**Final ladder (₹/profile prati tier lo thaggutundi):**

| Tier | Price | Profiles | ₹/profile | Story |
|---|---|---|---|---|
| Free Start | ₹0 | 3 | — | Funnel: register → 3 requests FREE |
| **Sambandham** | **₹99** | **5** | ₹19.8 | "Okka coffee price" impulse buy (fix #1) |
| **Family** *(most popular)* | **₹199** | **12** | ₹16.6 | Family involvement + verify badge + 1 porutham |
| **Premium** *(best value)* | **₹299** | **25** | ₹12.0 | 30-day boost + who-viewed 60d |
| **Vivaha VIP** | **₹499** | **50** | ₹10.0 | Matchmaker assist (mana team call) |
| Bureau | ₹999/₹2999 | 25 / 100 | ₹40 / ₹30 | B2B (brokers, agents) |

**Add-ons (ARPU wedge):** ⚡ Boost ₹49 • 👀 Who-viewed ₹49 • 🔮 10-Porutham ₹99 • ✅ Photo-verify ₹199
**Renewal:** ₹99 → **8 profiles** (loyalty = repeat revenue)
**Mee original amounts as-it-is** — only value ni correct chesam. Marchali ante **1 file**: `backend/interest.py` → `PLANS`
(frontend `requests/page.tsx` fallback + `PLANS` homepage kooda update cheyyali).

**Guard (ee sari kotha addition):** automated **pricing parity test** — API (`/api/plans`) ↔ UI (requests page) ↔
homepage ↔ strategy doc anni okate ladder chupinchali. Ee sari website lo **stale `₹99 → 3` text** dorkindi
(backend ₹99→5 chesaka UI lo 3 undipoyindi) — adi fix chesi, test tho lock chesam. (Customer ki rendu rakalu
kanipiste trust poye danger undi — ippudu CI lo pattukuntundi.)

**Revenue math (360 profiles, conservative):**
`360 profiles → ~90 paid users (25%) → avg ₹180 (mix of ₹99/₹199 + 30% add-on) → ₹16,200/month`
`+ Bureau 3 × ₹999 = ₹2,997` `+ renewals 20 × ₹99 = ₹1,980` → **≈ ₹21,000/month** (25% conversion tho).
Conversion 15% (55 users) ayina **≈ ₹11,000/month** — server cost (₹1,500–2,500) ki 5x.

---

## 6) 🛡️ WHATSAPP ANTI-BAN (recap — full detail `WHATSAPP-ANTIBAN-AND-REQUESTS.md`)

* **Order:** Telegram mundu → WhatsApp tarvata (dual posting)
* **Random gap:** `120–170s` (interest/request messages fast lane `60–120s`)
* **Break:** prathi 6 messages ki 8–20 nimushala break; 8% chance extra 3–8 min pause
* **Caps:** 60/day total (warmup day-1 lo 33% → day-4 lo 100%), target/group ki 8/day
* **Quiet hours:** 8–22 IST (raatri aapitam)
* **Safety:** 3 consecutive failures → 30 min auto-pause; pause/resume/reset endpoints + `/growth` lo buttons
* **Message variety:** text variants + emoji/formatting randomize (exact same message repeat avvadu)

## 7) 🧪 Tests

```bash
cd backend
python test_growth_namaste_leads.py     # 109 checks: namaste, leads, share kit, inventory, anti-ban, pricing parity
python test_interest_antiban.py         # 83 checks: interest flow + anti-ban + porutham/views/add-ons
python test_channels_router.py          # 57 checks: 65-channel routing (caste-wise + region)
```

## 8) 📅 90-DAY GROWTH PLAN (short)

* **Day 1–7:** VM deploy + bot token + WhatsApp bridge QR + `LAUNCH_SEED_COUNT=360` + 43 caste channels create
* **Day 8–30:** community onboarding (playbook §4) + daily digest (9 AM) + lead follow-up calls
* **Day 31–60:** SEO pages (already 289 → district × caste expand), YouTube/Reels campaign, bureau tie-ups
* **Day 61–90:** wedding vendors (₹5k/vendor), bureau SaaS dashboard, Telugu voice profile (phone lo cheppu → auto-fill)
