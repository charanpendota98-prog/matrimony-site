"use client";

/**
 * MANA VIVAHA — SMART MOBILE REGISTER (v3)
 * ========================================
 * Phone lo 3 nimushalalo complete avvali — adi target. Ela:
 *   • Chip pickers (type cheyyadam kanna tap cheyyadam easy) — caste, star, district, salary…
 *   • DOB ichina age **automatic** ga vastundi (nuvvu age type cheyyakkarledu)
 *   • Star pick chesthe **rasi automatic** ga suggest avutundi
 *   • Auto-save draft (phone refresh/back ayina form poyedu) + "Continue" banner
 *   • Bottom lo thumb-reachable big buttons (Next/Back) + sticky % progress
 *   • Inline Telugu validation — "ee field kavali" ani chepthundi (English errors ledu)
 *   • 📱 OTP verify (dev mode) → number verified badge
 *   • 📸 Photo phone lo ne compress (1200px) → upload → fast on 2G/3G too
 *   • 🎤 Voice input (about_myself) — supported browsers lo
 */
import { Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { CHANNEL_STATS } from "@/lib/channels";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Reveal from "@/components/Reveal";
import { SITE_CONFIG } from "@/lib/site-config";
import {
  BLOOD_GROUPS, BODY_TYPES, CASTES, COMPLEXIONS, DISTRICTS_BY_STATE, EDUCATIONS, FAMILY_STATUSES,
  FAMILY_TYPES, FAMILY_VALUES, HEIGHTS, JOBS, MARITAL_STATUSES, MOTHER_TONGUES, NAKSHATRAS, NAK_TO_RASI,
  OCCUPATIONS, PHYSICAL_STATUS, RASIS, RELIGIONS, SALARIES, WEIGHTS, WORK_TYPES,
  ageFromDob, compressImage, maxDobFor18,
} from "@/lib/telugu-data";

const DRAFT_KEY = "tsap_reg_draft_v3";
const STEPS = [
  { n: 1, label: "Basic", icon: "🙋", hint: "Mee basic details — 30 seconds" },
  { n: 2, label: "Community", icon: "💍", hint: "Caste + star details — card ki kavali" },
  { n: 3, label: "Education", icon: "🎓", hint: "Chaduvu + udyogam" },
  { n: 4, label: "Family", icon: "👨‍👩‍👧", hint: "Family + contact" },
  { n: 5, label: "Photo", icon: "📸", hint: "Photo + finish (chi-vi details)" },
];

const DEFAULT_FORM: Record<string, any> = {
  gender: "", full_name: "", dob: "", birth_time: "", age: "", height: "", weight: "",
  marital_status: "Pelli Kaledu", religion: "Hindu", mother_tongue: "Telugu",
  caste: "", sub_caste: "", gothram: "", star: "", rasi: "", moola_nakshatram: "No", dosham: "No",
  education: "", education_detail: "", college: "", job: "", company: "", salary: "",
  experience: "", work_type: "", work_location: "",
  father_name: "", father_occupation: "", mother_name: "", mother_occupation: "",
  brothers: "0", brothers_married: "0", sisters: "0", sisters_married: "0",
  family_type: "Nuclear", family_status: "Middle Class", family_values: "Traditional",
  native_place: "", state: "TS", district: "", mandal: "", current_city: "", pincode: "",
  phone: "", email: "", photo_private: true, about_myself: "",
  expectations: "", exp_age_min: "", exp_age_max: "", exp_job: "", exp_location: "", exp_caste: "",
  physical_status: "Normal", body_type: "Average", complexion: "Fair", blood_group: "",
  referral_code: "", consent: false,
};

/* ---------------------------------------------------------------- UI atoms */
function Chip({ on, gold, children, onClick }: { on?: boolean; gold?: boolean; children: React.ReactNode; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} className={`chip ${on ? (gold ? "chip-on-gold" : "chip-on") : ""}`}>
      {children}
    </button>
  );
}

function ChipGroup({
  label, options, value, onChange, required, searchable, te, hint, cols,
}: {
  label: string; options: { v: string; te?: string }[]; value: string; onChange: (v: string) => void;
  required?: boolean; searchable?: boolean; te?: boolean; hint?: string; cols?: number;
}) {
  const [q, setQ] = useState("");
  const list = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return options;
    return options.filter((o) => o.v.toLowerCase().includes(needle) || (o.te || "").includes(q.trim()));
  }, [q, options]);
  return (
    <div>
      <label className="text-[13px] font-bold text-ink">
        {label} {required ? <span className="req-star">*</span> : <span className="text-[10px] text-gray-400">(optional)</span>}
      </label>
      {hint && <div className="hint">{hint}</div>}
      {searchable && (
        <input
          value={q} onChange={(e) => setQ(e.target.value)} placeholder="🔍 Type chesi vethakandi…"
          className="input-mobile mt-2" inputMode="search"
        />
      )}
      <div className={`mt-2 flex flex-wrap gap-2 ${cols === 1 ? "flex-col" : ""}`}>
        {list.slice(0, searchable ? 60 : 40).map((o) => (
          <Chip key={o.v} on={value === o.v} gold={te} onClick={() => onChange(value === o.v ? "" : o.v)}>
            {te && o.te ? <span className="telugu">{o.te}</span> : null}
            <span>{o.v}</span>
          </Chip>
        ))}
        {list.length === 0 && (
          <div className="text-[12px] text-gray-500">
            Dorakaledu — <button type="button" onClick={() => onChange(q.trim())} className="text-maroon font-bold underline">“{q}” ni alane pettu</button>
          </div>
        )}
      </div>
    </div>
  );
}

function TextField({
  label, value, onChange, placeholder, required, hint, type = "text", inputMode, max, optional, telugu,
}: {
  label: string; value: string; onChange: (v: string) => void; placeholder?: string; required?: boolean;
  hint?: string; type?: string; inputMode?: "text" | "tel" | "numeric" | "email" | "decimal";
  max?: string; optional?: boolean; telugu?: boolean;
}) {
  const invalid = required && !String(value || "").trim();
  return (
    <div>
      <label className="text-[13px] font-bold text-ink">
        {label} {required ? <span className="req-star">*</span> : (optional ? <span className="text-[10px] text-gray-400">(optional)</span> : null)}
      </label>
      <input
        type={type} inputMode={inputMode} max={max} value={value} placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        aria-invalid={invalid ? "true" : "false"}
        className={`input-mobile mt-1 ${telugu ? "telugu" : ""}`}
      />
      {hint && <div className="hint">{hint}</div>}
    </div>
  );
}

