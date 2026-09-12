import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TSAP Matrimony - TS & AP No.1 | ₹99 ke Sambandham | First 3 FREE",
  description: "Telangana + Andhra Pradesh Top Matrimony - Telegram + WhatsApp + Website. Caste-wise channels, ₹99 lo 10 numbers, AI matching, Photo-private, Broker referral. 3 min lo register!",
  keywords: "TS matrimony, AP matrimony, Telugu matrimony, Reddy matrimony, Kamma matrimony, ₹99 matrimony",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="te">
      <body className="antialiased">{children}</body>
    </html>
  );
}
