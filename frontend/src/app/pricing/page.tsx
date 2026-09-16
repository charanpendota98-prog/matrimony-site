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
import { Duo, duo } from "@/lib/duo";

type Plan = {
  code: string; price: number; profiles: number; label: string; telugu: string;
  badge?: string; per_profile?: number; perks?: string[]; validity_days?: number;
};
type Addon = { code: string; price: number; label: string; telugu: string };

const FALLBACK_PLANS: Plan[] = [
  { code: "FREE", price: 0, profiles: 3, label: "Free Start", telugu: "Modati 3 requests FREE", badge: "No card needed", perks: ["3 interest requests", "WhatsApp lo mee profile share", "Anni channels ki auto-post"] },
  { code: "S_29", price: 29, profiles: 1, label: "Okka Request", telugu: "₹29 → 1 profile", badge: "Single • ₹29/profile", per_profile: 29, perks: ["1 interest request", "WhatsApp lo share + card", "Decline aithe refund"] },
  { code: "S_99", price: 99, profiles: 5, label: "Sambandham", telugu: "₹99 → 5 profiles", badge: "Entry • ₹20/profile", per_profile: 20, perks: ["5 interest requests", "⚡ 7-day profile boost", "Decline aithe refund"] },
  { code: "S_199", price: 199, profiles: 12, label: "Family", telugu: "₹199 → 12 profiles", badge: "Most popular • ₹16.6/profile", per_profile: 17, perks: ["12 interest requests", "✅ Photo-verified badge", "⭐ 1 porutham report", "Family bureau assist"] },
  { code: "S_299", price: 299, profiles: 25, label: "Premium", telugu: "₹299 → 25 profiles", badge: "Best value • ₹12/profile", per_profile: 12, perks: ["25 interest requests", "⚡ 30-day boost", "✅ Verified badge", "👀 Who-viewed 60 days", "Telugu support"] },
  { code: "S_499", price: 499, profiles: 50, label: "Vivaha VIP", telugu: "₹499 → 50 profiles", badge: "VIP • ₹10/profile", per_profile: 10, perks: ["50 interest requests", "🎯 Matchmaker assist", "⚡ 90-day boost", "💍 Vendor discounts", "Priority support"] },
];

const FALLBACK_ADDONS: Addon[] = [
  { code: "BOOST_49", price: 49, label: "Profile Boost (7 days)", telugu: "Mee card 7 days channel top lo — 3× views" },
  { code: "WHOVIEWED_49", price: 49, label: "Who viewed me (30 days)", telugu: "Mee profile ni evaru chusaru — names tho" },
  { code: "PORUTHAM_99", price: 99, label: "10-Porutham report", telugu: "Full kundli match report (Telugu)" },
  { code: "VERIFY_199", price: 199, label: "Photo verification badge", telugu: "✅ Verified badge — 3× ekkuva acceptances" },
];

const FAQ: { q: string; a: string }[] = [
  { q: "₹99 ki exact ga emi vasthundi?", a: "5 interest requests (profiles) + 7 రోజుల profile boost. ⚡ Ee boost valla mee card channel top lo kanipisthundi — 3× ekkuva views vastayi." },
  { q: "\"Profile request\" ante emiti? Chatting ledha?", a: "Chatting ledu (mee istam). Request ante — meeru నచ్చిన profile ki interest pampistham, vaalla daggara mee profile + WhatsApp చేరుతుంది. Vaallu OK అంటే numbers exchange avutayi (rendu vaipula oppuka tarvate)." },
  { q: "Free ga emi vastundi?", a: "3 interest requests FREE — card pettalsina avasaram ledu. Adi aipoyaka mee istam — ₹29 tho okka request try cheyyachu, leda ₹99 bundle." },
  { q: "Decline aithe naa dabbu poyinda?", a: "Ledu — evaru respond avvakapote leda decline chesthe, aa request ki **credit malli refund** avutundi (policy lo clear ga undi)." },
  { q: "Number eppudu vasthundi?", a: "Rendu vaipula oppuka tarvata matrame. Mana team WhatsApp lo confirm chesi number share chestundi — privacy guaranteed." },
  { q: "Validity entha?", a: "₹29 → 15 రోజులు, ₹99 → 30, ₹199 → 45, ₹299 → 60, ₹499 → 90 రోజులు. Pata customer ki **renewal ₹99 → 8 profiles**." },
  { q: "Auto-renewal unda? Hidden charges?", a: "Ledu. Auto-renewal ledu, hidden charges ledu. Meere malli pay cheyyali anukunnappudu pay chestaru." },
  { q: "GST invoice kavali — ela?", a: "Payment tarvata support ki cheppandi (care@manavivaha.in leda WhatsApp) — 24 గంటల్లో GST invoice pampistham." },
];

