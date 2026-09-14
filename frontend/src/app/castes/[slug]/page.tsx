/**
 * SEO landing page — /castes/reddy-bride-hyderabad
 * =================================================
 * Google lo "reddy bride hyderabad matrimony" search ki idi rank avuthundi.
 * Content: caste + role + district batti unique ga generate avutundi (SSR — fast + crawlable).
 */
import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CASTES, DISTRICTS, buildSlug, parseSlug } from "@/lib/seo-pages";
import { CHANNEL_STATS } from "@/lib/channels";
import { SITE_CONFIG } from "@/lib/site-config";

type Params = { params: { slug: string } };

export function generateMetadata({ params }: Params): Metadata {
  const parsed = parseSlug(params.slug);
  if (!parsed) return { title: "Caste Matrimony Channels" };
  const { caste, role, district } = parsed;
  const where = district ? `${district.name} (${district.state})` : "Telangana & Andhra Pradesh";
  const title = `${caste.name} ${role === "bride" ? "Bride" : "Groom"} ${district ? district.name : "TS/AP"} Matrimony`;
  return {
    title,
    description: `${caste.name} ${role} profiles ${where} — Mana Vivaha (TSAP Matrimony). ${caste.username} channel lo verified profiles, WhatsApp lo interest pampu, ₹99 → 5 profiles. Modati 3 requests FREE. Chatting ledu — consent based contact.`,
    keywords: [
      `${caste.name.toLowerCase()} matrimony`, `${caste.name.toLowerCase()} bride ${district?.name || "hyderabad"}`,
      `${caste.name.toLowerCase()} groom`, `${caste.name.toLowerCase()} sambandham`,
      `telugu matrimony ${district?.name || "telangana"}`, "TSAP matrimony", "manavivaha",
    ],
    alternates: { canonical: `${SITE_CONFIG.siteUrl}/castes/${params.slug}` },
  };
}

