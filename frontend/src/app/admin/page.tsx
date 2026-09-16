"use client";
/**
 * 🔐 ADMIN PANEL — Mana Vivaha
 * ============================
 * Tabs:
 *   👥 Profiles   → approve (auto-post ki veltundi) / manual credit gift
 *   💰 Payouts    → LIVE referral payout queue (₹50 per paying referral) — UTR tho approve, reject → wallet refund
 *   📊 Analytics  → leads, channels, referral funnel (API nunchi)
 */
import { useCallback, useEffect, useState } from "react";
import AuthGate from "@/components/AuthGate";
import MatchSend from "@/components/MatchSend";
import AstroConsole from "@/components/AstroConsole";
import AdsConsole from "@/components/AdsConsole";
import PayConsole from "@/components/PayConsole";
import OffersConsole from "@/components/OffersConsole";
import ContentConsole from "@/components/ContentConsole";
import ChannelsConsole from "@/components/ChannelsConsole";
import { apiGet, apiPost, authHeaders, getAdminKey, setAdminKey } from "@/lib/api";
import Link from "next/link";
import { Duo, duo } from "@/lib/duo";

const DEMO_PROFILES: any[] = [];
// 🐞 FIX (F05): ee list lo mundu fake rows (98480xxxxx / 98481xxxxx fake phone numbers) unnayi —
// admin ki nijam kaani data chupinche. Ippudu anni rows /api/admin/queue nunchi matrame.

