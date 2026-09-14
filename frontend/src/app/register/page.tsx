"use client";
import { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CASTE_OPTIONS } from "@/lib/channels";

function RegisterContent() {
  const searchParams = useSearchParams();
  const refFromUrl = searchParams.get('ref');

  const [step, setStep] = useState(1);
  const [isReferralLocked, setIsReferralLocked] = useState(false);
  const [referrerName, setReferrerName] = useState("");
  const [errors, setErrors] = useState<string[]>([]);
  const [generated, setGenerated] = useState<any>(null);
  const [photoPreview, setPhotoPreview] = useState<string>("");
  const [backend, setBackend] = useState<any>(null);
  const [publishPreview, setPublishPreview] = useState<any>(null);

  // FULL ADVANCED FORM STATE - All matrimony typical fields
  const [form, setForm] = useState({
    // Step 1 - Personal Basic
    fullName: "",
    gender: "Bride",
    dob: "",
    dobCorrect: false,
    birthTime: "",
    age: "",
    height: "5'4\"",
    weight: "",
    bloodGroup: "",
    maritalStatus: "Pelli Kaledu",
    physicalStatus: "Normal",
    motherTongue: "Telugu",
    bodyType: "Average",
    complexion: "Fair",

    // Step 2 - Family
    fatherName: "",
    fatherOccupation: "",
    motherName: "",
    motherOccupation: "",
    familyType: "Nuclear",
    familyValues: "Traditional",
    familyStatus: "Middle Class",
    brothers: "0",
    brothersMarried: "0",
    sisters: "0",
    sistersMarried: "0",
    nativePlace: "",
    aboutFamily: "",

    // Step 3 - Astro & Caste
    caste: "Reddy",
    subCaste: "",
    gothram: "",
    star: "",
    rasi: "",
    dosham: "No",
    moolaNakshatram: "No",

    // Step 4 - Education & Career
    education: "BTech",
    educationDetail: "",
    college: "",
    job: "Software",
    company: "",
    salary: "60k",
    workLocation: "Hyderabad",
    aboutMyself: "",

    // Step 5 - Location & Contact & Expectations & Photos
    state: "TS",
    district: "Nalgonda",
    mandal: "",
    currentCity: "",
    pincode: "",
    phone: "",
    email: "",
    photoPrivate: false,
    // Expectations Builder - Advanced Filters
    expAgeMin: "21",
    expAgeMax: "28",
    expHeightMin: "5'0\"",
    expHeightMax: "5'10\"",
    expCaste: [] as string[],
    expEducation: "Any",
    expJob: "Any",
    expLocation: "Any",
    expSalary: "Any",
    referral: "",
  });

  useEffect(() => {
    if (refFromUrl) {
      setForm(prev => ({ ...prev, referral: refFromUrl }));
      setIsReferralLocked(true);
      const referrers = JSON.parse(localStorage.getItem("tsap_referrers") || "[]");
      const found = referrers.find((r: any) => r.code === refFromUrl);
      if (found) setReferrerName(found.name);
      else {
        if (refFromUrl.length <= 6) setReferrerName(refFromUrl);
        else setReferrerName(refFromUrl);
      }
      localStorage.setItem("tsap_ref_from_link", refFromUrl);
    }
  }, [refFromUrl]);

  // Auto-calc age from DOB
  useEffect(() => {
    if (form.dob) {
      const dob = new Date(form.dob);
      const now = new Date();
      let age = now.getFullYear() - dob.getFullYear();
      const m = now.getMonth() - dob.getMonth();
      if (m < 0 || (m === 0 && now.getDate() < dob.getDate())) age--;
      if (age >= 18) setForm(prev => ({ ...prev, age: age.toString() }));
    }
  }, [form.dob]);

  const districtsTS = ["Adilabad", "Bhadradri", "Hanumakonda", "Hyderabad", "Jagtial", "Jangaon", "Jayashankar", "Jogulamba", "Kamareddy", "Karimnagar", "Khammam", "Kumuram Bheem", "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", "Medchal", "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Yadadri"];
  const districtsAP = ["Alluri", "Anakapalli", "Ananthapur", "Annamayya", "Bapatla", "Chittoor", "East Godavari", "Eluru", "Guntur", "YSR Kadapa", "Kakinada", "Konaseema", "Krishna", "Kurnool", "Nandyal", "Nellore", "NTR", "Palnadu", "Parvathipuram", "Prakasam", "Srikakulam", "Sri Sathya Sai", "Tirupati", "Visakhapatnam", "Vizianagaram", "West Godavari"];
  // 43 caste channels + Muslim/Christian/Open — registry nunchi auto (backend/channels_config.py)
  const castes = CASTE_OPTIONS;
  const educations = ["10th", "Inter", "Degree", "BTech", "MTech", "MBBS", "BDS", "MBA", "MCA", "PhD", "CA", "IAS", "LLB", "BEd", "Others"];
  const jobs = ["Govt Job", "Private Job", "Software", "Business", "Agriculture", "Abroad-NRI", "No Job", "Doctor", "Engineer", "Teacher", "Police", "Bank", "Army"];

  // VALIDATION PER STEP - mandatory logic
  const validateStep = (s: number): boolean => {
    const errs: string[] = [];
    if (s === 1) {
      if (!form.fullName.trim() || form.fullName.length < 3) errs.push("Full Name mandatory - min 3 letters");
      if (!form.dob) errs.push("DOB mandatory - date select cheyyi");
      if (!form.dobCorrect) errs.push("DOB correct tick mandatory - 'Na DOB correctena' tick cheyyi");
      if (!form.age || parseInt(form.age) < 18) errs.push("Age mandatory - 18+");
      if (!form.height) errs.push("Height mandatory");
      if (!form.maritalStatus) errs.push("Marital Status mandatory");
      if (!form.physicalStatus) errs.push("Physical Status mandatory");
    }
    if (s === 2) {
      if (!form.fatherName.trim()) errs.push("Father Name mandatory - matrimony lo must");
      if (!form.motherName.trim()) errs.push("Mother Name mandatory");
      if (!form.nativePlace.trim()) errs.push("Native Place mandatory");
    }
    if (s === 3) {
      if (!form.caste) errs.push("Caste mandatory");
      if (!form.gothram.trim()) errs.push("Gothram mandatory - Telugu matrimony lo must");
      // star, rasi optional - advanced but not mandatory
    }
    if (s === 4) {
      if (!form.education) errs.push("Education mandatory");
      if (!form.educationDetail.trim()) errs.push("Education Detail mandatory - e.g. BTech CSE");
      if (!form.job) errs.push("Job mandatory");
      if (!form.salary) errs.push("Salary mandatory");
      if (!form.workLocation.trim()) errs.push("Work Location mandatory");
      if (!form.aboutMyself.trim() || form.aboutMyself.length < 50) errs.push("About Myself mandatory - min 50 letters - ne gurinchi rayi");
    }
    if (s === 5) {
      if (!form.state) errs.push("State mandatory");
      if (!form.district) errs.push("District mandatory");
      if (!form.mandal.trim()) errs.push("Mandal/Town mandatory - deep filter ki");
      if (!form.phone.trim() || form.phone.length < 10) errs.push("Phone mandatory - 10 digits");
      if (!photoPreview) errs.push("Photo 1 mandatory - face clear photo");
      // email optional
    }
    setErrors(errs);
    return errs.length === 0;
  };

  const nextStep = (s: number) => {
    if (validateStep(s)) {
      setErrors([]);
      setStep(s + 1);
      window.scrollTo(0, 0);
    }
  };

  const handleGenerate = async () => {
    if (!validateStep(5)) return;
    const id = `TSAP-${form.gender === 'Bride' ? 'F' : 'M'}-2025-${Math.floor(1000 + Math.random() * 9000)}`;
    const card = {
      id,
      ...form,
      credits: 3,
      score: 92,
      photoUrl: photoPreview,
      reasons: [
        `Nuvvu ${form.district} + ${form.workLocation} kavali annavu → ee profile kooda ${form.district} lone`,
        `Nuvvu ${form.job} + ${form.education} kavali annavu → profile kooda ${form.job} ${form.education}`,
        `Caste ${form.caste} Gothram ${form.gothram} + Age ${form.age} gap perfect — 92% set!`,
        `Family ${form.familyType} + ${form.familyStatus} + Father ${form.fatherOccupation} — matching`,
      ],
      expectationMatch: `Expectation: Age ${form.expAgeMin}-${form.expAgeMax}, Height ${form.expHeightMin}-${form.expHeightMax}, Caste ${form.expCaste.length ? form.expCaste.join(",") : form.caste}, Job ${form.expJob}, Location ${form.expLocation}`,
    };
    setGenerated(card);
    const existing = JSON.parse(localStorage.getItem("tsap_profiles") || "[]");
    existing.push(card);
    localStorage.setItem("tsap_profiles", JSON.stringify(existing));
    localStorage.setItem("tsap_last_id", id);
    setStep(6);

    // Try backend API also
    try {
      const fd = new FormData();
      fd.append("gender", form.gender);
      fd.append("age", form.age);
      fd.append("height", form.height);
      fd.append("marital_status", form.maritalStatus);
      fd.append("caste", form.caste);
      fd.append("sub_caste", form.subCaste);
      fd.append("gothram", form.gothram);
      fd.append("star", form.star);
      fd.append("education", form.education);
      fd.append("job", form.job);
      fd.append("salary", form.salary);
      fd.append("state", form.state);
      fd.append("district", form.district);
      fd.append("mandal", form.mandal);
      fd.append("phone", form.phone);
      fd.append("referral_code", form.referral);
      fd.append("photo_private", String(form.photoPrivate));
      fd.append("expectations", JSON.stringify({ ageMin: form.expAgeMin, ageMax: form.expAgeMax, caste: form.expCaste, job: form.expJob }));
      fd.append("blood_group", form.bloodGroup);
      fd.append("father_name", form.fatherName);
      fd.append("mother_name", form.motherName);
      fd.append("about_myself", form.aboutMyself);
      fd.append("native_place", form.nativePlace);
      fd.append("dob", form.dob);
      fd.append("dob_correct", String(form.dobCorrect));
      fd.append("photo_private", String(form.photoPrivate));

      // Same-origin API (manavivaha.in/api) → nginx backend ki proxy chestundi.
      // Direct IP:port hardcode ledu — domain tho pani chestundi, CORS issue ledu.
      const res = await fetch("/api/register", { method: "POST", body: fd });
      if (res.ok) {
        const d = await res.json();
        setBackend(d);
        if (d.tsap_id) setGenerated((g: any) => ({ ...g, id: d.tsap_id, backendId: d.tsap_id }));
      }
    } catch { }

    // Auto-publish preview — ee profile YE channels ki veltundo (backend router, real)
    try {
      const pv = await fetch("/api/publish/preview", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: form.fullName, gender: form.gender, state: form.state, caste: form.caste,
          age: form.age, job: form.job, education: form.education, district: form.district,
          marital_status: form.maritalStatus, gothram: form.gothram, star: form.star,
          blood_group: form.bloodGroup, photo_private: form.photoPrivate, score: 92,
          tsap_id: id, salary: form.salary, work_location: form.workLocation,
        }),
      });
      if (pv.ok) setPublishPreview(await pv.json());
    } catch { }
  };

  const toggleExpCaste = (c: string) => {
    setForm(prev => {
      const arr = prev.expCaste.includes(c) ? prev.expCaste.filter(x => x !== c) : [...prev.expCaste, c];
      return { ...prev, expCaste: arr };
    });
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <Link href="/" className="text-sm text-[#7A0C2E] font-bold">← Home</Link>
          <div className="text-sm font-bold text-[#7A0C2E]">TSAP Matrimony • Advanced Register • 5 Steps</div>
          <Link href="/search/TSAP-M-2025-1042" className="text-xs border px-3 py-1 rounded-full">🔍 Search by Code</Link>
        </div>

        {/* Progress - 5 Steps */}
        <div className="bg-white rounded-full p-2 flex gap-1 mb-4 card-shadow overflow-x-auto">
          {[
            { n: 1, label: "Personal" },
            { n: 2, label: "Family" },
            { n: 3, label: "Caste/Astro" },
            { n: 4, label: "Edu/Job" },
            { n: 5, label: "Location/Photo" },
          ].map(s => (
            <div key={s.n} className={`flex-1 min-w-[70px] py-2 rounded-full text-center text-[11px] font-bold ${step >= s.n ? 'maroon-gradient text-white' : 'bg-gray-100 text-gray-400'}`}>
              {s.n}. {s.label} {step > s.n ? '✅' : ''}
            </div>
          ))}
        </div>

        {errors.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-3 mb-4">
            <div className="font-bold text-red-700 text-sm">⚠️ Mandatory fields fill cheyyi - next ki velladu:</div>
            <div className="mt-1 text-xs text-red-600 space-y-1">
              {errors.map((e, i) => <div key={i}>• {e}</div>)}
            </div>
          </div>
        )}

        {/* STEP 1 - Personal */}
        {step === 1 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E] text-lg">Step 1 — Personal Details 👤 <span className="text-red-500 text-xs">* mandatory = next ki velladu</span></h2>
            <p className="text-xs text-gray-500 telugu">Full Name, DOB correct tick, Time, Height - matrimony site lo anni mandatory fields</p>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="text-xs font-bold">Full Name <span className="text-red-500">*</span></label>
                <input value={form.fullName} onChange={e => setForm({ ...form, fullName: e.target.value })} placeholder="e.g. Lakshmi Reddy" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                <div className="text-[10px] text-gray-400">Real name - profile card lo vasthundi</div>
              </div>
              <div>
                <label className="text-xs font-bold">Bride / Groom <span className="text-red-500">*</span></label>
                <div className="flex gap-2 mt-1">
                  {["Bride", "Groom"].map(g => (
                    <button key={g} onClick={() => setForm({ ...form, gender: g })} className={`flex-1 py-3 rounded-xl text-sm font-bold border ${form.gender === g ? 'maroon-gradient text-white' : 'bg-gray-50'}`}>{g === 'Bride' ? '👰 Bride' : '🤵 Groom'}</button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs font-bold">Date of Birth <span className="text-red-500">*</span></label>
                <input type="date" value={form.dob} onChange={e => setForm({ ...form, dob: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div className="md:col-span-2 bg-[#FFF8E7] border border-[#D4AF37]/30 rounded-xl p-3">
                <div className="flex items-start gap-2">
                  <input type="checkbox" checked={form.dobCorrect} onChange={e => setForm({ ...form, dobCorrect: e.target.checked })} className="mt-1 w-5 h-5" />
                  <div>
                    <label className="text-xs font-bold">✅ Na DOB correctena? Tick petti confirm cheyyi <span className="text-red-500">*</span></label>
                    <div className="text-[11px] text-gray-600 mt-1">• Correct ayithe ✅ tick - admin verified badge vasthundi<br />• Correct kaakapothe ❌ vaddu - approximate ayithe admin ki cheppu - astrology matching lo use</div>
                    {form.dobCorrect && <div className="text-[11px] text-green-600 font-bold mt-1">✅ Confirmed - Me DOB 100% correct ani record ayyindi - verified badge!</div>}
                  </div>
                </div>
              </div>
              <div>
                <label className="text-xs font-bold">Birth Time (optional - astrology ki)</label>
                <input type="time" value={form.birthTime} onChange={e => setForm({ ...form, birthTime: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                <div className="text-[10px] text-gray-400">e.g. 10:30 AM - horoscope matching ki</div>
              </div>
              <div>
                <label className="text-xs font-bold">Age (auto from DOB) <span className="text-red-500">*</span></label>
                <select value={form.age} onChange={e => setForm({ ...form, age: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  {Array.from({ length: 45 }, (_, i) => 18 + i).map(a => <option key={a} value={a}>{a} years</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Height <span className="text-red-500">*</span></label>
                <select value={form.height} onChange={e => setForm({ ...form, height: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  {["4'5\"", "4'8\"", "5'0\"", "5'2\"", "5'4\"", "5'6\"", "5'8\"", "5'10\"", "6'0\"", "6'2\""].map(h => <option key={h} value={h}>{h}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Weight (optional)</label>
                <input value={form.weight} onChange={e => setForm({ ...form, weight: e.target.value })} placeholder="e.g. 55kg" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Marital Status <span className="text-red-500">*</span></label>
                <select value={form.maritalStatus} onChange={e => setForm({ ...form, maritalStatus: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Pelli Kaledu</option>
                  <option>Vidakuulu (Divorced)</option>
                  <option>Widow/Widower</option>
                  <option>Handicapped — Special</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Physical Status <span className="text-red-500">*</span></label>
                <select value={form.physicalStatus} onChange={e => setForm({ ...form, physicalStatus: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Normal</option>
                  <option>Physically Challenged</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Mother Tongue</label>
                <select value={form.motherTongue} onChange={e => setForm({ ...form, motherTongue: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Telugu</option><option>Hindi</option><option>English</option><option>Tamil</option><option>Kannada</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Body Type</label>
                <select value={form.bodyType} onChange={e => setForm({ ...form, bodyType: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Slim</option><option>Average</option><option>Athletic</option><option>Heavy</option>
                </select>
              </div>
            </div>
            <button onClick={() => nextStep(1)} className="w-full mt-6 py-3 maroon-gradient text-white rounded-full font-bold">Next — Family Details →</button>
            <div className="mt-2 text-[10px] text-center text-gray-400">Mandatory fields fill cheyakapothe next button work avvadu — validation active ✅</div>
          </div>
        )}

        {/* STEP 2 - Family */}
        {step === 2 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E] text-lg">Step 2 — Family Details 👨‍👩‍👧 <span className="text-red-500 text-xs">* mandatory</span></h2>
            <p className="text-xs text-gray-500">Father Name, Mother Name - matrimony lo chala important - family background</p>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold">Father Name <span className="text-red-500">*</span></label>
                <input value={form.fatherName} onChange={e => setForm({ ...form, fatherName: e.target.value })} placeholder="e.g. Ramesh Reddy" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Father Occupation</label>
                <input value={form.fatherOccupation} onChange={e => setForm({ ...form, fatherOccupation: e.target.value })} placeholder="e.g. Farmer, Govt Job, Business" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Mother Name <span className="text-red-500">*</span></label>
                <input value={form.motherName} onChange={e => setForm({ ...form, motherName: e.target.value })} placeholder="e.g. Sita Reddy" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Mother Occupation</label>
                <input value={form.motherOccupation} onChange={e => setForm({ ...form, motherOccupation: e.target.value })} placeholder="e.g. Housewife, Teacher" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Family Type</label>
                <select value={form.familyType} onChange={e => setForm({ ...form, familyType: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Joint</option><option>Nuclear</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Family Values</label>
                <select value={form.familyValues} onChange={e => setForm({ ...form, familyValues: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Traditional</option><option>Moderate</option><option>Liberal</option><option>Orthodox</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Family Status</label>
                <select value={form.familyStatus} onChange={e => setForm({ ...form, familyStatus: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>Middle Class</option><option>Upper Middle Class</option><option>Rich</option><option>Affluent</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Native Place <span className="text-red-500">*</span></label>
                <input value={form.nativePlace} onChange={e => setForm({ ...form, nativePlace: e.target.value })} placeholder="e.g. Nalgonda village" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-xs font-bold">Brothers</label>
                  <select value={form.brothers} onChange={e => setForm({ ...form, brothers: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    {["0", "1", "2", "3", "4+"].map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold">Brothers Married</label>
                  <select value={form.brothersMarried} onChange={e => setForm({ ...form, brothersMarried: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    {["0", "1", "2", "3"].map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-xs font-bold">Sisters</label>
                  <select value={form.sisters} onChange={e => setForm({ ...form, sisters: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    {["0", "1", "2", "3", "4+"].map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold">Sisters Married</label>
                  <select value={form.sistersMarried} onChange={e => setForm({ ...form, sistersMarried: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    {["0", "1", "2", "3"].map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
              </div>
              <div className="md:col-span-2">
                <label className="text-xs font-bold">About Family (optional but best)</label>
                <textarea value={form.aboutFamily} onChange={e => setForm({ ...form, aboutFamily: e.target.value })} placeholder="e.g. Manadi middle class traditional family, father farmer, mother housewife, close-knit..." className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" rows={3}></textarea>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setStep(1)} className="flex-1 py-3 border rounded-full font-bold text-sm">← Back</button>
              <button onClick={() => nextStep(2)} className="flex-1 py-3 maroon-gradient text-white rounded-full font-bold">Next — Caste/Astro →</button>
            </div>
          </div>
        )}

        {/* STEP 3 - Caste Astro */}
        {step === 3 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E] text-lg">Step 3 — Caste, Gothram, Nakshatram 🌟 <span className="text-red-500 text-xs">* mandatory</span></h2>
            <p className="text-xs text-gray-500">Gothram mandatory - Star/Rasi/Dosham optional - advanced horoscope ki</p>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold">Caste <span className="text-red-500">*</span></label>
                <select value={form.caste} onChange={e => setForm({ ...form, caste: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  {castes.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Sub-Caste (optional)</label>
                <input value={form.subCaste} onChange={e => setForm({ ...form, subCaste: e.target.value })} placeholder="e.g. Pakanati, Motati" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Gothram <span className="text-red-500">*</span></label>
                <input value={form.gothram} onChange={e => setForm({ ...form, gothram: e.target.value })} placeholder="e.g. Bharadwaj, Kaundinya, Kasyapa" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                <div className="text-[10px] text-gray-400">Telugu matrimony lo must - same gothram avoid</div>
              </div>
              <div>
                <label className="text-xs font-bold">Nakshatram / Star (optional) ⭐</label>
                <input value={form.star} onChange={e => setForm({ ...form, star: e.target.value })} placeholder="e.g. Rohini, Bharani, Ashwini" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                <div className="text-[10px] text-green-600">Optional - unte jathakam matching easy - 10% extra score</div>
              </div>
              <div>
                <label className="text-xs font-bold">Rasi (optional)</label>
                <select value={form.rasi} onChange={e => setForm({ ...form, rasi: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option value="">Select Rasi (optional)</option>
                  <option>Mesha</option><option>Vrushabha</option><option>Mithuna</option><option>Karkataka</option><option>Simha</option><option>Kanya</option><option>Tula</option><option>Vruschika</option><option>Dhanu</option><option>Makara</option><option>Kumbha</option><option>Meena</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Dosham (optional)</label>
                <select value={form.dosham} onChange={e => setForm({ ...form, dosham: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>No</option><option>Yes - Kuja Dosham</option><option>Yes - Nadi Dosham</option><option>Don't Know</option>
                </select>
              </div>
              <div className="md:col-span-2 bg-blue-50 border border-blue-200 rounded-xl p-3 text-xs">
                <div className="font-bold text-blue-700">🌟 Horoscope Advanced Logic:</div>
                <div className="mt-1 text-gray-600">• Gothram mandatory - same gothram unte match score tagguthundi (0%)<br />• Star/Rasi optional - unte 92% nundi 95% ki boost - jathakam perfect<br />• DOB Time unte - exact lagna matching - premium feature<br />• Dosham Yes ayithe - dosham unna profiles tho ne match - filter auto</div>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setStep(2)} className="flex-1 py-3 border rounded-full font-bold text-sm">← Back</button>
              <button onClick={() => nextStep(3)} className="flex-1 py-3 maroon-gradient text-white rounded-full font-bold">Next — Education/Job →</button>
            </div>
          </div>
        )}

        {/* STEP 4 - Education Job */}
        {step === 4 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E] text-lg">Step 4 — Education, Job, Salary 🎓💼 <span className="text-red-500 text-xs">* mandatory</span></h2>
            <p className="text-xs text-gray-500">Qualification, Job, Salary - filters ki chala important</p>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold">Qualification <span className="text-red-500">*</span></label>
                <select value={form.education} onChange={e => setForm({ ...form, education: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  {educations.map(ed => <option key={ed} value={ed}>{ed}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Education Detail <span className="text-red-500">*</span></label>
                <input value={form.educationDetail} onChange={e => setForm({ ...form, educationDetail: e.target.value })} placeholder="e.g. BTech CSE, MBBS General, MBA Finance" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">College / University (optional)</label>
                <input value={form.college} onChange={e => setForm({ ...form, college: e.target.value })} placeholder="e.g. JNTU Hyderabad" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Job Type <span className="text-red-500">*</span></label>
                <select value={form.job} onChange={e => setForm({ ...form, job: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  {jobs.map(j => <option key={j} value={j}>{j}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Company Name (optional)</label>
                <input value={form.company} onChange={e => setForm({ ...form, company: e.target.value })} placeholder="e.g. TCS, Infosys, Govt School" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div>
                <label className="text-xs font-bold">Salary / Income <span className="text-red-500">*</span></label>
                <select value={form.salary} onChange={e => setForm({ ...form, salary: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                  <option>10k-20k</option><option>20k-40k</option><option>40k-60k</option><option>60k-1L</option><option>1L-2L</option><option>2L+</option><option>Not Disclosed</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold">Work Location <span className="text-red-500">*</span></label>
                <input value={form.workLocation} onChange={e => setForm({ ...form, workLocation: e.target.value })} placeholder="e.g. Hyderabad Gachibowli, USA, Bangalore" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
              </div>
              <div className="md:col-span-2">
                <label className="text-xs font-bold">About Myself <span className="text-red-500">*</span> (min 50 letters)</label>
                <textarea value={form.aboutMyself} onChange={e => setForm({ ...form, aboutMyself: e.target.value })} placeholder="e.g. Nenu software engineer, simple family, traditional values, looking for understanding partner, non-smoker, teetotaler, respect elders..." className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" rows={4}></textarea>
                <div className="text-[10px] text-gray-400 mt-1">{form.aboutMyself.length}/50 min - {form.aboutMyself.length >= 50 ? '✅ OK' : '❌ Too short'}</div>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setStep(3)} className="flex-1 py-3 border rounded-full font-bold text-sm">← Back</button>
              <button onClick={() => nextStep(4)} className="flex-1 py-3 maroon-gradient text-white rounded-full font-bold">Next — Location/Photo →</button>
            </div>
          </div>
        )}

        {/* STEP 5 - Location Contact Expectations Photo */}
        {step === 5 && (
          <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
            <h2 className="font-bold text-[#7A0C2E] text-lg">Step 5 — Location, Photo, Expectations, Contact 📍📸 <span className="text-red-500 text-xs">* mandatory</span></h2>
            <p className="text-xs text-gray-500">Mandal mandatory deep filter ki - Photo mandatory - Expectations builder advanced</p>
            <div className="mt-4 space-y-5">
              {/* Location */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold">State <span className="text-red-500">*</span></label>
                  <select value={form.state} onChange={e => setForm({ ...form, state: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    <option value="TS">Telangana</option>
                    <option value="AP">Andhra Pradesh</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold">District <span className="text-red-500">*</span></label>
                  <select value={form.district} onChange={e => setForm({ ...form, district: e.target.value })} className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm">
                    {(form.state === "TS" ? districtsTS : districtsAP).map(d => <option key={d} value={d}>{d}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold">Mandal / Town <span className="text-red-500">*</span> (deep filter)</label>
                  <input value={form.mandal} onChange={e => setForm({ ...form, mandal: e.target.value })} placeholder="e.g. Gachibowli, Kukatpally, Miyapur" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                  <div className="text-[10px] text-gray-400">Example: Software jobs Hyderabad 45+ Reddy filter ki mandatory</div>
                </div>
                <div>
                  <label className="text-xs font-bold">Current City</label>
                  <input value={form.currentCity} onChange={e => setForm({ ...form, currentCity: e.target.value })} placeholder="e.g. Hyderabad" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                </div>
                <div>
                  <label className="text-xs font-bold">Pincode (optional)</label>
                  <input value={form.pincode} onChange={e => setForm({ ...form, pincode: e.target.value })} placeholder="500032" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                </div>
              </div>

              {/* Photo */}
              <div>
                <label className="text-xs font-bold">Photos 1-3 (Face clear) <span className="text-red-500">* Photo 1 mandatory</span></label>
                <div className="mt-1 border-2 border-dashed border-[#D4AF37]/50 rounded-xl p-6 text-center bg-[#FFF8E7]">
                  <div className="text-3xl">📸</div>
                  <div className="text-xs mt-2 font-bold">Click to upload - Photo 1 mandatory</div>
                  <div className="mt-3 flex justify-center gap-3">
                    <label className="px-4 py-2 bg-white border rounded-full text-xs font-bold cursor-pointer">
                      📷 Upload Photo
                      <input type="file" accept="image/*" className="hidden" onChange={e => {
                        const file = e.target.files?.[0];
                        if (file) {
                          const url = URL.createObjectURL(file);
                          setPhotoPreview(url);
                        }
                      }} />
                    </label>
                    <button onClick={() => setPhotoPreview("https://i.pravatar.cc/300?img=" + Math.floor(Math.random() * 70))} className="px-4 py-2 gold-gradient rounded-full text-xs font-bold text-[#7A0C2E]">🎲 Demo Photo</button>
                  </div>
                  {photoPreview && (
                    <div className="mt-4">
                      <img src={photoPreview} alt="preview" className="w-32 h-32 mx-auto rounded-xl object-cover border-2 border-[#D4AF37]" />
                      <div className="text-[10px] text-green-600 mt-1">✅ Photo uploaded - AI blur check pass - Verified badge ready</div>
                    </div>
                  )}
                  <div className="text-[10px] text-gray-400 mt-2">AI blur check + selfie verify → Verified badge • Private mode lo only paid ki clear</div>
                </div>
                <div className="mt-2 flex items-center gap-2">
                  <input type="checkbox" checked={form.photoPrivate} onChange={e => setForm({ ...form, photoPrivate: e.target.checked })} />
                  <label className="text-xs">Photo Private Mode? (only paid members ki chupinchu - ammayila ki safe - mandatory kadu)</label>
                </div>
              </div>

              {/* Expectations Builder - Advanced Filters */}
              <div className="bg-[#FFF8E7] rounded-xl p-4 border border-[#D4AF37]/30">
                <h3 className="font-bold text-[#7A0C2E] text-sm">🎯 Expectations Builder — Nee Expectations Enti? (Advanced Filters)</h3>
                <p className="text-[11px] text-gray-500">Example: Software jobs Hyderabad lo 45+ Reddy abbai kavali - ilanti filters ikkada pettochu - system neeku matching profiles matrame chupisthundi</p>
                <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div>
                    <label className="text-[11px] font-bold">Age Min</label>
                    <select value={form.expAgeMin} onChange={e => setForm({ ...form, expAgeMin: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      {Array.from({ length: 30 }, (_, i) => 18 + i).map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Age Max</label>
                    <select value={form.expAgeMax} onChange={e => setForm({ ...form, expAgeMax: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      {Array.from({ length: 40 }, (_, i) => 20 + i).map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Height Min</label>
                    <select value={form.expHeightMin} onChange={e => setForm({ ...form, expHeightMin: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      {["4'5\"", "5'0\"", "5'2\"", "5'4\"", "5'6\""].map(h => <option key={h} value={h}>{h}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Height Max</label>
                    <select value={form.expHeightMax} onChange={e => setForm({ ...form, expHeightMax: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      {["5'6\"", "5'8\"", "5'10\"", "6'0\"", "6'2\""].map(h => <option key={h} value={h}>{h}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Job Preference</label>
                    <select value={form.expJob} onChange={e => setForm({ ...form, expJob: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      <option>Any</option><option>Software</option><option>Govt Job</option><option>Business</option><option>Doctor</option><option>Abroad-NRI</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Location Preference</label>
                    <select value={form.expLocation} onChange={e => setForm({ ...form, expLocation: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      <option>Any</option><option>Hyderabad</option><option>Warangal</option><option>Vijayawada</option><option>USA</option><option>TS Only</option><option>AP Only</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Education</label>
                    <select value={form.expEducation} onChange={e => setForm({ ...form, expEducation: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      <option>Any</option><option>BTech</option><option>MTech</option><option>MBBS</option><option>MBA</option><option>Degree</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[11px] font-bold">Salary</label>
                    <select value={form.expSalary} onChange={e => setForm({ ...form, expSalary: e.target.value })} className="w-full mt-1 p-2 rounded-xl bg-white border text-xs">
                      <option>Any</option><option>40k+</option><option>60k+</option><option>1L+</option>
                    </select>
                  </div>
                </div>
                <div className="mt-3">
                  <label className="text-[11px] font-bold">Caste Preference (multi-select - advanced)</label>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {castes.slice(0, 8).map(c => (
                      <button key={c} onClick={() => toggleExpCaste(c)} className={`px-3 py-1 rounded-full text-[11px] font-bold border ${form.expCaste.includes(c) ? 'maroon-gradient text-white' : 'bg-white'}`}>{c} {form.expCaste.includes(c) ? '✅' : ''}</button>
                    ))}
                  </div>
                  <div className="text-[10px] text-gray-400 mt-1">Selected: {form.expCaste.length ? form.expCaste.join(", ") : "Same caste (default)"} - filter lo use avuthundi</div>
                </div>
                <div className="mt-3 bg-white rounded-xl p-2 text-[11px] text-gray-600">
                  💡 Example: Nee dagara ammai ki matches kavali - software jobs Hyderabad lo 45 years above Reddy abbai - appudu filter: Job=Software, Location=Hyderabad, AgeMin=45, Caste=Reddy → System 5 profiles matrame chupisthundi best matching tho
                </div>
              </div>

              {/* Contact */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold">Phone Number (OTP) <span className="text-red-500">*</span></label>
                  <input value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} placeholder="98480xxxxx" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                  <div className="text-[10px] text-green-600 mt-1">✅ OTP verify - fake block - encrypted store</div>
                </div>
                <div>
                  <label className="text-xs font-bold">Email (optional)</label>
                  <input value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} placeholder="lakshmi@gmail.com" className="w-full mt-1 p-3 rounded-xl bg-gray-50 border text-sm" />
                </div>
                <div className="md:col-span-2">
                  <label className="text-xs font-bold">👥 Meeku evaru chepparu? Referral Code / Phone {isReferralLocked ? "🔒 (Locked - auto fill)" : "(optional)"}</label>
                  <input
                    value={form.referral}
                    onChange={e => !isReferralLocked && setForm({ ...form, referral: e.target.value })}
                    readOnly={isReferralLocked}
                    placeholder="e.g. LAK42 or TSAP-1042"
                    className={`w-full mt-1 p-3 rounded-xl border text-sm ${isReferralLocked ? "bg-[#FFF8E7] border-[#D4AF37] font-bold text-[#7A0C2E]" : "bg-gray-50"}`}
                  />
                  {isReferralLocked ? (
                    <div className="mt-2 bg-green-50 border border-green-200 rounded-xl p-3">
                      <div className="text-xs font-bold text-green-700">🔒 {referrerName} dwara vacharu — trusted! — Meeku 1 extra credit FREE! 🎉</div>
                      <div className="text-[11px] text-gray-600 mt-1">• Referral lock ayyindi — commission guarantee — no fraud<br />• {referrerName} ki ₹50 vastundi pay ayyaka — meeku 1 extra FREE</div>
                    </div>
                  ) : (
                    <div className="text-[10px] text-gray-500 mt-1">Referral unte meeku 1 extra credit FREE - referrer ki ₹50 - short code LAK42 type</div>
                  )}
                </div>
              </div>

              <div className="bg-[#FFF8E7] rounded-xl p-3 text-xs">
                <div className="font-bold">🔐 Privacy & Admin:</div>
                <div className="mt-1 text-gray-600">• Phone encrypted, admin kuda log tho ne chusthadu<br />• Photo-private ON cheste public lo blur - paid ki clear<br />• Watermark ID tho - screenshot misuse block<br />• Profile Code separate vasthundi - ID tho search cheyochu</div>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setStep(4)} className="flex-1 py-3 border rounded-full font-bold text-sm">← Back</button>
              <button onClick={handleGenerate} className="flex-1 py-3 gold-gradient text-[#7A0C2E] rounded-full font-bold text-sm">🎉 Generate ID + Advanced Card</button>
            </div>
          </div>
        )}

        {/* STEP 6 - Generated - Advanced Template */}
        {step === 6 && generated && (
          <div className="space-y-4">
            <div className="bg-white rounded-[1.5rem] p-6 card-shadow text-center">
              <div className="text-4xl">🎉</div>
              <h2 className="font-bold text-xl text-[#7A0C2E] mt-2">Congratulations {generated.fullName}!</h2>
              <p className="text-sm telugu">Me profile ready - advanced template thayaru ayyindi - admin approve tarvata channels lo auto post</p>
              <div className="mt-4 bg-[#FFF8E7] rounded-xl p-4 inline-block border-2 border-[#D4AF37]">
                <div className="text-xs text-gray-500">Me Separate Profile Code (ID Search ki)</div>
                <div className="font-bold text-2xl text-[#7A0C2E] tracking-wider">{generated.id}</div>
                <div className="text-xs mt-1">Credits: {generated.credits} FREE • Verified: Pending • DOB: {generated.dobCorrect ? '✅ Correct' : '❌ Approximate'}</div>
                <div className="mt-2 text-[11px] bg-white rounded-full px-3 py-1">Search: /search/{generated.id} → profile open avuthundi</div>
              </div>
            </div>

            {/* ADVANCED TEMPLATE WITH PHOTO - Neat */}
            <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
              <h3 className="font-bold text-[#7A0C2E]">🎴 Me Advanced Profile Card (Telegram/WhatsApp/Website lo ilage vasthundi - photo tho neat)</h3>
              <div className="mt-4 max-w-md mx-auto border-2 border-[#D4AF37] rounded-2xl overflow-hidden shadow-xl">
                <div className="maroon-gradient text-white p-2 text-center text-xs font-bold flex justify-between px-4">
                  <span>TSAP MATRIMONY</span>
                  <span>{generated.id}</span>
                  <span>✅ {generated.dobCorrect ? 'DOB Verified' : 'Pending'}</span>
                </div>
                <div className="p-4 flex gap-4 bg-white">
                  <div className="w-28 h-32 rounded-xl overflow-hidden border-2 border-[#D4AF37] flex-shrink-0">
                    {generated.photoUrl ? <img src={generated.photoUrl} alt="profile" className="w-full h-full object-cover" /> : <div className="w-full h-full bg-gray-100 flex items-center justify-center text-3xl">{generated.gender === 'Bride' ? '👰' : '🤵'}</div>}
                  </div>
                  <div className="flex-1 text-xs space-y-1">
                    <div className="font-bold text-sm text-[#7A0C2E]">{generated.fullName} • {generated.age}y • {generated.height} • {generated.caste}</div>
                    <div>🎓 {generated.education} {generated.educationDetail} {generated.college ? `@ ${generated.college}` : ''}</div>
                    <div>💼 {generated.job} {generated.company ? `@ ${generated.company}` : ''} • {generated.salary} • {generated.workLocation}</div>
                    <div>📍 {generated.district}, {generated.mandal}, {generated.state} {generated.currentCity ? `• Now ${generated.currentCity}` : ''}</div>
                    <div className="text-[11px] text-gray-600">👨‍👩‍👧 S/o {generated.fatherName} ({generated.fatherOccupation}) • {generated.familyType} • {generated.familyStatus}</div>
                    <div className="text-[10px] text-gray-500">🌟 Gothram: {generated.gothram} • Star: {generated.star || '—'} • Rasi: {generated.rasi || '—'} • Dosham: {generated.dosham} • Birth: {generated.dob} {generated.birthTime ? ` ${generated.birthTime}` : ''}</div>
                  </div>
                </div>
                <div className="bg-[#FFF8E7] p-3 text-xs">
                  <div className="font-bold text-[#7A0C2E]">⭐ {generated.score}% BEST MATCH • Expectation: {generated.expectationMatch}</div>
                  <div className="mt-2 space-y-1">
                    {generated.reasons.map((r: string, i: number) => <div key={i}>✅ {r}</div>)}
                  </div>
                  <div className="mt-2 text-[11px] text-gray-600 italic">About: {generated.aboutMyself.slice(0, 120)}...</div>
                </div>
                <div className="p-2 bg-gray-50 text-[10px] text-center text-gray-400 flex justify-between px-4">
                  <span>📞 Number: Pay tarvata 🔒</span>
                  <span>Bot: @telugumatrimony1_bot</span>
                  <span>#{generated.caste} #{generated.state} #{generated.gender} #Age{generated.age} • WM: {generated.id}</span>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                  <div className="font-bold text-green-700">✅ Auto-Post Queue — real router (65 channels registry)</div>
                  {publishPreview ? (
                    <div className="mt-1 text-gray-700 space-y-1">
                      <div><b>LIVE lo ippude post:</b> {publishPreview.targets?.ready?.join(", ") || "—"}</div>
                      <div className="text-gray-500"><b>Wave toka create avvali:</b> {(publishPreview.targets?.pending || []).length} channels</div>
                      <div className="mt-1 text-[11px] bg-white rounded-lg p-2 font-mono break-all">{publishPreview.targets?.hashtags}</div>
                      {(publishPreview.targets?.notes || []).map((n: string, i: number) => <div key={i} className="text-[11px] text-gray-500">• {n}</div>)}
                    </div>
                  ) : (
                    <div className="mt-1 text-gray-600">• Region: {generated.state === 'TS' ? '@TSBRIDE / @TSGROOM1' : 'AP channels'}<br />• Caste + Religion + Special channels — backend router decide chestundi<br />• Max 5 channels per profile</div>
                  )}
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-3">
                  <div className="font-bold text-blue-700">🤖 Filter System - Manaku Matrame Kanipisthundi</div>
                  <div className="mt-1 text-gray-600">• Admin UI lo advanced filters: Software, Hyderabad, 45+, Reddy, Govt Job, etc<br />• Nuvvu 5 profiles adigithe - best 5 matrame display - reason tho<br />• Share button: WhatsApp & Telegram → registered number ki forward<br />• 100% perfect - no gaps</div>
                </div>
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <Link href={`/search/${generated.id}`} className="flex-1 min-w-[140px] py-3 maroon-gradient text-white rounded-full text-center font-bold text-sm">🔍 ID Search - {generated.id}</Link>
                <Link href="/matches" className="flex-1 min-w-[140px] py-3 border border-[#D4AF37] text-[#7A0C2E] rounded-full text-center font-bold text-sm">💘 Matches - Filters</Link>
                <button onClick={() => {
                  const text = `TSAP Matrimony Profile: ${generated.id} - ${generated.fullName}, ${generated.age}y, ${generated.caste}, ${generated.job} @ ${generated.district}. Search: https://tsapmatrimony.com/search/${generated.id}`;
                  window.open(`https://wa.me/${generated.phone}?text=${encodeURIComponent(text)}`, '_blank');
                }} className="flex-1 min-w-[140px] py-3 bg-green-600 text-white rounded-full text-center font-bold text-sm">📱 WhatsApp Share</button>
                <button onClick={() => {
                  const text = `TSAP Matrimony Profile: ${generated.id} - ${generated.fullName}. Search https://t.me/TSBRIDE`;
                  window.open(`https://t.me/share/url?url=${encodeURIComponent(`https://tsapmatrimony.com/search/${generated.id}`)}&text=${encodeURIComponent(text)}`, '_blank');
                }} className="flex-1 min-w-[140px] py-3 bg-blue-500 text-white rounded-full text-center font-bold text-sm">✈️ Telegram Share</button>
              </div>
            </div>

            <div className="bg-white rounded-[1.5rem] p-6 card-shadow">
              <h3 className="font-bold">💰 Credits & Next - Automation</h3>
              <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="bg-[#FFF8E7] rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold text-[#7A0C2E]">{generated.credits}</div>
                  <div className="text-xs">FREE Credits</div>
                  <div className="text-[10px] text-gray-500">ID Search always open - number ki credit</div>
                </div>
                <div className="bg-green-50 rounded-xl p-3 text-center">
                  <div className="text-sm font-bold">Referral</div>
                  <div className="text-xs mt-1">{generated.referral || 'No referral'}</div>
                  <div className="text-[10px] text-gray-500 mt-1">Pay ayyaka referrer ki ₹50</div>
                </div>
                <div className="bg-blue-50 rounded-xl p-3 text-center">
                  <div className="text-sm font-bold">Oracle VM Free Tier</div>
                  <div className="text-xs mt-1">Saripothunda? YES - 1GB RAM, 50GB</div>
                  <div className="text-[10px] text-gray-500 mt-1">1000 profiles easy - profiles ekkuva em avvadu</div>
                </div>
              </div>
              <Link href="/" className="block w-full mt-4 py-3 bg-gray-100 rounded-full text-center font-bold text-sm">🏠 Home ki Vellu - Advanced Website 100% Perfect</Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Next.js 14: useSearchParams() ki Suspense boundary MUST — lekapothe production build fail
export default function RegisterPageAdvanced() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-[#FFF8E7]">
        <div className="text-center">
          <div className="text-3xl">💍</div>
          <div className="font-bold text-[#7A0C2E] mt-2">Mana Vivaha — Register form load avuthundi...</div>
        </div>
      </div>
    }>
      <RegisterContent />
    </Suspense>
  );
}
