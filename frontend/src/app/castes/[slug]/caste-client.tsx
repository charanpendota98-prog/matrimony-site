"use client";

/** /castes/[slug] body — neat Telugu / clean English via toggle (SEO shell stays server). */
import Link from "next/link";
import { CASTES, DISTRICTS, buildSlug } from "@/lib/seo-pages";
import { CHANNEL_STATS } from "@/lib/channels";
import { useLang } from "@/lib/lang";

type Caste = {
  key: string; name: string; split?: boolean;
  username?: string; link?: string;
  bride?: { username?: string; link?: string };
  groom?: { username?: string; link?: string };
};
type District = { slug: string; name: string; state: string };
type Chan = {
  name?: string; username?: string; link?: string; deepLink?: string;
  desc?: string; live?: boolean; wave?: number; hashtags?: string[];
};

export default function CasteClient({ caste, role, district, chan, otherChan }: {
  caste: Caste; role: "bride" | "groom"; district: District | null;
  chan: Chan | null; otherChan: Chan | null;
}) {
  const { lang } = useLang();
  const te = lang === "te";
  const otherRole = role === "bride" ? "groom" : "bride";
  const roleTelugu = role === "bride" ? "పెళ్లి కూతురు (Bride)" : "పెళ్లి కొడుకు (Groom)";
  const roleEn = role === "bride" ? "Bride" : "Groom";
  const where = district ? `${district.name}, ${district.state}` : te ? "Telangana + Andhra Pradesh" : "Telangana + Andhra Pradesh";
  const sameCasteOtherRole = buildSlug(caste.key, role === "bride" ? "groom" : "bride", district?.slug);

  return (
    <main className="min-h-screen">
      <section className="maroon-gradient text-white">
        <div className="max-w-5xl mx-auto px-4 py-10">
          <nav className="text-[11px] opacity-90 flex gap-2 flex-wrap">
            <Link href="/" className="underline">{te ? "Home" : "Home"}</Link><span>/</span>
            <Link href="/castes" className="underline">{te ? "Castes" : "Castes"}</Link><span>/</span>
            <span>{caste.name} {role}</span>
          </nav>
          <h1 className="mt-3 text-2xl md:text-4xl font-bold">
            {caste.name} {role === "bride" ? "Bride" : "Groom"} Matrimony — {district ? district.name : "TS & AP"}
          </h1>
          <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
            {te ? (
              <>{caste.name} {roleTelugu} సంబంధాలు — {where}. 100% verified Telugu profiles, caste-wise Telegram channel
                (<b>{chan?.username}</b>) + WhatsApp లో interest పంపండి. 🚫 Chatting లేదు — accept అయితే direct number exchange.</>
            ) : (
              <>{caste.name} {roleEn} matches — {where}. 100% verified Telugu profiles, caste-wise Telegram channel
                (<b>{chan?.username}</b>) + send interest on WhatsApp. 🚫 No chatting — direct number exchange on accept.</>
            )}
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <Link href="/register" className="gold-gradient text-maroon font-bold text-sm px-5 py-3 rounded-xl hover-lift">
              {te ? "📝 FREE register — 3 నిమిషాలు" : "📝 Register FREE — 3 minutes"}
            </Link>
            <a href={chan?.link} target="_blank" rel="noreferrer" className="bg-white/10 border border-white/25 font-bold text-sm px-5 py-3 rounded-xl">
              📢 {chan?.username} {te ? "channel" : "channel"}
            </a>
            <Link href="/requests" className="bg-white/10 border border-white/25 font-bold text-sm px-5 py-3 rounded-xl">
              {te ? "💌 Requests dashboard" : "💌 Requests dashboard"}
            </Link>
          </div>
          <div className="mt-4 flex flex-wrap gap-2 text-[11px] font-bold">
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">✅ OTP + DOB verified</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">🔒 Photo-private mode</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">💰 ₹99 → 5 profiles</span>
            <span className="bg-white/10 border border-white/20 px-3 py-1 rounded-full">
              {te ? "↩️ Decline = refund" : "↩️ Decline = refund"}
            </span>
          </div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-4 py-8 grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <section className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <h2 className="text-lg font-bold text-maroon">
              {te ? <>{caste.name} {role === "bride" ? "Brides" : "Grooms"} ని ఎలా చూడాలి?</>
                  : <>How to see {caste.name} {role === "bride" ? "Brides" : "Grooms"}?</>}
            </h2>
            <ol className="mt-3 space-y-2 text-[13px] text-gray-700 list-decimal list-inside">
              {te ? (
                <>
                  <li><b>FREE register</b> (3 నిమిషాలు) — personal, family, caste/astro, education, location + photo.</li>
                  <li><b>Auto-post:</b> మీ profile card {chan?.username} channel లో + WhatsApp group లో (anti-ban safe).</li>
                  <li><b>💌 Interest పంపండి:</b> నచ్చిన profile కి — వాళ్లకి మన WhatsApp నుంచి మీ profile card వెళ్తుంది.</li>
                  <li><b>✅ Accept అయితే:</b> రెండు numbers automatic గా exchange ({role === "bride" ? "groom" : "bride"} side consent తో).</li>
                </>
              ) : (
                <>
                  <li><b>Register FREE</b> (3 minutes) — personal, family, caste/astro, education, location + photo.</li>
                  <li><b>Auto-post:</b> your profile card goes to the {chan?.username} channel + WhatsApp group (anti-ban safe).</li>
                  <li><b>💌 Send interest:</b> to profiles you like — they get your profile card from our WhatsApp.</li>
                  <li><b>✅ On accept:</b> both numbers exchange automatically (with the {role === "bride" ? "groom" : "bride"} side&apos;s consent).</li>
                </>
              )}
            </ol>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href="/register" className="maroon-gradient text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">
                {te ? "Register FREE" : "Register FREE"}
              </Link>
              <Link href={`/castes/${sameCasteOtherRole}`} className="border border-maroon/30 text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
                {te ? <>{caste.name} {role === "bride" ? "Grooms" : "Brides"} చూడండి →</>
                    : <>See {caste.name} {role === "bride" ? "Grooms" : "Brides"} →</>}
              </Link>
            </div>
          </section>

          <section className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <h2 className="text-lg font-bold text-maroon">
              {te ? <>ఎందుకు caste-wise channel ({caste.name})?</> : <>Why a caste-wise channel ({caste.name})?</>}
            </h2>
            {caste.split ? (
              <div className="mt-2 bg-white border border-gold/30 rounded-2xl p-3 text-[12px] text-gray-700">
                {te ? (
                  <>⭐ <b>{caste.name} కి bride + groom channels separate గా ఉన్నాయి</b> (caste ప్రకారం) —{" "}
                    {role === "bride" ? "మీరు ఇప్పుడు చూస్తున్నది" : "bride page"} <b>{chan?.username}</b>,{" "}
                    {role === "bride" ? "groom" : "మీ"} page <b>{otherChan?.username}</b>.{" "}
                    <Link className="underline font-bold text-maroon" href={`/castes/${buildSlug(caste.key, otherRole, district?.slug)}`}>
                      {otherRole === "bride" ? "Brides" : "Grooms"} page చూడండి →
                    </Link></>
                ) : (
                  <>⭐ <b>{caste.name} has separate bride + groom channels</b> (caste-wise) —{" "}
                    {role === "bride" ? "you are viewing" : "the bride page"} <b>{chan?.username}</b>,{" "}
                    {role === "bride" ? "the groom" : "your"} page is <b>{otherChan?.username}</b>.{" "}
                    <Link className="underline font-bold text-maroon" href={`/castes/${buildSlug(caste.key, otherRole, district?.slug)}`}>
                      See {otherRole === "bride" ? "Brides" : "Grooms"} page →
                    </Link></>
                )}
              </div>
            ) : null}
            <p className="mt-2 text-[13px] text-gray-700 leading-relaxed">
              {te ? (
                <>మన <b>{CHANNEL_STATS.by_tier.L3_CASTE} caste channels</b> లో ఇది ఒకటి — {caste.name} families కి
                  same community సంబంధాలు వెతుక్కోవడం easy అవుతుంది. Region (TS/AP) + religion + job (software, doctor, govt)
                  channels కూడా కలిసి <b>{CHANNEL_STATS.total} channels</b> network లో మీ profile అన్ని related చోటకి వెళ్తుంది —
                  ఒక్క register తో maximum reach. {chan?.desc}</>
              ) : (
                <>This is one of our <b>{CHANNEL_STATS.by_tier.L3_CASTE} caste channels</b> — it makes finding
                  same-community matches easy for {caste.name} families. Together with region (TS/AP) + religion + job (software, doctor, govt)
                  channels, your profile reaches every related corner of the <b>{CHANNEL_STATS.total}-channel</b> network —
                  maximum reach with one registration. {chan?.desc}</>
              )}
            </p>
            <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
              {(chan?.hashtags || []).slice(0, 6).map((h) => (
                <span key={h} className="bg-cream border border-gold/30 px-2 py-0.5 rounded-full text-gray-700">{h}</span>
              ))}
            </div>
          </section>

          <RelatedDistricts
            te={te} casteKey={caste.key} casteName={caste.name} role={role}
            districtSlug={district?.slug} districtName={district?.name} />
        </div>

        <aside className="space-y-4">
          <div className="bg-navy text-white rounded-2xl p-5">
            <div className="font-bold">{chan?.name}</div>
            <div className="text-[12px] opacity-85 mt-1">{chan?.username}</div>
            <div className="text-[11px] opacity-70 mt-1">
              {chan?.live ? "🟢 Live" : te ? `🟡 Wave-${chan?.wave || 1} లో open అవుతుంది` : `🟡 Opens in Wave-${chan?.wave || 1}`} • {(chan?.hashtags || []).length} hashtags
            </div>
            <a href={chan?.deepLink} target="_blank" rel="noreferrer"
              className="mt-3 block text-center gold-gradient text-maroon font-bold text-[12px] py-2.5 rounded-xl">
              {te ? "🤖 Bot తో join అవ్వండి" : "🤖 Join via bot"}
            </a>
            <Link href="/channels" className="mt-2 block text-center border border-white/25 text-white font-bold text-[12px] py-2.5 rounded-xl">
              {te ? <>అన్ని {CHANNEL_STATS.total} channels →</> : <>All {CHANNEL_STATS.total} channels →</>}
            </Link>
          </div>

          <RelatedCastes te={te} casteKey={caste.key} role={role} districtSlug={district?.slug} />

          <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
            <div className="font-bold text-maroon text-[14px]">
              {te ? "Pricing (chatting లేదు)" : "Pricing (no chatting)"}
            </div>
            <ul className="mt-2 text-[12px] text-gray-700 space-y-1">
              <li>{te ? <>🎁 మొదటి <b>3 interest requests FREE</b></> : <>🎁 First <b>3 interest requests FREE</b></>}</li>
              <li>₹99 → <b>5 profiles</b> (₹20/profile)</li>
              <li>₹199 → <b>12 profiles</b> + verified badge</li>
              <li>₹299 → <b>25 profiles</b> + who-viewed-me</li>
              <li>₹499 → <b>50 profiles</b> + matchmaker assist</li>
            </ul>
            <Link href="/requests" className="mt-3 block text-center maroon-gradient text-white font-bold text-[12px] py-2.5 rounded-xl">
              {te ? "Plans చూడండి →" : "See plans →"}
            </Link>
          </div>
        </aside>
      </div>

      <section className="max-w-5xl mx-auto px-4 pb-10">
        <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
          <h2 className="text-lg font-bold text-maroon">{caste.name} {role} — FAQ</h2>
          <div className="mt-3 space-y-3 text-[13px]">
            <div>
              <div className="font-bold text-ink">{te ? "Charge ఎంత?" : "How much does it cost?"}</div>
              <div className="text-gray-600">
                {te ? "Register FREE. మొదటి 3 interest requests FREE. తర్వాత ₹99 → 5 profiles (₹20/profile), ₹499 → 50 (₹10/profile)."
                    : "Registration is FREE. First 3 interest requests FREE. Then ₹99 → 5 profiles (₹20/profile), ₹499 → 50 (₹10/profile)."}
              </div>
            </div>
            <div>
              <div className="font-bold text-ink">{te ? "Chatting ఉందా?" : "Is there chatting?"}</div>
              <div className="text-gray-600">
                {te ? "లేదు. 💌 Interest పంపండి → వాళ్లకి WhatsApp లో మీ profile → accept అయితే numbers exchange. Decline అయితే credit refund."
                    : "No. 💌 Send interest → they get your profile on WhatsApp → numbers exchange on accept. Credit refund on decline."}
              </div>
            </div>
            <div>
              <div className="font-bold text-ink">{te ? "నా profile ఎక్కడ post అవుతుంది?" : "Where does my profile get posted?"}</div>
              <div className="text-gray-600">
                {te ? <>{chan?.username} + మీ district/region channel + job/education special channel (max 5 channels) — Telegram + WhatsApp రెండు చోట్లా.</>
                    : <>{chan?.username} + your district/region channel + job/education special channel (max 5 channels) — on both Telegram + WhatsApp.</>}
              </div>
            </div>
            <div>
              <div className="font-bold text-ink">
                {te ? <>{caste.name} porutham check ఉందా?</> : <>Is there {caste.name} porutham check?</>}
              </div>
              <div className="text-gray-600">
                {te ? "అవును — 10 porutham (rasi, nakshatra, gana, yoni, rajju, vedha…) report free గా /requests లో చూడొచ్చు."
                    : "Yes — the 10-porutham (rasi, nakshatra, gana, yoni, rajju, vedha…) report is free to view in /requests."}
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function RelatedDistricts({ te, casteKey, casteName, role, districtSlug, districtName }: {
  te: boolean; casteKey: string; casteName: string; role: "bride" | "groom";
  districtSlug?: string; districtName?: string;
}) {
  const related = DISTRICTS.filter((d) => d.slug !== districtSlug).slice(0, 10);
  return (
    <section className="bg-cream rounded-2xl p-5 border border-gold/30">
      <h2 className="text-lg font-bold text-maroon">
        {districtName || "TS/AP"} {te ? "districts" : "districts"} — {casteName} {te ? "సంబంధాలు" : "matches"}
      </h2>
      <div className="mt-3 flex flex-wrap gap-2">
        {related.map((d) => (
          <Link key={d.slug} href={`/castes/${buildSlug(casteKey, role, d.slug)}`}
            className="text-[12px] bg-white border border-gold/30 rounded-full px-3 py-1.5 hover-lift">
            {casteName} {role} {d.name}
          </Link>
        ))}
      </div>
    </section>
  );
}

function RelatedCastes({ te, casteKey, role, districtSlug }: {
  te: boolean; casteKey: string; role: "bride" | "groom"; districtSlug?: string;
}) {
  const related = CASTES.filter((c) => c.key !== casteKey).slice(0, 10);
  return (
    <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
      <div className="font-bold text-maroon text-[14px]">{te ? "వేరే castes" : "Other castes"}</div>
      <div className="mt-2 flex flex-wrap gap-1.5">
        {related.map((c) => (
          <Link key={c.key} href={`/castes/${buildSlug(c.key, role, districtSlug)}`}
            className="text-[11px] bg-cream border border-gold/25 rounded-full px-2.5 py-1">
            {c.name}
          </Link>
        ))}
      </div>
      <Link href="/castes" className="mt-3 block text-[12px] font-bold text-maroon underline">
        {te ? "అన్ని castes చూడండి →" : "See all castes →"}
      </Link>
    </div>
  );
}
