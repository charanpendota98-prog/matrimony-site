"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { SITE_CONFIG } from "@/lib/site-config";
import { useLang } from "@/lib/lang";

/**
 * Mobile sticky bottom bar — Register + Bot.
 * /register page lo chupinchadu (form fill chesthunnappudu distraction oddu).
 */
export default function StickyCTA() {
  const pathname = usePathname();
  const [show, setShow] = useState(false);
  const { lang } = useLang();

  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 420);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (!SITE_CONFIG.features.showStickyCta) return null;
  if (pathname?.startsWith("/register")) return null;

  return (
    <div
      className={`lg:hidden fixed bottom-3 left-3 right-3 z-40 no-print transition-all duration-300 ${
        show ? "translate-y-0 opacity-100" : "translate-y-24 opacity-0 pointer-events-none"
      }`}
    >
      <div className="glass border border-gold/40 rounded-2xl shadow-brandLg p-2 flex gap-2">
        <Link
          href="/register"
          className="flex-1 text-center py-3 rounded-xl maroon-gradient text-white text-sm font-bold"
        >
          {lang === "te" ? "ఉచిత నమోదు" : "Register FREE"}
        </Link>
        <a
          href={SITE_CONFIG.officialChannelUrl}
          target="_blank"
          rel="noreferrer"
          className="flex-1 text-center py-3 rounded-xl gold-gradient text-maroon text-sm font-bold"
        >
          {lang === "te" ? "టెలిగ్రామ్ ఛానల్" : "Telegram Channel"}
        </a>
      </div>
    </div>
  );
}
