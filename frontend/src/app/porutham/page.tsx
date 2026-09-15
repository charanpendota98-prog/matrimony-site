"use client";

/**
 * /porutham — 10-PORUTHAM FULL REPORT (advanced, printable, shareable) 💍
 * ======================================================================
 * Top matrimony sites lo "kundli match" paid add-on (₹300+). Manam:
 *   • 10 porutham lu — prathi daaniki pass/fail + Telugu note
 *   • Score /10 + stars + Telugu verdict + dosha (రజ్జు/వేధ) alert
 *   • WhatsApp lo share cheyyadaniki ready-made report IMAGE (backend Pillow)
 *   • 🖨️ Print / Save as PDF (purohitulu/pedda vaallaki chupinchadaniki)
 *   • Star teliyakapote — star/rasi direct ga select chesi kooda calculate cheyyachu
 */
import { Suspense, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { NAKSHATRAS, RASIS } from "@/lib/telugu-data";

type Res = Record<string, any>;

function PoruthamInner() {
  const sp = useSearchParams();
  const [bride, setBride] = useState("");
  const [groom, setGroom] = useState("");
  const [myId, setMyId] = useState("");
  const [bStar, setBStar] = useState("");
  const [gStar, setGStar] = useState("");
  const [bRasi, setBRasi] = useState("");
  const [gRasi, setGRasi] = useState("");
  const [mode, setMode] = useState<"id" | "star">("id");
  const [res, setRes] = useState<Res | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [imgOk, setImgOk] = useState(true);

  useEffect(() => {
    const mine = (localStorage.getItem("tsap_id") || "").toUpperCase();
    if (mine) setMyId(mine);
    const qb = (sp.get("bride") || "").toUpperCase();
    const qg = (sp.get("groom") || "").toUpperCase();
    if (qb) setBride(qb);
    if (qg) setGroom(qg);
    else if (mine) setGroom(mine);
  }, [sp]);

  const calcById = useCallback(async (b: string, g: string) => {
    if (!b || !g) { setErr("Rendu TSAP IDs ivvandi (bride + groom)"); return; }
    setBusy(true); setErr("");
    try {
      const d = await fetch(`/api/porutham?bride=${encodeURIComponent(b)}&groom=${encodeURIComponent(g)}`).then((r) => r.json());
      if (d.detail) { setErr(d.detail); setRes(null); } else { setRes({ ...d, _bride: b, _groom: g }); setImgOk(true); }
    } catch { setErr("Network problem — malli try cheyyandi"); }
    setBusy(false);
  }, []);

  const calcByStar = async () => {
    if (!bStar || !gStar) { setErr("Bride + Groom star (nakshatram) select cheyyandi"); return; }
    setBusy(true); setErr("");
    try {
      const d = await fetch("/api/porutham", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bride_star: bStar, bride_rasi: bRasi, groom_star: gStar, groom_rasi: gRasi }),
      }).then((r) => r.json());
      setRes({ ...d, _bride: bStar, _groom: gStar, _byStar: true });
    } catch { setErr("Network problem — malli try cheyyandi"); }
    setBusy(false);
  };

  const shareWa = () => {
    if (!res) return;
    const txt = `💍 10-Porutham Report — Mana Vivaha\n${res.bride?.full_name || res._bride} ❤️ ${res.groom?.full_name || res._groom}\n`
      + `Score: ${res.score}/${res.max_score} (${res.stars}★)\n${res.verdict}\n`
      + `Details: https://manavivaha.in/porutham`;
    window.open(`https://wa.me/?text=${encodeURIComponent(txt)}`, "_blank");
  };

  const shareImg = () => {
    if (!res?._bride || !res?._groom || res._byStar) return;
    const url = `${window.location.origin}/api/og/porutham/${encodeURIComponent(res._bride)}/${encodeURIComponent(res._groom)}.png`;
    window.open(url, "_blank");
  };

  const items: Res[] = res?.items || [];

  return (
    <main className="min-h-screen bg-cream pb-16">
      <section className="maroon-gradient text-white print:!bg-white print:!text-maroon">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="text-[11px] font-bold bg-white/10 border border-white/20 rounded-full px-3 py-1 inline-block">
            💍 10-Porutham • Traditional Telugu kundli match
          </div>
          <h1 className="mt-3 text-2xl md:text-3xl font-bold">Pelli porutham full report</h1>
          <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
            Rasi • Nakshatra • Gana • Yoni • Rajju • Vedha • Mahendra • Stree Deergha • Vashya • Rasi Adhipathi —
            10 porutham lu okate chota, Telugu explanation tho. Rajju/Vedha dosha unte manam mundhe warning istham.
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
            <span className="bg-white/10 border border-white/20 rounded-full px-3 py-1.5">📄 Print/PDF report</span>
            <span className="bg-white/10 border border-white/20 rounded-full px-3 py-1.5">🖼️ WhatsApp share image</span>
            <span className="bg-white/10 border border-white/20 rounded-full px-3 py-1.5">🎁 Add-on ₹49 lo detailed</span>
          </div>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 py-5 space-y-4">
        {/* ---------- input card ---------- */}
        <div className="bg-white rounded-[1.5rem] border border-gold/25 p-4 print:hidden">
          <div className="flex gap-2">
            {([["id", "🎫 TSAP ID tho"], ["star", "⭐ Star tho (register avvakunda)"]] as const).map(([v, l]) => (
              <button key={v} onClick={() => setMode(v)} className={`chip ${mode === v ? "chip-on" : ""}`}>{l}</button>
            ))}
          </div>

          {mode === "id" ? (
            <div className="mt-3 grid md:grid-cols-3 gap-3">
              <div>
                <label className="text-[12px] font-bold">👰 Bride TSAP ID</label>
                <input value={bride} onChange={(e) => setBride(e.target.value.toUpperCase())} placeholder="TSAP-F-2025-1042" className="input-mobile font-mono" />
              </div>
              <div>
                <label className="text-[12px] font-bold">🤵 Groom TSAP ID</label>
                <input value={groom} onChange={(e) => setGroom(e.target.value.toUpperCase())} placeholder="TSAP-M-2025-1042" className="input-mobile font-mono" />
              </div>
              <div className="flex items-end">
                <button onClick={() => calcById(bride, groom)} disabled={busy}
                  className="w-full py-3.5 rounded-2xl maroon-gradient text-white font-bold text-[13px] disabled:opacity-60">
                  {busy ? "Calculate…" : "💍 Porutham chudu"}
                </button>
              </div>
            </div>
          ) : (
            <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">
              <div>
                <label className="text-[12px] font-bold">Bride star</label>
                <select value={bStar} onChange={(e) => setBStar(e.target.value)} className="input-mobile">
                  <option value="">— select —</option>
                  {NAKSHATRAS.map((n) => <option key={n.en} value={n.en}>{n.te} ({n.en})</option>)}
                </select>
              </div>
              <div>
                <label className="text-[12px] font-bold">Bride rasi</label>
                <select value={bRasi} onChange={(e) => setBRasi(e.target.value)} className="input-mobile">
                  <option value="">— auto —</option>
                  {RASIS.map((r) => <option key={r.en} value={r.en}>{r.te} ({r.en})</option>)}
                </select>
              </div>
              <div>
                <label className="text-[12px] font-bold">Groom star</label>
                <select value={gStar} onChange={(e) => setGStar(e.target.value)} className="input-mobile">
                  <option value="">— select —</option>
                  {NAKSHATRAS.map((n) => <option key={n.en} value={n.en}>{n.te} ({n.en})</option>)}
                </select>
              </div>
              <div>
                <label className="text-[12px] font-bold">Groom rasi</label>
                <select value={gRasi} onChange={(e) => setGRasi(e.target.value)} className="input-mobile">
                  <option value="">— auto —</option>
                  {RASIS.map((r) => <option key={r.en} value={r.en}>{r.te} ({r.en})</option>)}
                </select>
              </div>
              <div className="col-span-2 md:col-span-4">
                <button onClick={calcByStar} disabled={busy}
                  className="w-full py-3.5 rounded-2xl maroon-gradient text-white font-bold text-[13px] disabled:opacity-60">
                  {busy ? "Calculate…" : "💍 Porutham chudu (star tho)"}
                </button>
              </div>
            </div>
          )}
          {myId && mode === "id" && (
            <div className="mt-2 text-[11px] text-gray-600">
              Mee ID: <b className="font-mono">{myId}</b> —{" "}
              <button onClick={() => calcById(myId, groom || bride)} className="text-maroon font-bold underline">
                naa ID ki vere profile tho compare cheyyi
              </button>
            </div>
          )}
          {err && <div className="mt-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl px-3 py-2 text-[12px]">{err}</div>}
        </div>

        {/* ---------- report ---------- */}
        {res && (
          <>
            <div className="bg-white rounded-[1.5rem] border border-gold/25 p-5">
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <div className="shrink-0 w-[124px] h-[124px] rounded-full maroon-gradient text-center flex flex-col items-center justify-center mx-auto md:mx-0">
                  <div className="text-4xl font-bold text-white">{res.score}<span className="text-[16px] opacity-80">/10</span></div>
                  <div className="text-[10px] text-[#EAD08A] mt-0.5">{res.percent}%</div>
                </div>
                <div className="flex-1 text-center md:text-left">
                  <div className="text-[17px] font-bold text-maroon telugu">{res.verdict}</div>
                  <div className="mt-1 text-[13px] text-gray-700">
                    {"★".repeat(res.stars || 0)}{"☆".repeat(5 - (res.stars || 0))} •{" "}
                    {res.available ? `${items.filter((i) => i.pass).length} porutham lu pass` : "data saripoledu"}
                  </div>
                  {res.available && (
                    <div className="mt-1.5 text-[12px] text-gray-700">
                      👰 {res.bride?.full_name || res._bride} — <b>{(res.bride_star_en || "")} ({res.bride_star || ""})</b>, {res.bride_rasi || ""}<br />
                      🤵 {res.groom?.full_name || res._groom} — <b>{(res.groom_star_en || "")} ({res.groom_star || ""})</b>, {res.groom_rasi || ""}
                    </div>
                  )}
                  {res.doshas?.length ? (
                    <div className="mt-2 inline-block bg-rose-50 border border-rose-200 text-rose-800 rounded-xl px-3 py-1.5 text-[11px] font-bold">
                      ⚠️ Dosha: {res.doshas.join(" + ")} — పెద్దలు/పురోహితులను సంప్రదించండి
                    </div>
                  ) : null}
                </div>
              </div>

              {res.available && items.length > 0 && (
                <div className="mt-4 grid md:grid-cols-2 gap-2">
                  {items.map((it) => (
                    <div key={it.no} className={`rounded-2xl p-3 border ${it.pass ? "bg-emerald-50/60 border-emerald-200" : "bg-rose-50/60 border-rose-200"}`}>
                      <div className="flex items-center gap-2">
                        <span className={`w-6 h-6 rounded-full text-white text-[12px] font-bold flex items-center justify-center ${it.pass ? "bg-emerald-600" : "bg-rose-600"}`}>
                          {it.pass ? "✓" : "✗"}
                        </span>
                        <span className="text-[13px] font-bold text-ink">{it.no}. {it.name}</span>
                        <span className="text-[11px] text-gray-500 telugu">{it.telugu}</span>
                      </div>
                      <div className="mt-1 text-[11px] text-gray-700 telugu leading-relaxed">{it.note}</div>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-3 bg-cream rounded-2xl p-3 text-[11px] text-gray-700 telugu leading-relaxed">
                🕉️ {res.advice_telugu || res.reason}
              </div>

              <div className="mt-4 flex flex-wrap gap-2 print:hidden">
                <button onClick={() => window.print()} className="px-4 py-3 rounded-2xl maroon-gradient text-white font-bold text-[12px]">🖨️ Print / PDF report</button>
                <button onClick={shareWa} className="px-4 py-3 rounded-2xl bg-green-600 text-white font-bold text-[12px]">WhatsApp share</button>
                {!res._byStar && <button onClick={shareImg} className="px-4 py-3 rounded-2xl border border-maroon/25 text-maroon font-bold text-[12px]">🖼️ Report image</button>}
                <Link href="/requests" className="px-4 py-3 rounded-2xl border border-maroon/25 text-maroon font-bold text-[12px]">💌 Interest pampu (1 credit)</Link>
              </div>
            </div>

            {/* ---------- report image preview ---------- */}
            {!res._byStar && imgOk && (
              <div className="bg-white rounded-[1.5rem] border border-gold/25 p-4 print:hidden">
                <div className="font-bold text-maroon text-[14px]">🖼️ WhatsApp lo share cheyyadaniki ready report image</div>
                <div className="text-[11px] text-gray-600 mt-1">
                  Ee image ni WhatsApp group / family ki pampandi — score, porutham lu, verdict anni kanipistayi.
                </div>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={`/api/og/porutham/${encodeURIComponent(res._bride)}/${encodeURIComponent(res._groom)}.png`}
                  onError={() => setImgOk(false)}
                  alt="Porutham report — 10 kootalu Telugu lo"
                  className="mt-3 w-full rounded-2xl border border-gold/30"
                />
              </div>
            )}
          </>
        )}

        {/* ---------- glossary ---------- */}
        <div className="bg-white rounded-[1.5rem] border border-gold/25 p-5 print:hidden">
          <div className="font-bold text-maroon text-[15px]">📚 10 porutham lu ante enti? (pelli peddalu ee 10 chustaru)</div>
          <div className="mt-3 grid md:grid-cols-2 gap-2 text-[11px] text-gray-700 telugu leading-relaxed">
            {[
              ["రాశి పొరుత్తం", "బ్రైడ్–గ్రూమ్ రాశుల మధ్య దూరం 6/8 కాకూడదు (షష్టాష్టక దోషం)."],
              ["నక్షత్ర పొరుత్తం", "నక్షత్రాల మధ్య వేధ (విరోధం) ఉండకూడదు."],
              ["గణ పొరుత్తం", "దేవ–మనుష్య–రాక్షస గణాలు కలవాలి (స్వభావం + మనస్తత్వం)."],
              ["యోని పొరుత్తం", "శారీరక + మానసిక అనుకూలత (శత్రు యోనులు కాకూడదు)."],
              ["రజ్జు పొరుత్తం", "⚠️ చాలా ముఖ్యం — ఒకే రజ్జు ఉంటే దోషం (ఆయుష్షు/ఆరోగ్యం)."],
              ["వేధ పొరుత్తం", "⚠️ ముఖ్యం — నక్షత్ర వేధ ఉంటే పరిహారం అవసరం."],
              ["మహేంద్ర పొరుత్తం", "ఐశ్వర్యం + సంతాన ప్రాప్తి కోసం (4,7,10,13,16,19,22,25 మంచివి)."],
              ["స్త్రీ దీర్ఘ", "స్త్రీకి దీర్ఘ సుమంగళి (13+ గణన) — భర్త ఆయుష్షు."],
              ["వశ్య పొరుత్తం", "ఒకరిపై ఒకరికి ఆధీనత/ప్రేమ, ఒకరినొకరు గౌరవించుకోవడం."],
              ["రాశి అధిపతి", "రాశి అధిపతుల స్నేహం — దాంపత్య బలం."],
            ].map(([t, d]) => (
              <div key={t} className="bg-cream rounded-xl p-2.5 border border-gold/20">
                <div className="font-bold text-maroon">{t}</div>
                <div className="mt-0.5">{d}</div>
              </div>
            ))}
          </div>
          <div className="mt-3 text-[11px] text-gray-500">
            🎁 <b>Detailed porutham report (PDF + purohitulu contact)</b> — add-on ₹49 (Requests page lo add cheyyandi).
          </div>
        </div>
      </div>
    </main>
  );
}

export default function PoruthamPage() {
  return (
    <Suspense fallback={<main className="min-h-screen bg-cream p-8 text-center text-[13px]">Porutham report load avutund…</main>}>
      <PoruthamInner />
    </Suspense>
  );
}
