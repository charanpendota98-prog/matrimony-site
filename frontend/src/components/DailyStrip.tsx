"use client";
/**
 * 🗓️ DAILY MATCHES STRIP (WAVE 40) — "ఈ రోజు మ్యాచ్‌లు"
 * Admin select chesina featured profiles — homepage lo horizontal cards.
 * Empty ayithe render avvadu (khali ga kanipinchadu).
 */
import { useEffect, useState } from "react";
import { useLang } from "@/lib/lang";

type Row = Record<string, any>;

export default function DailyStrip() {
  const { lang } = useLang();
  const te = lang === "te";
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    fetch("/api/daily-matches").then((r) => r.json()).then((d) => {
      if (d?.success && d.count > 0) setRows(d.matches || []);
    }).catch(() => { });
  }, []);

  if (!rows.length) return null;

  return (
    <section className="max-w-7xl mx-auto px-4 pt-6">
      <div className="rounded-[1.75rem] border border-[#B8860B]/30 bg-gradient-to-br from-[#FFF8E7] to-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="telugu text-lg font-extrabold text-[#7A0C2E]">
            🗓️ {te ? "ఈ రోజు మ్యాచ్‌లు — ఎంపిక profiles" : "Today&apos;s Matches — featured"}
          </h2>
          <span className="rounded-full bg-[#B8860B]/15 px-3 py-1 text-[11px] font-bold text-[#8B6914]">
            ⚡ {te ? "Boost తో మీ profile కూడా ఇక్కడ" : "Your profile here with Boost"}
          </span>
        </div>
        <div className="mt-4 flex gap-3 overflow-x-auto pb-2" style={{ scrollbarWidth: "thin" }}>
          {rows.map((x) => (
            <a key={x.tsap_id} href={`/search/${x.tsap_id}`}
              className="group w-[168px] flex-shrink-0 rounded-2xl border border-[#7A0C2E]/10 bg-white p-3 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
              <div className="flex h-[86px] items-center justify-center rounded-xl bg-gradient-to-br from-[#7A0C2E]/10 to-[#B8860B]/10 text-3xl">
                {x.gender === "Bride" ? "👰" : "🤵"}
              </div>
              <div className="mt-2 truncate text-sm font-bold text-[#7A0C2E]">{x.full_name}</div>
              <div className="telugu truncate text-[11px] text-gray-600">{x.age}y · {x.caste}</div>
              <div className="telugu truncate text-[11px] text-gray-500">{x.district} · {x.job || x.education || ""}</div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
