"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { CHANNEL_STATS } from "@/lib/channels";
import { SITE_CONFIG } from "@/lib/site-config";

const NAV: { href: string; label: string; xl?: boolean }[] = [
  { href: "/", label: "Home" },
  { href: "/channels", label: "Channels" },
  { href: "/pricing", label: "Pricing 💰" },
  { href: "/vendors", label: "Vendors 🏪" },
  { href: "/porutham", label: "Porutham 💍", xl: true },
  { href: "/safety", label: "Safety 🛡️", xl: true },
  { href: "/requests", label: "Requests 💌" },
  { href: "/growth", label: "Growth 📈" },
  { href: "/castes", label: "Castes" },
  { href: "/matches", label: "Matches" },
  { href: "/referral", label: "Referral" },
  { href: "/bureau", label: "Bureau" },
  { href: "/admin", label: "Admin" },
];

export default function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

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
              className={`${n.xl ? "hidden xl:inline-flex" : ""} px-3.5 py-2 rounded-full text-[13px] font-semibold transition ${
                isActive(n.href)
                  ? "bg-maroon text-white shadow-soft"
                  : "text-ink/75 hover:text-maroon hover:bg-maroon-soft"
              }`}
            >
              {n.label}
            </Link>
          ))}
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-2">
          <Link
            href="/search/TSAP-M-2025-1042"
            className="hidden md:inline-flex px-3.5 py-2 text-[13px] font-semibold border border-maroon/30 text-maroon rounded-full hover:bg-maroon-soft transition"
          >
            ID Search
          </Link>
          <Link
            href="/login"
            className="hidden sm:inline-flex px-3.5 py-2 text-[13px] font-semibold border border-maroon/30 text-maroon rounded-full hover:bg-maroon-soft transition"
          >
            📱 Login
          </Link>
          <Link
            href="/register"
            className="px-4 py-2.5 rounded-full text-[13px] font-bold maroon-gradient text-white shadow-soft hover:shadow-brand transition"
          >
            Register FREE
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
              {n.label}
            </Link>
          ))}
          <div className="flex gap-2 pt-2">
            <Link
              href="/search/TSAP-M-2025-1042"
              className="flex-1 text-center px-4 py-3 rounded-xl border border-maroon/25 text-maroon text-sm font-bold"
            >
              ID Search
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
