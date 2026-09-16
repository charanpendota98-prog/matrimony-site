"use client";

/**
 * 💬 WAVE 11 — Support widget (prathi page lo floating help).
 * /api/support/faq?q= tho Telugu Q&A search — login avasaram ledu.
 */
import { useEffect, useRef, useState } from "react";
import { apiGet } from "@/lib/api";

type Faq = { id: string; q: string; a: string };

export default function SupportWidget() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [faqs, setFaqs] = useState<Faq[]>([]);
  const [loading, setLoading] = useState(false);
  const [human, setHuman] = useState("");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  async function load(query: string) {
    setLoading(true);
    const r = await apiGet<{ faqs?: Faq[]; human_telugu?: string }>(
      `/api/support/faq?q=${encodeURIComponent(query)}&limit=6`
    );
    setLoading(false);
    if (r.ok && r.data) {
      setFaqs(r.data.faqs || []);
      setHuman(r.data.human_telugu || "");
    }
  }

  useEffect(() => {
    if (!open) return;
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => load(q), q ? 350 : 0);
    return () => { if (timer.current) clearTimeout(timer.current); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, q]);

  return (
    <div className="fixed bottom-20 right-4 z-50 flex flex-col items-end gap-2 sm:bottom-6">
      {open && (
        <div className="w-[20rem] max-w-[calc(100vw-2rem)] overflow-hidden rounded-2xl border border-rose-200 bg-white shadow-2xl">
          <div className="bg-gradient-to-r from-rose-700 to-rose-600 px-4 py-3 text-white">
            <p className="font-bold">💬 Sahayam (Help)</p>
            <p className="text-xs opacity-90">Telugu lo adagandi — ventane samadhanam</p>
          </div>
          <div className="p-3">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Ex: ₹99 enduku? numbers eppudu?"
              aria-label="Sahayam search"
              className="w-full rounded-xl border border-gray-300 px-3 py-2 text-sm outline-none focus:border-rose-500"
            />
            <div className="mt-2 max-h-72 space-y-2 overflow-y-auto pr-1">
              {loading && <p className="text-sm text-gray-500">⏳ Vetukuthunna…</p>}
              {!loading && faqs.map((f) => (
                <details key={f.id} className="rounded-xl bg-rose-50/60 p-2.5 text-sm">
                  <summary className="cursor-pointer font-semibold text-rose-900">{f.q}</summary>
                  <p className="mt-1 text-gray-700">{f.a}</p>
                </details>
              ))}
              {!loading && faqs.length === 0 && (
                <p className="text-sm text-gray-500">Samadhanam dorakaledu — /help try cheyyandi 🙏</p>
              )}
            </div>
            {human && <p className="mt-2 border-t pt-2 text-xs text-gray-500">{human}</p>}
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(!open)}
        aria-label={open ? "Sahayam close" : "Sahayam open"}
        className="flex h-12 w-12 items-center justify-center rounded-full bg-rose-700 text-2xl text-white shadow-xl transition hover:bg-rose-800"
      >
        {open ? "✕" : "💬"}
      </button>
    </div>
  );
}
