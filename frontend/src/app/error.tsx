"use client";
/** ⚠️ Error boundary — crash aithe friendly Telugu message + retry (white screen ledu) */
import { useEffect } from "react";

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    console.error("[MANA-VIVAHA] page error:", error?.message, error?.digest || "");
  }, [error]);
  return (
    <main className="mx-auto max-w-xl px-4 py-16 text-center">
      <p className="text-5xl">🛠️</p>
      <h1 className="mt-3 text-2xl font-extrabold text-[#7A0C2E]">Konchem problem vachindi</h1>
      <p className="mt-2 text-slate-600">
        Page load lo error. Mee data safe — malli try cheyyandi. Repeat aithe mana support WhatsApp ki cheppandi.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-2">
        <button onClick={reset} className="rounded-xl bg-[#7A0C2E] px-4 py-2 font-semibold text-white">🔄 Malli try</button>
        <a href="/" className="rounded-xl border border-[#7A0C2E] px-4 py-2 font-semibold text-[#7A0C2E]">🏠 Home</a>
      </div>
      {error?.digest && <p className="mt-4 text-xs text-slate-400">ref: {error.digest}</p>}
    </main>
  );
}
