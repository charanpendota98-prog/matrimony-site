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
import Link from "next/link";

const DEMO_PROFILES = [
  { id: "TSAP-F-2025-1042", gender: "Bride", age: 24, caste: "Reddy", district: "Nalgonda", state: "TS", phone: "98480xxxxx", status: "Pending", credits: 3 },
  { id: "TSAP-M-2025-1042", gender: "Groom", age: 27, caste: "Kamma", district: "Guntur", state: "AP", phone: "98481xxxxx", status: "Approved", credits: 5 },
];

export default function AdminPage() {
  const [tab, setTab] = useState("payouts");
  const [profiles, setProfiles] = useState<any[]>([]);
  const [queue, setQueue] = useState<any>({ items: [], count: 0, total_amount: 0 });
  const [utr, setUtr] = useState<Record<string, string>>({});
  const [status, setStatus] = useState("requested");
  const [search, setSearch] = useState("");
  const [flash, setFlash] = useState("");
  const [board, setBoard] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({});

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
    fetch(`/api/admin/payouts?status=${st}${tk ? `&token=${encodeURIComponent(tk)}` : ""}`)
      .then((r) => r.json())
      .then((d) => (d.success ? setQueue(d) : setFlash(d.message_telugu || "⚠️ Admin token check cheyyandi")))
      .catch(() => { });
  }, []);

  useEffect(() => { loadQueue(status); }, [status, loadQueue]);
  useEffect(() => {
    fetch("/api/referral/leaderboard?period=all&limit=5").then((r) => r.json()).then((d) => setBoard(d.leaderboard || [])).catch(() => { });
    fetch("/api/leads/stats").then((r) => r.json()).then((d) => setStats((s: any) => ({ ...s, leads: d }))).catch(() => { });
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
    const r = await fetch(`/api/admin/payouts/${id}/action?${q.toString()}`, { method: "POST" });
    const d = await r.json();
    setFlash(d.message_telugu || d.reason || "done");
    loadQueue(status);
  };

  const approveProfile = async (id: string) => {
    try {
      const r = await fetch(`/api/admin/approve/${id}`, { method: "POST" });
      const d = await r.json();
      setProfiles((prev) => prev.map((p) => (p.id === id ? { ...p, status: "Approved" } : p)));
      setFlash(`✅ ${id} approve + auto-post queue: ${(d.auto_post_queue || []).slice(0, 3).join(", ")}`);
    } catch { setFlash("Approve fail ayyindi — API check cheyyandi"); }
  };

  const filtered = profiles.filter((p) => (p.id + (p.caste || "") + (p.district || "")).toLowerCase().includes(search.toLowerCase()));
  const rows = (queue.items || []).filter((p: any) => ((p.code || "") + (p.name || "") + (p.upi_id || "") + p.id).toLowerCase().includes(search.toLowerCase()));

  return (
    <main className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">🔐 Admin Panel</div>
          <div className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Admin only</div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {[["payouts", "💰 Referral Payouts (live)"], ["profiles", "👥 Profiles"], ["analytics", "📊 Analytics"]].map(([k, l]) => (
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
              {tab === "payouts" ? "💰 Referral Payout Queue — UTR tho approve (audit trail)" : tab === "profiles" ? "Profiles — Approve → auto-post" : "Analytics"}
            </h2>
            <div className="flex gap-2">
              {tab === "payouts" && (
                <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded-full border px-3 py-1.5 text-xs">
                  <option value="requested">requested</option><option value="paid">paid</option>
                  <option value="rejected">rejected</option><option value="">anni</option>
                </select>
              )}
              <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Code / Name / UPI / ID"
                className="px-4 py-2 rounded-full bg-gray-50 border text-xs" />
            </div>
          </div>

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
                                placeholder="UTR / ref no" className="rounded-lg border px-2 py-1 text-xs w-36" />
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
