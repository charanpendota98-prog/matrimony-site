"use client";
import { useState } from "react";
import Link from "next/link";

export default function ReferralRegisterPage(){
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({name:"", phone:"", type:"Lady", district:"Nalgonda", contacts:"50+", upi:"", bankName:"", accountNo:"", ifsc:"", accountHolder:""});
  const [generated, setGenerated] = useState<any>(null);

  const handleGenerate = () => {
    const clean = form.name.replace(/[^a-zA-Z]/g,"").toUpperCase();
    const base = clean.substring(0,3).padEnd(3,"X"); // LAK
    const rand = Math.floor(10+Math.random()*90);
    let code = `${base}${rand}`; // LAK42 — 5 chars short!

    const existing = JSON.parse(localStorage.getItem("tsap_referrers")||"[]").map((r:any)=>r.code);
    if(existing.includes(code)) code = `${base}${rand+1}`;

    const dual = form.type==="Lady" ? `TSAP${rand}` : "";

    setGenerated({
      code,
      dual,
      type: form.type,
      name: form.name,
      upi: form.upi,
      link: `tsapmatrimony.com/r/${code}`,
      botLink: `t.me/telugumatrimony1_bot?start=r_${code.toLowerCase()}`,
      commission: form.type==="Broker" ? "₹50 per ₹99 (₹20 instant + ₹30 weekly) + Bonus" : form.type==="Bureau" ? "₹50 + 30% extra" : form.type==="Lady" ? "₹50 (₹20 instant + ₹30 weekly) + 3 credits + Trusted badge" : form.type==="Student" || form.type==="Influencer" ? "₹50 + 3 credits extra" : "₹50 + 2 credits",
      badge: form.type==="Lady" ? "Ladies Trusted ✅ + Priority" : form.type==="Broker" ? "Verified Broker ✅" : form.type==="Bureau" ? "Verified Bureau ✅" : form.type==="Student" ? "Student 🎓 + Extra" : form.type==="Influencer" ? "Influencer 📱 + Boost" : "Trusted",
      shortExplain: `3 letters (${base}) + 2 digits (${rand}) = 5 chars — short, smart, easy! — ${code}`,
    });
    setStep(3);
    const existingAll = JSON.parse(localStorage.getItem("tsap_referrers")||"[]");
    existingAll.push({code, name:form.name, type:form.type, phone:form.phone, district:form.district, upi:form.upi, bank:form.accountNo?{name:form.bankName, acc:form.accountNo, ifsc:form.ifsc, holder:form.accountHolder}:null, created:new Date().toISOString(), wallet:0, pending:0});
    localStorage.setItem("tsap_referrers", JSON.stringify(existingAll));
    // Also save to admin list
    const adminList = JSON.parse(localStorage.getItem("tsap_admin_payouts")||"[]");
    adminList.push({code, name:form.name, phone:form.phone, type:form.type, upi:form.upi, bank:form.accountNo?`${form.accountHolder} - ${form.accountNo} - ${form.ifsc}`:"", total:0, paid:0, earned:0, pending:0, status:"New", lastPayout:"Never"});
    localStorage.setItem("tsap_admin_payouts", JSON.stringify(adminList));
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">👥 Referral Register — Smart Short Code + ₹50</div>
          <Link href="/referral" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Dashboard</Link>
        </div>

        <div className="bg-white rounded-full p-2 flex gap-2 mb-6 card-shadow">
          {[1,2,3].map(s=>(
            <div key={s} className={`flex-1 py-2 rounded-full text-center text-xs font-bold ${step>=s?'maroon-gradient text-white':'bg-gray-100 text-gray-400'}`}>
              {s===1?'Basic':s===2?'Payout UPI':'Code + Dashboard'} {step>s?'✅':''}
            </div>
          ))}
        </div>

        {step===1 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-xl text-[#7A0C2E]">👥 Referral lo Join — Per Pay ki ₹50! 🔥 No Thappu — Viral!</h2>
            <p className="text-xs text-gray-500 telugu mt-2">Ladies, Students, Influencers, Brokers — andaru referral — register avvakunda kooda earn — short code LAK42 — 5 chars easy!</p>

            <div className="mt-6 grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="text-xs font-bold">Me Peru</label>
                <input value={form.name} onChange={e=>setForm({...form, name:e.target.value})} placeholder="e.g. Lakshmi, Raju" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Phone (OTP)</label>
                <input value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} placeholder="98480xxxxx" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">District</label>
                <select value={form.district} onChange={e=>setForm({...form, district:e.target.value})} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Nalgonda</option><option>Hyderabad</option><option>Warangal</option><option>Karimnagar</option><option>Guntur</option><option>Vijayawada</option><option>All TS/AP</option>
                </select>
              </div>
              <div className="col-span-2">
                <label className="text-xs font-bold">Nenu Evaru? — Short Code 5 Chars — LAK42 — Easy!</label>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {[
                    {id:"Lady", label:"👩 Lady", desc:"LAK42 — ₹50 (₹20 instant + ₹30 weekly) + 3 credits + Trusted badge — super!"},
                    {id:"Student", label:"🎓 Student", desc:"RAJ11 — ₹50 + 3 credits extra — pocket money!"},
                    {id:"Influencer", label:"📱 Influencer", desc:"SAI22 — ₹50 + 3 credits + Official mention"},
                    {id:"Broker", label:"🤝 Broker", desc:"RAJ01 — ₹50 + Bonus ₹500 + Profiles share + Verified"},
                    {id:"Bureau", label:"🏢 Bureau", desc:"SRI1 — ₹50 + 30% extra + White-label + API"},
                    {id:"User", label:"👤 User", desc:"LAK42 — ₹50 + 2 credits"},
                  ].map(t=>(
                    <button key={t.id} onClick={()=>setForm({...form, type:t.id})} className={`p-3 rounded-xl border-2 text-left ${form.type===t.id?'border-[#D4AF37] bg-[#FFF8E7]':'border-gray-100 bg-gray-50'}`}>
                      <div className="font-bold text-sm">{t.label}</div>
                      <div className="text-[11px] text-gray-600 mt-1">{t.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs font-bold">Contacts Entha?</label>
                <select value={form.contacts} onChange={e=>setForm({...form, contacts:e.target.value})} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>50+</option><option>100+</option><option>200+</option><option>500+</option>
                </select>
              </div>
              <div className="flex items-center gap-2 mt-6">
                <input type="checkbox" defaultChecked />
                <span className="text-[11px]">Terms + Privacy + No fraud</span>
              </div>
            </div>

            <div className="mt-6 bg-blue-50 rounded-xl p-4 text-xs">
              <div className="font-bold">💰 ₹50 Commission — No Thappu — Viral Loop — LTV High!</div>
              <div className="mt-2 space-y-1 text-gray-600">
                <div>• First ₹99 pay ke ₹50 — 50% — viral — motivation high — 1 user → 5 refers → LTV ₹768</div>
                <div>• Code LAK42 short — 5 chars — easy enter — tsapmatrimony.com/r/LAK42</div>
                <div>• Link → auto fill lock + 1 extra credit for referred — smart!</div>
                <div>• Min withdrawal ₹150 OR 3 paid — fraud avoid</div>
              </div>
            </div>

            <button onClick={()=>setStep(2)} className="w-full mt-6 py-3 maroon-gradient text-white rounded-full font-bold">Next — Payout UPI (PhonePe) →</button>
          </div>
        )}

        {step===2 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E]">💰 Payout Details — Meeku Dabbu Ela? 📱 — Easy Advanced!</h2>
            <p className="text-xs text-gray-500 telugu">PhonePe / GooglePay UPI ID chalu — bank optional backup — list manaku vastundi admin lo — easy!</p>

            <div className="mt-4 space-y-4">
              <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4">
                <div className="font-bold text-sm text-green-700">📱 UPI ID (PhonePe/GooglePay/Paytm) — Must — 10 sec!</div>
                <div className="text-[11px] text-gray-600 mt-1">PhonePe → Profile → My UPI ID → Copy — e.g. 98480xxxxx@ybl, 98480xxxxx@okicici, lakshmi@paytm, OR just phone number 98480xxxxx — phone number kooda chalu!</div>
                <input value={form.upi} onChange={e=>setForm({...form, upi:e.target.value})} placeholder="e.g. 98480xxxxx@ybl or 98480xxxxx@okicici or 98480xxxxx (phone number chalu)" className="w-full mt-2 p-3 rounded-xl bg-white border-2 border-[#D4AF37] text-sm font-bold" />
                <div className="text-[10px] text-green-600 mt-2">✅ UPI chalu manual payout ki — PhonePe lo paste + amount + send — 10 sec! Phone number kooda chalu! Bank optional backup.</div>
              </div>

              <div className="bg-gray-50 rounded-xl p-4">
                <div className="font-bold text-sm">🏦 Bank Account (Optional Backup — if UPI fail) — Advanced Best</div>
                <div className="text-[11px] text-gray-500 mt-1">UPI fail ayithe bank ki send chestham — optional — UPI chalu ippudu — but bank backup best — 2 options!</div>
                <div className="mt-3 grid grid-cols-2 gap-3">
                  <div className="col-span-2">
                    <label className="text-xs font-bold">Account Holder Name</label>
                    <input value={form.accountHolder} onChange={e=>setForm({...form, accountHolder:e.target.value})} placeholder="e.g. Lakshmi" className="w-full mt-1 p-3 rounded-xl bg-white border text-sm" />
                  </div>
                  <div>
                    <label className="text-xs font-bold">Account Number</label>
                    <input value={form.accountNo} onChange={e=>setForm({...form, accountNo:e.target.value})} placeholder="1234567890" className="w-full mt-1 p-3 rounded-xl bg-white border text-sm" />
                  </div>
                  <div>
                    <label className="text-xs font-bold">IFSC</label>
                    <input value={form.ifsc} onChange={e=>setForm({...form, ifsc:e.target.value})} placeholder="SBIN0001234" className="w-full mt-1 p-3 rounded-xl bg-white border text-sm" />
                  </div>
                  <div className="col-span-2">
                    <label className="text-xs font-bold">Bank Name</label>
                    <input value={form.bankName} onChange={e=>setForm({...form, bankName:e.target.value})} placeholder="SBI, HDFC" className="w-full mt-1 p-3 rounded-xl bg-white border text-sm" />
                  </div>
                </div>
              </div>

              <div className="bg-[#FFF8E7] rounded-xl p-3 text-xs">
                <div className="font-bold">🔐 List Manaku Vastundi — Admin Panel lo — Easy Advanced!</div>
                <div className="mt-1 text-gray-600">• Code, Name, Phone, Type, UPI ID, Pending, Total, Last Payout, Actions Copy UPI + Copy Amount + PhonePe deep link → Send → Mark as Paid — 10 sec per payout!<br/>• Min withdrawal ₹150 OR 3 paid — admin work thakkuva<br/>• UPI primary + Bank backup — 2 options — best!</div>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button onClick={()=>setStep(1)} className="flex-1 py-3 border rounded-full font-bold text-sm">← Back</button>
              <button onClick={handleGenerate} className="flex-1 py-3 gold-gradient text-[#7A0C2E] rounded-full font-bold">🎉 Code LAK42 Generate →</button>
            </div>
          </div>
        )}

        {step===3 && generated && (
          <div className="space-y-4">
            <div className="bg-white rounded-[1.5rem] p-6 card-shadow text-center">
              <div className="text-4xl">🎉</div>
              <h2 className="font-bold text-xl text-[#7A0C2E] mt-2">Congratulations {generated.name}!</h2>
              <p className="text-sm telugu">Me referral code ready — short — 5 chars — easy! — share chesi ₹50 per pay sampadhinchandi!</p>

              <div className="mt-6 bg-[#FFF8E7] border-2 border-[#D4AF37] rounded-[1.5rem] p-6">
                <div className="text-xs text-gray-500">Me Short Code ({generated.type}) — 3 letters + 2 digits = 5 chars — easy enter!</div>
                <div className="text-3xl font-bold text-[#7A0C2E] mt-1">{generated.code}</div>
                <div className="text-xs mt-1 text-gray-600">{generated.shortExplain}</div>
                <div className="mt-2 text-xs bg-white rounded-full inline-block px-3 py-1">{generated.badge} • {generated.commission}</div>

                <div className="mt-4 grid grid-cols-1 gap-2 text-left text-xs">
                  <div className="bg-white rounded-xl p-3">
                    <div className="font-bold">🔗 Short Link — Neat & Easy:</div>
                    <div className="font-mono text-[11px] mt-1 break-all font-bold text-[#7A0C2E]">{generated.link}</div>
                    <div className="text-[10px] text-gray-500 mt-1">5 chars short — tsapmatrimony.com/r/LAK42 — easy type phone lo!</div>
                  </div>
                  <div className="bg-white rounded-xl p-3">
                    <div className="font-bold">🤖 Bot Short Link:</div>
                    <div className="font-mono text-[11px] mt-1 break-all">{generated.botLink}</div>
                  </div>
                  <div className="bg-white rounded-xl p-3">
                    <div className="font-bold">📱 Smart Share Message Auto with Name:</div>
                    <div className="text-[11px] mt-1">Hi, nenu {generated.name} — TSAP Matrimony — na link tho join avvandi — ₹99 ke sambandham — first 3 free — https://{generated.link} — na referral tho meeku 1 extra credit FREE! 🙏</div>
                  </div>
                  <div className="bg-green-50 rounded-xl p-3">
                    <div className="font-bold">💰 Payout Details — List Manaku Vachindi Admin lo:</div>
                    <div className="text-[11px] mt-1">UPI: {generated.upi || form.upi || "Not given — add later"} — PhonePe lo 10 sec lo payout — easy advanced! Bank backup optional.</div>
                  </div>
                </div>

                <div className="mt-4 flex gap-2">
                  <button className="flex-1 py-3 bg-[#25D366] text-white rounded-full font-bold text-sm">WhatsApp Share</button>
                  <button className="flex-1 py-3 bg-[#0088cc] text-white rounded-full font-bold text-sm">Telegram Share</button>
                  <button className="flex-1 py-3 bg-gray-900 text-white rounded-full font-bold text-sm">Copy Link</button>
                </div>

                <div className="mt-4 flex justify-center">
                  <div className="w-32 h-32 bg-white rounded-xl flex items-center justify-center border-2 border-dashed">QR<br/>{generated.code}</div>
                </div>
                <div className="text-[10px] text-gray-500 mt-2">QR poster print chesi shop/college lo pettochu — scan → /r/{generated.code} → auto fill lock → register!</div>
              </div>
            </div>

            <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
              <h3 className="font-bold text-[#7A0C2E]">📊 Dashboard lo Em Untundi? — Manage Everything Smart</h3>
              <div className="mt-3 grid grid-cols-4 gap-2 text-center">
                <div className="bg-gray-50 rounded-xl p-3"><div className="font-bold text-lg">0</div><div className="text-[10px]">Total Refers</div></div>
                <div className="bg-green-50 rounded-xl p-3"><div className="font-bold text-lg text-green-600">0</div><div className="text-[10px]">Paid (₹50 each)</div></div>
                <div className="bg-[#FFF8E7] rounded-xl p-3"><div className="font-bold text-lg text-[#7A0C2E]">₹0</div><div className="text-[10px]">Earned</div></div>
                <div className="bg-blue-50 rounded-xl p-3"><div className="font-bold text-lg">2</div><div className="text-[10px]">Credits Bonus</div></div>
              </div>
              <div className="mt-4 bg-[#0F1F3C] text-white rounded-xl p-4">
                <div className="font-bold text-sm text-[#D4AF37]">🏆 Bonus Progress — Normal — Smart!</div>
                <div className="mt-2 bg-white/20 rounded-full h-3 overflow-hidden"><div className="bg-[#D4AF37] h-3 rounded-full" style={{width:"0%"}}></div></div>
                <div className="text-xs mt-2">25 pays ki ₹500 bonus + 10 profiles share — inka 25 kavali! Min withdrawal ₹150 OR 3 paid — smart manage!</div>
              </div>
              <div className="mt-4 flex gap-3">
                <Link href="/referral" className="flex-1 py-3 maroon-gradient text-white rounded-full text-center font-bold text-sm">📊 Dashboard Chudu →</Link>
                <Link href="/" className="flex-1 py-3 border rounded-full text-center font-bold text-sm">🏠 Home</Link>
              </div>
            </div>

            <div className="bg-[#0F1F3C] text-white rounded-[1.5rem] p-6">
              <h3 className="font-bold text-[#D4AF37]">💡 Smart Lock — Link Tho Auto Fill Lock — How?</h3>
              <div className="text-xs mt-2 opacity-90 space-y-1">
                <div>• Link tsapmatrimony.com/r/{generated.code} → /register?ref={generated.code} → auto fill + 🔒 lock + "Lakshmi aunty dwara vacharu — trusted! — 1 extra credit FREE!"</div>
                <div>• Lock — commission guarantee — no fraud — transparent — user sees who referred</div>
                <div>• Students, Ladies, Brokers, Influencers — andaru referral ga — register avvakunda kooda earn — short code 5 chars — easy!</div>
                <div>• UPI chalu manual payout — PhonePe lo 10 sec — list admin lo — Copy UPI + Copy Amount + PhonePe deep link → Send → Mark as Paid</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