export default function CasteLandingPage({ params }: Params) {
  const parsed = parseSlug(params.slug);
  if (!parsed) notFound();
  const { caste, role, district } = parsed;
  const roleTelugu = role === "bride" ? "పెళ్లి కూతురు (Bride)" : "పెళ్లి కొడుకు (Groom)";
  const where = district ? `${district.name}, ${district.state}` : "Telangana + Andhra Pradesh";

  const sameCasteOtherRole = buildSlug(caste.key, role === "bride" ? "groom" : "bride", district?.slug);
  const relatedDistricts = DISTRICTS.filter((d) => d.slug !== district?.slug).slice(0, 10);
  const relatedCastes = CASTES.filter((c) => c.key !== caste.key).slice(0, 10);

  return (
    <main className="min-h-screen">
      <section className="maroon-gradient text-white">
        <div className="max-w-5xl mx-auto px-4 py-10">
          <nav className="text-[11px] opacity-90 flex gap-2 flex-wrap">
            <Link href="/" className="underline">Home</Link><span>/</span>
            <Link href="/castes" className="underline">Castes</Link><span>/</span>
            <span>{caste.name} {role}</span>
          </nav>
          <h1 className="mt-3 text-2xl md:text-4xl font-bold">
            {caste.name} {role === "bride" ? "Bride" : "Groom"} Matrimony — {district ? district.name : "TS & AP"}
          </h1>
          <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
            {caste.name} {roleTelugu} సంబంధాలు — {where}. 100% verified Telugu profiles, caste-wise Telegram channel
            (<b>{caste.username}</b>) + WhatsApp lo interest pampu. 🚫 Chatting ledu — accept aithe direct number exchange.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <Link href="/register" className="gold-gradient text-maroon font-bold text-sm px-5 py-3 rounded-xl hover-lift">
              📝 FREE register — 3 nimushalu
            </Link>
            <a href={caste.link} target="_blank" rel="noreferrer" className="bg-white/10 border border-white/25 font-bold text-sm px-5 py-3 rounded-xl">
              📢 {caste.username} channel
            </a>
            <Link href="/requests" className="bg-white/10 border border-white/25 font-bold text-sm px-5 py-3 rounded-xl">
              💌 Requests dashboard
            </Link>
          </div>
          <div className="mt-4 flex flex-wrap gap-2 text-[11px] font-bold">
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">✅ OTP + DOB verified</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">🔒 Photo-private mode</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">💰 ₹99 → 5 profiles</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">↩️ Decline = refund</span>
          </div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-4 py-8 grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <section className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <h2 className="text-lg font-bold text-maroon">{caste.name} {role === "bride" ? "Brides" : "Grooms"} ni ela chudali?</h2>
            <ol className="mt-3 space-y-2 text-[13px] text-gray-700 list-decimal list-inside">
              <li><b>FREE register</b> (3 nimushalu) — personal, family, caste/astro, education, location + photo.</li>
              <li><b>Auto-post:</b> mee profile card {caste.username} channel lo + WhatsApp group lo (anti-ban safe).</li>
              <li><b>💌 Interest pampu:</b> nachhina profile ki — vaallaki mana WhatsApp nunchi mee profile card veltundi.</li>
              <li><b>✅ Accept aithe:</b> rendu numbers automatic ga exchange ({role === "bride" ? "groom" : "bride"} side consent tho).</li>
            </ol>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href="/register" className="maroon-gradient text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">Register FREE</Link>
              <Link href={`/castes/${sameCasteOtherRole}`} className="border border-maroon/30 text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
                {caste.name} {role === "bride" ? "Grooms" : "Brides"} chudu →
              </Link>
            </div>
          </section>

          <section className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <h2 className="text-lg font-bold text-maroon">Enduku caste-wise channel ({caste.name})?</h2>
            <p className="mt-2 text-[13px] text-gray-700 leading-relaxed">
              Mana <b>{CHANNEL_STATS.by_tier.L3_CASTE} caste channels</b> lo idi okati — {caste.name} families ki
              same community sambandhalu vetukovadam easy avutundi. Region (TS/AP) + religion + job (software, doctor, govt)
              channels kooda kalisi <b>{CHANNEL_STATS.total} channels</b> network lo mee profile anni related chotaki veltundi —
              okka register tho maximum reach. {caste.desc}
            </p>
            <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
              {caste.hashtags.slice(0, 6).map((h) => (
                <span key={h} className="bg-cream border border-gold/30 px-2 py-0.5 rounded-full text-gray-700">{h}</span>
              ))}
            </div>
          </section>

          <section className="bg-cream rounded-2xl p-5 border border-gold/30">
            <h2 className="text-lg font-bold text-maroon">{district ? `${district.name}` : "TS/AP"} districts — {caste.name} sambandhalu</h2>
            <div className="mt-3 flex flex-wrap gap-2">
              {relatedDistricts.map((d) => (
                <Link key={d.slug} href={`/castes/${buildSlug(caste.key, role, d.slug)}`}
                  className="text-[12px] bg-white border border-gold/30 rounded-full px-3 py-1.5 hover-lift">
                  {caste.name} {role} {d.name}
                </Link>
              ))}
            </div>
          </section>
        </div>

        <aside className="space-y-4">
          <div className="bg-navy text-white rounded-2xl p-5">
            <div className="font-bold">{caste.full}</div>
            <div className="text-[12px] opacity-85 mt-1">{caste.username}</div>
            <div className="text-[11px] opacity-70 mt-1">{caste.live ? "🟢 Live" : "🟡 Wave-1 lo open avutundi"} • {caste.hashtags.length} hashtags</div>
            <a href={caste.deepLink} target="_blank" rel="noreferrer"
              className="mt-3 block text-center gold-gradient text-maroon font-bold text-[12px] py-2.5 rounded-xl">
              🤖 Bot tho join avvandi
            </a>
            <Link href="/channels" className="mt-2 block text-center border border-white/25 text-white font-bold text-[12px] py-2.5 rounded-xl">
              Anni {CHANNEL_STATS.total} channels →
            </Link>
          </div>

          <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <div className="font-bold text-maroon text-[14px]">Vere castes</div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {relatedCastes.map((c) => (
                <Link key={c.key} href={`/castes/${buildSlug(c.key, role, district?.slug)}`}
                  className="text-[11px] bg-cream border border-gold/25 rounded-full px-2.5 py-1">
                  {c.name}
                </Link>
              ))}
            </div>
            <Link href="/castes" className="mt-3 block text-[12px] font-bold text-maroon underline">Anni castes chudu →</Link>
          </div>

          <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <div className="font-bold text-maroon text-[14px]">Pricing (chatting ledu)</div>
            <ul className="mt-2 text-[12px] text-gray-700 space-y-1">
              <li>🎁 Modati <b>3 interest requests FREE</b></li>
              <li>₹99 → <b>5 profiles</b> (₹20/profile)</li>
              <li>₹199 → <b>12 profiles</b> + verified badge</li>
              <li>₹299 → <b>25 profiles</b> + who-viewed-me</li>
              <li>₹499 → <b>50 profiles</b> + matchmaker assist</li>
            </ul>
            <Link href="/requests" className="mt-3 block text-center maroon-gradient text-white font-bold text-[12px] py-2.5 rounded-xl">
              Plans chudu →
            </Link>
          </div>
        </aside>
      </div>

      <section className="max-w-5xl mx-auto px-4 pb-10">
        <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
          <h2 className="text-lg font-bold text-maroon">{caste.name} {role} — FAQ</h2>
          <div className="mt-3 space-y-3 text-[13px]">
            <div>
              <div className="font-bold text-ink">Charge entha?</div>
              <div className="text-gray-600">Register FREE. Modati 3 interest requests FREE. Tarvata ₹99 → 5 profiles (₹20/profile), ₹499 → 50 (₹10/profile).</div>
            </div>
            <div>
              <div className="font-bold text-ink">Chatting unda?</div>
              <div className="text-gray-600">Ledu. 💌 Interest pampu → vaallaki WhatsApp lo mee profile → accept aithe numbers exchange. Decline aithe credit refund.</div>
            </div>
            <div>
              <div className="font-bold text-ink">Naa profile ekkada post avutundi?</div>
              <div className="text-gray-600">{caste.username} + mee district/region channel + job/education special channel (max 5 channels) — Telegram + WhatsApp rendu chotla.</div>
            </div>
            <div>
              <div className="font-bold text-ink">{caste.name} porutham check unda?</div>
              <div className="text-gray-600">Avunu — 10 porutham (rasi, nakshatra, gana, yoni, rajju, vedha…) report free ga /requests lo chudochu.</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
