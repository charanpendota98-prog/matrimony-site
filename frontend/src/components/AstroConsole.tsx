"use client";
/**
 * 🪐 WAVE 13 — ADMIN ASTRO CONSOLE
 * 36-guna checker (2 IDs) + dosha queue (jathakam verify) + stats.
 */
import { useEffect, useState } from "react";
import { authHeaders } from "@/lib/api";
import { useLang } from "@/lib/lang";

type Row = Record<string, any>;
const adminToken = () => {
  try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; }
};
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};

export default function AstroConsole() {
  const { lang } = useLang();
  const te = lang === "te";
  const [bride, setBride] = useState("");
  const [groom, setGroom] = useState("");
  const [guna, setGuna] = useState<Row | null>(null);
  const [flash, setFlash] = useState("");
  const [queue, setQueue] = useState<Row[]>([]);
  const [qStatus, setQStatus] = useState("");
  const [stats, setStats] = useState<Row | null>(null);
  const [note, setNote] = useState<Record<string, string>>({});

  const loadStats = async () => {
    try {
      const d = await fetch(withToken("/api/admin/astro/stats"), { headers: authHeaders(true) }).then((r) => r.json());
      if (d.success) setStats(d);
    } catch { /* ignore */ }
  };
  const loadQueue = async (st: string) => {
    try {
      const d = await fetch(withToken(`/api/admin/astro/queue${st ? `?status=${st}` : ""}`), { headers: authHeaders(true) }).then((r) => r.json());
      if (d.success) setQueue(d.items || []);
    } catch { /* ignore */ }
  };
  useEffect(() => { void loadStats(); void loadQueue(""); }, []);

  const checkGuna = async () => {
    if (!bride.trim() || !groom.trim()) { setFlash(te ? "⚠️ Bride + Groom IDs ఇవ్వండి" : "⚠️ Enter Bride + Groom IDs"); return; }
    setFlash(te ? "⏳ Guna చూస్తున్నాం…" : "⏳ Checking guna…");
    const r = await fetch(`/api/astro/guna?bride_id=${encodeURIComponent(bride.trim().toUpperCase())}&groom_id=${encodeURIComponent(groom.trim().toUpperCase())}`);
    const d = await r.json();
    if (!r.ok) { setFlash(d.detail || "Fail"); setGuna(null); return; }
    setGuna(d);
    setFlash(d.available ? `✅ ${d.total_36}/36 — ${d.verdict_telugu}` : (d.verdict_telugu || "Data ledu"));
  };

  const verify = async (id: string, ok: boolean) => {
    const r = await fetch(withToken(`/api/admin/astro/verify/${id}`),
      { method: "POST", headers: { ...authHeaders(true), "Content-Type": "application/json" },
        body: JSON.stringify({ ok, note: note[id] || "" }) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void loadQueue(qStatus); void loadStats();
  };

  return (
    <div>
      <p className="telugu mt-2 text-xs text-gray-500">
        {te ? "36-guna Ashtakoota (classical) + dosha screening + jathakam pandit-verify. Star/rasi లేకపోతే honest గా చెప్తుంది (guess వద్దు)." : "36-guna Ashtakoota (classical) + dosha screening + pandit-verified jathakam. Says so honestly when star/rasi is missing (no guessing)."}
      </p>
      {stats ? (
        <div className="mt-3 grid grid-cols-2 gap-3 text-center md:grid-cols-5">
          {[
            { l: "Profiles", v: stats.total }, { l: "🚫 Dosha declared", v: stats.dosha_declared },
            { l: "⚠️ Moola", v: stats.moola }, { l: "🪐 Jathakam verified", v: stats.jathakam_verified },
            { l: "⏳ Pandit queue", v: stats.jathakam_pending },
          ].map((x) => (
            <div key={x.l} className="rounded-2xl bg-gray-50 p-3">
              <div className="text-xl font-bold text-[#7A0C2E]">{x.v}</div>
              <div className="text-[11px] text-gray-500">{x.l}</div>
            </div>
          ))}
        </div>
      ) : null}

      {/* guna checker */}
      <div className="mt-3 rounded-2xl border p-4">
        <div className="font-bold text-[#7A0C2E]">🪐 36-Guna checker</div>
        <div className="mt-2 flex flex-wrap gap-2">
          <input value={bride} onChange={(e) => setBride(e.target.value.toUpperCase())} placeholder="Bride TSAP ID"
            aria-label="Bride ID" className="min-w-[200px] flex-1 rounded-xl border px-3 py-2 font-mono text-sm" />
          <input value={groom} onChange={(e) => setGroom(e.target.value.toUpperCase())} placeholder="Groom TSAP ID"
            aria-label="Groom ID" className="min-w-[200px] flex-1 rounded-xl border px-3 py-2 font-mono text-sm" />
          <button onClick={() => void checkGuna()} className="rounded-xl bg-[#7A0C2E] px-5 py-2 text-sm font-bold text-white">🔍 Guna chudu</button>
        </div>
        {flash ? <div className="mt-2 rounded-xl bg-[#0F1F3C] p-2 text-xs text-white">{flash}</div> : null}
        {guna?.available ? (
          <div className="mt-3">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-[#7A0C2E] px-4 py-2 text-center text-white">
                <div className="text-2xl font-extrabold">{guna.total_36}<span className="text-sm">/36</span></div>
                <div className="text-[10px]">{guna.percent}% · {guna.verdict}</div>
              </div>
              <div className="text-xs text-gray-600">
                👰 {guna.bride?.star} / {guna.bride?.rasi} × 🤵 {guna.groom?.star} / {guna.groom?.rasi}
                <div className="mt-1 font-bold text-[#7A0C2E]">{guna.verdict_telugu}</div>
              </div>
            </div>
            <div className="mt-2 grid gap-2 md:grid-cols-2">
              {(guna.kootas || []).map((k: Row) => (
                <div key={k.koota} className="rounded-xl bg-gray-50 p-2 text-xs">
                  <div className="flex justify-between font-bold"><span>{k.koota}</span><span className="text-[#7A0C2E]">{k.score}/{k.max}</span></div>
                  <div className="text-gray-500">{k.detail}</div>
                  <div>{k.telugu}</div>
                </div>
              ))}
            </div>
            {(guna.doshas || []).length ? (
              <div className="mt-2 rounded-xl bg-red-50 p-2 text-xs text-red-800">
                <b>🚫 Doshalu ({guna.doshas.length}):</b>
                <ul className="mt-1 list-disc pl-5">{guna.doshas.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul>
              </div>
            ) : null}
            <p className="mt-1 text-[11px] text-gray-500">{guna.note_telugu}</p>
          </div>
        ) : null}
      </div>

      {/* pandit queue */}
      <div className="mt-3 rounded-2xl border p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="font-bold text-[#7A0C2E]">📜 Pandit verify queue (jathakams)</div>
          <select value={qStatus} onChange={(e) => { setQStatus(e.target.value); void loadQueue(e.target.value); }}
            aria-label="Status" className="rounded-full border px-3 py-1.5 text-xs">
            <option value="">anni</option><option value="pending">pending</option>
            <option value="verified">verified</option><option value="rejected">rejected</option>
          </select>
        </div>
        <div className="mt-2 overflow-x-auto">
          <table className="w-full text-xs">
            <thead><tr className="border-b text-left text-gray-500">
              <th className="p-2">ID</th><th>Profile</th><th>File</th><th>Status</th><th>Note / Action</th>
            </tr></thead>
            <tbody>
              {queue.length === 0 ? <tr><td colSpan={5} className="p-4 text-center text-gray-500">Queue khaali 🙂</td></tr> : null}
              {queue.map((j) => (
                <tr key={j.id} className="border-b">
                  <td className="p-2 font-mono font-bold">{j.id}<div className="text-[10px] text-gray-400">{String(j.at || "").slice(0, 16)}</div></td>
                  <td className="p-2 font-mono">{j.tsap_id}</td>
                  <td className="p-2">{j.kind === "pdf" ? "📄" : "🖼️"} <span className="font-mono text-[10px]">{j.file}</span></td>
                  <td className="p-2"><span className={`rounded-full px-2 py-0.5 text-[10px] ${j.status === "verified" ? "bg-green-100 text-green-700" : j.status === "rejected" ? "bg-red-100 text-red-700" : "bg-orange-100 text-orange-700"}`}>{j.status}</span></td>
                  <td className="p-2">
                    {j.status === "pending" ? (
                      <div className="flex gap-1">
                        <input value={note[j.id] || ""} onChange={(e) => setNote({ ...note, [j.id]: e.target.value })}
                          placeholder="pandit note" aria-label="Note" className="w-28 rounded-lg border px-2 py-1" />
                        <button onClick={() => void verify(j.id, true)} className="rounded-full bg-green-600 px-3 py-1 text-white">✅</button>
                        <button onClick={() => void verify(j.id, false)} className="rounded-full bg-red-500 px-3 py-1 text-white">❌</button>
                      </div>
                    ) : <span className="text-gray-500">{j.note || "—"}</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
