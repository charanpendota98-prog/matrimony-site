"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { CHANNEL_STATS } from "@/lib/channels";
import { SITE_CONFIG } from "@/lib/site-config";
import { useSession, logout } from "@/lib/auth";
import { apiGet } from "@/lib/api";
import { Duo, duo } from "@/lib/duo";
import { LangToggle, useLang } from "@/lib/lang";

type NavItem = { href: string; en: string; te: string; icon: string; xl?: boolean };

/* Desktop pills — trimmed to the 10 most-used (rest live in the menu card) */
const NAV_MAIN: NavItem[] = [
  { href: "/", en: "Home", te: "హోమ్", icon: "🏠" },
  { href: "/matches", en: "Matches", te: "సంబంధాలు", icon: "💘" },
  { href: "/requests", en: "Requests", te: "రిక్వెస్టులు", icon: "💌" },
  { href: "/channels", en: "Channels", te: "ఛానళ్లు", icon: "📢" },
  { href: "/castes", en: "Castes", te: "కులాలు", icon: "🪔" },
  { href: "/pricing", en: "Pricing", te: "ధరలు", icon: "💰" },
  { href: "/referral", en: "Referral", te: "రెఫరల్", icon: "🤝" },
  { href: "/stories", en: "Stories", te: "కథలు", icon: "💑", xl: true },
  { href: "/vendors", en: "Vendors", te: "వెండర్లు", icon: "🏪", xl: true },
  { href: "/safety", en: "Safety", te: "భద్రత", icon: "🛡️", xl: true },
];

const NAV_EARN: NavItem[] = [
  { href: "/referral", en: "Referral dashboard", te: "రెఫరల్ డాష్‌బోర్డ్", icon: "🤝" },
  { href: "/referral/register", en: "Become a referrer", te: "రెఫరర్‌గా చేరండి", icon: "🎁" },
  { href: "/bureau", en: "Bureau (B2B)", te: "బ్యూరో (B2B)", icon: "🏛️" },
  { href: "/vendors", en: "Vendors", te: "వెండర్లు", icon: "🏪" },
  { href: "/vendors/register", en: "List your business", te: "మీ business చేర్చండి", icon: "📝" },
];

const NAV_MORE: NavItem[] = [
  { href: "/porutham", en: "Porutham", te: "పొరుతం", icon: "💍" },
  { href: "/stories", en: "Stories", te: "కథలు", icon: "💑" },
  { href: "/safety", en: "Safety", te: "భద్రత", icon: "🛡️" },
  { href: "/verify", en: "Verify profile", te: "Profile verify", icon: "✅" },
];

const NAV_TEAM: NavItem[] = [
  { href: "/admin", en: "Admin", te: "అడ్మిన్", icon: "🔐" },
  { href: "/growth", en: "Growth (leads)", te: "గ్రోత్ (leads)", icon: "📈" },
  { href: "/admin/photos", en: "Photo review", te: "Photo review", icon: "📸" },
];

export default function SiteHeader() {
  const pathname = usePathname();
  const { lang } = useLang();
  const te = lang === "te";
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

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open ]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  const groupTitle = (en: string, teL: string) => (
    <div className="px-4 pt-3 pb-1 text-[10px] font-extrabold uppercase tracking-[0.14em] text-gold-deep">
      {te ? teL : en}
    </div>
  );

  const menuLink = (n: NavItem) => (
    <Link
      key={n.href}
      href={n.href}
      className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-semibold transition ${
        isActive(n.href) ? "bg-maroon text-white shadow-soft" : "text-ink/80 hover:bg-white"
      }`}
    >
      <span className="w-6 text-center">{n.icon}</span>
      <Duo en={n.en} te={n.te} />
      {isActive(n.href) && <span className="ml-auto text-[10px] opacity-80">●</span>}
    </Link>
  );

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
        <nav className="hidden lg:flex items-center gap-1" aria-label="Main">
          {NAV_MAIN.map((n) => (
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
              {n.icon} {te ? n.te : n.en}
            </Link>
          ))}
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-2">
          <LangToggle compact />
          <Link
            href="/porutham"
            className="hidden md:inline-flex px-3.5 py-2 text-[13px] font-semibold border border-maroon/30 text-maroon rounded-full hover:bg-maroon-soft transition"
          >
            💍 <Duo en="Porutham" te="పొరుతం" />
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
            aria-label={te ? "మెనూ" : "Menu"}
            aria-expanded={open}
            aria-controls="mobile-menu"
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

      {/* Mobile menu card — grouped + scrollable */}
      <div
        id="mobile-menu"
        className={`lg:hidden overflow-hidden transition-all duration-300 ${
          open ? "max-h-[75vh]" : "max-h-0"
        }`}
      >
        <div className="glass border-t border-gold/25 px-4 pt-1 pb-4 max-h-[75vh] overflow-y-auto overscroll-contain menu-scroll">
          {groupTitle("Main", "మెయిన్")}
          <div className="space-y-1">
            {NAV_MAIN.filter((n) => !n.xl).map(menuLink)}
          </div>
          {groupTitle("Earn", "సంపాదించండి")}
          <div className="space-y-1">
            {NAV_EARN.map(menuLink)}
          </div>
          {groupTitle("More", "మరిన్ని")}
          <div className="space-y-1">
            {NAV_MORE.map(menuLink)}
          </div>
          {groupTitle("Team", "టీమ్")}
          <div className="space-y-1">
            {NAV_TEAM.map(menuLink)}
          </div>
          <div className="flex gap-2 pt-3">
            <Link
              href="/matches"
              className="flex-1 text-center px-4 py-3 rounded-xl border border-maroon/25 text-maroon text-sm font-bold"
            >
              <Duo en="🔍 Search matches" te="🔍 సంబంధాలు వెతకండి" />
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
          <div className="flex justify-center pt-3">
            <LangToggle />
          </div>
          <div className="text-[11px] text-center text-gray-500 pt-1">
            {CHANNEL_STATS.total} channels • {CHANNEL_STATS.by_tier.L3_CASTE} castes • {SITE_CONFIG.botUsername}
          </div>
        </div>
      </div>
    </header>
  );
}
