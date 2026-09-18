import type { MetadataRoute } from "next";

const SITE = process.env.SITE_URL || "https://manavivaha.in";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        // Private/owner pages — index avvakudadu (privacy)
        disallow: ["/admin", "/admin/photos", "/growth", "/api/", "/search/"],
      },
    ],
    sitemap: `${SITE}/sitemap.xml`,
    host: SITE,
  };
}
