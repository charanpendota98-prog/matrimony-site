"use client";
/**
 * 🗓️ DAILY MATCHES CONSOLE (WAVE 40)
 * ===================================
 * "Matches of the Day" — admin selects profiles → set as today's featured
 * + re-post to their caste channels (boost). ⚡ Boost-active (paid) users first.
 */
import { useEffect, useMemo, useState } from "react";
import { authHeaders } from "@/lib/api";
import { useLang } from "@/lib/lang";

type Row = Record<string, any>;

const adminToken = () => {
  try { return localStorage.getItem("tsap_admin_token") || ""; } catch { return ""; }
};
const withToken = (url: string) => {
  const tk = adminToken();
  return tk ? `${url}${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(tk)}` : url;
};

export default function DailyMatches() {
  const { lang } = useLang();
  const te = lang === "te";
  const [rows, setRows] = useState<Row[]>([]);
  const [today, setToday] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [flash, setFlash] = useState("");
  const [sel, setSel] = useState<Record<string, boolean>>({});
  const [q, setQ] = useState("");
  const [res, setRes] = useState<Row | null>(null);

  const load = async () => {
    setLoading(true); setFlash("");
    try {
      const r = await fetch(withToken("/api/admin/daily-matches/candidates?limit=100"), { headers: authHeaders(true) });
      const d = await r.json();
      if (d.success) {
        setRows(d.candidates || []);
        setToday(d.today || []);
        setFlash(te ? `✅ ${d.count} candidates · ⚡ ${d.boosted_count} boost active (paid)` : `✅ ${d.count} candidates · ⚡ ${d.boosted_count} boost active (paid)`);
      } else setFlash(d.detail || "load fail");
    } catch { setFlash(te ? "⚠️ API error" : "⚠️ API error"); }
    finally { setLoading(false); }
  };
  useEffect(() => { void load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const filtered = useMemo(() => {
    if (!q) return rows;
    const s = q.toLowerCase();
    return rows.filter((x) => `${x.tsap_id} ${x.full_name} ${x.caste} ${x.district}`.toLowerCase().includes(s));
  }, [rows, q]);

  const selIds = Object.keys(sel).filter((k) => sel[k]);
  const toggle = (id: string) => setSel((s) => ({ ...s, [id]: !s[id] }));
  const selectAll = (on: boolean) => {
    const o: Record<string, boolean> = {};
    filtered.forEach((x) => { o[x.tsap_id] = on; });
    setSel(o);
  };

  const apply = async (post: boolean) => {
    if (!selIds.length) { setFlash(te ? "⚠️ Profiles select చెయ్యండి (☑️)" : "⚠️ Select profiles (☑️)"); return; }
    setFlash(te ? "⏳ Setting + posting…" : "⏳ Setting + posting…");
    try {
      const r = await fetch(withToken("/api/admin/daily-matches"), {
        method: "POST", headers: { ...authHeaders(true), "Content-Type": "application/json" },
        body: JSON.stringify({ profile_ids: selIds, post_to_channels: post }),
      });
      const d = await r.json();
      if (d.success) {
        setRes(d); setToday(d.selected || []);
        setFlash(d.message_telugu || `✅ ${d.selected?.length} set · ${d.posted?.length} posted`);
      } else setFlash(d.detail || "fail");
    } catch { setFlash(te ? "⚠️ API error" : "⚠️ API error"); }
  };

  return (
    <div>
      <p className="telugu mt-2 text-xs text-gray-500">
        {te ? <>ఈ రోజు <b>Matches of the Day</b> — select చేసిన profiles home page లో featured గా + వారి caste channels లో మళ్లీ post (⚡ boost). Boost కొన్నవాళ్లు (paid) ముందు కనిపిస్తారు — అదే revenue.</> : <>Today&apos;s <b>Matches of the Day</b> — selected profiles featured on home + re-posted to their caste channels (boost). Paid boost users listed first.</>}
      </p>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={te ? "వెతకండి: ID / name / caste…" : "Search: ID / name / caste…"}
          aria-label="Search candidates" className="min-w-[220px] flex-1 rounded-xl border border-[#7A0C2E]/30 px-3 py-2 text-sm" />
        <button onClick={() => void load()} disabled={loading} className="rounded-xl border border-[#7A0C2E] px-4 py-2 text-xs font-bold text-[#7A0C2E]">🔄 {te ? "రిఫ్రెష్" : "Refresh"}</button>
      </div>

      {today.length > 0 && (
        <div className="mt-2 rounded-xl bg-emerald-50 border border-emerald-200 p-2 text-xs">
          🗓️ {te ? "ఈ రోజు ఎంపిక" : "Today's picks"}: <b>{today.join(", ")}</b>
        </div>
      )}
      {flash ? <div className="mt-2 rounded-xl bg-[#0F1F3C] p-3 text-xs text-white">{flash}</div> : null}

      <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
        <b className="text-[#7A0C2E]">{filtered.length} candidates</b>
        <button onClick={() => selectAll(true)} className="rounded-full bg-gray-200 px-3 py-1">{te ? "☑️ అన్నీ select" : "☑️ select all"}</button>
        <button onClick={() => selectAll(false)} className="rounded-full bg-gray-200 px-3 py-1">⬜ clear</button>
        <b>Selected: {selIds.length}</b>
      </div>

      <div className="mt-2 max-h-[380px] overflow-auto rounded-2xl border">
        <table className="w-full text-xs">
          <thead className="sticky top-0 bg-[#FFF8E7]">
            <tr className="text-left text-gray-500"><th className="p-2">☑️</th><th>Profile</th><th>Details</th><th>⚡</th></tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={4} className="p-4 text-center text-gray-500">{te ? "Profiles లేవు" : "No profiles"}</td></tr>
            ) : filtered.map((x) => (
              <tr key={x.tsap_id} className={`border-t ${sel[x.tsap_id] ? "bg-emerald-50" : ""} ${today.includes(x.tsap_id) ? "bg-amber-50" : ""}`}>
                <td className="p-2 text-center"><input type="checkbox" checked={!!sel[x.tsap_id]} onChange={() => toggle(x.tsap_id)} aria-label={`Select ${x.tsap_id}`} className="h-4 w-4 accent-[#7A0C2E]" /></td>
                <td className="p-2">
                  <div className="font-bold">{x.full_name}</div>
                  <div className="font-mono text-[10px] text-gray-500">{x.tsap_id}</div>
                </td>
                <td className="p-2">
                  {x.gender === "Bride" ? "👰" : "🤵"} {x.age}y · {x.caste} · {x.district}
                  <div className="text-[10px] text-gray-500">{x.job} · {x.marital_status || ""}</div>
                </td>
                <td className="p-2">{x.boost_active ? <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-700">⚡ PAID</span> : ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        <button onClick={() => void apply(true)} className="rounded-xl bg-[#7A0C2E] px-5 py-2.5 text-sm font-bold text-white">
          🗓️ {te ? "ఈ రోజు matches గా set + channels లో post" : "Set as today + post to channels"}
        </button>
        <button onClick={() => void apply(false)} className="rounded-xl border border-[#7A0C2E] px-4 py-2.5 text-xs font-bold text-[#7A0C2E]">
          {te ? "channels లో post చేయకుండా set మాత్రమే" : "Set only (no posting)"}
        </button>
      </div>

      {res ? (
        <div className="mt-2 rounded-xl bg-gray-50 p-3 text-xs">
          ✅ {te ? "సెట్ చేయబడ్డాయి" : "Set"}: <b>{(res.selected || []).length}</b> · 📢 {te ? "పోస్ట్ అయ్యాయి" : "posted"}: <b>{(res.posted || []).length}</b>
          {(res.failed || []).length > 0 && <span className="text-red-600"> · ⚠️ {(res.failed || []).length} failed</span>}
        </div>
      ) : null}
    </div>
  );
}
