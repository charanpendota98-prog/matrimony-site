"use client";
/**
 * 🦴 Skeleton loaders — text "Loading..." badulu professional shimmer cards.
 * Top matrimony sites lo ide standard — instant perceived speed.
 */
import { useEffect, useRef, useState } from "react";

/** సంఖ్యలు count-up చెయ్యడానికి (52 channels, 43 castes...) — professional touch */
export function useCountUp(target: number, duration = 900): number {
  const [v, setV] = useState(0);
  const started = useRef(false);
  useEffect(() => {
    if (started.current) return;
    started.current = true;
    // prefers-reduced-motion → instant
    try {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setV(target); return; }
    } catch { /* SSR */ }
    const t0 = performance.now();
    let raf = 0;
    const tick = (t: number) => {
      const p = Math.min(1, (t - t0) / duration);
      const eased = 1 - Math.pow(1 - p, 3); // ease-out cubic
      setV(Math.round(target * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return v;
}

/** shimmer bar — skeleton block */
function Bar({ className = "" }: { className?: string }) {
  return <div className={`skeleton-bar ${className}`} />;
}

/** Matches page lo profile card skeleton */
export function CardSkeleton() {
  return (
    <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 flex gap-3">
      <div className="w-20 h-24 rounded-xl shrink-0" aria-hidden>
        <Bar className="w-full h-full rounded-xl" />
      </div>
      <div className="flex-1 min-w-0 space-y-2">
        <Bar className="h-4 w-2/3" />
        <Bar className="h-3 w-1/3" />
        <Bar className="h-3 w-full" />
        <Bar className="h-3 w-5/6" />
        <div className="flex gap-1.5 pt-1">
          <Bar className="h-5 w-14 rounded-full" />
          <Bar className="h-5 w-16 rounded-full" />
          <Bar className="h-5 w-12 rounded-full" />
        </div>
      </div>
    </div>
  );
}

/** List of card skeletons */
export function CardSkeletonList({ n = 4 }: { n?: number }) {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading profiles">
      {Array.from({ length: n }).map((_, i) => <CardSkeleton key={i} />)}
    </div>
  );
}

/** Profile page (search/[id]) lo full skeleton */
export function ProfileSkeleton() {
  return (
    <div className="mt-4 rounded-3xl border border-rose-200 bg-white p-5 space-y-3" aria-busy="true">
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-2 flex-1">
          <Bar className="h-6 w-1/2" />
          <Bar className="h-4 w-1/3" />
        </div>
        <Bar className="h-14 w-14 rounded-full" />
      </div>
      <Bar className="h-3 w-full" />
      <Bar className="h-3 w-11/12" />
      <Bar className="h-3 w-4/5" />
      <div className="flex gap-2 pt-2">
        <Bar className="h-9 w-24 rounded-xl" />
        <Bar className="h-9 w-24 rounded-xl" />
      </div>
    </div>
  );
}
