# 🛡️ WhatsApp Anti-Ban + 💌 Requests Model — Full Playbook

> **Idi rendu modules tho website "top matrimony site" kanna advanced ga untundi:**
> 1. **Anti-ban WhatsApp publishing** — Telegram ayyaka WhatsApp ki, prati post madhya **120–170 sec random gap**
> 2. **Interest/Request model** — 🚫 chatting ledu, request → WhatsApp lo profile share → accept aithe number exchange

---

## PART 1 — 🛡️ ANTI-BAN WHATSAPP ENGINE

### Ela pani chestundi (order + timing)

```
Register / approve
   ↓
1) TELEGRAM channels (@TSBRIDE, caste channels… oka sari pothadi — 1.2s gap)
   ↓   (a tarvata matrame)
2) WHATSAPP queue (wa_antiban.py engine)
       ├─ RANDOM GAP 120–170s (fixed kadu — prati post ki kotha draw, aa gap LOCK avutundi)
       ├─ Prati 6 posts ki okasari 8–20 min "coffee break"
       ├─ 8% chance extra 3–8 min pause (manishi phone pakkana pettadu)
       ├─ Typing simulation: 2–9 sec "composing" presence (type chesthunnattu)
       ├─ Message variants: 5 greeting/CTA versions rotation (same text repeat avvadu)
       ├─ Order shuffle: channels random order lo (pattern kanipinchadu)
       └─ State file: wa_state.json (restart lo burst avvadu — counters persist)
```

### Anti-ban rules (anni env tho tune cheyyochu)

| Rule | Default | Env | Enduku |
|---|---|---|---|
| Random gap | **120–170 sec** | `WA_MIN_GAP`, `WA_MAX_GAP` | Bulk ga fixed timing = instant ban. Random = manishi la |
| Interest fast lane | 60–120 sec | `WA_MIN_GAP_INTEREST`, `WA_MAX_GAP_INTEREST` | Interest notification koncham fast (kani still random) |
| Long break | prati 6 msg → 8–20 min | `WA_BREAK_EVERY`, `WA_BREAK_MIN_MIN`, `WA_BREAK_MAX_MIN` | Continuous posting = spam signal |
| Random pause | 8% chance, 3–8 min | `WA_LONG_PAUSE_CHANCE` | Manishi behaviour |
| Daily cap | 60/day (total) | `WA_DAILY_CAP` | Number health |
| Warmup ramp | day1 33% → day2 55% → day3 75% → 100% | `WA_WARMUP_DAYS` | Kotha number ki ramp — WhatsApp new-number detection avoid |
| Per-channel cap | 8/day | `WA_TARGET_DAILY_CAP` | Okate group lo spam kanipinchakunda |
| Active hours | 8AM–10PM IST | `WA_ACTIVE_START`, `WA_ACTIVE_END` | Raatri 3 gantalaki posts = bot signal |
| Typing sim | 2–9 sec | auto | "composing" presence = human signal |
| Cooldown | 3 fails → 30 min pause | `WA_FAIL_COOLDOWN_MIN` | 429/network issues lo ventane aagutundi |
| Kill switch | — | `WA_ENABLED=false` leda `POST /api/wa/pause` | Eppudaina ventane aapochu |

**Combine lo daily capacity:** 60 msg/day × ~2.5 min average gap ≈ **2.5 గంటలు continuous posting** — 43 caste channels unnayi, so okate channel ki rojuki 1–2 posts padathayi. Ide safe pattern.

### Enduku idi "smart" (manishi la)

1. **Fixed timing ledu** — prati gap random, aa random value send-time lo lock (re-roll avvadu → floor ki collapse avvadu)
2. **Typing presence** — recipient ki "typing…" kanipisthundi (stalker bot ledu)
3. **Work hours + breaks** — manishi la tinnanki, nidraki aagutam
4. **Content variation** — same message repeated ga velladu (fingerprint detection avoid)
5. **Queue priority** — interest/request messages mundu (business critical), bulk channel posts tarvata
6. **State persist** — server restart ayyina counters gurthu untayi (restart burst = classic ban cause)

### WhatsApp connect cheyyadam (2 options)

