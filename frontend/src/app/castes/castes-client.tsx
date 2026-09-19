"use client";

/** /castes body — neat Telugu / clean English via toggle (SEO shell stays server). */
import Link from "next/link";
import Reveal from "@/components/Reveal";
import SectionHeading from "@/components/SectionHeading";
import { CASTES, buildSlug } from "@/lib/seo-pages";
import { CHANNEL_STATS } from "@/lib/channels";
import { waLink } from "@/lib/wa";
import { TelegramIcon, WhatsAppIcon } from "@/components/BrandIcons";
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
              🔎 OC • BC • SC • ST — {te ? "అన్ని కులాలు" : "all castes"} • {CHANNEL_STATS.by_tier.L3_CASTE} {te ? "caste channels" : "caste channels"}
            </div>
            <h1 className="mt-3 text-2xl md:text-4xl font-bold">
              {te ? "కులాల వారీగా — అన్ని కులాలు" : "Caste-wise — all castes"}
            </h1>
            <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
              {te ? (
                <>మీ caste select చెయ్యండి — ఆ community bride/groom సంబంధాలు, channel, porutham report,
                  pricing అంతా ఒక్క page లో. OC, BC, SC, ST — అన్ని castes cover ({CHANNEL_STATS.by_tier.L3_CASTE} channels).</>
              ) : (
                <>Select your caste — that community&apos;s bride/groom matches, channel, porutham report and
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
          subtitle={te ? "ప్రతి caste కి bride + groom channels ఉన్నాయి — register చేస్తే మీ profile అక్కడికి వెళ్తుంది." : "Bride + groom channels for every caste — your profile goes there on register."}
          telugu
        />

        <div className="mt-5 grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {CASTES.map((c, i) => (
            <Reveal key={c.key} delay={(i % 6) * 50}>
              <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 h-full">
                <div className="flex items-center justify-between gap-2">
                  <div className="font-bold text-maroon text-[15px]">{c.name}</div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${c.live ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}`}>
                    {c.live ? "🟢 Live" : (te ? "త్వరలో" : "Soon")}
                  </span>
                </div>
                <div className="mt-3 space-y-1.5">
                  <div className="flex items-center gap-1.5">
                    <Link href={`/castes/${buildSlug(c.key, "bride")}`}
                      className="flex-1 text-center text-[12px] font-bold maroon-gradient text-white px-3 py-2 rounded-xl hover-lift">
                      {te ? "👰 వధువులు" : "👰 Brides"}
                    </Link>
                    <a href={c.bride?.link || c.link} target="_blank" rel="noreferrer" aria-label={(te ? "వధువుల Telegram" : "Brides Telegram")}
                      className="grid place-items-center w-9 h-9 rounded-full bg-[#229ED9] text-white shadow-soft hover:brightness-110 active:scale-95 transition">
                      <TelegramIcon className="w-4 h-4" mono />
                    </a>
                    {waLink(c.bride?.key || c.key) ? (
                      <a href={waLink(c.bride?.key || c.key)} target="_blank" rel="noreferrer" aria-label={(te ? "వధువుల WhatsApp" : "Brides WhatsApp")}
                        className="grid place-items-center w-9 h-9 rounded-full bg-[#25D366] text-white shadow-soft hover:brightness-110 active:scale-95 transition">
                        <WhatsAppIcon className="w-4 h-4" mono />
                      </a>
                    ) : null}
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Link href={`/castes/${buildSlug(c.key, "groom")}`}
                      className="flex-1 text-center text-[12px] font-bold border border-maroon/30 text-maroon px-3 py-2 rounded-xl hover-lift">
                      {te ? "🤵 వరులు" : "🤵 Grooms"}
                    </Link>
                    <a href={c.groom?.link || c.bride?.link || c.link} target="_blank" rel="noreferrer" aria-label={(te ? "వరుల Telegram" : "Grooms Telegram")}
                      className="grid place-items-center w-9 h-9 rounded-full bg-[#229ED9] text-white shadow-soft hover:brightness-110 active:scale-95 transition">
                      <TelegramIcon className="w-4 h-4" mono />
                    </a>
                    {waLink(c.groom?.key) ? (
                      <a href={waLink(c.groom?.key)} target="_blank" rel="noreferrer" aria-label={(te ? "వరుల WhatsApp" : "Grooms WhatsApp")}
                        className="grid place-items-center w-9 h-9 rounded-full bg-[#25D366] text-white shadow-soft hover:brightness-110 active:scale-95 transition">
                        <WhatsAppIcon className="w-4 h-4" mono />
                      </a>
                    ) : null}
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
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
