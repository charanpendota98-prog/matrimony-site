"use client";
/**
 * 💰 PRICING — Mana Vivaha (Telugu-first, transparent)
 * ---------------------------------------------------
 * Okka chota anni: plans • add-ons • renewal • bureau • payment • refund • FAQ.
 * Data: GET /api/plans (backend interest.py PLANS — single source of truth)
 *       API fail ayithe SITE_CONFIG fallback (page khali ga kanipinchadu).
 */
import { useEffect, useState } from "react";
import Link from "next/link";
import { SITE_CONFIG } from "@/lib/site-config";
import PayBox from "@/components/PayBox";
import OffersBanner from "@/components/OffersBanner";
import BannerSlot from "@/components/BannerSlot";
import { CHANNEL_STATS } from "@/lib/channels";
import { useLang } from "@/lib/lang";

type Plan = {
  code: string; price: number; profiles: number; label: string; telugu: string;
  badge?: string; per_profile?: number; perks?: string[]; perksTe?: string[]; validity_days?: number;
};
type Addon = { code: string; price: number; label: string; telugu: string };

const FALLBACK_PLANS: Plan[] = [
  { code: "FREE", price: 0, profiles: 3, label: "Free Start", telugu: "మొదటి 3 requests FREE", badge: "No card needed", perks: ["3 interest requests", "Your profile shared on WhatsApp", "Auto-post to all channels"], perksTe: ["3 interest requests", "మీ profile WhatsApp లో share", "అన్ని channels కి auto-post"] },
  { code: "S_29", price: 29, profiles: 1, label: "Single Request", telugu: "₹29 → 1 profile", badge: "Single • ₹29/profile", per_profile: 29, perks: ["1 interest request", "Share on WhatsApp + card", "Refund on decline"], perksTe: ["1 interest request", "WhatsApp లో share + card", "Decline అయితే refund"] },
  { code: "S_99", price: 99, profiles: 5, label: "Sambandham", telugu: "₹99 → 5 profiles", badge: "Entry • ₹20/profile", per_profile: 20, perks: ["5 interest requests", "⚡ 7-day profile boost", "Refund on decline"], perksTe: ["5 interest requests", "⚡ 7-day profile boost", "Decline అయితే refund"] },
  { code: "S_199", price: 199, profiles: 12, label: "Family", telugu: "₹199 → 12 profiles", badge: "Most popular • ₹16.6/profile", per_profile: 17, perks: ["12 interest requests", "✅ Photo-verified badge", "⭐ 1 porutham report", "Family bureau assist"] },
  { code: "S_299", price: 299, profiles: 25, label: "Premium", telugu: "₹299 → 25 profiles", badge: "Best value • ₹12/profile", per_profile: 12, perks: ["25 interest requests", "⚡ 30-day boost", "✅ Verified badge", "👀 Who-viewed 60 days", "Telugu support"] },
  { code: "S_499", price: 499, profiles: 50, label: "Vivaha VIP", telugu: "₹499 → 50 profiles", badge: "VIP • ₹10/profile", per_profile: 10, perks: ["50 interest requests", "🎯 Matchmaker assist", "⚡ 90-day boost", "💍 Vendor discounts", "Priority support"] },
];

const FALLBACK_ADDONS: Addon[] = [
  { code: "BOOST_49", price: 49, label: "Profile Boost (7 days)", telugu: "మీ card 7 days channel top లో — 3× views" },
  { code: "WHOVIEWED_49", price: 49, label: "Who viewed me (30 days)", telugu: "మీ profile ని ఎవరు చూశారు — names తో" },
  { code: "PORUTHAM_99", price: 99, label: "10-Porutham report", telugu: "Full kundli match report (Telugu)" },
  { code: "VERIFY_199", price: 199, label: "Photo verification badge", telugu: "✅ Verified badge — 3× ఎక్కువ acceptances" },
];

