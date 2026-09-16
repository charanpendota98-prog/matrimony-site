"use client";

/**
 * 🤝🌊 WAVE 19 — Referral Partner registration:
 * name + phone + PhonePe + address + state + district → ID (charan108) + link.
 * Link tho register → code auto-fill → vallaki ₹50/payment.
 */
import { useState } from "react";
import Link from "next/link";
import { Duo, duo } from "@/lib/duo";
import { DISTRICTS_BY_STATE } from "@/lib/telugu-data";

const STATES = ["TS", "AP", "KA", "MH", "Other"];

export default function PartnerRegisterPage() {
  const [f, setF] = useState({ name: "", phone: "", phonepe: "", address: "", state: "TS", district: "" });
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [done, setDone] = useState<{ partner_id?: string; link?: string } | null>(null);
  const [copied, setCopied] = useState(false);
  const [lookup, setLookup] = useState("");
  const [dash, setDash] = useState<any>(null);

  const set = (k: string, v: string) => setF((p) => ({ ...p, [k]: v }));
  const dists: string[] = (DISTRICTS_BY_STATE as Record<string, string[]>)[f.state] || [];

  const submit = async () => {
    setBusy(true); setMsg(""); setDone(null);
    try {
      const r = await fetch("/api/referral/partner/register", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(f),
      });
      const d = await r.json();
      if (!r.ok) { setMsg(d.detail || "Fail ayyindi"); return; }
      setDone(d);
      setMsg(d.message_telugu || "Ready!");
    } catch {
      setMsg("Network ledu — malli try cheyyandi");
    }
    setBusy(false);
  };

  const copy = async (t: string) => {
    try { await navigator.clipboard.writeText(t); setCopied(true); setTimeout(() => setCopied(false), 1500); }
    catch { /* ignore */ }
  };

  const loadDash = async () => {
    const id = lookup.trim();
    if (!id) return;
    setDash(null); setMsg("");
    try {
      const r = await fetch(`/api/referral/partner/${encodeURIComponent(id)}`);
      const d = await r.json();
      if (!r.ok) { setMsg(d.detail || "ID dorakaledu"); return; }
      setDash(d);
    } catch { setMsg("Network ledu"); }
  };

  return (
    <main className="mx-auto max-w-2xl px-4 py-8">
      <h1 className="text-2xl font-extrabold text-maroon">🤝 <Duo en="Become a Referral Partner" te="రిఫరల్ భాగస్వామి అవండి" /></h1>
      <p className="mt-1 text-sm text-slate-600 telugu">
        {duo("Details ivvandi — mee ID + link vastundi. Friends join + pay chesthe meeku ₹50/payment (wallet → UPI).",
             "వివరాలు ఇవ్వండి — మీ ID + లింక్ వస్తుంది. ఫ్రెండ్స్ జాయిన్ + పే చేస్తే మీకు ₹50/పేమెంట్.")}
      </p>

      {!done ? (
        <section className="mt-4 rounded-2xl border border-gold/30 bg-white p-4 card-shadow space-y-3">
          <div>
            <label className="text-[13px] font-bold">👤 {duo("Your name", "మీ పేరు")} *</label>
            <input value={f.name} onChange={(e) => set("name", e.target.value)} placeholder="Charan Kumar"
              className="input-mobile mt-1" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[13px] font-bold">📞 {duo("Mobile", "మొబైల్")} *</label>
              <input value={f.phone} onChange={(e) => set("phone", e.target.value.replace(/\D/g, "").slice(0, 10))}
                inputMode="numeric" placeholder="98480 12345" className="input-mobile mt-1" />
            </div>
            <div>
              <label className="text-[13px] font-bold">💰 {duo("PhonePe number", "ఫోన్‌పే నంబర్")}</label>
              <input value={f.phonepe} onChange={(e) => set("phonepe", e.target.value.replace(/\D/g, "").slice(0, 10))}
                inputMode="numeric" placeholder="Payouts ki (same aithe khali)" className="input-mobile mt-1" />
            </div>
          </div>
          <div>
            <label className="text-[13px] font-bold">🏠 {duo("Address", "చిరునామా")}</label>
            <input value={f.address} onChange={(e) => set("address", e.target.value)} placeholder="Village/Town, Mandal"
              className="input-mobile mt-1" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[13px] font-bold">🗺️ {duo("State", "రాష్ట్రం")} *</label>
              <select value={f.state} onChange={(e) => { set("state", e.target.value); set("district", ""); }}
                className="input-mobile mt-1">
                {STATES.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="text-[13px] font-bold">📍 {duo("District", "జిల్లా")} *</label>
              {dists.length ? (
                <select value={f.district} onChange={(e) => set("district", e.target.value)} className="input-mobile mt-1">
                  <option value="">Select…</option>
                  {dists.map((d) => <option key={d} value={d}>{d}</option>)}
                </select>
              ) : (
                <input value={f.district} onChange={(e) => set("district", e.target.value)} placeholder="District"
                  className="input-mobile mt-1" />
              )}
            </div>
          </div>
          {msg ? <p className="text-[13px] font-medium text-maroon">{msg}</p> : null}
          <button onClick={submit} disabled={busy}
            className="w-full rounded-2xl maroon-gradient text-white font-bold py-3 disabled:opacity-50">
            {busy ? "…" : <>🚀 <Duo en="Create my Partner ID" te="నా భాగస్వామి ID సృష్టించండి" /></>}
          </button>
        </section>
      ) : (
        <section className="mt-4 rounded-2xl border border-emerald-300 bg-emerald-50 p-5 text-center">
          <div className="text-4xl">🎉</div>
          <div className="font-bold text-emerald-900 text-lg mt-1">ID: <span className="font-mono">{done.partner_id}</span></div>
          <div className="mt-2 rounded-xl bg-white border border-emerald-200 p-3 text-[12px] font-mono break-all">{done.link}</div>
          <div className="mt-3 flex gap-2 justify-center">
            <button onClick={() => void copy(String(done.link || ""))}
              className="rounded-full bg-[#7A0C2E] text-white px-5 py-2.5 text-sm font-bold">
              {copied ? "copied ✓" : "🔗 Link copy"}
            </button>
            <button onClick={() => { setDone(null); setMsg(""); }}
              className="rounded-full border border-emerald-400 px-5 py-2.5 text-sm font-bold text-emerald-800">
              + {duo("New partner", "కొత్త భాగస్వామి")}
            </button>
          </div>
          <p className="mt-3 text-[12px] text-emerald-800 telugu">
            {duo("Ee link tho evaru register ayina — vaalla payment ki meeku ₹50 wallet lo. Dashboard kindha chudandi.",
                 "ఈ లింక్‌తో ఎవరు రిజిస్టర్ అయినా — వాళ్ల పేమెంట్‌కు మీకు ₹50 వాలెట్‌లో.")}
          </p>
        </section>
      )}

      <section className="mt-5 rounded-2xl border border-slate-200 bg-white p-4">
        <h2 className="text-sm font-bold">📊 <Duo en="My partner dashboard" te="నా భాగస్వామి డాష్‌బోర్డ్" /></h2>
        <div className="mt-2 flex gap-2">
          <input value={lookup} onChange={(e) => setLookup(e.target.value)} placeholder="charan108"
            className="flex-1 rounded-xl border border-slate-300 px-3 py-2 text-sm" />
          <button onClick={loadDash} className="rounded-xl border border-[#7A0C2E] px-4 py-2 text-sm font-bold text-maroon">
            Chudu
          </button>
        </div>
        {dash?.success ? (
          <div className="mt-3 grid grid-cols-2 gap-2 text-center text-[12px]">
            <div className="rounded-xl bg-cream p-2"><b>{dash.clicks ?? 0}</b><br />👆 Clicks</div>
            <div className="rounded-xl bg-cream p-2"><b>{dash.registrations}</b><br />Joins</div>
            <div className="rounded-xl bg-cream p-2"><b>{dash.paid_count}</b><br />Paid</div>
            <div className="rounded-xl bg-emerald-50 p-2"><b>₹{dash.wallet}</b><br />Wallet</div>
            <div className="rounded-xl bg-emerald-50 p-2 col-span-2"><b>₹{dash.lifetime_earned}</b><br />Lifetime earned</div>
            {dash.link ? (
              <div className="col-span-2 flex gap-2 justify-center">
                <button onClick={() => void copy(String(dash.link))}
                  className="rounded-full bg-[#7A0C2E] text-white px-4 py-2 text-[12px] font-bold">
                  {copied ? "copied ✓" : "🔗 Link copy"}
                </button>
                <a href={`https://wa.me/?text=${encodeURIComponent(`Mana Vivaha lo register avvandi — naa link tho join ayithe meeku +1 credit FREE 🎁 ${dash.link}`)}`}
                  target="_blank" rel="noreferrer"
                  className="rounded-full bg-[#25D366] text-white px-4 py-2 text-[12px] font-bold">
                  📲 WhatsApp share
                </a>
              </div>
            ) : null}
            {Array.isArray(dash.joins) && dash.joins.length ? (
              <div className="col-span-2 text-left rounded-xl bg-white border border-slate-200 p-2">
                <b>Joins:</b> {dash.joins.map((j: any) => `${j.name || ""} (${j.tsap_id})${j.paid ? " 💰" : ""}`).join(" · ")}
              </div>
            ) : null}
          </div>
        ) : null}
      </section>

      <p className="mt-4 text-center text-sm text-slate-600">
        <Link href="/referral" className="font-semibold text-maroon underline">← Referral home</Link>
      </p>
    </main>
  );
}
