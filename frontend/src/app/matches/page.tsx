"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function MatchesAdvanced() {
  const [credits, setCredits] = useState(3);
  const [myPhone, setMyPhone] = useState("98480xxxxx");
  const [showCount, setShowCount] = useState(5);
  const [filters, setFilters] = useState({
    job: "Any",
    location: "Any",
    caste: "Any",
    ageMin: "18",
    ageMax: "60",
    salary: "Any",
    education: "Any",
    district: "Any",
    state: "Any",
    marital: "Any",
  });
  const [matches, setMatches] = useState<any[]>([]);

  useEffect(() => {
    const c = localStorage.getItem("tsap_credits");
    if (c) setCredits(parseInt(c));
    const all = [
      { id: "TSAP-F-2025-1042", fullName: "Lakshmi Reddy", age: 24, caste: "Reddy", edu: "BTech CSE", job: "Software", company: "TCS", district: "Hyderabad", state: "TS", mandal: "Gachibowli", salary: "60k", marital: "Pelli Kaledu", gothram: "Bharadwaj", star: "Rohini", workLocation: "Hyderabad", score: 92, photo: "https://i.pravatar.cc/300?img=32", reasons: ["Hyderabad + Software perfect", "Reddy + Bharadwaj same caste", "Age gap 3y ideal", "Middle Class Nuclear matching"], phone: "9848012345" },
      { id: "TSAP-M-2025-2042", fullName: "Ramesh Reddy", age: 45, caste: "Reddy", edu: "BTech", job: "Software", company: "Infosys", district: "Hyderabad", state: "TS", mandal: "Madhapur", salary: "1L+", marital: "Pelli Kaledu", gothram: "Kaundinya", star: "Bharani", workLocation: "Hyderabad", score: 88, photo: "https://i.pravatar.cc/300?img=12", reasons: ["Software Hyderabad 45y exact match", "Reddy same Gothram diff allowed", "Salary 1L+ stable", "Madhapur near Gachibowli 5km"], phone: "9848023456" },
      { id: "TSAP-M-2025-3042", fullName: "Suresh Reddy", age: 47, caste: "Reddy", edu: "MTech", job: "Software", company: "Wipro", district: "Hyderabad", state: "TS", mandal: "Kukatpally", salary: "1L+", marital: "Pelli Kaledu", gothram: "Kasyapa", star: "Ashwini", workLocation: "Hyderabad", score: 85, photo: "https://i.pravatar.cc/300?img=15", reasons: ["Software Hyd 45+ Reddy 100% filter", "Age 47 mature stable", "MTech educated", "Kukatpally Hyd circle"], phone: "9848034567" },
      { id: "TSAP-M-2025-4042", fullName: "Kiran Reddy", age: 28, caste: "Reddy", edu: "BTech", job: "Govt Job", company: "TS Govt", district: "Nalgonda", state: "TS", mandal: "Nalgonda", salary: "60k", marital: "Pelli Kaledu", gothram: "Bharadwaj", star: "Rohini", workLocation: "Nalgonda", score: 90, photo: "https://i.pravatar.cc/300?img=20", reasons: ["Govt Job hot secure", "Reddy same Gothram diff", "Nalgonda near Hyd 60km"], phone: "9848045678" },
      { id: "TSAP-M-2025-5042", fullName: "Arjun Reddy", age: 32, caste: "Reddy", edu: "MBBS", job: "Doctor", company: "Apollo", district: "Hyderabad", state: "TS", mandal: "Banjara Hills", salary: "2L+", marital: "Pelli Kaledu", gothram: "Vasishta", star: "Mrigasira", workLocation: "Hyderabad", score: 94, photo: "https://i.pravatar.cc/300?img=30", reasons: ["Doctor Hyderabad premium", "Reddy 32y young", "2L+ affluent"], phone: "9848056789" },
    ];
    setMatches(all);
  }, []);

  const filtered = matches.filter(m => {
    if (filters.job !== "Any" && m.job !== filters.job) return false;
    if (filters.location !== "Any" && m.workLocation.toLowerCase().indexOf(filters.location.toLowerCase()) === -1 && m.district.toLowerCase().indexOf(filters.location.toLowerCase()) === -1) return false;
    if (filters.caste !== "Any" && m.caste !== filters.caste) return false;
    if (filters.district !== "Any" && m.district !== filters.district) return false;
    if (filters.state !== "Any" && m.state !== filters.state) return false;
    if (filters.marital !== "Any" && m.marital !== filters.marital) return false;
    if (parseInt(m.age) < parseInt(filters.ageMin) || parseInt(m.age) > parseInt(filters.ageMax)) return false;
    if (filters.salary === "60k+" && (m.salary === "10k-20k" || m.salary === "20k-40k")) return false;
    if (filters.salary === "1L+" && !(m.salary === "1L+" || m.salary === "2L+")) return false;
    if (filters.education !== "Any" && m.edu.indexOf(filters.education) === -1) return false;
    return true;
  }).sort((a, b) => b.score - a.score).slice(0, showCount);

  const shareWhatsApp = (profile: any) => {
    const reason = profile.reasons[0] || "";
    const text = "TSAP Matrimony BEST " + profile.score + "% - " + profile.fullName + " (" + profile.id + ") Age " + profile.age + " " + profile.caste + " " + profile.job + " at " + profile.district + " " + profile.mandal + " Salary " + profile.salary + " Why: " + reason + " Search https://tsapmatrimony.com/search/" + profile.id + " Bot @telugumatrimony1_bot Phone " + (credits > 0 ? profile.phone : "Pay 99 unlock");
    window.open("https://wa.me/" + myPhone + "?text=" + encodeURIComponent(text), "_blank");
  };

  const shareTelegram = (profile: any) => {
    const reason = profile.reasons[0] || "";
    const url = "https://tsapmatrimony.com/search/" + profile.id;
    const txt = "TSAP " + profile.id + " " + profile.fullName + " " + profile.score + "% " + reason;
    window.open("https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(txt), "_blank");
  };

  const shareBulkWhatsApp = () => {
    let list = "";
    filtered.forEach(p => {
      list += "- " + p.id + " " + p.fullName + " " + p.age + "y " + p.caste + " " + p.job + " " + p.district + " " + p.score + "% " + p.reasons[0] + "\n";
    });
    const text = "TSAP Top " + filtered.length + " BEST Matches Filter Job=" + filters.job + " Location=" + filters.location + " Age " + filters.ageMin + "-" + filters.ageMax + " Caste=" + filters.caste + "\n\n" + list + "\nSearch each ID on tsapmatrimony.com Credits " + credits + " Bot @telugumatrimony1_bot Channels @TSBRIDE @TSGROOM1";
    window.open("https://wa.me/" + myPhone + "?text=" + encodeURIComponent(text), "_blank");
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">Home</Link>
          <div className="font-bold text-[#7A0C2E]">Advanced Matches Filters + Share</div>
          <div className="text-xs bg-white px-3 py-1 rounded-full">Credits {credits} Phone {myPhone}</div>
        </div>

        <div className="bg-gradient-to-r from-[#7A0C2E] to-[#A0143A] text-white rounded-2xl p-4">
          <div className="font-bold text-sm">Example: Software Hyderabad 45+ Reddy 5 profiles</div>
          <div className="text-xs opacity-90 mt-1">Filter Job Software Location Hyderabad AgeMin 45 Caste Reddy Show 5 then best 5 only reason + Share WhatsApp Telegram to registered number</div>
        </div>

        <div className="mt-4 bg-white rounded-[1.5rem] p-5 border-2 border-[#D4AF37]/30">
          <h3 className="font-bold text-[#7A0C2E]">Advanced Filters Manaku Matrame 100% Perfect No Gaps</h3>
          <p className="text-xs text-gray-500 mt-1">Filter matchable profiles only system manaku matrame advanced</p>
          <div className="mt-4 grid grid-cols-2 md:grid-cols-5 gap-3">
            <div>
              <label className="text-[11px] font-bold">Job Filter</label>
              <select value={filters.job} onChange={e => setFilters({ ...filters, job: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>Software</option><option>Govt Job</option><option>Business</option><option>Doctor</option><option>Private Job</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Location</label>
              <select value={filters.location} onChange={e => setFilters({ ...filters, location: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>Hyderabad</option><option>Nalgonda</option><option>Warangal</option><option>Vijayawada</option><option>USA</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Caste</label>
              <select value={filters.caste} onChange={e => setFilters({ ...filters, caste: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>Reddy</option><option>Kamma</option><option>Kapu</option><option>Velama</option><option>Yadav</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">District</label>
              <select value={filters.district} onChange={e => setFilters({ ...filters, district: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>Hyderabad</option><option>Nalgonda</option><option>Rangareddy</option><option>Medchal</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">State</label>
              <select value={filters.state} onChange={e => setFilters({ ...filters, state: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>TS</option><option>AP</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Age Min 45 example</label>
              <select value={filters.ageMin} onChange={e => setFilters({ ...filters, ageMin: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                {Array.from({ length: 45 }, (_, i) => 18 + i).map(a => <option key={a} value={a}>{a}</option>)}
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Age Max</label>
              <select value={filters.ageMax} onChange={e => setFilters({ ...filters, ageMax: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                {Array.from({ length: 45 }, (_, i) => 18 + i).map(a => <option key={a} value={a}>{a}</option>)}
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Salary</label>
              <select value={filters.salary} onChange={e => setFilters({ ...filters, salary: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>60k+</option><option>1L+</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Education</label>
              <select value={filters.education} onChange={e => setFilters({ ...filters, education: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs">
                <option>Any</option><option>BTech</option><option>MTech</option><option>MBBS</option><option>MBA</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold">Show Count 5 example</label>
              <select value={showCount} onChange={e => setShowCount(parseInt(e.target.value))} className="w-full mt-1 p-2 rounded-xl bg-gray-50 border text-xs font-bold border-[#D4AF37]">
                <option value={1}>1 Profile</option><option value={5}>5 Profiles example</option><option value={10}>10 Profiles</option><option value={20}>20 Profiles</option>
              </select>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <div className="text-xs bg-[#FFF8E7] px-3 py-2 rounded-full">Total Matched {filtered.length} / {matches.length} Best only 70+ Showing top {showCount}</div>
            <div className="text-xs bg-green-50 border border-green-200 px-3 py-2 rounded-full text-green-700">Filter Job {filters.job} Location {filters.location} Age {filters.ageMin}+ Caste {filters.caste} found {filtered.length}</div>
            <button onClick={shareBulkWhatsApp} className="text-xs bg-green-600 text-white px-4 py-2 rounded-full font-bold">Share All {filtered.length} to My WhatsApp {myPhone}</button>
            <button onClick={() => setFilters({ job: "Any", location: "Any", caste: "Any", ageMin: "18", ageMax: "60", salary: "Any", education: "Any", district: "Any", state: "Any", marital: "Any" })} className="text-xs border px-4 py-2 rounded-full">Reset Filters</button>
          </div>
          <div className="mt-3 text-[11px] text-gray-500">Registered Number <input value={myPhone} onChange={e => setMyPhone(e.target.value)} className="border rounded px-2 py-1 text-xs w-32" /> Share button WhatsApp Telegram to registered number forward 100% automation</div>
        </div>

        <div className="mt-4 grid md:grid-cols-2 gap-4">
          {filtered.map(m => (
            <div key={m.id} className="bg-white rounded-[1.5rem] p-4 border border-[#D4AF37]/20">
              <div className="flex gap-3">
                <img src={m.photo} alt={m.fullName} className="w-20 h-24 rounded-xl object-cover border" />
                <div className="flex-1">
                  <div className="font-bold text-sm">{m.fullName} {m.id} {m.age}y {m.caste} {m.edu}</div>
                  <div className="text-xs text-gray-500">{m.job} at {m.company} {m.district} {m.mandal} {m.state} {m.salary} {m.workLocation} Gothram {m.gothram} Star {m.star}</div>
                  <div className="mt-2 bg-[#FFF8E7] rounded-xl p-2 text-[11px] space-y-1">
                    <div className="font-bold text-[#7A0C2E]">Star {m.score}% BEST Why match</div>
                    {m.reasons.map((r: string, i: number) => <div key={i}>Yes {r}</div>)}
                  </div>
                  <div className="mt-3 flex gap-2">
                    <Link href={"/search/" + m.id} className="flex-1 py-2 border rounded-full text-center text-xs font-bold">Open ID</Link>
                    <button onClick={() => shareWhatsApp(m)} className="flex-1 py-2 bg-green-600 text-white rounded-full text-xs font-bold">WhatsApp Share</button>
                    <button onClick={() => shareTelegram(m)} className="flex-1 py-2 bg-blue-500 text-white rounded-full text-xs font-bold">Telegram Share</button>
                  </div>
                  <div className="mt-2 text-[10px] text-gray-400">Share to registered number {myPhone} forward neat WhatsApp Telegram</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="mt-6 bg-white rounded-2xl p-8 text-center">
            <div className="text-4xl">Search</div>
            <div className="font-bold mt-2">No profiles match filters change</div>
            <div className="text-xs text-gray-500 mt-1">Example Software Hyderabad 45+ Reddy profiles available filter exact</div>
          </div>
        )}

        <div className="mt-6 bg-white rounded-2xl p-4 text-center">
          <div className="text-sm font-bold">Credits Logic ID Search Always Open</div>
          <div className="text-xs text-gray-500 mt-1">Limit ayina kuda ID search open profile photos details open numbers lock if no credits malli pay 99 10 credits admin manual premium gift</div>
          <div className="mt-3 flex justify-center gap-2">
            <button className="px-6 py-2 gold-gradient rounded-full text-sm font-bold text-[#7A0C2E]">99 10 Credits + Share</button>
            <button className="px-6 py-2 maroon-gradient text-white rounded-full text-sm font-bold">299 50 Credits + Daily Auto WhatsApp</button>
          </div>
          <div className="mt-3 text-[11px] text-gray-400">Oracle VM Free Tier Saripodda YES 4 OCPU 24GB free tier 1 VM 1GB RAM 50GB disk chalu profiles text photos compressed 10k profiles less 5GB ekkuva em avvadu free tier more than enough backup Drive daily</div>
        </div>
      </div>
    </div>
  );
}
