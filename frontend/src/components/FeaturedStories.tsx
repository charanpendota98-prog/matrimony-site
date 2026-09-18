"use client";
/**
 * 💑 WAVE 15 — Featured success stories (admin-curated, photos + tags).
 */
import { useEffect, useState } from "react";
import { Duo } from "@/lib/duo";
import { useLang } from "@/lib/lang";

type Story = { id: string; groom: string; bride: string; photo: string;
  story_en: string; story_te: string; district: string; wedding_date: string; tags: string[] };

export default function FeaturedStories({ limit = 6 }: { limit?: number }) {
  const { lang } = useLang();
  const te = lang === "te";
  const [items, setItems] = useState<Story[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [tag, setTag] = useState("");
  useEffect(() => {
    fetch(`/api/cms/stories?limit=${limit}${tag ? `&tag=${encodeURIComponent(tag)}` : ""}`)
      .then((r) => r.json()).then((d) => {
        if (d?.success) { setItems(d.stories || []); if (d.tags) setTags(d.tags); }
      }).catch(() => {});
  }, [tag, limit]);
  if (!items.length && !tag) return null;
  return (
    <div>
      <h2 className="text-xl font-extrabold text-rose-900">💑 <Duo en="Featured success stories" te="ప్రత్యేక విజయగాథలు" /></h2>
      {tags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          <button onClick={() => setTag("")} className={`chip !py-1 !text-[11px] ${!tag ? "chip-on" : ""}`}>{te ? "అన్నీ" : "All"}</button>
          {tags.slice(0, 10).map((t) => (
            <button key={t} onClick={() => setTag(tag === t ? "" : t)}
              className={`chip !py-1 !text-[11px] ${tag === t ? "chip-on" : ""}`}>#{t}</button>
          ))}
        </div>
      )}
      <div className="mt-3 grid sm:grid-cols-2 gap-3">
        {items.map((s) => (
          <div key={s.id} className="rounded-2xl border border-rose-100 bg-white overflow-hidden shadow-sm">
            {s.photo ? <img src={s.photo} alt={`${s.groom} weds ${s.bride}`} className="w-full h-44 object-cover" loading="lazy" /> : null}
            <div className="p-3">
              <div className="font-bold text-rose-900 text-sm">💑 {s.groom} ♥ {s.bride}</div>
              <div className="text-[11px] text-gray-500">{s.district}{s.wedding_date ? ` • ${s.wedding_date}` : ""}</div>
              {s.story_te ? <p className="mt-1 text-xs telugu text-gray-700">{s.story_te}</p> : null}
              {s.story_en ? <p className="mt-1 text-[11px] text-gray-500">{s.story_en}</p> : null}
              {(s.tags || []).length > 0 && (
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {(s.tags || []).map((t) => (
                    <button key={t} onClick={() => setTag(t)} className="text-[10px] bg-rose-50 text-rose-700 rounded-full px-2 py-0.5">#{t}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      {!items.length && <p className="mt-2 text-xs text-gray-400">{te ? "ఈ tag లో stories లేవు." : "No stories in this tag."}</p>}
    </div>
  );
}
