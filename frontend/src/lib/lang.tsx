"use client";
/**
 * 🌐 WAVE 30 — ONE language at a time (Telugu ⇄ English toggle).
 * User: mix ("galiz") vaddu — neat + professional. Default Telugu, toggle English.
 * Persisted in localStorage (tsap_lang). SSR-safe (default te until mount).
 */
import React, { createContext, useCallback, useContext, useEffect, useState } from "react";

export type Lang = "te" | "en";
const STORE_KEY = "tsap_lang";

// module-level mirror so plain duo(en,te) calls (outside JSX) follow the toggle
let currentLang: Lang = "te";
export function getLang(): Lang {
  return currentLang;
}

type Ctx = { lang: Lang; setLang: (l: Lang) => void; t: (te: string, en: string) => string };
const LangCtx = createContext<Ctx>({ lang: "te", setLang: () => {}, t: (te) => te });

export function LangProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<Lang>("te");
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORE_KEY);
      if (saved === "en" || saved === "te") {
        currentLang = saved;
        setLangState(saved);
      }
    } catch { /* ignore */ }
  }, []);
  const setLang = useCallback((l: Lang) => {
    currentLang = l;
    setLangState(l);
    try { localStorage.setItem(STORE_KEY, l); } catch { /* ignore */ }
    try { document.documentElement.lang = l === "te" ? "te-IN" : "en-IN"; } catch { /* ignore */ }
  }, []);
  const t = useCallback((te: string, en: string) => (lang === "te" ? te : en), [lang]);
  return <LangCtx.Provider value={{ lang, setLang, t }}>{children}</LangCtx.Provider>;
}

export function useLang(): Ctx {
  return useContext(LangCtx);
}

/** JSX: <T te="నమోదు" en="Register" /> */
export function T({ te, en, className = "" }: { te: string; en: string; className?: string }) {
  const { lang } = useLang();
  return <span className={className}>{lang === "te" ? te : en}</span>;
}

/** Header pill toggle */
export function LangToggle({ compact = false }: { compact?: boolean }) {
  const { lang, setLang } = useLang();
  return (
    <div
      className={`inline-flex items-center rounded-full border border-maroon/25 bg-white p-0.5 ${compact ? "text-[11px]" : "text-[12px]"} font-bold`}
      role="group"
      aria-label="Language / భాష"
    >
      {(["te", "en"] as Lang[]).map((l) => (
        <button
          key={l}
          onClick={() => setLang(l)}
          aria-pressed={lang === l}
          className={`px-2.5 py-1 rounded-full transition ${
            lang === l ? "maroon-gradient text-white shadow-soft" : "text-maroon/70 hover:bg-maroon-soft"
          }`}
        >
          {l === "te" ? "తెలుగు" : "English"}
        </button>
      ))}
    </div>
  );
}
