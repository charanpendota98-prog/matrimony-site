# TEST — Normal First — 2 Channels Only — Simple Basic ✅
> Anna, yes — normal first 2 channels tho test cheddam — simple, basic, no deep verification — idi test plan — pin-to-pin — 2 hours lo full test!

## LIVE Setup — Ready for Test

- **Channels LIVE (2):**
  - 👰 TS BRIDE: https://t.me/TSBRIDE — @TSBRIDE — Bot Admin @telugumatrimony1_bot ✅
  - 🤵 TS GROOM: https://t.me/TSGROOM1 — @TSGROOM1 — Bot Admin ✅
- **Bot LIVE:** https://t.me/telugumatrimony1_bot — Token secure backend/.env
- **Website LIVE:** http://localhost:3000 — 9 pages — simple MVP
- **Backend LIVE:** http://localhost:8000 — /docs — API
- **Seed:** 40 profiles ready — backend/seed_profiles.json — 20 brides → @TSBRIDE, 20 grooms → @TSGROOM1
- **DPs:** dp-tsbride.png, dp-tsgroom1.png — frontend/public/
- **Referral Short Code:** LAK42 — 5 chars — easy — auto fill lock — LIVE
- **Commission:** ₹50 first ₹99 pay — 50% — no thappu — viral — LIVE

## Test Plan — 8 Tests — Normal, Simple, Basic — 2 Hours

### Test 1: Website Register with Referral Auto Fill Lock — Smart! (15 min)

**Steps:**
1. Open referral link: http://localhost:3000/r/LAK42
2. Check: Auto redirect to /register?ref=LAK42 → referral field auto fill LAK42 + 🔒 lock + message "Lakshmi aunty dwara vacharu — trusted! — 1 extra credit FREE! 🎉" — working?
3. Fill Step1: Bride, Age 24, Height 5'4", Marital Pelli Kaledu
4. Fill Step2: Caste Reddy, Education BTech, Job Software, State TS, District Nalgonda, Mandal Gachibowli, Photo-private OFF
5. Fill Step3: Photo 1 (mock), Phone 98480xxxxx, Referral LAK42 locked (cannot edit) — check lock working?
6. Submit → Generate ID TSAP-F-2025-XXXX + Card preview + 3 FREE credits + auto-post queue @TSBRIDE + @tsap_reddy (but now only @TSBRIDE) + Top 3 FREE reason basic
7. Check: ID generated? Card preview neat? Credits 3? Referral LAK42 saved?

**Expected:** ID + Card + 3 credits + Top 3 FREE + Referral locked — working — simple!

### Test 2: Admin Approve → Auto-Post to @TSBRIDE / @TSGROOM1 (15 min)

**Steps:**
1. Open Admin Panel: http://localhost:3000/admin → Profiles tab
2. Find new profile TSAP-F-XXXX — Status Pending
3. Click Approve → Check: Status Approved + posted_to @TSBRIDE (if Bride) or @TSGROOM1 (if Groom) — working?
4. Open Telegram Channel @TSBRIDE / @TSGROOM1 → Check: Card posted with footer "Bot: @telugumatrimony1_bot | ID Search: tsapmatrimony.com/search/TSAP-XXXX | Join: @TSBRIDE @TSGROOM1 | Fraud warning" — working?
5. If network blocked in sandbox, backend log shows "Would post to @TSBRIDE" — on Oracle VM with internet it will post real — test via backend/test_channels.py

**Expected:** Approve 1 click → auto-post to live channel — simple — working!

### Test 3: ID Search Always Open — Limit Ayina Kuda Open (10 min)

**Steps:**
1. Open Search: http://localhost:3000/search/TSAP-F-2025-1001 (seed profile)
2. Check: Profile open even if credits 0? — Yes — ID search always open — nuvvu adigina logic — working?
3. Check: Photo blur if FREE + private? Number lock 🔒 if credits 0? Reason basic "Same caste, same district"?
4. Click "Number Chudu (1 Credit)" → Credits deduct 3→2 → Number show 98480xxxxx → working?
5. Credits 0 ayyaka → Pay wall "Me credits ayipoyayi, malli ₹99 tho 10" → working?

**Expected:** ID search always open — profile chudochu — number ki credit — perfect!

### Test 4: Matches — Best Only 70%+ + Reason Basic (10 min)

**Steps:**
1. Open Matches: http://localhost:3000/matches
2. Check: Only 70%+ matches + reason "Same caste, same district" — random profiles vaddu — working?
3. Filter: All, Reddy, Nalgonda — filter working?
4. Click Open → goes to Search page → working?

**Expected:** Best only — no random — simple!

### Test 5: Payment Mock → Referral Commission ₹50 — No Thappu Viral! (15 min)

**Steps:**
1. Register with referral LAK42 → Pay ₹99 mock (backend /api/payment/webhook)
2. Backend: POST http://localhost:8000/api/payment/webhook?user_id=TSAP-F-1001&amount=99&razorpay_payment_id=test123
3. Check: User credits 3 → 13 (10 added) + daily quota 2 + plan TRIAL_99 — working?
4. Check: Referrer LAK42 gets ₹50 commission — wallet + credits — working?
   - Instant ₹20 + 2 credits instant + Weekly ₹30 Monday UPI
   - Notification "Lakshmi aunty, me friend pay chesadu — meeku ₹50 vachindi!"
5. Check: Referrer dashboard /referral → Earned ₹50 + Pending — working?
6. Check: Referred user gets 1 extra credit FREE because referral — working?

**Expected:** ₹99 pay → referrer ₹50 — 50% — viral — no thappu — LTV high — working!

### Test 6: Referral Registration — Andariki — Register Avvakunda Kooda Earn — Short Code LAK42 + UPI (15 min)

