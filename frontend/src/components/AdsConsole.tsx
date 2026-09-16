"use client";
/**
 * 📢 WAVE 13 — ADMIN ADS CONSOLE
 * Campaign queue (UTR approve → LIVE) + pause/reject + revenue stats.
 */
import { useEffect, useState } from "react";
import { authHeaders } from "@/lib/api";

type Row = Record<string, any>;
const adminToken = () => {
  try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; }
};
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};

export default function AdsConsole() {
  const [items, setItems] = useState<Row[]>([]);
  const [status, setStatus] = useState("pending");
  const [stats, setStats] = useState<Row | null>(null);
  const [utr, setUtr] = useState<Record<string, string>>({});
  const [flash, setFlash] = useState("");

  const load = async (st: string) => {
    try {
      const d = await fetch(withToken(`/api/admin/ads${st ? `?status=${st}` : ""}`), { headers: authHeaders(true) }).then((r) => r.json());
      if (d.success) setItems(d.campaigns || []);
      const s = await fetch(withToken("/api/admin/ads/stats"), { headers: authHeaders(true) }).then((r) => r.json());
      if (s.success) setStats(s);
    } catch { /* ignore */ }
  };
  useEffect(() => { void load(status); }, [status]);

  const approve = async (id: string) => {
    const u = (utr[id] || "").trim();
    if (!u) { setFlash("⚠️ UTR lekunda approve cheyyakoodadu"); return; }
    const r = await fetch(withToken(`/api/admin/ads/${id}/approve`),
      { method: "POST", headers: { ...authHeaders(true), "Content-Type": "application/json" },
        body: JSON.stringify({ utr: u }) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void load(status);
  };
  const act = async (id: string, action: string) => {
    const r = await fetch(withToken(`/api/admin/ads/${id}/action`),
      { method: "POST", headers: { ...authHeaders(true), "Content-Type": "application/json" },
        body: JSON.stringify({ action }) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void load(status);
  };

  return (
    <div>
      <p className="telugu mt-2 text-xs text-gray-500">
        Vendor (photo/decor/mall...) campaign → payment verify → <b>approve</b> chesthe district/state scope lo LIVE.
        Days ayipothe auto-expire · impressions/clicks auto-track.
      </p>
      {stats ? (
        <div className="mt-3 grid grid-cols-2 gap-3 text-center md:grid-cols-6">
          {[
            { l: "Campaigns", v: stats.total }, { l: "🟢 Live", v: stats.live },
            { l: "⏳ Pending", v: stats.pending }, { l: "💰 Collected ₹", v: stats.collected },
            { l: "👁️ Views", v: stats.impressions }, { l: "🖱️ Clicks", v: stats.clicks },
          ].map((x) => (
            <div key={x.l} className="rounded-2xl bg-gray-50 p-3">
              <div className="text-xl font-bold text-[#7A0C2E]">{x.v}</div>
              <div className="text-[11px] text-gray-500">{x.l}</div>
            </div>
          ))}
        </div>
      ) : null}
      {flash ? <div className="mt-2 rounded-xl bg-[#0F1F3C] p-2 text-xs text-white">{flash}</div> : null}
      <div className="mt-2 flex gap-2">
        <select value={status} onChange={(e) => setStatus(e.target.value)}
          aria-label="Status" className="rounded-full border px-3 py-1.5 text-xs">
          <option value="pending">pending</option><option value="active">active</option>
          <option value="paused">paused</option><option value="expired">expired</option>
          <option value="rejected">rejected</option><option value="">anni</option>
        </select>
      </div>
      <div className="mt-2 overflow-x-auto">
        <table className="w-full text-xs">
          <thead><tr className="border-b text-left text-gray-500">
            <th className="p-2">Campaign</th><th>Scope</th><th>Media/Slots</th><th>₹/Days</th><th>Stats</th><th>UTR / Action</th>
          </tr></thead>
          <tbody>
            {items.length === 0 ? <tr><td colSpan={6} className="p-4 text-center text-gray-500">Ee status lo campaigns levu 🙂</td></tr> : null}
            {items.map((c) => (
              <tr key={c.id} className="border-b align-top">
                <td className="p-2">
                  <div className="font-bold">{c.title}</div>
                  <div className="font-mono text-[10px] text-gray-500">{c.id} · vendor {c.vendor_id}</div>
                  {c.offer ? <div className="text-[11px] text-green-700">🎁 {c.offer}</div> : null}
                  <div className={`mt-1 inline-block rounded-full px-2 py-0.5 text-[10px] ${c.status === "active" ? "bg-green-100 text-green-700" : "bg-orange-100 text-orange-700"}`}>{c.status}{c.end ? ` → ${String(c.end).slice(0, 10)}` : ""}</div>
                </td>
                <td className="p-2">
                  <b>{c.level}</b>
                  <div className="text-[10px] text-gray-500">{c.level === "district" ? (c.districts || []).join(", ") : c.level === "state" ? c.state : "TS+AP"}</div>
                </td>
                <td className="p-2 text-[10px]">
                  <div>{c.image_url || c.banner_url ? "🖼️ photo/banner" : "—"} {c.video_url ? "🎬 video" : ""}</div>
                  <div className="text-gray-500">{(c.slots || []).join(", ")}</div>
                </td>
                <td className="p-2"><b className="text-[#7A0C2E]">₹{c.amount}</b><div className="text-[10px] text-gray-500">{c.days}d · ₹{c.per_day}/d</div></td>
                <td className="p-2 text-[10px]">👁️ {c.impressions} · 🖱️ {c.clicks}</td>
                <td className="p-2">
                  {c.status === "pending" ? (
                    <div className="flex flex-col gap-1">
                      <input value={utr[c.id] || ""} onChange={(e) => setUtr({ ...utr, [c.id]: e.target.value })}
                        placeholder="UTR" aria-label="UTR" className="w-28 rounded-lg border px-2 py-1" />
                      <div className="flex gap-1">
                        <button onClick={() => void approve(c.id)} className="rounded-full bg-green-600 px-3 py-1 text-white">✅ Live</button>
                        <button onClick={() => void act(c.id, "reject")} className="rounded-full bg-red-500 px-3 py-1 text-white">❌</button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex gap-1">
                      {c.status === "active"
                        ? <button onClick={() => void act(c.id, "pause")} className="rounded-full bg-gray-200 px-3 py-1">⏸️</button>
                        : <button onClick={() => void act(c.id, "resume")} className="rounded-full bg-green-600 px-3 py-1 text-white">▶️</button>}
                      <button onClick={() => void act(c.id, "expire")} className="rounded-full bg-gray-200 px-3 py-1">⏳</button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
