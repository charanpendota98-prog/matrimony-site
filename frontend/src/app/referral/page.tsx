"use client";
/**
 * 🤝 REFERRAL DASHBOARD — Mana Vivaha 2.0
 * ======================================
 * "₹99 kabatti first time vallu pay chestharu — kabatti manam ₹50 istham referal vallaki."
 * Ee page live API nunchi: code, link, clicks, registrations, payments, wallet,
 * tier, milestones, ledger, payouts, share kit (5 Telugu messages), poster (QR tho).
 */
import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { SITE_CONFIG } from "@/lib/site-config";
import { Duo, duo } from "@/lib/duo";
import { useLang } from "@/lib/lang";
import { authHeaders } from "@/lib/api";
import AuthGate from "@/components/AuthGate";

type Dash = any;

export default function ReferralPage() {
  const { lang } = useLang();
  const te = lang === "te";
  const [tsapId, setTsapId] = useState("");
  const [dash, setDash] = useState<Dash | null>(null);
  const [board, setBoard] = useState<any[]>([]);
  const [terms, setTerms] = useState<any>(null);
  const [msgIdx, setMsgIdx] = useState(0);
  const [err, setErr] = useState("");
  const [pay, setPay] = useState({ open: false, amount: "", upi: "", method: "upi" });
  const [payRes, setPayRes] = useState<any>(null);
  const [copied, setCopied] = useState("");
  const [needsLogin, setNeedsLogin] = useState(false);   // 🐞 FIX: referral dashboard owner-only — token lekapote 401

  /* ---------- load ---------- */
  useEffect(() => {
    // ?id=TSAP-... (register success nunchi vaste) → adi mundu chudu, tarvata localStorage
    const q = new URLSearchParams(window.location.search);
    const fromUrl = (q.get("id") || q.get("tsap_id") || "").toUpperCase().trim();
    const profiles = JSON.parse(localStorage.getItem("tsap_profiles") || "[]");
    const id = (fromUrl || profiles[0]?.id || profiles[0]?.tsap_id || localStorage.getItem("tsap_last_id") || "") as string;
    if (fromUrl) localStorage.setItem("tsap_last_id", fromUrl);
    if (!id) { setNeedsLogin(true); return; }
    setTsapId(id);
  }, []);

  const load = useCallback((id: string) => {
    if (!id) return;
    // 🐞 FIX: private dashboard — X-Tsap-Token pampali (lekapote 401 → mee account lo login cheyyali)
    fetch(`/api/referral/${id}`, { headers: authHeaders() })
      .then((r) => { if (r.status === 401) { setNeedsLogin(true); return { detail: te ? "🔒 మీ account లో login చెయ్యండి (OTP) — అప్పుడే మీ referral dashboard కనిపిస్తుంది" : "🔒 Login to your account (OTP) — only then your referral dashboard shows" }; } return r.json(); })
      .then((d) => { if (d.ok) setDash(d); else setErr(d.detail || (te ? "Dashboard load అవ్వలేదు" : "Dashboard failed to load")); })
      .catch(() => setErr(te ? "Server నుంచి data రాలేదు — API check చెయ్యండి" : "No data from server — check API"));
    fetch(`/api/referral/${id}/payouts`, { headers: authHeaders() }).then((r) => r.json()).then((d) => d.success && setDash((prev: Dash) => prev ? { ...prev, payouts_live: d.payouts, payout_meta: d } : prev)).catch(() => { });
  }, []);

  useEffect(() => { if (tsapId) load(tsapId); }, [tsapId, load]);
  useEffect(() => {
    fetch("/api/referral/leaderboard?period=all&limit=10").then((r) => r.json()).then((d) => setBoard(d.leaderboard || [])).catch(() => { });
    fetch("/api/referral/terms").then((r) => r.json()).then(setTerms).catch(() => { });
  }, []);

  const s = dash?.stats || {};
  const tier = dash?.tier || { key: "BRONZE", icon: "🥉", perks: [] };
  const next = dash?.next_milestone;
  const link = dash?.link || "";
  const kit = dash?.share_kit || {};
  const msgs: string[] = kit.whatsapp_messages || [];

  const copy = (text: string, label: string) => {
    navigator.clipboard?.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(""), 1800);
  };

  const submitPayout = async () => {
    const amount = parseInt(pay.amount || "0", 10);
    const url = `/api/referral/payout?tsap_id=${encodeURIComponent(tsapId)}&amount=${amount}&method=${pay.method}&upi_id=${encodeURIComponent(pay.upi)}`;
    const r = await fetch(url, { method: "POST" });
    const d = await r.json();
    setPayRes(d);
    if (d.success) { setPay({ ...pay, open: false, amount: "" }); load(tsapId); }
  };

  const progress = next
    ? Math.min(100, Math.round(((s.paid_count || 0) / (s.paid_count + next.need)) * 100))
    : 100;

  return (
    <main className="min-h-screen bg-[#FFF8E7] pb-16">
      {/* HERO */}
      <section className="maroon-gradient text-white">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h1 className="text-2xl md:text-3xl font-extrabold telugu">🤝 <Duo en="Referral Program" te="రెఫరల్ ప్రోగ్రామ్" /> — <span className="text-[#D4AF37]">{duo("₹50 per paying referral", "చెల్లించిన ప్రతి రెఫరల్‌కు ₹50")}</span></h1>
              <p className="text-xs md:text-sm opacity-90 telugu mt-1">
{te ? <>మీ friend ₹99 (లేదా ఏదైనా plan ≥₹29) pay చేస్తే — మీకు <b>₹50 flat</b> · వాళ్లకి <b>+1 credit FREE</b> · ₹50 ఒక్కసారి మాత్రమే, అంతే (tiers = badges)
                {" "}<span className="text-[#D4AF37] font-bold">ఎవ్వరు ఎన్ని అయినా refer చెయ్యొచ్చు — limit లేదు, conditions లేవు.</span></> : <>When your friend pays ₹99 (or any plan ≥₹29) — you get <b>₹50 flat</b> · they get <b>+1 credit FREE</b> · ₹50 only once, that\u2019s it (tiers = badges)
                {" "}<span className="text-[#D4AF37] font-bold">Anyone can refer any number — no limit, no conditions.</span></>}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Link href="/referral/register" className="rounded-full bg-[#D4AF37] text-[#7A0C2E] px-4 py-2 text-xs font-bold shadow-soft">{te ? "🎁 రెఫరర్‌గా చేరండి →" : "🎁 Become a referrer →"}</Link>
              <Link href="/pricing" className="rounded-full bg-white/15 border border-white/25 px-4 py-2 text-xs font-bold">Pricing 💰</Link>
            </div>
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
            <span className="px-3 py-1 rounded-full bg-white/10">ID: <b>{tsapId || "…"}</b></span>
            <input value={tsapId} onChange={(e) => setTsapId(e.target.value.toUpperCase())}
              className="px-3 py-1.5 rounded-full bg-white/10 border border-white/25 text-white placeholder-white/60 text-xs w-56"
              placeholder={te ? "మీ TSAP ID (TSAP-F-2025-1042)" : "Your TSAP ID (TSAP-F-2025-1042)"} aria-label={te ? "మీ TSAP ID" : "Your TSAP ID"} />
            <span className="px-3 py-1 rounded-full bg-[#D4AF37] text-[#7A0C2E] font-bold">{tier.icon} {tier.key}</span>
            {s.paid_count > 0 && <span className="px-3 py-1 rounded-full bg-white/10">{s.paid_count} paying referrals</span>}
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4">
        {err && <div className="mt-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs p-3">⚠️ {err}</div>}

        {/* CODE CARD */}
        <section className="mt-6 grid md:grid-cols-3 gap-4">
          <div className="md:col-span-2 bg-white rounded-3xl p-5 border border-[#D4AF37]/40 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <div className="text-xs text-gray-500">{te ? "మీ referral code" : "Your referral code"}</div>
                <div className="text-3xl font-extrabold text-[#7A0C2E] tracking-wide">{dash?.code || "…"}</div>
                {dash?.alias && <div className="text-[11px] text-gray-500 mt-1">alias: {dash.alias} {te ? "(ఇది కూడా పని చేస్తుంది)" : "(this works too)"}</div>}
              </div>
              <div className="flex flex-col gap-2 text-xs">
                <button onClick={() => copy(link, "link")} className="rounded-full bg-[#7A0C2E] text-white px-4 py-2 font-bold">{te ? "🔗 Link copy" : "🔗 Copy link"}</button>
                <button onClick={() => copy(dash?.code || "", "code")} className="rounded-full bg-gray-100 px-4 py-2 font-bold">{te ? "#️⃣ Code copy" : "#️⃣ Copy code"}</button>
              </div>
            </div>

            <div className="mt-3 rounded-2xl bg-[#FFF8E7] border border-[#D4AF37]/40 p-3 text-xs font-mono break-all">{link || "https://manavivaha.in/r/…"}</div>
            {copied && <div className="text-[11px] text-green-700 mt-1">{te ? <>✅ {copied} copy అయ్యింది</> : <>✅ {copied} copied</>}</div>}

            {/* STATS */}
            <div className="mt-4 grid grid-cols-3 md:grid-cols-6 gap-2 text-center">
              {[
                { l: "Clicks", v: s.clicks ?? 0, c: "" },
                { l: "Registers", v: s.registrations ?? 0, c: "" },
                { l: "Paid", v: s.paid_count ?? 0, c: "text-green-600" },
                { l: "Wallet", v: `₹${s.wallet ?? 0}`, c: "text-[#7A0C2E]" },
                { l: "Lifetime", v: `₹${s.lifetime_earned ?? 0}`, c: "" },
                { l: "Conv %", v: `${s.conversion_pct ?? 0}%`, c: "" },
              ].map((x) => (
                <div key={x.l} className="rounded-xl bg-gray-50 p-2">
                  <div className={`font-bold text-lg ${x.c}`}>{x.v}</div>
                  <div className="text-[10px] text-gray-500">{x.l}</div>
                </div>
              ))}
            </div>

            {/* FUNNEL */}
            <div className="mt-4">
              <div className="text-xs font-bold text-[#7A0C2E]">📊 Funnel — link → register → pay</div>
              <div className="mt-2 flex h-3 rounded-full overflow-hidden bg-gray-100">
                <div className="bg-[#7A0C2E]" style={{ width: `${Math.min(100, (s.registrations || 0) / Math.max(1, s.clicks || 1) * 100)}%` }} />
                <div className="bg-green-500" style={{ width: `${Math.min(100, (s.paid_count || 0) / Math.max(1, s.clicks || 1) * 100)}%` }} />
              </div>
              <div className="flex gap-4 text-[10px] text-gray-500 mt-1">
                <span>■ {s.clicks || 0} clicks</span><span className="text-[#7A0C2E]">■ {s.registrations || 0} registers</span><span className="text-green-600">■ {s.paid_count || 0} paid</span>
              </div>
            </div>
          </div>

          {/* WALLET + PAYOUT */}
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <div className="text-xs text-gray-500">Wallet balance</div>
            <div className="text-3xl font-extrabold text-[#7A0C2E]">₹{s.wallet ?? 0}</div>
            <div className="text-[11px] text-gray-500 mt-1">
              Pending payout ₹{s.pending_payout ?? 0} · paid out ₹{s.paid_out ?? 0} · min payout ₹{dash?.commission_rules?.min_payout ?? 100}
            </div>
            <button
              onClick={() => setPay({ ...pay, open: !pay.open, amount: String(Math.floor(s.wallet || 0)) })}
              disabled={!dash?.wallet_can_withdraw}
              className={`mt-3 w-full rounded-xl py-2.5 font-bold text-sm ${dash?.wallet_can_withdraw ? "gold-gradient text-[#7A0C2E]" : "bg-gray-100 text-gray-400"}`}>
              {dash?.wallet_can_withdraw ? (te ? "💸 Payout అడగండి (UPI)" : "💸 Request payout (UPI)") : te ? `₹${Math.max(0, 100 - (s.wallet || 0))} ఇంకా కావాలి` : `₹${Math.max(0, 100 - (s.wallet || 0))} more needed`}
            </button>
            <div className="mt-2 text-[11px] text-gray-500 telugu">{dash?.message_telugu}</div>

            {pay.open && (
              <div className="mt-3 rounded-xl border border-[#D4AF37]/40 bg-[#FFF8E7] p-3 text-xs">
                <div className="font-bold text-[#7A0C2E]">💸 Payout request</div>
                <input value={pay.amount} onChange={(e) => setPay({ ...pay, amount: e.target.value.replace(/\D/g, "") })}
                  className="mt-2 w-full rounded-lg border px-3 py-2" placeholder="Amount (min ₹100)" aria-label="Amount (min ₹100)" />
                <input value={pay.upi} onChange={(e) => setPay({ ...pay, upi: e.target.value })}
                  className="mt-2 w-full rounded-lg border px-3 py-2" placeholder={te ? "UPI ID — ఉదాహరణ: name@okhdfcbank" : "UPI ID — e.g. name@okhdfcbank"} aria-label="UPI ID" />
                <button onClick={submitPayout} className="mt-2 w-full rounded-lg bg-[#7A0C2E] text-white py-2 font-bold">{te ? "Request పంపు" : "Send request"}</button>
                <div className="text-[10px] text-gray-500 mt-1">{te ? "3 working days లో మీ UPI కి — UTR తో confirm అవుతుంది." : "To your UPI in 3 working days — confirmed with UTR."}</div>
              </div>
            )}
            {payRes && (
              <div className={`mt-2 rounded-xl p-2 text-[11px] ${payRes.success ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
                {payRes.message_telugu || payRes.reason}
              </div>
            )}

            {/* PAYOUT HISTORY */}
            {(dash?.payouts?.length || dash?.payouts_live?.length) ? (
              <div className="mt-4">
                <div className="text-xs font-bold text-[#7A0C2E]">Payout history</div>
                <div className="mt-1 space-y-1 text-[11px]">
                  {(dash.payouts_live || dash.payouts).slice(0, 5).map((p: any) => (
                    <div key={p.id} className="flex justify-between bg-gray-50 rounded-lg px-2 py-1.5">
                      <span>{p.id}</span>
                      <span className="font-bold">₹{p.amount}</span>
                      <span className={p.status === "paid" ? "text-green-600" : p.status === "rejected" ? "text-red-600" : "text-orange-600"}>
                        {p.status}{p.utr ? ` · ${p.utr}` : ""}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        </section>

        {/* SHARE KIT */}
        <section className="mt-6 bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h2 className="font-bold text-[#7A0C2E] telugu">📲 <Duo en="Share kit — ready messages for WhatsApp/Status" te="వాట్సాప్/స్టేటస్‌కు రెడీ మెసేజ్‌లు" /></h2>
            <div className="flex gap-2 text-xs">
              <a href={`/api/referral/${tsapId}/poster.png?style=square`} className="rounded-full bg-[#7A0C2E] text-white px-3 py-1.5 font-bold">🖼️ Poster (square)</a>
              <a href={`/api/referral/${tsapId}/poster.png?style=status`} className="rounded-full bg-[#0F1F3C] text-white px-3 py-1.5 font-bold">📱 Status poster</a>
            </div>
          </div>

          {msgs.length > 0 && (
            <>
              <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
                {msgs.map((_, i) => (
                  <button key={i} onClick={() => setMsgIdx(i)}
                    className={`px-3 py-1 rounded-full font-bold ${msgIdx === i ? "bg-[#D4AF37] text-[#7A0C2E]" : "bg-gray-100"}`}>
                    Message {i + 1}
                  </button>
                ))}
              </div>
              <div className="mt-2 rounded-2xl bg-[#FFF8E7] border border-[#D4AF37]/40 p-3 text-xs whitespace-pre-wrap">{msgs[msgIdx]}</div>
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                <a href={kit.whatsapp_share_variants?.[msgIdx] || kit.whatsapp_share} target="_blank" rel="noreferrer"
                  className="rounded-full bg-[#25D366] text-white px-4 py-2 font-bold">{te ? "💬 WhatsApp కి పంపు" : "💬 Send to WhatsApp"}</a>
                <a href={kit.telegram_share} target="_blank" rel="noreferrer"
                  className="rounded-full bg-[#0088cc] text-white px-4 py-2 font-bold">✈️ Telegram share</a>
                <button onClick={() => copy(msgs[msgIdx], "message")} className="rounded-full bg-gray-100 px-4 py-2 font-bold">📋 Copy</button>
                <a href={`sms:?&body=${encodeURIComponent(kit.sms_text || "")}`} className="rounded-full bg-gray-100 px-4 py-2 font-bold">✉️ SMS</a>
              </div>
            </>
          )}

          <div className="mt-4 grid md:grid-cols-3 gap-3 text-xs">
            {(dash?.commission_rules) && Object.entries(dash.commission_rules).map(([k, v]) => (
              <div key={k} className="rounded-xl bg-gray-50 p-3">
                <div className="font-bold text-[#7A0C2E] capitalize">{k.replace(/_/g, " ")}</div>
                <div className="text-gray-600 mt-0.5">{String(v)}</div>
              </div>
            ))}
          </div>
        </section>

        {/* TIERS + MILESTONES */}
        <section className="mt-6 grid md:grid-cols-2 gap-4">
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">🏆 <Duo en="Tiers — refer more, earn more %" te="ఎక్కువ రెఫర్ చేస్తే ఎక్కువ %" /></h2>
            <div className="mt-3 space-y-2 text-xs">
              {(dash?.tiers || []).map((t: any) => (
                <div key={t.key} className={`flex items-center justify-between rounded-xl p-3 ${t.key === tier.key ? "bg-[#D4AF37]/20 border border-[#D4AF37]" : "bg-gray-50"}`}>
                  <div>
                    <div className="font-bold">{t.icon} {t.key} <span className="text-gray-500 font-normal">({t.min}+ pays)</span></div>
                    <div className="text-[11px] text-gray-500">{(t.perks || []).join(" • ")}</div>
                  </div>
                  <div className="font-bold text-[#7A0C2E]">{t.key === tier.key ? (te ? "← మీ tier" : "← your tier") : t.icon}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">🎯 <Duo en="Milestones — badges + recognition" te="మైలురాళ్లు — బ్యాడ్జ్‌లు" /></h2>
            <div className="mt-3">
              <div className="h-3 rounded-full bg-gray-100 overflow-hidden">
                <div className="h-3 bg-[#7A0C2E]" style={{ width: `${progress}%` }} />
              </div>
              <div className="text-[11px] text-gray-500 mt-1">
                {next ? (te ? `${next.need} more paying referrals → ${next.title} (badge)` : `${next.need} more paying referrals → ${next.title} (badge)`) : (te ? "👑 అన్ని milestones complete!" : "👑 All milestones complete!")}
              </div>
            </div>
            <div className="mt-3 space-y-2 text-xs">
              {(dash?.milestones || []).map((m: any) => {
                const hit = (dash?.milestones_hit || []).includes(m.paid);
                return (
                  <div key={m.paid} className={`rounded-xl p-3 ${hit ? "bg-green-50 border border-green-200" : "bg-gray-50"}`}>
                    <div className="font-bold">{hit ? "✅" : "⬜"} {m.title} <span className="text-gray-500 font-normal">({m.paid} pays)</span></div>
                    <div className="text-[11px] text-gray-600 telugu">{m.telugu}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* RECENT + LEDGER */}
        <section className="mt-6 grid md:grid-cols-2 gap-4">
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">{te ? "👥 మీ referrals (recent)" : "👥 Your referrals (recent)"}</h2>
            {(dash?.recent_registrations || []).length === 0 && <div className="mt-2 text-xs text-gray-500">{te ? "ఇంకా ఎవరూ register అవ్వలేదు — మీ link share చెయ్యండి 🙂" : "Nobody registered yet — share your link 🙂"}</div>}
            <div className="mt-2 space-y-1 text-xs">
              {(dash?.recent_registrations || []).map((r: any) => (
                <div key={r.tsap_id} className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 gap-2">
                  <div className="min-w-0">
                    <div className="font-bold text-[13px] truncate">{r.name || r.tsap_id}</div>
                    <div className="font-mono text-[10px] text-gray-500">{r.tsap_id} · {String(r.joined || "").slice(0, 10)}</div>
                  </div>
                  <span className={`shrink-0 text-[11px] ${r.paid ? "text-green-600 font-bold" : "text-amber-600"}`}>
                    {r.paid ? `💰 ₹${r.commission ?? 50} ✅` : "⏳ pay pending"}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">🧾 Wallet ledger (audit)</h2>
            {(dash?.ledger || []).length === 0 && <div className="mt-2 text-xs text-gray-500">{te ? "Ledger ఖాళీ — మొదటి referral తో start అవుతుంది" : "Ledger empty — starts with first referral"}</div>}
            <div className="mt-2 space-y-1 text-[11px] max-h-72 overflow-y-auto">
              {(dash?.ledger || []).map((l: any) => (
                <div key={l.id} className="flex items-center justify-between border-b border-gray-100 py-1.5">
                  <div>
                    <div className="font-bold">
                      {l.type === "payout_paid" ? <span className="text-green-700">✅ PAID</span> : l.type}{l.first_payment ? " (first)" : ""}
                    </div>
                    <div className="text-gray-500">{l.from || l.note}{l.utr ? ` · UTR ${l.utr}` : ""}</div>
                  </div>
                  <span className={Number(l.amount) >= 0 ? "text-green-600 font-bold" : "text-red-600 font-bold"}>
                    {l.type === "payout_paid" ? "done" : `₹${l.amount}`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* LEADERBOARD */}
        <section className="mt-6 bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
          <h2 className="font-bold text-[#7A0C2E] telugu">🏅 Top referrers — leaderboard</h2>
          <div className="text-[11px] text-gray-500">{te ? "Weekly top-1 కి ₹1000 + Elite badge" : "Weekly top-1 gets ₹1000 + Elite badge"}</div>
          <div className="mt-3 space-y-2 text-xs">
            {board.length === 0 && <div className="text-gray-500">{te ? "ఇంకా ఎవరూ — మొదటి place మీదే అవ్వచ్చు! 🥇" : "Nobody yet — first place could be yours! 🥇"}</div>}
            {board.map((b: any) => (
              <div key={b.code} className={`flex items-center gap-3 rounded-xl p-3 ${b.code === dash?.code ? "bg-[#D4AF37]/20 border border-[#D4AF37]" : "bg-gray-50"}`}>
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center font-bold">{b.rank}</div>
                <div className="flex-1">
                  <div className="font-bold">{b.name} {b.code === dash?.code && <span className="text-[10px] bg-[#7A0C2E] text-white px-2 py-0.5 rounded-full ml-1">YOU</span>}</div>
                  <div className="text-[11px] text-gray-500">{b.icon} {b.tier} • {b.refers} refers • {b.paid} paid</div>
                </div>
                <div className="font-bold text-green-600">₹{b.earned}</div>
              </div>
            ))}
          </div>
        </section>

        {/* RULES */}
        <section className="mt-6 grid md:grid-cols-2 gap-4">
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">📜 Rules ({terms?.version || "2.0"})</h2>
            <ul className="mt-2 space-y-1 text-xs text-gray-700">
              {(terms?.rules_telugu || []).map((r: string, i: number) => <li key={i}>{r.replace(/\*\*/g, "")}</li>)}
            </ul>
          </div>
          <div className="bg-white rounded-3xl p-5 border border-gray-200 shadow-sm">
            <h2 className="font-bold text-[#7A0C2E] telugu">{te ? "🚫 చెయ్యకూడదు (ban అవుతుంది)" : "🚫 Don\u2019t do this (leads to ban)"}</h2>
            <ul className="mt-2 space-y-1 text-xs text-gray-700">
              {(terms?.not_allowed || ["Self-referral", "Fake registrations", "Spam/bots"]).map((r: string) => <li key={r}>⛔ {r}</li>)}
            </ul>
            <div className="mt-3 rounded-xl bg-[#FFF8E7] border border-[#D4AF37]/40 p-3 text-[11px] text-[#7A0C2E]">
              {te ? "💡 Tip: మీ caste/district WhatsApp group లో poster + message పెట్టండి — weekend లో ఎక్కువ registrations వస్తాయి." : "💡 Tip: post the poster + message in your caste/district WhatsApp group — more registrations on weekends."}
            </div>
            <div className="mt-3 flex flex-wrap gap-2 text-xs">
              <Link href="/pricing" className="underline font-bold text-[#7A0C2E]">Pricing</Link>
              <Link href="/channels" className="underline font-bold text-[#7A0C2E]">Channels</Link>
              <a href={SITE_CONFIG.supportLink} className="underline font-bold text-[#7A0C2E]">Support WhatsApp</a>
            </div>
          </div>
        </section>
        {needsLogin && <AuthGate
          title={te ? "🔒 మీ referral dashboard కి OTP login కావాలి" : "🔒 OTP login needed for your referral dashboard"}
          note={te ? "మీ referral code, clicks, wallet, payouts — ఇవి మీ account data. OTP తో login చెయ్యండి, అప్పుడే కనిపిస్తుంది (వేరే వాళ్లకి కనిపించదు)." : "Your referral code, clicks, wallet, payouts — this is your account data. Login with OTP to see it (others can\u2019t)."} />}

      </div>
    </main>
  );
}
