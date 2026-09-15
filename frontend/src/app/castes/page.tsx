/**
 * /castes — SEO hub: anni 43 caste pages ki index (Google crawl + internal linking)
 */
import Link from "next/link";
import type { Metadata } from "next";
import Reveal from "@/components/Reveal";
import SectionHeading from "@/components/SectionHeading";
import { CASTES, DISTRICTS, SEO_PAGE_COUNT, buildSlug } from "@/lib/seo-pages";
import { CHANNEL_STATS } from "@/lib/channels";

export const metadata: Metadata = {
  title: "Caste-wise Telugu Matrimony Channels — 43 Castes (TS & AP)",
  description:
    "Reddy, Kamma, Kapu, Velama, Vysya, Brahmin, Yadav, Mala, Madiga, Lambada… 43 caste-wise Telugu matrimony channels. Bride & groom profiles, district-wise pages, WhatsApp interest model. Mana Vivaha (TSAP Matrimony).",
  keywords: ["caste wise matrimony", "telugu caste matrimony", "reddy matrimony", "kamma matrimony",
             "mala matrimony", "madiga matrimony", "lambada matrimony", "tsap matrimony"],
  alternates: { canonical: "https://manavivaha.in/castes" },
};

export default function CastesHub() {
  return (
    <main className="min-h-screen">
      <section className="maroon-gradient text-white">
        <div className="max-w-6xl mx-auto px-4 py-10">
          <Reveal>
            <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-3 py-1 text-[11px] font-bold">
              🔎 {SEO_PAGE_COUNT}+ caste pages • {CHANNEL_STATS.by_tier.L3_CASTE} caste channels
            </div>
            <h1 className="mt-3 text-2xl md:text-4xl font-bold">Caste-wise Telugu Matrimony — Anni Castes</h1>
            <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
              Mee caste + district select cheyyandi — aa community bride/groom profiles, channel, porutham report,
              pricing antha okka page lo. OC, BC, SC, ST — anni castes cover ({CHANNEL_STATS.by_tier.L3_CASTE} channels).
            </p>
          </Reveal>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <SectionHeading eyebrow="Mee caste" title="Caste select cheyyandi" subtitle="Prati caste ki bride + groom pages — district-wise links kooda unnayi." telugu />

        <div className="mt-5 grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {CASTES.map((c, i) => (
            <Reveal key={c.key} delay={(i % 6) * 50}>
              <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 h-full">
                <div className="flex items-center justify-between gap-2">
                  <div className="font-bold text-maroon text-[15px]">{c.name}</div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${c.live ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}`}>
                    {c.live ? "🟢 Live" : "Wave-1"}
                  </span>
                </div>
                <div className="text-[11px] text-gray-500 mt-1">
                  {c.split ? `${c.bride?.username} • ${c.groom?.username}` : c.username}
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Link href={`/castes/${buildSlug(c.key, "bride")}`}
                    className="text-[12px] font-bold maroon-gradient text-white px-3 py-1.5 rounded-full">👰 Brides</Link>
                  <Link href={`/castes/${buildSlug(c.key, "groom")}`}
                    className="text-[12px] font-bold border border-maroon/30 text-maroon px-3 py-1.5 rounded-full">🤵 Grooms</Link>
                  <a href={c.bride?.link || c.link} target="_blank" rel="noreferrer" className="text-[12px] font-bold text-gray-600 px-2 py-1.5">
                    channel →
                  </a>
                </div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {DISTRICTS.slice(0, 5).map((d) => (
                    <Link key={d.slug} href={`/castes/${buildSlug(c.key, "bride", d.slug)}`}
                      className="text-[10px] bg-cream border border-gold/25 rounded-full px-2 py-0.5 text-gray-600">
                      {c.name} {d.name}
                    </Link>
                  ))}
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        <div className="mt-8 bg-cream border border-gold/30 rounded-2xl p-5">
          <div className="font-bold text-maroon">District-wise pages</div>
          <div className="mt-3 flex flex-wrap gap-2">
            {DISTRICTS.map((d) => (
              <Link key={d.slug} href={`/castes/${buildSlug("reddy", "bride", d.slug)}`}
                className="text-[12px] bg-white border border-gold/30 rounded-full px-3 py-1.5">
                {d.name} ({d.state})
              </Link>
            ))}
          </div>
          <div className="mt-3 text-[11px] text-gray-600">
            Prati caste × district × bride/groom ki separate page undi — Google lo mee district sambandhalu easy ga dorukutayi.
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-2">
          <Link href="/register" className="maroon-gradient text-white font-bold px-5 py-3 rounded-xl">📝 FREE register</Link>
          <Link href="/channels" className="border border-maroon/30 text-maroon font-bold px-5 py-3 rounded-xl">📢 {CHANNEL_STATS.total} channels</Link>
          <Link href="/requests" className="border border-maroon/30 text-maroon font-bold px-5 py-3 rounded-xl">💌 Requests + porutham</Link>
        </div>
      </div>
    </main>
  );
}
