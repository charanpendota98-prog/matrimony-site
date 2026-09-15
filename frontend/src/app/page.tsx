"use client";
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ALL_CHANNELS, CHANNEL_STATS, Channel } from "@/lib/channels";
import Reveal from "@/components/Reveal";
import SectionHeading from "@/components/SectionHeading";
import { SITE_CONFIG } from "@/lib/site-config";
import { apiGet } from "@/lib/api";

const BOT = SITE_CONFIG.botUrl;

const FAQS = [
  {
    q: "Register cheyyadaniki entha time, entha charge?",
    a: "5 steps — 3 nimushalu. Register 100% FREE. Modati 3 interest requests kooda FREE. Aa tarvata ₹99 tho 5 profiles, ₹199 tho 12, ₹299 tho 25, ₹499 tho 50 profiles (₹10–20/profile).",
  },
  {
    q: "Chatting unda? Ela matladukovali?",
    a: "Chatting ledu — anthe. Meeku nachhina profile ki \"💌 Interest Pampu\" (1 credit). Valla profile + mee details WhatsApp lo vallaki veltundi. Vaallu Accept chesthe rendu numbers automatic ga WhatsApp lo exchange avutayi — direct ga matladukovachu. Decline chesthe mee credit refund (mana trust policy).",
  },
  {
    q: "Number eppudu kanipisthundi? Direct ga isthara?",
    a: "Interest pampinappudu number lock lo untundi. Vaallu Accept chesina tarvata matrame numbers exchange avutayi — iddaru oppukunnappude. Ante spam calls, fake ids, mosam — anni block. Ee consent logic top matrimony sites lo ide, kani manam WhatsApp lo fast ga chestham.",
  },
  {
    q: "Naa photo public lo kanipisthunda?",
    a: "Photo-Private ON cheste public lo blur ga kanipisthundi — WhatsApp/Telegram cards lo kooda watermark. Interest accept ayyaka matrame clear photos. Screenshot misuse jarigina watermark + report system tho action teesukuntam.",
  },
  {
    q: "Naa profile ee channels lo post avutundi?",
    a: `Mee caste + state + job batti ${CHANNEL_STATS.total} channels nunchi saripoyE vi (max 5) — udaharanaki Reddy TS Bride Software ayithe @TSBRIDE + @manavivaha_reddy_bride + @manavivaha_software. 4 main + caste prakaram (bride/groom separate) + religion + special anni cover.`,
  },
  {
    q: "WhatsApp lo kooda vasthunda? Anti-ban safe a?",
    a: "Avunu — Telegram post ayyaka WhatsApp channels/groups ki kooda veltundi. Manam manishi la ne post chestham: 120–170 seconds random gap, typing simulation, roju caps, raatri aapitam — WhatsApp ban risk chala thakkuva. Interest vachinappudu kooda WhatsApp lo ne notification + profile card.",
  },
  {
    q: "Mosam/fake profiles unte em chestharu?",
    a: "DOB + OTP verify, photo watermark, 3 reports → auto hide, @manavivaha_alerts lo fraud alerts. Advance money adigithe ventane report cheyyandi — 24h lo action. Decline ayyina credit refund istham.",
  },
];

const PLANS = [
  {
    name: "FREE",
    price: "₹0",
    tag: "Start ikkade",
    credits: "Modati 3 profiles FREE",
    features: ["3 interest requests FREE", "WhatsApp lo mee profile share", `Auto-post ${CHANNEL_STATS.total} channel network`, "ID search always open", "Photo-private mode"],
  },
  {
    name: "Sambandham",
    price: "₹99",
    tag: "Entry • ₹20/profile",
    credits: "5 profiles • 30 days",
    features: ["5 interest requests", "⚡ 7-day profile boost (channel top)", "Accept aithe number exchange", "Decline aithe credit refund", "Referral tho ₹50 earn"],
  },
  {
    name: "Family",
    price: "₹199",
    tag: "Most popular • ₹17/profile",
    popular: true,
    credits: "12 profiles • 45 days",
    features: ["12 interest requests", "✅ Photo-verified badge", "🔮 Free 10-porutham report (1)", "Daily fresh matches digest", "Family bureau assist"],
  },
  {
    name: "Premium",
    price: "₹299",
    tag: "Best value • ₹12/profile",
    credits: "25 profiles • 60 days",
    features: ["25 interest requests", "⚡ 30-day boost (top of channel)", "👀 Who-viewed-me 60 days", "✅ Verified badge", "Telugu dedicated support"],
  },
  {
    name: "Vivaha VIP",
    price: "₹499",
    tag: "VIP • ₹10/profile",
    credits: "50 profiles • 90 days",
    features: ["50 interest requests", "🎯 Matchmaker assist (mana team call)", "⚡ 90-day boost", "💍 Wedding vendor discounts", "Priority WhatsApp support"],
  },
];

// 🎁 ADD-ONS — credits kanna per-item revenue (margin 100%)
const ADDONS = [
  { p: "₹49", t: "Profile Boost", d: "7 days channel top lo" },
  { p: "₹49", t: "Who viewed me", d: "30 days — names tho" },
  { p: "₹99", t: "10-Porutham report", d: "Full kundli match (Telugu)" },
  { p: "₹199", t: "Photo verify badge", d: "3x ekkuva acceptances" },
];

const TESTIMONIALS = [
  { name: "Reddy family, Nalgonda", text: "Channel lo post ayyina 3rd day ke sambandham set ayyindi. Caste + gothram details clear ga undadam valla nammakam vachindi.", tag: "Demo testimonial" },
  { name: "Software Bride, Hyderabad", text: "Photo-private mode valla tension ledu. Number pay tarvata matrame kanipinchadam chala safe anipinchindi.", tag: "Demo testimonial" },
  { name: "Muslim family, Warangal", text: "Mana community channel separate ga undadam valla pani chala easy ayyindi — direct ga matching profiles vachayi.", tag: "Demo testimonial" },
];

