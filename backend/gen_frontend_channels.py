"""
Registry → frontend/src/lib/channels.ts  (auto-generate, no drift)
Run: python gen_frontend_channels.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from channels_config import CHANNELS, channel_stats  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "frontend", "src", "lib", "channels.ts")

TIER_LABEL = {
    "L0_OFFICIAL": ("Official Hub", "📢", "Top-3 daily, success stories, safety alerts"),
    "L1_REGION": ("Main 4 Channels", "📍", "TS Bride • TS Groom • AP Bride • AP Groom (+ NRI)"),
    "L2_RELIGION": ("Religion", "🕊️", "Hindu, Muslim, Christian, Other, Inter-faith"),
    "L3_CASTE": ("Caste-wise", "💍", "Caste prakaram — top 18 castes ki bride/groom separate, migilina 25 castes ki mixed"),
    "L4_SPECIAL": ("Special", "⭐", "2nd marriage, able, govt, IT, doctors, 35+, bureau"),
}
TIER_ORDER = ["L0_OFFICIAL", "L1_REGION", "L2_RELIGION", "L3_CASTE", "L4_SPECIAL"]


def main():
    rows = []
    for key, ch in CHANNELS.items():
        rows.append({
            "key": key,
            "tier": ch["tier"],
            "name": ch["name"],
            "username": "@" + ch["username"],
            "link": f"https://t.me/{ch['username']}",
            "deepLink": f"https://t.me/telugumatrimony1_bot?start=ch_{ch['username'].lower()}",
            "desc": " ".join(ch["desc"].split()),
            "hashtags": ch.get("hashtags", []),
            "wave": ch.get("wave", 4),
            "live": bool(ch.get("live")),
            "status": "LIVE ✅ Bot Admin" if ch.get("live") else f"Wave-{ch.get('wave')}",
            "fallbacks": ch.get("fallbacks", []),
        })
    # Register form dropdown — 43 caste channels + religion options + Open
    caste_options = [c.get("route", {}).get("caste") for c in CHANNELS.values()
                     if c["tier"] == "L3_CASTE" and isinstance(c.get("route"), dict)]
    caste_options = [c for c in caste_options if c]
    caste_options = list(dict.fromkeys(caste_options)) + ["Muslim", "Christian", "Open"]

    tiers = [{"key": t, "label": TIER_LABEL[t][0], "icon": TIER_LABEL[t][1],
              "hint": TIER_LABEL[t][2],
              "count": sum(1 for r in rows if r["tier"] == t)} for t in TIER_ORDER]
    stats = channel_stats()

    ts = "// AUTO-GENERATED from backend/channels_config.py — edit registry, run gen_frontend_channels.py\n"
    ts += "// Mana Vivaha | TSAP Matrimony — MASTER CHANNEL REGISTRY\n\n"
    ts += "export type Channel = {\n  key: string;\n  tier: string;\n  name: string;\n  username: string;\n"
    ts += "  link: string;\n  deepLink: string;\n  desc: string;\n  hashtags: string[];\n"
    ts += "  wave: number;\n  live: boolean;\n  status: string;\n  fallbacks: string[];\n};\n\n"
    ts += f"export const CHANNEL_STATS = {json.dumps(stats, ensure_ascii=False)} as const;\n\n"
    ts += f"export const CHANNEL_TIERS = {json.dumps(tiers, ensure_ascii=False, indent=2)} as const;\n\n"
    ts += "export const ALL_CHANNELS: Channel[] = " + json.dumps(rows, ensure_ascii=False, indent=2) + ";\n\n"
    ts += "// Register form dropdown — registry nunchi (43 castes + Muslim/Christian/Open)\n"
    ts += "export const CASTE_OPTIONS: string[] = " + json.dumps(caste_options, ensure_ascii=False, indent=2) + ";\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(ts)
    print(f"✅ wrote {os.path.relpath(OUT)} — {len(rows)} channels, {len(tiers)} tiers, stats={stats}")


if __name__ == "__main__":
    main()
