"use client";
import Link from "next/link";
import { Duo, duo } from "@/lib/duo";

export default function BureauPage(){
  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">🏢 <Duo en="Bureau — Best Advanced Offer — 3 Plans" te="బ్యూరో — 3 ప్లాన్లు" /></div>
          <Link href="/referral/register" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">{duo("Bureau Register", "బ్యూరో నమోదు")} →</Link>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          {/* Starter */}
          <div className="bg-white rounded-[1.5rem] p-5 card-shadow border border-gray-100">
            <div className="flex justify-between items-start">
              <div><div className="font-bold">Bureau Starter</div><div className="text-xs text-gray-500">Small bureaus — simple</div></div>
              <div className="text-[10px] bg-green-100 text-green-700 px-2 py-1 rounded-full">First ₹499</div>
            </div>
            <div className="mt-3"><span className="text-2xl font-bold text-[#7A0C2E]">₹999</span><span className="text-sm">/mo</span><span className="ml-2 text-xs line-through text-gray-400">₹999</span><span className="ml-1 text-xs text-green-600 font-bold">50% OFF first month ₹499</span></div>
            <div className="mt-4 text-xs space-y-2">
              <div>✅ 100 white-label profiles — card meeda "Via Sri Sai Bureau" + logo</div>
              <div>✅ Per client ₹30 (₹99) / ₹90 (₹299) commission</div>
              <div>✅ 25 credits + Dashboard + Verified Bureau ✅ badge</div>
              <div>✅ Short code SRI1 — easy — tsapmatrimony.com/r/SRI1 — auto fill lock</div>
              <div>✅ Lead Guarantee 25 paid/mo — lekapothe 10 extra free</div>
              <div>✅ Marketing posters with bureau name — free</div>
            </div>
            <div className="mt-3 bg-[#FFF8E7] rounded-xl p-2 text-[11px]">Profit: Client nunchi ₹500 charge → manaki ₹99 → meeku ₹401 + ₹30 = ₹431 ×25 = ₹10,775/mo</div>
            <button className="w-full mt-4 py-3 border border-[#7A0C2E] text-[#7A0C2E] rounded-full font-bold text-sm">Subscribe Starter — ₹999 (First ₹499)</button>
          </div>

          {/* Pro — Most Popular */}
          <div className="bg-white rounded-[1.5rem] p-5 card-shadow border-2 border-[#D4AF37] relative">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#D4AF37] text-[#7A0C2E] text-[10px] px-3 py-1 rounded-full font-bold">MOST POPULAR — BEST VALUE</div>
            <div className="flex justify-between items-start mt-2">
              <div><div className="font-bold">Bureau Pro 🚀</div><div className="text-xs text-gray-500">Medium — advanced — best</div></div>
              <div className="text-[10px] bg-[#D4AF37] text-[#7A0C2E] px-2 py-1 rounded-full font-bold">First ₹1499</div>
            </div>
            <div className="mt-3"><span className="text-2xl font-bold text-[#7A0C2E]">₹2999</span><span className="text-sm">/mo</span><span className="ml-2 text-xs line-through">₹2999</span><span className="ml-1 text-xs text-green-600 font-bold">50% OFF first ₹1499</span></div>
            <div className="mt-4 text-xs space-y-2">
              <div>✅ <b>500 profiles + API access</b> — fetch/post profiles — advanced</div>
              <div>✅ <b>Unlimited credits</b> — no limit</div>
              <div>✅ <b>Custom domain</b> — srisai.tsapmatrimony.com — white-label website free!</div>
              <div>✅ <b>Telegram channel</b> @srisai_matrimony — we create + manage free</div>
              <div>✅ Per client ₹33 + 10% extra + Bonus ₹500/₹1200</div>
              <div>✅ Marketing Poster+Video+Reels with bureau name — 3/month free</div>
              <div>✅ Training 1h + Verified + Priority + Featured Official 1/month</div>
              <div>✅ Lead Guarantee 100 paid/mo — lekapothe 50 extra free</div>
            </div>
            <div className="mt-3 bg-green-50 rounded-xl p-2 text-[11px]">Profit: 100 clients × ₹431 = ₹43,100/mo + API + Website + Channel — ultra advanced!</div>
            <button className="w-full mt-4 py-3 maroon-gradient text-white rounded-full font-bold text-sm">Subscribe Pro — ₹2999 (First ₹1499) — Best!</button>
          </div>

          {/* Enterprise */}
          <div className="bg-white rounded-[1.5rem] p-5 card-shadow border border-gray-100">
            <div className="flex justify-between items-start">
              <div><div className="font-bold">Bureau Enterprise 🏢</div><div className="text-xs text-gray-500">Big — franchise level</div></div>
              <div className="text-[10px] bg-gray-900 text-white px-2 py-1 rounded-full">First ₹4999</div>
            </div>
            <div className="mt-3"><span className="text-2xl font-bold">₹9999</span><span className="text-sm">/mo</span><span className="ml-2 text-xs line-through">₹9999</span><span className="ml-1 text-xs text-green-600 font-bold">50% OFF first ₹4999</span></div>
            <div className="mt-4 text-xs space-y-2">
              <div>✅ Unlimited profiles + Full API + Webhook</div>
              <div>✅ 40% revenue share — ₹40 per ₹99</div>
              <div>✅ Own domain srisaimatrimony.com — we build + host + maintain</div>
              <div>✅ Telegram + WhatsApp Community + Channel — we manage</div>
              <div>✅ FB Ads ₹5000/mo we run free + Google Ads</div>
              <div>✅ Franchise — sub-bureaus open → 10% commission passive</div>
              <div>✅ Dedicated manager + Lead Guarantee 300/mo</div>
            </div>
            <div className="mt-3 bg-blue-50 rounded-xl p-2 text-[11px]">Profit: 300 clients × ₹500+ = ₹1.5L/mo + franchise passive — enterprise!</div>
            <button className="w-full mt-4 py-3 bg-gray-900 text-white rounded-full font-bold text-sm">Subscribe Enterprise — ₹9999 (First ₹4999)</button>
          </div>
        </div>

        <div className="mt-6 grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h3 className="font-bold text-[#7A0C2E]">📊 My Bureau Stats (Mock)</h3>
            <div className="mt-4 grid grid-cols-4 gap-3 text-center">
              <div className="bg-gray-50 rounded-xl p-3"><div className="font-bold text-xl">42</div><div className="text-[11px]">Clients Added</div></div>
              <div className="bg-green-50 rounded-xl p-3"><div className="font-bold text-xl text-green-600">30</div><div className="text-[11px]">Paid</div></div>
              <div className="bg-[#FFF8E7] rounded-xl p-3"><div className="font-bold text-xl text-[#7A0C2E]">₹900</div><div className="text-[11px]">Earned</div></div>
              <div className="bg-blue-50 rounded-xl p-3"><div className="font-bold text-xl">₹500</div><div className="text-[11px]">Bonus</div></div>
            </div>
            <div className="mt-4">
              <div className="font-bold text-sm">My Clients — Short Code SRI1</div>
              <div className="text-xs text-gray-500">Link: tsapmatrimony.com/r/SRI1 — auto fill lock — 5 chars short!</div>
              <div className="mt-2 space-y-2">
                {[
                  {id:"TSAP-F-1042", name:"Reddy Bride 24", status:"Paid ₹99", commission:"₹30"},
                  {id:"TSAP-M-1043", name:"Kamma Groom 27", status:"Paid ₹299", commission:"₹90"},
                ].map(c=>(
                  <div key={c.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-xl text-sm">
                    <div><span className="font-bold">{c.id}</span> — {c.name}</div>
                    <div className="flex gap-2 items-center"><span className="text-xs bg-white px-2 py-1 rounded-full">{c.status}</span><span className="text-xs font-bold text-green-600">{c.commission}</span></div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-[#0F1F3C] text-white rounded-[1.5rem] p-6">
              <h3 className="font-bold text-[#D4AF37]">Short Code — 5 Chars — Smart! SRI1</h3>
              <div className="mt-3 text-xs space-y-2 opacity-90">
                <div>• Old: BUREAU-SRI-01 (13 chars) peddaga</div>
                <div>• New: SRI1 (4 chars) / SAI01 (5 chars) — short, easy enter!</div>
                <div>• 3 letters (SRI) + 1-2 digits (1) = 4-5 chars — best!</div>
                <div>• Link: tsapmatrimony.com/r/SRI1 — neat, attractive, easy type phone lo</div>
                <div>• Auto fill lock: /r/SRI1 → /register?ref=SRI1 → auto fill + 🔒 lock + "Sri Sai Bureau dwara — trusted!"</div>
                <div>• Custom: Bureau can choose own short code if available — SRI1, SAI01, SS01</div>
              </div>
            </div>
            <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
              <h3 className="font-bold text-[#7A0C2E]">Offer Pitch — Copy-Paste Telugu</h3>
              <div className="mt-3 bg-[#FFF8E7] rounded-xl p-3 text-[11px] font-mono">
                🙏 Namaste Sri Sai Bureau garu!<br/>
                TSAP Matrimony — ₹99 ke — First 3 FREE<br/>
                Bureau Pro — ₹2999 (First ₹1499 only!)<br/>
                ✅ 500 white-label + API + Custom domain srisai.tsapmatrimony.com<br/>
                ✅ Per client ₹33 + Bonus + Unlimited credits<br/>
                ✅ Telegram channel + Marketing 3/month free + Training<br/>
                ✅ Lead Guarantee 100/mo<br/>
                Profit: 100×₹431=₹43k/mo!<br/>
                Short Code: SRI1 — tsapmatrimony.com/r/SRI1 — auto fill lock!<br/>
                Join: tsapmatrimony.com/bureau/register<br/>
                Bot: @telugumatrimony1_bot
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
