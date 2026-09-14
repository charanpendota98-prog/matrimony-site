"use client";
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ALL_CHANNELS, CHANNEL_STATS, CHANNEL_TIERS, Channel } from "@/lib/channels";

export default function ChannelsPage() {
  const [tier, setTier] = useState<string>("ALL");
  const [wave, setWave] = useState<number | 0>(0);
  const [q, setQ] = useState("");
  const [onlyLive, setOnlyLive] = useState(false);

  // ?tier=L3_CASTE / ?wave=1 / ?q=reddy — home page nunchi vachina filters apply chey
  // (Suspense avasaram ledu — build static ga ne untundi)
  useEffect(() => {
    if (typeof window === "undefined") return;
    const sp = new URLSearchParams(window.location.search);
    const t = sp.get("tier");
    const w = sp.get("wave");
    const query = sp.get("q");
    const live = sp.get("live");
    if (t && ["L0_OFFICIAL", "L1_REGION", "L2_RELIGION", "L3_CASTE", "L4_SPECIAL"].includes(t)) setTier(t);
    if (w && ["1", "2", "3", "4"].includes(w)) setWave(Number(w));
    if (query) setQ(query);
    if (live === "1") setOnlyLive(true);
  }, []);

  const list = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return ALL_CHANNELS.filter(c =>
      (tier === "ALL" || c.tier === tier) &&
      (wave === 0 || c.wave === wave) &&
      (!onlyLive || c.live) &&
      (!needle || c.name.toLowerCase().includes(needle) || c.username.toLowerCase().includes(needle) ||
        c.desc.toLowerCase().includes(needle) || c.hashtags.join(" ").toLowerCase().includes(needle))
    );
  }, [tier, wave, q, onlyLive]);

  const liveCount = ALL_CHANNELS.filter(c => c.live).length;

  return (
    <div className="min-h-screen bg-[#FFF8E7] p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <Link href="/" className="text-sm font-bold text-[#7A0C2E]">← Home</Link>
          <div className="font-bold text-[#7A0C2E]">📂 Channels — {CHANNEL_STATS.total} total</div>
          <Link href="/register" className="text-xs bg-[#7A0C2E] text-white px-3 py-1 rounded-full">Register FREE</Link>
        </div>

        {/* Hero + stats */}
        <div className="maroon-gradient rounded-[1.5rem] p-6 text-white">
          <h1 className="font-bold text-xl">📢 Mana Vivaha — Master Channel Network</h1>
          <p className="text-xs mt-1 opacity-90">
            One profile post → auto ga anni relevant channels lo ki. Region + Religion + Caste + Special — 65 channels.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4">
            {[
              { l: "Total", v: CHANNEL_STATS.total },
              { l: "Live now", v: liveCount },
              { l: "To create", v: CHANNEL_STATS.total - liveCount },
              { l: "Castes", v: CHANNEL_STATS.by_tier.L3_CASTE },
              { l: "Religions", v: CHANNEL_STATS.by_tier.L2_RELIGION },
            ].map(s => (
              <div key={s.l} className="bg-white/10 rounded-xl p-3 text-center">
                <div className="text-2xl font-bold text-[#D4AF37]">{s.v}</div>
                <div className="text-[11px]">{s.l}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Router explainer */}
        <div className="mt-4 bg-white rounded-[1.5rem] p-5 card-shadow">
          <h2 className="font-bold text-[#7A0C2E] text-sm">🤖 Bot Auto-Router — One Approve = Viral Everywhere</h2>
          <div className="mt-3 bg-[#FFF8E7] border border-[#D4AF37]/40 rounded-xl p-3 text-xs font-mono text-[#7A0C2E]">
            Reddy + TS + Bride + Software job →&nbsp;
            <span className="font-bold">@TSBRIDE → @manavivaha_reddy → @manavivaha_software</span>
            &nbsp;(max 5 channels • #Reddy #Telangana #Bride #Nalgonda #Age24)
          </div>
          <div className="grid md:grid-cols-4 gap-2 mt-3 text-[11px]">
            <div className="bg-gray-50 rounded-lg p-2">Muslim / Christian → religion channel, caste channel skip ✅</div>
            <div className="bg-gray-50 rounded-lg p-2">Caste unte → general Hindu hub skip (duplicate oddu) ✅</div>
            <div className="bg-gray-50 rounded-lg p-2">Divorcee / Handicapped / 35+ → special channels ✅</div>
            <div className="bg-gray-50 rounded-lg p-2">Govt / Software / Doctors / Teachers → job channels ✅</div>
          </div>
        </div>

        {/* Filters */}
        <div className="mt-4 bg-white rounded-[1.5rem] p-4 card-shadow">
          <input value={q} onChange={e => setQ(e.target.value)}
            placeholder="🔍 Search channel — Reddy, Muslim, NRI, 2nd marriage, doctors..."
            className="w-full p-3 rounded-xl bg-gray-50 border text-sm" />
          <div className="flex flex-wrap gap-2 mt-3">
            <button onClick={() => setTier("ALL")}
              className={`px-3 py-1.5 rounded-full text-xs font-bold border ${tier === "ALL" ? "maroon-gradient text-white" : "bg-white"}`}>
              All ({ALL_CHANNELS.length})
            </button>
            {CHANNEL_TIERS.map(t => (
              <button key={t.key} onClick={() => setTier(t.key)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold border ${tier === t.key ? "maroon-gradient text-white" : "bg-white"}`}>
                {t.icon} {t.label} ({t.count})
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2 mt-2 items-center">
            <span className="text-[11px] font-bold text-gray-500">Wave:</span>
            {[0, 1, 2, 3, 4].map(w => (
              <button key={w} onClick={() => setWave(w as number | 0)}
                className={`px-3 py-1 rounded-full text-[11px] font-bold border ${wave === w ? "bg-[#D4AF37] text-[#7A0C2E]" : "bg-white"}`}>
                {w === 0 ? "All" : `W${w}`}
              </button>
            ))}
            <label className="ml-auto flex items-center gap-2 text-[11px] font-bold">
              <input type="checkbox" checked={onlyLive} onChange={e => setOnlyLive(e.target.checked)} />
              LIVE matrame chupinchu
            </label>
          </div>
          <div className="text-[11px] text-gray-500 mt-2 flex flex-wrap items-center gap-2">
            <span>{list.length} channels kanipisthunnayi</span>
            {tier !== "ALL" && <span className="px-2 py-0.5 rounded-full bg-maroon-soft text-maroon font-bold">{tier.replace("_", " ")}</span>}
            {wave !== 0 && <span className="px-2 py-0.5 rounded-full bg-gold-soft text-maroon font-bold">Wave {wave}</span>}
            {q && <span className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 font-bold">“{q}”</span>}
            {(tier !== "ALL" || wave !== 0 || q || onlyLive) && (
              <button
                onClick={() => { setTier("ALL"); setWave(0); setQ(""); setOnlyLive(false); }}
                className="px-2 py-0.5 rounded-full border border-maroon/30 text-maroon font-bold"
              >
                ✕ filters clear
              </button>
            )}
            <span className="text-gray-400">• per channel ki bot admin + pinned post must</span>
          </div>
        </div>

        {/* Tier sections */}
        {CHANNEL_TIERS.filter(t => tier === "ALL" || tier === t.key).map(t => {
          const items = list.filter(c => c.tier === t.key);
          if (!items.length) return null;
          return (
            <div key={t.key} className="mt-4 bg-white rounded-[1.5rem] p-5 card-shadow">
              <div className="flex items-center justify-between">
                <h2 className="font-bold text-[#7A0C2E] text-sm">{t.icon} {t.label} — {items.length}</h2>
                <span className="text-[11px] text-gray-500">{t.hint}</span>
              </div>
              <div className="grid md:grid-cols-2 gap-2 mt-3">
                {items.map((c: Channel) => (
                  <div key={c.key} className={`border rounded-2xl p-3 ${c.live ? "border-green-300 bg-green-50/40" : ""}`}>
                    <div className="flex justify-between items-start gap-2">
                      <div className="min-w-0">
                        <div className="font-bold text-[13px] text-[#7A0C2E] truncate">{c.name}</div>
                        <div className="text-[11px] text-gray-500">{c.username} • {c.status}</div>
                      </div>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold whitespace-nowrap ${c.live ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
                        {c.live ? "LIVE" : `W${c.wave}`}
                      </span>
                    </div>
                    <div className="text-[11px] text-gray-600 mt-1 line-clamp-2">{c.desc}</div>
                    <div className="text-[10px] text-[#D4AF37] mt-1">{c.hashtags.join(" ")}</div>
                    <div className="flex gap-2 mt-2">
                      {c.live ? (
                        <>
                          <a href={c.link} target="_blank" rel="noreferrer"
                            className="px-3 py-1.5 maroon-gradient text-white rounded-full text-[11px] font-bold">Join</a>
                          <a href={c.deepLink} target="_blank" rel="noreferrer"
                            className="px-3 py-1.5 border border-[#7A0C2E] text-[#7A0C2E] rounded-full text-[11px] font-bold">Bot tho join</a>
                        </>
                      ) : (
                        <>
                          <span className="px-3 py-1.5 bg-gray-100 text-gray-500 rounded-full text-[11px] font-bold">Create — Wave {c.wave}</span>
                          <button
                            onClick={() => navigator.clipboard?.writeText(`${c.name}\n@${c.username}\n${c.desc}`)}
                            className="px-3 py-1.5 border rounded-full text-[11px] font-bold">Copy info</button>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}

        {list.length === 0 && (
          <div className="mt-4 bg-white rounded-[1.5rem] p-8 text-center text-sm text-gray-500">
            Ee filter ki channels levu — verovati try chey 🔍
          </div>
        )}

        {/* Creation waves */}
        <div className="mt-4 bg-[#0F1F3C] text-white rounded-[1.5rem] p-6">
          <h3 className="font-bold text-[#D4AF37]">🚀 Creation Waves — ee order lo cheyyi</h3>
          <div className="grid md:grid-cols-4 gap-3 mt-3 text-xs">
            {[
              { w: 1, t: "Day 1-3", d: "Official + TS/AP Bride&Groom + Reddy, Kamma, Kapu, Velama" },
              { w: 2, t: "Week 1-2", d: "Vysya, Brahmin, Goud, Yadav, Mala, Madiga, Lambada + Muslim, Christian, 2nd marriage, Govt" },
              { w: 3, t: "Week 3-4", d: "Migitha BC castes + Doctors, Software, 35+, Success, Alerts, Bureau" },
              { w: 4, t: "Month 2", d: "SC/ST + chinnadi castes + Other religions — 65 complete" },
            ].map(x => (
              <div key={x.w} className="bg-white/10 rounded-xl p-3">
                <div className="font-bold text-[#D4AF37]">Wave-{x.w} • {x.t}</div>
                <div className="mt-1 opacity-90">{x.d}</div>
                <div className="mt-1 text-[10px] opacity-70">{ALL_CHANNELS.filter(c => c.wave === x.w).length} channels</div>
              </div>
            ))}
          </div>
          <div className="mt-4 bg-white/10 rounded-xl p-3 text-[11px] font-mono">
            Server lo: <span className="text-[#D4AF37]">python backend/create_channels.py --wave 1</span> · check: --check · create ayyaka: --mark-live reddy
          </div>
        </div>

        {/* Footer CTA */}
        <div className="mt-4 bg-white rounded-[1.5rem] p-6 card-shadow text-center">
          <div className="font-bold text-[#7A0C2E]">Mana Vivaha — {CHANNEL_STATS.total} channels, okka platform</div>
          <div className="text-xs text-gray-500 mt-1">₹99 ke Sambandham • Modati 3 FREE • {CHANNEL_STATS.bot}</div>
          <div className="flex justify-center gap-3 mt-3">
            <Link href="/register" className="px-4 py-2 maroon-gradient text-white rounded-full text-xs font-bold">Register 3 min lo</Link>
            <Link href="/bureau" className="px-4 py-2 border border-[#D4AF37] text-[#7A0C2E] rounded-full text-xs font-bold">Bureau / Broker</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
