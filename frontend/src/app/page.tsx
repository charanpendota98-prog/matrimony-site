"use client";
import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [searchId, setSearchId] = useState("");

  const mainChannels = [
    { name: "TS Brides 👰", id: "TS Brides", members: "LIVE", color: "maroon", username: "@TSBRIDE", link: "https://t.me/TSBRIDE" },
    { name: "TS Grooms 🤵", id: "TS Grooms", members: "LIVE", color: "navy", username: "@TSGROOM1", link: "https://t.me/TSGROOM1" },
    { name: "AP Brides 👰", id: "AP Brides", members: "Soon", color: "maroon", username: "@APBRIDE", link: "#" },
    { name: "AP Grooms 🤵", id: "AP Grooms", members: "Soon", color: "navy", username: "@APGROOM1", link: "#" },
  ];

  const casteChannels = [
    { name: "Reddy", members: "4.2k", hot: true },
    { name: "Kamma", members: "3.8k", hot: true },
    { name: "Kapu", members: "3.1k", hot: false },
    { name: "Velama", members: "2.5k", hot: true },
    { name: "Vysya", members: "1.9k", hot: false },
    { name: "Brahmin", members: "1.5k", hot: false },
    { name: "Goud", members: "2.2k", hot: false },
    { name: "Yadav", members: "1.8k", hot: false },
  ];

  const special = [
    { name: "💔 2nd Marriage", desc: "Divorced/Widow — respectful", count: "1.2k" },
    { name: "♿ Handicapped", desc: "Special needs — separate care", count: "450" },
    { name: "👮 Govt Jobs", desc: "Govt job only — hot", count: "2.8k" },
    { name: "🌍 NRI", desc: "USA, Gulf, Abroad", count: "1.5k" },
  ];

  const leaderboard = [
    { name: "Raju Broker", refers: 42, earned: "₹1260" },
    { name: "Sai Bureau", refers: 38, earned: "₹1140" },
    { name: "Lakshmi", refers: 28, earned: "₹560" },
  ];

  return (
    <div className="min-h-screen bg-[#FFF8E7]">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-[#D4AF37]/20">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 maroon-gradient rounded-xl flex items-center justify-center text-white font-bold text-xl">T</div>
            <div>
              <div className="font-bold text-[#7A0C2E] leading-none">TSAP Matrimony</div>
              <div className="text-[10px] text-gray-500 telugu">TS + AP No.1 • ₹99 ke</div>
            </div>
          </div>
          <div className="flex gap-2">
            <Link href="/search/TSAP-M-2025-1042" className="px-3 py-2 text-xs border border-[#7A0C2E] text-[#7A0C2E] rounded-full font-semibold">🔍 ID Search</Link>
            <Link href="/register" className="px-4 py-2 text-xs maroon-gradient text-white rounded-full font-bold shadow">🚀 Register</Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 pt-6 pb-8">
        <div className="maroon-gradient rounded-[2rem] p-6 md:p-10 text-white relative overflow-hidden card-shadow">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[#D4AF37]/20 rounded-full blur-3xl"></div>
          <div className="relative z-10 grid md:grid-cols-2 gap-6 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur px-3 py-1 rounded-full text-xs mb-3">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span> 12,543+ Active Profiles • Live
              </div>
              <h1 className="text-3xl md:text-5xl font-bold leading-tight">
                TS-AP Matrimony<br />
                <span className="text-[#FFD700]">₹99 ke Sambandham</span><br />
                <span className="text-xl md:text-2xl font-normal opacity-90 telugu">మొదటి 3 సంబంధాలు FREE!</span>
              </h1>
              <p className="mt-3 text-sm md:text-base opacity-90 telugu">
                Telegram + WhatsApp + Website — 3 min lo register, caste-wise channels, photo-private, broker referral, AI matching — never before!
              </p>
              <div className="mt-5 flex flex-wrap gap-3">
                <Link href="/register" className="px-6 py-3 bg-white text-[#7A0C2E] rounded-full font-bold text-sm shadow-lg hover:scale-105 transition">
                  🚀 Telugu lo Register — 3 min
                </Link>
                <a href="https://t.me/telugumatrimony1_bot" target="_blank" className="px-6 py-3 bg-[#D4AF37] text-[#7A0C2E] rounded-full font-bold text-sm shadow">
                  🤖 Telegram Bot Open — @telugumatrimony1_bot
                </a>
              </div>
              <div className="mt-4 flex gap-4 text-xs">
                <span>✅ OTP Verified</span><span>✅ Photo-Private</span><span>✅ ₹99 Only</span>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white rounded-[1.5rem] p-4 text-gray-800 card-shadow float">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-[#7A0C2E] to-[#A0143A] rounded-full flex items-center justify-center text-white">👰</div>
                  <div>
                    <div className="font-bold text-sm">TSAP-F-2025-1042 • 24y • Reddy</div>
                    <div className="text-xs text-gray-500">BTech, Software @ Hyd • Nalgonda</div>
                  </div>
                  <div className="ml-auto text-[10px] bg-green-100 text-green-700 px-2 py-1 rounded-full">✅ Verified</div>
                </div>
                <div className="bg-[#FFF8E7] rounded-xl p-3 text-xs space-y-1">
                  <div className="font-semibold text-[#7A0C2E]">⭐ 92% BEST MATCH — Meeku Perfect!</div>
                  <div>✅ Nuvvu Hyd kavali annavu → Ammai kooda Hyd lone</div>
                  <div>✅ Nuvvu Software annavu → Ammai kooda Software</div>
                  <div>✅ Reddy + Age gap 3 years perfect</div>
                </div>
                <div className="mt-3 flex gap-2">
                  <button className="flex-1 py-2 bg-[#7A0C2E] text-white rounded-full text-xs font-bold">❤️ Interest</button>
                  <button className="flex-1 py-2 border border-[#D4AF37] text-[#7A0C2E] rounded-full text-xs font-bold">📞 Number (1 Credit)</button>
                </div>
                <div className="mt-2 text-[10px] text-center text-gray-400">ID: TSAP-F-2025-1042 • #Reddy #TS #Bride #Age24</div>
              </div>
            </div>
          </div>
        </div>

        {/* Search ID bar */}
        <div className="mt-4 bg-white rounded-full p-2 flex items-center gap-2 card-shadow max-w-2xl mx-auto">
          <div className="pl-4 text-gray-400">🔍</div>
          <input value={searchId} onChange={e=>setSearchId(e.target.value)} placeholder="ID tho search cheyyi — TSAP-1042" className="flex-1 outline-none text-sm py-2" />
          <Link href={`/search/${searchId || "TSAP-M-2025-1042"}`} className="px-5 py-2 maroon-gradient text-white rounded-full text-sm font-bold">Search</Link>
        </div>
      </section>

      {/* Main 4 Channels */}
      <section className="max-w-7xl mx-auto px-4 py-6">
        <h2 className="text-xl font-bold text-[#7A0C2E]">📢 Main 4 Channels — Live Members tho</h2>
        <p className="text-xs text-gray-500 telugu">Main channels lo anni castes — daily 10+ kotha profiles</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3">
          {mainChannels.map(ch=>(
            <div key={ch.id} className={`rounded-2xl p-4 text-white card-shadow ${ch.color==='maroon'?'maroon-gradient':'navy-gradient'}`}>
              <div className="text-sm font-bold">{ch.name}</div>
              <div className="text-xs opacity-80 mt-1">{ch.members} members • 20+ today</div>
              <div className="mt-3 flex gap-2">
                <span className="text-[10px] bg-white/20 px-2 py-1 rounded-full">{ch.username}</span>
                <span className="text-[10px] bg-[#D4AF37] text-[#7A0C2E] px-2 py-1 rounded-full font-bold">Join</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Caste + Special */}
      <section className="max-w-7xl mx-auto px-4 py-6 grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <h2 className="text-xl font-bold text-[#7A0C2E]">💍 Caste-Wise Channels — 1 Caste = 1 Channel</h2>
          <p className="text-xs text-gray-500 telugu">Mee caste channel lo join avvandi — same caste profiles easy ga</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3">
            {casteChannels.map(c=>(
              <div key={c.name} className="bg-white rounded-2xl p-3 card-shadow border border-[#D4AF37]/20 hover:scale-105 transition cursor-pointer">
                <div className="flex items-center justify-between">
                  <div className="font-bold text-sm text-[#7A0C2E]">{c.name}</div>
                  {c.hot && <span className="text-[9px] bg-red-100 text-red-600 px-2 py-0.5 rounded-full">🔥 HOT</span>}
                </div>
                <div className="text-xs text-gray-500 mt-1">{c.members} • Today 5 new</div>
                <div className="mt-2 text-[10px] text-[#D4AF37] font-semibold">@tsap_{c.name.toLowerCase()}</div>
              </div>
            ))}
          </div>
          <Link href="/channels" className="inline-block mt-3 text-xs text-[#7A0C2E] font-bold border border-[#7A0C2E] px-4 py-2 rounded-full">📂 Anni 20 Caste Channels Chudu →</Link>
        </div>
        <div>
          <h2 className="text-lg font-bold text-[#7A0C2E]">✨ Special Categories</h2>
          <div className="space-y-3 mt-3">
            {special.map(s=>(
              <div key={s.name} className="bg-white rounded-2xl p-3 card-shadow flex items-center gap-3">
                <div className="w-10 h-10 bg-[#FFF8E7] rounded-xl flex items-center justify-center text-lg">{s.name.split(' ')[0]}</div>
                <div className="flex-1">
                  <div className="font-bold text-sm">{s.name}</div>
                  <div className="text-[11px] text-gray-500">{s.desc}</div>
                </div>
                <div className="text-[11px] bg-[#7A0C2E] text-white px-2 py-1 rounded-full">{s.count}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works + Pricing */}
      <section className="max-w-7xl mx-auto px-4 py-6 grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
          <h3 className="font-bold text-[#7A0C2E]">⚡ 3 Steps lo Ela Panichestundi?</h3>
          <div className="mt-4 space-y-4">
            {[
              { n: "1", t: "Form Fill (2 min) — Telugu lo", d: "Age, Caste, District, Mandal, Photo, Phone OTP, Referral. Typing <10 words." },
              { n: "2", t: "ID + Card + Top 3 FREE (5 sec)", d: "TSAP-2025-1042 ID + neat card + 92% match reason tho 3 profiles FREE (numbers lock)" },
              { n: "3", t: "₹99 Pay → Numbers + Daily Auto", d: "UPI pay → 10 numbers instant + rojoo 2 matches WhatsApp/Telegram lo + Family group auto" },
            ].map(s=>(
              <div key={s.n} className="flex gap-3">
                <div className="w-8 h-8 maroon-gradient text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">{s.n}</div>
                <div><div className="font-bold text-sm">{s.t}</div><div className="text-xs text-gray-500 mt-1">{s.d}</div></div>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
          <h3 className="font-bold text-[#7A0C2E]">💰 Plans — Simple, Affordable</h3>
          <div className="mt-4 grid grid-cols-3 gap-3">
            {[
              { name: "FREE", price: "₹0", credits: "3 profiles (lock)", features: ["Top 3 FREE", "ID Search", "Week 1 auto"], color: "gray" },
              { name: "Trial", price: "₹99", credits: "10 Credits", features: ["10 numbers", "Daily 2", "30 days", "Reason"], color: "gold", popular: true },
              { name: "Premium", price: "₹299", credits: "50 Credits", features: ["50 numbers", "Daily 5", "60 days", "Priority"], color: "maroon" },
            ].map(p=>(
              <div key={p.name} className={`rounded-2xl p-3 border-2 ${p.popular?'border-[#D4AF37] bg-[#FFF8E7]':'border-gray-100'} relative`}>
                {p.popular && <div className="absolute -top-2 left-1/2 -translate-x-1/2 text-[9px] bg-[#D4AF37] text-[#7A0C2E] px-2 py-0.5 rounded-full font-bold">POPULAR</div>}
                <div className="font-bold text-sm">{p.name}</div>
                <div className="text-xl font-bold text-[#7A0C2E]">{p.price}</div>
                <div className="text-[10px] text-gray-500">{p.credits}</div>
                <div className="mt-2 space-y-1">
                  {p.features.map(f=><div key={f} className="text-[10px]">✅ {f}</div>)}
                </div>
                <button className={`w-full mt-3 py-2 rounded-full text-xs font-bold ${p.color==='maroon'?'maroon-gradient text-white':p.color==='gold'?'gold-gradient text-[#7A0C2E]':'bg-gray-100'}`}>Pay</button>
              </div>
            ))}
          </div>
          <div className="mt-3 text-[11px] text-gray-500 telugu">💡 1000 registers → 200×₹99 = ₹19,800 + 50×₹299 = ₹14,950 = ₹35k/mo. Bureau tho ₹70k!</div>
        </div>
      </section>

      {/* Referral Leaderboard + Bureau */}
      <section className="max-w-7xl mx-auto px-4 py-6 grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
          <h3 className="font-bold text-[#7A0C2E]">🏆 Referral Leaderboard — Top Earners</h3>
          <p className="text-xs text-gray-500 telugu">Mee link share cheyyi — per pay ki ₹30, 25 pays ki ₹500 bonus</p>
          <div className="mt-4 space-y-2">
            {leaderboard.map((l,i)=>(
              <div key={l.name} className="flex items-center gap-3 p-2 bg-[#FFF8E7] rounded-xl">
                <div className="w-8 h-8 bg-[#7A0C2E] text-white rounded-full flex items-center justify-center font-bold text-xs">{i+1}</div>
                <div className="flex-1"><div className="font-bold text-sm">{l.name}</div><div className="text-xs text-gray-500">{l.refers} refers</div></div>
                <div className="font-bold text-sm text-green-600">{l.earned}</div>
              </div>
            ))}
          </div>
          <Link href="/referral" className="mt-3 inline-block text-xs bg-[#7A0C2E] text-white px-4 py-2 rounded-full font-bold">👥 Naa Referral Code Chudu →</Link>
        </div>
        <div className="navy-gradient rounded-[1.5rem] p-6 text-white card-shadow">
          <h3 className="font-bold">🏢 Bureau B2B — Marriage Bureaus ki Special</h3>
          <p className="text-xs opacity-80 mt-1 telugu">Already bureau nadipisthunara? Mana profiles share + commission</p>
          <div className="mt-4 bg-white/10 backdrop-blur rounded-xl p-3">
            <div className="font-bold text-sm">Bureau Starter — ₹999/mo</div>
            <div className="text-xs opacity-80 mt-1">✅ 100 white-label profiles (mee peru tho card)<br/>✅ 25 credits + Dashboard<br/>✅ Per client ₹30 commission + extra charge meere</div>
          </div>
          <div className="mt-3 flex gap-2">
            <Link href="/bureau" className="px-4 py-2 bg-white text-[#0F1F3C] rounded-full text-xs font-bold">Bureau Dashboard →</Link>
            <span className="px-4 py-2 bg-[#D4AF37] text-[#0F1F3C] rounded-full text-xs font-bold">10 Bureaus Joined</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-8 bg-[#0F1F3C] text-white py-8">
        <div className="max-w-7xl mx-auto px-4 grid md:grid-cols-4 gap-6 text-sm">
          <div>
            <div className="font-bold text-[#D4AF37]">TSAP Matrimony</div>
            <div className="text-xs opacity-70 mt-2 telugu">TS + AP No.1 — Bot + Website + Channels — ₹99 ke sambandham — First 3 FREE — Telugu lo</div>
            <div className="mt-3 text-xs">📱 Telegram: @tsap_bot<br/>📢 Channels: 25<br/>🏢 Bureau: 10 joined</div>
          </div>
          <div>
            <div className="font-bold">Main Links</div>
            <div className="mt-2 space-y-1 text-xs opacity-70">
              <div><Link href="/register">Register</Link></div>
              <div><Link href="/channels">All Channels</Link></div>
              <div><Link href="/search/TSAP-1042">ID Search</Link></div>
              <div><Link href="/referral">Referral</Link></div>
            </div>
          </div>
          <div>
            <div className="font-bold">Trust</div>
            <div className="mt-2 space-y-1 text-xs opacity-70">
              <div>✅ OTP Verified</div>
              <div>✅ Photo-Private Mode</div>
              <div>✅ Selfie Verify</div>
              <div>✅ Family Group Auto</div>
            </div>
          </div>
          <div>
            <div className="font-bold">Contact</div>
            <div className="text-xs opacity-70 mt-2">Oracle VM Hosted<br/>Razorpay Secure<br/>Daily Backup<br/>⚠️ Direct money adigithe fraud — report!</div>
          </div>
        </div>
        <div className="text-center text-[11px] opacity-50 mt-6">© 2025 TSAP Matrimony • Made for TS/AP with ❤️ • More & More Advanced, Deep, Never Before</div>
      </footer>
    </div>
  );
}
