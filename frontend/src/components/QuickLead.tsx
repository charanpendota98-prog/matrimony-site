"use client";

/**
 * QUICK LEAD — phone-first entry point (mass adoption + lead capture)
 * ==================================================================
 * "Register form 55 fields" ani bhaya padakunda — 30 seconds lo number iste,
 * mana team call chesi profile FREE ga complete chestundi.
 * Ee data antha DB lo save avutundi (lead capture — growth engine).
 */
import { useEffect, useState } from "react";
import { DISTRICTS_BY_STATE } from "@/lib/telugu-data";

const HIDE_KEY = "tsap_quicklead_done";

export default function QuickLead({ source = "site", compact = false }: { source?: string; compact?: boolean }) {
  const [open, setOpen] = useState(false);
  const [done, setDone] = useState(false);
  const [hidden, setHidden] = useState(false);   // SSR lo kanipisthundi (promo bar); done aithe client hide chestundi
  const [form, setForm] = useState({ name: "", phone: "", gender: "Bride", district: "", state: "TS", caste: "" });
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setHidden(localStorage.getItem(HIDE_KEY) === "1");
  }, []);

  if (hidden && !done) return null;

  const submit = async () => {
    if (!/^\d{10}$/.test(form.phone)) {
      setMsg({ ok: false, text: "10 digit mobile number ivvandi" });
      return;
    }
    setBusy(true);
    try {
      const r = await fetch("/api/leads/quick", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source }),
      });
      const d = await r.json();
      if (r.ok && d.success) {
        setMsg({ ok: true, text: d.message_telugu });
        setDone(true);
        localStorage.setItem(HIDE_KEY, "1");
      } else {
        setMsg({ ok: false, text: d.detail || "Save avvaledu — malli try cheyyandi" });
      }
    } catch {
      setMsg({ ok: false, text: "Network problem — malli try cheyyandi" });
    }
    setBusy(false);
  };

  if (done) {
    return (
      <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
        <div className="font-bold text-emerald-900 text-[14px]">✅ Number save ayyindi!</div>
        <div className="text-[12px] text-emerald-800 mt-1 telugu">{msg?.text}</div>
        <div className="text-[11px] text-emerald-700 mt-2">
          ⚡ Fast ga kavali antе ippude{" "}
          <a href="/register" className="underline font-bold">3-nimushala register</a> cheyyandi — profile + card ventane ready.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-[#7A0C2E] to-[#A0143A] rounded-2xl p-4 text-white">
      {!open ? (
        <div className="flex items-center gap-3">
          <div className="text-2xl">📱</div>
          <div className="flex-1 min-w-0">
            <div className="font-bold text-[14px]">Form fill cheyyadaniki time leda?</div>
            <div className="text-[11px] opacity-90 telugu">Number pettu — mana team call chesi profile FREE ga complete chestundi (2 nimushalu)</div>
          </div>
          <button onClick={() => setOpen(true)} className="shrink-0 gold-gradient text-maroon font-bold text-[13px] px-4 py-2.5 rounded-xl">
            Start
          </button>
        </div>
      ) : (
        <div className="space-y-2.5">
          <div className="flex items-center justify-between">
            <div className="font-bold text-[14px]">📱 30 seconds lo start</div>
            <button onClick={() => setOpen(false)} className="text-[12px] opacity-80">✕</button>
          </div>
          <input value={form.phone} inputMode="tel" placeholder="WhatsApp number (10 digit) *"
            onChange={(e) => setForm({ ...form, phone: e.target.value.replace(/\D/g, "").slice(0, 10) })}
            className="input-mobile !bg-white/95" />
          <input value={form.name} placeholder="Mee peru (optional)"
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="input-mobile !bg-white/95" />
          <div className="flex gap-2">
            {["Bride", "Groom"].map((g) => (
              <button key={g} onClick={() => setForm({ ...form, gender: g })}
                className={`chip flex-1 justify-center ${form.gender === g ? "chip-on-gold" : "!bg-white/95 !text-maroon"}`}>
                {g === "Bride" ? "👰 Bride" : "🤵 Groom"}
              </button>
            ))}
          </div>
          {!compact && (
            <div className="flex gap-2">
              <select value={form.state} onChange={(e) => setForm({ ...form, state: e.target.value, district: "" })}
                className="input-mobile !bg-white/95 !text-maroon">
                <option value="TS">Telangana</option><option value="AP">Andhra Pradesh</option>
              </select>
              <select value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })}
                className="input-mobile !bg-white/95 !text-maroon">
                <option value="">District (optional)</option>
                {(DISTRICTS_BY_STATE[form.state] || []).map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
          )}
          <button onClick={submit} disabled={busy}
            className="w-full py-3.5 rounded-2xl gold-gradient text-maroon font-bold text-[15px] disabled:opacity-60">
            {busy ? "Save avutund…" : "✅ Callback teesukondi (FREE)"}
          </button>
          {msg && <div className={`text-[12px] ${msg.ok ? "text-emerald-200" : "text-amber-200"}`}>{msg.text}</div>}
          <div className="text-[10px] opacity-80">🔒 Number evariki share avvadu • 🚫 Chatting ledu • ⚠️ Advance money adigithe report cheyyandi</div>
        </div>
      )}
    </div>
  );
}
