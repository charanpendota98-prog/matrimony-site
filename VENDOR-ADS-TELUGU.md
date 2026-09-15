# 🏪 VENDOR ADS + PROMOTIONS — "పెళ్లి సంబంధం వాళ్లందరికీ ప్రచారం"

> **ఒక్క లైన్:** కేటరింగ్, ఫోటోగ్రఫీ, డెకరేషన్స్, హాల్, పండితులు, నగలు, మేకప్, DJ… **పెళ్లి సంబంధం
> ఉన్న ప్రతి బిజినెస్** Mana Vivaha లో ప్రచారం చేసుకోవచ్చు — **₹149 నుండి**. ఎంక్వైరీలు **నేరుగా వాళ్ల
> WhatsApp కి**.
>
> Website: **manavivaha.in/vendors** · బిజినెస్ add చేయడానికి: **manavivaha.in/vendors/register** ·
> Admin: **manavivaha.in/admin → 🏪 Vendor Ads**

---

## 1. 18 categories (పెళ్లి సంబంధం అన్నీ)

| | | | |
|---|---|---|---|
| 🍛 Catering (విందు భోజనం) | 📸 Photography | 🎥 Videography / Drone | 🌸 Decorations & Flowers |
| 🏛️ Function Hall | ⛺ Tent House | 🕉️ Pandit / Priest | 💍 Jewellery |
| 👰 Bridal & Groom Wear | 💄 Makeup & Beautician | 🌿 Mehendi (గోరింటాకు) | 🎶 DJ / మేళం బ్యాండ్ |
| ✉️ Invitations / Printing | 🚗 Cars & Travel | 📋 Wedding Planner | 🎂 Bakery & Cake |
| 🎁 Gifts & Hampers | ✈️ Honeymoon Packages | | |

---

## 2. Ad packages (₹)

| Package | ధర | రోజులు | ఏమి వస్తుంది |
|---|---|---|---|
| **Single Channel Post** | **₹149** | 1 | 1 Telegram post (mirror channel) + report (views/enquiries) — test చేయడానికి |
| **Basic Listing** | **₹499** | 30 | Directory listing + 1 Telegram promo post + call/WhatsApp CTA |
| **WhatsApp Status Blast** | **₹499** | 1 | మా 3 status lanes లో promo + bonus Telegram post |
| **Spotlight (7 days)** | **₹999** | 7 | Top banner (7 రోజులు) + status blast + 4 main channels post — season push |
| **Standard Promo** 🔥 | **₹1499** | 90 | 3 listings + 3 TG + 2 WA posts + **lead box** + priority placement + monthly report |
| **Premium Partner** 👑 | **₹3999** | 180 | 5 listings + weekly posts (24+) + top slot + ✅ Verified badge + status blasts + account manager |

**Add-ons:** Photo/Video gallery ₹299 · Reel/Short video ₹999 · Vendor interview video ₹1499 · Bride/Groom DB mail ₹799
**Renewal:** 15% discount · **Ad slots:** home top banner · home mid strip · vendors top · matches sidebar · requests sidebar

---

## 3. వాళ్లకి ఏమి దొరుకుతుంది (value)

| | |
|---|---|
| 📢 **Reach** | 52 Telegram channels (region + religion + caste) + WhatsApp lanes (anti-ban safe order) + website banners |
| 📊 **Report** | Impressions · Clicks · Enquiries — ఏది పని చేసిందో వెండర్ dashboard లో live |
| 📩 **Leads** | ఎంక్వైరీ form → వెండర్ WhatsApp కి instant message (పేరు, ఫోన్, ఈవెంట్ తేదీ, బడ్జెట్, requirement) |
| 🖼️ **Poster** | QR ఉన్న poster (1080×1080 + status 1080×1920) — వాళ్ల WhatsApp గ్రూపుల్లో పెట్టుకోవచ్చు |
| 📝 **Post ready** | Telugu promo post (Telegram + WhatsApp variants) — ఒక్క copy |
| ✅ **Trust** | Verified badge + rating + reviews |
| 🔁 **Renewal** | 15% discount + season offers (ఆషాఢం, మార్గశిర, పడ్వ) |

---

## 4. వెండర్ flow (5 steps — 2 నిమిషాలు)

1. **/vendors/register** → category select → business details (peru, phone, city, rate range, 3-4 lines about)
2. Package select → **submit (free signup)**
3. **Payment** (UPI / PhonePe deep link — amount auto) + screenshot మా WhatsApp కి (reference: MVV-xxxx)
4. **Admin verify (2 గంటల్లో)** → listing **ACTIVE** + ✅ badge + promo post + poster ready
5. **Enquiries direct WhatsApp కి** + dashboard లో performance report

---

## 5. మనకి ఏమి వస్తుంది (business case)

| విషయం | లెక్క |
|---|---|
| 1 vendor (Standard ₹1499 / 90 days) | ≈ **₹500/నెల** per vendor |
| 20 vendors (Basic/Standard mix) | ≈ **₹12,000–20,000/నెల** recurring |
| 5 Premium (₹3999 / 180 days) | ≈ **₹11,000/నెల** + premium badge revenue |
| Season spotlight (₹999 × 10) | **₹9,990** per season (ఆషాఢం/మార్గశిర) |
| Leads → booking commission (తరువాత) | 2–5% (optional, vendor agreement తో) |

