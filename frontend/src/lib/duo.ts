/**
 * 🌐 WAVE 15 — DUO bilingual system (English • తెలుగు)
 * =====================================================
 * Oka neat form everywhere: English first (clarity) + Telugu alongside (warmth).
 * Usage:
 *   import { Duo, duo } from "@/lib/duo";
 *   <Duo en="Matches" te="సంబంధాలు" />
 *   <h1><Duo en="Pricing" te="ధరలు" /></h1>
 */
import React from "react";

export function duo(en: string, te: string): string {
  return `${en} • ${te}`;
}

export function Duo({ en, te, className = "" }: { en: string; te: string; className?: string }) {
  return React.createElement(
    "span",
    { className: `duo ${className}`.trim() },
    en,
    " ",
    React.createElement("span", { className: "duo-te" }, `• ${te}`)
  );
}
