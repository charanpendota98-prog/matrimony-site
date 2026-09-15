# 🎨 WEBSITE CUSTOMIZATION GUIDE — Mana Vivaha

> **Anna, ee website ni nuvve customize cheyyagalav** — code rayakunda, okka file lo values marchi.
> Ee guide lo: enti ekkada undi, ela marchali, em verify cheyyali — antha clear ga.

---

## 1. ⚡ 1 FILE — anni content ikkade (`frontend/src/lib/site-config.ts`)

Ee file lo marchi → `npm run build` → anthe. Header, Footer, Home, CTA anni ikkada nunchi chaduvutayi.

```ts
export const SITE_CONFIG = {
  brandName: "Mana Vivaha",          // ← site peru
  legalName: "TSAP Matrimony",       // ← legal/brand peru
  logoText: "MV",                    // ← logo square lo text
  tagline: "TS-AP No.1 Telugu Matrimony",
  taglineTelugu: "₹99 ke Sambandham • Modati 3 FREE",
  domain: "manavivaha.in",

  botUsername: "@telugumatrimony1_bot",
  botUrl: "https://t.me/telugumatrimony1_bot",
  supportWhatsapp: "919848012345",   // ← mee customer care number
  supportEmail: "care@manavivaha.in",

  pricing: { trial: 99, premium: 299, bureauMonthly: 999, freeCredits: 3, referralPerPay: 50 },

  features: {                        // ← section ON/OFF switches
    showTestimonials: true,   // reviews ready ayyaka demo tag teesey
    showFaq: true,
    showPricing: true,
    showReferral: true,
    showBureau: true,
    showStickyCta: true,      // mobile bottom bar
    autoPostOnRegister: true,
  },

  trustPoints: ["OTP + DOB verified", "Photo-private mode",
                "Number pay tarvata matrame", "Watermark + fraud alerts"],
};
```

**Em marchali → ekkada:**

| Enti kavali | File | Chamges |
|---|---|---|
| Site peru / tagline | `frontend/src/lib/site-config.ts` | `brandName`, `tagline` |
| Bot username / link | `site-config.ts` | `botUsername`, `botUrl` |
| Support number / email | `site-config.ts` | `supportWhatsapp`, `supportEmail` |
| Prices (₹99/₹299/₹999) | `site-config.ts` | `pricing` |
| FAQ on/off, testimonials on/off | `site-config.ts` | `features` |
| Trust badges text | `site-config.ts` | `trustPoints` |
| Home page lo plan list | `frontend/src/app/page.tsx` | `PLANS` array |
| FAQ questions/answers | `frontend/src/app/page.tsx` | `FAQS` array |
| Testimonials text | `frontend/src/app/page.tsx` | `TESTIMONIALS` array |
| Nav menu items | `frontend/src/components/SiteHeader.tsx` | `NAV` array |
| Footer links | `frontend/src/components/SiteFooter.tsx` | `cols` array |

---

## 2. 🎨 COLORS + FONTS (brand look)

Ee rendu files chalu — antha ikkade:

**A) `frontend/tailwind.config.ts`** — colors
```ts
colors: {
  maroon: { DEFAULT: "#7A0C2E", dark: "#5C0822", light: "#A0143A", soft: "#F9EDF1" },
  gold:   { DEFAULT: "#D4AF37", light: "#F0D68C", soft: "#FFF6DC", deep: "#B8912A" },
  cream:  { DEFAULT: "#FFF8E7", deep: "#F7EED8" },
  navy:   { DEFAULT: "#0F1F3C", light: "#1E3A5F" },
},
fontFamily: {
  sans: ["Poppins", ...],      // main font
  telugu: ["'Noto Sans Telugu'", ...],
},
```
**B) `frontend/src/app/globals.css`** — gradients + utilities
```css
:root { --maroon:#7A0C2E; --gold:#D4AF37; --cream:#FFF8E7; --navy:#0F1F3C; }
.maroon-gradient { background: linear-gradient(135deg, #7A0C2E 0%, #A0143A 100%); }
.gold-gradient   { background: linear-gradient(135deg, #D4AF37 0%, #FFD700 50%, #D4AF37 100%); }
```

**Colors marchina tarvata:** `npm run build` → hard refresh (Ctrl+Shift+R).

**Fonts marchali ante:** `globals.css` lo `@import url('https://fonts.googleapis.com/...')` line marchi, `tailwind.config.ts` lo `fontFamily` update chey.

---

## 3. 🧩 Ee components already ready — malli rayakku, reuse chey

