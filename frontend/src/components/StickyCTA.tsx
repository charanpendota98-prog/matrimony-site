"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useLang } from "@/lib/lang";

/** Mobile app navigation — always reachable, thumb-friendly, safe-area aware. */
const ITEMS = [
  { href: "/", icon: "⌂", te: "హోమ్", en: "Home" },
  { href: "/matches", icon: "⌕", te: "వెతుకు", en: "Search" },
  { href: "/matches?mode=daily", icon: "♡", te: "మ్యాచ్‌లు", en: "Matches" },
  { href: "/requests", icon: "✉", te: "రిక్వెస్ట్‌లు", en: "Requests" },
  { href: "/me", icon: "♙", te: "నేను", en: "Me" },
] as const;

export default function StickyCTA() {
  const pathname = usePathname();
  const [dailyMode, setDailyMode] = useState(false);
  const { lang } = useLang();
  useEffect(() => setDailyMode(new URLSearchParams(window.location.search).get("mode") === "daily"), [pathname]);
  if (pathname?.startsWith("/register")) return null;

  return (
    <nav className="mobile-bottom-nav no-print lg:hidden" aria-label={lang === "te" ? "మొబైల్ నావిగేషన్" : "Mobile navigation"}>
      <div className="mx-auto flex h-[64px] max-w-lg items-stretch px-1">
        {ITEMS.map((item, index) => {
          const active = item.href === "/"
            ? pathname === "/"
            : index === 1
              ? pathname === "/matches" && !dailyMode
              : index === 2
                ? pathname === "/matches" && dailyMode
                : pathname?.startsWith(item.href.split("?")[0]);
          return (
            <Link key={item.href} href={item.href} onClick={() => { if (index === 1) setDailyMode(false); if (index === 2) setDailyMode(true); }} className={`nav-tab focus-brand ${active ? "nav-tab-on" : ""}`} aria-current={active ? "page" : undefined}>
              <span className={`nav-tab-icon ${active ? "nav-tab-icon-on" : ""}`} aria-hidden="true">{item.icon}</span>
              <span className="telugu leading-none">{lang === "te" ? item.te : item.en}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
