"use client";

/** /castes body — neat Telugu / clean English via toggle (SEO shell stays server). */
import Link from "next/link";
import Reveal from "@/components/Reveal";
import SectionHeading from "@/components/SectionHeading";
import { CASTES, DISTRICTS, SEO_PAGE_COUNT, buildSlug } from "@/lib/seo-pages";
import { CHANNEL_STATS } from "@/lib/channels";
import { useLang } from "@/lib/lang";

export default function CastesClient() {
  const { lang } = useLang();
  const te = lang === "te";
  return (
    <main className="min-h-screen">
      <section className="maroon-gradient text-white">
        <div className="max-w-6xl mx-auto px-4 py-10">
          <Reveal>
            <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-3 py-1 text-[11px] font-bold">
              🔎 {SEO_PAGE_COUNT}+ {te ? "caste pages" : "caste pages"} • {CHANNEL_STATS.by_tier.L3_CASTE} {te ? "caste channels" : "caste channels"}
            </div>
            <h1 className="mt-3 text-2xl md:text-4xl font-bold">
              {te ? "కులాల వారీగా — అన్ని కులాలు" : "Caste-wise — all castes"}
            </h1>
            <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
              {te ? (
                <>మీ caste + district select చెయ్యండి — ఆ community bride/groom profiles, channel, porutham report,
                  pricing అంతా ఒక్క page లో. OC, BC, SC, ST — అన్ని castes cover ({CHANNEL_STATS.by_tier.L3_CASTE} channels).</>
              ) : (
                <>Select your caste + district — that community&apos;s bride/groom profiles, channel, porutham report and
                  pricing all on one page. OC, BC, SC, ST — all castes covered ({CHANNEL_STATS.by_tier.L3_CASTE} channels).</>
              )}
            </p>
          </Reveal>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <SectionHeading
          eyebrow={te ? "మీ caste" : "Your caste"}
          title={te ? "Caste select చెయ్యండి" : "Select your caste"}
          subtitle={te ? "ప్రతి caste కి bride + groom pages — district-wise links కూడా ఉన్నాయి." : "Bride + groom pages for every caste — with district-wise links too."}
          telugu
        />

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
                    className="text-[12px] font-bold maroon-gradient text-white px-3 py-1.5 rounded-full">
                    {te ? "👰 Brides (వధువులు)" : "👰 Brides"}
                  </Link>
                  <Link href={`/castes/${buildSlug(c.key, "groom")}`}
                    className="text-[12px] font-bold border border-maroon/30 text-maroon px-3 py-1.5 rounded-full">
                    {te ? "🤵 Grooms (వరులు)" : "🤵 Grooms"}
                  </Link>
                  <a href={c.bride?.link || c.link} target="_blank" rel="noreferrer" className="text-[12px] font-bold text-gray-600 px-2 py-1.5">
                    {te ? "channel →" : "channel →"}
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
          <div className="font-bold text-maroon">{te ? "District-wise pages" : "District-wise pages"}</div>
          <div className="mt-3 flex flex-wrap gap-2">
            {DISTRICTS.map((d) => (
              <Link key={d.slug} href={`/castes/${buildSlug("reddy", "bride", d.slug)}`}
                className="text-[12px] bg-white border border-gold/30 rounded-full px-3 py-1.5">
                {d.name} ({d.state})
              </Link>
            ))}
          </div>
          <div className="mt-3 text-[11px] text-gray-600">
            {te ? "ప్రతి caste × district × bride/groom కి separate page ఉంది — Google లో మీ district సంబంధాలు easy గా దొరుకుతాయి."
                : "A separate page for every caste × district × bride/groom — your district matches are easy to find on Google."}
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-2">
          <Link href="/register" className="maroon-gradient text-white font-bold px-5 py-3 rounded-xl">
            {te ? "📝 FREE register" : "📝 Register FREE"}
          </Link>
          <Link href="/channels" className="border border-maroon/30 text-maroon font-bold px-5 py-3 rounded-xl">
            📢 {CHANNEL_STATS.total} {te ? "channels" : "channels"}
          </Link>
          <Link href="/requests" className="border border-maroon/30 text-maroon font-bold px-5 py-3 rounded-xl">
            {te ? "💌 Requests + porutham" : "💌 Requests + porutham"}
          </Link>
        </div>
      </div>
    </main>
  );
}
