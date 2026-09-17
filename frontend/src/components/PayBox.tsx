"use client";
/**
 * 💳 WAVE 14 — SAFE-PAY BOX (pricing → order → Razorpay/manual-UPI → verify)
 * Amount SERVER computes — client amount nammamu. Secret eppudu frontend ki radhu.
 * Props: planCode (S_29..S_499), price (display), label.
 */
import { useState } from "react";
import { authHeaders } from "@/lib/api";

declare global { interface Window { Razorpay?: any } }

function loadRazorpay(): Promise<boolean> {
  if (typeof window === "undefined") return Promise.resolve(false);
  if (window.Razorpay) return Promise.resolve(true);
  return new Promise((res) => {
    const s = document.createElement("script");
    s.src = "https://checkout.razorpay.com/v1/checkout.js";
    s.onload = () => res(true);
    s.onerror = () => res(false);
    document.body.appendChild(s);
  });
}

export default function PayBox({ planCode, price, label }: { planCode: string; price: number; label: string }) {
  const [open, setOpen] = useState(false);
  const [offer, setOffer] = useState("");
  const [order, setOrder] = useState<any>(null);
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState("");
  const [utr, setUtr] = useState("");
  const [claimBusy, setClaimBusy] = useState(false);

  const myId = () => {
    try { return localStorage.getItem("tsap_id") || ""; } catch { return ""; }
  };

  const createOrder = async () => {
    const id = myId();
    if (!id) { setMsg("⚠️ Mundhu login/register cheyyandi (Mee TSAP ID kavali)"); return; }
    setBusy(true); setMsg("");
    try {
      const r = await fetch("/api/pay/order", {
        method: "POST", headers: { ...authHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({ tsap_id: id, purpose: "credits", ref: planCode, offer_code: offer.trim().toUpperCase() }),
      });
      const d = await r.json();
      if (!r.ok) { setMsg(d.detail || d.message_telugu || "Order fail"); setBusy(false); return; }
      setOrder(d.pay_order);
      setMsg(d.message_telugu || "");
    } catch { setMsg("Network problem — malli try cheyyandi"); }
    setBusy(false);
  };

  const submitClaim = async () => {
    if (!order) return;
    if (!/^\d{12}$/.test(utr.trim())) { setMsg("⚠️ UTR = 12 digits (GPay/PhonePe statement nunchi copy cheyyandi)"); return; }
    setClaimBusy(true); setMsg("");
    try {
      const r = await fetch("/api/pay/claim", {
        method: "POST", headers: { ...authHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: order.id, utr: utr.trim() }),
      });
      const d = await r.json();
      setMsg(r.ok ? (d.message_telugu || "✅ UTR vachindi!") : (d.detail || d.message_telugu || "Claim fail"));
      if (r.ok) { setOrder({ ...order, status: "claimed" }); setUtr(""); }
    } catch { setMsg("Network problem — malli try cheyyandi"); }
    setClaimBusy(false);
  };

  const payNow = async () => {
    if (!order) return;
    if (order.mode !== "razorpay" || !order.key_id) {
      setMsg(`💳 ${order.upi_id || "manavivaha@upi"} ki ₹${order.final_amount} pay chesi — kindha UTR (12 digits) ivvandi. Admin bank statement verify chesi confirm chesthadu 🙏 (Order: ${order.id})`);
      return;
    }
    const ok = await loadRazorpay();
    if (!ok || !window.Razorpay) { setMsg("⚠️ Razorpay load avvaledu — UPI manual tho try cheyyandi"); return; }
    if (!order.rzp_order_id) { setMsg("⚠️ Order ID ledu — kotha order create cheyyandi"); return; }
    const rzp = new window.Razorpay({
      key: order.key_id,
      order_id: order.rzp_order_id,
      amount: order.checkout_amount_paise,
      currency: "INR",
      name: "Mana Vivaha",
      description: order.label || label,
      handler: async (resp: any) => {
        setBusy(true);
        try {
          const r = await fetch("/api/pay/verify", {
            method: "POST", headers: { ...authHeaders(), "Content-Type": "application/json" },
            body: JSON.stringify({
              order_id: order.id, razorpay_order_id: resp.razorpay_order_id || "",
              razorpay_payment_id: resp.razorpay_payment_id, razorpay_signature: resp.razorpay_signature,
            }),
          });
          const d = await r.json();
          if (r.ok) { setDone(d.message_telugu || "✅ Payment success!"); setOrder(null); }
          else setMsg(d.detail || "Verify fail — amount cut ayithe support ki payment ID pampandi");
        } catch { setMsg("Verify error — payment ID tho support ni contact cheyyandi"); }
        setBusy(false);
      },
      prefill: {},
      theme: { color: "#7A0C2E" },
    });
    rzp.open();
  };

  if (done) return <div className="rounded-xl bg-green-50 border border-green-200 text-green-800 text-xs font-bold p-3">{done}</div>;

  if (!open)
    return (
      <button onClick={() => setOpen(true)}
        className="w-full rounded-xl bg-[#7A0C2E] text-white px-4 py-2.5 font-bold text-sm hover:bg-[#5f0923]">
        💳 {label} — Pay ₹{price}
      </button>
    );

  return (
    <div className="rounded-xl border border-[#7A0C2E]/20 bg-rose-50/50 p-3 space-y-2">
      {!order ? (
        <>
          <div className="flex gap-2">
            <input value={offer} onChange={(e) => setOffer(e.target.value)} placeholder="Offer code (DIWALI25…)"
              className="flex-1 rounded-lg border px-3 py-2 text-xs font-mono uppercase" aria-label="Offer code" />
            <button onClick={createOrder} disabled={busy}
              className="rounded-lg bg-[#7A0C2E] text-white px-4 py-2 text-xs font-bold disabled:opacity-50">
              {busy ? "⏳…" : "Order →"}
            </button>
          </div>
          <p className="text-[11px] text-gray-500">Amount server nunchi fix — offer auto-apply. Secret safe 🔒</p>
        </>
      ) : (
        <>
          <div className="text-xs font-bold text-[#7A0C2E]">
            Order {order.id} • ₹{order.final_amount}
            {order.discount ? <span className="ml-1 text-green-700">(−₹{order.discount} {order.offer_code})</span> : null}
          </div>
          {order.mode !== "razorpay" && (
            <div className="text-[11px] bg-white rounded-lg p-2 border space-y-2">
              <div>💳 UPI ID: <b className="font-mono">{order.upi_id}</b> • Amount: <b>₹{order.final_amount}</b></div>
              {order.status === "claimed" ? (
                <div className="font-bold text-green-700">✅ UTR vachindi — admin verify chestunnadu, thwaralone credits add 🙏</div>
              ) : (
                <div className="flex gap-2">
                  <input value={utr} onChange={(e) => setUtr(e.target.value.replace(/\D/g, "").slice(0, 12))}
                    placeholder="12-digit UTR" inputMode="numeric"
                    className="flex-1 rounded-lg border px-3 py-2 font-mono" aria-label="12-digit UTR" />
                  <button onClick={submitClaim} disabled={claimBusy}
                    className="rounded-lg bg-green-700 text-white px-3 py-2 font-bold disabled:opacity-50">
                    {claimBusy ? "⏳…" : "UTR pampu"}
                  </button>
                </div>
              )}
            </div>
          )}
          <button onClick={payNow} disabled={busy}
            className="w-full rounded-lg bg-green-700 text-white px-4 py-2 text-xs font-bold disabled:opacity-50">
            {order.mode === "razorpay" ? "💳 Razorpay tho Pay" : "✅ Pay chesanu — details chudandi"}
          </button>
          <button onClick={() => { setOrder(null); setMsg(""); }} className="text-[11px] underline text-gray-500">← Offer marchali</button>
        </>
      )}
      {msg && <p className="text-[11px] font-bold text-gray-700">{msg}</p>}
      <button onClick={() => { setOpen(false); setOrder(null); setMsg(""); }} className="text-[11px] underline text-gray-400">close</button>
    </div>
  );
}