function Stepper({ label, value, onChange, max = 10 }: { label: string; value: string; onChange: (v: string) => void; max?: number }) {
  const n = parseInt(value || "0", 10) || 0;
  return (
    <div className="flex items-center justify-between bg-white rounded-2xl border border-gold/30 px-3 py-2">
      <span className="text-[13px] font-bold text-ink">{label}</span>
      <div className="flex items-center gap-3">
        <button type="button" onClick={() => onChange(String(Math.max(0, n - 1)))}
          className="w-11 h-11 rounded-full maroon-gradient text-white text-xl font-bold leading-none">−</button>
        <span className="w-7 text-center font-bold text-maroon">{n}</span>
        <button type="button" onClick={() => onChange(String(Math.min(max, n + 1)))}
          className="w-11 h-11 rounded-full gold-gradient text-maroon text-xl font-bold leading-none">+</button>
      </div>
    </div>
  );
}

function Toggle({ label, sub, value, onChange }: { label: string; sub?: string; value: boolean; onChange: (v: boolean) => void }) {
  return (
    <button type="button" onClick={() => onChange(!value)}
      className="w-full flex items-center gap-3 bg-white rounded-2xl border border-gold/30 p-3 text-left">
      <span className={`w-14 h-8 rounded-full p-1 transition ${value ? "bg-maroon" : "bg-gray-300"}`}>
        <span className={`block w-6 h-6 bg-white rounded-full transition ${value ? "translate-x-6" : ""}`} />
      </span>
      <span className="min-w-0">
        <span className="block text-[13px] font-bold text-ink">{label}</span>
        {sub && <span className="block text-[11px] text-gray-500">{sub}</span>}
      </span>
    </button>
  );
}

