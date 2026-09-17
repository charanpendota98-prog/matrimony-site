"use client";

/**
 * PWA — service worker register + "app laga install cheyyandi" prompt (Telugu)
 * Matrimony lo pedda advantage: phone home screen lo icon → repeat visits 3x penchutundi.
 */
import { useEffect, useState } from "react";
import { useLang } from "@/lib/lang";

export default function PWA() {
  const { lang } = useLang();
  const te = lang === "te";
  const [show, setShow] = useState(false);
  const [promptEvent, setPromptEvent] = useState<any>(null);

  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js").catch(() => undefined);
    }
    const onPrompt = (e: Event) => {
      e.preventDefault();
      setPromptEvent(e);
      if (!localStorage.getItem("tsap_pwa_dismissed")) setTimeout(() => setShow(true), 6000);
    };
    window.addEventListener("beforeinstallprompt", onPrompt);
    return () => window.removeEventListener("beforeinstallprompt", onPrompt);
  }, []);

  const install = async () => {
    try {
      await promptEvent?.prompt();
      setShow(false);
    } catch { setShow(false); }
  };

  const close = () => {
    setShow(false);
    localStorage.setItem("tsap_pwa_dismissed", "1");
  };

  if (!show && !promptEvent) return null;
  return (
    <div className="fixed bottom-3 left-3 right-3 md:left-auto md:right-4 md:w-[360px] z-40 no-print">
      <div className="bg-white rounded-2xl border border-gold/40 shadow-brand p-3 flex items-center gap-3 step-slide">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/icons/icon-192.png" alt="Mana Vivaha app" className="w-11 h-11 rounded-xl border border-gold/30" />
        <div className="flex-1 min-w-0">
          <div className="text-[12px] font-bold text-maroon">{te ? "📲 Mana Vivaha app లాగా install చెయ్యండి" : "📲 Install Mana Vivaha as app"}</div>
          <div className="text-[11px] text-gray-600 telugu">{te ? "Home screen లో icon వస్తుంది — matches + requests వెంటనే చూడొచ్చు (offline లో కూడా open అవుతుంది)." : "Icon on home screen — matches + requests instantly (opens offline too)."}</div>
        </div>
        <div className="flex flex-col gap-1">
          <button onClick={install} className="px-3 py-2 rounded-xl maroon-gradient text-white text-[11px] font-bold">Install</button>
          <button onClick={close} className="px-3 py-1 text-[10px] text-gray-500">{te ? "తర్వాత" : "later"}</button>
        </div>
      </div>
    </div>
  );
}