**ఇది pure profit margin** — ఖర్చు: ఒక్క promo post (ఇప్పటికే channels + WhatsApp lanes ఉన్నాయి).
Bureau (broker B2B) + referral (₹50) + vendor ads (₹149+) = **మూడు revenue lines**.

---

## 6. Technical (developer కోసం)

| భాగం | ఫైల్ / endpoint |
|---|---|
| Engine (categories, packages, register/activate, directory, rotation, leads, dashboards, revenue) | `backend/vendors.py` |
| Poster with QR (1080×1080 / 1080×1920, ASCII-safe) | `backend/vendor_kit.py` |
| Public API | `GET /api/vendors/categories` · `/packages` · `/stats` · `/vendors?category&district&city&q` · `/ads?slot&limit` · `/{id}` · `/{id}/dashboard` · `/{id}/promo` · `/{id}/poster.png?style` |
| Public POST | `/api/vendors/register` · `/{id}/lead` · `/{id}/click` |
| Admin | `GET /api/admin/vendors?status=` · `POST /api/admin/vendors/{id}/action?action=approve&utr=&package=|reject|expire` · `GET /api/admin/vendors/revenue/summary` (ADMIN_TOKEN ఉంటే token తప్పనిసరి) |
| Pages | `/vendors` (directory + packages) · `/vendors/register` (signup + payment) · `/vendors/[id]` (customer view + **vendor dashboard tab**) · home ad strip · `/admin` vendor tab |
| Tests | `backend/test_vendors_ads.py` (**130 checks**) · `backend/verify_live_flow.py --vendor` (live E2E: register → approve → lead → revenue) |

**Ad priority order:** SPOTLIGHT/PREMIUM → STANDARD → BASIC → SINGLE_POST (weights 6/5/3/1, random shuffle).
**State:** `backend/vendor_state.json` (gitignored) — vendors, leads, impressions/clicks log.

---

## 7. ఇప్పుడు మీరు చేయాల్సిన పని (3 నిమిషాలు)

1. **/vendors** చూడండి — 10 demo vendors ready ఉన్నాయి (Warangal, Hyderabad, Vijayawada, Karimnagar, Guntur, Nizamabad, Vizag, Khammam).
2. మీకు తెలిసిన **5 vendors** కి ఈ message పంపండి (కింద copy ఉంది) — వాళ్లు register చేసుకుంటారు.
3. Admin లో **🏪 Vendor Ads** tab → payment వచ్చాక **UTR paste → ✅ Activate** → listing + promo post live (+ poster download).

---

## 8. Vendors కి పంపాల్సిన WhatsApp message (copy-paste)

```
🙏 Namaste! Mana Vivaha (TS/AP Telugu Matrimony — manavivaha.in) nunchi.

మా దగ్గర ఇప్పుడు TS + AP నుండి పెళ్లి చూసుకునే 1000+ families ఉన్నారు (52 Telegram channels + WhatsApp groups).
మీ <CATERING / PHOTOGRAPHY / DECORATIONS> business ని వాళ్లకి చూపించగలము — **₹149 నుండి**.

ఏమి దొరుకుతుంది:
✅ Website directory listing (18 categories — మీ category లో)
✅ 52 channels లో Telugu promo post (మీ city/caste channel + 4 main)
✅ WhatsApp status/groups లో ప్రచారం (anti-ban safe order lo)
✅ **Enquiries నేరుగా మీ WhatsApp కి** (పేరు, ఫోన్, event date, budget)
✅ QR poster (మీ groups లో పెట్టుకోవచ్చు) + dashboard report (views/clicks/leads)

Packages: ₹149 (1 post) · ₹499 (30 days listing) · ₹999 (spotlight) · ₹1499 (90 days + lead box) · ₹3999 (180 days + top slot + verified badge + weekly posts)
Renewal కి 15% discount.

Register: manavivaha.in/vendors/register (2 నిమిషాలు) — payment తరువాత 2 గంటల్లో listing live.
Demo చూడండి: manavivaha.in/vendors
```

---

## 9. Referral update — **షరతులు లేవు** ✅

- **ఎవరైనా, ఎన్ని అయినా** refer చేయోచ్చు — **లిమిట్ లేదు**.
- **ఒకే ఫోన్ నుండి కూడా** పర్వాలేదు (ఇంట్లో అందరూ ఒకే నంబర్ వాడుకుంటున్నా సరే) — conditions లేవు.
- Flow: **Register FREE (3 profiles free)** → తరువాత ఆ friend **₹99 pay చేసి offer తీసుకున్నప్పుడే** → referrer కి **₹50**.
- 3+ accounts ఒకే నంబర్ నుండి వస్తే → *review flag* మాత్రమే (block కాదు, commission hold కాదు); నిజమైన కేసులకి ఎటువంటి ఇబ్బంది లేదు.
- Daily/lifetime caps కూడా **soft** (50/day, 500 lifetime) — flag మాత్రమే.
- Details: **REFERRAL-2-TELUGU.md**
