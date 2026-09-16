"use client";

/**
 * 💑 WAVE 11 — Success Stories (trust + viral).
 * Public list + logged-in users story submit + like.
 */
import { useEffect, useState } from "react";
import { Duo, duo } from "@/lib/duo";
import Link from "next/link";
import { apiGet, apiPost, TSAP_KEY } from "@/lib/api";
import FeaturedStories from "@/components/FeaturedStories";

type Story = {
  story_id: string;
  couple_names: string;
  text: string;
  district: string;
  photo_url: string;
  likes: number;
  created_at: string;
};

function myId(): string {
  if (typeof window === "undefined") return "";
  try { return localStorage.getItem(TSAP_KEY) || ""; } catch { return ""; }
}

export default function StoriesClient() {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ text: "", couple_names: "", partner_id: "", district: "" });
  const [msg, setMsg] = useState("");
  const [sending, setSending] = useState(false);
  const [liked, setLiked] = useState<Set<string>>(new Set());

  async function load() {
    setLoading(true);
    const r = await apiGet<{ stories?: Story[] }>("/api/stories?limit=20");
    setLoading(false);
    if (r.ok && r.data) setStories(r.data.stories || []);
  }
  useEffect(() => { load(); }, []);

  async function submit() {
    const tid = myId();
    if (!tid) { setMsg("🔒 Mundu login/register cheyyandi — appudu story pampochu"); return; }
    if (form.text.trim().length < 20) { setMsg("⚠️ Story konchem peddaga rayandi (20+ letters)"); return; }
    setSending(true);
    const r = await apiPost<{ message_telugu?: string }>("/api/stories/submit", { tsap_id: tid, ...form });
    setSending(false);
    setMsg(r.ok ? (r.data?.message_telugu || "✅ Story vachindi!") : (r.errorTelugu || "⚠️ Malli try"));
    if (r.ok) setForm({ text: "", couple_names: "", partner_id: "", district: "" });
  }

  async function like(id: string) {
    if (liked.has(id)) return;
    const r = await apiPost<{ likes?: number }>(`/api/stories/${id}/like`, {});
    if (r.ok) {
      setLiked(new Set(liked).add(id));
      setStories((s) => s.map((x) => (x.story_id === id ? { ...x, likes: r.data?.likes ?? x.likes + 1 } : x)));
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-3xl font-extrabold text-rose-900">💑 <Duo en="Success Stories" te="విజయగాథలు" /></h1>
      <div className="mt-4"><FeaturedStories limit={6} /></div>
      <h2 className="mt-8 text-xl font-extrabold text-rose-900">💬 <Duo en="Community stories" te="మీ కథలు" /></h2>
      <p className="mt-1 text-gray-600">
        Mana Vivaha dwara kalisina jantalu 🎉 — meeku kooda ilanti sambandham kavali ante{" "}
        <Link href="/register" className="font-semibold text-rose-700 underline">3 min lo register</Link> (modati 3 FREE).
      </p>

      {loading && <p className="mt-6 text-gray-500">⏳ Stories loading…</p>}
      {!loading && stories.length === 0 && (
        <div className="mt-6 rounded-2xl border border-dashed border-rose-300 bg-rose-50 p-6 text-center">
          <p className="text-lg font-semibold text-rose-900">🆕 Modati story meeru avvandi!</p>
          <p className="mt-1 text-sm text-gray-600">Pelli ayina jantalu kinda form lo story pampandi — approve ayyaka ikkada + channels lo kanipistundi.</p>
        </div>
      )}
      <div className="mt-6 space-y-4">
        {stories.map((s) => (
          <article key={s.story_id} className="rounded-2xl border border-rose-100 bg-white p-5 shadow-sm">
            <p className="font-bold text-rose-900">💑 {s.couple_names || "Mana Vivaha janta"}{s.district ? ` · ${s.district}` : ""}</p>
            <p className="mt-2 whitespace-pre-wrap text-gray-700">“{s.text}”</p>
            <div className="mt-3 flex items-center justify-between">
              <button
                onClick={() => like(s.story_id)}
                disabled={liked.has(s.story_id)}
                aria-label={`${s.likes} likes, like cheyyandi`}
                className="rounded-full bg-rose-50 px-3 py-1 text-sm font-semibold text-rose-700 hover:bg-rose-100 disabled:opacity-60"
              >
                ❤️ {s.likes} {liked.has(s.story_id) ? "· Thanks!" : ""}
              </button>
              <span className="text-xs text-gray-400">{(s.created_at || "").slice(0, 10)}</span>
            </div>
          </article>
        ))}
      </div>

      <div className="mt-10 rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5">
        <h2 className="text-xl font-bold text-emerald-900">📝 Mee story pampandi</h2>
        <p className="text-sm text-gray-600">Pelli ayinda? Janta peru + 2 lines + photo link (optional) — admin approve (24h) tarvata public.</p>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          <input value={form.couple_names} onChange={(e) => setForm({ ...form, couple_names: e.target.value })}
            placeholder="Janta peru (Ex: Raju ❤️ Lakshmi)" aria-label="Janta peru"
            className="rounded-xl border px-3 py-2 text-sm outline-none focus:border-emerald-500" />
          <input value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })}
            placeholder="District (Ex: Nalgonda)" aria-label="District"
            className="rounded-xl border px-3 py-2 text-sm outline-none focus:border-emerald-500" />
        </div>
        <textarea value={form.text} onChange={(e) => setForm({ ...form, text: e.target.value })}
          placeholder="Mee story (20+ letters) — ela kalisaru, eppudu pelli…" aria-label="Mee story"
          rows={3} className="mt-2 w-full rounded-xl border px-3 py-2 text-sm outline-none focus:border-emerald-500" />
        <input value={form.partner_id} onChange={(e) => setForm({ ...form, partner_id: e.target.value })}
          placeholder="Partner TSAP ID (optional)" aria-label="Partner TSAP ID"
          className="mt-2 w-full rounded-xl border px-3 py-2 text-sm outline-none focus:border-emerald-500" />
        <button onClick={submit} disabled={sending}
          className="mt-3 rounded-xl bg-emerald-700 px-5 py-2 font-bold text-white hover:bg-emerald-800 disabled:opacity-60">
          {sending ? "⏳ Pampistunna…" : "💑 Story pampu"}
        </button>
        {msg && <p className="mt-2 text-sm font-semibold text-gray-700">{msg}</p>}
      </div>
    </div>
  );
}
