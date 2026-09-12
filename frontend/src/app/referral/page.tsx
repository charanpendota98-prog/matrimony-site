"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function ReferralPage(){
  const [code, setCode] = useState("TSAP-REF-1042");
  const [stats, setStats] = useState({total:12, paid:8, earned:240, credits:6});

  useEffect(()=>{
    const profiles = JSON.parse(localStorage.getItem("tsap_profiles")||"[]");
    if(profiles.length>0) setCode(profiles[0].id.replace("TSAP-","TSAP-REF-"));
  },[]);

  const leaderboard = [
    {name:"Raju Broker", code:"RAJ01", refers:42, paid:35, earned:1750, bonus:500},
    {name:"Sai Bureau", code:"SAI01", refers:38, paid:30, earned:1500, bonus:500},
    {name:"Lakshmi (Lady)", code:"LAK42", refers:28, paid:20, earned:1000, bonus:0},
    {name:"Nuvvu", code:code, refers:stats.total, paid:stats.paid, earned:stats.earned, bonus:0, me:true},
  ];

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">👥 Referral Program — Earn upto ₹30 per pay</div>
          <Link href="/register" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Share</Link>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E]">Naa Referral Code</h2>
            <div className="mt-4 bg-[#FFF8E7] border-2 border-[#D4AF37] rounded-2xl p-4 text-center">
              <div className="text-xs text-gray-500">Me Code</div>
              <div className="text-2xl font-bold text-[#7A0C2E]">{code}</div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                <div className="bg-white rounded-xl p-2">Link:<br/><span className="font-mono text-[10px]">tsapmatrimony.com/r/{code}</span></div>
                <div className="bg-white rounded-xl p-2">Bot Link:<br/><span className="font-mono text-[10px]">t.me/tsap_bot?start=ref_{code}</span></div>
              </div>
              <div className="mt-3 flex gap-2">
                <button className="flex-1 py-2 bg-[#25D366] text-white rounded-full text-xs font-bold">WhatsApp Share</button>
                <button className="flex-1 py-2 bg-[#0088cc] text-white rounded-full text-xs font-bold">Telegram Share</button>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-4 gap-2 text-center">
              <div className="bg-gray-50 rounded-xl p-3"><div className="font-bold text-lg">{stats.total}</div><div className="text-[10px]">Total Refers</div></div>
              <div className="bg-green-50 rounded-xl p-3"><div className="font-bold text-lg text-green-600">{stats.paid}</div><div className="text-[10px]">Paid</div></div>
              <div className="bg-[#FFF8E7] rounded-xl p-3"><div className="font-bold text-lg text-[#7A0C2E]">₹{stats.earned}</div><div className="text-[10px]">Earned</div></div>
              <div className="bg-blue-50 rounded-xl p-3"><div className="font-bold text-lg">{stats.credits}</div><div className="text-[10px]">Free Credits</div></div>
            </div>

            <div className="mt-4 bg-blue-50 rounded-xl p-3 text-xs">
              <div className="font-bold">💸 Ela Sampadistharu?</div>
              <div className="mt-1">• Me link tho register + ₹99 pay → Meeku ₹20 or 2 credits<br/>• Broker code (BROKER-xxx) → ₹30 per pay<br/>• 25 pays/month → ₹500 bonus + 10 profiles share<br/>• Payout: Weekly UPI via RazorpayX</div>
            </div>

            <button className="w-full mt-4 py-3 maroon-gradient text-white rounded-full font-bold text-sm">💰 Withdraw ₹{stats.earned} → UPI</button>
          </div>

          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E]">🏆 Leaderboard — Top Referrers</h2>
            <p className="text-xs text-gray-500 telugu">Highest refer chesina vallaki weekly ₹1000 prize + VIP badge</p>
            <div className="mt-4 space-y-3">
              {leaderboard.sort((a,b)=>b.refers-a.refers).map((l,i)=>(
                <div key={l.code} className={`flex items-center gap-3 p-3 rounded-xl ${l.me?'bg-[#D4AF37]/20 border border-[#D4AF37]':'bg-gray-50'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs ${i===0?'bg-yellow-400':i===1?'bg-gray-300':i===2?'bg-orange-300':'bg-white'}`}>{i+1}</div>
                  <div className="flex-1">
                    <div className="font-bold text-sm flex items-center gap-2">{l.name} {l.me&&<span className="text-[10px] bg-[#7A0C2E] text-white px-2 py-0.5 rounded-full">YOU</span>}</div>
                    <div className="text-[11px] text-gray-500">{l.code} • {l.refers} refers • {l.paid} paid</div>
                  </div>
                  <div className="text-right"><div className="font-bold text-sm text-green-600">₹{l.earned + l.bonus}</div><div className="text-[10px] text-gray-500">{l.bonus?`+₹${l.bonus} bonus`:''}</div></div>
                </div>
              ))}
            </div>

            <div className="mt-6 bg-[#0F1F3C] text-white rounded-xl p-4">
              <div className="font-bold text-sm text-[#D4AF37]">🏢 Bureau B2B — Special</div>
              <div className="text-xs opacity-80 mt-1">Already bureau run chesthunara? ₹999/mo → 100 white-label profiles + 25 credits + dashboard. 25 paid users guarantee tecchali.</div>
              <Link href="/bureau" className="inline-block mt-3 px-4 py-2 bg-white text-[#0F1F3C] rounded-full text-xs font-bold">Bureau Dashboard →</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
