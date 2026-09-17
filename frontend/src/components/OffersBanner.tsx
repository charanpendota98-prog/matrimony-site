"use client";
/**
 * 🎉 WAVE 14 — OFFERS BANNER (homepage strip)
 * Live festival offers → pricing ki link.
 */
import { useEffect, useState } from "react";
import Link from "next/link";

type Offer = { code: string; title: string; pct_off: number; flat_off: number; valid_to?: string };

export default function OffersBanner() {
  const [offers, setOffers] = useState<Offer[]>([]);
  useEffect(() => {
    fetch("/api/offers/active").then((r) => r.json()).then((d) => {
      if (d?.success && Array.isArray(d.offers)) setOffers(d.offers.slice(0, 3));
    }).catch(() => {});
  }, []);
  if (!offers.length) return null;
  return (
    <Link href="/pricing" className="block rounded-2xl bg-gradient-to-r from-[#7A0C2E] via-[#A31633] to-[#E8A020] text-white px-4 py-3 shadow-md hover:shadow-lg transition">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-lg">🎉</span>
        <span className="text-sm font-extrabold">Festival Offers LIVE!</span>
        {offers.map((o) => (
          <span key={o.code} className="text-[11px] font-bold bg-white/20 rounded-full px-2 py-0.5">
            {o.title} • <span className="font-mono">{o.code}</span>
          </span>
        ))}
        <span className="ml-auto text-xs font-bold underline">Plans chudandi →</span>
      </div>
    </Link>
  );
}