| Component | Path | Enti chestundi |
|---|---|---|
| `SiteHeader` | `components/SiteHeader.tsx` | Sticky glass header + mobile menu + active link highlight |
| `SiteFooter` | `components/SiteFooter.tsx` | Navy footer — Explore / Earn / Trust columns |
| `StickyCTA` | `components/StickyCTA.tsx` | Mobile bottom bar (Register + Bot), /register lo hide |
| `Reveal` | `components/Reveal.tsx` | Scroll-reveal animation wrapper: `<Reveal delay={100}>...</Reveal>` |
| `SectionHeading` | `components/SectionHeading.tsx` | Eyebrow + title + subtitle + action link |
| Channel data | `lib/channels.ts` | **AUTO-GENERATED** (65 channels) — edit cheyyaku, registry marchi run chey |
| Site config | `lib/site-config.ts` | Brand/pricing/features — ikkada customize chey |

**CSS utility classes (globals.css):** `card-shadow`, `card-shadow-lg`, `maroon-gradient`, `gold-gradient`,
`navy-gradient`, `cream-gradient`, `text-gradient-gold`, `glass`, `hover-lift`, `focus-brand`,
`dotted-bg`, `field`, `reveal`, `faq-body`, `ticker-track`, `scrollbar-hide`.

---

## 4. 📢 CHANNELS (65) marchali ante

**Source of truth:** `backend/channels_config.py` — channel peru, username, description, wave, hashtags.
Edit chesaka:
```bash
python3 backend/gen_frontend_channels.py   # → frontend/src/lib/channels.ts (website data)
python3 backend/gen_master_list.py         # → CHANNELS-MASTER-LIST-TELUGU.md (docs)
cd frontend && npm run build
```
⚠️ `frontend/src/lib/channels.ts` ni **direct ga edit cheyyaku** — next generation lo poyi untundi.

---

## 5. 🧪 MARCHINA TARUVATA — VERIFY (mistakes lekunda)

```bash
cd ~/matrimony-site/frontend

npx tsc --noEmit        # 1. TypeScript errors check (0 errors ravali)
npm run build           # 2. Build — "✓ Generating static pages (14/14)" + "Compiled successfully"

cd ~/matrimony-site
python3 backend/test_channels_router.py    # 3. Channels: 57/57 pass

# 4. Server live unte — anni routes check
for p in / /register /channels /matches /referral /bureau /sitemap.xml /robots.txt; do
  printf "%-16s " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:3000$p"
done
```
**Anni 200 ravali. 404/500 vaste aagu — logs chudu:**
```bash
sudo docker logs matrimony-site_frontend_1 --tail 50
sudo docker logs matrimony-site_backend_1 --tail 50
```

---

## 6. 🖼️ LOGO / IMAGES (next step)

Ippudu logo = gold square lo `MV` text. Real logo image kavali ante:
1. `frontend/public/logo.png` (square, 512×512) pettu
2. `SiteHeader.tsx` lo `{SITE_CONFIG.logoText}` ni `<img src="/logo.png" alt="Mana Vivaha" className="w-10 h-10 rounded-xl" />` ga marchu
3. Same for `SiteFooter.tsx`

Home page hero lo profile card mock ki real photo kavali ante: `frontend/public/demo-bride.jpg` petti,
`page.tsx` lo `LR` div ni `<img src="/demo-bride.jpg" ... />` ga marchu.

---

## 7. 🚀 DEPLOY (marchina tarvata server lo)

```bash
cd ~/matrimony-site
git pull                                     # nenu chesina commits
python3 backend/gen_frontend_channels.py     # registry → website sync
export COMPOSE_HTTP_TIMEOUT=300
sudo -E docker-compose up -d --build frontend backend bot
sudo docker ps
curl -s localhost:3000 | head -c 200
```

---

## 8. ❓ Common questions

**Q: Language toggle (తెలుగు/English) kavali?**
A: `site-config.ts` lo rendu versions pettukoni toggle cheyyali — cheppu, add chestha (i18n setup).

**Q: Dark mode kavali?**
A: `globals.css` lo `@media (prefers-color-scheme: dark)` block + tailwind `darkMode: 'class'` — cheppu, add chestha.

**Q: Kotha page kavali (success stories / safety / plans)?**
A: `frontend/src/app/<page-name>/page.tsx` create chey — Header/Footer automatic vasthayi (layout lo unnayi).
`SectionHeading` + `Reveal` vadukoni same look maintain chey.

**Q: Build fail ayyindi!**
A: 99% cases: (1) `@import` line ni CSS lo **paina** pettu, (2) `useSearchParams` unte **Suspense** wrapper pettu
(Next.js 14 requirement), (3) telugu text lo `"` unte `&quot;` leda es-lint off chey (`next.config.mjs` lo already off).

---

**Mana Vivaha — customize cheyyadam chala easy: okka config file + colors. Mistakes raakunda verification steps 5 unnayi (paina).** ✅
