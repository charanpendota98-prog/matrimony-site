"use client";

/**
 * MANA VIVAHA — ADVANCED MATCHES (v3)
 * ===================================
 * Real backend /api/search tho wire ayyindi (mundu client-side demo filter matrame).
 *  • 13 filters: gender, age range (slider), caste, district, state, job, education,
 *    salary_min, marital, religion, verified only, photo only, keyword
 *  • 5 sorts: Best match (score) / New / Age / Porutham 10/10 / Boosted
 *  • Why-match reasons + 10-porutham badge per card (viewer tho compare chesi)
 *  • Active filter chips (✕ remove) + saved searches (🔔 local) + share-search link
 *  • Phone lo: bottom-sheet filters, thumb buttons, sticky search
 *  • API fail aithe demo data fallback (site eppudu khali ga kanipinchadu)
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { CASTES, DISTRICTS_BY_STATE, EDUCATIONS, JOBS, MARITAL_STATUSES, RELIGIONS, SALARIES } from "@/lib/telugu-data";
import { SITE_CONFIG } from "@/lib/site-config";
import QuickLead from "@/components/QuickLead";

type Row = Record<string, any>;
const SAVED_SEARCHES_KEY = "tsap_saved_searches_v1";
const SORTS = [
  { v: "score", l: "🏆 Best match" },
  { v: "porutham", l: "💍 Porutham (10)" },
  { v: "new", l: "🆕 New" },
  { v: "age", l: "🎂 Age" },
  { v: "boosted", l: "⚡ Boosted" },
];
const DEFAULT_FILTERS: Row = {
  gender: "", q: "", caste: "", district: "", state: "", job: "", education: "",
  salary_min: 0, marital_status: "", religion: "", age_min: 18, age_max: 60,
  verified_only: false, photo_only: false,
};

/* demo fallback — API fail aithe ee rows chupistham (site khali ga kanipinchadu) */
const FALLBACK: Row[] = [
  { tsap_id: "TSAP-F-2025-1042", full_name: "Lakshmi Reddy", age: 24, gender: "Bride", caste: "Reddy", sub_caste: "Pakanati", education: "BTech", education_detail: "CSE", job: "Software Engineer", company: "TCS", salary: "8L", height: "5'4\"", district: "Hyderabad", state: "TS", gothram: "Bharadwaj", star: "Rohini", rasi: "Vrishabha", marital_status: "Pelli Kaledu", phone_verified: true, has_photo: false, boosted: false, score: 92, reasons: ["Hyderabad + Software perfect", "Reddy same caste — channels lo reach ekkuva", "Age gap ideal", "Family values matching"], porutham: { score: 8, max: 10, verdict: "Uttama porutham" } },
  { tsap_id: "TSAP-F-2025-2042", full_name: "Sravani Chowdary", age: 26, gender: "Bride", caste: "Kamma", education: "MSc", job: "Data Analyst", company: "Deloitte", salary: "10L", height: "5'5\"", district: "Vijayawada", state: "AP", gothram: "Kasyapa", star: "Ashwini", marital_status: "Pelli Kaledu", phone_verified: true, has_photo: false, score: 84, reasons: ["AP + Kamma same region", "Education MSc match", "Salary range matching"], porutham: { score: 7, max: 10, verdict: "Manchi porutham" } },
  { tsap_id: "TSAP-F-2025-3042", full_name: "Meghana Vysya", age: 25, gender: "Bride", caste: "Vysya", education: "BPharm", job: "Pharmacist", company: "MedPlus", salary: "4.5L", height: "5'3\"", district: "Hyderabad", state: "TS", gothram: "Kaushika", star: "Chitra", marital_status: "Pelli Kaledu", phone_verified: true, has_photo: false, score: 78, reasons: ["Hyderabad same city", "Healthcare field stable", "Age perfect"], porutham: { score: 7, max: 10, verdict: "Manchi porutham" } },
];