/* ---------------------------------------------------------------- main */
function Wizard() {
  const params = useSearchParams();
  const [step, setStep] = useState(1);
  const [f, setF] = useState<Record<string, any>>(DEFAULT_FORM);
  const [errs, setErrs] = useState<string[]>([]);
  const [shake, setShake] = useState(false);
  const [busy, setBusy] = useState(false);
  const [draftFound, setDraftFound] = useState(false);
  const [savedAt, setSavedAt] = useState<string>("");
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState("");
  const [photoUrl, setPhotoUrl] = useState("");
  const [photoInfo, setPhotoInfo] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otpCode, setOtpCode] = useState("");
  const [otpMsg, setOtpMsg] = useState("");
  const [phoneOk, setPhoneOk] = useState(false);
  const [refLocked, setRefLocked] = useState("");
  const [result, setResult] = useState<any>(null);
  const [clarity, setClarity] = useState<any>(null);
  const [copied, setCopied] = useState("");
  const topRef = useRef<HTMLDivElement>(null);
  const voiceRef = useRef<any>(null);

  const set = (k: string, v: any) => {
    setF((prev) => ({ ...prev, [k]: v }));
    setErrs([]);
  };

  /* ---------- 🆓 FREE vs PAID clarity (numbers rule) — /api/free-plan ---------- */
  useEffect(() => {
    fetch("/api/free-plan").then((r) => r.json()).then(setClarity).catch(() => { });
  }, []);

  /* ---------- referral auto-lock (?ref=LAK42) ---------- */
  useEffect(() => {
    const ref = (params?.get("ref") || "").trim().toUpperCase();
    if (ref) {
      setRefLocked(ref);
      setF((prev) => ({ ...prev, referral_code: ref }));
    }
  }, [params]);

  /* ---------- draft resume ---------- */
  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (!raw) return;
      const d = JSON.parse(raw);
      if (d?.data && (d.data.full_name || d.data.phone)) {
        setDraftFound(true);
        setSavedAt(d.savedAt || "");
      }
    } catch { /* ignore */ }
  }, []);

  const resumeDraft = () => {
    try {
      const d = JSON.parse(localStorage.getItem(DRAFT_KEY) || "{}");
      setF({ ...DEFAULT_FORM, ...(d.data || {}) });
      setStep(Math.min(5, Math.max(1, d.step || 1)));
      setDraftFound(false);
    } catch { /* ignore */ }
  };

  const clearDraft = () => {
    localStorage.removeItem(DRAFT_KEY);
    setDraftFound(false);
    setF({ ...DEFAULT_FORM, referral_code: refLocked });
  };

  /* ---------- auto-save (debounced) ---------- */
  useEffect(() => {
    if (result) return;
    const t = setTimeout(() => {
      try {
        const now = new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
        localStorage.setItem(DRAFT_KEY, JSON.stringify({ data: f, step, savedAt: now }));
        setSavedAt(now);
      } catch { /* ignore */ }
    }, 700);
    return () => clearTimeout(t);
  }, [f, step, result]);

  /* ---------- age from DOB ---------- */
  useEffect(() => {
    const a = ageFromDob(f.dob);
    if (a && String(a) !== String(f.age)) setF((prev) => ({ ...prev, age: String(a) }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [f.dob]);

  /* ---------- star → rasi auto ---------- */
  useEffect(() => {
    if (f.star && !f.rasi && NAK_TO_RASI[f.star]) setF((prev) => ({ ...prev, rasi: NAK_TO_RASI[f.star] }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [f.star]);

  const scrollTop = () => topRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });

  /* ---------- validation per step ---------- */
  const validate = (s: number): string[] => {
    const e: string[] = [];
    if (s === 1) {
      if (!f.gender) e.push("Bride / Groom select cheyyandi");
      if (!String(f.full_name).trim()) e.push("Full name type cheyyandi");
      if (!f.dob) e.push("Date of birth select cheyyandi");
      else if (!ageFromDob(f.dob)) e.push("DOB correct ga ledu");
      if (!f.height) e.push("Height select cheyyandi");
      if (!f.marital_status) e.push("Marital status select cheyyandi");
    }
    if (s === 2) {
      if (!f.caste) e.push("Caste select cheyyandi (channels ki kavali)");
    }
    if (s === 3) {
      if (!f.education) e.push("Education select cheyyandi");
      if (!f.job) e.push("Job / udyogam select cheyyandi");
      if (!f.salary) e.push("Salary range select cheyyandi");
    }
    if (s === 4) {
      if (!f.state) e.push("State select cheyyandi");
      if (!f.district) e.push("District select cheyyandi");
      if (!/^\d{10}$/.test(String(f.phone))) e.push("10 digit mobile number ivvandi");
    }
    if (s === 5) {
      if (!f.consent) e.push("Terms + privacy accept cheyyandi (kindha checkbox)");
    }
    return e;
  };

  const next = () => {
    const e = validate(step);
    if (e.length) {
      setErrs(e);
      setShake(true);
      setTimeout(() => setShake(false), 400);
      scrollTop();
      return;
    }
    setErrs([]);
    setStep((s) => Math.min(5, s + 1));
    scrollTop();
  };

  const back = () => {
    setErrs([]);
    setStep((s) => Math.max(1, s - 1));
    scrollTop();
  };

  /* ---------- profile strength ---------- */
  const strength = useMemo(() => {
    const keys = ["full_name", "gender", "dob", "height", "weight", "marital_status", "caste", "sub_caste",
      "gothram", "star", "rasi", "education", "education_detail", "college", "job", "company", "salary",
      "experience", "work_type", "work_location", "father_name", "father_occupation", "mother_name",
      "native_place", "state", "district", "mandal", "current_city", "pincode", "phone", "about_myself",
      "body_type", "complexion", "blood_group"];
    const filled = keys.filter((k) => String(f[k] || "").trim()).length + (photoUrl ? 2 : 0);
    return Math.min(100, Math.round((filled / (keys.length + 2)) * 100));
  }, [f, photoUrl]);

  /* ---------- photo pick + compress ---------- */
  const pickPhoto = async (file?: File | null) => {
    if (!file) return;
    if (!file.type.startsWith("image/")) return setErrs(["Photo file matrame (JPG/PNG/WebP)"]);
    if (file.size > 8 * 1024 * 1024) return setErrs(["Photo chala peddadi (8MB+) — chinna photo pettandi"]);
    setBusy(true);
    const small = await compressImage(file, 1200, 0.85);
    setPhotoFile(small);
    setPhotoPreview(URL.createObjectURL(small));
    setPhotoInfo(`${(small.size / 1024).toFixed(0)} KB${small.size < file.size ? ` (${(file.size / 1024).toFixed(0)} KB → compress)` : ""} • upload chesthunnam…`);
    try {
      const fd = new FormData();
      fd.append("file", small);
      const r = await fetch("/api/photo/upload", { method: "POST", body: fd });
      const d = await r.json();
      if (r.ok) {
        setPhotoUrl(d.url);
        setPhotoInfo(`${d.kb} KB ✅ uploaded — card lo mee photo vasthundi`);
      } else {
        setPhotoInfo("");
        setErrs([d.detail || "Photo upload avvaledu"]);
      }
    } catch {
      setErrs(["Network problem — photo malli try cheyyandi"]);
    }
    setBusy(false);
  };

  /* ---------- OTP ---------- */
  const sendOtp = async () => {
    if (!/^\d{10}$/.test(f.phone)) return setErrs(["Mundu 10 digit number ivvandi"]);
    setBusy(true);
    try {
      const d = await fetch("/api/otp/send", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: f.phone }),
      }).then((r) => r.json());
      setOtpSent(true);
      setOtpMsg(d.message_telugu || "OTP pampinchaam");
      if (d.dev_code) setOtpCode(d.dev_code);
    } catch {
      setErrs(["OTP pampaledu — malli try cheyyandi"]);
    }
    setBusy(false);
  };

  const verifyOtp = async () => {
    setBusy(true);
    try {
      const r = await fetch("/api/otp/verify", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: f.phone, code: otpCode }),
      });
      const d = await r.json();
      if (r.ok && d.success) {
        setPhoneOk(true);
        setOtpMsg(d.message_telugu);
      } else {
        setOtpMsg(d.message_telugu || "OTP tappu");
      }
    } catch {
      setOtpMsg("Verify avvaledu — malli try cheyyandi");
    }
    setBusy(false);
  };

  /* ---------- voice input (about_myself) ---------- */
  const startVoice = () => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) return setErrs(["Ee browser lo voice input ledu — type cheyyandi"]);
    try {
      const rec = new SR();
      rec.lang = "te-IN";
      rec.continuous = false;
      rec.interimResults = false;
      rec.onresult = (ev: any) => {
        const text = ev.results?.[0]?.[0]?.transcript || "";
        set("about_myself", (f.about_myself ? f.about_myself + " " : "") + text);
      };
      rec.start();
      voiceRef.current = rec;
    } catch {
      setErrs(["Voice input start avvaledu"]);
    }
  };

  /* ---------- submit ---------- */
  const submit = async () => {
    const all = [1, 2, 3, 4, 5].flatMap(validate);
    if (all.length) {
      setErrs(all);
      setShake(true);
      setTimeout(() => setShake(false), 400);
      return;
    }
    setBusy(true);
    setErrs([]);
    try {
      const fd = new FormData();
      const strings = [
        "gender", "full_name", "dob", "birth_time", "height", "weight", "marital_status", "religion",
        "mother_tongue", "caste", "sub_caste", "gothram", "star", "rasi", "moola_nakshatram", "dosham",
        "education", "education_detail", "college", "job", "company", "salary", "experience", "work_type",
        "work_location", "father_name", "father_occupation", "mother_name", "mother_occupation", "brothers",
        "brothers_married", "sisters", "sisters_married", "family_type", "family_status", "family_values",
        "native_place", "state", "district", "mandal", "current_city", "pincode", "phone", "email",
        "about_myself", "expectations", "exp_age_min", "exp_age_max", "exp_job", "exp_location", "exp_caste",
        "physical_status", "body_type", "complexion", "blood_group", "referral_code",
      ];
      strings.forEach((k) => fd.append(k, String(f[k] ?? "")));
      fd.append("age", String(f.age || ageFromDob(f.dob) || ""));
      fd.append("photo_private", String(!!f.photo_private));
      fd.append("dob_correct", "true");
      fd.append("phone_verified", String(phoneOk));
      if (photoUrl) fd.append("photo_url", photoUrl);
      if (refLocked) fd.append("referral_code", refLocked);

      const r = await fetch("/api/register", { method: "POST", body: fd });
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail || "Register avvaledu");
      setResult(d);
      localStorage.removeItem(DRAFT_KEY);
      // 🤝 Referral page + requests lo ide user kanipinchali (demo ID kaadu)
      try {
        const newId = d.tsap_id || d.user_id || "";
        if (newId) {
          localStorage.setItem("tsap_last_id", newId);
          const list = JSON.parse(localStorage.getItem("tsap_profiles") || "[]");
          localStorage.setItem("tsap_profiles", JSON.stringify(
            [{ id: newId, name: f.full_name, gender: f.gender, at: Date.now() },
              ...list.filter((p: any) => (p?.id || p?.tsap_id) !== newId)].slice(0, 5)));
        }
      } catch { /* private mode lo localStorage block ayithe parvaledu */ }
      scrollTop();
    } catch (e: any) {
      setErrs([e?.message || "Register lo problem — malli try cheyyandi"]);
    }
    setBusy(false);
  };

  const copy = (text: string, tag: string) => {
    navigator.clipboard?.writeText(text).then(() => {
      setCopied(tag);
      setTimeout(() => setCopied(""), 1600);
    });
  };

  /* ================= SUCCESS SCREEN ================= */
  if (result) {
    const tsap = result.tsap_id || result.user_id || "TSAP-XXXX";
    const cardUrl = result.card_url || `/cards/${tsap}.png`;
    const share = result.share_text || `${SITE_CONFIG.brandName} profile ${tsap}`;
    return (
      <main className="min-h-screen">
        <section className="maroon-gradient text-white">
          <div className="max-w-3xl mx-auto px-4 py-9 text-center">
            <div className="text-5xl">🎉</div>
            <h1 className="mt-2 text-2xl font-bold">Profile ready ayyindi!</h1>
            <p className="text-[13px] opacity-90 mt-1 telugu">Mee ID + card kindha undi — WhatsApp status lo share cheyyandi, reach double avutundi.</p>
            <div className="mt-4 inline-flex items-center gap-2 bg-white/10 border border-white/25 rounded-2xl px-4 py-3">
              <span className="font-mono text-lg font-bold">{tsap}</span>
              <button onClick={() => copy(tsap, "id")} className="text-[11px] font-bold gold-gradient text-maroon px-3 py-1.5 rounded-full">
                {copied === "id" ? "copied ✓" : "copy"}
              </button>
            </div>
          </div>
        </section>

        <div className="max-w-3xl mx-auto px-4 py-6 space-y-4">
          {result.publish_targets?.length ? (
            <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
              <div className="font-bold text-emerald-900">📢 Auto-post queue ayyindi</div>
              <div className="text-[12px] text-emerald-800 mt-1">
                {result.publish_targets.join(" • ")} + WhatsApp (anti-ban random gap tho)
              </div>
            </div>
          ) : null}

          <div className="bg-white rounded-2xl p-4 border border-gold/30 card-shadow">
            <div className="font-bold text-maroon text-[15px]">🎁 Mee account ki enti vachindi</div>
            <div className="mt-2 grid sm:grid-cols-3 gap-2 text-[12px]">
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-emerald-900">
                <b>{result.credits ?? 3} requests</b> ready<br /><span className="text-[11px]">(FREE 3 + referral bonus {result.referral?.joined_with?.ok ? "+1" : ""})</span>
              </div>
              <div className="bg-cream border border-gold/40 rounded-xl p-3 text-maroon">
                <b>3 profiles</b> chudochu<br /><span className="text-[11px]">numbers 🔒 locked</span>
              </div>
              <div className="bg-navy text-white rounded-xl p-3">
                <b>Numbers eppudu?</b><br /><span className="text-[11px] opacity-90">interest pampi vaallu accept cheste (leda ₹99 plan tho ekkuva profiles)</span>
              </div>
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              <Link href={`/matches?id=${tsap}`} className="maroon-gradient text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">
                🔎 Mee 3 profiles chudandi (FREE)
              </Link>
              <Link href={`/requests?id=${tsap}`} className="border border-maroon/25 text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                💌 Interests pampandi
              </Link>
              <Link href="/pricing" className="gold-gradient text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                💰 ₹99 → 5 profiles + boost
              </Link>
            </div>
          </div>

          {result.referral?.my_code ? (
            <div className="bg-gradient-to-br from-maroon to-[#5b1030] text-white rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div className="font-bold text-[15px]">🤝 Mee referral code ready</div>
                <span className="text-[11px] font-bold gold-gradient text-maroon px-2.5 py-1 rounded-full">
                  ₹{result.referral.commission_offer || 50}/friend
                </span>
              </div>
              {result.referral.joined_with?.ok ? (
                <div className="mt-2 bg-white/10 border border-white/20 rounded-xl px-3 py-2 text-[12px]">
                  🤝 <b>{result.referral.joined_with.referrer_name} garu</b> dwara vacharu — meeku{" "}
                  <b>+{result.referral.joined_with.bonus_credits} FREE credit</b> vachindi (code {result.referral.joined_with.referrer_code}).
                  Vaallaki kooda mee first payment tho ₹50 veltundi 🙌
                </div>
              ) : result.referral.joined_with?.reason && result.referral.joined_with.reason !== "no_code" ? (
                <div className="mt-2 bg-amber-400/20 border border-amber-200/40 rounded-xl px-3 py-2 text-[11px]">
                  ℹ️ {result.referral.joined_with.message_telugu || "Referral code lock avvaledu"} — parvaledu, mee sontha code tho ippudu start cheyyandi.
                </div>
              ) : null}
              <div className="mt-3 bg-white/10 border border-white/20 rounded-xl px-3 py-2 flex items-center gap-2">
                <span className="font-mono text-base font-bold">{result.referral.my_code}</span>
                <button onClick={() => copy(String(result.referral.my_code), "refcode")}
                  className="text-[11px] font-bold gold-gradient text-maroon px-2.5 py-1 rounded-full">
                  {copied === "refcode" ? "copied ✓" : "code copy"}
                </button>
                <button onClick={() => copy(String(result.referral.my_link), "reflink")}
                  className="text-[11px] font-bold bg-white/15 border border-white/25 px-2.5 py-1 rounded-full">
                  {copied === "reflink" ? "copied ✓" : "link copy"}
                </button>
              </div>
              <div className="mt-1 text-[11px] opacity-90 break-all font-mono">{result.referral.my_link}</div>
              <div className="mt-2 text-[12px] opacity-95 telugu">{result.referral.earn_telugu}</div>
              <div className="mt-3 flex flex-wrap gap-2">
                <a href={`https://wa.me/?text=${encodeURIComponent(String(result.referral.share_message || ""))}`}
                  target="_blank" rel="noreferrer"
                  className="bg-green-600 text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  📲 WhatsApp group ki pampu
                </a>
                <a href={result.referral.poster_url} download={`${result.referral.my_code}-manavivaha-referral.png`}
                  className="gold-gradient text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  ⬇️ Poster (QR tho)
                </a>
                <a href={result.referral.poster_status_url} target="_blank" rel="noreferrer"
                  className="bg-white/10 border border-white/25 text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  📱 Status poster
                </a>
                <Link href={`${result.referral.dashboard || "/referral"}?id=${tsap}`}
                  className="bg-white/10 border border-white/25 text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  📊 Referral dashboard
                </Link>
              </div>
              <ul className="mt-2 space-y-0.5 text-[11px] opacity-85 list-disc list-inside">
                {(result.referral.rule_telugu || []).map((t: string) => <li key={t}>{t}</li>)}
              </ul>
            </div>
          ) : null}

          {result.namaste_queued ? (
            <div className="bg-cream border border-gold/40 rounded-2xl p-4">
              <div className="font-bold text-maroon text-[14px]">🙏 Namaste message mee WhatsApp ki pampam</div>
              <div className="text-[12px] text-gray-700 mt-1 telugu">
                Mana side nunchi mee profile card + full details + next steps mee number ki veltayi (chatting ledu — spam undadu).
                {result.welcome_status?.manual_text ? " Bridge connect ayyaka automatic ga pothundi; ippudu support team manual ga pampisthundi." : ""}
              </div>
              {result.welcome_status?.manual_text ? (
                <button onClick={() => copy(String(result.welcome_status.manual_text), "namaste")}
                  className="mt-2 text-[11px] font-bold gold-gradient text-maroon px-3 py-2 rounded-xl">
                  {copied === "namaste" ? "copied ✓" : "📋 Namaste message copy (support ki)"}
                </button>
              ) : null}
            </div>
          ) : null}

          {result.share_kit ? (
            <div className="bg-white rounded-2xl p-4 border border-gold/25 card-shadow">
              <div className="font-bold text-maroon text-[14px]">🎴 Share kit — reach penchandi</div>
              <div className="text-[12px] text-gray-600 mt-1 telugu">
                Card image + caption ready. Status lo pettandi — {result.share_kit.best_time_to_post}.
              </div>
              <pre className="mt-2 bg-cream rounded-xl p-3 text-[11px] whitespace-pre-wrap telugu">{result.share_kit.caption_short}</pre>
              <div className="mt-2 flex flex-wrap gap-2">
                <a href={result.share_kit.whatsapp_share} target="_blank" rel="noreferrer"
                  className="bg-green-600 text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">WhatsApp status ki</a>
                <a href={result.share_kit.telegram_share} target="_blank" rel="noreferrer"
                  className="bg-blue-500 text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">Telegram ki</a>
                <button onClick={() => copy(String(result.share_kit.caption), "kit")}
                  className="border border-maroon/25 text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  {copied === "kit" ? "copied ✓" : "📋 Caption copy"}
                </button>
                <a href={result.share_kit.card_image} download={`${tsap}-manavivaha-card.png`}
                  className="gold-gradient text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">⬇️ Card image</a>
              </div>
              <ul className="mt-2 space-y-0.5">
                {(result.share_kit.tips_telugu || []).map((t: string) => (
                  <li key={t} className="text-[11px] text-gray-600">• {t}</li>
                ))}
              </ul>
            </div>
          ) : null}

          <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/25">
            <div className="font-bold text-maroon text-[15px]">🎴 Mee profile card</div>
            {cardUrl ? (
              <img src={cardUrl} alt={`${tsap} profile card`} className="mt-3 w-full rounded-2xl border border-gold/30" />
            ) : null}
            <div className="mt-3 flex flex-wrap gap-2">
              <a href={cardUrl} download={`${tsap}-manavivaha-card.png`} className="maroon-gradient text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">
                ⬇️ Download card
              </a>
              <a href={cardUrl} target="_blank" rel="noreferrer" className="border border-maroon/30 text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
                🔍 Full size
              </a>
              <button onClick={() => copy(share, "share")} className="gold-gradient text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
                {copied === "share" ? "copied ✓" : "📋 Share text copy"}
              </button>
              <a href={`https://wa.me/?text=${encodeURIComponent(share)}`} target="_blank" rel="noreferrer"
                className="bg-green-600 text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">WhatsApp lo pampu</a>
            </div>
          </div>

          <div className="bg-navy text-white rounded-2xl p-4">
            <div className="font-bold text-[14px]">Ippudu em cheyyali? (2 steps)</div>
            <ol className="mt-2 text-[12px] space-y-1 opacity-90 list-decimal list-inside">
              <li>Mee profile {CHANNEL_STATS.total} channels lo post avutundi (4 main + caste-wise) — 30 nimushalalo live</li>
              <li>Matches chusi <b>💌 Interest pampu</b> — modati 3 FREE, vaallaki WhatsApp lo mee profile veltundi</li>
            </ol>
            <div className="mt-3 flex flex-wrap gap-2">
              <Link href={`/requests?id=${tsap}`} className="gold-gradient text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">💌 Requests dashboard</Link>
              <Link href={`/search/${tsap}`} className="bg-white/10 border border-white/25 text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">Mee profile chudu</Link>
            </div>
          </div>

          <div className="text-[11px] text-gray-500 text-center">
            ⚠️ Photos/numbers watermark + log tho untayi • Advance money adigithe report cheyyandi: {SITE_CONFIG.supportPhone}
          </div>
        </div>
      </main>
    );
  }

  /* ================= WIZARD ================= */
  const pct = Math.round(((step - 1) / 5) * 100);
  const stepMeta = STEPS[step - 1];
  const distList = DISTRICTS_BY_STATE[f.state] || [];

  return (
    <main className="min-h-screen pb-32" ref={topRef}>
      {/* ---------- sticky progress ---------- */}
      <div className="sticky top-0 z-30 bg-white/95 backdrop-blur border-b border-gold/25 safe-top">
        <div className="max-w-3xl mx-auto px-4 py-3">
          <div className="flex items-center gap-3">
            <Link href="/" className="text-[12px] font-bold text-maroon">← Home</Link>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <span className="text-lg">{stepMeta.icon}</span>
                <div className="min-w-0">
                  <div className="text-[13px] font-bold text-ink truncate">
                    Step {step} of 5 — {stepMeta.label}
                  </div>
                  <div className="text-[10px] text-gray-500 telugu truncate">{stepMeta.hint}</div>
                </div>
              </div>
            </div>
            <div className="text-right shrink-0">
              <div className="text-[11px] font-bold text-maroon">{strength}%</div>
              <div className="text-[9px] text-gray-500">profile strength</div>
            </div>
          </div>
          <div className="mt-2 flex items-center gap-1.5">
            {STEPS.map((s) => (
              <button key={s.n} onClick={() => { if (s.n < step) setStep(s.n); }}
                className={`h-1.5 flex-1 rounded-full ${s.n <= step ? "maroon-gradient" : "bg-gray-200"}`} aria-label={`Step ${s.n}`} />
            ))}
          </div>
          <div className="mt-1.5 flex items-center justify-between text-[10px] text-gray-500">
            <span>≈ {Math.max(1, 5 - step)} nimishalu migilindi</span>
            <span>{savedAt ? `💾 draft save ${savedAt}` : "💾 auto-save ON"}</span>
          </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-5">
        {/* 🆓 FREE vs PAID — SCREEN 1 lo ne clear ga (numbers rule kooda) */}
        <div className="mb-4 bg-white rounded-2xl border border-gold/40 card-shadow p-4">
          <div className="font-bold text-maroon text-[14px]">🆓 Register 100% FREE — enti vasthundi, enti raadu (clear ga)</div>
          <div className="mt-2 grid sm:grid-cols-2 gap-3 text-[12px]">
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3">
              <div className="font-bold text-emerald-900">FREE లో ఇచ్చేది</div>
              <ul className="mt-1 space-y-0.5 text-emerald-900">
                <li>✅ <b>{(clarity?.free?.profiles ?? 3)} profiles</b> chudochu (full details: caste, education, job, family, porutham)</li>
                <li>✅ <b>{(clarity?.free?.requests ?? 3)} interests</b> pampochu — vaallaki mana WhatsApp nunchi mee profile veltundi</li>
                <li>✅ Mee profile card FREE (Telugu, neat) + channels lo auto-post</li>
                <li>✅ Vaallu <b>accept cheste → numbers exchange</b> (WhatsApp lo, consent tho)</li>
              </ul>
            </div>
            <div className="bg-rose-50 border border-rose-200 rounded-xl p-3">
              <div className="font-bold text-rose-900">FREE లో ఇవ్వనిది (🔒)</div>
              <ul className="mt-1 space-y-0.5 text-rose-900">
                <li>🔒 <b>Phone numbers — ఇవ్వము</b> (98••••••45 ani matrame kanipisthundi)</li>
                <li>🔒 Photo (privacy mode unna profiles ki blur)</li>
                <li>🚫 Chatting ledu (manam chat platform kaadu — spam/report తగ్గడానికి)</li>
              </ul>
              <div className="mt-1 text-[11px]">3 FREE taruvata: <b>₹99 → 5 profiles + boost</b> · ₹199 → 12 · ₹299 → 25 · ₹499 → 50</div>
            </div>
          </div>
          <div className="mt-2 text-[11px] text-gray-600">
            🔐 Mee number DB lo encrypt ga untundi. Consent (accept) tho matrame evariki kanipisthundi.
            {" "}<a href="/pricing" className="underline font-bold text-maroon">Pricing</a> ·
            {" "}<a href="/safety" className="underline font-bold text-maroon">Safety</a>
          </div>
        </div>

        {/* draft banner */}
        {draftFound && (
          <div className="mb-4 bg-cream border border-gold/40 rounded-2xl p-4">
            <div className="font-bold text-maroon text-[14px]">💾 Mee pura form dorkindi{draftSavedLabel(savedAt)}</div>
            <div className="text-[12px] text-gray-600 mt-1">Ekkada aagipoyindo akkada nunchi continue cheyyochu — malli type cheyyakkarledu.</div>
            <div className="mt-3 flex gap-2">
              <button onClick={resumeDraft} className="maroon-gradient text-white font-bold text-[13px] px-4 py-2.5 rounded-xl">▶️ Continue chey</button>
              <button onClick={clearDraft} className="border border-maroon/25 text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">Kotha ga start</button>
            </div>
          </div>
        )}

        {refLocked && (
          <div className="mb-4 bg-emerald-50 border border-emerald-200 rounded-2xl px-4 py-3 text-[12px] text-emerald-900">
            🤝 <b>{refLocked}</b> referral code lock ayyindi — mee friend ki ₹50 + meeku <b>+1 credit FREE</b>.
            {" "}Register FREE (3 profiles free) — tarvata mee ₹99 plan thisukunte aa ₹50 mee friend wallet ki veltundi.
          </div>
        )}

        {errs.length > 0 && (
          <div className={`mb-4 bg-rose-50 border border-rose-200 rounded-2xl px-4 py-3 ${shake ? "shake" : ""}`}>
            <div className="font-bold text-rose-800 text-[13px]">Ivi saricheyyali:</div>
            <ul className="mt-1 text-[12px] text-rose-700 list-disc list-inside">
              {errs.slice(0, 5).map((e) => <li key={e}>{e}</li>)}
            </ul>
          </div>
        )}

        <div key={step} className="step-slide space-y-5">
          {/* ---------------- STEP 1 ---------------- */}
          {step === 1 && (
            <>
              <div>
                <label className="text-[13px] font-bold text-ink">Evaru register chesthunnaru? <span className="req-star">*</span></label>
                <div className="mt-2 grid grid-cols-2 gap-3">
                  {[{ v: "Bride", l: "👰 పెళ్లి కూతురు", s: "Bride" }, { v: "Groom", l: "🤵 పెళ్లి కొడుకు", s: "Groom" }].map((g) => (
                    <button key={g.v} type="button" onClick={() => set("gender", g.v)}
                      className={`rounded-2xl border-2 p-4 text-center ${f.gender === g.v ? "border-maroon bg-maroon-soft" : "border-gold/30 bg-white"}`}>
                      <div className="text-2xl">{g.v === "Bride" ? "👰" : "🤵"}</div>
                      <div className="font-bold text-[14px] text-maroon mt-1 telugu">{g.l}</div>
                      <div className="text-[11px] text-gray-500">{g.s}</div>
                    </button>
                  ))}
                </div>
              </div>

              <TextField label="Full name" value={f.full_name} onChange={(v) => set("full_name", v)} required
                placeholder="Lakshmi Reddy" hint="Card + channels lo ide peru kanipisthundi" />

              <div className="grid grid-cols-2 gap-3">
                <TextField label="Date of birth" value={f.dob} onChange={(v) => set("dob", v)} required
                  type="date" max={maxDobFor18()} hint="Age automatic vastundi" />
                <div>
                  <label className="text-[13px] font-bold text-ink">Age (auto)</label>
                  <div className="input-mobile mt-1 flex items-center justify-between bg-cream">
                    <span className="font-bold text-maroon">{f.age || "—"}</span>
                    <span className="text-[10px] text-gray-500">DOB nunchi</span>
                  </div>
                </div>
              </div>

              <ChipGroup label="Height" required options={HEIGHTS.map((h) => ({ v: h }))} value={f.height}
                onChange={(v) => set("height", v)} />
              <ChipGroup label="Weight" options={WEIGHTS.map((w) => ({ v: w }))} value={f.weight}
                onChange={(v) => set("weight", v)} />
              <ChipGroup label="Marital status" required options={MARITAL_STATUSES.map((m) => ({ v: m }))}
                value={f.marital_status} onChange={(v) => set("marital_status", v)} />
              <ChipGroup label="Religion" options={RELIGIONS.map((r) => ({ v: r }))} value={f.religion}
                onChange={(v) => set("religion", v)} />
              <ChipGroup label="Mother tongue" options={MOTHER_TONGUES.map((m) => ({ v: m }))} value={f.mother_tongue}
                onChange={(v) => set("mother_tongue", v)} />
            </>
          )}

          {/* ---------------- STEP 2 ---------------- */}
          {step === 2 && (
            <>
              <ChipGroup label="Caste" required searchable
                options={CASTES.map((c) => ({ v: c }))} value={f.caste} onChange={(v) => set("caste", v)}
                hint="43 caste channels unnayi — mee caste channel lo profile post avutundi" />
              <TextField label="Sub caste" optional value={f.sub_caste} onChange={(v) => set("sub_caste", v)}
                placeholder="Pakanati / Deshathi / Telaga…" />
              <TextField label="Gothram" optional value={f.gothram} onChange={(v) => set("gothram", v)}
                placeholder="Bharadwaj" hint="Porutham report ki kavali" />
              <ChipGroup label="Star / Nakshatram" searchable te
                options={NAKSHATRAS.map((n) => ({ v: n.en, te: n.te }))} value={f.star}
                onChange={(v) => set("star", v)} hint="Star select chesthe rasi automatic vastundi (porutham 10/10)" />
              <ChipGroup label="Rasi" te options={RASIS.map((r) => ({ v: r.en, te: r.te }))} value={f.rasi}
                onChange={(v) => set("rasi", v)} />
              <ChipGroup label="Moola nakshatram?" options={[{ v: "No" }, { v: "Yes" }]} value={f.moola_nakshatram}
                onChange={(v) => set("moola_nakshatram", v)} />
              <ChipGroup label="Dosham unda?" options={[{ v: "No" }, { v: "Yes" }, { v: "Not Sure" }]} value={f.dosham}
                onChange={(v) => set("dosham", v)} />
            </>
          )}

          {/* ---------------- STEP 3 ---------------- */}
          {step === 3 && (
            <>
              <ChipGroup label="Education" required searchable options={EDUCATIONS.map((x) => ({ v: x }))}
                value={f.education} onChange={(v) => set("education", v)} />
              <TextField label="Education detail" optional value={f.education_detail} onChange={(v) => set("education_detail", v)}
                placeholder="CSE / Finance / Nursing…" />
              <TextField label="College / University" optional value={f.college} onChange={(v) => set("college", v)}
                placeholder="JNTU Hyderabad" />
              <ChipGroup label="Job / Udyogam" required searchable options={JOBS.map((j) => ({ v: j }))}
                value={f.job} onChange={(v) => set("job", v)} />
              <TextField label="Company" optional value={f.company} onChange={(v) => set("company", v)} placeholder="TCS / Govt / Own business" />
              <TextField label="Experience" optional value={f.experience} onChange={(v) => set("experience", v)}
                inputMode="numeric" placeholder="3 years" />
              <div className="grid grid-cols-2 gap-3">
                <ChipGroup label="Work type" options={WORK_TYPES.map((w) => ({ v: w }))} value={f.work_type}
                  onChange={(v) => set("work_type", v)} />
              </div>
              <ChipGroup label="Salary" required options={SALARIES.map((s) => ({ v: s }))} value={f.salary}
                onChange={(v) => set("salary", v)} hint="Approximate range chalu — exact number vadalasina avasaram ledu" />
              <TextField label="Work location" optional value={f.work_location} onChange={(v) => set("work_location", v)}
                placeholder="Hyderabad / Gachibowli / USA" />
            </>
          )}

          {/* ---------------- STEP 4 ---------------- */}
          {step === 4 && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <ChipGroup label="State" required options={[{ v: "TS" }, { v: "AP" }, { v: "Other" }]} value={f.state}
                  onChange={(v) => { set("state", v); set("district", ""); }} />
              </div>
              <ChipGroup label="District" required searchable options={distList.map((d) => ({ v: d }))}
                value={f.district} onChange={(v) => set("district", v)}
                hint="District channel + local matches ki kavali" />
              <div className="grid grid-cols-1 gap-3">
                <TextField label="Mandal / Area" optional value={f.mandal} onChange={(v) => set("mandal", v)} placeholder="Miryalaguda" />
                <TextField label="Current city" optional value={f.current_city} onChange={(v) => set("current_city", v)} placeholder="Hyderabad" />
                <TextField label="Pincode" optional value={f.pincode} onChange={(v) => set("pincode", v)} inputMode="numeric" placeholder="500032" />
                <TextField label="Native place" optional value={f.native_place} onChange={(v) => set("native_place", v)} placeholder="Nalgonda" />
              </div>

              <div className="bg-white rounded-2xl border border-gold/30 p-4 space-y-3">
                <div className="font-bold text-maroon text-[14px]">📱 Mobile number (verification)</div>
                <TextField label="WhatsApp / Mobile" required value={f.phone} onChange={(v) => set("phone", v.replace(/\D/g, "").slice(0, 10))}
                  type="tel" inputMode="tel" placeholder="98480 12345"
                  hint="Mee number evariki kanipinchadu — interest accept ayyaka matrame exchange avutundi" />
                {!phoneOk ? (
                  <div className="flex flex-wrap items-center gap-2">
                    <button type="button" onClick={sendOtp} disabled={busy || f.phone.length !== 10}
                      className="maroon-gradient text-white font-bold text-[13px] px-4 py-2.5 rounded-xl disabled:opacity-50">
                      {otpSent ? "OTP malli pampu" : "OTP pampu"}
                    </button>
                    {otpSent && (
                      <>
                        <input value={otpCode} onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, "").slice(0, 4))}
                          inputMode="numeric" placeholder="4 digit OTP"
                          className="input-mobile w-32 text-center tracking-[0.4em] font-bold" />
                        <button type="button" onClick={verifyOtp} disabled={busy || otpCode.length !== 4}
                          className="gold-gradient text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl disabled:opacity-50">✅ Verify</button>
                      </>
                    )}
                  </div>
                ) : (
                  <div className="text-[12px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-xl px-3 py-2">
                    ✅ Number verify ayyindi — verified badge profile ki vastundi
                  </div>
                )}
                {otpMsg && <div className="text-[11px] text-gray-600">{otpMsg}</div>}
                <TextField label="Email" optional value={f.email} onChange={(v) => set("email", v)} inputMode="email" placeholder="name@gmail.com" />
              </div>

              <div className="grid grid-cols-1 gap-3">
                <TextField label="Father name" optional value={f.father_name} onChange={(v) => set("father_name", v)} />
                <ChipGroup label="Father occupation" options={OCCUPATIONS.map((o) => ({ v: o }))} value={f.father_occupation}
                  onChange={(v) => set("father_occupation", v)} />
                <TextField label="Mother name" optional value={f.mother_name} onChange={(v) => set("mother_name", v)} />
                <ChipGroup label="Mother occupation" options={OCCUPATIONS.map((o) => ({ v: o }))} value={f.mother_occupation}
                  onChange={(v) => set("mother_occupation", v)} />
              </div>

              <Stepper label="Brothers" value={f.brothers} onChange={(v) => set("brothers", v)} />
              <Stepper label="Brothers (married)" value={f.brothers_married} onChange={(v) => set("brothers_married", v)} />
              <Stepper label="Sisters" value={f.sisters} onChange={(v) => set("sisters", v)} />
              <Stepper label="Sisters (married)" value={f.sisters_married} onChange={(v) => set("sisters_married", v)} />
              <ChipGroup label="Family type" options={FAMILY_TYPES.map((x) => ({ v: x }))} value={f.family_type}
                onChange={(v) => set("family_type", v)} />
              <ChipGroup label="Family status" options={FAMILY_STATUSES.map((x) => ({ v: x }))} value={f.family_status}
                onChange={(v) => set("family_status", v)} />
              <ChipGroup label="Family values" options={FAMILY_VALUES.map((x) => ({ v: x }))} value={f.family_values}
                onChange={(v) => set("family_values", v)} />
            </>
          )}

          {/* ---------------- STEP 5 ---------------- */}
          {step === 5 && (
            <>
              <div className="bg-white rounded-2xl border border-gold/30 p-4">
                <div className="font-bold text-maroon text-[15px]">📸 Photo (3x ekkuva matches vastayi)</div>
                <div className="hint">Phone gallery / camera nunchi teesukondi. Photo automatic ga compress avutundi (fast upload). Watermark + private mode tho safe.</div>
                <div className="mt-3 flex items-center gap-3">
                  <label className="cursor-pointer">
                    <input type="file" accept="image/*" className="hidden"
                      onChange={(e) => pickPhoto(e.target.files?.[0])} />
                    <span className="inline-block maroon-gradient text-white font-bold text-[13px] px-4 py-3 rounded-xl">
                      {photoPreview ? "Photo marchu" : "📷 Photo select / camera"}
                    </span>
                  </label>
                  {photoPreview && (
                    <div className="relative">
                      <img src={photoPreview} alt="preview" className="w-20 h-20 rounded-2xl object-cover border-2 border-gold" />
                      <button type="button"
                        onClick={() => { setPhotoFile(null); setPhotoPreview(""); setPhotoUrl(""); setPhotoInfo(""); }}
                        className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-white border border-rose-300 text-rose-600 font-bold text-xs">✕</button>
                    </div>
                  )}
                </div>
                {photoInfo && <div className="hint mt-2">{photoInfo}</div>}
              </div>

              <Toggle label="🔒 Photo-private mode" sub="Public lo blur ga kanipisthundi — interest accept ayyaka matrame clear"
                value={!!f.photo_private} onChange={(v) => set("photo_private", v)} />

              <div>
                <label className="text-[13px] font-bold text-ink">About me / Naa gurinchi <span className="text-[10px] text-gray-400">(optional)</span></label>
                <textarea value={f.about_myself} onChange={(e) => set("about_myself", e.target.value.slice(0, 600))}
                  rows={4} placeholder="Nenu simple family, software engineer… (Telugu lo kooda rayochu)"
                  className="input-mobile mt-1 telugu" />
                <div className="mt-2 flex items-center gap-2">
                  <button type="button" onClick={startVoice}
                    className="border border-maroon/30 text-maroon font-bold text-[12px] px-3 py-2 rounded-xl">🎤 Voice tho cheppu</button>
                  <span className="text-[10px] text-gray-500">{f.about_myself.length}/600</span>
                </div>
              </div>

              <ChipGroup label="Body type" options={BODY_TYPES.map((x) => ({ v: x }))} value={f.body_type}
                onChange={(v) => set("body_type", v)} />
              <ChipGroup label="Complexion" options={COMPLEXIONS.map((x) => ({ v: x }))} value={f.complexion}
                onChange={(v) => set("complexion", v)} />
              <ChipGroup label="Blood group" options={BLOOD_GROUPS.map((x) => ({ v: x }))} value={f.blood_group}
                onChange={(v) => set("blood_group", v)} />
              <ChipGroup label="Physical status" options={PHYSICAL_STATUS.map((x) => ({ v: x }))} value={f.physical_status}
                onChange={(v) => set("physical_status", v)} />

              <div className="bg-cream rounded-2xl border border-gold/30 p-4 space-y-3">
                <div className="font-bold text-maroon text-[14px]">💞 Mee expectations (matches filter ki)</div>
                <div className="grid grid-cols-2 gap-3">
                  <TextField label="Age from" optional value={f.exp_age_min} onChange={(v) => set("exp_age_min", v.replace(/\D/g, "").slice(0, 2))}
                    inputMode="numeric" placeholder="22" />
                  <TextField label="Age to" optional value={f.exp_age_max} onChange={(v) => set("exp_age_max", v.replace(/\D/g, "").slice(0, 2))}
                    inputMode="numeric" placeholder="30" />
                </div>
                <ChipGroup label="Job preference" options={JOBS.slice(0, 12).map((j) => ({ v: j }))} value={f.exp_job}
                  onChange={(v) => set("exp_job", v)} />
                <TextField label="Location preference" optional value={f.exp_location} onChange={(v) => set("exp_location", v)}
                  placeholder="Hyderabad / USA" />
                <ChipGroup label="Caste preference" options={[{ v: "Same caste" }, { v: "Any caste" }, { v: "Caste no bar" }]}
                  value={f.exp_caste} onChange={(v) => set("exp_caste", v)} />
                <TextField label="Free text expectations" optional value={f.expectations} onChange={(v) => set("expectations", v)}
                  placeholder="Govt job / business / respects elders…" />
              </div>

              <label className="flex items-start gap-3 bg-white rounded-2xl border border-gold/30 p-4">
                <input type="checkbox" checked={!!f.consent} onChange={(e) => set("consent", e.target.checked)}
                  className="mt-1 w-5 h-5 accent-[#7A0C2E]" />
                <span className="text-[12px] text-gray-700">
                  Naa details <b>nijam</b> ani confirm chesthunnanu. <b>Mana Vivaha</b> terms + privacy policy accept chesthunnanu —
                  details channels lo post avutayi, number accept ayyaka matrame share avutundi.
                </span>
              </label>
            </>
          )}
        </div>

        {/* ---------------- trust strip ---------------- */}
        <div className="mt-6 grid grid-cols-2 gap-2 text-[11px] text-gray-600">
          {["🔒 Number evariki ivvamu", "🛡️ Watermark + log", "↩️ Decline aithe refund", "🚫 Chatting ledu"].map((t) => (
            <div key={t} className="bg-white border border-gold/25 rounded-xl px-3 py-2">{t}</div>
          ))}
        </div>
      </div>

      {/* ---------------- sticky action bar ---------------- */}
      <div className="fixed bottom-0 left-0 right-0 z-40 bg-white/97 backdrop-blur border-t border-gold/30 safe-bottom">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center gap-3">
          {step > 1 && (
            <button onClick={back} className="px-5 py-3.5 rounded-2xl border border-maroon/25 text-maroon font-bold text-[14px]">
              ← Back
            </button>
          )}
          <div className="flex-1 text-[10px] text-gray-500">
            {step < 5 ? `Next: ${STEPS[step].label}` : "Chivari step — submit cheyyandi"}
          </div>
          {step < 5 ? (
            <button onClick={next} className="px-7 py-3.5 rounded-2xl maroon-gradient text-white font-bold text-[15px]">
              Next →
            </button>
          ) : (
            <button onClick={submit} disabled={busy}
              className="px-6 py-3.5 rounded-2xl gold-gradient text-maroon font-bold text-[15px] disabled:opacity-60">
              {busy ? "Register avutund…" : "✅ Register cheyyi"}
            </button>
          )}
        </div>
      </div>
    </main>
  );
}

function draftSavedLabel(savedAt: string) {
  return savedAt ? ` (${savedAt} ki save ayyindi)` : "";
}

export default function RegisterPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[60vh] flex items-center justify-center text-gray-500 text-sm">
          Register form load avutundi…
        </div>
      }
    >
      <Wizard />
    </Suspense>
  );
}
