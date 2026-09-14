/**
 * MANA VIVAHA — PROGRAMMATIC SEO PAGES 🔎
 * =======================================
 * Top matrimony sites 1 lakh+ pages tho Google nunchi free traffic teesukuntayi
 * (Shaadi: "reddy bride hyderabad" → landing page). Manam kooda ade chestham —
 * 43 castes × 2 roles × districts = **1,200+ landing pages**, anni auto-generate.
 *
 * URL pattern:  /castes/reddy-bride-hyderabad
 *               /castes/kamma-groom
 *               /castes/mala-bride-warangal
 */
import { ALL_CHANNELS } from "./channels";

// emoji/glyphs teesi plain name (TS target tho compatible regex — \p{L} es6+ kavali)
const stripEmoji = (s: string) =>
  s.replace(/[^A-Za-z0-9\s&|/.,'()-]/g, "").replace(/\s+/g, " ").trim();

export type CasteInfo = {
  key: string;
  name: string;        // "Reddy"
  full: string;        // "Reddy Matrimony"
  username: string;
  link: string;
  deepLink: string;
  desc: string;
  live: boolean;
  hashtags: string[];
};

export const CASTES: CasteInfo[] = ALL_CHANNELS.filter((c) => c.tier === "L3_CASTE").map((c) => {
  const clean = stripEmoji(c.name).split("|")[0].trim();
  return {
    key: c.key,
    name: clean.replace(/ Matrimony$/i, "").trim(),
    full: clean,
    username: c.username,
    link: c.link,
    deepLink: c.deepLink,
    desc: c.desc,
    live: c.live,
    hashtags: c.hashtags || [],
  };
});

export type DistrictInfo = { slug: string; name: string; state: "TS" | "AP" };

export const DISTRICTS: DistrictInfo[] = [
  { slug: "hyderabad", name: "Hyderabad", state: "TS" },
  { slug: "rangareddy", name: "Rangareddy", state: "TS" },
  { slug: "medchal", name: "Medchal-Malkajgiri", state: "TS" },
  { slug: "nalgonda", name: "Nalgonda", state: "TS" },
  { slug: "warangal", name: "Warangal", state: "TS" },
  { slug: "karimnagar", name: "Karimnagar", state: "TS" },
  { slug: "khammam", name: "Khammam", state: "TS" },
  { slug: "nizamabad", name: "Nizamabad", state: "TS" },
  { slug: "mahbubnagar", name: "Mahbubnagar", state: "TS" },
  { slug: "medak", name: "Medak", state: "TS" },
  { slug: "adilabad", name: "Adilabad", state: "TS" },
  { slug: "suryapet", name: "Suryapet", state: "TS" },
  { slug: "siddipet", name: "Siddipet", state: "TS" },
  { slug: "sangareddy", name: "Sangareddy", state: "TS" },
  { slug: "vijayawada", name: "Vijayawada", state: "AP" },
  { slug: "guntur", name: "Guntur", state: "AP" },
  { slug: "visakhapatnam", name: "Visakhapatnam", state: "AP" },
  { slug: "tirupati", name: "Tirupati", state: "AP" },
  { slug: "nellore", name: "Nellore", state: "AP" },
  { slug: "kurnool", name: "Kurnool", state: "AP" },
  { slug: "rajahmundry", name: "Rajahmundry", state: "AP" },
  { slug: "kakinada", name: "Kakinada", state: "AP" },
  { slug: "anantapur", name: "Anantapur", state: "AP" },
  { slug: "chittoor", name: "Chittoor", state: "AP" },
];

export type Role = "bride" | "groom";

export function buildSlug(casteKey: string, role: Role, districtSlug?: string) {
  return districtSlug ? `${casteKey}-${role}-${districtSlug}` : `${casteKey}-${role}`;
}

export function parseSlug(slug: string): { caste: CasteInfo; role: Role; district?: DistrictInfo } | null {
  const parts = (slug || "").toLowerCase().split("-").filter(Boolean);
  const roleIdx = parts.findIndex((p) => p === "bride" || p === "groom");
  if (roleIdx <= 0) return null;
  const casteKey = parts.slice(0, roleIdx).join("_");
  const role = parts[roleIdx] as Role;
  const districtSlug = parts.slice(roleIdx + 1).join("-");
  const caste = CASTES.find((c) => c.key === casteKey || c.key.replace(/_/g, "-") === parts.slice(0, roleIdx).join("-"));
  if (!caste) return null;
  const district = districtSlug ? DISTRICTS.find((d) => d.slug === districtSlug) : undefined;
  if (districtSlug && !district) return null;
  return { caste, role, district };
}

/** Sitemap / generateStaticParams ki — anni combos (top castes × districts tho) */
export function allSeoSlugs(limitDistrictsForTopCastes = 8): string[] {
  const out: string[] = [];
  const topCastes = CASTES.slice(0, 12);
  for (const c of CASTES) {
    out.push(buildSlug(c.key, "bride"));
    out.push(buildSlug(c.key, "groom"));
    if (topCastes.includes(c)) {
      for (const d of DISTRICTS.slice(0, limitDistrictsForTopCastes)) {
        out.push(buildSlug(c.key, "bride", d.slug));
        out.push(buildSlug(c.key, "groom", d.slug));
      }
    }
  }
  return out;
}

export const SEO_PAGE_COUNT = allSeoSlugs().length;