export default function Home() {
  const [trustBoard, setTrustBoard] = useState<{ count: number; average_trust: number; board: Record<string, unknown>[] } | null>(null);
  const [posture, setPosture] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    void apiGet<{ count: number; average_trust: number; board: Record<string, unknown>[] }>("/api/trust/board?limit=6")
      .then(({ ok, data }) => { if (ok && data) setTrustBoard(data); });
    void apiGet<Record<string, unknown>>("/api/security/posture")
      .then(({ ok, data }) => { if (ok && data) setPosture(data); });
  }, []);

  const [searchId, setSearchId] = useState("");
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  const regionChannels: Channel[] = useMemo(() => ALL_CHANNELS.filter((c) => c.tier === "L1_REGION"), []);
  const religionChannels: Channel[] = useMemo(() => ALL_CHANNELS.filter((c) => c.tier === "L2_RELIGION"), []);
  const casteChannels: Channel[] = useMemo(() => ALL_CHANNELS.filter((c) => c.tier === "L3_CASTE"), []);
  const specialChannels: Channel[] = useMemo(() => ALL_CHANNELS.filter((c) => c.tier === "L4_SPECIAL"), []);
  const liveChannels = ALL_CHANNELS.filter((c) => c.live);

  const tickerItems = [
    `${CHANNEL_STATS.total} channels — Region • Religion • ${CHANNEL_STATS.by_tier.L3_CASTE} Castes • Special`,
    "₹99 ke Sambandham — modati 3 numbers FREE",
    "Photo-Private • DOB Verified • Watermark protected",
    "Telegram + WhatsApp auto-post",
    "43 castes: Reddy nunchi Madiga, Lambada, Boya varaku",
    "Muslim • Christian • Inter-faith channels kooda",
    "Referral — per profile ₹50",
  ];

  return (
    <div className="bg-cream">
      {/* ================= HERO ================= */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 dotted-bg opacity-60 pointer-events-none" />
        <div className="absolute -top-24 -right-24 w-80 h-80 rounded-full bg-gold/20 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-80 h-80 rounded-full bg-maroon/10 blur-3xl pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-4 pt-8 pb-10 grid lg:grid-cols-[1.15fr_0.85fr] gap-10 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-gold/40 shadow-soft text-[11px] font-bold text-maroon">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulseRing" />
              LIVE • {liveChannels.length} channels live now • {CHANNEL_STATS.total} total planned
            </div>

            <h1 className="mt-4 text-[32px] md:text-[46px] font-bold text-maroon leading-[1.12]">
              Mana Vivaha lo <span className="text-gradient-gold">Sambandham</span>
              <br />
              manaki daggara ga, nammakam ga.
            </h1>

            <p className="mt-3 text-sm md:text-base text-gray-700 telugu leading-relaxed max-w-xl">
              Telangana + Andhra Pradesh Telugu Matrimony.{" "}
              <b>Region • Religion • 43 Castes • Special</b> — {CHANNEL_STATS.total} channels,
              okka register tho mee profile saripoyE anni chotaki auto ga veltundi.{" "}
              <b>₹99 ke Sambandham — modati 3 numbers FREE.</b>
            </p>

            <div className="mt-5 flex flex-wrap gap-3">
              <Link
                href="/register"
                className="px-6 py-3.5 rounded-full maroon-gradient text-white text-sm font-bold shadow-brand hover:shadow-brandLg transition"
              >
                🚀 Register FREE — 3 nimushalu
              </Link>
              <a
                href={BOT}
                target="_blank"
                rel="noreferrer"
                className="px-6 py-3.5 rounded-full gold-gradient text-maroon text-sm font-bold shadow-soft"
              >
                🤖 Telegram Bot — {SITE_CONFIG.botUsername}
              </a>
            </div>

            <div className="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-[12px] font-semibold text-gray-700">
              {SITE_CONFIG.trustPoints.map((t) => (
                <span key={t}>✓ {t}</span>
              ))}
            </div>

            {/* ID search */}
            <div className="mt-6 bg-white rounded-2xl p-1.5 flex items-center gap-2 card-shadow max-w-xl border border-gold/25">
              <span className="pl-3.5 text-gray-400" aria-hidden>🔍</span>
              <input
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                placeholder="Profile ID tho search cheyyi — TSAP-F-2025-5775"
                className="flex-1 outline-none text-sm py-2.5 bg-transparent"
                aria-label="Profile ID search"
              />
              <Link
                href={`/search/${searchId.trim() || "TSAP-M-2025-1042"}`}
                className="px-5 py-2.5 maroon-gradient text-white rounded-xl text-sm font-bold whitespace-nowrap"
              >
                Search
              </Link>
            </div>
          </div>

          {/* Hero card mock */}
          <Reveal delay={120}>
            <div className="relative max-w-md mx-auto w-full">
              <div className="absolute inset-0 maroon-gradient rounded-[2rem] rotate-3 opacity-15" />
              <div className="relative bg-white rounded-[2rem] p-5 card-shadow-lg border border-gold/30">
                <div className="flex items-center justify-between">
                  <div className="text-[10px] font-bold text-gold-deep uppercase tracking-widest">
                    Mana Vivaha • Profile Card
                  </div>
                  <div className="text-[10px] px-2 py-1 rounded-full bg-green-50 text-green-700 font-bold">
                    ✓ DOB Verified
                  </div>
                </div>

                <div className="mt-3 flex gap-3">
                  <div className="w-20 h-24 rounded-xl maroon-gradient flex items-center justify-center text-gold font-bold text-xl shrink-0">
                    LR
                  </div>
                  <div className="min-w-0">
                    <div className="font-bold text-sm text-maroon">TSAP-F-2025-5775</div>
                    <div className="text-[12px] text-gray-700 mt-0.5">25y • 5'4" • Reddy</div>
                    <div className="text-[12px] text-gray-700">BTech • Software @ Hyderabad</div>
                    <div className="text-[12px] text-gray-700">Nalgonda, TS</div>
                    <div className="mt-1.5 flex flex-wrap gap-1">
                      {["O+", "Rohini", "Bharadwaj"].map((c) => (
                        <span key={c} className="text-[10px] px-2 py-0.5 rounded-full bg-gold-soft text-maroon font-bold">
                          {c}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="ml-auto text-right shrink-0">
                    <div className="text-[22px] font-bold text-gradient-gold leading-none">97%</div>
                    <div className="text-[9px] font-bold text-gold-deep">BEST MATCH</div>
                  </div>
                </div>

                <div className="mt-3 bg-cream rounded-2xl p-3 text-[11px] space-y-1">
                  <div className="font-bold text-maroon">Enduku set avutharu?</div>
                  <div>✓ Reddy Bharadwaj gothram + Rohini nakshatram — clear</div>
                  <div>✓ BTech + Software Engineer (8 LPA) — settled</div>
                  <div>✓ Hyderabad lo work — same city</div>
                </div>

                <div className="mt-3 flex gap-2">
                  <button className="flex-1 py-2.5 maroon-gradient text-white rounded-full text-[12px] font-bold">
                    ❤️ Interest Pampu
                  </button>
                  <button className="flex-1 py-2.5 border border-gold text-maroon rounded-full text-[12px] font-bold">
                    📞 Number (1 credit)
                  </button>
                </div>

                <div className="mt-2 text-[10px] text-center text-gray-400">
                  #Reddy #TSBride #Software #Nalgonda #Age25 • WM TSAP-F-2025-5775
                </div>
              </div>
            </div>
          </Reveal>
        </div>

        {/* Ticker */}
        <div className="relative bg-maroon text-white py-2.5 ticker-mask">
          <div className="ticker-track text-[11px] font-semibold tracking-wide">
            {[...tickerItems, ...tickerItems].map((t, i) => (
              <span key={i} className="mx-6 inline-flex items-center gap-2">
                <span className="text-gold">◆</span>
                {t}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ================= STATS ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { v: CHANNEL_STATS.total, l: "Channels (network)", s: "Region + Religion + Caste + Special" },
            { v: CHANNEL_STATS.by_tier.L3_CASTE, l: "Castes covered", s: "Reddy nunchi SC/ST varaku" },
            { v: "0 chat", l: "Chatting ledu — direct contact", s: "Anti-ban WhatsApp delivery" },
            { v: "₹99→3", l: "Profiles (₹199→10, ₹299→20)", s: "Modati 3 requests FREE" },
          ].map((s, i) => (
            <Reveal key={s.l} delay={i * 80}>
              <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 h-full">
                <div className="text-2xl md:text-3xl font-bold text-maroon">{s.v}</div>
                <div className="text-[13px] font-bold text-ink mt-1">{s.l}</div>
                <div className="text-[11px] text-gray-500 mt-0.5">{s.s}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ================= HOW IT WORKS ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Elaga pani chestundi"
            title="4 steps lo sambandham — antha automatic"
            subtitle="Register nunchi channel post varaku bot chusukuntundi. Nuvvu manual ga edi post cheyyakkarledu."
            telugu
          />
        </Reveal>
        <div className="mt-6 grid md:grid-cols-4 gap-4">
          {[
            { n: "01", t: "Register — 3 min", d: "Personal, family, caste/astro, education, location + photo. 5 steps, mobile lo easy.", icon: "📝" },
            { n: "02", t: "Card + ID ready", d: "Profile card automatic ga generate avutundi — anni details, QR, watermark tho.", icon: "🎴" },
            { n: "03", t: "Channels lo auto-post", d: `Mee caste + state + job batti ${CHANNEL_STATS.total} channels nunchi saripoyE vi — Telegram + WhatsApp.`, icon: "📢" },
            { n: "04", t: "Interest pampu → number exchange", d: "Nachhina profile ki 💌 Interest pampu (1 credit). Accept aithe rendu numbers WhatsApp lo automatic.", icon: "💌" },
          ].map((s, i) => (
            <Reveal key={s.n} delay={i * 90}>
              <div className="relative bg-white rounded-2xl p-5 card-shadow border border-gold/20 h-full hover-lift">
                <div className="text-3xl" aria-hidden>{s.icon}</div>
                <div className="mt-2 text-[11px] font-bold text-gold-deep tracking-widest">STEP {s.n}</div>
                <div className="font-bold text-maroon text-[15px] mt-1">{s.t}</div>
                <div className="text-[12px] text-gray-600 mt-1.5 leading-relaxed">{s.d}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ================= REQUEST MODEL (CHATTING LEDU) ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <div className="rounded-3xl cream-gradient border border-gold/30 p-5 md:p-8">
          <Reveal>
            <SectionHeading
              eyebrow="Advanced model — top matrimony sites kanna smart"
              title="Chatting ledu. Interest pampu → WhatsApp lo number exchange"
              subtitle="Chat = time waste + fake ids + moderation cost. Manam consent-based request model: evaru accept cheste vaallu matrame matladukuntaru."
              telugu
              action={{ href: "/requests", label: "💌 Requests dashboard" }}
            />
          </Reveal>

          <div className="mt-6 grid md:grid-cols-2 gap-5 items-start">
            {/* LEFT: 4 steps */}
            <div className="space-y-3">
              {[
                { i: "💌", t: "1. Interest pampu (1 credit)", d: "Profile chusi \"Interest Pampu\" press chey — modati 3 requests FREE, tarvata ₹99 → 5 profiles." },
                { i: "📲", t: "2. Waallaki WhatsApp lo mee profile", d: "Mana WhatsApp nunchi vaallaki mee profile card + details veltundi — \"oka person mee profile chusi interesting ga unnaru\"." },
                { i: "✅", t: "3. Accept aithe numbers exchange", d: "Vaallu accept chesthe — rendu numbers automatic ga WhatsApp lo. Direct ga call/chat chesukovachu, manam middle lo undamu." },
                { i: "↩️", t: "4. Decline aithe credit refund", d: "Ee sari kudaraledu ante polite message + mee credit tirigi vasthundi. Ante evaru money waste cheyyaru." },
              ].map((x, i) => (
                <Reveal key={x.t} delay={i * 80}>
                  <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 flex gap-3 hover-lift">
                    <div className="text-2xl leading-none" aria-hidden>{x.i}</div>
                    <div>
                      <div className="font-bold text-maroon text-[14px]">{x.t}</div>
                      <div className="text-[12px] text-gray-600 mt-1 leading-relaxed">{x.d}</div>
                    </div>
                  </div>
                </Reveal>
              ))}
              <Reveal delay={320}>
                <div className="flex flex-wrap gap-2 text-[11px] font-bold">
                  <span className="px-3 py-1 rounded-full bg-maroon text-white">🚫 0 chatting</span>
                  <span className="px-3 py-1 rounded-full bg-white text-maroon border border-maroon/30">🔒 Consent first</span>
                  <span className="px-3 py-1 rounded-full bg-white text-maroon border border-maroon/30">↩️ Decline = refund</span>
                  <span className="px-3 py-1 rounded-full bg-gold text-maroon">🛡️ Anti-ban WhatsApp</span>
                </div>
              </Reveal>
            </div>

            {/* RIGHT: WhatsApp mockup (real message we send) */}
            <Reveal delay={140}>
              <div className="rounded-3xl overflow-hidden card-shadow-lg border border-black/10 bg-[#0b141a]">
                <div className="bg-[#202c33] px-4 py-3 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full gold-gradient flex items-center justify-center font-bold text-maroon">MV</div>
                  <div className="min-w-0">
                    <div className="text-white text-[13px] font-bold truncate">Mana Vivaha Matrimony</div>
                    <div className="text-[10px] text-emerald-300">🟢 online • verified business</div>
                  </div>
                  <span className="ml-auto text-[10px] text-gray-400">🔒 secured</span>
                </div>
                <div className="p-3 space-y-2 dotted-bg">
                  <div className="bg-[#005c4b] text-white text-[12px] rounded-xl rounded-tl-sm p-3 leading-relaxed max-w-[95%]">
                    <div className="font-bold">💌 MANA VIVAHA — Mee profile ki INTEREST vachhindi!</div>
                    <div className="opacity-90 mt-1">Oka person mee profile chusi <b>&quot;interesting ga unnaru&quot;</b> ani request pettaru 👇</div>
                    <div className="mt-2 pl-1 border-l-2 border-white/30">
                      👤 <b>Kiran Kumar Reddy</b> (29y)<br />
                      🎓 MBBS MD • 💼 Doctor, Apollo<br />
                      📍 Nalgonda, TS • 💍 Reddy<br />
                      ⭐ <b>82% match</b>
                    </div>
                    <div className="mt-2 opacity-90">✅ Accept chesthe → valla number meeku WhatsApp lo</div>
                    <div className="text-[10px] opacity-70 mt-2 text-right">11:42 ✓✓</div>
                  </div>
                  <div className="bg-[#202c33] text-white text-[12px] rounded-xl p-3 max-w-[80%]">
                    Profile card + photo ikkade vasthundi 🎴
                    <div className="text-[10px] opacity-70 mt-1">attachment: TSAP-M-2025-1042.png</div>
                  </div>
                  <div className="flex gap-2 pt-1">
                    <button className="flex-1 bg-emerald-600 text-white text-[12px] font-bold rounded-xl py-2">✅ Accept</button>
                    <button className="flex-1 bg-white/10 text-white text-[12px] font-bold rounded-xl py-2">❌ Decline (refund)</button>
                  </div>
                  <div className="text-[10px] text-gray-400 text-center pt-1">
                    🛡️ Mana posts: 120–170s random gap • typing simulation • daily caps
                  </div>
                </div>
              </div>
            </Reveal>
          </div>

          {/* Pricing strip */}
          <div className="mt-6 grid grid-cols-3 gap-3">
            {[
              { p: "₹99", n: "5 profiles", s: "₹20/profile — entry" },
              { p: "₹199", n: "12 profiles", s: "₹17/profile — popular" },
              { p: "₹299", n: "25 profiles", s: "₹12/profile — best value" },
            ].map((x, i) => (
              <Reveal key={x.p} delay={i * 70}>
                <div className="bg-white rounded-2xl p-3 text-center card-shadow border border-gold/25">
                  <div className="text-xl font-bold text-maroon">{x.p}</div>
                  <div className="text-[12px] font-bold text-ink">{x.n}</div>
                  <div className="text-[10px] text-gray-500">{x.s}</div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CHANNELS: REGION + RELIGION ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Channel network"
            title={`${CHANNEL_STATS.total} channels — mee profile saripoyE anni chotaki`}
            subtitle="Region + Religion + Caste + Special. Okka approve = anni related channels lo post."
            telugu
            action={{ href: "/channels", label: `Anni ${CHANNEL_STATS.total} channels` }}
          />
        </Reveal>

        <div className="mt-5 grid grid-cols-2 md:grid-cols-5 gap-3">
          {[...regionChannels, ...religionChannels].slice(0, 10).map((ch, i) => (
            <Reveal key={ch.key} delay={i * 50}>
              <a
                href={ch.live ? ch.link : "/channels"}
                target={ch.live ? "_blank" : undefined}
                rel="noreferrer"
                className={`block rounded-2xl p-3.5 text-white card-shadow h-full hover-lift ${
                  ch.key.startsWith("ts") ? "maroon-gradient" : ch.tier === "L2_RELIGION" ? "navy-gradient" : "maroon-gradient"
                }`}
              >
                <div className="text-[13px] font-bold leading-tight">{ch.name}</div>
                <div className="text-[11px] opacity-85 mt-1">{ch.status}</div>
                <div className="mt-2 flex gap-1 flex-wrap">
                  <span className="text-[10px] bg-white/20 px-2 py-1 rounded-full">{ch.username}</span>
                  <span className="text-[10px] bg-gold text-maroon px-2 py-1 rounded-full font-bold">
                    {ch.live ? "Join" : `W${ch.wave}`}
                  </span>
                </div>
              </a>
            </Reveal>
          ))}
        </div>

        {/* Auto-post flow explainer */}
        <Reveal>
          <div className="mt-5 bg-white rounded-2xl p-5 card-shadow border border-gold/25">
            <div className="font-bold text-maroon text-[15px]">🤖 Auto-post flow — okka register, anni chotaki</div>
            <div className="mt-3 grid md:grid-cols-4 gap-3 text-[12px]">
              <div className="bg-cream rounded-xl p-3">
                <div className="font-bold text-maroon">1. Profile submit</div>
                <div className="text-gray-600 mt-1">Register 5 steps + photo</div>
              </div>
              <div className="bg-cream rounded-xl p-3">
                <div className="font-bold text-maroon">2. Router decide</div>
                <div className="text-gray-600 mt-1">Caste × State × Gender × Job × Special flags</div>
              </div>
              <div className="bg-cream rounded-xl p-3">
                <div className="font-bold text-maroon">3. Telegram + WhatsApp</div>
                <div className="text-gray-600 mt-1">Bot card + caption + hashtags post</div>
              </div>
              <div className="bg-cream rounded-xl p-3">
                <div className="font-bold text-maroon">4. Retry + log</div>
                <div className="text-gray-600 mt-1">429/error → 3 retries, publish log audit</div>
              </div>
            </div>
            <div className="mt-3 bg-navy text-white rounded-xl p-3 text-[11px] font-mono overflow-x-auto scrollbar-hide">
              Reddy + TS + Bride + Software → <span className="text-gold">@TSBRIDE → @manavivaha_reddy → @manavivaha_software</span> (max 5 channels)
            </div>
          </div>
        </Reveal>
      </section>

      {/* ================= CASTES ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Caste-wise"
            title={`${CHANNEL_STATS.by_tier.L3_CASTE} caste channels — 1 caste = 1 channel`}
            subtitle="Bride + Groom iddaru okkate channel lo — #Bride / #Groom hashtag tho filter. 5000 members dataka split cheyyamu (empty channels fail avuthayi)."
            telugu
            action={{ href: "/channels?tier=L3_CASTE", label: "Caste list chudu" }}
          />
        </Reveal>
        <div className="mt-5 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2.5">
          {casteChannels.slice(0, 24).map((c, i) => (
            <Reveal key={c.key} delay={i * 25}>
              <Link
                href="/channels"
                className="block bg-white rounded-xl p-3 border border-gold/20 hover-lift h-full"
              >
                <div className="flex items-start justify-between gap-1">
                  <div className="text-[13px] font-bold text-maroon leading-tight">
                    {c.name.replace(/^💍 /, "").replace(" Matrimony", "").replace(" | TS-AP", "")}
                  </div>
                  {c.wave === 1 && (
                    <span className="text-[9px] bg-red-100 text-red-600 px-1.5 py-0.5 rounded-full font-bold shrink-0">W1</span>
                  )}
                </div>
                <div className="text-[10px] text-gray-500 mt-1">
                  {c.live ? "LIVE ✅" : `Wave-${c.wave}`}
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-3 text-[12px] text-gray-600">
          + inka {casteChannels.length - 24} castes (Boya, Kuruba, Uppara, Vaddera, Rajaka, Viswakarma, Kummara,
          Gandla, Devanga, Koya, Gond, SC/ST sub-castes...) —{" "}
          <Link href="/channels?tier=L3_CASTE" className="font-bold text-maroon underline">
            full list chudu
          </Link>
        </div>
      </section>

      {/* ================= SPECIAL CATEGORIES ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Special respect"
            title="Prathi okkariki separate space — dignity tho"
            subtitle="2nd marriage, differently abled, 35+, govt jobs, doctors, NRI — prathi vallaki prathyeka channel."
            telugu
          />
        </Reveal>
        <div className="mt-5 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {specialChannels.map((sp, i) => (
            <Reveal key={sp.key} delay={i * 40}>
              <Link
                href="/channels?tier=L4_SPECIAL"
                className="block bg-white rounded-2xl p-4 card-shadow border border-gold/20 h-full hover-lift"
              >
                <div className="text-xl" aria-hidden>{sp.name.split(" ")[0]}</div>
                <div className="font-bold text-[13px] text-maroon mt-1.5">
                  {sp.name.replace(/^[^\s]+\s/, "")}
                </div>
                <div className="text-[11px] text-gray-600 mt-1 line-clamp-2">{sp.desc}</div>
                <div className="text-[10px] mt-2 font-bold text-gold-deep">
                  {sp.live ? "LIVE ✅" : `Wave-${sp.wave}`}
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ================= 🏪 WEDDING VENDORS (ads) ================= */}
      <VendorStrip />

      {/* ================= PRICING ================= */}
      {SITE_CONFIG.features.showPricing && (
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Pricing"
            title="Simple ga — ₹99 ke Sambandham"
            subtitle="Register FREE. Modati 3 interest requests FREE. Tarvata ₹99 → 5 profiles, ₹199 → 12, ₹299 → 25, ₹499 → 50. Prati tier ki ₹/profile thaggutundi — decline aithe credit refund."
            telugu
            align="center"
          />
        </Reveal>
        <div className="mt-6 grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {PLANS.map((p, i) => (
            <Reveal key={p.name} delay={i * 90}>
              <div
                className={`relative rounded-3xl p-5 h-full ${
                  p.popular
                    ? "bg-white border-2 border-gold card-shadow-lg"
                    : "bg-white border border-gold/20 card-shadow"
                }`}
              >
                {p.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] gold-gradient text-maroon px-3 py-1 rounded-full font-bold shadow-gold">
                    POPULAR
                  </div>
                )}
                <div className="text-[11px] font-bold text-gold-deep tracking-widest uppercase">{p.tag}</div>
                <div className="font-bold text-maroon text-lg mt-1">{p.name}</div>
                <div className="mt-2 flex items-end gap-1">
                  <span className="text-3xl font-bold text-maroon">{p.price}</span>
                  <span className="text-[11px] text-gray-500 mb-1">one-time</span>
                </div>
                <div className="text-[11px] text-gray-600 mt-1">{p.credits}</div>
                <div className="mt-3 space-y-1.5">
                  {p.features.map((f) => (
                    <div key={f} className="text-[12px] flex gap-2">
                      <span className="text-green-600 font-bold">✓</span>
                      <span className="text-gray-700">{f}</span>
                    </div>
                  ))}
                </div>
                <Link
                  href="/register"
                  className={`block text-center mt-4 py-3 rounded-full text-[13px] font-bold ${
                    p.popular ? "gold-gradient text-maroon" : "maroon-gradient text-white"
                  }`}
                >
                  {p.price === "₹0" ? "FREE ga start" : `${p.price} pay chesi start`}
                </Link>
                <div className="mt-2 text-[10px] text-center text-gray-400">Razorpay secure • refund policy</div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* 🎁 ADD-ONS */}
        <Reveal delay={120}>
          <div className="mt-6 rounded-3xl bg-white border border-gold/30 card-shadow p-5">
            <div className="flex flex-wrap items-center gap-2">
              <div className="font-bold text-maroon">🎁 Add-ons — credits kanna extra value</div>
              <span className="text-[10px] font-bold bg-cream border border-gold/40 px-2 py-0.5 rounded-full">per-item • eppudaina</span>
            </div>
            <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">
              {ADDONS.map((a) => (
                <div key={a.t} className="rounded-2xl bg-cream border border-gold/25 p-3">
                  <div className="text-lg font-bold text-maroon">{a.p}</div>
                  <div className="text-[12px] font-bold text-ink">{a.t}</div>
                  <div className="text-[10px] text-gray-600">{a.d}</div>
                </div>
              ))}
            </div>
            <div className="mt-3 text-[11px] text-gray-600">
              🔁 <b>Renewal offer:</b> pata customers ki ₹99 → 8 profiles (first-time ₹99 → 5) • 🏢 Bureau: ₹999/mo → 25 profiles + monthly report
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              <Link href="/requests" className="text-[12px] font-bold maroon-gradient text-white px-4 py-2 rounded-full">Plans + add-ons konandi →</Link>
              <Link href="/requests" className="text-[12px] font-bold border border-maroon/30 text-maroon px-4 py-2 rounded-full">👀 Evaru chusaro chudandi</Link>
            </div>
          </div>
        </Reveal>
      </section>
      )}

      {/* ================= TESTIMONIALS ================= */}
      {SITE_CONFIG.features.showTestimonials && (
      <section className="max-w-7xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Nammakam"
            title="Families em antunnaru"
            subtitle="Real reviews add avuthayi — ippatiki demo samples."
            telugu
          />
        </Reveal>
        <div className="mt-5 grid md:grid-cols-3 gap-4">
          {TESTIMONIALS.map((t, i) => (
            <Reveal key={t.name} delay={i * 80}>
              <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20 h-full">
                <div className="text-gold text-sm" aria-hidden>★★★★★</div>
                <div className="text-[13px] text-gray-700 mt-2 leading-relaxed italic">“{t.text}”</div>
                <div className="mt-3 flex items-center justify-between">
                  <div className="text-[12px] font-bold text-maroon">{t.name}</div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-cream text-gray-500">{t.tag}</span>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>
      )}

      {/* ================= REFERRAL + BUREAU ================= */}
      <section className="max-w-7xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-5">
        <Reveal>
          <div className="bg-white rounded-3xl p-6 card-shadow border border-gold/20 h-full">
            <div className="font-bold text-maroon text-[16px]">🏆 Referral — mee link share, mee earning</div>
            <div className="text-[12px] text-gray-600 mt-1.5 telugu">
              Mee referral link (short code: LAK42 lantidi) share cheyyandi — prathi profile pay ki <b>₹50</b>.
              Bureaus/brokers ki prathyeka dashboard + leaderboard.
            </div>
            <div className="mt-4 grid grid-cols-3 gap-2.5 text-center">
              {[
                { k: "Per pay", v: "₹50" },
                { k: "25 pays", v: "+₹500" },
                { k: "Payout", v: "UPI weekly" },
              ].map((x) => (
                <div key={x.k} className="bg-cream rounded-xl p-3">
                  <div className="font-bold text-maroon text-[15px]">{x.v}</div>
                  <div className="text-[10px] text-gray-500 mt-0.5">{x.k}</div>
                </div>
              ))}
            </div>
            <div className="mt-4 flex gap-2">
              <Link href="/referral" className="px-4 py-2.5 maroon-gradient text-white rounded-full text-[12px] font-bold">
                Naa referral code →
              </Link>
              <Link href="/referral/register" className="px-4 py-2.5 border border-gold text-maroon rounded-full text-[12px] font-bold">
                Referrer ga join
              </Link>
            </div>
          </div>
        </Reveal>

        <Reveal delay={100}>
          <div className="navy-gradient rounded-3xl p-6 text-white h-full">
            <div className="font-bold text-gold text-[16px]">🏢 Bureau / Broker B2B</div>
            <div className="text-[12px] opacity-85 mt-1.5 telugu">
              Already marriage bureau nadipisthunara? Mana profiles share cheyyandi + commission teesukondi.
            </div>
            <div className="mt-4 bg-white/10 rounded-2xl p-4">
              <div className="font-bold text-[15px]">Bureau Starter — ₹999/mo</div>
              <div className="text-[12px] opacity-85 mt-1.5 space-y-1">
                <div>✓ 100 white-label profile cards (mee peru tho)</div>
                <div>✓ 25 credits + dashboard + bulk CSV upload</div>
                <div>✓ Per client ₹30 commission + extra charge meere</div>
                <div>✓ Leaderboard + weekly UPI payout</div>
              </div>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href="/bureau" className="px-4 py-2.5 bg-white text-navy rounded-full text-[12px] font-bold">
                Bureau dashboard →
              </Link>
              <span className="px-4 py-2.5 bg-gold text-navy rounded-full text-[12px] font-bold">
                {CHANNEL_STATS.bot.includes("bot") ? "B2B open" : "B2B open"}
              </span>
            </div>
          </div>
        </Reveal>
      </section>

      {/* ================= FAQ ================= */}
      {SITE_CONFIG.features.showFaq && (
      <section className="max-w-4xl mx-auto px-4 py-8">
        <Reveal>
          <SectionHeading
            eyebrow="Prashnalu"
            title="Frequently asked — Telugu lo clear answers"
            align="center"
          />
        </Reveal>
        <div className="mt-6 space-y-3">
          {FAQS.map((f, i) => (
            <Reveal key={f.q} delay={i * 40}>
              <div className="bg-white rounded-2xl border border-gold/20 card-shadow overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  aria-expanded={openFaq === i}
                  className="w-full flex items-center justify-between gap-3 px-5 py-4 text-left focus-brand"
                >
                  <span className="font-bold text-[13.5px] text-maroon">{f.q}</span>
                  <span
                    className={`w-7 h-7 shrink-0 rounded-full maroon-gradient text-white flex items-center justify-center text-sm transition-transform ${
                      openFaq === i ? "rotate-45" : ""
                    }`}
                    aria-hidden
                  >
                    +
                  </span>
                </button>
                <div className={`faq-body px-5 ${openFaq === i ? "open" : ""}`}>
                  <div className="pb-4 text-[12.5px] text-gray-700 leading-relaxed telugu">{f.a}</div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>
      )}

      {/* ================= FINAL CTA ================= */}
      <section className="max-w-7xl mx-auto px-4 py-10">
        <Reveal>
          <div className="maroon-gradient rounded-[2rem] p-8 md:p-10 text-white relative overflow-hidden">
            <div className="absolute -top-16 -right-16 w-64 h-64 rounded-full bg-gold/20 blur-3xl" />
            <div className="relative md:flex items-center justify-between gap-6">
              <div>
                <h2 className="text-2xl md:text-3xl font-bold leading-snug">
                  Ippude start chey — <span className="text-gradient-gold">3 nimushalu</span> chalu
                </h2>
                <p className="mt-2 text-[13px] opacity-90 telugu max-w-xl">
                  Register FREE → profile card ready → {CHANNEL_STATS.total} channels network lo auto-post →
                  modati 3 interest requests FREE. Tarvata ₹99 → 5 profiles, ₹199 → 12, ₹299 → 25, ₹499 → 50 (VIP).
                </p>
                <div className="mt-4 flex flex-wrap gap-3">
                  <Link
                    href="/register"
                    className="px-6 py-3.5 rounded-full gold-gradient text-maroon text-sm font-bold shadow-gold"
                  >
                    🚀 Register FREE
                  </Link>
                  <a
                    href={BOT}
                    target="_blank"
                    rel="noreferrer"
                    className="px-6 py-3.5 rounded-full bg-white/15 border border-white/30 text-white text-sm font-bold"
                  >
                    🤖 Bot lo register
                  </a>
                </div>
              </div>
              <div className="mt-6 md:mt-0 text-center shrink-0">
                <div className="text-[11px] opacity-80">ID search</div>
                <div className="font-mono text-gold text-lg">{SITE_CONFIG.domain}/search</div>
                <div className="text-[11px] opacity-80 mt-2">Bot</div>
                <div className="font-mono text-gold text-lg">{SITE_CONFIG.botUsername}</div>
              </div>
            </div>
          </div>
        </Reveal>
      </section>
    {/* 🛡️ WAVE 9 — Trust & security (transparency: numbers policy, audit, rate limits) */}
    <section className="max-w-7xl mx-auto px-4 py-8">
      <SectionHeading title="🛡️ Trust & Security — numbers eppudu public kaadu"
        subtitle="Phone numbers 🔒 lock — interest accept (consent) tho matrame exchange. Consent ledger, rate limits, audit anni open ga chupisthunnam." />
      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
          <p className="text-2xl font-extrabold text-emerald-900">{trustBoard ? `${trustBoard.average_trust}/100` : "—"}</p>
          <p className="text-[13px] font-semibold text-emerald-900">Average trust score ({trustBoard?.count ?? 0} profiles)</p>
          <p className="mt-1 text-[12px] text-emerald-800">Verify + complete profile unte score perugutundi — matches kooda ekkuva.</p>
        </div>
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4">
          <p className="text-[13px] font-bold text-rose-900">🔒 Numbers policy</p>
          <p className="mt-1 text-[12px] text-rose-800">{String(posture?.numbers_policy || "Phone numbers public API lo eppudu ledu (98••••••45 mask).")}</p>
          <p className="mt-2 text-[12px] font-semibold text-rose-900">Free: 3 profiles + 3 interests · Paid: ₹99 → 5 profiles</p>
        </div>
        <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4">
          <p className="text-[13px] font-bold text-sky-900">🧱 Abuse protection live</p>
          <ul className="mt-1 space-y-1 text-[12px] text-sky-900">
            <li>🚦 Rate limit: {String(posture?.rate_limit || "sliding-window")}</li>
            <li>🔐 Auth: {posture?.auth_enforced ? "enforced" : "dev mode (token optional)"}</li>
            <li>🔁 Payment replay protection (idempotency)</li>
            <li>📜 Consent ledger: numbers exchange audit trail</li>
          </ul>
        </div>
      </div>
      {trustBoard?.board?.length ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {trustBoard.board.map((b) => (
            <Link key={String(b.tsap_id)} href={`/search/${b.tsap_id}`}
              className="rounded-full border border-gold/40 bg-white px-3 py-1.5 text-[11px] font-semibold text-maroon hover:bg-cream">
              {String(b.badge_telugu || "⭐")} {String(b.tsap_id)} · {String(b.trust_score)}/100
            </Link>
          ))}
        </div>
      ) : null}
      <p className="mt-3 text-[12px] text-gray-600">
        Ee page load ayyaka API nunchi live data vastundi (<code>/api/trust/board</code>, <code>/api/security/posture</code>) —
        mee profile complete chesukoni board lo top lo kanipinchandi.
      </p>
    </section>
    </div>
  );
}

/* ---------------------------------------------------------------------------
   🏪 VENDOR AD STRIP — catering / photography / decorations / halls...
   ("pelli sambandham related vaallaki promotions kooda cheyyali bestga")
   Paid-first rotation (/api/vendors/ads) — house ad tho fill avutundi.
--------------------------------------------------------------------------- */
function VendorStrip() {
  const [ads, setAds] = useState<any[]>([]);
  const [cats, setCats] = useState<any[]>([]);

  useEffect(() => {
    fetch("/api/vendors/ads?slot=home_mid_strip&limit=4")
      .then((r) => r.json()).then((d) => setAds(d.ads || [])).catch(() => { });
    fetch("/api/vendors/categories")
      .then((r) => r.json()).then((d) => setCats((d.categories || []).slice(0, 10))).catch(() => { });
  }, []);

  return (
    <section className="max-w-7xl mx-auto px-4 py-8">
      <Reveal>
        <SectionHeading
          eyebrow="Wedding Vendors"
          title="🏪 Pelli ki kavalsina anni — okate chota"
          subtitle="Catering • Photography • Decorations • Function Hall • Tent House • Pandit • Jewellery • Makeup • DJ • Invitations • Cars • Planner. Verified vendors, direct WhatsApp, best rates."
          telugu
          align="center"
        />
      </Reveal>

      <div className="mt-5 flex flex-wrap gap-2 justify-center">
        {cats.map((c) => (
          <Link key={c.key} href={`/vendors?category=${c.key}`}
            className="px-3 py-1.5 rounded-full bg-white border border-gold/40 text-[12px] font-semibold text-maroon hover:bg-maroon-soft transition">
            {c.icon} {c.en}
          </Link>
        ))}
        <Link href="/vendors" className="px-3 py-1.5 rounded-full maroon-gradient text-white text-[12px] font-bold">
          Anni 18 categories →
        </Link>
      </div>

      {ads.length > 0 && (
        <div className="mt-5 grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {ads.map((a) => (
            <div key={a.vendor_id} className="bg-white rounded-3xl border border-gold/30 card-shadow p-4 flex flex-col">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <div className="text-lg">{a.icon}</div>
                  <div className="font-bold text-maroon text-[14px] truncate">{a.business_name}</div>
                  <div className="text-[11px] text-gray-600">{a.category_te}</div>
                  <div className="text-[11px] text-gray-500">📍 {a.city}</div>
                </div>
                {a.verified && <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5">✅ Verified</span>}
              </div>
              {a.price_range && <div className="mt-2 text-[11px] font-semibold text-maroon">💰 {a.price_range}</div>}
              <div className="mt-auto pt-3 flex gap-2">
                {a.whatsapp_link && (
                  <a href={a.whatsapp_link} target="_blank" rel="noreferrer"
                    className="flex-1 text-center bg-green-600 text-white font-bold text-[11px] px-3 py-2 rounded-xl">💬 WhatsApp</a>
                )}
                <Link href={a.detail_url || "/vendors"} className="flex-1 text-center border border-maroon/25 text-maroon font-bold text-[11px] px-3 py-2 rounded-xl">
                  Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-5 bg-navy text-white rounded-3xl p-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="font-bold">Mee business kooda promote cheyyali anthena? 🏪</div>
          <div className="text-[12px] opacity-90 mt-0.5">
            ₹149 nunchi — 52 channels + WhatsApp lanes + website banner + leads direct mee WhatsApp ki.
          </div>
        </div>
        <Link href="/vendors/register" className="gold-gradient text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
          Advertise cheyyandi →
        </Link>
      </div>
    </section>
  );
}
