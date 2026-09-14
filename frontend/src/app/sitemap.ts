import type { MetadataRoute } from "next";

const SITE = process.env.SITE_URL || "https://manavivaha.in";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const routes: { path: string; priority: number; freq: MetadataRoute.Sitemap[number]["changeFrequency"] }[] = [
    { path: "/", priority: 1.0, freq: "daily" },
    { path: "/register", priority: 0.95, freq: "weekly" },
    { path: "/channels", priority: 0.9, freq: "daily" },
    { path: "/channels?tier=L3_CASTE", priority: 0.85, freq: "weekly" },
    { path: "/channels?tier=L4_SPECIAL", priority: 0.8, freq: "weekly" },
    { path: "/matches", priority: 0.75, freq: "weekly" },
    { path: "/referral", priority: 0.7, freq: "weekly" },
    { path: "/referral/register", priority: 0.6, freq: "monthly" },
    { path: "/bureau", priority: 0.6, freq: "monthly" },
  ];

  return routes.map((r) => ({
    url: `${SITE}${r.path}`,
    lastModified: now,
    changeFrequency: r.freq,
    priority: r.priority,
  }));
}
