"use client";
/**
 * 🎉 WAVE 14 — ADMIN OFFERS CONSOLE
 * Festival promo codes: 1-click seed + create + ON/OFF. ADMIN ONLY.
 */
import { useEffect, useState } from "react";
import { authHeaders } from "@/lib/api";

type Row = Record<string, any>;
const adminToken = () => { try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; } };
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};
const H = () => ({ ...authHeaders(true), "Content-Type": "application/json" });

export default function OffersConsole() {
  const [items, setItems] = useState<Row[]>([]);
  const [flash, setFlash] = useState("");
  const [f, setF] = useState<Row>({ code: "", title: "", pct_off: "10", flat_off: "", applies_to: "credits,assisted", valid_from: "", valid_to: "", max_uses: "100", min_amount: "", festival: "" });

  const load = async () => {
    try {
      const d = await fetch(withToken("/api/admin/offers"), { headers: authHeaders(true) }).then((r) => r.json());
      if (d?.success) setItems(d.offers || []);
      else setFlash(d.detail || "Load fail");
    } catch { setFlash("Network problem"); }
  };
  useEffect(() => { void load(); }, []);

  const seed = async () => {
    const r = await fetch(withToken("/api/admin/offers/seed"), { method: "POST", headers: H(), body: JSON.stringify({}) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void load();
  };
  const create = async () => {
    const r = await fetch(withToken("/api/admin/offers"), { method: "POST", headers: H(), body: JSON.stringify({
      code: f.code, title: f.title || f.code, pct_off: Number(f.pct_off || 0), flat_off: Number(f.flat_off || 0),
      applies_to: f.applies_to, valid_from: f.valid_from, valid_to: f.valid_to,
      max_uses: Number(f.max_uses || 100), min_amount: Number(f.min_amount || 0), festival: f.festival,
    }) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    if (r.ok) { setF({ ...f, code: "", title: "" }); void load(); }
  };
  const toggle = async (code: string) => {
    const r = await fetch(withToken(`/api/admin/offers/${code}/toggle`), { method: "POST", headers: H() });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void load();
  };

  return (
    <div>
      <p className="telugu mt-2 text-xs text-gray-500">
        Festival codes (Diwali/Sankranti/Ugadi…) — user <b>pricing lo code vesthe discount</b>. Dates + usage-cap
        server enforce chesthundi. Homepage banner auto-update.
      </p>
      <div className="flex gap-2 my-2">
        <button onClick={() => void seed()} className="rounded-xl bg-[#7A0C2E] text-white px-4 py-2 text-xs font-bold">
          🪔 Festival presets ON (Diwali25/Sankranti20/Ugadi15/First50)
        </button>
        <button onClick={() => void load()} className="text-xs underline ml-auto">↻ refresh</button>
      </div>
      {flash && <div className="mb-2 rounded-xl bg-[#0F1F3C] text-white text-xs p-2">{flash}</div>}
      <div className="rounded-xl border p-3 text-xs space-y-2 bg-rose-50/40">
        <div className="font-bold text-[#7A0C2E]">➕ Kotha offer</div>
        <div className="grid md:grid-cols-4 gap-2">
          <input value={f.code} onChange={(e) => setF({ ...f, code: e.target.value.toUpperCase() })} placeholder="CODE (ex: DIWALI25)" className="rounded-lg border px-2 py-1.5 font-mono" aria-label="Code" />
          <input value={f.title} onChange={(e) => setF({ ...f, title: e.target.value })} placeholder="Title (🪔 Diwali Dhamaka)" className="rounded-lg border px-2 py-1.5" aria-label="Title" />
          <input value={f.pct_off} onChange={(e) => setF({ ...f, pct_off: e.target.value })} placeholder="% off" inputMode="numeric" className="rounded-lg border px-2 py-1.5" aria-label="Percent off" />
          <input value={f.flat_off} onChange={(e) => setF({ ...f, flat_off: e.target.value })} placeholder="₹ flat off" inputMode="numeric" className="rounded-lg border px-2 py-1.5" aria-label="Flat off" />
          <input value={f.applies_to} onChange={(e) => setF({ ...f, applies_to: e.target.value })} placeholder="applies: credits,assisted,ads,boost" className="rounded-lg border px-2 py-1.5" aria-label="Applies to" />
          <input value={f.valid_from} onChange={(e) => setF({ ...f, valid_from: e.target.value })} placeholder="from YYYY-MM-DD" className="rounded-lg border px-2 py-1.5" aria-label="Valid from" />
          <input value={f.valid_to} onChange={(e) => setF({ ...f, valid_to: e.target.value })} placeholder="to YYYY-MM-DD" className="rounded-lg border px-2 py-1.5" aria-label="Valid to" />
          <input value={f.max_uses} onChange={(e) => setF({ ...f, max_uses: e.target.value })} placeholder="max uses" inputMode="numeric" className="rounded-lg border px-2 py-1.5" aria-label="Max uses" />
        </div>
        <button onClick={() => void create()} className="rounded-lg bg-green-700 text-white px-4 py-1.5 text-xs font-bold">✅ Create offer</button>
      </div>
      <div className="mt-2 space-y-2">
        {items.map((o) => (
          <div key={o.code} className="rounded-xl border p-2.5 text-xs flex flex-wrap items-center gap-2">
            <span className={`px-2 py-0.5 rounded-full font-bold ${o.active ? "bg-green-100 text-green-800" : "bg-gray-200 text-gray-500"}`}>{o.active ? "ON" : "OFF"}</span>
            <span className="font-mono font-bold">{o.code}</span>
            <span>{o.title}</span>
            <span className="text-green-700 font-bold">{o.pct_off ? `${o.pct_off}%` : `₹${o.flat_off}`} OFF</span>
            <span className="text-gray-500">{(o.applies_to || []).join(",")} {o.valid_to ? `• till ${o.valid_to}` : ""} • used {o.used || 0}/{o.max_uses || 0}</span>
            <button onClick={() => void toggle(o.code)} className="ml-auto rounded-lg bg-gray-800 text-white px-3 py-1 text-[11px] font-bold">ON/OFF</button>
          </div>
        ))}
        {!items.length && <p className="text-xs text-gray-400">Live offers levu — presets ON cheyyandi.</p>}
      </div>
    </div>
  );
}
