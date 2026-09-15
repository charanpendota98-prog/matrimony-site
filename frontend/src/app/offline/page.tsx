import Link from "next/link";

export const metadata = {
  title: "Offline — internet ledu | Mana Vivaha",
  description: "Internet connection ledu. Malli try cheyyandi — Mana Vivaha Telugu matrimony.",
};

export default function OfflinePage() {
  return (
    <main className="min-h-screen bg-cream flex items-center justify-center px-4">
      <div className="bg-white rounded-[2rem] border border-gold/30 p-7 max-w-md w-full text-center card-shadow">
        <div className="text-5xl">📡</div>
        <h1 className="mt-3 text-xl font-bold text-maroon">Internet ledu anukunta…</h1>
        <p className="mt-2 text-[13px] text-gray-700 telugu">
          Signal ragane malli try cheyyandi. Meera already chusina pages offline lo kooda open avutayi
          (matches, porutham report, safety tips).
        </p>
        <div className="mt-4 flex flex-col gap-2">
          <Link href="/" className="py-3 rounded-2xl maroon-gradient text-white font-bold text-[13px]">🏠 Home ki vellu</Link>
          <Link href="/matches" className="py-3 rounded-2xl border border-maroon/25 text-maroon font-bold text-[13px]">🔎 Matches chudu</Link>
          <Link href="/porutham" className="py-3 rounded-2xl border border-maroon/25 text-maroon font-bold text-[13px]">💍 Porutham report</Link>
        </div>
        <div className="mt-4 text-[11px] text-gray-500">
          Offline lo kooda mee WhatsApp number + card ready untayi — mana support ki message pettandi.
        </div>
      </div>
    </main>
  );
}
