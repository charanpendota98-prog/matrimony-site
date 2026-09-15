/** ⏳ Global loading skeleton — white screen kaadu */
export default function Loading() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <div className="animate-pulse space-y-4">
        <div className="h-8 w-2/3 rounded-lg bg-rose-100" />
        <div className="h-4 w-1/3 rounded bg-rose-50" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-40 rounded-2xl bg-rose-50" />
          ))}
        </div>
      </div>
      <p className="mt-6 text-center text-sm text-slate-500">⏳ Load avutundi… mana profiles rich data tho vastunnayi</p>
    </main>
  );
}
