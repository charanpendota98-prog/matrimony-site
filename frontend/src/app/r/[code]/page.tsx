"use client";
/**
 * 🔗 /r/<code> — Referral landing (smart tracking)
 * Click ni API ki pampistundi (funnel), code validate chestundi, referrer peru + bonus chupistundi,
 * tarvata /register?ref=CODE ki redirect (auto-lock + referee bonus credit).
 */
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

export default function ReferralLandingPage() {
  const params = useParams();
  const router = useRouter();
  const code = String(params?.code || "").toUpperCase();
  const [info, setInfo] = useState<any>(null);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    if (!code) return;
    localStorage.setItem("tsap_ref_from_link", code);          // backup (register page kooda chaduvutundi)
    try { sessionStorage.setItem("tsap_click_fired", code); } catch { /* ignore */ }  // 🌊 W20 dedupe
    fetch(`/api/referral/click/${code}?source=link`, { method: "POST" })
      .then((r) => r.json())
      .then((d) => setInfo(d))
      .catch(() => { })
      .finally(() => setChecked(true));
  }, [code]);

  const valid = info?.valid_code;
  const name = info?.referrer_name;

  // valid code ayithe 1.2 sec lo register ki auto-redirect (user experience smooth)
  useEffect(() => {
    if (!checked) return;
    if (valid !== false) {
      const t = setTimeout(() => router.replace(`/register?ref=${code}`), 1600);
      return () => clearTimeout(t);
    }
  }, [checked, valid, code, router]);

  return (
    <main className="min-h-screen bg-[#FFF8E7] flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-[1.5rem] shadow-lg p-6 text-center">
        <div className="w-16 h-16 maroon-gradient rounded-full flex items-center justify-center text-white text-3xl mx-auto">
          {valid === false ? "⚠️" : "🎁"}
        </div>

        {!checked && <div className="mt-4 text-sm text-gray-500">Code check chestunnam…</div>}

        {checked && valid && (
          <>
            <h1 className="mt-4 font-extrabold text-xl text-[#7A0C2E] telugu">
              {name ? `${name} garu` : "Mee friend"} dwara vacharu! 🙏
            </h1>
            <p className="mt-2 text-sm text-gray-600 telugu">
              Code: <b className="text-[#7A0C2E]">{code}</b> — register cheste mee account ki{" "}
              <b className="text-green-700">+{info?.bonus_credits || 1} credit FREE</b> 🎁
            </p>
            <div className="mt-4 rounded-2xl bg-[#FFF8E7] border border-[#D4AF37]/40 p-3 text-left text-[11px] text-[#7A0C2E] space-y-1">
              <div>✅ Modati <b>3 requests FREE</b> (+1 bonus credit mee friend nunchi)</div>
              <div>✅ ₹99 → 5 profiles, ₹199 → 12, ₹299 → 25, ₹499 → 50</div>
              <div>✅ 52 Telegram channels lo mee profile auto-post</div>
              <div>✅ ఫోటో గోప్యం · numbers rendu vaipula ok ayyaka matrame</div>
            </div>
            <a href={`/register?ref=${code}`}
              className="mt-5 block w-full py-3 maroon-gradient text-white rounded-full font-bold text-sm">
              🚀 Register cheyyandi (ref auto-lock)
            </a>
            <div className="text-[11px] text-gray-400 mt-2">2 sec lo automatic ga register page ki veltundi…</div>
          </>
        )}

        {checked && valid === false && (
          <>
            <h1 className="mt-4 font-extrabold text-lg text-[#7A0C2E]">Ee referral code dorakaledu</h1>
            <p className="mt-2 text-sm text-gray-600 telugu">
              Code <b>{code}</b> valid kaadu (leda pedda/chinna letters tappu). Parvaledu — meeru normal ga register avvachu,
              mee sontha referral link kooda automatic ga vastundi.
            </p>
            <a href="/register" className="mt-5 block w-full py-3 maroon-gradient text-white rounded-full font-bold text-sm">
              Register cheyyandi →
            </a>
          </>
        )}

        <div className="mt-4 text-[11px] text-gray-400">
          Mana Vivaha · manavivaha.in · ₹99 ke Sambandham
        </div>
      </div>
    </main>
  );
}
