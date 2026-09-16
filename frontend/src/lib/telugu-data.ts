/**
 * MANA VIVAHA — SMART FORM DATA (Telugu-first pickers)
 * ====================================================
 * Phone lo type cheyyadam kanna **tap cheyyadam** easy — so anni options chips ga.
 * (Form lo 70%+ fields chip/stepper tho — 3 nimushalalo complete avutundi)
 */

// 27 nakshatras — Telugu + English (form lo rendu kanipisthayi)
export const NAKSHATRAS: { te: string; en: string }[] = [
  { te: "అశ్విని", en: "Ashwini" }, { te: "భరణి", en: "Bharani" }, { te: "కృత్తిక", en: "Krittika" },
  { te: "రోహిణి", en: "Rohini" }, { te: "మృగశిర", en: "Mrigasira" }, { te: "ఆరుద్ర", en: "Ardra" },
  { te: "పునర్వసు", en: "Punarvasu" }, { te: "పుష్యమి", en: "Pushya" }, { te: "ఆశ్లేష", en: "Ashlesha" },
  { te: "మఘ", en: "Magha" }, { te: "పూర్వ ఫల్గుణి", en: "Pubba" }, { te: "ఉత్తర ఫల్గుణి", en: "Uttara" },
  { te: "హస్త", en: "Hasta" }, { te: "చిత్ర", en: "Chitra" }, { te: "స్వాతి", en: "Swati" },
  { te: "విశాఖ", en: "Vishakha" }, { te: "అనూరాధ", en: "Anuradha" }, { te: "జ్యేష్ఠ", en: "Jyeshtha" },
  { te: "మూల", en: "Moola" }, { te: "పూర్వాషాఢ", en: "Purvashadha" }, { te: "ఉత్తరాషాఢ", en: "Uttarashadha" },
  { te: "శ్రవణం", en: "Shravana" }, { te: "ధనిష్ఠ", en: "Dhanishta" }, { te: "శతభిషం", en: "Shatabhisha" },
  { te: "పూర్వాభాద్ర", en: "Purvabhadra" }, { te: "ఉత్తరాభాద్ర", en: "Uttarabhadra" }, { te: "రేవతి", en: "Revati" },
];

// nakshatra → rasi (auto-suggest: star select chesthe rasi automatic ga vastundi)
export const NAK_TO_RASI: Record<string, string> = (() => {
  const map: Record<string, string> = {};
  const rasiOrder = ["Mesha", "Vrishabha", "Mithuna", "Karkataka", "Simha", "Kanya",
                     "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"];
  const idx = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 11];
  NAKSHATRAS.forEach((n, i) => { map[n.en] = rasiOrder[idx[i]]; });
  return map;
})();

export const RASIS: { te: string; en: string }[] = [
  { te: "మేషం", en: "Mesha" }, { te: "వృషభం", en: "Vrishabha" }, { te: "మిథునం", en: "Mithuna" },
  { te: "కర్కాటకం", en: "Karkataka" }, { te: "సింహం", en: "Simha" }, { te: "కన్య", en: "Kanya" },
  { te: "తుల", en: "Tula" }, { te: "వృశ్చికం", en: "Vrishchika" }, { te: "ధనుస్సు", en: "Dhanu" },
  { te: "మకరం", en: "Makara" }, { te: "కుంభం", en: "Kumbha" }, { te: "మీనం", en: "Meena" },
];

// 43 castes (registry tho sync — channels ki route avutundi)
export const CASTES: string[] = [
  "Reddy", "Kamma", "Kapu", "Velama", "Vysya", "Brahmin", "Raju", "Goud", "Yadav", "Mudiraj",
  "Padmashali", "Munnuru Kapu", "Balija", "Telaga", "Koppula Velama", "Kalinga", "Boya", "Kuruba",
  "Uppara", "Vaddera", "Rajaka", "Mangali", "Viswakarma", "Kummara", "Gandla", "Devanga", "Srisayana",
  "Jangam", "Jogi", "Dasari", "Bhatraju", "Gavara", "Bestha", "Jalari", "Vadabalija",
  "Mala", "Madiga", "Adi Andhra", "SC Others", "Lambada", "Koya", "Gond", "ST Others",
];

export const RELIGIONS = ["Hindu", "Muslim", "Christian", "Sikh", "Jain", "Buddhist", "Other"];

export const MOTHER_TONGUES = ["Telugu", "Urdu", "Hindi", "Tamil", "Kannada", "English", "Other"];

export const HEIGHTS = [
  '4\'8"', '4\'9"', '4\'10"', '4\'11"', '5\'0"', '5\'1"', '5\'2"', '5\'3"', '5\'4"', '5\'5"',
  '5\'6"', '5\'7"', '5\'8"', '5\'9"', '5\'10"', '5\'11"', '6\'0"', '6\'1"', '6\'2"', '6\'3"',
  '6\'4"', '6\'5"', '6\'6"',
];

export const WEIGHTS = Array.from({ length: 61 }, (_, i) => `${40 + i}kg`);

export const EDUCATIONS = ["SSC", "Intermediate", "Diploma", "BCom", "BSc", "BA", "BBA", "BTech", "BE",
  "BPharm", "BEd", "MBBS", "BDS", "LLB", "MCom", "MSc", "MA", "MBA", "MTech", "MCA", "MD", "MS",
  "MPharm", "PhD", "CA", "ICWA", "Other"];

