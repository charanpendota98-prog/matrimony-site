"use client";
/**
 * 🔑 "Mee referral link teesukondi" — TSAP ID pettandi (register appude code auto-create ayyindi).
 * Advanced: live API nunchi code + link + poster + share messages + wallet summary.
 */
import { authHeaders } from "@/lib/api";
import { useState } from "react";
import Link from "next/link";

export default function GetMyReferralCodePage() {
  const [tsapId, setTsapId] = useState("");
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState("");

  const load = async () => {
    const id = tsapId.trim().toUpperCase();
    if (!id) { setErr("TSAP ID pettandi (udaharanam: TSAP-F-2025-1042)"); return; }
    setLoading(true); setErr(""); setData(null);
    try {
      const r = await fetch(`/api/referral/${id}`, { headers: authHeaders() });
      const d = await r.json();
      if (d.ok) { setData(d); localStorage.setItem("tsap_last_id", id); }
      else setErr(d.detail || "Ee ID dorakaledu — sari ga chusukondi leda register avvandi");
    } catch {
      setErr("Server nunchi data ravaledu — malli try cheyyandi");
    }
    setLoading(false);
  };

  const copy = (t: string, l: string) => { navigator.clipboard?.writeText(t); setCopied(l); setTimeout(() => setCopied(""), 1500); };

  return (
    <main className="min-h-screen bg-[#FFF8E7] py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <Link href="/referral" className="text-sm font-bold text-[#7A0C2E]">← Referral dashboard</Link>

        <div className="mt-4 bg-white rounded-3xl p-6 shadow-sm border border-gray-200">
          <h1 className="text-xl font-extrabold text-[#7A0C2E] telugu">🔑 Mee Referral Code & Link</h1>
          <p className="mt-1 text-xs text-gray-600 telugu">
            Register ayyaka mee code automatic ga create ayyindi. Mee TSAP ID pettandi —
            link, poster (QR tho), WhatsApp messages anni ready ga istham. Friend ₹99 pay chesthe meeku <b>₹50</b>.
          </p>

          <div className="mt-4 flex flex-col sm:flex-row gap-2">
            <input value={tsapId} onChange={(e) => setTsapId(e.target.value.toUpperCase())}
              onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="TSAP-F-2025-1042 / TSAP-M-2025-1042"
              className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-sm font-mono" aria-label="TSAP-F-2025-1042 / TSAP-M-2025-1042" />
            <button onClick={load} disabled={loading}
              className="rounded-xl maroon-gradient text-white px-6 py-3 font-bold text-sm">
              {loading ? "…" : "Teesukondi →"}
            </button>
          </div>
          {err && <div className="mt-2 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs p-3">⚠️ {err}</div>}
          <div className="mt-2 text-[11px] text-gray-500 telugu">
            ID marchipoyara? Register appudu pampina WhatsApp message lo undi · leda{" "}
            <Link href="/register" className="underline font-bold text-[#7A0C2E]">kotha register</Link> cheyyandi (mee sontha code auto vastundi).
          </div>
        </div>

        {data && (
          <div className="mt-4 space-y-4">
            <div className="bg-white rounded-3xl p-6 shadow-sm border border-[#D4AF37]/40">
              <div className="text-xs text-gray-500">Mee code</div>
              <div className="text-3xl font-extrabold text-[#7A0C2E]">{data.code}</div>
              <div className="mt-3 rounded-2xl bg-[#FFF8E7] border border-[#D4AF37]/40 p-3 text-xs font-mono break-all">{data.link}</div>
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                <button onClick={() => copy(data.link, "link")} className="rounded-full bg-[#7A0C2E] text-white px-4 py-2 font-bold">🔗 Link copy</button>
                <button onClick={() => copy(data.code, "code")} className="rounded-full bg-gray-100 px-4 py-2 font-bold">#️⃣ Code copy</button>
                <a href={`/api/referral/${data.stats ? tsapId : ""}/poster.png?style=square`} className="rounded-full bg-[#0F1F3C] text-white px-4 py-2 font-bold">🖼️ Poster (QR)</a>
                <a href={data.share_kit?.whatsapp_share} target="_blank" rel="noreferrer" className="rounded-full bg-[#25D366] text-white px-4 py-2 font-bold">💬 WhatsApp share</a>
              </div>
              {copied && <div className="text-[11px] text-green-700 mt-2">✅ {copied} copy ayyindi</div>}
            </div>

            <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-200">
              <div className="font-bold text-[#7A0C2E] text-sm">📊 Mee stats</div>
              <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
                <div className="rounded-xl bg-gray-50 p-3"><div className="font-bold text-lg">{data.stats?.clicks ?? 0}</div><div className="text-[10px] text-gray-500">Clicks</div></div>
                <div className="rounded-xl bg-gray-50 p-3"><div className="font-bold text-lg">{data.stats?.registrations ?? 0}</div><div className="text-[10px] text-gray-500">Registers</div></div>
                <div className="rounded-xl bg-green-50 p-3"><div className="font-bold text-lg text-green-600">{data.stats?.paid_count ?? 0}</div><div className="text-[10px] text-gray-500">Paid</div></div>
                <div className="rounded-xl bg-[#FFF8E7] p-3"><div className="font-bold text-lg text-[#7A0C2E]">₹{data.stats?.wallet ?? 0}</div><div className="text-[10px] text-gray-500">Wallet</div></div>
              </div>
              <div className="mt-3 text-xs text-gray-600 telugu">
                💡 Friend ₹99 pay chesthe ₹50 mee wallet ki · repeat payments ki 10% · 3 pays → Silver tier (extra 5%).
              </div>
              <Link href="/referral" className="mt-3 inline-block text-xs font-bold text-[#7A0C2E] underline">
                Full dashboard (milestones, ledger, payout) →
              </Link>
            </div>
          </div>
        )}

        <div className="mt-6 bg-white rounded-3xl p-6 shadow-sm border border-gray-200 text-xs text-gray-700">
          <div className="font-bold text-[#7A0C2E]">🤝 Referral ela pani chestundi (3 steps)</div>
          <ol className="mt-2 space-y-1 list-decimal pl-5 telugu">
            <li>Mee link/poster friend ki pampandi (WhatsApp group, status, friend circle)</li>
            <li>Vaallu register cheste — vaallaki <b>+1 credit FREE</b>, meeku stats lo kanipisthundi</li>
            <li>Vaallu ₹99 (leda edaina plan) pay chesthe — <b>meeku ₹50</b> wallet ki (repeat ki 10%)</li>
          </ol>
          <div className="mt-2 text-[11px] text-gray-500">
            Payout: wallet ₹100 datithe UPI ki adagochu (3 working days, UTR tho) · Self-referral/fake registrations ban.
          </div>
        </div>
      </div>
    </main>
  );
}
