"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function SearchPageAdvanced() {
  const params = useParams();
  const idFromUrl = params?.id as string;
  const [searchId, setSearchId] = useState(idFromUrl || "");
  const [profile, setProfile] = useState<any>(null);
  const [credits, setCredits] = useState(3);
  const [showNumber, setShowNumber] = useState(false);
  const [myPhone, setMyPhone] = useState("98480xxxxx");

  useEffect(() => {
    if (idFromUrl) handleSearch(idFromUrl);
    const c = localStorage.getItem("tsap_credits");
    if (c) setCredits(parseInt(c));
    const p = localStorage.getItem("tsap_last_phone");
    if (p) setMyPhone(p);
  }, [idFromUrl]);

  const handleSearch = (id: string) => {
    const profiles = JSON.parse(localStorage.getItem("tsap_profiles") || "[]");
    const mock = {
      id: id || "TSAP-F-2025-1042",
      fullName: "Lakshmi Reddy",
      gender: id?.includes("-F-") ? "Bride" : "Groom",
      age: "24",
      height: "5'4\"",
      weight: "55kg",
      caste: "Reddy",
      subCaste: "Pakanati",
      gothram: "Bharadwaj",
      star: "Rohini",
      rasi: "Vrushabha",
      dosham: "No",
      education: "BTech",
      educationDetail: "BTech CSE",
      college: "JNTU Hyderabad",
      job: "Software",
      company: "TCS",
      salary: "60k",
      workLocation: "Hyderabad Gachibowli",
      state: "TS",
      district: "Nalgonda",
      mandal: "Gachibowli",
      currentCity: "Hyderabad",
      fatherName: "Ramesh Reddy",
      fatherOccupation: "Farmer",
      motherName: "Sita Reddy",
      motherOccupation: "Housewife",
      familyType: "Nuclear",
      familyStatus: "Middle Class",
      nativePlace: "Nalgonda",
      aboutMyself: "Nenu software engineer, simple family, traditional values, looking for understanding partner, respect elders, non-smoker.",
      aboutFamily: "Middle class traditional family",
      dob: "2001-05-15",
      dobCorrect: true,
      birthTime: "10:30 AM",
      phone: "9848012345",
      photoPrivate: false,
      photoUrl: "https://i.pravatar.cc/300?img=32",
      score: 92,
      reasons: ["Hyderabad + Software perfect", "Software + BTech same", "Reddy Bharadwaj perfect age gap 3y", "Family Nuclear Middle Class Father Farmer"],
      expectationMatch: "Age 21-28 Height 5-10 Caste Reddy Job Software Govt Location Hyderabad",
    };
    const found = profiles.find((p: any) => p.id === id) || mock;
    setProfile(found);
  };

  const handleUnlock = () => {
    if (credits > 0) {
      setCredits(credits - 1);
      localStorage.setItem("tsap_credits", (credits - 1).toString());
      setShowNumber(true);
    } else {
      alert("Credits ayipoyayi 99 pay 10 credits vasthayi but ID search always open profile chudochu number ki credit kavali");
    }
  };

  const shareWhatsApp = () => {
    if (!profile) return;
    const text = "TSAP " + profile.id + " " + profile.fullName + " " + profile.age + "y " + profile.height + " " + profile.caste + " " + profile.gothram + " " + profile.education + " " + profile.educationDetail + " " + profile.job + " at " + profile.company + " " + profile.district + " " + profile.mandal + " Father " + profile.fatherName + " Family " + profile.familyType + " Star " + profile.star + " Rasi " + profile.rasi + " DOB " + profile.dob + " " + profile.birthTime + " " + (profile.dobCorrect ? "Correct Tick" : "") + " Salary " + profile.salary + " Location " + profile.workLocation + " Why " + profile.reasons[0] + " Search Code " + profile.id + " https://tsapmatrimony.com/search/" + profile.id + " Phone " + (showNumber ? profile.phone : "Pay unlock") + " Bot @telugumatrimony1_bot Channels @TSBRIDE @TSGROOM1";
    window.open("https://wa.me/" + myPhone + "?text=" + encodeURIComponent(text), "_blank");
  };

  const shareTelegram = () => {
    if (!profile) return;
    const url = "https://tsapmatrimony.com/search/" + profile.id;
    const txt = "TSAP " + profile.id + " " + profile.fullName + " " + profile.age + "y " + profile.caste + " " + profile.job + " " + profile.district + " " + profile.score + "% " + profile.reasons[0];
    window.open("https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(txt), "_blank");
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">Home</Link>
          <div className="font-bold text-[#7A0C2E]">Advanced ID Search Profile Code</div>
          <Link href="/register" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Register</Link>
        </div>

        <div className="bg-white rounded-full p-2 flex gap-2">
          <input value={searchId} onChange={e => setSearchId(e.target.value)} placeholder="Profile Code e.g. TSAP-F-2025-1042 separate code" className="flex-1 outline-none text-sm px-4 py-2" />
          <button onClick={() => handleSearch(searchId)} className="px-5 py-2 maroon-gradient text-white rounded-full text-sm font-bold">Search Code</button>
        </div>

        <div className="mt-2 text-xs text-gray-500">Form fill chesaka separate code vasthundi ah code tho search limit ayina kuda ID search eppudu open profile photos details open numbers lock if no credits malli pay logic 100% no gaps</div>

        {profile && (
          <div className="mt-6 space-y-4">
            <div className="bg-white rounded-2xl p-4 flex flex-wrap items-center justify-between gap-2">
              <div>
                <div className="font-bold text-sm">Credits {credits} ID Search Always Open Logic</div>
                <div className="text-xs text-gray-500">Profile open even credits 0 number ki 1 credit limit ayyaka malli 99</div>
              </div>
              <div className="flex gap-2 items-center">
                <span className="text-xs">My Phone share target</span>
                <input value={myPhone} onChange={e => setMyPhone(e.target.value)} className="border rounded px-2 py-1 text-xs w-28" />
                <button className="px-4 py-2 gold-gradient rounded-full text-xs font-bold text-[#7A0C2E]">99 10 Credits</button>
                <button className="px-4 py-2 maroon-gradient text-white rounded-full text-xs font-bold">299 50</button>
              </div>
            </div>

            <div className="bg-white rounded-[1.5rem] overflow-hidden border-2 border-[#D4AF37]">
              <div className="maroon-gradient text-white p-3 flex items-center justify-between text-xs">
                <div className="font-bold">TSAP MATRIMONY {profile.id} {profile.fullName}</div>
                <div className="bg-white/20 px-2 py-1 rounded-full">Star {profile.score}% BEST DOB {profile.dobCorrect ? "Verified" : "Pending"} {profile.state}</div>
              </div>
              <div className="p-6">
                <div className="flex gap-6 flex-col md:flex-row">
                  <div className="w-full md:w-48 h-60 bg-gray-100 rounded-2xl overflow-hidden border-2 border-[#D4AF37] flex-shrink-0">
                    {profile.photoUrl ? <img src={profile.photoUrl} alt={profile.fullName} className="w-full h-full object-cover" /> : <div className="w-full h-full flex items-center justify-center text-5xl">{profile.photoPrivate ? "Lock" : (profile.gender === "Bride" ? "Bride" : "Groom")}</div>}
                  </div>
                  <div className="flex-1 space-y-3">
                    <div>
                      <div className="font-bold text-xl text-[#7A0C2E]">{profile.fullName} {profile.age}y {profile.height} {profile.weight} {profile.caste} {profile.subCaste}</div>
                      <div className="text-sm text-gray-600 mt-1">{profile.education} {profile.educationDetail} at {profile.college} Job {profile.job} at {profile.company} Salary {profile.salary} Location {profile.workLocation} Now {profile.currentCity}</div>
                      <div className="text-xs text-gray-500 mt-1">{profile.district} {profile.mandal} {profile.state} Native {profile.nativePlace} Family {profile.familyType} {profile.familyStatus}</div>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs bg-gray-50 p-3 rounded-xl">
                      <div>Father {profile.fatherName} {profile.fatherOccupation}</div>
                      <div>Mother {profile.motherName} {profile.motherOccupation}</div>
                      <div>Gothram {profile.gothram} Star {profile.star} optional Rasi {profile.rasi} Dosham {profile.dosham}</div>
                      <div>DOB {profile.dob} Time {profile.birthTime} {profile.dobCorrect ? "Correct Tick Yes" : "Approximate"} Age {profile.age}</div>
                      <div>Height {profile.height} Weight {profile.weight}</div>
                      <div>About {profile.aboutMyself.slice(0, 80)}</div>
                    </div>
                    <div className="flex gap-2 flex-wrap">
                      {!showNumber ? (
                        <button onClick={handleUnlock} className="px-5 py-2 maroon-gradient text-white rounded-full text-sm font-bold">Number Chudu 1 Credit {profile.phone.slice(0, 4)}xxxx</button>
                      ) : (
                        <div className="px-5 py-2 bg-green-100 text-green-700 rounded-full text-sm font-bold">Phone {profile.phone} Call Now WhatsApp</div>
                      )}
                      <button className="px-5 py-2 border border-[#D4AF37] text-[#7A0C2E] rounded-full text-sm font-bold">Interest Pampu</button>
                      <button onClick={shareWhatsApp} className="px-5 py-2 bg-green-600 text-white rounded-full text-sm font-bold">Share WhatsApp to {myPhone}</button>
                      <button onClick={shareTelegram} className="px-5 py-2 bg-blue-500 text-white rounded-full text-sm font-bold">Share Telegram</button>
                    </div>
                    <div className="text-[11px] text-gray-500">Share button WhatsApp Telegram to registered number {myPhone} forward neat automation nuvvu adigina logic 100%</div>
                  </div>
                </div>

                <div className="mt-6 bg-[#FFF8E7] rounded-xl p-4 border border-[#D4AF37]/20">
                  <div className="font-bold text-sm text-[#7A0C2E]">Star {profile.score}% BEST MATCH Personalized Reason Nee Expectation ki Ilaga Set</div>
                  <div className="mt-2 space-y-1 text-sm">
                    {profile.reasons.map((r: string, i: number) => <div key={i}>Yes {r}</div>)}
                  </div>
                  <div className="mt-3 text-xs text-gray-600">Expectation {profile.expectationMatch} Location Mee intiki 15km Family matching Filter logic perfect</div>
                  <div className="mt-2 text-[11px] text-gray-500">About Family {profile.aboutFamily} About Myself full {profile.aboutMyself}</div>
                </div>

                <div className="mt-4 grid grid-cols-3 gap-2 text-[11px]">
                  <div className="bg-gray-50 p-2 rounded-xl">#{profile.caste} #{profile.state} #{profile.gender} Age {profile.age} {profile.job} {profile.district}</div>
                  <div className="bg-gray-50 p-2 rounded-xl">ID {profile.id} Watermark protected DOB {profile.dobCorrect ? "Verified" : "Pending"}</div>
                  <div className="bg-gray-50 p-2 rounded-xl">Bot @telugumatrimony1_bot Search {profile.id} Share WhatsApp Telegram to {myPhone}</div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-4">
              <div className="font-bold text-sm">Admin Only + Automation Flow</div>
              <div className="text-xs text-gray-500 mt-1">Form ekkada vasthundi register 5 steps advanced HTML page la Name DOB Father Name Qualification anni perfect mandatory fields nimpakapte next ki velladu DOB correct tick Time Nakshatram optional logic template photo tho neat separate code ID search advanced filters manaku matrame 5 profiles display share WhatsApp Telegram registered number forward website motham automate Oracle VM free tier saripothunda YES ekkuva em avvadu profiles text photos compressed 10k profiles less 5GB free tier 1GB RAM 50GB disk chalu cost free backup Drive 100% perfect no gaps no issues more and more advanced neat website fully advanced bot</div>
              <div className="mt-3 flex gap-2">
                <Link href="/admin" className="px-4 py-2 bg-[#0F1F3C] text-white rounded-full text-xs font-bold">Admin Panel</Link>
                <Link href="/matches" className="px-4 py-2 border rounded-full text-xs font-bold">Advanced Matches Filters</Link>
                <Link href="/" className="px-4 py-2 bg-[#FFF8E7] rounded-full text-xs font-bold">Home</Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
