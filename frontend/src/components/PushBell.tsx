"use client";
/**
 * 🔔 WAVE 38 — PUSH BELL (match alerts ON/OFF + test).
 * Browser PushManager + VAPID → /api/push/subscribe. VAPID keys lekapothe
 * preview mode (queue lone — admin push queue lo kanipistundi).
 */
import { useCallback, useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
import { useLang } from "@/lib/lang";

function b64ToU8(base64: string): Uint8Array<ArrayBuffer> {
  const pad = "=".repeat((4 - (base64.length % 4)) % 4);
  const bin = window.atob((base64 + pad).replace(/-/g, "+").replace(/_/g, "/"));
  const out: Uint8Array<ArrayBuffer> = new Uint8Array(new ArrayBuffer(bin.length));
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function bufToB64(buf: ArrayBuffer | null): string {
  if (!buf) return "";
  const bytes = new Uint8Array(buf);
  let bin = "";
  bytes.forEach((b) => { bin += String.fromCharCode(b); });
  return window.btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

export default function PushBell({ myId }: { myId: string }) {
  const { lang } = useLang();
  const te = lang === "te";
  const [supported, setSupported] = useState(true);
  const [vapid, setVapid] = useState("");
  const [mode, setMode] = useState("preview");
  const [perm, setPerm] = useState("");
  const [on, setOn] = useState(false);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const refresh = useCallback(async () => {
    try {
      const reg = await navigator.serviceWorker?.ready;
      const sub = await reg?.pushManager?.getSubscription();
      setOn(!!sub);
    } catch { /* ignore */ }
    try { setPerm(Notification.permission); } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    const ok = typeof window !== "undefined" && "Notification" in window
      && "serviceWorker" in navigator && "PushManager" in window;
    setSupported(ok);
    if (!ok) return;
    void apiGet<{ vapid_public_key?: string; mode?: string }>("/api/push/vapid").then(({ data }) => {
      if (data?.vapid_public_key) { setVapid(data.vapid_public_key); setMode(data.mode || "live-ready"); }
    });
    void refresh();
  }, [refresh]);

  const enable = async () => {
    setBusy(true); setMsg("");
    try {
      const p = await Notification.requestPermission();
      setPerm(p);
      if (p !== "granted") { setMsg(te ? "🔕 Permission ivvaledu — browser settings lo allow cheyandi" : "🔕 Permission denied — allow in browser settings"); setBusy(false); return; }
      if (!vapid) { setMsg(te ? "ℹ️ Server push keys (VAPID) ఇంకా set కాలేదు — admin కి చెప్పండి" : "ℹ️ Server push keys (VAPID) not set yet — tell admin"); setBusy(false); return; }
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ToU8(vapid) });
      const { ok, data, errorTelugu } = await apiPost<{ message_telugu?: string }>("/api/push/subscribe", {
        tsap_id: myId, endpoint: sub.endpoint,
        keys: { p256dh: bufToB64(sub.getKey("p256dh")), auth: bufToB64(sub.getKey("auth")) },
        ua: navigator.userAgent.slice(0, 120),
      });
      setMsg(ok ? String(data?.message_telugu || "ON") : errorTelugu);
      void refresh();
    } catch { setMsg(te ? "Subscribe fail — మళ్ళీ try చేయండి" : "Subscribe failed — retry"); }
    setBusy(false);
  };

  const disable = async () => {
    setBusy(true); setMsg("");
    try {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      const ep = sub?.endpoint || "";
      if (sub) await sub.unsubscribe();
      const { data } = await apiPost<{ message_telugu?: string }>("/api/push/unsubscribe", { tsap_id: myId, endpoint: ep });
      setMsg(String(data?.message_telugu || "OFF"));
      void refresh();
    } catch { setMsg("Unsubscribe fail"); }
    setBusy(false);
  };

  const test = async () => {
    setBusy(true); setMsg("");
    const { ok, data, errorTelugu } = await apiPost<Record<string, any>>(`/api/push/notify/${encodeURIComponent(myId)}`, {
      title: te ? "💍 మన వివాహ — test alert!" : "💍 మన వివాహ — test alert!",
      body: te ? "Alerts పని చేస్తున్నాయి ✅ — కొత్త matches వస్తే ఇలా వస్తుంది" : "Alerts work ✅ — new matches come like this",
      url: "/me",
    });
    setBusy(false);
    setMsg(ok ? `${data?.message_telugu || "sent"} (${data?.mode || ""})` : String(data?.message_telugu || errorTelugu));
  };

  if (!supported) {
    return <p className="text-[13px] text-slate-500">{te ? "ℹ️ ఈ browser లో push alerts లేవు (Chrome/Android best)." : "ℹ️ Push alerts not supported in this browser (Chrome/Android best)."}</p>;
  }
  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        <span className={`rounded-full px-3 py-1 text-[12px] font-bold ${on ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"}`}>
          {on ? "🔔 ON" : "🔕 OFF"}
        </span>
        {mode === "preview" && <span className="text-[11px] text-amber-700">ℹ️ {te ? "server preview mode (VAPID keys pending)" : "server preview mode (VAPID keys pending)"}</span>}
        {perm === "denied" && <span className="text-[11px] text-red-700">⚠️ {te ? "browser permission blocked" : "browser permission blocked"}</span>}
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {!on ? (
          <button onClick={() => void enable()} disabled={busy}
            className="rounded-xl bg-[#7A0C2E] px-4 py-2 text-[12px] font-bold text-white disabled:opacity-50">
            {busy ? "…" : te ? "🔔 Alerts ON chey" : "🔔 Turn alerts ON"}
          </button>
        ) : (
          <>
            <button onClick={() => void test()} disabled={busy}
              className="rounded-xl bg-green-600 px-4 py-2 text-[12px] font-bold text-white disabled:opacity-50">
              {busy ? "…" : te ? "📲 Test notification" : "📲 Test notification"}
            </button>
            <button onClick={() => void disable()} disabled={busy}
              className="rounded-xl border border-slate-300 px-4 py-2 text-[12px] font-bold text-slate-600 disabled:opacity-50">
              {te ? "🔕 OFF chey" : "Turn OFF"}
            </button>
          </>
        )}
      </div>
      {msg && <p className="mt-2 rounded-xl bg-slate-50 p-2 text-[12px] font-bold text-slate-700">{msg}</p>}
      <p className="mt-2 text-[11px] text-slate-500">
        {te ? "కొత్త matches + interest replies కి notification — browser close చేసినా వస్తుంది." : "Notification for new matches + interest replies — even with browser closed."}
      </p>
    </div>
  );
}