const PAY_METHODS = ["UPI (GPay / PhonePe / Paytm)", "Debit / Credit Card", "Net Banking", "Razorpay secure checkout"];

export default function PricingPage() {
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
          💰 {duo("Transparent Pricing • No hidden charges • No auto-renewal", "పారదర్శక ధరలు • దాచిన ఛార్జీలు లేవు")}
        </div>
        <h1 className="mt-3 text-3xl md:text-4xl font-extrabold text-[#7A0C2E] telugu">
          <Duo en="₹99 ke Sambandham — first 3 requests" te="మొదటి 3 రిక్వెస్టులు" /> <span className="text-[#B8860B]">FREE</span>
        </h1>
        <p className="mt-2 text-sm text-gray-600 telugu max-w-3xl mx-auto">
          Register <b>100% FREE</b> → <b>3 profiles</b> chudochu + <b>3 interests</b> pampochu. Kani{" "}
          <b className="text-[#7A0C2E]">🔒 phone numbers ivvamu</b> — interest pampi vaallu <b>accept</b> cheste matrame
          rendu vaipula numbers share avutayi (chatting ledu). 3 FREE taruvata ₹99 → 5 profiles + boost.
        </p>
        {/* 🆓 FREE vs PAID — crystal clear */}
        <div className="mt-4 grid sm:grid-cols-2 gap-3 text-left max-w-3xl mx-auto">
          <div className="rounded-2xl bg-emerald-50 border border-emerald-200 p-3 text-xs text-emerald-900">
            <div className="font-bold">✅ FREE లో (₹0)</div>
            <ul className="mt-1 space-y-0.5">
              <li>• 3 profiles full details + card</li>
              <li>• 3 interests (WhatsApp lo mee profile share)</li>
              <li>• Accept ayithe numbers exchange</li>
            </ul>
          </div>
          <div className="rounded-2xl bg-rose-50 border border-rose-200 p-3 text-xs text-rose-900">
            <div className="font-bold">🔒 FREE లో ఇవ్వనిది</div>
            <ul className="mt-1 space-y-0.5">
              <li>• Phone numbers (locked — 98••••••45 matrame)</li>
              <li>• Chatting (ledu — requests matrame)</li>
              <li>• 3 taruvata: ₹99 → 5 · ₹199 → 12 · ₹299 → 25 · ₹499 → 50</li>
            </ul>
          </div>
        </div>
        <div className="mt-3 text-[11px] text-gray-500 telugu">
          🔐 Mee number DB lo encrypt ga untundi · consent tho matrame share · decline ayithe credit refund (loss ledu)
        </div>
        {live && <div className="mt-2 text-[11px] text-green-700">✅ Live pricing (server nunchi)</div>}
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
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu">📦 <Duo en="Plans — as per your budget" te="మీ బడ్జెట్‌ను బట్టి" /></h2>
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
                <div className="mt-1 text-sm telugu text-gray-700">{p.telugu}</div>
                <div className="mt-2 flex items-center gap-2 text-[11px] text-gray-500">
                  <span className="px-2 py-0.5 rounded-full bg-gray-100">{p.badge}</span>
                  {p.validity_days && <span>{p.validity_days} రోజుల validity</span>}
                </div>
                <ul className="mt-3 space-y-1.5 text-xs text-gray-700">
                  {(p.perks || []).map((k) => <li key={k} className="telugu">✅ {k}</li>)}
                </ul>
                {p.price === 0 ? (
                  <Link href="/register"
                    className="mt-4 block text-center rounded-xl py-2.5 font-bold text-sm bg-gray-100 text-[#7A0C2E]">
                    Free ga start cheyyandi
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
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu mb-3">📊 <Duo en="Compare — why ₹299/₹499 is best" te="ఎందుకు బెస్ట్" /></h2>
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
              ["Auto-post (amma channels)", "✅", ...paid.map(() => "✅")],
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
          <div className="font-bold text-[#7A0C2E] telugu">🎁 Add-ons (plan lekunda kooda)</div>
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
          <div className="font-bold text-[#7A0C2E] telugu">🔁 Renewal bonus (pata customers ki)</div>
          <div className="mt-3 text-sm telugu">
            ₹{renewal.price} → <b>{renewal.profiles} profiles</b> + 7-day boost free.
            <div className="text-xs text-gray-600 mt-1">(₹{(renewal.price / renewal.profiles).toFixed(1)}/profile — modati sari kanna ekkuva value)</div>
          </div>
          <Link href="/requests#renew" className="mt-3 inline-block text-xs font-bold text-[#7A0C2E] underline">Renewal teesukondi →</Link>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="font-bold text-[#7A0C2E] telugu">🤝 Referral — ₹{SITE_CONFIG.pricing.referralPerPay}/profile</div>
          <div className="mt-3 text-xs telugu text-gray-700">
            Mee friend register ayi pay chesthe — meeku <b>₹{SITE_CONFIG.pricing.referralPerPay}</b> (UPI lo direct leda credits lo).
            Bureau/brokers ki B2B plans kooda unnai.
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
          <div className="font-bold">💳 <Duo en="Payment & security" te="చెల్లింపు & భద్రత" /></div>
          <ul className="mt-3 space-y-1.5 text-xs opacity-90">
            {PAY_METHODS.map((m) => <li key={m}>✅ {m}</li>)}
            <li>✅ Razorpay secure checkout (PCI-DSS)</li>
            <li>✅ GST invoice (request chesina 24h lo)</li>
            <li>✅ Auto-renewal ledu • Hidden charges ledu</li>
          </ul>
          <div className="mt-3 text-[11px] opacity-75">
            Support: {SITE_CONFIG.supportPhoneDisplay} • {SITE_CONFIG.supportEmail}
          </div>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-5">
          <div className="font-bold text-[#7A0C2E]">📜 Policies (tap chesi chaduvandi)</div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
            <Link href="/refund" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">💸 Refund & Cancellation</Link>
            <Link href="/terms" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">📄 Terms of Use</Link>
            <Link href="/privacy" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">🔒 Privacy Policy</Link>
            <Link href="/safety" className="rounded-xl border border-gray-200 p-3 hover:border-[#7A0C2E]">🛡️ Trust & Safety</Link>
          </div>
          <div className="mt-3 text-[11px] text-gray-500 telugu">
            ⚠️ Advance money adigedi evaru unna — 100% mosam. Ventane /safety lo report cheyyandi.
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="mt-10">
        <h2 className="text-xl font-bold text-[#7A0C2E] telugu">❓ <Duo en="FAQ — questions everyone asks" te="అందరూ అడిగే ప్రశ్నలు" /></h2>
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
          Modati 3 requests FREE — ippude start cheyyandi 🙏
        </div>
        <div className="text-xs text-[#7A0C2E]/80 telugu mt-1">Card details avasaram ledu • 3 నిమిషాల్లో register</div>
        <div className="mt-4 flex flex-wrap gap-3 justify-center">
          <Link href="/register" className="rounded-xl bg-[#7A0C2E] text-white px-5 py-2.5 font-bold text-sm">Register FREE →</Link>
          <Link href="/channels" className="rounded-xl bg-white/70 text-[#7A0C2E] px-5 py-2.5 font-bold text-sm border border-[#7A0C2E]/20">52 Channels chudandi</Link>
          <a href={SITE_CONFIG.supportLink} className="rounded-xl bg-white/70 text-[#7A0C2E] px-5 py-2.5 font-bold text-sm border border-[#7A0C2E]/20">WhatsApp lo adagandi</a>
        </div>
      </section>

      {best && (
        <div className="mt-4 text-center text-[11px] text-gray-500 telugu">
          ₹{best.price} plan lo profile ki ₹{best.per_profile || Math.round(best.price / best.profiles)} matrame — 52 channels + WhatsApp share + matchmaker assist.
        </div>
      )}
    </main>
  );
}