**Option A — Bridge (Baileys, mee own number, free):**
```bash
cd ~/matrimony-site
# .env lo:
WHATSAPP_MODE=bridge
WHATSAPP_BRIDGE_URL=http://whatsapp-bridge:3001
WHATSAPP_BRIDGE_TARGETS=120363xxxxxxxx@g.us,9198480xxxxx@s.whatsapp.net
WA_MIN_GAP=120  WA_MAX_GAP=170        # mee ishtam — slow ga safer
sudo -E docker-compose up -d --build whatsapp-bridge
# QR scan: http://<server-ip>:3001/qr  → WhatsApp → Linked Devices → Link a Device
```
✅ Free, groups + newsletter ki post cheyyochu • ⚠️ Unofficial → gap rules **strict ga** follow avvali

**Option B — Meta WhatsApp Cloud API (official, safe):**
```bash
WHATSAPP_MODE=cloud_api
WHATSAPP_TOKEN=EAAG...      WHATSAPP_PHONE_ID=1234567890
WHATSAPP_TO=9198480xxxxx    # opt-in numbers / broadcast list
```
✅ Ban risk ledu (official) • ⚠️ Template messages + opt-in rules • Business verification kavali

**Best combo (recommended):** Bridge tho **groups/community channels**, Cloud API tho **customer notifications** (interest, accept, decline). Rendante oke queue — anti-ban engine rendu handle chesthundi.

### Ban ayyithe em cheyyali (recovery)

1. `POST /api/wa/pause` — ventane aapandi (queue retain avutundi)
2. WhatsApp Business app lo appeal cheyyandi (ban reason + usage explain)
3. Backup number ki switch: kotha session (`SESSION_DIR` kotha folder) → **warmup ramp** tho start (`WA_WARMUP_DAYS=7` pettu, `WA_DAILY_CAP=25`)
4. 2–3 numbers rotation: `.env` lo bridge targets number-wise separate ga pettukoni, weekly rotate cheyyandi
5. **Permanent fix:** Cloud API ki migrate (official — ee settings motham akkarki apply avutayi)
6. Telegram ni primary ga unchandi — WhatsApp down ayyina business aagadu (already 65 Telegram channels ready)

### Monitoring (admin)

```bash
curl -s localhost:8000/api/wa/status | python3 -m json.tool     # gap, cap, queue, last events
curl -s localhost:8000/api/wa/pause                             # ventane aapu
curl -s localhost:8000/api/wa/resume                            # malli start
curl -s localhost:8000/api/wa/reset_day                         # (test) day counters reset
curl -s localhost:8000/api/publish/log?limit=20                 # per-post audit (ok/fail)
```
Frontend: **/requests** page lo anti-ban live widget undi (gap, cap, today sent, queue).

---

## PART 2 — 💌 REQUESTS MODEL (CHATTING LEDU)

### Enduku chatting ledu (mee decision — 100% correct)

| Chatting unte | Chatting lekunda (mana model) |
|---|---|
| 24/7 moderation team kavali (₹40k+/mo) | Moderation avasaram ledu |
| Fake ids, harassment, screenshots leak | Consent-based — iddaru oppukunnappude contact |
| Time waste (endless hi/hello) | Direct: accept → phone numbers |
| Legal risk (abuse reports, police cases) | Report + block + refund policy tho clean |
| Server load (websockets, storage) | Simple REST — 1GB RAM lo kooda chalu |

### Flow (exact ga)

```
1. User A: profile B chusi "💌 Interest Pampu"  → 1 credit (modati 3 FREE)
        ↓
2. Mana WhatsApp nunchi → B ki message:
   "💌 Mee profile ki INTEREST vachhindi! Oka person mee profile chusi
    'interesting ga unnaru' ani request pettaru 👇
    👤 Kiran Kumar Reddy (29y) 🎓 MBBS 💼 Doctor
    📍 Nalgonda 💍 Reddy ⭐ 82% match
    📸 Aa person profile card (image attachment)
    ✅ Accept chesthe → valla number meeku WhatsApp lo
    🆔 REQ-260914-5573 ⏳ 7 days valid"
        ↓
3. B: ✅ Accept  →  rendu numbers WhatsApp lo (iddariki) — direct matladukovachu
   B: ❌ Decline →  polite message + A ki credit REFUND (trust!)
        ↓
4. Status tracker: /api/interest/status/{id} → 4 steps (pampu → deliver → reply → exchange)
```

