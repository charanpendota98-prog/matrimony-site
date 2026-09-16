"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { CHANNEL_STATS } from "@/lib/channels";
import { SITE_CONFIG } from "@/lib/site-config";
import { useSession, logout } from "@/lib/auth";
import { apiGet } from "@/lib/api";
import { Duo, duo } from "@/lib/duo";

const NAV: { href: string; en: string; te: string; icon: string; xl?: boolean }[] = [
  { href: "/", en: "Home", te: "హోమ్", icon: "🏠" },
  { href: "/channels", en: "Channels", te: "ఛానళ్లు", icon: "📢" },
  { href: "/pricing", en: "Pricing", te: "ధరలు", icon: "💰" },
  { href: "/vendors", en: "Vendors", te: "వెండర్లు", icon: "🏪" },
  { href: "/porutham", en: "Porutham", te: "పొరుతం", icon: "💍", xl: true },
  { href: "/safety", en: "Safety", te: "భద్రత", icon: "🛡️", xl: true },
  { href: "/requests", en: "Requests", te: "రిక్వెస్టులు", icon: "💌" },
  { href: "/growth", en: "Growth", te: "గ్రోత్", icon: "📈" },
  { href: "/castes", en: "Castes", te: "కులాలు", icon: "🪔" },
  { href: "/matches", en: "Matches", te: "సంబంధాలు", icon: "💘" },
  { href: "/stories", en: "Stories", te: "కథలు", icon: "💑" },
  { href: "/referral", en: "Referral", te: "రెఫరల్", icon: "🤝" },
  { href: "/bureau", en: "Bureau", te: "బ్యూరో", icon: "🏛️" },
  { href: "/admin", en: "Admin", te: "అడ్మిన్", icon: "🔐" },
];

export default function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  // 🔐 WAVE 13 — persistent session chip (login ayithe eppudu kanipisthundi)
  const { tsapId, token, ready } = useSession();
  const [sessionOk, setSessionOk] = useState(false);
  useEffect(() => {
    if (!ready || !token) { setSessionOk(false); return; }
    apiGet<{ valid?: boolean }>("/api/auth/verify").then(({ ok, data }) =>
      setSessionOk(!!(ok && (data as { valid?: boolean } | null)?.valid)));
  }, [ready, token]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header
      className={`sticky top-0 z-50 no-print border-b transition-all duration-300 ${
        scrolled ? "glass border-gold/30 shadow-soft" : "bg-cream border-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-3">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 min-w-0 focus-brand rounded-xl">
          <div className="w-10 h-10 maroon-gradient rounded-xl flex items-center justify-center text-gold font-bold text-lg shadow-gold shrink-0">
            {SITE_CONFIG.logoText}
          </div>
          <div className="min-w-0">
            <div className="font-bold text-maroon leading-none truncate">{SITE_CONFIG.brandName}</div>
            <div className="text-[10px] text-gray-500 telugu leading-tight truncate">
              {SITE_CONFIG.legalName} • {SITE_CONFIG.taglineTelugu}
            </div>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center gap-1">
          {NAV.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              title={duo(n.en, n.te)}
              className={`${n.xl ? "hidden xl:inline-flex" : ""} px-3.5 py-2 rounded-full text-[13px] font-semibold transition ${
                isActive(n.href)
                  ? "bg-maroon text-white shadow-soft"
                  : "text-ink/75 hover:text-maroon hover:bg-maroon-soft"
              }`}
            >
              {n.icon} {n.en}
            </Link>
          ))}
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-2">
          <Link
            href="/search/TSAP-M-2025-1042"
            className="hidden md:inline-flex px-3.5 py-2 text-[13px] font-semibold border border-maroon/30 text-maroon rounded-full hover:bg-maroon-soft transition"
          >
            <Duo en="ID Search" te="వెతకండి" />
          </Link>
          {ready && tsapId && sessionOk ? (
            <span className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 text-[13px] font-semibold border border-emerald-300 bg-emerald-50 text-emerald-800 rounded-full">
              👤 {tsapId.length > 14 ? `${tsapId.slice(0, 9)}…${tsapId.slice(-4)}` : tsapId}
              <button
                onClick={() => { logout(); window.location.href = "/"; }}
                className="ml-1 rounded-full bg-emerald-200 px-2 py-0.5 text-[11px] font-bold hover:bg-emerald-300"
                aria-label="Logout"
              >
                ⎋
              </button>
            </span>
          ) : (
            <Link
              href="/login"
              className="hidden sm:inline-flex px-3.5 py-2 text-[13px] font-semibold border border-maroon/30 text-maroon rounded-full hover:bg-maroon-soft transition"
            >
              📱 <Duo en="Login" te="లాగిన్" />
            </Link>
          )}
          <Link
            href="/register"
            className="px-4 py-2.5 rounded-full text-[13px] font-bold maroon-gradient text-white shadow-soft hover:shadow-brand transition"
          >
            <Duo en="Register FREE" te="ఉచిత నమోదు" />
          </Link>
          <button
            aria-label="Menu"
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            className="lg:hidden w-10 h-10 rounded-xl border border-maroon/20 flex items-center justify-center text-maroon focus-brand"
          >
            <span className="relative block w-5 h-3.5">
              <span
                className={`absolute left-0 h-0.5 w-5 bg-maroon rounded transition-all ${
                  open ? "top-1.5 rotate-45" : "top-0"
                }`}
              />
              <span
                className={`absolute left-0 top-1.5 h-0.5 w-5 bg-maroon rounded transition-all ${
                  open ? "opacity-0" : "opacity-100"
                }`}
              />
              <span
                className={`absolute left-0 h-0.5 w-5 bg-maroon rounded transition-all ${
                  open ? "top-1.5 -rotate-45" : "top-3"
                }`}
              />
            </span>
          </button>
        </div>
      </div>

      {/* Mobile drawer */}
      <div
        className={`lg:hidden overflow-hidden transition-all duration-300 ${
          open ? "max-h-[420px]" : "max-h-0"
        }`}
      >
        <div className="glass border-t border-gold/25 px-4 py-3 space-y-1">
          {NAV.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              className={`block px-4 py-3 rounded-xl text-sm font-semibold ${
                isActive(n.href) ? "bg-maroon text-white" : "text-ink/80 hover:bg-white"
              }`}
            >
              {n.icon} <Duo en={n.en} te={n.te} />
            </Link>
          ))}
          <div className="flex gap-2 pt-2">
            <Link
              href="/search/TSAP-M-2025-1042"
              className="flex-1 text-center px-4 py-3 rounded-xl border border-maroon/25 text-maroon text-sm font-bold"
            >
              <Duo en="ID Search" te="వెతకండి" />
            </Link>
            <a
              href={SITE_CONFIG.botUrl}
              target="_blank"
              rel="noreferrer"
              className="flex-1 text-center px-4 py-3 rounded-xl gold-gradient text-maroon text-sm font-bold"
            >
              Telegram Bot
            </a>
          </div>
          <div className="text-[11px] text-center text-gray-500 pt-1">
            {CHANNEL_STATS.total} channels • {CHANNEL_STATS.by_tier.L3_CASTE} castes • {SITE_CONFIG.botUsername}
          </div>
        </div>
      </div>
    </header>
  );
}
