"use client";

/**
 * 🤝🌊 WAVE 19 — ADMIN referral report: evariki entha + evari referral lo evaru.
 * Partners + users, earning sort, CSV sheet download.
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

export default function ReferralReport() {
  const [data, setData] = useState<Row | null>(null);
  const [q, setQ] = useState("");
  const [flash, setFlash] = useState("");
  const [busy, setBusy] = useState(false);
  const [openId, setOpenId] = useState("");
  const [ledger, setLedger] = useState<Row | null>(null);
  const [ledgerBusy, setLedgerBusy] = useState(false);

  const payFull = async (id: string, wallet: number) => {
    const utr = prompt(`PhonePe/bank lo ₹${wallet} pampinara? UTR/reference ivvandi (wallet ₹0 avutundi):`);
    if (!utr || !utr.trim()) return;
    if (!confirm(`₹${wallet} → ${id} PAID mark + wallet ₹0? (UTR: ${utr.trim()})`)) return;
    setBusy(true);
    try {
      const r = await fetch(withToken("/api/admin/referrals/pay-full"),
        { method: "POST", headers: H(), body: JSON.stringify({ code: id, utr: utr.trim() }) });
      const d = await r.json();
      setFlash(d.message_telugu || d.detail || "done");
      if (d?.success) void load();
    } catch { setFlash("API error"); }
    setBusy(false);
  };

  const openLedger = async (id: string) => {
    if (openId === id) { setOpenId(""); setLedger(null); return; }
    setOpenId(id); setLedger(null); setLedgerBusy(true);
    try {
      const d = await fetch(withToken(`/api/admin/referrals/ledger?code=${encodeURIComponent(id)}`),
        { headers: authHeaders(true) }).then((r) => r.json());
      if (d?.success) setLedger(d);
      else setFlash(d.detail || "Ledger fail");
    } catch { setFlash("API error"); }
    setLedgerBusy(false);
  };

  const load = useCallback(async () => {
    try {
      const d = await fetch(withToken("/api/admin/referrals/report"), { headers: authHeaders(true) }).then((r) => r.json());
      if (d?.success) { setData(d); setFlash(""); }
      else setFlash(d.detail || "Load fail");
    } catch { setFlash("API error"); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  const rows: Row[] = (data?.rows || []).filter((r: Row) => {
    const s = `${r.id} ${r.name} ${r.district}`.toLowerCase();
    return !q || s.includes(q.toLowerCase());
  });

  return (
    <div className="mt-4 rounded-2xl border border-gold/30 bg-white p-4">
      <div className="flex flex-wrap items-center gap-2">
        <h3 className="font-bold text-[#7A0C2E]">🤝 <Duo en="Referral Report — who earned what" te="రిఫరల్ రిపోర్ట్" /></h3>
        <button onClick={() => void load()} className="text-xs underline">↻ refresh</button>
        <a href={withToken("/api/admin/referrals/partners.csv")} download
          className="ml-auto rounded-xl border border-emerald-500 px-3 py-1.5 text-xs font-bold text-emerald-700">
          📥 Partners sheet (CSV)
        </a>
      </div>
      {data ? (
        <p className="text-[11px] text-gray-500">
          {data.count} referrers · Wallets total ₹{data.total_wallet} · Lifetime ₹{data.total_earned}
        </p>
      ) : null}
      {flash ? <p className="text-[12px] text-maroon">{flash}</p> : null}
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="🔍 id / name / district…"
        className="mt-2 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm" />
      <div className="mt-2 max-h-[420px] overflow-auto space-y-2">
        {rows.map((r: Row) => (
          <div key={`${r.kind}:${r.id}`} className="rounded-xl border border-slate-200 p-2.5 text-[12px]">
            <div className="flex flex-wrap items-center gap-2">
              <b>{r.kind === "partner" ? "🤝" : "👤"} {String(r.name)} <span className="font-mono text-gray-500">· {String(r.id)}</span></b>
              <button onClick={() => void openLedger(String(r.id))}
                className="rounded-lg border border-[#7A0C2E]/40 px-2 py-0.5 text-[11px] font-bold text-maroon">
                {openId === String(r.id) ? "▲ close" : "📒 ledger"}
              </button>
              {Number(r.wallet) > 0 ? (
                <button disabled={busy} onClick={() => void payFull(String(r.id), Number(r.wallet))}
                  className="rounded-lg bg-emerald-700 px-2 py-0.5 text-[11px] font-bold text-white disabled:opacity-50">
                  💸 Pay ₹{r.wallet} → zero
                </button>
              ) : null}
              <span className="ml-auto font-bold text-emerald-700">₹{r.wallet} wallet · ₹{r.lifetime_earned} earned</span>
            </div>
            {openId === String(r.id) ? (
              <div className="mt-2 rounded-lg bg-cream/70 border border-gold/25 p-2">
                {ledgerBusy ? <div className="text-[11px] text-gray-500">⏳ ledger loading…</div>
                  : ledger && ledger.id === String(r.id) ? (
                    <div className="space-y-1">
                      {(ledger.joins || []).map((j: Row) => (
                        <div key={String(j.tsap_id)} className="flex flex-wrap items-center gap-2 text-[11px] bg-white rounded-lg px-2 py-1.5 border border-slate-100">
                          <b>{String(j.name || "")}</b>
                          <span className="font-mono text-gray-500">{String(j.tsap_id)}</span>
                          <span className="text-gray-500">{String(j.joined || "").slice(0, 10)}</span>
                          <span className={`ml-auto font-bold ${j.paid ? "text-emerald-700" : "text-amber-700"}`}>{String(j.status)}</span>
                        </div>
                      ))}
                      {!(ledger.joins || []).length ? <div className="text-[11px] text-gray-500">Joins levu.</div> : null}
                      <div className="text-[11px] text-gray-600 pt-1">
                        Wallet ₹{ledger.wallet} · Earned ₹{ledger.lifetime_earned} · Paid-out ₹{ledger.paid_out}
                        {Number(ledger.pending_payout) ? ` · ⏳ ₹${ledger.pending_payout} pending` : ""}
                        {" "}— chusi kindha payout queue lo UTR tho approve cheyyandi.
                      </div>
                    </div>
                  ) : <div className="text-[11px] text-gray-500">Ledger load kaledu.</div>}
              </div>
            ) : null}
            <div className="text-gray-600">
              {r.district}{r.state ? `, ${r.state}` : ""} · {r.registrations} joins · {r.paid_count} paid
              {Number(r.pending_payout) ? ` · ⏳ ₹${r.pending_payout} pending` : ""} · paid out ₹{r.paid_out}
              {r.phonepe ? ` · 📱 ${r.phonepe}` : ""}
            </div>
            {Array.isArray(r.joined_ids) && r.joined_ids.length ? (
              <div className="mt-1 text-[11px] text-gray-500 font-mono break-all">
                → {r.joined_ids.slice(0, 12).join(", ")}{r.joined_ids.length > 12 ? ` +${r.joined_ids.length - 12}` : ""}
              </div>
            ) : null}
          </div>
        ))}
        {!rows.length ? <p className="text-[12px] text-gray-500">No referrers yet.</p> : null}
      </div>
    </div>
  );
}
