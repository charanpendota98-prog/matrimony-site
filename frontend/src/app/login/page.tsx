"use client";
/** 📱 Login — phone OTP (real users) + demo login (seed profiles) */
import { useState } from "react";
import Link from "next/link";
import { Duo, duo } from "@/lib/duo";
import { useRouter } from "next/navigation";
import { demoLogin, rememberSession, sendOtp, verifyOtp } from "@/lib/auth";
import { readLocal } from "@/lib/api";

type Profile = { tsap_id?: string; full_name?: string };

export default function LoginPage() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [stage, setStage] = useState<"phone" | "otp">("phone");
  const [msg, setMsg] = useState("");
  const [devCode, setDevCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [demoId, setDemoId] = useState("");
  const myProfiles = readLocal<Profile[]>("tsap_profiles", []);

  async function onSend() {
    setBusy(true); setMsg("");
    const digits = phone.replace(/\D/g, "");
    if (digits.length !== 10) { setMsg("⚠️ 10 digit mobile number ivvandi (6/7/8/9 tho start)"); setBusy(false); return; }
    const { ok, data, errorTelugu } = await sendOtp(digits);
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    const d = (data || {}) as { dev_code?: string; message_telugu?: string };
    setStage("otp");
    setDevCode(d.dev_code || "");
    setMsg(d.message_telugu || "📱 OTP pampinchaam — 10 nimushalalo enter cheyyandi");
  }

  async function onVerify() {
    setBusy(true); setMsg("");
    const digits = phone.replace(/\D/g, "");
    const { ok, data, errorTelugu } = await verifyOtp(digits, code.trim());
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    const d = (data || {}) as { auth_token?: string; tsap_id?: string; has_account?: boolean; message_telugu?: string };
    rememberSession(String(d.tsap_id || ""), String(d.auth_token || ""));
    setMsg(d.message_telugu || "✅ Login ayyindi");
    if (d.has_account) setTimeout(() => router.push("/requests"), 700);
    else setTimeout(() => router.push("/register?phone=" + digits), 700);
  }

  async function onDemo() {
    const id = (demoId || "").trim().toUpperCase();
    if (!id) { setMsg("⚠️ Demo TSAP ID ivvandi (example: TSAP-F-2025-1042)"); return; }
    setBusy(true); setMsg("");
    const { ok, data, errorTelugu } = await demoLogin(id);
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    const d = (data || {}) as { auth_token?: string; message_telugu?: string };
    rememberSession(id, String(d.auth_token || ""));
    setMsg(d.message_telugu || "🎬 Demo login ayyindi");
    setTimeout(() => router.push("/matches"), 700);
  }

  return (
    <main className="mx-auto max-w-md px-4 py-10">
      <h1 className="text-2xl font-extrabold text-[#7A0C2E]">📱 <Duo en="Login — with your number" te="మీ నంబర్‌తో లాగిన్" /></h1>
      <p className="mt-1 text-sm text-slate-600">
        🔒 Mee inbox, credits, shortlist — ee data meeru matrame chudagalaru (token tho protect chesam).
      </p>

      <section className="mt-6 rounded-2xl border-2 border-rose-200 bg-rose-50/60 p-4">
        <label htmlFor="phone" className="block text-sm font-semibold text-slate-700">📞 Mobile number (10 digits)</label>
        <input id="phone" inputMode="numeric" autoComplete="tel" value={phone} maxLength={13}
          onChange={(e) => setPhone(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && stage === "phone") void onSend(); }}
          placeholder="98480 12345"
          className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-lg tracking-wide focus:border-[#7A0C2E] focus:outline-none" />
        {stage === "otp" && (
          <>
            <label htmlFor="otp" className="mt-3 block text-sm font-semibold text-slate-700">🔢 4-digit OTP</label>
            <input id="otp" inputMode="numeric" value={code} maxLength={6}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") void onVerify(); }}
              placeholder="1234"
              className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-center text-2xl tracking-[0.4em] focus:border-[#7A0C2E] focus:outline-none" />
            {devCode && <p className="mt-1 text-xs text-emerald-700">DEV MODE OTP: <b>{devCode}</b> (SMS provider configure cheyyaka)</p>}
          </>
        )}
        <p aria-live="polite" className="mt-3 min-h-[1.25rem] text-sm font-medium text-[#7A0C2E]">{msg}</p>
        <div className="mt-3 flex gap-2">
          {stage === "phone" ? (
            <button onClick={onSend} disabled={busy}
              className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
              {busy ? "…" : "📩 OTP pampu"}
            </button>
          ) : (
            <>
              <button onClick={onVerify} disabled={busy}
                className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
                {busy ? "…" : "✅ Verify + Login"}
              </button>
              <button onClick={() => { setStage("phone"); setCode(""); setDevCode(""); }} className="rounded-xl border border-slate-300 px-3 py-3 text-sm">
                ↺ Number marchu
              </button>
            </>
          )}
        </div>
      </section>

      <section className="mt-5 rounded-2xl border border-slate-200 bg-white p-4">
        <h2 className="text-sm font-bold text-slate-800">🎬 <Duo en="Demo login (preview / testing)" te="డెమో లాగిన్" /></h2>
        <p className="text-xs text-slate-500">Demo profile ID tho login — real users ki phone OTP eh.</p>
        <div className="mt-2 flex gap-2">
          <input value={demoId} onChange={(e) => setDemoId(e.target.value.toUpperCase())}
            placeholder="TSAP-F-2025-1042" aria-label="Demo TSAP ID"
            className="flex-1 rounded-xl border border-slate-300 px-3 py-2 text-sm focus:border-[#7A0C2E] focus:outline-none" />
          <button onClick={onDemo} disabled={busy} className="rounded-xl border border-[#7A0C2E] px-3 py-2 text-sm font-semibold text-[#7A0C2E] disabled:opacity-50">
            🎬 Enter
          </button>
        </div>
        {myProfiles.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {myProfiles.slice(0, 6).map((p) => (
              <button key={p.tsap_id} onClick={() => { setDemoId(String(p.tsap_id || "")); void onDemo(); }}
                className="rounded-full bg-slate-100 px-2 py-1 text-[11px] hover:bg-slate-200">
                {p.full_name || p.tsap_id}
              </button>
            ))}
          </div>
        )}
      </section>

      <p className="mt-5 text-center text-sm text-slate-600">
        Account leda? <Link href="/register" className="font-semibold text-[#7A0C2E] underline">Register FREE</Link> — 3 profiles chudochu, numbers 🔒 (consent tho matrame)
      </p>
    </main>
  );
}
