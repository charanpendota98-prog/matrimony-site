"use client";

/**
 * MANA VIVAHA — REQUESTS DASHBOARD (💌 Interest model — chatting LEDU)
 * ====================================================================
 * • Interest pampu (1 credit; modati 3 FREE) → owner ki WhatsApp lo mee profile
 * • Inbox: vachina requests → ✅ Accept / ❌ Decline (decline = credit refund)
 * • Sent: pampina requests + status + accept ayyaka contact
 * • Plans: ₹99 → 3 profiles | ₹199 → 10 | ₹299 → 20
 * • Anti-ban WhatsApp status (queue + random gap) chupisthundi
 */
import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import SectionHeading from "@/components/SectionHeading";

type Plan = { code: string; price: number; profiles: number; label: string; telugu: string; badge: string; per_profile: number };
type Req = {
  request_id: string; from_id: string; to_id: string; status: string; score: number;
  note?: string; reasons?: string[]; created_at?: string; credit_refunded?: boolean;
  requester?: any; profile?: any; requester_phone?: string; contact?: string; actions?: string[];
};

const PLANS_FALLBACK: Plan[] = [
  { code: "S_99", price: 99, profiles: 3, label: "Sambandham", telugu: "₹99 → 3 profiles", badge: "Starter", per_profile: 33 },
  { code: "S_199", price: 199, profiles: 10, label: "Family", telugu: "₹199 → 10 profiles", badge: "Best for families", per_profile: 20 },
  { code: "S_299", price: 299, profiles: 20, label: "Premium", telugu: "₹299 → 20 profiles", badge: "₹15/profile — best", per_profile: 15 },
];

const STATUS_STYLE: Record<string, string> = {
  pending: "bg-amber-100 text-amber-800 border-amber-300",
  accepted: "bg-emerald-100 text-emerald-800 border-emerald-300",
  declined: "bg-rose-100 text-rose-800 border-rose-300",
  expired: "bg-gray-100 text-gray-600 border-gray-300",
  withdrawn: "bg-gray-100 text-gray-600 border-gray-300",
};

