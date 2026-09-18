"use client";
/**
 * ⭐ WAVE 36 — TOP PICKS (mutual-ranked, boosted-first, gothram/surname/age filtered).
 * Backend /api/top-matches — login unna user ke (owner token).
 */
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet } from "@/lib/api";
import { firstName } from "@/lib/names";
import { useLang } from "@/lib/lang";

type Row = Record<string, any>;

export default function TopPicks() {
  const { lang } = useLang();
  const te = lang === "te";
  const [myId, setMyId] = useState("");
  const [rows, setRows] = useState<Row[]>([]);
  const [mutual, setMutual] = useState(0);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let id = "";
    try { id = localStorage.getItem("tsap_id") || ""; } catch { /* ignore */ }
    if (!id) { setLoaded(true); return; }
    setMyId(id);
    void apiGet<Row>(`/api/top-matches/${encodeURIComponent(id)}?limit=8&min_score=60`).then(({ ok, data }) => {
      setLoaded(true);
      if (ok && data) { setRows(data.results || []); setMutual(data.mutual_matches || 0); }
    });
  }, []);

  if (!loaded) return null;
  if (!myId) {
    return (
      <div className="mb-4 rounded-2xl border border-gold/30 bg-white p-4 text-[13px]">
        <p className="font-bold text-maroon">⭐ {te ? "Top Picks — మీకు ప్రత్యేకంగా (login తో)" : "Top Picks — curated for you (with login)"}</p>
        <p className="mt-1 text-gray-600">
          {te ? "Login చేస్తే mutual score + boosted + గోత్రం/వయసు filter తో best matches ఇక్కడ చూపిస్తాం." : "Login to see best matches ranked by mutual score + boosted + gothram/age filters."}{" "}
          <Link href="/login" className="font-bold text-maroon underline">{te ? "Login" : "Login"}</Link>
        </p>
      </div>
    );
  }
  if (!rows.length) return null;
  return (
    <div className="mb-4 rounded-2xl border border-gold/30 bg-gradient-to-b from-amber-50 to-white p-4">
      <div className="flex items-center gap-2">
        <p className="text-[14px] font-bold text-maroon">⭐ {te ? "Top Picks — మీ best matches" : "Top Picks — your best matches"}</p>
        {mutual > 0 && <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[11px] font-bold text-rose-700">💞 {mutual} mutual</span>}
      </div>
      <div className="mt-3 flex gap-3 overflow-x-auto pb-1">
        {rows.map((r: Row) => (
          <Link key={r.tsap_id} href={`/search/${r.tsap_id}`}
            className="w-[190px] shrink-0 rounded-2xl border border-gold/25 bg-white p-3">
            <div className="flex items-center justify-between">
              <span className="rounded-full bg-[#7A0C2E] px-2 py-0.5 text-[11px] font-bold text-white">{r.score}/100</span>
              {r.boosted ? <span className="text-[11px]">⚡</span> : null}
              {r.has_voice ? <span className="text-[11px]">🎙️</span> : null}
              {r.is_nri ? <span className="text-[11px]">✈️</span> : null}
            </div>
            <p className="mt-1 truncate text-[13px] font-bold">{firstName(r.full_name)} • {r.age}y</p>
            <p className="truncate text-[11px] text-gray-600">{r.caste} • {r.district}</p>
            <p className="font-mono text-[10px] text-gray-400">{r.tsap_id}</p>
            {r.mutual?.both_like ? <p className="mt-1 text-[11px] font-bold text-rose-700">💞 Mutual!</p> : null}
          </Link>
        ))}
      </div>
    </div>
  );
}
