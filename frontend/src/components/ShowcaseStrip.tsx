"use client";
/**
 * 🎊 WEEKLY SHOWCASE STRIP (WAVE 41) — వారానికి ఒక కులం
 * Public homepage strip: ఈ వారం caste + ఆ caste best profiles. Empty → render avvadu.
 */
import { useEffect, useState } from "react";
import { useLang } from "@/lib/lang";

type Row = Record<string, any>;

export default function ShowcaseStrip() {
  const { lang } = useLang();
  const te = lang === "te";
  const [caste, setCaste] = useState("");
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    fetch("/api/showcase").then((r) => r.json()).then((d) => {
      if (d?.success && d.count > 0) { setCaste(d.caste || ""); setRows(d.matches || []); }
    }).catch(() => { });
  }, []);

  if (!rows.length) return null;

  return (
    <section className="max-w-7xl mx-auto px-4 pt-6">
      <div className="rounded-[1.75rem] border border-[#7A0C2E]/15 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="telugu text-lg font-extrabold text-[#7A0C2E]">
            🎊 {te ? `ఈ వారం ${caste} కులస్తుల showcase` : `This week: ${caste} showcase`}
          </h2>
          <span className="telugu rounded-full bg-[#7A0C2E]/8 px-3 py-1 text-[11px] font-bold text-[#7A0C2E]">
            {te ? "వారానికి ఒక కులం — రోజూ కొత్త profiles" : "One caste a week"}
          </span>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-6">
          {rows.slice(0, 6).map((x) => (
            <a key={x.tsap_id} href={`/search/${x.tsap_id}`}
              className="group rounded-2xl border border-[#7A0C2E]/10 bg-gradient-to-br from-white to-[#FFF8E7] p-3 text-center shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
              <div className="mx-auto flex h-[70px] w-[70px] items-center justify-center rounded-full bg-gradient-to-br from-[#7A0C2E]/12 to-[#B8860B]/15 text-3xl">
                {x.gender === "Bride" ? "👰" : "🤵"}
              </div>
              <div className="mt-2 truncate text-[13px] font-bold text-[#7A0C2E]">{x.full_name}</div>
              <div className="telugu truncate text-[11px] text-gray-600">{x.age}y · {x.district}</div>
              <div className="telugu truncate text-[11px] text-gray-500">{x.job || x.education || ""}</div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
