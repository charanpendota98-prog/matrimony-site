"use client";
import { useLang } from "@/lib/lang";
/** ⭐ Trust + completeness badge (matches/search pages lo) */
export type TrustInfo = { score?: number; level?: string; badge_telugu?: string; next_steps_telugu?: string[] };

export default function TrustBadge({ trust, completeness, compact = false }: { trust?: TrustInfo | null; completeness?: number; compact?: boolean }) {
  const { lang } = useLang();
  const te = lang === "te";
  const score = Math.max(0, Math.min(100, Number(trust?.score ?? 0)));
  const tone = score >= 80 ? "bg-emerald-100 text-emerald-800 border-emerald-300"
    : score >= 60 ? "bg-sky-100 text-sky-800 border-sky-300"
    : score >= 35 ? "bg-amber-100 text-amber-800 border-amber-300"
    : "bg-slate-100 text-slate-700 border-slate-300";
  const icon = score >= 80 ? "🥇" : score >= 60 ? "🥈" : score >= 35 ? "🥉" : "🆕";
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-semibold ${tone}`}
      title={trust?.badge_telugu || (te ? "Trust score — verify + complete profile తో పెరుగుతుంది" : "Trust score — grows as you verify + complete your profile")}>
      {icon} {te ? "నమ్మకం" : "Trust"} {score}
      {typeof completeness === "number" && <span className="opacity-80">· {completeness}% {te ? "పూర్తి" : "complete"}</span>}
      {!compact && trust?.next_steps_telugu?.[0] && <span className="hidden sm:inline opacity-80">· {trust.next_steps_telugu[0]}</span>}
    </span>
  );
}
