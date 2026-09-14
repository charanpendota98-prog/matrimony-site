import Link from "next/link";
import { CHANNEL_STATS } from "@/lib/channels";
import { SITE_CONFIG } from "@/lib/site-config";

export default function SiteFooter() {
  const year = new Date().getFullYear();
  const cols: { title: string; links: { href: string; label: string }[] }[] = [
    {
      title: "Explore",
      links: [
        { href: "/register", label: "Register (FREE)" },
        { href: "/channels", label: `All ${CHANNEL_STATS.total} Channels` },
        { href: "/matches", label: "Matches & Filters" },
        { href: "/search/TSAP-M-2025-1042", label: "ID Search" },
      ],
    },
    {
      title: "Earn",
      links: [
        { href: "/referral", label: "Referral — ₹50/profile" },
        { href: "/referral/register", label: "Become a Referrer" },
        { href: "/bureau", label: "Bureau / Broker B2B" },
        { href: "/admin", label: "Admin Panel" },
      ],
    },
  ];

  return (
    <footer className="mt-10 navy-gradient text-white no-print">
      <div className="max-w-7xl mx-auto px-4 py-10 grid md:grid-cols-4 gap-8 text-sm">
        {/* Brand */}
        <div>
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 gold-gradient rounded-xl flex items-center justify-center text-maroon font-bold text-lg">
              MV
            </div>
            <div>
              <div className="font-bold text-gold leading-none">Mana Vivaha</div>
              <div className="text-[10px] opacity-70">TSAP Matrimony</div>
            </div>
          </div>
          <div className="text-xs opacity-75 mt-3 telugu leading-relaxed">
            TS + AP No.1 Telugu Matrimony. ₹99 ke Sambandham — modati 3 numbers FREE.
            Region • Religion • {CHANNEL_STATS.by_tier.L3_CASTE} Castes • Special channels.
          </div>
          <div className="mt-4 flex flex-wrap gap-2 text-[11px]">
            <span className="px-2.5 py-1 rounded-full bg-white/10">{CHANNEL_STATS.total} Channels</span>
            <span className="px-2.5 py-1 rounded-full bg-white/10">Telegram + WhatsApp</span>
            <span className="px-2.5 py-1 rounded-full bg-white/10">Photo Private</span>
          </div>
        </div>

        {cols.map((c) => (
          <div key={c.title}>
            <div className="font-bold text-gold text-[13px] uppercase tracking-wide">{c.title}</div>
            <div className="mt-3 space-y-2 text-xs">
              {c.links.map((l) => (
                <div key={l.href}>
                  <Link href={l.href} className="opacity-75 hover:opacity-100 hover:text-gold transition">
                    {l.label}
                  </Link>
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* Trust + contact */}
        <div>
          <div className="font-bold text-gold text-[13px] uppercase tracking-wide">Trust & Safety</div>
          <div className="mt-3 space-y-2 text-xs opacity-85">
            <div>✓ OTP verified numbers</div>
            <div>✓ DOB verified badge</div>
            <div>✓ Photo watermark + private mode</div>
            <div>✓ Number pay tarvata matrame</div>
            <div>✓ 3 reports → auto hide</div>
          </div>
          <div className="mt-4 text-xs opacity-75">
            <div>Bot: {SITE_CONFIG.botUsername}</div>
            <div>Site: {SITE_CONFIG.domain}</div>
            <div>Care: {SITE_CONFIG.supportEmail}</div>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between gap-2 text-[11px] opacity-70">
          <div>© {year} {SITE_CONFIG.brandName} ({SITE_CONFIG.legalName}) • Made for TS/AP with ❤️</div>
          <div className="text-center md:text-right">
            ⚠️ Advance money adigithe ventane report cheyyandi — mosam jagratha!
          </div>
        </div>
      </div>
    </footer>
  );
}
