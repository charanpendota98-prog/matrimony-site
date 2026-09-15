"use client";
/**
 * 🔒 AuthGate — private data 401/403 aithe friendly card (login ki pampistundi).
 * IDOR fix tarvata pages lo ide use chestam (inbox/credits/views/saved).
 */
import Link from "next/link";

export default function AuthGate({ title = "🔒 Mee account ki login cheyyandi", note = "", admin = false }: { title?: string; note?: string; admin?: boolean }) {
  return (
    <div className="rounded-2xl border-2 border-amber-300 bg-amber-50 p-5 text-center">
      <p className="text-lg font-bold text-amber-900">{title}</p>
      <p className="mt-1 text-sm text-amber-800">
        {note || (admin
          ? "Admin console ki X-Admin-Key kavali — /admin lo key pettandi (team nunchi teesukondi)."
          : "Mee phone number tho OTP login cheyyandi — mee data (inbox, credits, shortlist) matrame meeru chudagalaru. Ee security, mee privacy koraku.")}
      </p>
      <div className="mt-3 flex flex-wrap justify-center gap-2">
        <Link href="/login" className="rounded-xl bg-[#7A0C2E] px-4 py-2 text-sm font-semibold text-white hover:bg-[#5c0821]">
          📱 OTP tho login
        </Link>
        <Link href="/register" className="rounded-xl border border-[#7A0C2E] px-4 py-2 text-sm font-semibold text-[#7A0C2E] hover:bg-rose-50">
          🆓 Kotha registration (FREE 3 profiles)
        </Link>
      </div>
      <p className="mt-2 text-xs text-amber-700">
        🔒 Phone numbers eppudu public ga kanipinchavu — interest accept ayithe matrame exchange (consent).
      </p>
    </div>
  );
}
