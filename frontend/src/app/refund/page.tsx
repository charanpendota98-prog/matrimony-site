import Link from "next/link";
import { SITE_CONFIG } from "@/lib/site-config";

/**
 * 💸 REFUND & CANCELLATION POLICY — Razorpay/UPI compliance ki kooda kavali.
 * Clear ga: emi refund avutundi, emi avvadu, ela apply cheyyali, entha time.
 */
export const metadata = {
  title: "Refund & Cancellation Policy | Mana Vivaha (TSAP Matrimony)",
  description: "Mana Vivaha refund policy — decline aithe credit refund, 7-day money-back, cancellation, GST invoice, contact details.",
};

const LAST_UPDATED = "14 Sep 2026";

export default function RefundPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl md:text-3xl font-extrabold text-[#7A0C2E] telugu">💸 Refund & Cancellation Policy</h1>
      <div className="text-xs text-gray-500 mt-1">Last updated: {LAST_UPDATED} • {SITE_CONFIG.legalName} ({SITE_CONFIG.domain})</div>

      <div className="mt-5 rounded-2xl bg-[#FFF8E1] border border-[#B8860B]/30 p-4 text-sm telugu text-[#7A0C2E]">
        <b>Short ga (Telugu):</b> Meere pay chesina amount ki **profile credits** vasthayi. Ee credits
        vaadaledu ante — 7 రోజుల్లో full refund adagochu. Vaadina tarvata migilina credits ki refund ivvamu
        (kaani decline aithe aa request credit malli vasthundi). Auto-renewal ledu, hidden charges ledu.
      </div>

      <Section title="1. Eemi refund avutundi ✅">
        <ul>
          <li><b>Zero usage (7 days):</b> Register ayi ₹ pay chesi, <b>okka request kooda</b> pampakapote —
            payment date nunchi <b>7 రోజుల</b> lopu adigithe <b>100% refund</b> (same payment method ki).</li>
          <li><b>Decline / no response:</b> Mee request target vaallu decline cheste leda {""}
            <b>7 రోజుల</b> lo respond avvakapote — aa <b>1 credit malli mee account ki</b> refund avutundi
            (idi automatic ga jarugutundi).</li>
          <li><b>Duplicate / wrong payment:</b> Okate order rendu sari pay aithe, verify chesi 3–5 working days lo refund.</li>
          <li><b>Technical failure:</b> Mee payment success ayindi kaani credits add avvakapote — screenshot pampandi, 24h lo fix leda refund.</li>
        </ul>
      </Section>

      <Section title="2. Eemi refund avvadu ❌">
        <ul>
          <li>Credits <b>vaadina tarvata</b> (request pampina tarvata) — service deliver ayyindi kabatti.</li>
          <li>Numbers share ayyina tarvata leda match finalize ayyaka.</li>
          <li>Fake / wrong details icchi account block ayina cases.</li>
          <li>Terms violate chesi ban ayina accounts (fraud, advance money adagadam, harassment).</li>
          <li><b>Bureau / B2B plans</b> — monthly service kabatti cycle start ayina tarvata refund ledu (cycle start avvakapote 7 రోజుల lopu adjust/refund).</li>
          <li>Add-on services (boost / who-viewed / porutham report) — activate ayinaka refund ledu.</li>
        </ul>
      </Section>

      <Section title="3. Refund ela adagali (process)">
        <ol>
          <li>WhatsApp: <b>{SITE_CONFIG.supportPhone}</b> leda email: <b>{SITE_CONFIG.supportEmail}</b></li>
          <li>Pampalsinavi: TSAP ID • payment date • amount • Razorpay payment ID • reason (1 line)</li>
          <li>Verify chesi <b>2 working days</b> lo approve/decline cheppi cheptham.</li>
          <li>Approve ayithe <b>5–7 working days</b> lo mee bank/UPI ki credited avutundi (bank timing batti).</li>
          <li>Ledger lo refund entry + email confirmation pampistham.</li>
        </ol>
      </Section>

      <Section title="4. Cancellation">
        <ul>
          <li>Plan cancel cheyyali ante — support ki cheppandi. Migilina credits <b>validity varaku</b> vaadukovachu.</li>
          <li><b>Auto-renewal ledu</b> — mee plan automatic ga renew avvadu, reminder messages matrame vasthayi.</li>
          <li>Account delete cheyyali ante — /privacy lo cheppina privacy section lo process undi (data delete + credits forfeit).</li>
        </ul>
      </Section>

      <Section title="5. GST, invoices & receipts">
        <ul>
          <li>Prathi payment ki receipt email/WhatsApp lo vasthundi.</li>
          <li><b>GST invoice</b> kavali ante payment tarvata 24 గంటల్లో adagandi (GSTIN unte pampandi) — mana team pampistundi.</li>
          <li>Prices anni INR lo, taxes tho saha (jaha chupinchina price final).</li>
        </ul>
      </Section>

      <Section title="6. Chargebacks / disputes">
        <ul>
          <li>Mundu mana support ki cheppandi — 90% cases 48h lo resolve avutayi.</li>
          <li>Bank chargeback initiate chesthe, mana records (payment ID + service usage) pampistham.</li>
          <li>Fraudulent chargebacks ayithe account temporary suspend avvachu.</li>
        </ul>
      </Section>

      <div className="mt-8 rounded-2xl border border-gray-200 bg-white p-5 text-xs text-gray-700">
        <div className="font-bold text-[#7A0C2E]">📞 Contact (refunds & payments)</div>
        <div className="mt-2 space-y-1">
          <div>WhatsApp / Phone: <b>{SITE_CONFIG.supportPhone}</b></div>
          <div>Email: <b>{SITE_CONFIG.supportEmail}</b></div>
          <div>Website: <b>https://{SITE_CONFIG.domain}</b> • Bot: {SITE_CONFIG.botUsername}</div>
          <div>Business: {SITE_CONFIG.legalName}, Hyderabad, Telangana, India</div>
          <div>Working hours: Mon–Sat, 9 AM – 8 PM IST (response 24h lopu)</div>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-3 text-xs">
        <Link href="/pricing" className="underline text-[#7A0C2E] font-bold">💰 Pricing</Link>
        <Link href="/terms" className="underline text-[#7A0C2E] font-bold">📄 Terms</Link>
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
      <div className="mt-2 text-sm text-gray-700 telugu leading-relaxed [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:space-y-1.5 [&_ol]:list-decimal [&_ol]:pl-5 [&_ol]:space-y-1.5">
        {children}
      </div>
    </section>
  );
}
