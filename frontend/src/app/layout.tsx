import type { Metadata, Viewport } from "next";
import "./globals.css";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";
import StickyCTA from "@/components/StickyCTA";
import { CHANNEL_STATS } from "@/lib/channels";
import PWA from "@/components/PWA";

const SITE = process.env.SITE_URL || "https://manavivaha.in";

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "Mana Vivaha — TS-AP No.1 Telugu Matrimony | ₹99 ke Sambandham | Modati 3 FREE",
    template: "%s | Mana Vivaha (TSAP Matrimony)",
  },
  description:
    `Telangana + Andhra Pradesh No.1 Telugu Matrimony. ${CHANNEL_STATS.total} channels — 4 main (TS/AP × Bride/Groom), caste-wise (bride/groom separate), religion, special. ₹99 ke Sambandham, modati 3 numbers FREE, photo-private, DOB verified, Telegram + WhatsApp auto-post. 3 min lo register!`,
  keywords: [
    "Telugu matrimony", "TS matrimony", "AP matrimony", "Reddy matrimony", "Kamma matrimony",
    "Kapu matrimony", "Madiga matrimony", "Lambada matrimony", "Muslim matrimony Telugu",
    "Christian matrimony Telugu", "second marriage Telugu", "₹99 matrimony", "manavivaha",
    "Telangana brides", "Telangana grooms", "Andhra brides", "NRI Telugu matrimony",
  ],
  authors: [{ name: "Mana Vivaha" }],
  applicationName: "Mana Vivaha",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    locale: "te_IN",
    url: SITE,
    siteName: "Mana Vivaha — TSAP Matrimony",
    title: "Mana Vivaha — TS-AP No.1 Telugu Matrimony | ₹99 ke Sambandham",
    description:
      `${CHANNEL_STATS.total} channels, 43 castes (top castes ki bride/groom separate), ₹99 lo 5 numbers, modati 3 FREE. Photo-private + DOB verified.`,
  },
  twitter: {
    card: "summary_large_image",
    title: "Mana Vivaha — TS-AP Telugu Matrimony",
    description: `₹99 ke Sambandham • Modati 3 FREE • ${CHANNEL_STATS.total} channels • caste prakaram`,
  },
  robots: { index: true, follow: true },
  manifest: "/manifest.webmanifest",
  icons: {
    icon: [{ url: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
           { url: "/icons/icon-512.png", sizes: "512x512", type: "image/png" }],
    apple: [{ url: "/icons/apple-touch-icon.png", sizes: "180x180" }],
    shortcut: ["/favicon.png"],
  },
  appleWebApp: { capable: true, title: "Mana Vivaha", statusBarStyle: "default" },
  formatDetection: { telephone: true },
  category: "Matrimony",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#7A0C2E",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="te-IN">
      <body className="antialiased min-h-screen flex flex-col">
        <SiteHeader />
        <main className="flex-1">{children}</main>
        <SiteFooter />
        <StickyCTA />
        <PWA />
      </body>
    </html>
  );
}
