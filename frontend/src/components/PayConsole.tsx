"use client";
/**
 * 💳 WAVE 14 — ADMIN PAYMENTS CONSOLE
 * Safe-pay orders (Razorpay verify auto / manual-UPI UTR confirm) + collection stats.
 * ADMIN ONLY.
 */
import { useEffect, useState } from "react";
import { authHeaders } from "@/lib/api";

type Row = Record<string, any>;
const adminToken = () => { try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; } };
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};

export default function PayConsole() {
  const [items, setItems] = useState<Row[]>([]);
  const [stats, setStats] = useState<Row | null>(null);
  const [status, setStatus] = useState("");
  const [utr, setUtr] = useState<Record<string, string>>({});
  const [flash, setFlash] = useState("");

  const load = async () => {
    try {
      const d = await fetch(withToken(`/api/admin/payments${status ? `?status=${status}` : ""}`),
        { headers: authHeaders(true) }).then((r) => r.json());
      if (d.success) { setItems(d.orders || []); setStats(d.stats || null); }
      else setFlash(d.detail || "Load fail");
    } catch { setFlash("Network problem"); }
  };
  useEffect(() => { void load(); }, [status]);

  const confirm = async (id: string) => {
    const u = (utr[id] || "").trim();
    if (!u) { setFlash("⚠️ UTR lekunda confirm cheyyakoodadu (audit)"); return; }
    const r = await fetch(withToken(`/api/admin/payments/${id}/confirm`),
      { method: "POST", headers: { ...authHeaders(true), "Content-Type": "application/json" },
        body: JSON.stringify({ utr: u }) });
    const d = await r.json();
    setFlash(d.message_telugu || d.detail || "done");
    void load();
  };

  return (
    <div>
      <p className="telugu mt-2 text-xs text-gray-500">
        Razorpay payments <b>auto-verify → auto-fulfill</b>. Manual-UPI orders ki UTR verify chesi <b>confirm</b> —
        appude credits/assisted/ads add (double-credit impossible — idempotent).
      </p>
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 my-3">
          {[["Orders", stats.orders], ["Paid", stats.paid], ["Pending", stats.pending],
            ["Collected ₹", stats.collected], ["Offers live", stats.offers_live]].map(([l, v]) => (
            <div key={l as string} className="rounded-xl bg-rose-50 border border-rose-100 p-2 text-center">
              <div className="text-lg font-extrabold text-[#7A0C2E]">{String(v ?? 0)}</div>
              <div className="text-[11px] text-gray-500">{l}</div>
            </div>
          ))}
        </div>
      )}
      <div className="flex gap-2 my-2">
        {[["", "anni"], ["created", "pending"], ["paid", "paid"]].map(([v, l]) => (
          <button key={v} onClick={() => setStatus(v)}
            className={`px-3 py-1 rounded-full text-xs font-bold ${status === v ? "maroon-gradient text-white" : "bg-gray-100"}`}>{l}</button>
        ))}
        <button onClick={() => void load()} className="ml-auto text-xs underline">↻ refresh</button>
      </div>
      {flash && <div className="mb-2 rounded-xl bg-[#0F1F3C] text-white text-xs p-2">{flash}</div>}
      <div className="space-y-2 max-h-[420px] overflow-auto pr-1">
        {items.map((o) => (
          <div key={o.id} className="rounded-xl border p-3 text-xs">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono font-bold">{o.id}</span>
              <span className={`px-2 py-0.5 rounded-full font-bold ${o.status === "paid" ? "bg-green-100 text-green-800" : "bg-amber-100 text-amber-800"}`}>
                {o.status}
              </span>
              <span className="font-bold">₹{o.final_amount}</span>
              {o.discount ? <span className="text-green-700">−₹{o.discount} ({o.offer_code})</span> : null}
              <span className="text-gray-500">{o.purpose}:{o.ref} • {o.tsap_id} • {o.mode}</span>
              <span className="ml-auto text-gray-400">{o.created_at}</span>
            </div>
            <div className="mt-1 text-gray-600">{o.label}</div>
            {o.status !== "paid" && (
              <div className="mt-2 flex gap-2">
                <input value={utr[o.id] || ""} onChange={(e) => setUtr({ ...utr, [o.id]: e.target.value })}
                  placeholder="UTR (12-digit)" className="flex-1 rounded-lg border px-3 py-1.5 text-xs font-mono" aria-label="UTR" />
                <button onClick={() => void confirm(o.id)}
                  className="rounded-lg bg-green-700 text-white px-4 py-1.5 text-xs font-bold">✅ Confirm + fulfill</button>
              </div>
            )}
            {o.status === "paid" && o.receipt && (
              <div className="mt-1 text-[11px] text-green-700">🧾 {o.receipt.payment_id || o.receipt.utr} • {o.paid_at}</div>
            )}
          </div>
        ))}
        {!items.length && <p className="text-xs text-gray-400">Orders levu.</p>}
      </div>
    </div>
  );
}
