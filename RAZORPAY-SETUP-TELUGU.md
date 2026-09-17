# 💳 RAZORPAY SETUP — Step by Step (Telugu)

> Ippudu site **UPI-manual mode** lo nadustundi (user pay chesi UTR isthe admin confirm).
> Razorpay keys pedithe **automatic online payment** ON — user pay cheyyagane credits auto-add. 
> Code 100% ready — kevalam keys + webhook matrame kavali.

## 0. Dabbulu ela vastayi (mana site flow)

```
User /pricing → plan select → Order create (server amount fix chestundi)
  → Razorpay checkout (UPI/Card/Netbanking) → Pay
  → /api/pay/verify (signature verify) → ✅ credits auto-add
  → backup: webhook payment.captured vachina fulfill (rendu safe: duplicate kaadu)
Refund: Admin → PayConsole → Refund (Razorpay nunchi money back + credits reverse)
```

Secret key **eppudu browser ki velladu** — anni backend lone. 🔒

## 1. Razorpay account (10 min, FREE)

1. https://dashboard.razorpay.com/signup — email + phone tho account
2. Business details: *Mana Vivaha / matrimony services*, website `https://manavivaha.in`
3. **TEST mode** lo start chey (KYC akkarledu — test keys instant ga vastayi)

## 2. Test keys teesuko (2 min)

1. Dashboard → left menu **Settings → API Keys → Test Mode** → *Generate*
2. Vastayi: `Key Id` (`rzp_test_...`) + `Key Secret` (okkasari matrame kanipistundi — copy chesko!)

## 3. Server .env lo pettu + restart (2 min)

Server lo (Oracle VM / docker host):

```bash
cd matrimony-site
cp .env.example .env        # okkasari matrame
nano .env                   # kindha 2 lines fill chey:
```

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxx
RAZORPAY_VERIFY_CAPTURE=1
PAY_UPI_ID=manavivaha@upi
```

```bash
docker-compose up -d --build backend    # restart
curl https://manavivaha.in/api/pay/config
# {"mode":"razorpay", ...} vaste ✅ ON (manual_upi vaste keys sarigga ledu)
```

## 4. Webhook pettu (3 min — backup fulfill kosam MUST)

1. Dashboard → **Settings → Webhooks → + Add New Webhook**
2. URL: `https://manavivaha.in/api/pay/webhook`
3. Events (4): `payment.authorized` + `payment.captured` + `payment.failed` + `refund.processed`
4. Secret generate chesi copy → `.env` lo pettu:
   ```env
   RAZORPAY_WEBHOOK_SECRET=whsec_xxxx
   ```
5. Restart backend. Dashboard lo *Send test event* → mana side accept ayyinda chudu.

## 5. Test payment chey (5 min — REAL dabbulu povi!)

Test mode lo dabbulu **real kaadu**:
- UPI: `success@razorpay` (success) / `failure@razorpay` (fail test)
- Card: `4111 1111 1111 1111`, CVV edaina, date future

Site lo /pricing → ₹99 plan → pay → **credits add ayyaya?** Admin → PayConsole lo order `paid` kanipinchala? ✅ ayithe perfect.

## 6. LIVE ki (real dabbulu kosam)

1. Dashboard → **KYC submit**: PAN + bank account + address proof + business proof
2. Razorpay approve chesaka (1–3 days) → **Live Mode** → live keys (`rzp_live_...`)
3. `.env` lo test keys → live keys replace + **webhook malli live mode lo create** (secret kotha)
4. Restart → `/api/pay/config` → `mode: razorpay` ✅
5. First real payment: nee phone nunchi ₹99 pay → credits + bank settlement (T+2 days) check

## 7. Fees + settlement (telusuko)

- Razorpay commission: domestic ~**2% + GST** per transaction (exact dashboard → Pricing)
- Settlement: T+2 working days nee bank account ki
- Refund chesina commission Razorpay ki pothundi (policy — admin refund ki mundu alochinchu)

## 8. Troubleshoot (problem vaste)

| Symptom | Fix |
|---|---|
| `/api/pay/config` → `manual_upi` | Keys `.env` lo levu / spelling tappu / restart cheyyaledu |
| Checkout open avvadu | `key_id` khali — backend log chudu (`docker logs backend`) |
| Pay ayindi, credits raledu | `/api/pay/verify` fail — browser console + backend log; webhook backup undi kabatti konchem wait chey |
| Webhook 401/unsigned | `RAZORPAY_WEBHOOK_SECRET` dashboard secret tho match avvatledu |
| Test key tho live pay | Test/Live keys kalisayi — mode okate vadali (rendu keys same mode) |
| Refund fail | Razorpay dashboard → payment captured ayyinda chudu; uncaptured ki refund kudharadu |

## 9. Security notes (MUST — dabbulu matter!)

- `.env` file **GitHub lo petta vaddu** (gitignore lo undi — alaage unchali) 🔒
- `Key Secret` + `Webhook Secret` evariki ivvaddu (team ki ivvalsina — admin key matrame)
- LIVE keys test server lo vaddu; TEST keys live site lo vaddu
- Edaina doubt vaste: Razorpay support chat (dashboard lone) — 24x7 untaru

---
*Code status: order → checkout → verify → fulfill + webhook backup + refund + audit — anni tested (Wave 34: 53/0).*