export const JOBS = ["Software Engineer", "Doctor", "Govt Job", "Business", "Teacher", "Lecturer",
  "Bank Employee", "Private Job", "Engineer", "Accountant", "Nurse", "Pharmacist", "Lawyer",
  "Agriculture", "Police/Defence", "Driver", "Tailor", "Not Working", "Other"];

export const SALARIES = ["Not specified", "1L - 2L", "2L - 4L", "4L - 6L", "6L - 8L", "8L - 10L",
  "10L - 15L", "15L - 20L", "20L - 30L", "30L+", "50L+", "1Cr+"];

export const WORK_TYPES = ["Private", "Government", "Business", "Self Employed", "Not Working", "Retired"];

// 🌊 WAVE 16 canonical (backend-accepted; register pills map to these)
export const MARITAL_STATUSES = ["Pelli Kaledu", "Widow", "Widower", "Divorced", "Awaiting Divorce", "Separated"];
export const CHILDREN_OPTIONS = ["None", "1", "2", "3", "4+"];

// "5'6\"" → "5 ft 6 in (168 cm)" (BharatMatrimony-style pro dropdown)
export function heightLabel(h: string): string {
  const m = /^(\d)'(\d{1,2})"?$/.exec((h || "").trim());
  if (!m) return h;
  const cm = Math.round(Number(m[1]) * 30.48 + Number(m[2]) * 2.54);
  return `${m[1]} ft ${m[2]} in (${cm} cm)`;
}

export const FAMILY_TYPES = ["Nuclear", "Joint"];
// 🌊 WAVE 17 canonical (screenshot) — backend maps legacy values here
export const FAMILY_STATUSES = ["Middle Class", "Upper Middle Class", "Rich / Affluent (Elite)"];
export const FAMILY_VALUES = ["Traditional", "Moderate", "Liberal"];
export const BODY_TYPES = ["Slim", "Average", "Athletic", "Heavy"];
export const COMPLEXIONS = ["Very Fair", "Fair", "Wheatish", "Wheatish Brown", "Dark"];
export const BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"];
export const PHYSICAL_STATUS = ["Normal", "Physically Challenged"];
export const OCCUPATIONS = ["Farmer", "Business", "Govt Employee", "Private Employee", "Teacher",
  "Housewife", "Retired", "Daily Wage", "Driver", "Other"];

// TS + AP districts (chips) — registration + search rendu ikkada nunchi
export const TS_DISTRICTS = ["Hyderabad", "Rangareddy", "Medchal-Malkajgiri", "Nalgonda", "Suryapet",
  "Warangal", "Hanamkonda", "Karimnagar", "Peddapalli", "Jagtial", "Khammam", "Bhadradri Kothagudem",
  "Nizamabad", "Kamareddy", "Mahbubnagar", "Nagarkurnool", "Wanaparthy", "Jogulamba Gadwal",
  "Medak", "Sangareddy", "Siddipet", "Adilabad", "Nirmal", "Mancherial", "Vikarabad", "Yadadri Bhuvanagiri"];

export const AP_DISTRICTS = ["Vijayawada (NTR)", "Guntur", "Palnadu", "Krishna", "Visakhapatnam",
  "Anakapalli", "Tirupati", "Chittoor", "Nellore", "Kurnool", "Nandyal", "Anantapur", "Sri Sathya Sai",
  "Rajahmundry", "Kakinada", "Eluru", "Bhimavaram", "Ongole", "Prakasam", "Srikakulam", "Vizianagaram",
  "Parvathipuram", "Machilipatnam", "Bapatla", "Markapuram"];

export const DISTRICTS_BY_STATE: Record<string, string[]> = {
  TS: TS_DISTRICTS,
  AP: AP_DISTRICTS,
  Other: [],
};

/** DOB nunchi age — smart (manual type cheyyakkarledu) */
export function ageFromDob(dob: string): number | null {
  if (!dob) return null;
  const d = new Date(dob);
  if (isNaN(d.getTime())) return null;
  const diff = Date.now() - d.getTime();
  const age = Math.floor(diff / (365.25 * 24 * 3600 * 1000));
  return age > 0 && age < 100 ? age : null;
}

/** DOB input ki max date (18 years today) */
export function maxDobFor18(): string {
  const d = new Date();
  d.setFullYear(d.getFullYear() - 18);
  return d.toISOString().slice(0, 10);
}

/** Photo ni phone lo ne compress chey — slow network ki smart (10k profiles < 5GB goal) */
export async function compressImage(file: File, maxDim = 1200, quality = 0.85): Promise<File> {
  try {
    if (!file.type.startsWith("image/") || typeof document === "undefined") return file;
    const bitmap = await createImageBitmap(file);
    const scale = Math.min(1, maxDim / Math.max(bitmap.width, bitmap.height));
    const w = Math.round(bitmap.width * scale);
    const h = Math.round(bitmap.height * scale);
    const canvas = document.createElement("canvas");
    canvas.width = w; canvas.height = h;
    const ctx = canvas.getContext("2d");
    if (!ctx) return file;
    ctx.drawImage(bitmap, 0, 0, w, h);
    const blob: Blob | null = await new Promise((res) => canvas.toBlob(res, "image/jpeg", quality));
    if (!blob || blob.size >= file.size) return file;
    return new File([blob], file.name.replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" });
  } catch {
    return file;
  }
}
