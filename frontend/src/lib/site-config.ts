/**
 * MANA VIVAHA — SITE CONFIG (single place to customize everything)
 * ================================================================
 * Brand name, taglines, bot link, support numbers, prices, toggles —
 * anni ikkade marchandi. Header/Footer/CTA/Home anni ikkada nunchi chaduvutayi.
 *
 * Colors marchali ante: tailwind.config.ts (brand tokens) + src/app/globals.css (gradients).
 */

export const SITE_CONFIG = {
  // ---------- Brand ----------
  brandName: "Mana Vivaha",
  legalName: "TSAP Matrimony",
  logoText: "MV",
  tagline: "TS-AP No.1 Telugu Matrimony",
  taglineTelugu: "₹99 ke Sambandham • Modati 3 FREE • Chatting ledu",
  domain: "manavivaha.in",
  siteUrl: process.env.SITE_URL || "https://manavivaha.in",
  established: 2025,

  // ---------- Contact / channels ----------
  botUsername: "@telugumatrimony1_bot",
  botUrl: "https://t.me/telugumatrimony1_bot",
  supportWhatsapp: "919848012345", // +91 98480 12345 (change)
  supportPhone: "+91 98480 12345",
  supportEmail: "care@manavivaha.in",

  // ---------- Social (optional, empty = hide) ----------
  social: {
    telegramChannel: "https://t.me/TSBRIDE",
    youtube: "",
    instagram: "",
    facebook: "",
  },

  // ---------- Pricing (home page lo chupisthundi) ----------
  pricing: {                       // 1 credit = 1 profile (interest request)
    currency: "₹",
    trial: 99,                     // ₹99 → 3 profiles
    family: 199,                   // ₹199 → 10 profiles
    premium: 299,                  // ₹299 → 20 profiles
    bureauMonthly: 999,
    freeCredits: 3,                // modati 3 interest requests FREE
    referralPerPay: 50,            // referrer ki ₹50
    bundles: [
      { price: 99, profiles: 3, label: "Sambandham" },
      { price: 199, profiles: 10, label: "Family" },
      { price: 299, profiles: 20, label: "Premium" },
    ],
  },
  model: {
    chatting: false,               // 🚫 chatting ledu — consent-based requests
    interestCreditCost: 1,
    refundOnDecline: true,
  },

  // ---------- Feature toggles ----------
  features: {
    showTestimonials: true,     // real reviews vachaka demo tag teesesi ON unchu
    showFaq: true,
    showPricing: true,
    showReferral: true,
    showBureau: true,
    showTicker: true,
    showStickyCta: true,        // mobile bottom bar
    showIdSearch: true,         // hero lo ID search box
    photoPrivateDefault: false,
    autoPostOnRegister: true,
  },

  // ---------- Trust points (home hero lo) ----------
  trustPoints: [
    "OTP + DOB verified",
    "Photo-private mode",
    "Number pay tarvata matrame",
    "Watermark + fraud alerts",
  ],

  // ---------- Legal / compliance ----------
  legal: {
    refundPolicy: "7 days — pay ayyaka profile work avvakapoyina full refund",
    privacyNote: "Mee number evariki share cheyyamu. Data India lo store avutundi.",
    grievanceOfficer: "Charana Pendota, care@manavivaha.in",
  },
} as const;

export type SiteConfig = typeof SITE_CONFIG;
