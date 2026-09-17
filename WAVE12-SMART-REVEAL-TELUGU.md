# 🔒 WAVE 12 — SMART REVEAL ENGINE (branch lone, merge cheyaledu)

> User demand: channels lo number ❌ peru ❌ surname ❌ → credits/premium tho unlock →
> ₹500 assisted: admin Match&Send → personal Telegram/WhatsApp → copy-list.
> Chat vaddu (interest-only continue).

## ✅ Emi build ayindi (100% workable + tests + live proof)

### 1. 🔒 Masked channel posts (TEASER model)
- Caption v2: `👰 L•••••i R•••y • 24y • Reddy • BTech • Software • Hyd • 🆔 TSAP-F-9882`
- Number ❌ full-name ❌ surname ❌ — caste/filters ki kavalsinavi matrame kanipisthayi
- CTA: `🤖 Bot → /unlock TSAP-F-9882 (1 credit)` + site link + mosam-jagratha line
- Telegram + WhatsApp rendu captions masked (`build_caption`, `build_whatsapp_text` rewire)
- Bot `/search` card kooda masked + `/unlock <ID>` hint

### 2. 💳 Credits → Unlock engine (`backend/smart12.py`)
- `POST /api/unlock {viewer_id, target_id}`:
  - entitled (paid/granted) → **FREE** reveal · lekapothe **1 credit cut** → reveal
  - 0 credits → paywall (`₹99=5 credits` / `₹500 assisted` options tho)
  - self unlock eppudu free · anni reveals **audit log** (`REVEAL_LOG`)
- `GET /api/unlocks/{id}` — naa unlocked list (**masked**, full number per-unlock matrame)
- Entitlements `unlocks12.json` lo persist (restart ayina potavu)

### 3. 🤖 Bot commands (kotha 5)
- `/link TSAP-ID` — Telegram ↔ profile link (unlock + personal delivery kosam)
- `/unlock <ID>` — number reveal (1 credit / entitled-free)
- `/mylist` — unlocked profiles masked list · `/balance` — credits · `/pay` — UPI/call + packs
- `/help` update · pure formatters (network lekunda test Qiu)

### 4. 🎯 Admin Match&Send console (`/admin` → 🎯 tab)
- Buyer ID → **perfect matches auto-load** (score sort, same-gothram auto-skip, boosted first)
- Neat filters: age, caste, district, marital, ✅verified, 📸photo, text search — **enni unte anni**
- ☑️ select → `➕ ₹500 order` → UTR → `✅ Paid` → via (both/TG/WA) → `🚀 Send personal ga`
- 📩 Telegram DM (buyer chat_id ki, bot pool failover) + 💬 WhatsApp queue (anti-ban safe)
- Tokens lekapothe **honest dry-run** + 📋 **copy-list** (`1. 👰 Lakshmi R. -- 9848012345 (...)`)
- Copy button — admin copy chesi manual ga paste cheyochu
- **STRICT**: pampina profiles mathrame buyer ki unlock — `/mylist` lo ivi matrame

### 5. 📞 Website unlock button (`/search/[id]`)
- `📞 Number Unlock (1 credit)` → reveal → Call/WhatsApp buttons
- Login lekunte AuthGate · 0 credits ayithe paywall msg

## 🧪 Proof
- **Kotha suite `test_wave12_smart.py`: 75/75** ✅ (masking/caption/unlock/orders/API/bot/privacy)
- **Patha suites anni green** (~1316 checks, 0 fail) ✅
- Frontend `npm run build` ✅ · Backend :8000 + Website :3000 live, curl tho verify ✅
  - caption leak-check False · unlock 1-cut · match-send 3 · copy-list `NAME -- NUMBER` · deliver dry-run honest

## 🔌 Kotha endpoints
| Method | Path | Auth |
|---|---|---|
| POST | `/api/link-telegram` | open (bot) |
| POST | `/api/unlock` | open (logged) |
| GET | `/api/unlocks/{id}` | open (masked) |
| POST | `/api/admin/assist-orders` | 🔐 admin |
| GET | `/api/admin/assist-orders?status=` | 🔐 admin |
| POST | `/api/admin/assist-orders/{id}/paid` | 🔐 admin |
| POST | `/api/admin/assist-orders/{id}/profiles` | 🔐 admin |
| GET | `/api/admin/match-send/{buyer}` | 🔐 admin (full phones) |
| GET | `/api/admin/match-send/copy-list?buyer=&ids=` | 🔐 admin |
| POST | `/api/admin/match-send/deliver` | 🔐 admin |
| POST | `/api/admin/link-telegram` | 🔐 admin |

## ⏳ Live ki kavalsinavi (code ready, keys/link lu pedithe live)
- `BOT_TOKEN` (bot + Telegram DM send) · `ADMIN_CHAT_ID`
- WhatsApp: `WHATSAPP_MODE=bridge/cloud_api` + targets (personal WA send)
- `PAY_UPI_ID` + `SUPPORT_CALL_NUMBER` (bot /pay lo kanipisthayi)
- Razorpay (auto credits — ippudu manual UTR flow, adi kooda workable)

## 📁 Files
- NEW: `backend/smart12.py`, `backend/test_wave12_smart.py`, `frontend/src/components/MatchSend.tsx`
- EDIT: `backend/main.py` (routes), `backend/channels_config.py` (masked caption),
  `backend/publisher.py` (masked WA), `backend/telegram_bot.py` (5 commands + masked card),
  `frontend/src/app/admin/page.tsx` (tab), `frontend/src/app/search/[id]/ProfileView.tsx` (unlock)