### Pricing (final — mee numbers)

| Plan | Price | Profiles | Per profile | Validity |
|---|---|---|---|---|
| **FREE** | ₹0 | **3 requests** | — | 365 days |
| **Sambandham** | ₹99 | **3** | ₹33 | 30 days |
| **Family** | ₹199 | **10** | ₹20 | 45 days |
| **Premium** | ₹299 | **20** | **₹15** (best) | 60 days |
| Bureau/Agents | ₹999/mo | 25 + monthly report | ₹40 | 30 days |

**Extra trust rules (already code lo):**
- Decline **leda** withdraw aithe → **credit refund** ✅
- Request 7 days lo reply rakapothe → auto expire (+ refund)
- Oka profile ki rendu sarlu request pampalevu (duplicate block)
- Rojuki max 20 requests per user (spam/fraud block)
- Own profile / same gender / fake ID → block
- Contact accept varaku **LOCK** (🔒) — evaru data dump cheyyaledu

### APIs (anni frontend ki wired)

| Endpoint | Enti chestundi |
|---|---|
| `GET /api/plans` | Pricing ladder (₹99→3, ₹199→10, ₹299→20) |
| `GET /api/credits/{tsap_id}` | Balance + sent/pending/accepted/refunded |
| `POST /api/credits/buy` | Plan buy (Razorpay live ayyaka webhook tho verify; `PAYMENT_AUTO_APPROVE=true` → demo lo instant) |
| `POST /api/interest/send` | Interest pampu (1 credit) → owner WhatsApp + requester confirmation |
| `GET /api/interest/inbox/{id}` | Vachina requests (+ actions accept/decline) |
| `GET /api/interest/sent/{id}` | Pampina requests + status + contact (accept ayyaka) |
| `POST /api/interest/respond` | accept / decline / withdraw (refund logic tho) |
| `GET /api/interest/status/{id}` | 4-step tracker |
| `GET /api/wa/status` | Anti-ban live status |
| `POST /api/wa/pause` / `resume` / `reset_day` | Control |

### Frontend (ready)

- **/requests** — dashboard: ID load, inbox (accept/decline), sent list, interest pampu form, plans+credits, anti-ban widget, demo button
- **/matches** — prati card ki **💌 Interest Pampu (1 credit)** button
- **/search/{id}** — profile page lo interest CTA
- **/** — "Chatting ledu" section WhatsApp mockup tho + pricing strip

### Test cheyyadam (2 nimushalu)

```bash
cd ~/matrimony-site/backend
WA_TEST_FAST=true PUBLISH_DRY_RUN=true python3 test_interest_antiban.py    # 54 checks
```
Website lo: **/requests** → "🎬 Demo profiles load" → mee ID `TSAP-M-2025-1042` → bride `TSAP-F-2025-1042` ki interest pampu → `TSAP-F-2025-1042` tho load chesi **Accept** cheyyandi → numbers exchange kanipisthundi.

---

## ✅ QUICK CHECKLIST (production ki)

- [ ] `.env` lo `WA_MIN_GAP=120`, `WA_MAX_GAP=170` (mee ishtam — 180–240 inka safer)
- [ ] `WHATSAPP_MODE` set (bridge QR scan ayyindi / cloud_api token)
- [ ] `PUBLIC_BASE_URL=https://manavivaha.in` (card image bridge ki reach avvali)
- [ ] Razorpay live ayyaka `PAYMENT_AUTO_APPROVE=false` + webhook URL
- [ ] `DEMO_SEED_ENABLED=false` (production lo demo profiles vaddu)
- [ ] Daily: `curl /api/wa/status` chusi cap/queue monitor cheyyandi
- [ ] Weekly: WhatsApp number rotation plan (2–3 numbers ready)
- [ ] `INTEREST_REFUND_ON_DECLINE=true` unchandi (trust = conversions)
