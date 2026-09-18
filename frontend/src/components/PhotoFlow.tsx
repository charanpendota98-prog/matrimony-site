"use client";

/**
 * 📸 WAVE 17 — PhotoFlow: top-matrimony standard photo step.
 * benefits → pick → uploading/validating → approved / pending / not-approved(+reason+retry).
 * Strict: server validates (resolution/blur/dark/glare/fake) + admin human review.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { Duo, duo } from "@/lib/duo";
import { useLang } from "@/lib/lang";

type Status = {
  photo_url: string; photo_status: string;
  photo_reason: string; photo_reason_te: string;
};

export default function PhotoFlow({ tsapId, onDone }: { tsapId: string; onDone?: () => void }) {
  const { lang } = useLang();
  const te = lang === "te";
  const [st, setSt] = useState<Status | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [skipped, setSkipped] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const load = useCallback(async () => {
    try {
      const r = await fetch(`/api/photo/status/${encodeURIComponent(tsapId)}`);
      if (r.ok) setSt(await r.json());
    } catch { /* offline — retry later */ }
  }, [tsapId]);

  useEffect(() => { void load(); }, [load]);

  const upload = async (f: File | undefined) => {
    if (!f) return;
    setBusy(true); setErr("");
    try {
      const fd = new FormData();
      fd.append("file", f);
      fd.append("tsap_id", tsapId);
      const r = await fetch("/api/photo/upload", { method: "POST", body: fd });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) {
        const det = d?.detail || d;
        setErr(det?.te || det?.en || d?.message_telugu || (te ? "Upload fail అయ్యింది — మళ్లీ try చెయ్యండి" : "Upload failed — retry"));
        setSt((s) => ({ photo_url: "", photo_status: "rejected", photo_reason: det?.en || "", photo_reason_te: det?.te || "", ...(s || {}) }));
      } else {
        await load();
      }
    } catch {
      setErr(te ? "Network లేదు — మళ్లీ try చెయ్యండి" : "No network — retry");
    }
    setBusy(false);
  };

  if (skipped) return null;
  const status = st?.photo_status || "none";

  /* ---------- APPROVED ---------- */
  if (status === "approved") {
    return (
      <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 text-center">
        <div className="text-3xl">✅</div>
        <div className="font-bold text-emerald-900 mt-1"><Duo en="Photo approved!" te="ఫోటో ఆమోదించబడింది!" /></div>
        {st?.photo_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={st.photo_url} alt="Approved profile photo" className="mx-auto mt-2 w-28 h-36 object-cover rounded-xl border border-emerald-300" />
        ) : null}
        <p className="text-[12px] text-emerald-800 mt-2 telugu">{te ? "Profile ఇప్పుడు photo తో కనిపిస్తుంది — responses 10x ఎక్కువ!" : "Your profile now shows with photo — 10x more responses!"}</p>
      </div>
    );
  }

  /* ---------- PENDING (admin review) ---------- */
  if (status === "pending") {
    return (
      <div className="bg-white rounded-2xl p-5 border border-gold/30 card-shadow text-center">
        <div className="mx-auto w-10 h-10 rounded-full border-4 border-gold/30 border-t-maroon animate-spin" />
        <div className="font-bold text-maroon mt-3"><Duo en="Photo validation in progress" te="ఫోటో పరిశీలన జరుగుతోంది" /></div>
        <p className="text-[12px] text-gray-600 mt-1 telugu">{te ? "Technical checks pass అయ్యాయి ✅ — admin approval అవ్వగానే photo live అవుతుంది (కొన్ని నిమిషాల్లో)." : "Technical checks passed ✅ — photo goes live on admin approval (in a few minutes)."}</p>
        <button onClick={() => void load()} className="mt-3 text-[12px] font-bold text-maroon underline">↻ Status refresh</button>
      </div>
    );
  }

  /* ---------- NOT APPROVED (reason + retry) ---------- */
  if (status === "rejected") {
    return (
      <div className="bg-white rounded-2xl p-5 border border-red-200 card-shadow">
        <div className="font-bold text-[16px]"><Duo en="Photo not approved" te="ఫోటో ఆమోదించబడలేదు" /></div>
        <div className="mt-2 flex items-start gap-2 bg-red-50 border border-red-200 rounded-xl p-3">
          <span className="text-xl">⚠️</span>
          <div>
            <div className="font-bold text-red-700 text-[13px]">{st?.photo_reason || "Try another photo"}</div>
            <div className="text-[12px] text-gray-700 telugu">{st?.photo_reason_te || err || (te ? "Clear original photo మళ్లీ పంపండి" : "Send a clear original photo again")}</div>
          </div>
        </div>
        <input ref={fileRef} type="file" accept="image/jpeg,image/png,image/webp" className="hidden"
          onChange={(e) => void upload(e.target.files?.[0])} />
        <button disabled={busy} onClick={() => fileRef.current?.click()}
          className="mt-3 w-full rounded-2xl maroon-gradient text-white font-bold py-3 disabled:opacity-50">
          {busy ? <Duo en="Validating… please wait" te="పరిశీలిస్తున్నాం… వేచి ఉండండి" /> : <Duo en="Add new photo" te="కొత్త ఫోటో జోడించండి" />}
        </button>
        <button onClick={() => { setSkipped(true); onDone?.(); }}
          className="mt-2 w-full text-center text-[13px] font-bold text-maroon/70">
          <Duo en="I will do this later" te="తర్వాత చేస్తాను" />
        </button>
      </div>
    );
  }

  /* ---------- BENEFITS + PICK (default) ---------- */
  return (
    <div className="bg-white rounded-2xl p-5 border border-gold/30 card-shadow">
      <div className="flex items-center justify-between">
        <div className="font-bold text-[16px]"><Duo en="Add photo" te="ఫోటో జోడించండి" /></div>
        <button onClick={() => { setSkipped(true); onDone?.(); }} className="text-[13px] font-bold text-maroon">
          <Duo en="Skip for now ›" te="ప్రస్తుతానికి దాటవేయి ›" />
        </button>
      </div>
      <div className="mt-3 flex gap-3 items-center">
        <div className="w-16 h-20 rounded-xl maroon-gradient text-white flex items-center justify-center text-3xl shrink-0">📸</div>
        <div>
          <div className="font-bold text-maroon"><Duo en="Add photo for better responses" te="మంచి స్పందనల కోసం ఫోటో జోడించండి" /></div>
          <div className="text-[12px] text-gray-600 mt-1 space-y-0.5">
            <div>👍 <Duo en="90% members contact only profiles with photo" te="90% మంది ఫోటో ఉన్న ప్రొఫైళ్లనే సంప్రదిస్తారు" /></div>
            <div>💬 <Duo en="10 times more responses" te="10 రెట్లు ఎక్కువ స్పందనలు" /></div>
          </div>
        </div>
      </div>
      {busy ? (
        <div className="mt-4 text-center py-3">
          <div className="mx-auto w-10 h-10 rounded-full border-4 border-gold/30 border-t-maroon animate-spin" />
          <div className="font-bold text-maroon mt-2"><Duo en="Upload in progress" te="అప్‌లోడ్ జరుగుతోంది" /></div>
          <p className="text-[12px] text-gray-600 telugu">{duo("Your photo is getting validated. Please wait", "మీ ఫోటో పరిశీలించబడుతోంది. వేచి ఉండండి")}</p>
        </div>
      ) : (
        <>
          <input ref={fileRef} type="file" accept="image/jpeg,image/png,image/webp" className="hidden"
            onChange={(e) => void upload(e.target.files?.[0])} />
          <button onClick={() => fileRef.current?.click()}
            className="mt-4 w-full rounded-2xl maroon-gradient text-white font-bold py-3">
            <Duo en="Add photo now" te="ఇప్పుడే ఫోటో జోడించండి" />
          </button>
          <p className="mt-2 text-center text-[11px] text-gray-500 telugu">
            {duo("Clear original photo only — blur/dark/screenshot auto-reject + admin review", "క్లియర్ ఒరిజినల్ ఫోటో మాత్రమే — బ్లర్/చీకటి/స్క్రీన్‌షాట్ ఆటో-రిజెక్ట్ + అడ్మిన్ పరిశీలన")}
          </p>
        </>
      )}
    </div>
  );
}
