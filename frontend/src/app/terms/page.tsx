import Link from "next/link";
import { SITE_CONFIG } from "@/lib/site-config";

/** 📄 TERMS OF USE — Matrimony service ni safe ga, legal ga nadapadaniki. */
export const metadata = {
  title: "Terms of Use | Mana Vivaha (TSAP Matrimony)",
  description: "Mana Vivaha service terms — eligibility, requests policy, prohibited conduct, fees, liability, governing law.",
};

const LAST_UPDATED = "14 Sep 2026";

export default function TermsPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl md:text-3xl font-extrabold text-[#7A0C2E] telugu">📄 Terms of Use (Seva Niyamalu)</h1>
      <div className="text-xs text-gray-500 mt-1">Last updated: {LAST_UPDATED} • {SITE_CONFIG.legalName} ({SITE_CONFIG.domain})</div>

      <Section title="1. Ee service enti">
        <ul>
          <li>Mana Vivaha (TSAP Matrimony) oka <b>Telugu matrimony platform</b> — Telangana, Andhra Pradesh &
            other-state/NRI Telugu families ki <b>profiles + channels + WhatsApp sharing</b> service.</li>
          <li>Manam <b>broker kaadu, marriage guarantee ivvamu</b> — mana pani: correct profiles ni correct families ki cherchadam,
            safe & respect tho.</li>
          <li>Website: {SITE_CONFIG.domain} • Telegram channels (52) • WhatsApp sharing • Bot: {SITE_CONFIG.botUsername}</li>
        </ul>
      </Section>

      <Section title="2. Eligibility (evaru join avvachu)">
        <ul>
          <li>Bride: <b>18+</b> మరియు Groom: <b>21+</b> (Indian marriage law prakaram).</li>
          <li>Profile ni <b>sva-ichcha tho</b> (own will) create cheyyali — family tho cheppina OK, kaani <b>vaalla permission tho</b>.</li>
          <li>Okka vyakti ki — okka <b>active profile matrame</b> (duplicate profiles ban avutayi).</li>
          <li>Adhar/PAN/photo verification adagochu (trust kosam) — ivvakapote profile <b>limited reach</b> lo untundi.</li>
        </ul>
      </Section>

      <Section title="3. Mee responsibility (profile & content)">
        <ul>
          <li>Icche details <b>nijam</b> ga undali — age, marital status, job, income, caste, photo.</li>
          <li>Fake photos, other person photos, morphed images → <b>immediate ban</b> + legal action.</li>
          <li>Mee profile ki copyright mee de. Profile post ni mana channels/WhatsApp lo promote cheyyadaniki
            <b>permission isthunnaru</b> (name, photo, details tho — mee privacy settings batti).</li>
          <li>Photo private mode / watermark — ee options unnai, mee istam.</li>
        </ul>
      </Section>

      <Section title="4. Requests policy (chatting ledu)">
        <ul>
          <li><b>Chatting / DM feature ledu</b> — spam & mosam aapadaniki ide mana design.</li>
          <li>Meeru pampina <b>request</b> — target ki mee profile + card WhatsApp lo velthundi (mana official number nunchi).</li>
          <li>Numbers <b>rendu vaipula oppuka tarvate</b> share avutayi. Declined ayina vaalla number eppudu ivvamu.</li>
          <li>Okka request = okka credit. Decline/no-response (7 రోజులు) ayithe credit malli vasthundi.</li>
          <li>Daily limits + duplicate check unnai (oka profile ki repeat requests block).</li>
        </ul>
      </Section>

      <Section title="5. Prohibited conduct (veeti valla ban avutaru) 🚫">
        <ul>
          <li><b>Advance / registration / visa / hospital money adagadam</b> — idi fraud. Report ayithe ban + police complaint.</li>
          <li>Harassment, caste/religion abuses, stalking, repeated unwanted requests.</li>
          <li>Business promotions, ads, other websites links channel/WhatsApp lo pettadam.</li>
          <li>Other profiles data (photos/numbers) ni bayata share cheyyadam.</li>
          <li>Automated scraping, bots, bulk fake registrations.</li>
        </ul>
      </Section>

      <Section title="6. Fees & payments">
        <ul>
          <li>Plans, add-ons, renewal prices — <Link href="/pricing" className="underline font-bold">/pricing</Link> page lo clear ga unnai.</li>
          <li>Free tier: modati 3 requests FREE (card details avasaram ledu).</li>
          <li><b>Auto-renewal ledu</b>. Payment Razorpay/UPI secure gateway tho.</li>
          <li>Refund rules → <Link href="/refund" className="underline font-bold">/refund</Link> policy lo.</li>
          <li>Prices eppudaina marchochu — kaani meeru pay chesina plan features ivvakunda undamu.</li>
        </ul>
      </Section>

      <Section title="7. Mana limits (liability)">
        <ul>
          <li>Profiles ni verify cheyyadaniki manam best efforts pedtham (OTP, ID, photo) — kaani <b>100% guarantee ivvalemu</b>.
            Meere kooda verify cheyyali (meeting, documents, family background).</li>
          <li>Vyakti vera vyakti madhya jarige matter, meetings, money dealings ki manam <b>party kaadu, responsible kaadu</b>.</li>
          <li>Manam ivvE service maximum liability = <b>mee last 3 months lo pay chesina amount</b> వరకే.</li>
          <li>Fraud jarigina ventane <Link href="/safety" className="underline font-bold">/safety</Link> lo report cheyyandi — manam 24h lo action teesukuntam (hide/ban + help).</li>
        </ul>
      </Section>

      <Section title="8. Account suspend / terminate">
        <ul>
          <li>Terms violate, fake details, fraud reports, repeated complaints → warning → <b>hide</b> → <b>ban</b>.</li>
          <li>Banned accounts' remaining credits refund avvavu (fraud cases lo).</li>
          <li>Meeru account delete cheyyali ante — /privacy lo process (data delete, credits forfeit).</li>
        </ul>
      </Section>

      <Section title="9. Governing law & changes">
        <ul>
          <li>Ee terms <b>Indian law</b> batti, disputes ki <b>Hyderabad, Telangana</b> courts jurisdiction.</li>
          <li>Terms update ayithe ee page lo date marchutamu — kotha features ki chinna additions jarguthayi.</li>
          <li>Dispute unte — mundu <b>{SITE_CONFIG.supportEmail}</b> ki email cheyyandi (30 రోజుల్లో resolve cheyyadaniki try chestam).</li>
        </ul>
      </Section>

      <div className="mt-8 rounded-2xl border border-gray-200 bg-white p-5 text-xs text-gray-700">
        <div className="font-bold text-[#7A0C2E]">Contact</div>
        <div className="mt-2 space-y-1">
          <div>Email: <b>{SITE_CONFIG.supportEmail}</b> • WhatsApp: <b>{SITE_CONFIG.supportPhone}</b></div>
          <div>{SITE_CONFIG.legalName}, Hyderabad, Telangana, India</div>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-3 text-xs">
        <Link href="/pricing" className="underline text-[#7A0C2E] font-bold">💰 Pricing</Link>
        <Link href="/refund" className="underline text-[#7A0C2E] font-bold">💸 Refund Policy</Link>
        <Link href="/privacy" className="underline text-[#7A0C2E] font-bold">🔒 Privacy</Link>
        <Link href="/safety" className="underline text-[#7A0C2E] font-bold">🛡️ Safety</Link>
      </div>
    </main>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-6">
      <h2 className="font-bold text-[#7A0C2E] telugu">{title}</h2>
      <div className="mt-2 text-sm text-gray-700 telugu leading-relaxed [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:space-y-1.5">
        {children}
      </div>
    </section>
  );
}
