"use client";
/**
 * 🏪 VENDOR REGISTER — mee business ni Mana Vivaha lo promote cheyyandi
 * ==================================================================
 * 18 categories (catering, photography, decorations, hall, pandit...) + ad packages ₹149 → ₹3999.
 * Register → payment (UPI/PhonePe) → admin verify (2 గంటల్లో) → listing ACTIVE + promo post + poster.
 */
import { useEffect, useState } from "react";
import Link from "next/link";

type Cat = { key: string; en: string; te: string; icon: string; kw: string };
type Pkg = { code: string; name: string; price: number; days: number; telugu: string; perks: string[]; popular?: boolean };

const EMPTY = {
  business_name: "", owner_name: "", category: "", phone: "", whatsapp: "", city: "", district: "",
  state: "TS", service_areas: "", price_range: "", about: "", experience_years: "", photo_url: "",
  package: "V_STANDARD", source: "website",
};

export default function VendorRegisterPage() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [pkgs, setPkgs] = useState<Pkg[]>([]);
  const [f, setF] = useState<any>({ ...EMPTY });
  const [busy, setBusy] = useState(false);
  const [errs, setErrs] = useState<string[]>([]);
  const [res, setRes] = useState<any>(null);
  const [copied, setCopied] = useState("");

  useEffect(() => {
    fetch("/api/vendors/categories").then((r) => r.json()).then((d) => setCats(d.categories || [])).catch(() => { });
    fetch("/api/vendors/packages").then((r) => r.json()).then((d) => {
      setPkgs(d.packages || []);
      const q = new URLSearchParams(window.location.search).get("package");
      if (q) setF((p: any) => ({ ...p, package: q.toUpperCase() }));
      // default: popular package
      const pop = (d.packages || []).find((p: Pkg) => p.popular);
      if (pop && !q) setF((p: any) => ({ ...p, package: pop.code }));
    }).catch(() => { });
  }, []);

  const set = (k: string, v: any) => setF((p: any) => ({ ...p, [k]: v }));

  const validate = () => {
    const e: string[] = [];
    if ((f.business_name || "").trim().length < 3) e.push("Business peru ivvandi (3+ aksharalu)");
    if (!f.category) e.push("Mee category select cheyyandi");
    if (!/^\d{10}$/.test((f.phone || "").replace(/\D/g, ""))) e.push("10 digit mobile number ivvandi");
    if (!f.city.trim()) e.push("City/town ivvandi");
    if (!f.package) e.push("Package select cheyyandi");
    return e;
  };

  const submit = async () => {
    const e = validate();
    setErrs(e);
    if (e.length) { window.scrollTo({ top: 0, behavior: "smooth" }); return; }
    setBusy(true);
    try {
      const r = await fetch("/api/vendors/register", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...f, phone: f.phone.replace(/\D/g, ""), whatsapp: (f.whatsapp || f.phone).replace(/\D/g, "") }),
      });
      const d = await r.json();
      if (!r.ok || !d.success) setErrs(d.problems || [d.message_telugu || "Register avvaledu — malli try cheyyandi"]);
      else setRes(d);
    } catch {
      setErrs(["Server problem — konchem tarvata malli try cheyyandi"]);
    } finally {
      setBusy(false);
    }
  };

  const selectedPkg = pkgs.find((p) => p.code === f.package);
  const copy = (t: string, k: string) => { navigator.clipboard?.writeText(t); setCopied(k); setTimeout(() => setCopied(""), 1500); };

  /* ---------------- SUCCESS ---------------- */
  if (res) {
    const v = res.vendor;
    return (
      <main className="min-h-screen bg-cream pb-20">
        <section className="maroon-gradient text-white">
          <div className="max-w-3xl mx-auto px-4 py-9 text-center">
            <div className="text-5xl">🎉</div>
            <h1 className="mt-2 text-2xl font-bold">Mee vendor request vachindi!</h1>
            <div className="mt-3 inline-flex flex-wrap items-center gap-2 justify-center bg-white/10 border border-white/25 rounded-2xl px-4 py-3">
              <span className="font-mono text-lg font-bold">{v.id}</span>
              <button onClick={() => copy(v.id, "id")} className="text-[11px] font-bold gold-gradient text-maroon px-3 py-1.5 rounded-full">
                {copied === "id" ? "copied ✓" : "ID copy"}
              </button>
              <span className="text-[12px] opacity-90">{v.business_name} · {v.category_te}</span>
            </div>
          </div>
        </section>

        <div className="max-w-3xl mx-auto px-4 py-6 space-y-4">
          <div className="bg-white rounded-3xl border border-gold/30 p-5">
            <div className="font-bold text-maroon text-[15px]">💰 Ippudu payment cheyyandi — ₹{res.amount}</div>
            <div className="text-[12px] text-gray-600 mt-1">
              Package: <b>{res.package.name}</b> ({res.package.days} days). Payment verify ayagane listing ACTIVE avutundi (2 గంటల్లో).
            </div>
            <ol className="mt-3 space-y-1 text-[12px] text-gray-700 list-decimal list-inside">
              {(res.steps_telugu || []).map((s: string) => <li key={s}>{s.replace(/^\d️⃣\s*/, "")}</li>)}
            </ol>
            <div className="mt-3 flex flex-wrap gap-2">
              {res.phonepe_link && (
                <a href={res.phonepe_link} className="gold-gradient text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                  📱 PhonePe / UPI tho pay cheyyandi
                </a>
              )}
              <button onClick={() => copy(String(res.vendor_id), "ref")}
                className="border border-maroon/25 text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                {copied === "ref" ? "copied ✓" : "📋 Reference copy (payment note lo pettandi)"}
              </button>
            </div>
            {res.upi_id && <div className="mt-2 text-[12px] text-gray-600">UPI ID: <b>{res.upi_id}</b></div>}
          </div>

          <div className="bg-cream border border-gold/40 rounded-3xl p-5">
            <div className="font-bold text-maroon">✅ Payment tarvata em avutundi?</div>
            <ul className="mt-2 space-y-1 text-[12px] text-gray-700">
              <li>1️⃣ Admin verify (2 గంటల్లో) → listing ACTIVE + ✅ Verified badge</li>
              <li>2️⃣ Telugu promo post ready — mee city/caste channel + 4 main channels lo</li>
              <li>3️⃣ QR tho poster (square + status) — mee WhatsApp groups lo pettukondi</li>
              <li>4️⃣ Enquiries direct mee WhatsApp ki + dashboard lo impressions/clicks/leads</li>
            </ul>
            <div className="mt-3 flex flex-wrap gap-2">
              <Link href={`/vendors/${v.id}`} className="maroon-gradient text-white font-bold text-[12px] px-4 py-2.5 rounded-xl">
                📊 Mee vendor page (dashboard)
              </Link>
              <Link href="/vendors" className="border border-maroon/25 text-maroon font-bold text-[12px] px-4 py-2.5 rounded-xl">
                🏪 Vendors directory
              </Link>
            </div>
          </div>
          <div className="text-[11px] text-gray-500 text-center">
            Support: mana WhatsApp number ki screenshot pampandi — reference <b>{v.id}</b>
          </div>
        </div>
      </main>
    );
  }

  /* ---------------- FORM ---------------- */
  return (
    <main className="min-h-screen bg-cream pb-24">
      <section className="maroon-gradient text-white">
        <div className="max-w-3xl mx-auto px-4 py-8">
          <div className="text-[12px] opacity-90 mb-1">
            <Link href="/vendors" className="underline">← Vendors</Link>
          </div>
          <h1 className="text-2xl font-extrabold">🏪 Mee business ni Mana Vivaha lo add cheyyandi</h1>
          <p className="text-[13px] opacity-90 mt-2 telugu">
            Catering, photography, decorations, hall, tent, pandit, jewellery, makeup, DJ, invitations, cars, planner —
            2 nimushalalo register. <b>Enquiries direct mee WhatsApp ki.</b> ₹149 nunchi.
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
            <span className="px-3 py-1 rounded-full bg-white/10">✅ 2 నిమిషాల form</span>
            <span className="px-3 py-1 rounded-full bg-white/10">📢 52 channels + WhatsApp</span>
            <span className="px-3 py-1 rounded-full bg-gold text-maroon font-bold">📞 Leads direct mee number ki</span>
          </div>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-4 py-5 space-y-4">
        {errs.length > 0 && (
          <div className="bg-rose-50 border border-rose-200 rounded-2xl px-4 py-3">
            <div className="font-bold text-rose-800 text-[13px]">Ivi saricheyyali:</div>
            <ul className="mt-1 text-[12px] text-rose-700 list-disc list-inside">
              {errs.slice(0, 6).map((e) => <li key={e}>{e}</li>)}
            </ul>
          </div>
        )}

        {/* CATEGORY */}
        <div className="bg-white rounded-3xl border border-gold/30 p-4">
          <label className="text-[13px] font-bold text-ink">1. Mee category <span className="text-maroon">*</span></label>
          <div className="mt-2 grid grid-cols-2 sm:grid-cols-3 gap-2">
            {cats.map((c) => (
              <button key={c.key} type="button" onClick={() => set("category", c.key)}
                className={`rounded-2xl border-2 p-2.5 text-left text-[12px] font-semibold ${f.category === c.key ? "border-maroon bg-maroon-soft" : "border-gold/30 bg-white"}`}>
                <div className="text-lg">{c.icon}</div>
                <div className="text-maroon">{c.en}</div>
                <div className="text-[10px] text-gray-500 telugu">{c.te}</div>
              </button>
            ))}
          </div>
        </div>

        {/* BUSINESS */}
        <div className="bg-white rounded-3xl border border-gold/30 p-4 space-y-3">
          <div className="text-[13px] font-bold text-ink">2. Business details</div>
          <input className="input-mobile" placeholder="Business peru * (udaharanam: Sri Lakshmi Catering)"
            value={f.business_name} onChange={(e) => set("business_name", e.target.value)} aria-label="Business peru * (udaharanam: Sri Lakshmi Catering)" />
          <div className="grid sm:grid-cols-2 gap-3">
            <input className="input-mobile" placeholder="Owner peru" value={f.owner_name} onChange={(e) => set("owner_name", e.target.value)} aria-label="Owner peru" />
            <input className="input-mobile" placeholder="Experience (years)" value={f.experience_years} onChange={(e) => set("experience_years", e.target.value)} inputMode="numeric" aria-label="Experience (years)" />
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            <input className="input-mobile" placeholder="Mobile number * (10 digits)" value={f.phone}
              onChange={(e) => set("phone", e.target.value)} inputMode="tel" aria-label="Mobile number * (10 digits)" />
            <input className="input-mobile" placeholder="WhatsApp number (veru unte)" value={f.whatsapp}
              onChange={(e) => set("whatsapp", e.target.value)} inputMode="tel" aria-label="WhatsApp number (veru unte)" />
          </div>
          <div className="grid sm:grid-cols-3 gap-3">
            <input className="input-mobile" placeholder="City / town *" value={f.city} onChange={(e) => set("city", e.target.value)} aria-label="City / town *" />
            <input className="input-mobile" placeholder="District" value={f.district} onChange={(e) => set("district", e.target.value)} aria-label="District" />
            <select className="input-mobile" value={f.state} onChange={(e) => set("state", e.target.value)} aria-label="Select option">
              <option value="TS">Telangana</option>
              <option value="AP">Andhra Pradesh</option>
              <option value="KA">Karnataka</option>
              <option value="OTHER">Other</option>
            </select>
          </div>
          <input className="input-mobile" placeholder="Service areas (udaharanam: Warangal, Hanamkonda, Kazipet)"
            value={f.service_areas} onChange={(e) => set("service_areas", e.target.value)} aria-label="Service areas (udaharanam: Warangal, Hanamkonda, Kazipet)" />
          <input className="input-mobile" placeholder="Rate range (udaharanam: ₹250-450 per plate / ₹40,000 nunchi)"
            value={f.price_range} onChange={(e) => set("price_range", e.target.value)} aria-label="Rate range (udaharanam: ₹250-450 per plate / ₹40,000 nunchi)" />
          <textarea className="input-mobile min-h-[90px]" placeholder="Mee business gurinchi 3-4 lines (Telugu/English) — customers ki ide kanipisthundi"
            value={f.about} onChange={(e) => set("about", e.target.value)} aria-label="Text area" />
          <input className="input-mobile" placeholder="Photo/logo URL (optional — tarvata WhatsApp lo pampochu)"
            value={f.photo_url} onChange={(e) => set("photo_url", e.target.value)} aria-label="Photo/logo URL (optional — tarvata WhatsApp lo pampochu)" />
        </div>

        {/* PACKAGE */}
        <div className="bg-white rounded-3xl border border-gold/30 p-4">
          <label className="text-[13px] font-bold text-ink">3. Ad package <span className="text-maroon">*</span></label>
          <div className="mt-2 space-y-2">
            {pkgs.map((p) => (
              <button key={p.code} type="button" onClick={() => set("package", p.code)}
                className={`w-full text-left rounded-2xl border-2 p-3 ${f.package === p.code ? "border-maroon bg-maroon-soft" : "border-gold/30 bg-white"}`}>
                <div className="flex items-center justify-between">
                  <div className="font-bold text-maroon text-[13px]">{p.name} {p.popular ? "🔥" : ""}</div>
                  <div className="font-extrabold text-maroon">₹{p.price} <span className="text-[10px] font-semibold text-gray-500">/ {p.days}d</span></div>
                </div>
                <div className="text-[11px] text-gray-600 mt-0.5">{p.telugu}</div>
                <ul className="mt-1 grid sm:grid-cols-2 gap-x-3 text-[10px] text-gray-600">
                  {(p.perks || []).slice(0, 4).map((x) => <li key={x}>✅ {x}</li>)}
                </ul>
              </button>
            ))}
          </div>
          {selectedPkg && (
            <div className="mt-2 text-[11px] text-emerald-800 bg-emerald-50 border border-emerald-200 rounded-xl px-3 py-2">
              Selected: <b>{selectedPkg.name}</b> — ₹{selectedPkg.price} / {selectedPkg.days} days.
              Payment verify ayagane listing + promo post live.
            </div>
          )}
        </div>

        <div className="bg-cream border border-gold/40 rounded-2xl px-4 py-3 text-[11px] text-gray-700">
          🔒 Mee number public ga kanipisthundi (customers WhatsApp cheyyadaniki) — vere vaallaki ivvamu.
          Fake listings remove chestham. Terms: manavivaha.in/terms
        </div>

        <button onClick={submit} disabled={busy}
          className="w-full maroon-gradient text-white font-bold text-[15px] py-4 rounded-2xl disabled:opacity-60">
          {busy ? "⏳ Submit avutundi…" : "🏪 Vendor request pampandi (free signup)"}
        </button>
      </div>
    </main>
  );
}