**Steps:**
1. Open Referral Register: http://localhost:3000/referral/register
2. Fill Step1: Name Lakshmi, Phone 98480xxxxx, Type Lady, District Nalgonda, Contacts 50+
3. Fill Step2 Payout: UPI 98480xxxxx@ybl (must) — 10 sec — easy — Bank optional backup
4. Submit → Code Generate LAK42 short (5 chars) — 3 letters LAK + 2 digits 42 — easy enter! — Links tsapmatrimony.com/r/LAK42 + Bot t.me/telugumatrimony1_bot?start=r_LAK42 + QR poster
5. Check: Code short 5 chars? Easy? Custom option? Share buttons WhatsApp/Telegram/Copy/QR?
6. Check: List saved to localStorage tsap_referrers + admin payouts tsap_admin_payouts — working?
7. Test short link: http://localhost:3000/r/LAK42 → auto redirect → /register?ref=LAK42 → auto fill lock — working? (Test 1 already)

**Expected:** Referral registration for all — no bride/groom needed — short code LAK42 — UPI — easy advanced — best!

### Test 7: Admin Payout — Manual PhonePe — UPI Chalu — Easy 10 Sec! (15 min)

**Steps:**
1. Open Admin: http://localhost:3000/admin → Referral Payouts tab — LIVE!
2. Check: Table Code (short 5 chars LAK42), Name, Type, UPI ID, Bank Backup, Total Refers, Paid, Earned, Pending, Status, Actions
3. Filter: Pending Only → Sort high to low
4. For LAK42 pending ₹250 → Click Copy UPI → UPI copied → Click Copy Amount ₹250 → Amount copied → Click Open PhonePe deep link → phonepe://pay?pa=98480xxxxx@ybl&pn=Lakshmi&am=250&tn=TSAP Referral LAK42 → PhonePe auto open with UPI + Amount + Note — just Send — 5 sec — working? (Deep link works on phone)
5. After send in PhonePe app (real phone) → Come back → Mark as Paid → Enter TXN ID optional → Save → Notification auto to referrer "Meeku ₹250 payout ayyindi PhonePe lo! TXN XXX" + Dashboard update
6. Check: Pending 0, Status Paid ✅, Last Payout date, History log

**Expected:** UPI chalu — PhonePe number kooda chalu — Bank optional — list admin lo — Copy UPI + Copy Amount + PhonePe deep link → Send → Mark Paid — 10 sec per payout — easy advanced — best! — 10 payouts = 1.5 min!

### Test 8: Channel Join + Forward Viral + Launch Poster (15 min)

**Steps:**
1. Open @TSBRIDE https://t.me/TSBRIDE → Check DP dp-tsbride.png, Description copy-paste from LAUNCH-KIT, Pinned Post rules + bot link + footer — perfect?
2. Open @TSGROOM1 same
3. Check: 20 seed profiles posted? If not, post 1-2 manually with footer to test
4. Test forward viral: Forward 1 post from @TSBRIDE to friend → Friend sees footer Bot link + Caste + ID search → clicks Bot link with deep link ch_tsbride → Bot open → Gender → Register → referral auto? — viral loop working?
5. Test launch poster: Copy poster text from LAUNCH-KIT → Share to FB Group TS/AP matrimony + WhatsApp Status + Insta — working?

**Expected:** Channels neat, DP, Description, Pinned, Footer, 20 posts min, forward viral, launch poster — simple MVP ready!

## Test Checklist — 2 Channels Normal — Simple — 2 Hours

- [ ] Test 1 Register with referral auto fill lock LAK42 — 15 min
- [ ] Test 2 Admin approve → auto-post to @TSBRIDE/@TSGROOM1 — 15 min
- [ ] Test 3 ID search always open + credits deduct — 10 min
- [ ] Test 4 Matches best only + reason — 10 min
- [ ] Test 5 Payment ₹99 → referral ₹50 commission — 15 min
- [ ] Test 6 Referral registration all + UPI + short code LAK42 — 15 min
- [ ] Test 7 Admin payout manual PhonePe UPI copy + mark paid — 15 min
- [ ] Test 8 Channel DP + Description + Pinned + Seed 20 + Forward viral + Poster — 15 min

**Total: 2 hours — simple — normal — 2 channels only — no deep verification — basic launch ready!**

## After Test OK — Launch in 2 Days

**Today:** Test 8 tests — fix small bugs — DP + Description + Pinned Post set — 30 min
**Tomorrow:** Seed 20 per channel (40 total) — post to channels — 1 day
**Day-2:** Launch FB + WhatsApp + Insta poster + Referral Register page share for students/ladies/brokers — 2 hours
**Day-3-7:** Daily 1 post per channel, payment test, feedback, 100 members + 50 profiles → Add AP channels + Official + Caste + Verifications Phase-2

## LIVE Links for Test

- Website: http://localhost:3000 — Home, Register, Search, Matches, Channels, Referral, Referral/Register, Bureau, Admin, r/[code]
- Backend: http://localhost:8000/docs — API test
- Channels: https://t.me/TSBRIDE , https://t.me/TSGROOM1 — LIVE ✅ Bot Admin
- Bot: https://t.me/telugumatrimony1_bot — LIVE
- Seed: backend/seed_profiles.json — 40 profiles
- DPs: frontend/public/dp-tsbride.png, dp-tsgroom1.png
- Launch Kit: LAUNCH-KIT-2-CHANNELS.md — DP + Description + Pinned + Footer + Posters copy-paste

**Anna, normal first 2 channels tho test — simple, basic, no deep verification — 8 tests — 2 hours — test plan ready — chudu 👆**

**Test cheddama ippude? Website http://localhost:3000 open chesi Test 1 nunchi start cheddama?**
