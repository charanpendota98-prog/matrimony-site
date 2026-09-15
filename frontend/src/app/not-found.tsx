import Link from "next/link";

export default function NotFound() {
  return (
    <main className="mx-auto max-w-xl px-4 py-16 text-center">
      <p className="text-5xl">🔍</p>
      <h1 className="mt-3 text-2xl font-extrabold text-[#7A0C2E]">Ee page dorakaledu (404)</h1>
      <p className="mt-2 text-slate-600">
        Link tappu undochu (leda profile teesesaru). Kinda options try cheyyandi — mana site lo 76+ profiles unnayi.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-2">
        <Link href="/" className="rounded-xl bg-[#7A0C2E] px-4 py-2 font-semibold text-white">🏠 Home</Link>
        <Link href="/matches" className="rounded-xl border border-[#7A0C2E] px-4 py-2 font-semibold text-[#7A0C2E]">💞 Matches</Link>
        <Link href="/register" className="rounded-xl border border-[#7A0C2E] px-4 py-2 font-semibold text-[#7A0C2E]">🆓 Register FREE</Link>
        <Link href="/channels" className="rounded-xl border border-slate-300 px-4 py-2 font-semibold text-slate-700">📢 Channels</Link>
      </div>
    </main>
  );
}