const FAQ_TE: { q: string; a: string }[] = [
  { q: "₹99 కి exact గా ఏమి వస్తుంది?", a: "5 interest requests (profiles) + 7 రోజుల profile boost. ⚡ ఈ boost వల్ల మీ card channel top లో కనిపిస్తుంది — 3× ఎక్కువ views వస్తాయి." },
  { q: "\"Profile request\" అంటే ఏమిటి? Chatting లేదా?", a: "Chatting లేదు (మీ ఇష్టం). Request అంటే — మీకు నచ్చిన profile కి interest పంపిస్తాం, వాళ్ల దగ్గరకు మీ profile + WhatsApp చేరుతుంది. వాళ్లు OK అంటే numbers exchange అవుతాయి (రెండు వైపులా ఒప్పుకున్న తర్వాత)." },
  { q: "Free గా ఏమి వస్తుంది?", a: "3 interest requests FREE — card పెట్టాల్సిన అవసరం లేదు. అది అయిపోయాక మీ ఇష్టం — ₹29 తో ఒక్క request try చెయ్యచ్చు, లేదా ₹99 bundle." },
  { q: "Decline అయితే నా డబ్బు పోయిందా?", a: "లేదు — ఎవరూ respond అవ్వకపోతే లేదా decline చేస్తే, ఆ request కి credit మళ్లీ refund అవుతుంది (policy లో clear గా ఉంది)." },
  { q: "Number ఎప్పుడు వస్తుంది?", a: "రెండు వైపులా ఒప్పుకున్న తర్వాతే. మన team WhatsApp లో confirm చేసి number share చేస్తుంది — privacy guaranteed." },
  { q: "Validity ఎంత?", a: "₹29 → 15 రోజులు, ₹99 → 30, ₹199 → 45, ₹299 → 60, ₹499 → 90 రోజులు. పాత customer కి renewal ₹99 → 8 profiles." },
  { q: "Auto-renewal ఉందా? Hidden charges?", a: "లేదు. Auto-renewal లేదు, hidden charges లేవు. మీరే మళ్లీ pay చెయ్యాలి అనుకున్నప్పుడు pay చేస్తారు." },
  { q: "GST invoice కావాలి — ఎలా?", a: "Payment తర్వాత support కి చెప్పండి (care@manavivaha.in లేదా WhatsApp) — 24 గంటల్లో GST invoice పంపిస్తాం." },
];
const FAQ_EN: { q: string; a: string }[] = [
  { q: "What exactly do I get for ₹99?", a: "5 interest requests (profiles) + 7-day profile boost. ⚡ The boost keeps your card at channel top — 3× more views." },
  { q: "What is a \"profile request\"? No chatting?", a: "No chatting (your choice). A request means — we send interest to a profile you like; your profile + WhatsApp reaches them. If they say OK, numbers exchange (only after both sides agree)." },
  { q: "What is free?", a: "3 interest requests FREE — no card needed. After that, your choice — try one request for ₹29, or the ₹99 bundle." },
  { q: "If declined, is my money gone?", a: "No — if nobody responds or they decline, the credit for that request is refunded (clearly stated in policy)." },
  { q: "When do I get the number?", a: "Only after both sides agree. Our team confirms on WhatsApp and shares the number — privacy guaranteed." },
  { q: "How long is validity?", a: "₹29 → 15 days, ₹99 → 30, ₹199 → 45, ₹299 → 60, ₹499 → 90 days. Existing customers get renewal ₹99 → 8 profiles." },
  { q: "Auto-renewal? Hidden charges?", a: "None. No auto-renewal, no hidden charges. You pay again only when you want to." },
  { q: "How do I get a GST invoice?", a: "Tell support after payment (care@manavivaha.in or WhatsApp) — GST invoice within 24 hours." },
];
const PAY_METHODS = ["UPI (GPay / PhonePe / Paytm)", "Debit / Credit Card", "Net Banking", "Razorpay secure checkout"];