export default function RequestsPage() {
  const [myId, setMyId] = useState("");
  const [tab, setTab] = useState<"inbox" | "sent" | "send" | "plans">("inbox");
  const [credits, setCredits] = useState<number | null>(null);
  const [plans, setPlans] = useState<Plan[]>(PLANS_FALLBACK);
  const [inbox, setInbox] = useState<any>({ received: [], pending: 0, accepted: 0, declined: 0 });
  const [sent, setSent] = useState<any>({ sent: [] });
  const [toId, setToId] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState<{ kind: "ok" | "err" | "info"; text: string } | null>(null);
  const [lastSend, setLastSend] = useState<any>(null);
  const [wa, setWa] = useState<any>(null);
  const [showOwnerMsg, setShowOwnerMsg] = useState(false);

  // ---- load my ID (localStorage / ?id=) + plans -------------------------
  useEffect(() => {
    if (typeof window === "undefined") return;
    const sp = new URLSearchParams(window.location.search);
    const fromUrl = sp.get("id") || "";
    const stored = window.localStorage.getItem("tsap_id") || "";
    const id = (fromUrl || stored || "").toUpperCase();
    if (id) {
      setMyId(id);
      window.localStorage.setItem("tsap_id", id);
    }
    fetch("/api/plans")
      .then((r) => r.json())
      .then((d) => d?.plans && setPlans(d.plans.filter((p: Plan) => p.price > 0)))
      .catch(() => {});
    fetch("/api/wa/status").then((r) => r.json()).then(setWa).catch(() => {});
  }, []);

  const refresh = useCallback(
    async (id: string) => {
      if (!id) return;
      try {
        const [c, i, s] = await Promise.all([
          fetch(`/api/credits/${id}`).then((r) => r.json()),
          fetch(`/api/interest/inbox/${id}`).then((r) => r.json()),
          fetch(`/api/interest/sent/${id}`).then((r) => r.json()),
        ]);
        if (typeof c?.credits === "number") setCredits(c.credits);
        if (i?.received) setInbox(i);
        if (s?.sent) setSent(s);
      } catch {
        setToast({ kind: "err", text: "Server tho connect avvaledu — malli try cheyyandi" });
      }
    },
    []
  );

  useEffect(() => {
    if (myId) refresh(myId);
  }, [myId, refresh]);

  const saveId = (v: string) => {
    const id = v.trim().toUpperCase();
    setMyId(id);
    if (typeof window !== "undefined" && id) window.localStorage.setItem("tsap_id", id);
    if (id) refresh(id);
  };

  const sendInterest = async () => {
    if (!myId) return setToast({ kind: "err", text: "Mundu mee TSAP ID ivvandi (register chesaka vastundi)" });
    if (!toId.trim()) return setToast({ kind: "err", text: "Ee profile ki pampali — TSAP ID type cheyyandi" });
    setBusy(true);
    setToast(null);
    try {
      const r = await fetch("/api/interest/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from_id: myId, to_id: toId.trim().toUpperCase(), note }),
      });
      const d = await r.json();
      if (r.status === 402) {
        setToast({ kind: "err", text: d.message_telugu || "Credits ledu" });
        setTab("plans");
        setCredits(0);
      } else if (!r.ok) {
        setToast({ kind: "err", text: d.message_telugu || d.detail || "Request fail ayyindi" });
      } else {
        setLastSend(d);
        setToast({ kind: "ok", text: d.message_telugu });
        setNote("");
        setCredits(d.credits_left);
        refresh(myId);
      }
    } catch {
      setToast({ kind: "err", text: "Network problem — malli try cheyyandi" });
    }
    setBusy(false);
  };

  const respond = async (request_id: string, action: string) => {
    setBusy(true);
    try {
      const r = await fetch("/api/interest/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tsap_id: myId, request_id, action }),
      });
      const d = await r.json();
      setToast({ kind: r.ok ? "ok" : "err", text: d.message_telugu || d.detail || d.message });
      refresh(myId);
    } catch {
      setToast({ kind: "err", text: "Network problem" });
    }
    setBusy(false);
  };

  const buy = async (plan: string) => {
    setBusy(true);
    try {
      const r = await fetch("/api/credits/buy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tsap_id: myId, plan }),
      });
      const d = await r.json();
      if (r.ok) {
        setCredits(d.credits_now);
        setToast({ kind: "ok", text: d.message_telugu });
        if (d.upi_link) window.open(d.upi_link, "_blank");
      } else setToast({ kind: "err", text: d.detail || "Payment start avvaledu" });
    } catch {
      setToast({ kind: "err", text: "Network problem" });
    }
    setBusy(false);
  };

  const loadDemo = async () => {
    setBusy(true);
    try {
      const d = await fetch("/api/demo/seed", { method: "POST" }).then((r) => r.json());
      const list = (d.created || []).map((x: any) => x.tsap_id).join(", ");
      setToast({ kind: "info", text: `Demo profiles: ${list} — veetilo oka ID me "Mee ID" ga petti, inkokati ki interest pampandi` });
    } catch {
      setToast({ kind: "err", text: "Demo load avvaledu" });
    }
    setBusy(false);
  };

  const chip = (s: string) =>
    `text-[10px] font-bold px-2 py-0.5 rounded-full border ${STATUS_STYLE[s] || "bg-gray-100 text-gray-600 border-gray-300"}`;

  return (
    <main className="min-h-screen">
      {/* HERO */}
      <section className="maroon-gradient text-white">
        <div className="max-w-6xl mx-auto px-4 py-10">
          <Reveal>
            <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-3 py-1 text-[11px] font-bold">
              🚫 Chatting ledu • 💌 Interest request • 🛡️ Anti-ban WhatsApp delivery
            </div>
            <h1 className="mt-3 text-2xl md:text-4xl font-bold">Requests Dashboard</h1>
            <p className="mt-2 text-[13px] md:text-sm opacity-90 telugu max-w-3xl">
              Nachhina profile ki <b>Interest pampu</b> — vaallaki WhatsApp lo mee profile card veltundi.
              Vaallu <b>Accept</b> chesthe rendu numbers automatic ga exchange avutayi. <b>Decline</b> chesthe mee credit refund.
              Chatting, spam calls, fake ids — anni ikkade aagutayi.
            </p>
          </Reveal>

          <div className="mt-5 flex flex-wrap gap-3 items-end">
            <div>
              <label className="text-[11px] font-bold opacity-90">Mee TSAP ID</label>
              <input
                value={myId}
                onChange={(e) => setMyId(e.target.value.toUpperCase())}
                onBlur={(e) => saveId(e.target.value)}
                placeholder="TSAP-M-2025-1042"
                className="mt-1 w-56 px-3 py-2 rounded-xl text-ink font-mono text-sm outline-none focus-brand"
              />
            </div>
            <button onClick={() => saveId(myId)} className="gold-gradient text-maroon font-bold text-sm px-4 py-2.5 rounded-xl hover-lift">
              Load my dashboard
            </button>
            <button onClick={loadDemo} disabled={busy} className="bg-white/10 border border-white/25 text-white font-bold text-sm px-4 py-2.5 rounded-xl">
              🎬 Demo profiles load
            </button>
            <div className="ml-auto bg-white/10 border border-white/20 rounded-xl px-4 py-2">
              <div className="text-[10px] opacity-80">Credits</div>
              <div className="font-bold text-lg leading-none">{credits === null ? "—" : credits}</div>
            </div>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 py-6">
        {toast && (
          <div
            className={`mb-4 rounded-2xl px-4 py-3 text-[13px] border card-shadow ${
              toast.kind === "ok"
                ? "bg-emerald-50 border-emerald-200 text-emerald-900"
                : toast.kind === "err"
                ? "bg-rose-50 border-rose-200 text-rose-900"
                : "bg-amber-50 border-amber-200 text-amber-900"
            }`}
          >
            {toast.text}
          </div>
        )}

        {/* TABS */}
        <div className="flex flex-wrap gap-2 mb-4">
          {[
            { k: "inbox", l: `📥 Vachina requests${inbox.pending ? ` (${inbox.pending})` : ""}` },
            { k: "sent", l: `📤 Pampina requests${sent.sent?.length ? ` (${sent.sent.length})` : ""}` },
            { k: "send", l: "💌 Interest pampu" },
            { k: "plans", l: "💳 Plans & Credits" },
          ].map((t) => (
            <button
              key={t.k}
              onClick={() => setTab(t.k as any)}
              className={`px-4 py-2 rounded-xl text-[13px] font-bold border transition ${
                tab === t.k ? "bg-maroon text-white border-maroon" : "bg-white text-maroon border-maroon/20 hover-lift"
              }`}
            >
              {t.l}
            </button>
          ))}
        </div>

        {/* INBOX */}
        {tab === "inbox" && (
          <div className="space-y-3">
            {!myId && <Empty text="Mee TSAP ID ivvandi — inbox chudataniki." />}
            {myId && inbox.received?.length === 0 && <Empty text="Inka requests raledu. Mee profile ni 1 channel lo post cheyyandi — reach perugutundi." />}
            {inbox.received?.map((it: Req) => (
              <Reveal key={it.request_id}>
                <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={chip(it.status)}>{it.status.toUpperCase()}</span>
                    <span className="text-[11px] text-gray-500 font-mono">{it.request_id}</span>
                    {it.score > 0 && <span className="text-[11px] font-bold text-maroon">⭐ {it.score}% match</span>}
                    <span className="ml-auto text-[11px] text-gray-500">{it.requester_phone}</span>
                  </div>
                  <div className="mt-2 grid md:grid-cols-2 gap-3">
                    <div>
                      <div className="font-bold text-[15px] text-maroon">{it.requester?.full_name} ({it.requester?.age}y)</div>
                      <div className="text-[12px] text-gray-600 mt-1 leading-relaxed">
                        🆔 {it.from_id}{it.requester?.verified ? " ✅" : ""}<br />
                        🎓 {it.requester?.education} {it.requester?.education_detail}<br />
                        💼 {it.requester?.job} {it.requester?.company}<br />
                        💰 {it.requester?.salary} • 📏 {it.requester?.height}<br />
                        📍 {it.requester?.district}, {it.requester?.state}<br />
                        💍 {it.requester?.caste} {it.requester?.gothram ? `• Gothram ${it.requester?.gothram}` : ""}<br />
                        🌟 {it.requester?.star || "—"} • Rasi {it.requester?.rasi || "—"}
                      </div>
                      {it.note ? <div className="mt-2 text-[12px] bg-cream border border-gold/30 rounded-xl p-2">📝 &ldquo;{it.note}&rdquo;</div> : null}
                    </div>
                    <div>
                      {it.reasons?.length ? (
                        <div className="text-[12px] text-gray-700">
                          <div className="font-bold text-maroon mb-1">Enduku match avutaru:</div>
                          {it.reasons.slice(0, 4).map((r) => (
                            <div key={r}>✅ {r}</div>
                          ))}
                        </div>
                      ) : null}
                      <div className="mt-3 flex flex-wrap gap-2">
                        {it.actions?.includes("accept") ? (
                          <>
                            <button onClick={() => respond(it.request_id, "accept")} disabled={busy} className="bg-emerald-600 text-white font-bold text-[13px] px-4 py-2 rounded-xl hover-lift">
                              ✅ Accept — number exchange
                            </button>
                            <button onClick={() => respond(it.request_id, "decline")} disabled={busy} className="bg-white border border-rose-300 text-rose-700 font-bold text-[13px] px-4 py-2 rounded-xl">
                              ❌ Decline (credit refund)
                            </button>
                          </>
                        ) : it.status === "accepted" ? (
                          <div className="text-[12px] bg-emerald-50 border border-emerald-200 rounded-xl px-3 py-2 text-emerald-900">
                            ✅ Accepted — contact: <b>{it.requester_phone}</b> (WhatsApp lo kooda vachhindi)
                          </div>
                        ) : (
                          <div className="text-[12px] text-gray-500">Ee request {it.status} — inka action ledu</div>
                        )}
                        <Link href={`/search/${it.from_id}`} className="text-[13px] font-bold text-maroon underline px-2 py-2">
                          Full profile chudu →
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        )}

        {/* SENT */}
        {tab === "sent" && (
          <div className="space-y-3">
            {myId && sent.sent?.length === 0 && <Empty text="Inka evariki interest pampaledu — 💌 'Interest pampu' tab lo start cheyyandi." />}
            {sent.sent?.map((it: Req) => (
              <Reveal key={it.request_id}>
                <div className="bg-white rounded-2xl p-4 card-shadow border border-gold/20 flex flex-wrap items-center gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={chip(it.status)}>{it.status.toUpperCase()}</span>
                      <span className="font-bold text-[14px] text-maroon">{it.profile?.full_name} ({it.profile?.age}y)</span>
                      <span className="text-[11px] text-gray-500 font-mono">{it.to_id}</span>
                      {it.score > 0 && <span className="text-[11px] font-bold">⭐ {it.score}%</span>}
                      {it.credit_refunded && <span className="text-[10px] font-bold text-emerald-700">↩️ refund</span>}
                    </div>
                    <div className="text-[12px] text-gray-600 mt-1">
                      🎓 {it.profile?.education} • 💼 {it.profile?.job} • 📍 {it.profile?.district}, {it.profile?.state} • 💍 {it.profile?.caste}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] text-gray-500">Contact</div>
                    <div className={`text-[13px] font-bold ${it.status === "accepted" ? "text-emerald-700" : "text-gray-400"}`}>{it.contact}</div>
                  </div>
                  <Link href={`/search/${it.to_id}`} className="text-[12px] font-bold text-maroon underline">
                    Profile →
                  </Link>
                </div>
              </Reveal>
            ))}
          </div>
        )}

        {/* SEND */}
        {tab === "send" && (
          <div className="grid md:grid-cols-2 gap-5">
            <div className="bg-white rounded-2xl p-5 card-shadow border border-gold/20">
              <SectionHeading eyebrow="1 credit = 1 profile" title="💌 Interest pampu" subtitle="Profile ID ivvandi — vaallaki mana WhatsApp nunchi mee profile + card veltundi." telugu align="left" />
              <div className="mt-4 space-y-3">
                <div>
                  <label className="text-[12px] font-bold text-ink">Profile TSAP ID *</label>
                  <input
                    value={toId}
                    onChange={(e) => setToId(e.target.value.toUpperCase())}
                    placeholder="TSAP-F-2025-1042"
                    className="mt-1 w-full px-3 py-2.5 rounded-xl border border-gold/40 font-mono text-sm outline-none focus-brand"
                  />
                </div>
                <div>
                  <label className="text-[12px] font-bold text-ink">Chinna message (optional)</label>
                  <textarea
                    value={note}
                    onChange={(e) => setNote(e.target.value.slice(0, 280))}
                    rows={3}
                    placeholder="Mee profile chala bagundi — mana family values match avutunnayi. Matladukovachu."
                    className="mt-1 w-full px-3 py-2.5 rounded-xl border border-gold/40 text-sm outline-none focus-brand"
                  />
                  <div className="text-[10px] text-gray-500 mt-1">{note.length}/280 • number/email pettaku (privacy policy)</div>
                </div>
                <button onClick={sendInterest} disabled={busy} className="w-full maroon-gradient text-white font-bold py-3 rounded-xl hover-lift disabled:opacity-60">
                  {busy ? "Pampisthunnam…" : "💌 Interest pampu"}
                </button>
                <div className="text-[11px] text-gray-500">
                  Credits: <b>{credits === null ? "—" : credits}</b> • Modati 3 requests FREE • Decline aithe refund
                </div>
              </div>
            </div>

            <div className="space-y-4">
              {lastSend ? (
                <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
                  <div className="font-bold text-emerald-900">✅ {lastSend.request_id} pampincharu</div>
                  <div className="text-[12px] text-emerald-900 mt-1">
                    ⭐ {lastSend.score}% match • ⏳ {lastSend.expires_in_days} days valid • credits migilayi <b>{lastSend.credits_left}</b>
                  </div>
                  <div className="text-[12px] text-emerald-900 mt-2">
                    📲 WhatsApp: {lastSend.whatsapp?.owner_queued ? "owner ki queue ayyindi" : "queue avvaledu (WHATSAPP_MODE chudu)"} • {lastSend.whatsapp?.anti_ban}
                  </div>
                  <button onClick={() => setShowOwnerMsg(!showOwnerMsg)} className="mt-3 text-[12px] font-bold text-emerald-800 underline">
                    {showOwnerMsg ? "Message daachi pettu" : "Vaallaki velle message chudu (preview)"}
                  </button>
                  {showOwnerMsg && (
                    <pre className="mt-2 text-[11px] whitespace-pre-wrap bg-white border border-emerald-200 rounded-xl p-3 max-h-72 overflow-auto">{lastSend.owner_message_preview}</pre>
                  )}
                </div>
              ) : (
                <div className="bg-cream border border-gold/30 rounded-2xl p-5">
                  <div className="font-bold text-maroon">Ela pani chestundi?</div>
                  <ol className="mt-2 text-[12px] text-gray-700 space-y-1 list-decimal list-inside">
                    <li>Mee ID + vaalla ID ivvandi → request pampistham (1 credit)</li>
                    <li>Vaallaki mana WhatsApp nunchi mee profile card + details</li>
                    <li>Vaallu Accept chesthe — rendu numbers automatic ga WhatsApp lo</li>
                    <li>Decline/expire aithe — mee credit refund (expire ki kooda)</li>
                  </ol>
                  <div className="mt-3 text-[11px] text-gray-600">🚫 Chatting ledu — consent-based contact exchange matrame. Fake ids, spam calls block.</div>
                </div>
              )}

              {wa?.antiban && (
                <div className="bg-navy text-white rounded-2xl p-4">
                  <div className="font-bold text-[13px]">🛡️ WhatsApp anti-ban status</div>
                  <div className="mt-2 text-[11px] opacity-90 grid grid-cols-2 gap-1">
                    <span>Gap: {wa.antiban.random_gap}</span>
                    <span>Roju cap: {wa.antiban.daily_cap}</span>
                    <span>Today sent: {wa.antiban.sent_today}</span>
                    <span>Queue: {wa.queued}</span>
                    <span>Type sim: {wa.antiban.sent_since_break >= 0 ? "ON" : "OFF"}</span>
                    <span>Hours: {wa.antiban.active_hours_ist?.[0]}–{wa.antiban.active_hours_ist?.[1]} IST</span>
                  </div>
                  <div className="text-[10px] opacity-70 mt-2">Telegram post ayyaka → WhatsApp (random gap) — ban risk thakkuva</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* PLANS */}
        {tab === "plans" && (
          <div>
            <SectionHeading eyebrow="Credits" title="Plans — 1 credit = 1 profile" subtitle="Decline aithe credit refund. Razorpay live ayyaka automatic — ippudu UPI link tho." telugu align="left" />
            <div className="mt-4 grid md:grid-cols-3 gap-4">
              {plans.map((p, i) => (
                <Reveal key={p.code} delay={i * 80}>
                  <div className={`bg-white rounded-2xl p-5 card-shadow border h-full ${p.code === "S_299" ? "border-gold" : "border-gold/20"}`}>
                    {p.badge && <div className="text-[10px] font-bold text-gold-deep tracking-widest uppercase">{p.badge}</div>}
                    <div className="text-2xl font-bold text-maroon mt-1">₹{p.price}</div>
                    <div className="font-bold text-[14px] text-ink">{p.profiles} profiles</div>
                    <div className="text-[11px] text-gray-500">₹{p.per_profile}/profile • {p.label}</div>
                    <ul className="mt-3 text-[12px] text-gray-700 space-y-1">
                      <li>✅ {p.profiles} interest requests</li>
                      <li>✅ WhatsApp lo profile share</li>
                      <li>✅ Accept aithe number exchange</li>
                      <li>✅ Decline aithe refund</li>
                    </ul>
                    <button
                      onClick={() => buy(p.code)}
                      disabled={busy || !myId}
                      className="mt-4 w-full gold-gradient text-maroon font-bold py-2.5 rounded-xl hover-lift disabled:opacity-50"
                    >
                      {myId ? `₹${p.price} pay → ${p.profiles} profiles` : "Mee TSAP ID ivvandi"}
                    </button>
                  </div>
                </Reveal>
              ))}
            </div>
            <div className="mt-4 text-[12px] text-gray-600 bg-cream border border-gold/30 rounded-2xl p-4">
              💡 <b>Free plan:</b> register cheyagane 3 interest requests FREE. <b>Referral:</b> friend ni pilichi vaallu ₹99 pay chesthe meeku ₹50 +
              vaallaki extra credit. <b>Bureau/agents:</b> ₹999/mo → 25 profiles + monthly report.
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

function Empty({ text }: { text: string }) {
  return (
    <div className="bg-white rounded-2xl p-6 text-center card-shadow border border-gold/20">
      <div className="text-3xl">💌</div>
      <div className="text-[13px] text-gray-600 mt-2">{text}</div>
    </div>
  );
}
