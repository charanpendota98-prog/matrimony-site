# 📱 PLAY STORE APP — Step by Step (Telugu)

> Mana site already **PWA** (install prompt + offline + push ready). Play Store lo app ga
> pettali ante **TWA (Trusted Web Activity)** — website ne app ga wrap chestham.
> Code ready — kevalam keystore + Play Console steps matrame (2–3 hours pani).

## 0. Mundara kavalsinavi (checklist)

- [ ] Site live HTTPS lo (`https://manavivaha.in`) — TWA ki MUST
- [ ] VAPID keys set (push alerts live kosam) — `.env.example` chudu
- [ ] Google Play Console account ($25 one-time) — https://play.google.com/console
- [ ] App icon 512x512 (undi: `frontend/public/icons/icon-maskable-512.png`) ✅

## 1. TWA app generate (PWABuilder — easy, 15 min)

1. https://www.pwabuilder.com → URL `https://manavivaha.in` → *Start* → score check
2. *Package for stores* → **Android** → options:
   - Package ID: `in.manavivaha.app` (marckoddu — lifetime same!)
   - App name: `Mana Vivaha`
   - Display: `standalone`, Orientation: `portrait`
   - Signing key: **New** (PWABuilder keystore download chesko — **backup MUST** 🔒)
3. Download `.aab` file (Play Store ki ide upload chestham)

> Alternative (developers): Bubblewrap CLI — `npx @bubblewrap/cli init --manifest https://manavivaha.in/manifest.webmanifest` → `bubblewrap build`

## 2. Asset links (app ↔ site trust, 10 min)

1. PWABuilder/Bubblewrap ichina **SHA-256 fingerprint** copy chey
2. `frontend/public/.well-known/assetlinks.json` lo `REPLACE_WITH...` place lo paste
3. Deploy → `https://manavivaha.in/.well-known/assetlinks.json` open ayyinda chudu
4. Idi lekunte app lo URL bar kanipistundi (trust miss) — **MUST step**

## 3. Play Console upload (30 min)

1. Play Console → *Create app* → name `Mana Vivaha`, category **Social**, free app
2. **App content** fill: privacy policy URL (`https://manavivaha.in/privacy`), 
   data safety (phone number + photos collect chestham — declare chey!), target audience 18+
3. Matrimony = **dating-related** — Play policy: 18+ rating + report/block feature undali
   (manaki ✅ undi: block/report/moderation — review lo cheppu)
4. Release → Production → `.aab` upload → rollout
5. Review 3–7 days → LIVE 🎉

## 4. Release tarvata (prathi update ki)

- Website update ayithe app ki **update akkarledu** (TWA = live site)! 🎉
- App update kavalsindi: icon/name/package change ayithe matrame (version bump + kotha .aab)
- Push alerts: VAPID keys + `pywebpush` server lo unte real send; lekapothe preview queue
- Crash/ANR: Play Console → Android vitals lo chudu (TWA kabatti almost zero)

## 5. iOS (App Store) — tarvata

- iOS lo PWA: Safari → Share → *Add to Home Screen* (already pani chestundi, push iOS 16.4+)
- App Store wrapper (Capacitor) kavali ante cheppu — tarvata wave lo chestham

## 6. Troubleshoot

| Symptom | Fix |
|---|---|
| PWABuilder score low | HTTPS + manifest + icons + sw.js live lo unnai chudu |
| App lo URL bar | assetlinks fingerprint tappu / deploy kaledu / package ID mismatch |
| Push radu | VAPID keys `.env` + `pywebpush` install + backend restart; `/api/admin/push/queue` lo check |
| Install prompt radu | PWA already install ayyundachu / criteria (HTTPS + SW + manifest + icons) miss |
| Play reject (policy) | 18+ rating + privacy policy + data safety + report/block — anni set chesko |

---
*Code status: manifest ✅ sw.js (offline + push) ✅ install prompt ✅ VAPID backend ✅ /me Alerts tab ✅*