export default function AdminPage() {
  const [tab, setTab] = useState("payouts");
  const [profiles, setProfiles] = useState<any[]>([]);
  const [queue, setQueue] = useState<any>({ items: [], count: 0, total_amount: 0 });
  const [utr, setUtr] = useState<Record<string, string>>({});
  const [status, setStatus] = useState("requested");
  const [search, setSearch] = useState("");
  const [flash, setFlash] = useState("");
  const [board, setBoard] = useState<any[]>([]);
  const [vQueue, setVQueue] = useState<any>({ items: [], count: 0, total_amount: 0 });
  const [vStatus, setVStatus] = useState("pending");
  const [vUtr, setVUtr] = useState<Record<string, string>>({});
  const [vRevenue, setVRevenue] = useState<any>(null);
  const [stats, setStats] = useState<any>({});
  // 🔐 WAVE 9 — admin key (X-Admin-Key) + abuse dashboard
  const [adminKey, setAdminKeyState] = useState("");
  const [needKey, setNeedKey] = useState(false);
  const [abuse, setAbuse] = useState<any>(null);

  useEffect(() => { setAdminKeyState(getAdminKey()); }, []);

  const saveAdminKey = () => {
    setAdminKey(adminKey.trim());
    setNeedKey(false);
    setFlash(adminKey.trim() ? "🔐 Admin key save ayyindi (localStorage lo — browser tarvata kooda gurtu untundi)" : "🔐 Key teesesaaru");
  };

  const loadAbuse = useCallback(async () => {
    const { ok, data, needsAdminKey } = await apiGet<any>("/api/admin/abuse", true);
    if (needsAdminKey) { setNeedKey(true); return; }
    if (ok) setAbuse(data);
  }, []);

  useEffect(() => { void loadAbuse(); }, [loadAbuse]);

  /* ---------- loaders ---------- */
  useEffect(() => {
    const p = JSON.parse(localStorage.getItem("tsap_profiles") || "[]");
    setProfiles(p.length ? p.map((x: any) => ({ ...x, status: x.status || "Pending" })) : DEMO_PROFILES);
  }, []);

  // 🔐 ADMIN_TOKEN env set unte ee token tho vellali (lekapote dev/demo mode lo open)
  const adminToken = () => {
    try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; }
  };

  const loadQueue = useCallback((st: string) => {
    const tk = adminToken();
    fetch(`/api/admin/payouts?status=${st}${tk ? `&token=${encodeURIComponent(tk)}` : ""}`, { headers: authHeaders(true) })
      .then((r) => { if (r.status === 403) setNeedKey(true); return r.json(); })
      .then((d) => (d.success ? setQueue(d) : setFlash(d.message_telugu || "⚠️ Admin key check cheyyandi (/admin lo key pettandi)")))
      .catch(() => { });
  }, []);

  useEffect(() => { loadQueue(status); }, [status, loadQueue]);

  const loadVendors = useCallback((st: string) => {
    const tk = adminToken();
    fetch(`/api/admin/vendors?status=${st}${tk ? `&token=${encodeURIComponent(tk)}` : ""}`, { headers: authHeaders(true) })
      .then((r) => { if (r.status === 403) setNeedKey(true); return r.json(); })
      .then((d) => (d.success ? setVQueue(d) : setFlash(d.message_telugu || "⚠️ Admin key check cheyyandi (/admin lo key pettandi)")))
      .catch(() => { });
    fetch(`/api/admin/vendors/revenue/summary${tk ? `?token=${encodeURIComponent(tk)}` : ""}`, { headers: authHeaders(true) })
      .then((r) => r.json()).then((d) => d.success && setVRevenue(d)).catch(() => { });
  }, []);

  useEffect(() => { if (tab === "vendors") loadVendors(vStatus); }, [tab, vStatus, loadVendors]);

  const actVendor = async (id: string, action: string, pkg?: string) => {
    const q = new URLSearchParams({ action });
    const tk = adminToken();
    if (tk) q.set("token", tk);
    if (action === "approve") {
      const v = (vUtr[id] || "").trim();
      if (!v) { setFlash("⚠️ Payment reference (UTR) ivvakunda vendor activate cheyyakoodadu — audit ki. Free/demo ki 'FREE' ani type cheyyandi"); return; }
      q.set("utr", v);
      if (pkg) q.set("package", pkg);
    } else if (action === "reject") {
      q.set("reason", "admin_reject: payment/details verify avvaledu");
    }
    const r = await fetch(`/api/admin/vendors/${id}/action?${q.toString()}`, { method: "POST", headers: authHeaders(true) });
    const d = await r.json();
    setFlash(d.message_telugu || d.reason || "done");
    loadVendors(vStatus);
  };
  useEffect(() => {
    fetch("/api/referral/leaderboard?period=all&limit=5").then((r) => r.json()).then((d) => setBoard(d.leaderboard || [])).catch(() => { });
    fetch("/api/leads/stats", { headers: authHeaders(true) })
      .then((r) => { if (r.status === 403) setNeedKey(true); return r.json(); })
      .then((d) => setStats((s: any) => ({ ...s, leads: d }))).catch(() => { });
    fetch("/api/channels").then((r) => r.json()).then((d) => setStats((s: any) => ({ ...s, channels: d.stats }))).catch(() => { });
  }, []);

  const act = async (id: string, action: string) => {
    const q = new URLSearchParams({ action });
    const tk = adminToken();
    if (tk) q.set("token", tk);
    if (action === "approve") {
      const v = (utr[id] || "").trim();
      if (!v) { setFlash("⚠️ UTR/reference number ivvakunda approve cheyyakoodadu (audit ki)"); return; }
      q.set("utr", v);
    } else {
      q.set("reason", "admin_reject: details verify avvaledu");
    }
    const r = await fetch(`/api/admin/payouts/${id}/action?${q.toString()}`, { method: "POST", headers: authHeaders(true) });
    const d = await r.json();
    setFlash(d.message_telugu || d.reason || "done");
    loadQueue(status);
  };

  const approveProfile = async (id: string) => {
    try {
      const r = await fetch(`/api/admin/approve/${id}`, { method: "POST", headers: authHeaders(true) });
      const d = await r.json();
      setProfiles((prev) => prev.map((p) => (p.id === id ? { ...p, status: "Approved" } : p)));
      setFlash(`✅ ${id} approve + auto-post queue: ${(d.auto_post_queue || []).slice(0, 3).join(", ")}`);
    } catch { setFlash("Approve fail ayyindi — API check cheyyandi"); }
  };

  const filtered = profiles.filter((p) => (p.id + (p.caste || "") + (p.district || "")).toLowerCase().includes(search.toLowerCase()));
  const rows = (queue.items || []).filter((p: any) => ((p.code || "") + (p.name || "") + (p.upi_id || "") + p.id).toLowerCase().includes(search.toLowerCase()));

  return (
    <main className="min-h-screen bg-[#FFF8E7] p-4">

      {/* 🔐 WAVE 9 — ADMIN KEY + ABUSE DASHBOARD */}
      <section className="mx-auto max-w-6xl px-4 pt-4">
        <div className="rounded-2xl border-2 border-[#7A0C2E]/25 bg-white p-4">
          <div className="flex flex-wrap items-end gap-2">
            <label className="flex-1 min-w-[240px] text-[12px] font-bold text-[#7A0C2E]">
              🔐 Admin key (X-Admin-Key) — leads / payouts / moderation / abuse ki kavali
              <input value={adminKey} onChange={(e) => setAdminKeyState(e.target.value)} type="password"
                placeholder="ADMIN_KEY env value (server log lo kooda untundi)"
                className="mt-1 w-full rounded-xl border border-[#7A0C2E]/30 px-3 py-2 font-mono text-[12px]" aria-label="ADMIN_KEY env value (server log lo kooda untundi)" />
            </label>
            <button onClick={saveAdminKey} className="rounded-xl bg-[#7A0C2E] px-4 py-2 text-[12px] font-bold text-white">💾 Save key</button>
            <button onClick={() => void loadAbuse()} className="rounded-xl border border-[#7A0C2E] px-4 py-2 text-[12px] font-bold text-[#7A0C2E]">🔄 Abuse refresh</button>
          </div>
          {needKey ? (
            <div className="mt-3">
              <AuthGate admin title="🔒 Admin key kavali"
                note="PII (leads phones) + money (payouts) endpoints ippudu key tho protect chesam. Server start lo '[HARDENING] admin_key=…' line lo key untundi — leda ADMIN_KEY env lo pettandi." />
            </div>
          ) : null}
          {abuse ? (
            <div className="mt-3 grid grid-cols-2 gap-2 text-[12px] sm:grid-cols-4 lg:grid-cols-6">
              <div className="rounded-xl bg-amber-50 p-2"><b>{abuse.rate_limited}</b><br />🚦 rate limited</div>
              <div className="rounded-xl bg-rose-50 p-2"><b>{abuse.auth_denied}</b><br />🔒 auth denied</div>
              <div className="rounded-xl bg-rose-50 p-2"><b>{abuse.admin_denied}</b><br />🛡️ admin denied</div>
              <div className="rounded-xl bg-sky-50 p-2"><b>{abuse.webhook_replay}</b><br />🔁 payment replay</div>
              <div className="rounded-xl bg-emerald-50 p-2"><b>{abuse.validation_errors}</b><br />🧹 bad inputs</div>
              <div className="rounded-xl bg-slate-50 p-2"><b>{abuse.consent_events}</b><br />📜 consents</div>
            </div>
          ) : null}
        </div>
      </section>
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">🔐 Admin Panel</div>
          <div className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Admin only</div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {[["payouts", duo("💰 Referral Payouts (live)", "💰 రెఫరల్ చెల్లింపులు")], ["vendors", duo("🏪 Vendor Ads (live)", "🏪 వెండర్ ప్రకటనలు")],
            ["matchsend", duo("🎯 Match & Send (₹500)", "🎯 మ్యాచ్ & సెండ")], ["astro", duo("🪐 Astro", "🪐 జ్యోతిషం")], ["ads", duo("📢 Ads", "📢 ప్రకటనలు")], ["pay", duo("💳 Payments", "💳 చెల్లింపులు")], ["offers", duo("🎉 Offers", "🎉 ఆఫర్లు")], ["content", duo("📝 Content (CMS)", "📝 కంటెంట్")], ["channels", duo("📡 Channels + Poster", "📡 ఛానళ్లు")], ["profiles", duo("👥 Profiles", "👥 ప్రొఫైళ్లు")], ["analytics", duo("📊 Analytics", "📊 విశ్లేషణ")]].map(([k, l]) => (
            <button key={k} onClick={() => setTab(k)}
              className={`px-5 py-2 rounded-full text-sm font-bold ${tab === k ? "maroon-gradient text-white" : "bg-white border"}`}>{l}</button>
          ))}
        </div>

        <div className="grid md:grid-cols-4 gap-3 mb-4">
          <div className="bg-white rounded-2xl p-4 shadow-sm text-center"><div className="text-2xl font-bold text-orange-600">{queue.count || 0}</div><div className="text-xs">Payout requests</div></div>
          <div className="bg-white rounded-2xl p-4 shadow-sm text-center"><div className="text-2xl font-bold text-[#7A0C2E]">₹{queue.total_amount || 0}</div><div className="text-xs">Pending amount</div></div>
          <div className="bg-white rounded-2xl p-4 shadow-sm text-center"><div className="text-2xl font-bold text-green-600">{stats.channels?.total || 0}</div><div className="text-xs">Channels ({stats.channels?.live || 0} live)</div></div>
          <div className="bg-white rounded-2xl p-4 shadow-sm text-center"><div className="text-2xl font-bold">{stats.leads?.total_leads ?? stats.leads?.total ?? 0}</div><div className="text-xs">Leads (visitors)</div></div>
        </div>

        {flash && <div className="mb-3 rounded-xl bg-[#0F1F3C] text-white text-xs p-3">{flash} <button onClick={() => setFlash("")} className="underline ml-2">close</button></div>}

        <div className="bg-white rounded-[1.5rem] p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h2 className="font-bold text-[#7A0C2E]">
              {tab === "payouts" ? duo("💰 Referral Payout Queue — approve with UTR (audit trail)", "💰 రెఫరల్ చెల్లింపులు — UTR తో ఆమోదం")
                : tab === "vendors" ? duo("🏪 Vendor Ads — approve (UTR) → listing live + promo post", "🏪 వెండర్ ప్రకటనలు — ఆమోదం → లైవ్")
                : tab === "profiles" ? duo("Profiles — Approve → auto-post", "ప్రొఫైళ్లు — ఆమోదం → ఆటో-పోస్ట్") : duo("Analytics", "విశ్లేషణ")}
            </h2>
            <div className="flex gap-2">
              {tab === "payouts" && (
                <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded-full border px-3 py-1.5 text-xs" aria-label="Select option">
                  <option value="requested">requested</option><option value="paid">paid</option>
                  <option value="rejected">rejected</option><option value="">anni</option>
                </select>
              )}
              {tab === "vendors" && (
                <select value={vStatus} onChange={(e) => setVStatus(e.target.value)} className="rounded-full border px-3 py-1.5 text-xs" aria-label="Select option">
                  <option value="pending">pending</option><option value="active">active</option>
                  <option value="expired">expired</option><option value="rejected">rejected</option><option value="">anni</option>
                </select>
              )}
              <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Code / Name / UPI / ID"
                className="px-4 py-2 rounded-full bg-gray-50 border text-xs" aria-label="Code / Name / UPI / ID" />
            </div>
          </div>

          {/* ---------------- MATCH & SEND (₹500 assisted) ---------------- */}
          {tab === "matchsend" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">🎯 Match &amp; Send — buyer ID → perfect matches → personal Telegram/WhatsApp</h2>
              <MatchSend />
            </>
          )}

          {/* ---------------- ASTRO ---------------- */}
          {tab === "astro" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">🪐 Astrology — 36-guna + dosha + jathakam verify</h2>
              <AstroConsole />
            </>
          )}

          {/* ---------------- ADS ---------------- */}
          {tab === "ads" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">📢 Ad campaigns — approve → district/state LIVE</h2>
              <AdsConsole />
            </>
          )}

          {/* ---------------- PAYMENTS ---------------- */}
          {tab === "pay" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">💳 Safe-Pay orders — Razorpay auto / UPI-UTR confirm</h2>
              <PayConsole />
            </>
          )}

          {/* ---------------- OFFERS ---------------- */}
          {tab === "offers" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">🎉 Festival offers — codes + dates + caps</h2>
              <OffersConsole />
            </>
          )}

          {/* ---------------- CONTENT (CMS) ---------------- */}
          {tab === "content" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">📝 Content — pages + stories + banners (code vaddu)</h2>
              <ContentConsole />
            </>
          )}

          {/* ---------------- CHANNELS + POSTER ---------------- */}
          {tab === "channels" && (
            <>
              <h2 className="font-bold text-[#7A0C2E] mt-2">📡 Channels — links map + bulk import + smart poster</h2>
              <ChannelsConsole />
            </>
          )}

          {/* ---------------- PAYOUTS ---------------- */}
          {tab === "payouts" && (
            <>
              <p className="text-xs text-gray-500 mt-2 telugu">
                ₹50 per paying referral (first payment) + 10% repeat + tier extra. UPI copy → PhonePe deep link → pay → UTR pettandi → approve.
                Reject chesthe wallet ki malli credit avutundi (automatic).
              </p>
              <div className="mt-4 overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="text-xs text-gray-500 border-b">
                    <th className="text-left p-2">Request</th><th>Referrer</th><th>UPI / Bank</th>
                    <th>Amount</th><th>UTR / Action</th>
                  </tr></thead>
                  <tbody>
                    {rows.length === 0 && <tr><td colSpan={5} className="p-4 text-center text-xs text-gray-500">Ee status lo requests levu 🙂</td></tr>}
                    {rows.map((p: any) => (
                      <tr key={p.id} className="border-b">
                        <td className="p-2 text-xs">
                          <div className="font-bold">{p.id}</div>
                          <div className="text-[10px] text-gray-500">{p.requested_at?.slice(0, 16).replace("T", " ")}</div>
                          <div className={`mt-1 inline-block px-2 py-0.5 rounded-full text-[10px] ${p.status === "paid" ? "bg-green-100 text-green-700" : p.status === "rejected" ? "bg-red-100 text-red-700" : "bg-orange-100 text-orange-700"}`}>{p.status}{p.utr ? ` · ${p.utr}` : ""}</div>
                        </td>
                        <td className="p-2 text-xs">
                          <div className="font-bold">{p.name}</div>
                          <div className="text-[11px] text-gray-500">{p.code} • {p.tier}</div>
                          <div className="text-[10px] text-gray-400">{p.tsap_id}</div>
                        </td>
                        <td className="p-2 text-xs">
                          {p.method === "upi" ? <div className="font-bold">📱 {p.upi_id}</div>
                            : <div className="font-bold">🏦 {p.bank?.holder}<br />{p.bank?.account_no} · {p.bank?.ifsc}</div>}
                          <button onClick={() => navigator.clipboard?.writeText(p.upi_id || p.bank?.account_no || "")}
                            className="mt-1 px-2 py-0.5 bg-gray-100 rounded-full text-[10px]">📋 copy</button>
                        </td>
                        <td className="p-2 text-center font-bold text-[#7A0C2E]">₹{p.amount}</td>
                        <td className="p-2">
                          {p.status === "requested" ? (
                            <div className="flex flex-col gap-1">
                              <input value={utr[p.id] || ""} onChange={(e) => setUtr({ ...utr, [p.id]: e.target.value })}
                                placeholder="UTR / ref no" className="rounded-lg border px-2 py-1 text-xs w-36" aria-label="UTR / ref no" />
                              <div className="flex gap-1">
                                <button onClick={() => act(p.id, "approve")} className="px-3 py-1 bg-green-600 text-white rounded-full text-xs">✅ Paid</button>
                                <button onClick={() => act(p.id, "reject")} className="px-3 py-1 bg-red-500 text-white rounded-full text-xs">❌ Reject</button>
                                {p.method === "upi" && (
                                  <a href={`phonepe://pay?pa=${p.upi_id}&pn=${encodeURIComponent(p.name)}&am=${p.amount}&tn=Manavivaha Referral ${p.code}`}
                                    className="px-3 py-1 bg-[#6739B7] text-white rounded-full text-center text-xs">📱 PhonePe</a>
                                )}
                              </div>
                            </div>
                          ) : (
                            <div className="text-[11px] text-gray-500">{p.paid_at ? `paid ${p.paid_at.slice(0, 16).replace("T", " ")}` : p.reason}</div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="mt-4 rounded-xl bg-[#0F1F3C] text-white text-xs p-4">
                <div className="font-bold text-[#D4AF37]">💡 Payout process (manual — 10 sec)</div>
                <div className="mt-1 space-y-0.5 opacity-90">
                  <div>1. Copy UPI → 2. PhonePe deep link (amount auto) → 3. Send → 4. UTR paste → 5. ✅ Paid</div>
                  <div>Reject ayithe → referrer wallet ki auto-credit + message veltundi. Anni entries ledger lo (audit) untayi.</div>
                </div>
              </div>
            </>
          )}

          {/* ---------------- VENDOR ADS ---------------- */}
          {tab === "vendors" && (
            <>
              <p className="text-xs text-gray-500 mt-2 telugu">
                Vendor signup (catering/photography/decorations/hall/pandit...) → payment verify → <b>activate</b> chesthe
                listing + Telugu promo post + poster ready. Enquiries direct vendor WhatsApp ki veltayi.
              </p>
              {vRevenue && (
                <div className="mt-3 grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
                  {[
                    { l: "Active vendors", v: vRevenue.active, c: "text-green-600" },
                    { l: "Pending", v: vRevenue.pending, c: "text-orange-600" },
                    { l: "Collected (₹)", v: vRevenue.collected, c: "text-[#7A0C2E]" },
                    { l: "MRR (₹)", v: vRevenue.mrr, c: "text-[#7A0C2E]" },
                    { l: "Leads (total)", v: vRevenue.leads_total, c: "text-[#0F1F3C]" },
                  ].map((x) => (
                    <div key={x.l} className="bg-gray-50 rounded-2xl p-3">
                      <div className={`text-xl font-bold ${x.c}`}>{x.v}</div>
                      <div className="text-[11px] text-gray-500">{x.l}</div>
                    </div>
                  ))}
                </div>
              )}
              {vRevenue?.renewals_due?.length > 0 && (
                <div className="mt-3 rounded-xl bg-[#FFF8E7] border border-[#D4AF37]/50 p-3 text-xs text-[#7A0C2E]">
                  ⏳ <b>{vRevenue.renewals_due.length}</b> listings ee వారంలో expire avutunnayi — renewal call cheyyandi:
                  {" "}{vRevenue.renewals_due.map((r: any) => r.name).join(", ")}
                </div>
              )}
              <div className="mt-4 overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="text-xs text-gray-500 border-b">
                    <th className="text-left p-2">Vendor</th><th>Category</th><th>Contact</th>
                    <th>Package</th><th>UTR / Action</th>
                  </tr></thead>
                  <tbody>
                    {(vQueue.items || []).length === 0 && (
                      <tr><td colSpan={5} className="p-4 text-center text-xs text-gray-500">Ee status lo vendor requests levu 🙂</td></tr>
                    )}
                    {(vQueue.items || []).map((v: any) => (
                      <tr key={v.id} className="border-b align-top">
                        <td className="p-2 text-xs">
                          <div className="font-bold">{v.icon} {v.business_name}</div>
                          <div className="text-[10px] text-gray-500">{v.id} • {v.city}{v.district ? `, ${v.district}` : ""}</div>
                          <div className={`mt-1 inline-block px-2 py-0.5 rounded-full text-[10px] ${v.status === "active" ? "bg-green-100 text-green-700" : v.status === "rejected" ? "bg-red-100 text-red-700" : v.status === "expired" ? "bg-gray-200 text-gray-700" : "bg-orange-100 text-orange-700"}`}>
                            {v.status}{v.expires_at ? ` → ${v.expires_at.slice(0, 10)}` : ""}
                          </div>
                          {v.about && <div className="text-[10px] text-gray-500 mt-1 max-w-[220px] line-clamp-2">{v.about}</div>}
                        </td>
                        <td className="p-2 text-xs">{v.category_te || v.category}<div className="text-[10px] text-gray-500">{v.price_range}</div></td>
                        <td className="p-2 text-xs">
                          <a href={`https://wa.me/91${v.whatsapp || v.phone}`} target="_blank" rel="noreferrer" className="font-bold text-green-700 underline">📞 {v.phone}</a>
                          <div className="text-[10px] text-gray-500">owner: {v.owner_name || "-"} • {v.experience_years || "-"} yrs</div>
                        </td>
                        <td className="p-2 text-xs">
                          <div className="font-bold text-[#7A0C2E]">₹{v.package_price} <span className="text-[10px] text-gray-500">/ {v.package_days}d</span></div>
                          <div className="text-[10px] text-gray-500">{v.package}</div>
                        </td>
                        <td className="p-2">
                          {v.status === "pending" ? (
                            <div className="flex flex-col gap-1">
                              <input value={vUtr[v.id] || ""} onChange={(e) => setVUtr({ ...vUtr, [v.id]: e.target.value })}
                                placeholder="UTR / payment ref" className="rounded-lg border px-2 py-1 text-xs w-36" aria-label="UTR / payment ref" />
                              <div className="flex flex-wrap gap-1">
                                <button onClick={() => actVendor(v.id, "approve", v.package)} className="px-3 py-1 bg-green-600 text-white rounded-full text-xs">✅ Activate</button>
                                <button onClick={() => actVendor(v.id, "reject")} className="px-3 py-1 bg-red-500 text-white rounded-full text-xs">❌ Reject</button>
                                {v.whatsapp_link && (
                                  <a href={v.whatsapp_link} target="_blank" rel="noreferrer" className="px-3 py-1 bg-[#6739B7] text-white rounded-full text-xs">💬 WA</a>
                                )}
                              </div>
                            </div>
                          ) : (
                            <div className="flex flex-wrap gap-1">
                              {v.status === "active" && (
                                <button onClick={() => actVendor(v.id, "expire")} className="px-3 py-1 bg-gray-200 rounded-full text-xs">⏳ Expire</button>
                              )}
                              {v.status !== "active" && (
                                <button onClick={() => actVendor(v.id, "approve", v.package)} className="px-3 py-1 bg-green-600 text-white rounded-full text-xs">♻️ Reactivate</button>
                              )}
                              <a href={`/vendors/${v.id}`} className="px-3 py-1 bg-gray-100 rounded-full text-xs">👁️ view</a>
                              <a href={`/api/vendors/${v.id}/poster.png`} download className="px-3 py-1 bg-gray-100 rounded-full text-xs">⬇️ poster</a>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="mt-4 rounded-xl bg-[#0F1F3C] text-white text-xs p-4">
                <div className="font-bold text-[#D4AF37]">🏪 Vendor process (30 sec)</div>
                <div className="mt-1 space-y-0.5 opacity-90">
                  <div>1. Payment vachhinda check (UPI/phone) → 2. UTR paste → 3. ✅ Activate → 4. Listing + promo post live (+ poster download)</div>
                  <div>Enquiries anni vendor WhatsApp ki auto-veltayi (lead text lo number, budget, event date untundi).</div>
                </div>
              </div>
            </>
          )}

          {/* ---------------- PROFILES ---------------- */}
          {tab === "profiles" && (
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="text-xs text-gray-500 border-b">
                  <th className="text-left p-2">ID</th><th>Details</th><th>Credits</th><th>Status</th><th>Actions</th>
                </tr></thead>
                <tbody>
                  {filtered.map((p) => (
                    <tr key={p.id} className="border-b">
                      <td className="p-2 font-bold">{p.id}</td>
                      <td className="p-2 text-xs">{p.gender} • {p.age}y • {p.caste} • {p.district} ({p.state})</td>
                      <td className="p-2 text-center">{p.credits ?? 3}</td>
                      <td className="p-2"><span className={`px-2 py-1 rounded-full text-xs ${p.status === "Approved" ? "bg-green-100 text-green-700" : "bg-orange-100 text-orange-700"}`}>{p.status}</span></td>
                      <td className="p-2">
                        <button onClick={() => approveProfile(p.id)} className="px-3 py-1 bg-green-600 text-white rounded-full text-xs">✅ Approve → channels</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* ---------------- ANALYTICS ---------------- */}
          {tab === "analytics" && (
            <div className="mt-4 grid md:grid-cols-2 gap-4 text-xs">
              <div className="rounded-2xl border p-4">
                <div className="font-bold text-[#7A0C2E]">🏆 Top referrers (live)</div>
                <div className="mt-2 space-y-1">
                  {board.length === 0 && <div className="text-gray-500">Data ledu — referrers start cheyyandi</div>}
                  {board.map((b) => (
                    <div key={b.code} className="flex justify-between bg-gray-50 rounded-lg px-3 py-2">
                      <span>{b.rank}. {b.name} ({b.code})</span>
                      <span className="font-bold text-green-600">₹{b.earned} · {b.paid} paid</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-2xl border p-4">
                <div className="font-bold text-[#7A0C2E]">📢 Channels</div>
                <div className="mt-2 space-y-1">
                  <div>Total: <b>{stats.channels?.total ?? "—"}</b> • Live: <b>{stats.channels?.live ?? "—"}</b> • To create: <b>{stats.channels?.to_create ?? "—"}</b></div>
                  {stats.channels?.by_tier && Object.entries(stats.channels.by_tier).map(([k, v]) => (
                    <div key={k} className="flex justify-between bg-gray-50 rounded-lg px-3 py-1.5"><span>{k}</span><span className="font-bold">{String(v)}</span></div>
                  ))}
                </div>
                <Link href="/channels" className="mt-2 inline-block underline font-bold text-[#7A0C2E]">Channel setup →</Link>
              </div>
              <div className="rounded-2xl border p-4">
                <div className="font-bold text-[#7A0C2E]">📈 Leads / visitors</div>
                <div className="mt-2 space-y-1">
                  {stats.leads ? Object.entries(stats.leads).slice(0, 6).map(([k, v]) => (
                    <div key={k} className="flex justify-between bg-gray-50 rounded-lg px-3 py-1.5"><span>{k}</span><span className="font-bold">{typeof v === "object" ? JSON.stringify(v).slice(0, 40) : String(v)}</span></div>
                  )) : <div className="text-gray-500">Loading…</div>}
                </div>
              </div>
              <div className="rounded-2xl border p-4">
                <div className="font-bold text-[#7A0C2E]">🩺 System health</div>
                <a href="/api/system/health" target="_blank" rel="noreferrer" className="mt-2 block underline font-bold text-[#7A0C2E]">/api/system/health →</a>
                <a href="/api/wa/status" target="_blank" rel="noreferrer" className="mt-1 block underline font-bold text-[#7A0C2E]">/api/wa/status →</a>
                <a href="/api/referral/leaderboard?period=week" target="_blank" rel="noreferrer" className="mt-1 block underline font-bold text-[#7A0C2E]">/api/referral/leaderboard?period=week →</a>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
