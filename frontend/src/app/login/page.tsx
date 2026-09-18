"use client";
/**
 * 🔑 WAVE 18 — Login: Number+Password (default) | OTP | Forgot password (OTP reset) + demo.
 */
import { useState } from "react";
import Link from "next/link";
import { Duo } from "@/lib/duo";
import { useLang } from "@/lib/lang";
import { useRouter } from "next/navigation";
import { rememberSession, sendOtp, verifyOtp } from "@/lib/auth";
import { apiPost } from "@/lib/api";


export default function LoginPage() {
  const router = useRouter();
  const { lang } = useLang();
  const te = lang === "te";
  const [tab, setTab] = useState<"password" | "otp">("password");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [code, setCode] = useState("");
  const [stage, setStage] = useState<"phone" | "otp">("phone");
  const [msg, setMsg] = useState("");
  const [devCode, setDevCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [keep, setKeep] = useState(true);
  // forgot flow
  const [forgot, setForgot] = useState(false);
  const [fStage, setFStage] = useState<"phone" | "reset">("phone");
  const [newPw, setNewPw] = useState("");

  const digits = () => phone.replace(/\D/g, "");
  const go = (tsapId: string, token: string, hasAccount: boolean) => {
    rememberSession(tsapId, token, keep);
    setTimeout(() => router.push(hasAccount ? "/requests" : "/register?phone=" + digits()), 700);
  };

  async function onPasswordLogin() {
    if (digits().length !== 10) { setMsg(te ? "⚠️ 10 digit mobile number ఇవ్వండి" : "⚠️ Enter a 10-digit mobile number"); return; }
    if (!password) { setMsg(te ? "⚠️ Password ఇవ్వండి (లేదా OTP tab వాడండి)" : "⚠️ Enter password (or use the OTP tab)"); return; }
    setBusy(true); setMsg("");
    const { ok, data, errorTelugu } = await apiPost<{ auth_token?: string; tsap_id?: string; message_telugu?: string }>(
      "/api/auth/login-password", { phone: digits(), password });
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    setMsg(data?.message_telugu || (te ? "✅ Login అయ్యింది" : "✅ Logged in"));
    go(String(data?.tsap_id || ""), String(data?.auth_token || ""), true);
  }

  async function onSend() {
    setBusy(true); setMsg("");
    if (digits().length !== 10) { setMsg(te ? "⚠️ 10 digit mobile number ఇవ్వండి (6/7/8/9 తో start)" : "⚠️ Enter a 10-digit mobile number (starting 6/7/8/9)"); setBusy(false); return; }
    const { ok, data, errorTelugu } = await sendOtp(digits());
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    const d = (data || {}) as { dev_code?: string; message_telugu?: string };
    setStage("otp");
    setDevCode(d.dev_code || "");
    setMsg(d.message_telugu || (te ? "📱 OTP పంపించాం — 10 నిమిషాల్లో enter చెయ్యండి" : "📱 OTP sent — enter within 10 minutes"));
  }

  async function onVerify() {
    setBusy(true); setMsg("");
    const { ok, data, errorTelugu } = await verifyOtp(digits(), code.trim());
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    const d = (data || {}) as { auth_token?: string; tsap_id?: string; has_account?: boolean; message_telugu?: string };
    setMsg(d.message_telugu || (te ? "✅ Login అయ్యింది" : "✅ Logged in"));
    go(String(d.tsap_id || ""), String(d.auth_token || ""), !!d.has_account);
  }

  async function onForgotSend() {
    setBusy(true); setMsg("");
    if (digits().length !== 10) { setMsg(te ? "⚠️ 10 digit mobile number ఇవ్వండి" : "⚠️ Enter a 10-digit mobile number"); setBusy(false); return; }
    const { ok, data, errorTelugu } = await apiPost<{ dev_code?: string; message_telugu?: string }>(
      "/api/auth/forgot", { phone: digits() });
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    setFStage("reset");
    setDevCode((data as { dev_code?: string })?.dev_code || "");
    setMsg(data?.message_telugu || (te ? "📱 Reset OTP పంపించాం" : "📱 Reset OTP sent"));
  }

  async function onReset() {
    if (newPw.trim().length < 6) { setMsg(te ? "⚠️ కొత్త password minimum 6 characters" : "⚠️ New password: minimum 6 characters"); return; }
    setBusy(true); setMsg("");
    const { ok, data, errorTelugu } = await apiPost<{ auth_token?: string; tsap_id?: string; message_telugu?: string }>(
      "/api/auth/reset", { phone: digits(), code: code.trim(), new_password: newPw.trim() });
    setBusy(false);
    if (!ok) { setMsg(errorTelugu); return; }
    setMsg(data?.message_telugu || (te ? "✅ Password మార్చింది" : "✅ Password changed"));
    go(String(data?.tsap_id || ""), String(data?.auth_token || ""), true);
  }

  return (
    <main className="mx-auto max-w-md px-4 py-10">
      <h1 className="text-2xl font-extrabold text-[#7A0C2E]">🔑 <Duo en="Member Login" te="సభ్యుల లాగిన్" /></h1>
      <p className="mt-1 text-sm text-slate-600">
        {te ? "🔒 మీ inbox, credits, shortlist — ఈ data మీరు మాత్రమే చూడగలరు, safe గా ఉంటుంది." : "🔒 Your inbox, credits, shortlist — only you can see this data, kept safe."}
      </p>

      <section className="mt-6 rounded-2xl border-2 border-rose-200 bg-rose-50/60 p-4">
        <div className="flex gap-2">
          {(["password", "otp"] as const).map((t) => (
            <button key={t} onClick={() => { setTab(t); setMsg(""); setForgot(false); }}
              className={`flex-1 rounded-xl py-2.5 text-sm font-bold ${tab === t ? "maroon-gradient text-white" : "bg-white border border-rose-200 text-maroon"}`}>
              {t === "password" ? "🔑 Password" : "📱 OTP"}
            </button>
          ))}
        </div>

        <label htmlFor="phone" className="mt-4 block text-sm font-semibold text-slate-700">{te ? "📞 మొబైల్ నంబర్ (10 digits)" : "📞 Mobile number (10 digits)"}</label>
        <input id="phone" inputMode="numeric" autoComplete="tel" value={phone} maxLength={13}
          onChange={(e) => setPhone(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") void (tab === "password" && !forgot ? onPasswordLogin() : tab === "otp" && stage === "phone" ? onSend() : onVerify()); }}
          placeholder="98480 12345"
          className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-lg tracking-wide focus:border-[#7A0C2E] focus:outline-none" />

        {tab === "password" && !forgot ? (
          <>
            <label htmlFor="pw" className="mt-3 block text-sm font-semibold text-slate-700">🔑 Password</label>
            <div className="relative">
              <input id="pw" type={showPw ? "text" : "password"} value={password} autoComplete="current-password"
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") void onPasswordLogin(); }}
                placeholder={te ? "మీ password" : "Your password"}
                className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-lg pr-16 focus:border-[#7A0C2E] focus:outline-none" />
              <button onClick={() => setShowPw(!showPw)} className="absolute right-2 top-1/2 -translate-y-1/2 text-[12px] font-bold text-maroon px-2">
                {showPw ? "🙈" : "👁️"}
              </button>
            </div>
            <button onClick={() => { setForgot(true); setFStage("phone"); setCode(""); setMsg(""); }}
              className="mt-2 text-[13px] font-bold text-maroon underline">
              <Duo en="Forgot password? Reset with OTP" te="పాస్‌వర్డ్ మర్చిపోయారా? OTP తో రీసెట్" />
            </button>
          </>
        ) : null}

        {forgot ? (
          <>
            {fStage === "reset" ? (
              <>
                <label htmlFor="fotp" className="mt-3 block text-sm font-semibold text-slate-700">🔢 Reset OTP</label>
                <input id="fotp" inputMode="numeric" value={code} maxLength={6}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="1234"
                  className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-center text-2xl tracking-[0.4em] focus:border-[#7A0C2E] focus:outline-none" />
                <label htmlFor="npw" className="mt-3 block text-sm font-semibold text-slate-700">{te ? "🔑 కొత్త password (min 6)" : "🔑 New password (min 6)"}</label>
                <input id="npw" type={showPw ? "text" : "password"} value={newPw} autoComplete="new-password"
                  onChange={(e) => setNewPw(e.target.value)}
                  placeholder={te ? "కొత్త password" : "New password"}
                  className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-lg focus:border-[#7A0C2E] focus:outline-none" />
              </>
            ) : null}
            {devCode && fStage === "reset" ? <p className="mt-1 text-xs text-emerald-700">{te ? <>మీ OTP: <b>{devCode}</b></> : <>Your OTP: <b>{devCode}</b></>}</p> : null}
          </>
        ) : tab === "otp" && stage === "otp" ? (
          <>
            <label htmlFor="otp" className="mt-3 block text-sm font-semibold text-slate-700">🔢 4-digit OTP</label>
            <input id="otp" inputMode="numeric" value={code} maxLength={6}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") void onVerify(); }}
              placeholder="1234"
              className="mt-1 w-full rounded-xl border border-rose-300 px-3 py-2 text-center text-2xl tracking-[0.4em] focus:border-[#7A0C2E] focus:outline-none" />
            {devCode && <p className="mt-1 text-xs text-emerald-700">{te ? <>మీ OTP: <b>{devCode}</b></> : <>Your OTP: <b>{devCode}</b></>}</p>}
          </>
        ) : null}

        <label className="mt-3 flex items-center gap-2 text-sm font-medium text-slate-700 cursor-pointer">
          <input type="checkbox" checked={keep} onChange={(e) => setKeep(e.target.checked)}
            className="w-4 h-4 accent-[#7A0C2E]" />
          ✅ <Duo en="Keep me logged in" te="లాగిన్‌లోనే ఉంచండి" />
        </label>
        <p aria-live="polite" className="mt-2 min-h-[1.25rem] text-sm font-medium text-[#7A0C2E]">{msg}</p>
        <div className="mt-3 flex gap-2">
          {forgot ? (
            <>
              {fStage === "phone" ? (
                <button onClick={onForgotSend} disabled={busy}
                  className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
                  {busy ? "…" : te ? "📩 Reset OTP పంపు" : "📩 Send reset OTP"}
                </button>
              ) : (
                <button onClick={onReset} disabled={busy}
                  className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
                  {busy ? "…" : te ? "✅ Password మార్చు + Login" : "✅ Change password + Login"}
                </button>
              )}
              <button onClick={() => { setForgot(false); setCode(""); setNewPw(""); }} className="rounded-xl border border-slate-300 px-3 py-3 text-sm">
                ← Back
              </button>
            </>
          ) : tab === "password" ? (
            <button onClick={onPasswordLogin} disabled={busy}
              className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
              {busy ? "…" : "🔑 Login"}
            </button>
          ) : stage === "phone" ? (
            <button onClick={onSend} disabled={busy}
              className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
              {busy ? "…" : te ? "📩 OTP పంపు" : "📩 Send OTP"}
            </button>
          ) : (
            <>
              <button onClick={onVerify} disabled={busy}
                className="flex-1 rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white hover:bg-[#5c0821] disabled:opacity-50">
                {busy ? "…" : "✅ Verify + Login"}
              </button>
              <button onClick={() => { setStage("phone"); setCode(""); setDevCode(""); }} className="rounded-xl border border-slate-300 px-3 py-3 text-sm">
                {te ? "↺ Number మార్చు" : "↺ Change number"}
              </button>
            </>
          )}
        </div>
      </section>

      <p className="mt-5 text-center text-sm text-slate-600">
        {te ? <>Account లేదా? <Link href="/register" className="font-semibold text-[#7A0C2E] underline">Register FREE</Link> — 3 profiles చూడొచ్చు, numbers 🔒 (consent తోనే)</> : <>No account? <Link href="/register" className="font-semibold text-[#7A0C2E] underline">Register FREE</Link> — see 3 profiles, numbers 🔒 (only with consent)</>}
      </p>
    </main>
  );
}