function FilterSheet({
  open, onClose, filters, setF, reset, onApply, resultsInfo,
}: {
  open: boolean; onClose: () => void; filters: Row; setF: (k: string, v: any) => void;
  reset: () => void; onApply: () => void; resultsInfo: string;
}) {
  const districts: string[] = filters.state ? (DISTRICTS_BY_STATE[filters.state] || []) : [];
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center">
      <div className="absolute inset-0 bg-black/45" onClick={onClose} />
      <div className="relative w-full md:max-w-2xl max-h-[88vh] overflow-y-auto bg-cream rounded-t-[2rem] md:rounded-[2rem] p-4 step-slide">
        <div className="flex items-center justify-between sticky top-0 bg-cream pb-2 -mt-1 pt-1">
          <div className="font-bold text-maroon text-[16px]">🔎 Advanced filters</div>
          <button onClick={onClose} className="w-10 h-10 rounded-full bg-white border border-gold/40 font-bold">✕</button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-[13px] font-bold text-ink">Evarini chusthunnaru?</label>
            <div className="mt-2 flex gap-2">
              {[{ v: "", l: "Andaru" }, { v: "Bride", l: "👰 Brides" }, { v: "Groom", l: "🤵 Grooms" }].map((g) => (
                <button key={g.v} onClick={() => setF("gender", g.v)}
                  className={`chip ${filters.gender === g.v ? "chip-on" : ""}`}>{g.l}</button>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-gold/30 p-3">
            <div className="flex items-center justify-between text-[13px] font-bold text-ink">
              <span>Age range</span><span className="text-maroon">{filters.age_min} – {filters.age_max} yrs</span>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              <input type="range" min={18} max={60} value={filters.age_min}
                onChange={(e) => setF("age_min", Math.min(parseInt(e.target.value), filters.age_max))} className="accent-[#7A0C2E]" />
              <input type="range" min={18} max={60} value={filters.age_max}
                onChange={(e) => setF("age_max", Math.max(parseInt(e.target.value), filters.age_min))} className="accent-[#7A0C2E]" />
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">State</label>
            <div className="mt-2 flex flex-wrap gap-2">
              {[{ v: "", l: "Anni" }, { v: "TS", l: "Telangana" }, { v: "AP", l: "Andhra Pradesh" }, { v: "Other", l: "Other states" }].map((s) => (
                <button key={s.v} onClick={() => { setF("state", s.v); setF("district", ""); }}
                  className={`chip ${filters.state === s.v ? "chip-on" : ""}`}>{s.l}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">District {filters.state ? "" : "(state select cheyyandi)"}</label>
            <div className="mt-2 flex flex-wrap gap-2 max-h-44 overflow-y-auto">
              {districts.map((d) => (
                <button key={d} onClick={() => setF("district", filters.district === d ? "" : d)}
                  className={`chip ${filters.district === d ? "chip-on" : ""}`}>{d}</button>
              ))}
              {!districts.length && <span className="text-[12px] text-gray-500">State select cheyyandi — districts vasthayi</span>}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Caste ({CASTES.length} options)</label>
            <div className="mt-2 flex flex-wrap gap-2 max-h-48 overflow-y-auto">
              {CASTES.map((c) => (
                <button key={c} onClick={() => setF("caste", filters.caste === c ? "" : c)}
                  className={`chip ${filters.caste === c ? "chip-on" : ""}`}>{c}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Job</label>
            <div className="mt-2 flex flex-wrap gap-2 max-h-40 overflow-y-auto">
              {JOBS.slice(0, 24).map((j) => (
                <button key={j} onClick={() => setF("job", filters.job === j ? "" : j)}
                  className={`chip ${filters.job === j ? "chip-on" : ""}`}>{j}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Education</label>
            <div className="mt-2 flex flex-wrap gap-2 max-h-40 overflow-y-auto">
              {EDUCATIONS.slice(0, 24).map((e) => (
                <button key={e} onClick={() => setF("education", filters.education === e ? "" : e)}
                  className={`chip ${filters.education === e ? "chip-on" : ""}`}>{e}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Salary (min)</label>
            <div className="mt-2 flex flex-wrap gap-2">
              {[{ v: 0, l: "Any" }].concat(SALARIES.map((s) => ({ v: Number(String(s).replace(/[^\d]/g, "").slice(0, 2)) * 100000, l: s }))).slice(0, 10).map((s) => (
                <button key={String(s.v)} onClick={() => setF("salary_min", s.v)}
                  className={`chip ${filters.salary_min === s.v ? "chip-on" : ""}`}>{s.l}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Marital status</label>
            <div className="mt-2 flex flex-wrap gap-2">
              {MARITAL_STATUSES.map((m) => (
                <button key={m} onClick={() => setF("marital_status", filters.marital_status === m ? "" : m)}
                  className={`chip ${filters.marital_status === m ? "chip-on" : ""}`}>{m}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[13px] font-bold text-ink">Religion</label>
            <div className="mt-2 flex flex-wrap gap-2">
              {RELIGIONS.map((r) => (
                <button key={r} onClick={() => setF("religion", filters.religion === r ? "" : r)}
                  className={`chip ${filters.religion === r ? "chip-on" : ""}`}>{r}</button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <button onClick={() => setF("verified_only", !filters.verified_only)}
              className={`chip justify-center ${filters.verified_only ? "chip-on" : ""}`}>✅ Verified only</button>
            <button onClick={() => setF("photo_only", !filters.photo_only)}
              className={`chip justify-center ${filters.photo_only ? "chip-on" : ""}`}>📸 Photo unnavi</button>
          </div>
        </div>

        <div className="sticky bottom-0 bg-cream pt-3 pb-1 safe-bottom">
          <div className="text-[11px] text-gray-600 mb-2">{resultsInfo}</div>
          <div className="flex gap-2">
            <button onClick={reset} className="px-5 py-3 rounded-2xl border border-maroon/25 text-maroon font-bold text-[14px]">Reset</button>
            <button onClick={onApply} className="flex-1 py-3 rounded-2xl maroon-gradient text-white font-bold text-[15px]">
              {resultsInfo.includes("—") ? "Results chudu" : "Apply chey"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function MatchesAdvanced() {
  const [filters, setFilters] = useState<Row>({ ...DEFAULT_FILTERS });
  const [sort, setSort] = useState("score");
  const [rows, setRows] = useState<Row[]>([]);
  const [total, setTotal] = useState(0);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);
  const [sheet, setSheet] = useState(false);
  const [myTsapId, setMyTsapId] = useState("TSAP-M-2025-1042");
  const [credits, setCredits] = useState(3);
  const [savedIds, setSavedIds] = useState<string[]>([]);
  const [sending, setSending] = useState("");
  const [note, setNote] = useState<{ ok: boolean; text: string } | null>(null);
  const [savedSearches, setSavedSearches] = useState<any[]>([]);
  const [myPhone, setMyPhone] = useState("98480xxxxx");
  const reqId = useRef(0);

  const setF = useCallback((k: string, v: any) => setFilters((p) => ({ ...p, [k]: v })), []);

  /* ---------- viewer + credits + saved shortlist + saved searches ---------- */
  useEffect(() => {
    const id = localStorage.getItem("tsap_id");
    if (id) setMyTsapId(id.toUpperCase());
    const c = localStorage.getItem("tsap_credits");
    if (c) setCredits(parseInt(c));
    try {
      const ss = JSON.parse(localStorage.getItem(SAVED_SEARCHES_KEY) || "[]");
      if (Array.isArray(ss)) setSavedSearches(ss);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    if (!myTsapId) return;
    fetch(`/api/saved/${myTsapId}`)
      .then((r) => r.json())
      .then((d) => setSavedIds((d.items || []).map((x: any) => x.profile?.tsap_id).filter(Boolean)))
      .catch(() => { /* ignore */ });
  }, [myTsapId]);

  /* ---------- fetch (debounced) ---------- */
  const load = useCallback(async () => {
    const id = ++reqId.current;
    setLoading(true);
    const qs = new URLSearchParams();
    const skip: Row = { age_min: 18, age_max: 60, salary_min: 0, verified_only: false, photo_only: false };
    Object.keys(filters).forEach((k) => {
      const v = filters[k];
      if (v === "" || v === null || v === undefined) return;
      if (v === false) { if (skip[k]) return; }
      if (v === true) qs.set(k, "true");
      else if (typeof v === "number") { if (skip[k] === v) return; qs.set(k, String(v)); }
      else if (k in skip && String(skip[k]) === String(v)) return;
      else qs.set(k, String(v));
    });
    qs.set("sort", sort);
    qs.set("limit", "30");
    if (myTsapId) qs.set("viewer_id", myTsapId);
    try {
      const r = await fetch(`/api/search?${qs.toString()}`);
      const d = await r.json();
      if (id !== reqId.current) return;
      if (r.ok && Array.isArray(d.results)) {
        setRows(d.results);
        setTotal(d.total ?? d.results.length);
        setMsg(d.message_telugu || "");
      } else {
        throw new Error("bad");
      }
    } catch {
      if (id !== reqId.current) return;
      setRows(FALLBACK);
      setTotal(FALLBACK.length);
      setMsg("⚠️ Server nunchi results ravaledu — demo profiles chupisthunnam (filters Apply chesthe malli try avutundi)");
    }
    setLoading(false);
  }, [filters, sort, myTsapId]);

  useEffect(() => {
    const t = setTimeout(load, 320);
    return () => clearTimeout(t);
  }, [load]);

  /* ---------- actions ---------- */
  const toggleSave = async (row: Row) => {
    try {
      const d = await fetch("/api/save", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tsap_id: myTsapId, saved_id: row.tsap_id }),
      }).then((r) => r.json());
      if (d.success) {
        setSavedIds((prev) => (d.saved ? (prev.includes(row.tsap_id) ? prev : [...prev, row.tsap_id])
                                       : prev.filter((x) => x !== row.tsap_id)));
        setNote({ ok: true, text: d.message_telugu || "Shortlist update ayyindi" });
      }
    } catch {
      setNote({ ok: false, text: "Save avvaledu — malli try cheyyandi" });
    }
  };

  const sendInterest = async (row: Row) => {
    setSending(row.tsap_id);
    setNote(null);
    try {
      const r = await fetch("/api/interest/send", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from_id: myTsapId, to_id: row.tsap_id, channel: "matches_page" }),
      });
      const d = await r.json();
      setNote({ ok: !!d.success, text: d.message_telugu || d.detail || "Interest pampaledu" });
      if (d.credits_left !== undefined) {
        setCredits(d.credits_left);
        localStorage.setItem("tsap_credits", String(d.credits_left));
      }
    } catch {
      setNote({ ok: false, text: "Network problem — malli try cheyyandi" });
    }
    setSending("");
  };

  const shareText = (row: Row) =>
    `🙏 ${SITE_CONFIG.brandName} profile — ${row.full_name} (${row.tsap_id})\n` +
    `👉 ${row.age}y • ${row.caste} • ${row.education} • ${row.job}${row.company ? " @ " + row.company : ""}\n` +
    `📍 ${row.district}, ${row.state} • 💰 ${row.salary} • ⭐ ${row.star || "—"}\n` +
    `Full details: ${SITE_CONFIG.siteUrl || "https://manavivaha.in"}/search/${row.tsap_id}`;

  const shareWhatsApp = (row: Row) =>
    window.open(`https://wa.me/?text=${encodeURIComponent(shareText(row))}`, "_blank");
  const shareTelegram = (row: Row) =>
    window.open(`https://t.me/share/url?url=${encodeURIComponent((SITE_CONFIG.siteUrl || "https://manavivaha.in") + "/search/" + row.tsap_id)}&text=${encodeURIComponent(shareText(row))}`, "_blank");

  const copySearchLink = () => {
    const url = `${window.location.origin}/matches?${new URLSearchParams(
      Object.keys(filters).filter((k) => filters[k] !== "" && filters[k] !== false).map((k) => [k, String(filters[k])] as [string, string])
    ).toString()}`;
    navigator.clipboard?.writeText(url);
    setNote({ ok: true, text: "🔗 Search link copy ayyindi — WhatsApp group lo pettandi (vaallu kooda ee filters tho chustharu)" });
  };

  const saveSearch = () => {
    const active = activeChips;
    if (!active.length) { setNote({ ok: false, text: "Modata filters select cheyyandi" }); return; }
    const label = active.map((c) => c.label).join(" • ");
    const next = [{ label, filters: { ...filters }, sort }, ...savedSearches.filter((s) => s.label !== label)].slice(0, 8);
    setSavedSearches(next);
    localStorage.setItem(SAVED_SEARCHES_KEY, JSON.stringify(next));
    setNote({ ok: true, text: `🔔 Search save ayyindi: ${label} — kotha matches vachinappudu digest lo vastayi` });
  };

  /* ---------- active filter chips ---------- */
  const activeChips = useMemo(() => {
    const out: { key: string; label: string; clear: () => void }[] = [];
    const add = (key: string, label: string, v: any) => out.push({ key, label, clear: () => setF(key, v) });
    if (filters.gender) add("gender", filters.gender === "Bride" ? "👰 Brides" : "🤵 Grooms", "");
    if (filters.q) add("q", `🔍 "${filters.q}"`, "");
    if (filters.state) add("state", filters.state === "TS" ? "Telangana" : filters.state === "AP" ? "Andhra" : filters.state, "");
    if (filters.district) add("district", filters.district, "");
    if (filters.caste) add("caste", filters.caste, "");
    if (filters.job) add("job", filters.job, "");
    if (filters.education) add("education", filters.education, "");
    if (filters.marital_status) add("marital_status", filters.marital_status, "");
    if (filters.religion) add("religion", filters.religion, "");
    if (filters.salary_min) add("salary_min", `💰 ${filters.salary_min / 100000}L+`, 0);
    if (filters.age_min !== 18 || filters.age_max !== 60) add("age_min", `🎂 ${filters.age_min}–${filters.age_max}y`, 18);
    if (filters.verified_only) add("verified_only", "✅ Verified", false);
    if (filters.photo_only) add("photo_only", "📸 Photo", false);
    return out;
  }, [filters, setF]);

  const resultsInfo = loading ? "⏳ వెతుకుతున్నాం…" : `${total} profiles dorikayi`;

  /* ---------- card ---------- */
  const Card = ({ row }: { row: Row }) => {
    const saved = savedIds.includes(row.tsap_id);
    const initial = String(row.full_name || "?").trim().charAt(0).toUpperCase();
    return (
      <div className="bg-white rounded-[1.5rem] border border-gold/25 card-shadow overflow-hidden">
        <div className="flex gap-3 p-4">
          <Link href={`/search/${row.tsap_id}`} className="shrink-0">
            {row.photo_url || row.has_photo ? (
              <img src={row.photo_url || `/photos/${row.tsap_id}_1.jpg`} alt={row.full_name}
                className="w-[84px] h-[104px] rounded-2xl object-cover border border-gold/40" />
            ) : (
              <div className="w-[84px] h-[104px] rounded-2xl maroon-gradient text-white flex flex-col items-center justify-center border border-gold/40">
                <span className="text-3xl font-bold telugu">{initial}</span>
                <span className="text-[9px] mt-1 opacity-90">photo ledu</span>
              </div>
            )}
          </Link>

          <div className="flex-1 min-w-0">
            <div className="flex items-start gap-2">
              <div className="min-w-0 flex-1">
                <div className="font-bold text-[15px] text-ink truncate">
                  {row.full_name}
                  {row.phone_verified ? <span className="ml-1 text-[11px] text-emerald-700">✅</span> : null}
                  {row.boosted ? <span className="ml-1 text-[11px]">⚡</span> : null}
                </div>
                <div className="text-[11px] text-gray-500 font-mono">{row.tsap_id}</div>
              </div>
              {row.score ? (
                <div className="shrink-0 text-center">
                  <div className="w-12 h-12 rounded-full gold-gradient text-maroon font-bold flex items-center justify-center text-[15px]">
                    {row.score}
                  </div>
                  <div className="text-[9px] text-gray-500 mt-0.5">match %</div>
                </div>
              ) : null}
            </div>

            <div className="mt-1.5 text-[12px] text-gray-700 leading-relaxed">
              {row.age}y • {row.height || "—"} • <b>{row.caste}</b>{row.sub_caste ? ` (${row.sub_caste})` : ""}<br />
              🎓 {row.education}{row.education_detail ? ` ${row.education_detail}` : ""} • 💼 {row.job}{row.company ? ` @ ${row.company}` : ""}<br />
              📍 {row.district}, {row.state}{row.work_location ? ` • work: ${row.work_location}` : ""} • 💰 {row.salary}
            </div>

            <div className="mt-1.5 flex flex-wrap gap-1.5 text-[10px]">
              <span className="bg-cream border border-gold/30 rounded-full px-2 py-0.5">⭐ {row.star || "—"} / {row.rasi || "—"}</span>
              <span className="bg-cream border border-gold/30 rounded-full px-2 py-0.5">🕉️ {row.gothram || "—"}</span>
              <span className="bg-cream border border-gold/30 rounded-full px-2 py-0.5">💍 {row.marital_status || "—"}</span>
              {row.porutham?.score ? (
                <span className="bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-full px-2 py-0.5">
                  🧮 {row.porutham.score}/{row.porutham.max} — {row.porutham.verdict}
                </span>
              ) : null}
            </div>
          </div>
        </div>

        {Array.isArray(row.reasons) && row.reasons.length > 0 && (
          <div className="mx-4 mb-3 bg-cream rounded-2xl p-3">
            <div className="text-[11px] font-bold text-maroon">💡 Enduku match avutharu?</div>
            <ul className="mt-1 space-y-0.5">
              {row.reasons.slice(0, 4).map((r: string, i: number) => (
                <li key={i} className="text-[11px] text-gray-700">✔️ {r}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="px-4 pb-4 flex flex-wrap gap-2">
          <Link href={`/search/${row.tsap_id}`} className="flex-1 min-w-[92px] py-2.5 rounded-xl border border-maroon/25 text-center text-[12px] font-bold text-maroon">
            👁️ Profile
          </Link>
          <button onClick={() => sendInterest(row)} disabled={sending === row.tsap_id}
            className="flex-1 min-w-[140px] py-2.5 rounded-xl maroon-gradient text-white text-[12px] font-bold disabled:opacity-60">
            {sending === row.tsap_id ? "Pampisthunnam…" : "💌 Interest (1 credit)"}
          </button>
          <button onClick={() => toggleSave(row)}
            className={`py-2.5 px-3 rounded-xl text-[12px] font-bold border ${saved ? "border-rose-300 bg-rose-50 text-rose-700" : "border-maroon/25 text-maroon"}`}>
            {saved ? "❤️ Saved" : "🤍 Save"}
          </button>
          <button onClick={() => shareWhatsApp(row)} className="py-2.5 px-3 rounded-xl bg-green-600 text-white text-[12px] font-bold">WhatsApp</button>
          <button onClick={() => shareTelegram(row)} className="py-2.5 px-3 rounded-xl bg-blue-500 text-white text-[12px] font-bold">Telegram</button>
        </div>
      </div>
    );
  };

  return (
    <main className="min-h-screen bg-cream pb-24 md:pb-10">
      {/* ---------- sticky header ---------- */}
      <div className="sticky top-0 z-30 bg-cream/95 backdrop-blur border-b border-gold/25 safe-top">
        <div className="max-w-6xl mx-auto px-4 py-3">
          <div className="flex items-center gap-2">
            <Link href="/" className="text-[12px] font-bold text-maroon shrink-0">← Home</Link>
            <div className="flex-1 flex items-center gap-2 bg-white border border-gold/40 rounded-2xl px-3">
              <span className="text-[15px]">🔍</span>
              <input value={filters.q} onChange={(e) => setF("q", e.target.value)} placeholder="Peru / caste / district / job…"
                className="flex-1 py-3 bg-transparent outline-none text-[14px]" />
            </div>
            <button onClick={() => setSheet(true)} className="md:hidden shrink-0 px-3 py-3 rounded-2xl maroon-gradient text-white text-[12px] font-bold">
              Filters{activeChips.length ? ` ${activeChips.length}` : ""}
            </button>
            <div className="hidden md:flex items-center gap-2 shrink-0">
              <input value={myTsapId} onChange={(e) => { const v = e.target.value.toUpperCase(); setMyTsapId(v); localStorage.setItem("tsap_id", v); }}
                className="text-[11px] font-mono bg-white border border-gold/40 rounded-full px-3 py-2 w-44" title="Mee TSAP ID" />
              <span className="text-[11px] bg-white border border-gold/40 rounded-full px-3 py-2">credits <b>{credits}</b></span>
            </div>
          </div>

          <div className="mt-2 flex gap-2 overflow-x-auto pb-1">
            {SORTS.map((s) => (
              <button key={s.v} onClick={() => setSort(s.v)}
                className={`chip shrink-0 ${sort === s.v ? "chip-on" : ""}`}>{s.l}</button>
            ))}
            <button onClick={saveSearch} className="chip shrink-0">🔔 Save search</button>
            <button onClick={copySearchLink} className="chip shrink-0">🔗 Share search</button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-4 md:grid md:grid-cols-[280px_1fr] md:gap-5 md:items-start">
        {/* ---------- desktop filter sidebar ---------- */}
        <aside className="hidden md:block bg-white rounded-[1.5rem] border border-gold/25 p-4 sticky top-[132px] max-h-[76vh] overflow-y-auto">
          <div className="font-bold text-maroon text-[14px]">🔎 Filters ({activeChips.length})</div>
          <button onClick={() => { setFilters({ ...DEFAULT_FILTERS }); setSort("score"); }}
            className="mt-2 w-full py-2 rounded-xl border border-maroon/20 text-[12px] font-bold text-maroon">♻️ Reset anni</button>
          <div className="mt-3">
            <div className="text-[11px] font-bold text-ink">Evarini?</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {[{ v: "", l: "Andaru" }, { v: "Bride", l: "👰 Brides" }, { v: "Groom", l: "🤵 Grooms" }].map((g) => (
                <button key={g.v} onClick={() => setF("gender", g.v)} className={`chip ${filters.gender === g.v ? "chip-on" : ""}`}>{g.l}</button>
              ))}
            </div>
          </div>
          <div className="mt-3">
            <div className="text-[11px] font-bold text-ink">Age: <span className="text-maroon">{filters.age_min}–{filters.age_max}</span></div>
            <input type="range" min={18} max={60} value={filters.age_min} onChange={(e) => setF("age_min", Math.min(parseInt(e.target.value), filters.age_max))} className="w-full accent-[#7A0C2E]" />
            <input type="range" min={18} max={60} value={filters.age_max} onChange={(e) => setF("age_max", Math.max(parseInt(e.target.value), filters.age_min))} className="w-full accent-[#7A0C2E]" />
          </div>
          <div className="mt-3">
            <div className="text-[11px] font-bold text-ink">State</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {["", "TS", "AP", "Other"].map((s) => (
                <button key={s || "all"} onClick={() => { setF("state", s); setF("district", ""); }}
                  className={`chip ${filters.state === s ? "chip-on" : ""}`}>{s === "TS" ? "Telangana" : s === "AP" ? "Andhra" : s === "Other" ? "Other" : "Anni"}</button>
              ))}
            </div>
          </div>
          {filters.state ? (
            <div className="mt-3">
              <div className="text-[11px] font-bold text-ink">District</div>
              <div className="mt-1.5 flex flex-wrap gap-1.5 max-h-40 overflow-y-auto">
                {(DISTRICTS_BY_STATE[filters.state] || []).map((d) => (
                  <button key={d} onClick={() => setF("district", filters.district === d ? "" : d)}
                    className={`chip ${filters.district === d ? "chip-on" : ""}`}>{d}</button>
                ))}
              </div>
            </div>
          ) : null}
          <div className="mt-3">
            <div className="text-[11px] font-bold text-ink">Caste</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5 max-h-44 overflow-y-auto">
              {CASTES.slice(0, 20).map((c) => (
                <button key={c} onClick={() => setF("caste", filters.caste === c ? "" : c)}
                  className={`chip ${filters.caste === c ? "chip-on" : ""}`}>{c}</button>
              ))}
            </div>
          </div>
          <div className="mt-3">
            <div className="text-[11px] font-bold text-ink">Job</div>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {JOBS.slice(0, 10).map((j) => (
                <button key={j} onClick={() => setF("job", filters.job === j ? "" : j)}
                  className={`chip ${filters.job === j ? "chip-on" : ""}`}>{j}</button>
              ))}
            </div>
          </div>
          <button onClick={() => setSheet(true)} className="mt-3 w-full py-2.5 rounded-xl gold-gradient text-maroon text-[12px] font-bold">
            ➕ Inka ekkuva filters (caste 43, edu, salary…)
          </button>
        </aside>

        {/* ---------- results ---------- */}
        <section>
          {note && (
            <div className={`mb-3 rounded-2xl px-4 py-3 text-[13px] border ${note.ok ? "bg-emerald-50 border-emerald-200 text-emerald-900" : "bg-amber-50 border-amber-200 text-amber-900"}`}>
              {note.text}{!note.ok && <> <Link href="/requests" className="underline font-bold">Requests page →</Link></>}
            </div>
          )}

          <div className="mb-3"><QuickLead source="matches_page" /></div>

          <div className="maroon-gradient text-white rounded-[1.5rem] p-4">
            <div className="font-bold text-[14px] telugu">🚫 Chatting ledu — 💌 Interest pampu, accept aithe WhatsApp lo numbers exchange</div>
            <div className="text-[12px] opacity-90 mt-1 telugu">
              Modati 3 interest requests <b>FREE</b> • 1 request = 1 credit • Decline aithe credit refund.
            </div>
          </div>

          {activeChips.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1.5">
              {activeChips.map((c) => (
                <button key={c.key} onClick={c.clear} className="chip">
                  {c.label} <span className="text-maroon font-bold">✕</span>
                </button>
              ))}
              <button onClick={() => setFilters({ ...DEFAULT_FILTERS })} className="chip">♻️ anni clear</button>
            </div>
          )}

          {savedSearches.length > 0 && (
            <div className="mt-3">
              <div className="text-[11px] font-bold text-ink mb-1.5">🔔 Mee saved searches</div>
              <div className="flex flex-wrap gap-1.5">
                {savedSearches.map((s, i) => (
                  <button key={i} onClick={() => { setFilters({ ...DEFAULT_FILTERS, ...s.filters }); setSort(s.sort || "score"); }} className="chip">
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="mt-3 flex items-center justify-between">
            <div className="text-[12px] text-gray-600">{msg || resultsInfo}</div>
            <div className="text-[11px] text-gray-500 md:hidden">credits <b className="text-maroon">{credits}</b></div>
          </div>

          {loading ? (
            <div className="mt-3 grid md:grid-cols-2 gap-4">
              {[0, 1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-[1.5rem] border border-gold/20 p-4 animate-pulse">
                  <div className="flex gap-3">
                    <div className="w-[84px] h-[104px] rounded-2xl bg-gray-200" />
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-gray-200 rounded w-2/3" />
                      <div className="h-3 bg-gray-200 rounded w-1/3" />
                      <div className="h-3 bg-gray-200 rounded w-5/6" />
                      <div className="h-3 bg-gray-200 rounded w-3/4" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : rows.length === 0 ? (
            <div className="mt-4 bg-white rounded-[1.5rem] p-8 text-center border border-gold/25">
              <div className="text-4xl">🔍</div>
              <div className="font-bold text-ink mt-2">Ee filters ki profiles dorakaledu</div>
              <div className="text-[12px] text-gray-500 mt-1">Try cheyandi: age range penchandi, district remove cheyyandi, salary tagginchandi.</div>
              <div className="mt-3 flex flex-wrap justify-center gap-2">
                <button onClick={() => setFilters({ ...DEFAULT_FILTERS })} className="chip">♻️ Anni filters clear</button>
                <button onClick={() => setF("age_max", 60)} className="chip">🎂 Age 60 varaku</button>
                <button onClick={() => { setF("district", ""); setF("salary_min", 0); }} className="chip">📍 District + 💰 salary remove</button>
              </div>
            </div>
          ) : (
            <div className="mt-3 grid md:grid-cols-2 gap-4">
              {rows.map((row) => <Card key={row.tsap_id} row={row} />)}
            </div>
          )}

          {/* ---------- pricing strip (new ladder) ---------- */}
          <div className="mt-6 bg-white rounded-[1.5rem] p-4 border border-gold/25 text-center">
            <div className="text-[14px] font-bold text-maroon">1 credit = 1 interest request</div>
            <div className="text-[12px] text-gray-600 mt-1">
              FREE 3 • ₹99 → 5 • ₹199 → 12 • ₹299 → 25 • ₹499 → 50 (VIP) —
              <span className="text-maroon font-bold"> pedda tier lo ₹/profile thaggutundi</span>
            </div>
            <div className="text-[11px] text-gray-500 mt-1">Add-ons: ⚡ Boost ₹49 • 👀 Who-viewed ₹49 • 🧮 Porutham ₹99 • ✅ Verify badge ₹199</div>
            <div className="mt-3 flex flex-wrap justify-center gap-2">
              <Link href="/requests" className="px-5 py-2 gold-gradient rounded-full text-[13px] font-bold text-maroon">💌 Credits teesukondi</Link>
              <Link href="/register" className="px-5 py-2 maroon-gradient rounded-full text-[13px] font-bold text-white">📝 Free profile create</Link>
            </div>
          </div>
        </section>
      </div>

      <FilterSheet
        open={sheet} onClose={() => setSheet(false)} filters={filters} setF={setF}
        reset={() => setFilters({ ...DEFAULT_FILTERS })} onApply={() => setSheet(false)} resultsInfo={resultsInfo}
      />

      {myPhone ? (
        <div className="fixed bottom-3 right-3 z-20 md:hidden">
          <Link href="/requests" className="bg-white border border-gold/40 rounded-full px-4 py-2.5 text-[11px] font-bold text-maroon card-shadow">
            💌 Requests
          </Link>
        </div>
      ) : null}
    </main>
  );
}
