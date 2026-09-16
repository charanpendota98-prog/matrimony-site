"use client";

/**
 * 📱🌊 WAVE 19 — ADMIN WA numbers: OTP + Channels + Personal (+backup).
 * Add / pause / resume / delete + live health (caps, cooldowns, orders).
 */
import { useCallback, useEffect, useState } from "react";
import { authHeaders } from "@/lib/api";
import { Duo } from "@/lib/duo";

type Row = Record<string, any>;
const adminToken = () => { try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; } };
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};
const H = () => ({ ...authHeaders(true), "Content-Type": "application/json" });

const LANE_META: Record<string, { icon: string; telugu: string }> = {
  otp: { icon: "🔑", telugu: "OTP lu matrame (fast 25–60s)" },
  channels: { icon: "📢", telugu: "Channel posts (120–170s gaps)" },
  personal: { icon: "💬", telugu: "Interest/referral DMs (60–120s)" },
  both: { icon: "🛟", telugu: "Backup (failover)" },
};

export default function WANumbersConsole() {
  const [data, setData] = useState<Row | null>(null);
  const [flash, setFlash] = useState("");
  const [busy, setBusy] = useState(false);
  const [f, setF] = useState({ name: "", url: "", lane: "both", daily_cap: "60", token: "", number: "" });

  const load = useCallback(async () => {
    try {
      const d = await fetch(withToken("/api/admin/wa/numbers"), { headers: authHeaders(true) }).then((r) => r.json());
      if (d?.success) { setData(d); setFlash(""); }
      else setFlash(d.detail || "Load fail");
    } catch { setFlash("API error"); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  const act = async (method: string, url: string, body?: Row) => {
    setBusy(true); setFlash("");
    try {
      const r = await fetch(withToken(url), { method, headers: H(), body: body ? JSON.stringify(body) : undefined });
      const d = await r.json();
      setFlash(d.message_telugu || (d.success ? "✅ Done" : "⚠️ Fail"));
      await load();
    } catch { setFlash("API error"); }
    setBusy(false);
  };

  const inst: Row[] = data?.instances || [];
  return (
    <div className="mt-4 rounded-2xl border border-gold/30 bg-white p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-[#7A0C2E]">📱 <Duo en="WhatsApp Numbers (OTP / Channels / Personal)" te="వాట్సాప్ నంబర్లు" /></h3>
        <button onClick={() => void load()} className="text-xs underline">↻ refresh</button>
      </div>
      <p className="text-[11px] text-gray-500 telugu">3 separate numbers — okati down ayithe backup automatic (duplicate avvadu). Pause = temporary off.</p>
      {flash ? <p className="mt-1 text-[12px] font-medium text-maroon">{flash}</p> : null}

      <div className="mt-3 grid md:grid-cols-2 gap-2">
        {inst.map((n) => {
          const meta = LANE_META[String(n.lane)] || LANE_META.both;
          return (
            <div key={String(n.name)} className={`rounded-xl border p-3 text-[12px] ${n.paused ? "border-slate-300 bg-slate-50 opacity-70" : "border-gold/30"}`}>
              <div className="flex items-center justify-between">
                <b>{meta.icon} {String(n.name)} <span className="font-mono text-[11px] text-gray-500">· {String(n.lane)} · {String(n.number_masked || "")}</span></b>
                <span className={`px-2 py-0.5 rounded-full font-bold ${n.available ? "bg-emerald-100 text-emerald-800" : "bg-rose-100 text-rose-800"}`}>
                  {n.paused ? "⏸️ paused" : n.available ? "✅ live" : `⏳ ${n.cooldown_s || 0}s`}
                </span>
              </div>
              <div className="mt-1 text-gray-600">
                Sent today <b>{n.sent_today}/{n.daily_cap}</b> · total {n.total_sent} · fails {n.failures}
                {n.last_error ? <span className="text-rose-700"> · {String(n.last_error).slice(0, 60)}</span> : null}
              </div>
              <div className="mt-2 flex gap-2">
                <button disabled={busy} onClick={() => void act("POST", `/api/admin/wa/numbers/${n.name}`, { paused: !n.paused })}
                  className="rounded-lg border border-slate-300 px-3 py-1.5 font-bold">
                  {n.paused ? "▶️ Resume" : "⏸️ Pause"}
                </button>
                <button disabled={busy} onClick={() => { if (confirm(`${n.name} teeseyala?`)) void act("DELETE", `/api/admin/wa/numbers/${n.name}`); }}
                  className="rounded-lg border border-rose-300 px-3 py-1.5 font-bold text-rose-700">🗑️</button>
              </div>
            </div>
          );
        })}
      </div>
      {data ? (
        <div className="mt-2 text-[11px] text-gray-600">
          OTP: {(data.otp_order || []).join(" → ") || "—"} · Channels: {(data.channels_order || []).join(" → ") || "—"} · Personal: {(data.personal_order || []).join(" → ") || "—"}
        </div>
      ) : null}

      <div className="mt-3 rounded-xl bg-cream/60 border border-gold/20 p-3">
        <div className="text-[12px] font-bold text-maroon">+ {` `}<Duo en="Add number" te="నంబర్ జోడించండి" /></div>
        <div className="mt-2 grid grid-cols-2 md:grid-cols-3 gap-2">
          <input value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} placeholder="wa-otp (name)"
            className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px]" />
          <input value={f.url} onChange={(e) => setF({ ...f, url: e.target.value })} placeholder="http://wa-otp:3000"
            className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px] col-span-2" />
          <select value={f.lane} onChange={(e) => setF({ ...f, lane: e.target.value })}
            className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px]">
            {(["otp", "channels", "personal", "both"] as const).map((l) => (
              <option key={l} value={l}>{LANE_META[l].icon} {l} — {LANE_META[l].telugu}</option>
            ))}
          </select>
          <input value={f.daily_cap} onChange={(e) => setF({ ...f, daily_cap: e.target.value })} placeholder="daily cap (60)"
            inputMode="numeric" className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px]" />
          <input value={f.number} onChange={(e) => setF({ ...f, number: e.target.value })} placeholder="9198… (number)"
            inputMode="numeric" className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px]" />
          <input value={f.token} onChange={(e) => setF({ ...f, token: e.target.value })} placeholder="bridge token (optional)"
            className="rounded-lg border border-slate-300 px-2 py-1.5 text-[12px] col-span-2" />
          <button disabled={busy} onClick={() => void act("POST", "/api/admin/wa/numbers", { ...f, daily_cap: Number(f.daily_cap) || 60 })}
            className="rounded-lg maroon-gradient text-white px-3 py-1.5 text-[12px] font-bold disabled:opacity-50">
            ✅ Add
          </button>
        </div>
      </div>
    </div>
  );
}
