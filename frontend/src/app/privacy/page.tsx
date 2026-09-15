import Link from "next/link";
import { SITE_CONFIG } from "@/lib/site-config";

/** 🔒 PRIVACY POLICY — DPDP Act 2023 (India) + matrimony privacy expectations. */
export const metadata = {
  title: "Privacy Policy | Mana Vivaha (TSAP Matrimony)",
  description: "Mana Vivaha privacy policy — emi data collect chestam, enduku, evaritho share chestam, photo privacy, delete requests, grievance officer.",
};

const LAST_UPDATED = "14 Sep 2026";

export default function PrivacyPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl md:text-3xl font-extrabold text-[#7A0C2E] telugu">🔒 Privacy Policy</h1>
      <div className="text-xs text-gray-500 mt-1">Last updated: {LAST_UPDATED} • {SITE_CONFIG.legalName} ({SITE_CONFIG.domain})</div>

      <div className="mt-5 rounded-2xl bg-[#FFF8E1] border border-[#B8860B]/30 p-4 text-sm telugu text-[#7A0C2E]">
        <b>Short ga:</b> Mee data ni <b>ammamu, rent ki ivvamu</b>. Photos private mode tho chupistham.
        Numbers <b>rendu vaipula oppuka tarvate</b> share avutayi. Eppudaina mee data delete adagochu —
        30 రోజుల్లో theestham.
      </div>

      <Section title="1. Eemi data collect chestam">
        <ul>
          <li><b>Profile:</b> peru, gender, DOB/age, height, marital status, caste, religion, district/state, education, job, salary range, gothram, nakshatram/rasi (mee istam tho), about, photo(s).</li>
          <li><b>Contact:</b> mobile number (OTP verify), optional WhatsApp number, guardian contact (optional).</li>
          <li><b>Activity:</b> profile views, requests, saves, channel posts, login times, device/browser (basic), IP (security kosam).</li>
          <li><b>Payments:</b> payment ID, amount, plan — <b>card/UPI details mana daggara store avvavu</b> (Razorpay handle chestundi).</li>
          <li><b>Support:</b> meeru pampina messages/screenshots (complaints resolve cheyyadaniki).</li>
        </ul>
      </Section>

      <Section title="2. Enduku vaadutam (purpose)">
        <ul>
          <li>Mee profile ni channels/WhatsApp lo post cheyyadam + matching profiles chupinchadam.</li>
          <li>Requests deliver cheyyadam (mee profile target ki, vaalla profile meeku).</li>
          <li>Fraud detection, moderation, block/report handling, safety alerts.</li>
          <li>Payments, receipts, GST invoices, referral payouts.</li>
          <li>Service updates (plan expiry reminder, kotha matches) — marketing messages ki <b>opt-out</b> option undi.</li>
        </ul>
      </Section>

      <Section title="3. Evaritho share chestam">
        <ul>
          <li><b>Other members:</b> meeru request accept chesina tarvata matrame — number/WhatsApp share.</li>
          <li><b>Channels (public):</b> profile card lo peru, age, caste, job, district kanipisthundi — <b>phone number eppudu public ga pettamu</b>. Photo mee privacy setting batti (private mode ayithe channels lo kooda chupinchamu leda blur chesi pettam).</li>
          <li><b>Payment gateway:</b> Razorpay (amount + order details matrame).</li>
          <li><b>WhatsApp:</b> mana official number nunchi mee profile/card share cheyyadaniki — message delivery ki anthe.</li>
          <li><b>Legal:</b> court/police order unte matrame — required minimum data.</li>
          <li>❌ Manam mee data ni <b>third-party advertisers ki ammamu leda rent ki ivvamu</b>.</li>
        </ul>
      </Section>

      <Section title="4. Photo & number privacy (matrimony special)">
        <ul>
          <li><b>Photo private mode:</b> channel/WhatsApp posts lo photo chupincham (mee request batti) — profile lo matrame kanipisthundi.</li>
          <li><b>Watermark:</b> photos meeda mana watermark untaadi — misuse aapitundi.</li>
          <li><b>Numbers:</b> rendu vaipula oppuka tarvata matrame — mana team WhatsApp lo confirm chesi isthundi. Declined profiles numbers eppudu ivvamu.</li>
          <li>Screenshot/share cheyyadam bayata vaallaki — <b>term violation</b> (report chesina vaalla account ban avutundi).</li>
        </ul>
      </Section>

      <Section title="5. Cookies & analytics">
        <ul>
          <li>Login session, language preference, saved filters ki <b>cookies</b> vaadutam.</li>
          <li><b>Booking/Interesting? Vaddu</b> — mee data ni ad-tech companies ki ivvamu.</li>
          <li>Basic analytics (enni pages chusaru) — service improve cheyyadaniki matrame, personal ga trace cheyyamu.</li>
          <li>Browser lo cookies disable cheyyachu (kaani login/saved features pani cheyyavu).</li>
        </ul>
      </Section>

      <Section title="6. Data security">
        <ul>
          <li>OTP verification, encrypted transport (HTTPS), access limited to authorized team members.</li>
          <li>Support team members ki kooda <b>need-to-know</b> access matrame — logs audit chestam.</li>
          <li>Data breach jarigithe — 72 గంటల్లో affected users ki notify chestam (DPDP Act requirement).</li>
        </ul>
      </Section>

      <Section title="7. Entha time store chestam (retention)">
        <ul>
          <li><b>Active profile:</b> meeru account unna varaku.</li>
          <li><b>Inactive (12 నెలలు login ledu):</b> reminder pampistham → 30 రోజుల tarvata profile hide.</li>
          <li><b>Payment records:</b> 8 సంవత్సరాలు (tax/legal requirement).</li>
          <li><b>Complaints/fraud evidence:</b> 3 సంవత్సరాలు (repeat fraud aapadaniki).</li>
        </ul>
      </Section>

      <Section title="8. Mee rights (మీ హక్కులు)">
        <ul>
          <li><b>Chudatam / correct cheyyadam:</b> mee profile eppudaina edit cheyyachu (support tho leda admin tho).</li>
          <li><b>Delete:</b> account + data delete adagochu — <b>30 రోజుల్లో</b> profile + photos + personal data theestham (payment records legal ga untayi).</li>
          <li><b>Consent withdraw:</b> channels/WhatsApp sharing aapinchachu (kaani appudu service reach thakkuva avutundi).</li>
          <li><b>Marketing opt-out:</b> "STOP" ane message pampandi leda support ki cheppandi.</li>
        </ul>
      </Section>

      <Section title="9. Children & 3rd party links">
        <ul>
          <li>Ee service <b>18+</b> ki matrame (bride 18+, groom 21+).</li>
          <li>Third-party links (payment gateway, vendor offers) ki vaallaki sva-privacy policies untayi — manam responsible kaadu.</li>
        </ul>
      </Section>

      <div className="mt-8 rounded-2xl border border-gray-200 bg-white p-5 text-xs text-gray-700">
        <div className="font-bold text-[#7A0C2E]">🧑‍⚖️ Grievance Officer (DPDP Act 2023)</div>
        <div className="mt-2 space-y-1">
          <div>Name: Grievance Officer, {SITE_CONFIG.legalName}</div>
          <div>Email: <b>{SITE_CONFIG.supportEmail}</b> • WhatsApp/Phone: <b>{SITE_CONFIG.supportPhoneDisplay}</b></div>
          <div>Address: Hyderabad, Telangana, India</div>
          <div>Response: 15 రోజుల్లో (complaint acknowledge 48h lopu)</div>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-3 text-xs">
        <Link href="/pricing" className="underline text-[#7A0C2E] font-bold">💰 Pricing</Link>
        <Link href="/terms" className="underline text-[#7A0C2E] font-bold">📄 Terms</Link>
        <Link href="/refund" className="underline text-[#7A0C2E] font-bold">💸 Refund</Link>
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