export default function PricingPage() {
  const { lang } = useLang();
  const te = lang === "te";
  const FAQ = te ? FAQ_TE : FAQ_EN;
  const [plans, setPlans] = useState<Plan[]>(FALLBACK_PLANS);
  const [addons, setAddons] = useState<Addon[]>(FALLBACK_ADDONS);
  const [renewal, setRenewal] = useState<{ price: number; profiles: number; label: string }>(SITE_CONFIG.pricing.renewal);
  const [bureau, setBureau] = useState<Plan[]>([]);
  const [live, setLive] = useState(false);

  useEffect(() => {
    fetch("/api/plans")
      .then((r) => r.json())
      .then((d) => {
        if (Array.isArray(d.plans) && d.plans.length) {
          setPlans([d.plans[0], ...d.plans.filter((p: Plan) => p.price > 0)]);
          setLive(true);
        }
        if (Array.isArray(d.addons) && d.addons.length) setAddons(d.addons);
        if (d.renewal) setRenewal(d.renewal);
        if (Array.isArray(d.bureau)) setBureau(d.bureau);
      })
      .catch(() => { });
  }, []);

  const paid = plans.filter((p) => p.price > 0);
  const free = plans.find((p) => p.price === 0) || FALLBACK_PLANS[0];
  const best = paid.find((p) => p.code === "S_499");

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      {/* HERO */}
      <div className="text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#7A0C2E]/10 text-[#7A0C2E] text-xs font-bold">
          💰 {te ? "పారదర్శక ధరలు • దాచిన ఛార్జీలు లేవు • ఆటో-రెన్యూవల్ లేదు" : "Transparent Pricing • No hidden charges • No auto-renewal"}
        </div>
        <h1 className="mt-3 text-3xl md:text-4xl font-extrabold text-[#7A0C2E] telugu">
          {te ? "మొదటి 3 రిక్వెస్టులు" : "₹99 Sambandham — first 3 requests"} <span className="text-[#B8860B]">FREE</span>
        </h1>
        <p className="mt-2 text-sm text-gray-600 telugu max-w-3xl mx-auto">
          {te ? <>Register <b>100% FREE</b> → <b>3 profiles</b> చూడొచ్చు + <b>3 interests</b> పంపొచ్చు. కానీ{" "}
          <b className="text-[#7A0C2E]">🔒 phone numbers ఇవ్వము</b> — interest పంపి వాళ్లు <b>accept</b> చేస్తే మాత్రమే
          రెండు వైపులా numbers share అవుతాయి (chatting లేదు). 3 FREE తర్వాత ₹99 → 5 profiles + boost.</>
          : <>Register <b>100% FREE</b> → see <b>3 profiles</b> + send <b>3 interests</b>. But{" "}
          <b className="text-[#7A0C2E]">🔒 we never give phone numbers</b> — only after you send interest and they
          <b>accept</b> are numbers shared both sides (no chatting). After 3 FREE: ₹99 → 5 profiles + boost.</>}
        </p>
        {/* 🆓 FREE vs PAID — crystal clear */}
        <div className="mt-4 grid sm:grid-cols-2 gap-3 text-left max-w-3xl mx-auto">
          <div className="rounded-2xl bg-emerald-50 border border-emerald-200 p-3 text-xs text-emerald-900">
            <div className="font-bold">{te ? "✅ FREE లో (₹0)" : "✅ In FREE (₹0)"}</div>
            <ul className="mt-1 space-y-0.5">
              <li>• 3 profiles full details + card</li>
              <li>{te ? "• 3 interests (WhatsApp లో మీ profile share)" : "• 3 interests (your profile shared on WhatsApp)"}</li>
              <li>{te ? "• Accept అయితే numbers exchange" : "• Numbers exchange on accept"}</li>
            </ul>
          </div>
          <div className="rounded-2xl bg-rose-50 border border-rose-200 p-3 text-xs text-rose-900">
            <div className="font-bold">{te ? "🔒 FREE లో ఇవ్వనిది" : "🔒 Not included in FREE"}</div>
            <ul className="mt-1 space-y-0.5">
              <li>{te ? "• Phone numbers (locked — 98••••••45 మాత్రమే)" : "• Phone numbers (locked — only 98••••••45)"}</li>
              <li>{te ? "• Chatting (లేదు — requests మాత్రమే)" : "• Chatting (none — requests only)"}</li>
              <li>• 3 taruvata: ₹99 → 5 · ₹199 → 12 · ₹299 → 25 · ₹499 → 50</li>
            </ul>
          </div>
        </div>
        <div className="mt-3 text-[11px] text-gray-500 telugu">
          {te ? "🔐 మీ number DB లో encrypt గా ఉంటుంది · consent తోనే share · decline అయితే credit refund (loss లేదు)" : "🔐 Your number stays encrypted in DB · shared only with consent · credit refund on decline (no loss)"}
        </div>
        {live && <div className="mt-2 text-[11px] text-green-700">{te ? "✅ Live pricing (server నుంచి)" : "✅ Live pricing (from server)"}</div>}
      </div>
      <div className="mt-4"><OffersBanner /></div>
      <div className="mt-3"><BannerSlot page="pricing" /></div>

      {/* VALUE LADDER STRIP */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-2 text-center text-xs">
        {paid.map((p) => (
          <div key={p.code} className="rounded-xl bg-white border border-gray-200 p-3 shadow-sm">
            <div className="font-extrabold text-[#7A0C2E] text-lg">₹{p.price}</div>
            <div className="text-gray-600">{p.profiles} profiles</div>
            <div className="text-[10px] text-gray-400">₹{p.per_profile || Math.round(p.price / p.profiles)}/profile</div>
          </div>
        ))}
        <div className="rounded-xl bg-green-50 border border-green-200 p-3">
          <div className="font-extrabold text-green-700 text-lg">FREE</div>
          <div className="text-green-700">{free.profiles} profiles</div>
          <div className="text-[10px] text-green-600">first time</div>
        </div>
      </div>

      {/* PLAN CARDS */}
      <section className="mt-8">
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu">📦 {te ? "మీ బడ్జెట్‌ను బట్టి ప్లాన్లు" : "Plans — as per your budget"}</h2>
        <div className="mt-4 grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[free, ...paid].map((p) => {
            const isPopular = p.code === "S_199";
            const isBest = p.code === "S_299";
            return (
              <div key={p.code}
                className={`rounded-2xl border p-5 bg-white shadow-sm relative ${isPopular ? "border-[#B8860B] ring-2 ring-[#B8860B]/30" : isBest ? "border-[#7A0C2E]" : "border-gray-200"}`}>
                {(isPopular || isBest) && (
                  <div className="absolute -top-3 left-4 px-2 py-0.5 rounded-full text-[10px] font-bold text-white"
                    style={{ background: isPopular ? "#B8860B" : "#7A0C2E" }}>
                    {isPopular ? "⭐ MOST POPULAR" : "🏆 BEST VALUE"}
                  </div>
                )}
                <div className="flex items-baseline justify-between">
                  <div className="font-bold text-[#7A0C2E] text-lg telugu">{p.label}</div>
                  <div className="text-2xl font-extrabold text-[#7A0C2E]">{p.price === 0 ? "FREE" : `₹${p.price}`}</div>
                </div>
                <div className="mt-1 text-sm telugu text-gray-700">{te ? p.telugu : `₹${p.price} → ${p.profiles} profiles`}</div>
                <div className="mt-2 flex items-center gap-2 text-[11px] text-gray-500">
                  <span className="px-2 py-0.5 rounded-full bg-gray-100">{p.badge}</span>
                  {p.validity_days && <span>{te ? `${p.validity_days} రోజుల validity` : `${p.validity_days}-day validity`}</span>}
                </div>
                <ul className="mt-3 space-y-1.5 text-xs text-gray-700">
                  {((te && p.perksTe ? p.perksTe : p.perks) || []).map((k) => <li key={k} className="telugu">✅ {k}</li>)}
                </ul>
                {p.price === 0 ? (
                  <Link href="/register"
                    className="mt-4 block text-center rounded-xl py-2.5 font-bold text-sm bg-gray-100 text-[#7A0C2E]">
                    {te ? "Free గా start చెయ్యండి" : "Start free"}
                  </Link>
                ) : (
                  <div className="mt-4"><PayBox planCode={p.code} price={p.price} label={p.label} /></div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* COMPARISON */}
      <section className="mt-10 overflow-x-auto">
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu mb-3">📊 {te ? "Compare — ఎందుకు బెస్ట్" : "Compare — why ₹299/₹499 is best"}</h2>
        <table className="w-full text-xs border-collapse bg-white rounded-xl overflow-hidden">
          <thead>
            <tr className="bg-[#7A0C2E] text-white">
              <th className="text-left p-2.5">Feature</th>
              <th className="p-2.5">FREE</th>
              {paid.map((p) => <th key={p.code} className="p-2.5">₹{p.price}</th>)}
            </tr>
          </thead>
          <tbody className="telugu">
            {[
              ["Interest requests", String(free.profiles), ...paid.map((p) => String(p.profiles))],
              ["₹/profile", "0", ...paid.map((p) => `₹${p.per_profile || Math.round(p.price / p.profiles)}`)],
              [te ? "Auto-post (anni channels)" : "Auto-post (all channels)", "✅", ...paid.map(() => "✅")],
              ["WhatsApp lo profile share", "✅", ...paid.map(() => "✅")],
              ["Profile boost (channel top)", "—", "7d", "—", "30d", "90d"],
              ["Verified badge", "—", "—", "✅", "✅", "✅"],
              ["Porutham report (10 items)", "—", "—", "1", "3", "Unlimited"],
              ["Who viewed me", "—", "—", "—", "60d", "90d"],
              ["Matchmaker assist (team call)", "—", "—", "—", "—", "✅"],
              ["Support", "WhatsApp", "WhatsApp", "Priority", "Priority", "Dedicated"],
            ].map((row, i) => (
              <tr key={i} className={i % 2 ? "bg-gray-50" : "bg-white"}>
                {row.map((c, j) => (
                  <td key={j} className={`p-2.5 ${j === 0 ? "text-left font-semibold text-gray-700" : "text-center text-gray-700"}`}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* ADD-ONS + RENEWAL + REFERRAL */}
      <section className="mt-10 grid md:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="font-bold text-[#7A0C2E] telugu">{te ? "🎁 Add-ons (plan లేకుండా కూడా)" : "🎁 Add-ons (even without a plan)"}</div>
          <ul className="mt-3 space-y-2 text-xs">
            {addons.map((a) => (
              <li key={a.code} className="flex items-start justify-between gap-2">
                <span className="telugu">{a.label}<span className="block text-gray-500">{a.telugu}</span></span>
                <span className="font-bold text-[#7A0C2E] whitespace-nowrap">₹{a.price}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-2xl border border-[#B8860B]/40 bg-[#FFF8E1] p-5">
          <div className="font-bold text-[#7A0C2E] telugu">{te ? "🔁 Renewal bonus (పాత customers కి)" : "🔁 Renewal bonus (for existing customers)"}</div>
          <div className="mt-3 text-sm telugu">
            ₹{renewal.price} → <b>{renewal.profiles} profiles</b> + 7-day boost free.
            <div className="text-xs text-gray-600 mt-1">{te ? `(₹${(renewal.price / renewal.profiles).toFixed(1)}/profile — మొదటి సారి కన్నా ఎక్కువ value)` : `(₹${(renewal.price / renewal.profiles).toFixed(1)}/profile — more value than first time)`}</div>
          </div>
          <Link href="/requests#renew" className="mt-3 inline-block text-xs font-bold text-[#7A0C2E] underline">{te ? "Renewal తీసుకోండి →" : "Get renewal →"}</Link>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="font-bold text-[#7A0C2E] telugu">🤝 Referral — ₹{SITE_CONFIG.pricing.referralPerPay}/profile</div>
          <div className="mt-3 text-xs telugu text-gray-700">
            {te ? <>మీ friend register అయి pay చేస్తే — మీకు <b>₹{SITE_CONFIG.pricing.referralPerPay}</b> (UPI లో direct లేదా credits లో). Bureau/brokers కి B2B plans కూడా ఉన్నాయి.</>
            : <>When your friend registers and pays — you get <b>₹{SITE_CONFIG.pricing.referralPerPay}</b> (direct to UPI or as credits). B2B plans available for bureaus/brokers.</>}
          </div>
          <div className="mt-3 flex gap-2">
            <Link href="/referral" className="text-xs font-bold text-[#7A0C2E] underline">Referral program →</Link>
            <Link href="/bureau" className="text-xs font-bold text-[#7A0C2E] underline">Bureau plans →</Link>
          </div>
        </div>
      </section>

      {/* BUREAU */}
      <section className="mt-10">
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu">🏢 Bureaus / Brokers / Agents (B2B)</h2>
        <div className="mt-3 grid md:grid-cols-2 gap-4">
          {(bureau.length ? bureau : [
            { code: "BUREAU_999", price: 999, profiles: 25, label: "Bureau Starter", telugu: "₹999 → 25 profiles (monthly)", perks: ["25 profiles", "Monthly report", "Bulk register"] },
            { code: "BUREAU_2999", price: 2999, profiles: 100, label: "Bureau Pro", telugu: "₹2999 → 100 profiles (monthly)", perks: ["100 profiles", "Agent dashboard", "Priority channel posting"] },
          ]).map((b) => (
            <div key={b.code} className="rounded-2xl border border-gray-200 bg-white p-5">
              <div className="flex items-baseline justify-between">
                <div className="font-bold text-[#7A0C2E]">{b.label}</div>
                <div className="text-xl font-extrabold text-[#7A0C2E]">₹{b.price}<span className="text-xs font-normal text-gray-500">/mo</span></div>
              </div>
              <div className="text-xs telugu text-gray-600 mt-1">{b.telugu}</div>
              <ul className="mt-2 text-xs text-gray-700 space-y-1">{(b.perks || []).map((k) => <li key={k}>✅ {k}</li>)}</ul>
            </div>
          ))}
        </div>
      </section>

      {/* PAYMENT + TRUST */}
      <section className="mt-10 grid md:grid-cols-2 gap-4">
        <div className="rounded-2xl bg-[#7A0C2E] text-white p-5">
          <div className="font-bold">💳 {te ? "చెల్లింపు & భద్రత" : "Payment & security"}</div>
          <ul className="mt-3 space-y-1.5 text-xs opacity-90">
            {PAY_METHODS.map((m) => <li key={m}>✅ {m}</li>)}
            <li>✅ Razorpay secure checkout (PCI-DSS)</li>
            <li>{te ? "✅ GST invoice (request చేసిన 24h లో)" : "✅ GST invoice (within 24h of request)"}</li>
            <li>{te ? "✅ Auto-renewal లేదు • Hidden charges లేవు" : "✅ No auto-renewal • No hidden charges"}</li>
          </ul>
          <div className="mt-3 text-[11px] opacity-75">
            Support: {SITE_CONFIG.supportPhoneDisplay} • {SITE_CONFIG.supportEmail}
          </div>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="font-bold text-[#7A0C2E]">{te ? "📜 Policies (tap చేసి చదవండి)" : "📜 Policies (tap to read)"}</div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
            <Link href="/refund" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">💸 Refund & Cancellation</Link>
            <Link href="/terms" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">📄 Terms of Use</Link>
            <Link href="/privacy" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">🔒 Privacy Policy</Link>
            <Link href="/safety" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">🛡️ Trust & Safety</Link>
          </div>
          <div className="mt-3 text-[11px] text-gray-500 telugu">
            {te ? "⚠️ Advance money అడిగేది ఎవరైనా — 100% మోసం. వెంటనే /safety లో report చెయ్యండి." : "⚠️ Anyone asking advance money is 100% fraud. Report immediately in /safety."}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="mt-10">
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu">❓ {te ? "అందరూ అడిగే ప్రశ్నలు" : "FAQ — questions everyone asks"}</h2>
        <div className="mt-3 space-y-2">
          {FAQ.map((f) => (
            <details key={f.q} className="rounded-xl border border-gray-200 bg-white p-4 open:shadow-sm">
              <summary className="cursor-pointer font-semibold text-sm text-[#7A0C2E] telugu">{f.q}</summary>
              <p className="mt-2 text-xs text-gray-700 telugu leading-relaxed">{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mt-10 rounded-3xl gold-gradient p-6 text-center">
        <div className="text-lg font-extrabold text-[#7A0C2E] telugu">
          {te ? "మొదటి 3 requests FREE — ఇప్పుడే start చెయ్యండి 🙏" : "First 3 requests FREE — start now 🙏"}
        </div>
        <div className="text-xs text-[#7A0C2E]/80 telugu mt-1">{te ? "Card details అవసరం లేదు • 3 నిమిషాల్లో register" : "No card details needed • register in 3 minutes"}</div>
        <div className="mt-4 flex flex-wrap gap-3 justify-center">
          <Link href="/register" className="rounded-xl bg-[#7A0C2E] text-white px-5 py-2.5 font-bold text-sm">Register FREE →</Link>
          <Link href="/channels" className="rounded-xl bg-white/70 text-[#7A0C2E] px-5 py-2.5 font-bold text-sm border border-[#7A0C2E]/20">{te ? `${CHANNEL_STATS.total} Channels చూడండి` : `See ${CHANNEL_STATS.total} channels`}</Link>
          <a href={SITE_CONFIG.supportLink} className="rounded-xl bg-white/70 text-[#7A0C2E] px-5 py-2.5 font-bold text-sm border border-[#7A0C2E]/20">{te ? "WhatsApp లో అడగండి" : "Ask on WhatsApp"}</a>
        </div>
      </section>

      {best && (
        <div className="mt-4 text-center text-[11px] text-gray-500 telugu">
{te ? <>₹{best.price} plan లో profile కి ₹{best.per_profile || Math.round(best.price / best.profiles)} మాత్రమే — {CHANNEL_STATS.total} channels + WhatsApp share + matchmaker assist.</> : <>Just ₹{best.per_profile || Math.round(best.price / best.profiles)} per profile on the ₹{best.price} plan — {CHANNEL_STATS.total} channels + WhatsApp share + matchmaker assist.</>}
        </div>
      )}
    </main>
  );
}
