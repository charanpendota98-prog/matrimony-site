/**
 * /castes — SEO hub: anni 43 caste pages ki index (Google crawl + internal linking)
 * Shell stays server (metadata); body is client with te/en toggle.
 */
import type { Metadata } from "next";
import CastesClient from "./castes-client";

export const metadata: Metadata = {
  title: "Caste-wise Telugu Matrimony Channels — 43 Castes (TS & AP)",
  description:
    "Reddy, Kamma, Kapu, Velama, Vysya, Brahmin, Yadav, Mala, Madiga, Lambada… 43 caste-wise Telugu matrimony channels. Bride & groom profiles, district-wise pages, WhatsApp interest model. Mana Vivaha (TSAP Matrimony).",
  keywords: ["caste wise matrimony", "telugu caste matrimony", "reddy matrimony", "kamma matrimony",
             "mala matrimony", "madiga matrimony", "lambada matrimony", "tsap matrimony"],
  alternates: { canonical: "https://manavivaha.in/castes" },
};

export default function CastesHub() {
  return <CastesClient />;
}
