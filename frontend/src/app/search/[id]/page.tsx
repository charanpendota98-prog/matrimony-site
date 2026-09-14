import type { Metadata } from "next";
import { headers } from "next/headers";
import ProfileView from "./ProfileView";

/**
 * 🖼️ /search/[id] — SERVER wrapper (SEO + WhatsApp/Telegram OG preview)
 * ====================================================================
 * Mundu ee page "use client" matrame — anduke per-profile title/description/OG image
 * pettalem (WhatsApp lo link pampinappudu photo preview rakunde). Ippudu:
 *   • generateMetadata → per-profile title, description, og:image (backend Pillow tho generate ayyedi)
 *   • <ProfileView />   → asalu advanced client UI (filters, interest, number reveal…)
 * Backend fail aithe safe fallback (site eppudu kanipistundi).
 */
const SITE = (process.env.SITE_URL || "https://manavivaha.in").replace(/\/$/, "");
const BACKEND = process.env.BACKEND_URL || "http://localhost:8000";

/**
 * 🌐 Request host ni batti absolute URL (staging / preview / prod — anni chotla OG pani cheyyali).
 * SITE_URL set unte adi ne vadutham (production lo manavivaha.in).
 */
function siteBase(): string {
  if (process.env.SITE_URL) return SITE;
  try {
    const h = headers();
    const host = h.get("x-forwarded-host") || h.get("host");
    const proto = h.get("x-forwarded-proto") || "https";
    if (host) return `${proto}://${host}`;
  } catch { /* static build lo skip */ }
  return SITE;
}

async function fetchProfile(id: string) {
  try {
    const r = await fetch(`${BACKEND}/api/search/${encodeURIComponent(id)}`, { cache: "no-store" });
    if (!r.ok) return null;
    const d = await r.json();
    return (d && (d.profile || d)) as Record<string, any> | null;
  } catch {
    return null;
  }
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const id = String(params?.id || "").toUpperCase();
  const p = await fetchProfile(id);
  const name = p?.full_name ? String(p.full_name) : "Telugu Matrimony Profile";
  const bits = [p?.age ? `${p.age} yrs` : "", p?.caste, p?.education, p?.job, p?.district].filter(Boolean).join(" • ");
  const title = `${name} (${id}) — ${bits || "Profile"} | Mana Vivaha`;
  const description = p
    ? `${bits}. Porutham, family, horoscope details + interest pampandi. Mana Vivaha — Telugu matrimony (TS + AP), 65 channels, 3 FREE requests.`
    : "Mana Vivaha — Telugu matrimony. TS + AP, 43 castes, 65 channels, 3 FREE requests. Register FREE.";
  const base = siteBase();
  const ogImage = `${base}/api/og/profile/${encodeURIComponent(id)}.png`;
  return {
    title: { absolute: title },
    description,
    alternates: { canonical: `${base}/search/${encodeURIComponent(id)}` },
    openGraph: {
      title,
      description,
      url: `${base}/search/${encodeURIComponent(id)}`,
      siteName: "Mana Vivaha",
      type: "profile",
      locale: "te_IN",
      images: [{ url: ogImage, width: 1200, height: 630, alt: title }],
    },
    twitter: { card: "summary_large_image", title, description, images: [ogImage] },
    other: { "profile:tsap_id": id, ...(p?.caste ? { "profile:caste": String(p.caste) } : {}) },
  };
}

export default function Page({ params }: { params: { id: string } }) {
  const base = siteBase();
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Person",
            identifier: String(params?.id || ""),
            url: `${base}/search/${encodeURIComponent(String(params?.id || ""))}`,
            name: "Mana Vivaha verified profile",
            description: "Telugu matrimony profile — Mana Vivaha (TS + AP)",
            isPartOf: { "@type": "WebSite", name: "Mana Vivaha", url: base },
          }),
        }}
      />
      <ProfileView />
    </>
  );
}
