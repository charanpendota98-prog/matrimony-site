"use client";
import Link from "next/link";

export default function ChannelsPage(){
  const main = [
    {name:"TS Brides 👰", user:"@TSBRIDE", members:"LIVE ✅", desc:"TS ammayilu — anni castes — Bot Admin", link:"https://t.me/TSBRIDE"},
    {name:"TS Grooms 🤵", user:"@TSGROOM1", members:"LIVE ✅", desc:"TS abbayilu — Bot Admin", link:"https://t.me/TSGROOM1"},
    {name:"AP Brides 👰", user:"@APBRIDE", members:"Soon", desc:"AP ammayilu — next", link:"#"},
    {name:"AP Grooms 🤵", user:"@APGROOM1", members:"Soon", desc:"AP abbayilu — next", link:"#"},
    {name:"📢 Official", user:"@TSAP_MATRIMONY", members:"Soon", desc:"Top 3/day, Success stories", link:"#"},
  ];
  const caste = ["Reddy (4.2k)","Kamma (3.8k)","Kapu (3.1k)","Velama (2.5k)","Vysya (1.9k)","Brahmin (1.5k)","Goud (2.2k)","Yadav (1.8k)","Mudiraj (1.2k)","Padmashali (900)","Raju (800)","SC-Mala (1.1k)","SC-Madiga (1k)","ST-Lambadi (700)","Muslim (600)","Christian (500)","Open (2k)"];
  const special = ["💔 2nd Marriage @tsap_second (1.2k)","♿ Handicapped @tsap_handicapped (450)","👮 Govt Jobs @tsap_govt (2.8k)","🌍 NRI @tsap_nri (1.5k)"];

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">📂 All Channels — 25 Total</div>
          <Link href="/register" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Register</Link>
        </div>

        <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
          <h2 className="font-bold text-[#7A0C2E]">Main 4 + Official — Day-1 Live</h2>
          <div className="grid md:grid-cols-2 gap-3 mt-3">
            {main.map(m=>(
              <div key={m.user} className="border rounded-2xl p-4 flex justify-between items-center">
                <div><div className="font-bold text-sm">{m.name}</div><div className="text-xs text-gray-500">{m.desc} • {m.members}</div><div className="text-[11px] text-[#D4AF37] mt-1">{m.user} • Deep link: t.me/tsap_bot?start=ch_{m.user.replace('@','')}</div></div>
                <button className="px-4 py-2 maroon-gradient text-white rounded-full text-xs font-bold">Join</button>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-6 grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E]">💍 Caste-Wise — 20 Channels (ONE per caste)</h2>
            <p className="text-xs text-gray-500 telugu">Caste × State × Gender = 80 channels chesthe fail — ONE per caste best, hashtags tho filter</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-3">
              {caste.map(c=>(
                <div key={c} className="bg-[#FFF8E7] rounded-xl p-3 text-sm font-bold text-[#7A0C2E] flex justify-between">
                  <span>{c.split(' ')[0]}</span><span className="text-xs text-gray-500">{c.match(/\(.*\)/)?.[0]}</span>
                </div>
              ))}
            </div>
            <div className="mt-3 text-xs bg-blue-50 p-3 rounded-xl">
              <span className="font-bold">Bot Auto-Router:</span> Reddy TS Bride approve → @ts_brides + @tsap_reddy auto post. One post = viral everywhere.
            </div>
          </div>
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E]">✨ Special — Separate Respect</h2>
            <div className="mt-3 space-y-2">
              {special.map(s=><div key={s} className="bg-gray-50 rounded-xl p-3 text-sm">{s}</div>)}
            </div>
            <div className="mt-4 text-xs text-gray-500">Launch Waves: Wave-1 Day-1 = 9 channels (Official+4 main+Reddy,Kamma,Kapu,Velama) min 20 profiles each before public link. Wave-2 Week-2 = +8, Wave-3 = +8 total 25.</div>
          </div>
        </div>

        <div className="mt-6 bg-[#0F1F3C] text-white rounded-[1.5rem] p-6">
          <h3 className="font-bold text-[#D4AF37]">🚀 Viral Footer — Every Post (Growth Engine)</h3>
          <div className="mt-3 bg-white/10 rounded-xl p-3 text-xs font-mono">
            ━━━━━━━━━━━━━━━<br/>
            👆 Nachinda? Number kavala? 👇<br/>
            🤖 Bot: @tsap_bot (First 3 FREE!)<br/>
            📂 Caste: Reddy | Kamma | Kapu | Velama | Vysya...<br/>
            🔍 ID Search: tsapmatrimony.com/search/TSAP-1042<br/>
            ⚠️ Number Bot lo pay tarvata matrame!
          </div>
        </div>
      </div>
    </div>
  );
}
