"""
Mana Vivaha — Channel Creation Helper
=====================================
Usage:
  python create_channels.py            # full creation plan (waves + copy-paste info)
  python create_channels.py --wave 1   # only Wave-1 channels
  python create_channels.py --key reddy
  python create_channels.py --check    # Telegram API tho username availability / bot admin check
  python create_channels.py --mark-live <key>   # create ayyaka registry lo live=True cheyyi

--check ki BOT_TOKEN kavali (env lo leda backend/.env lo).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from channels_config import (  # noqa: E402
    CHANNELS, channel_stats, channels_by_tier, live_channels, BOT_USERNAME, SITE,
)

TIER_ORDER = ["L0_OFFICIAL", "L1_REGION", "L2_RELIGION", "L3_CASTE", "L4_SPECIAL"]
TIER_TITLE = {
    "L0_OFFICIAL": "LEVEL 0 — OFFICIAL HUB (1)",
    "L1_REGION": "LEVEL 1 — REGION FLAGSHIP (5)",
    "L2_RELIGION": "LEVEL 2 — RELIGION (5)",
    "L3_CASTE": "LEVEL 3 — HINDU CASTE-WISE (43) — ONE per caste",
    "L4_SPECIAL": "LEVEL 4 — SPECIAL (11)",
}


def print_channel(key, ch, index=None):
    mark = "✅ LIVE" if ch.get("live") else "⬜ create"
    print(f"\n  {'#' + str(index) + ' ' if index else ''}{ch['name']}   [{mark}]")
    print(f"     Username : @{ch['username']}")
    if ch.get("fallbacks"):
        print(f"     Taken?   : {', '.join('@'+f for f in ch['fallbacks'])}")
    print(f"     Link     : https://t.me/{ch['username']}")
    print(f"     Wave     : {ch['wave']}")
    print(f"     Hashtags : {' '.join(ch.get('hashtags', []))}")
    print(f"     Desc     : {ch['desc']}")


def plan(wave=None, key=None):
    stats = channel_stats()
    print("=" * 70)
    print(f"  MANA VIVAHA — CHANNEL CREATION PLAN   |   {BOT_USERNAME}")
    print("=" * 70)
    print(f"  Total: {stats['total']}   Live: {stats['live']}   To create: {stats['to_create']}")
    print(f"  Tiers: " + " | ".join(f"{t.split('_',1)[1]}={n}" for t, n in stats["by_tier"].items()))
    print("  Steps per channel: (1) Telegram → New Channel → (2) name+username+desc")
    print(f"  (3) {BOT_USERNAME} ni Admin cheyyi (Post/Edit/Delete rights) → (4) pin welcome post")
    print(f"  (5) python create_channels.py --mark-live <key>")

    for tier in TIER_ORDER:
        items = [(k, v) for k, v in CHANNELS.items() if v.get("tier") == tier]
        if wave:
            items = [(k, v) for k, v in items if v.get("wave") == wave]
        if key:
            items = [(k, v) for k, v in items if k == key]
        if not items:
            continue
        print("\n" + "─" * 70)
        print(f" {TIER_TITLE[tier]}   ({len(items)} channels)")
        print("─" * 70)
        for i, (k, v) in enumerate(items, 1):
            print_channel(k, v, i)
            print(f"     KEY      : {k}   →  --mark-live {k}")

    print("\n" + "=" * 70)
    print("  PINNED WELCOME POST (prathi channel ki idi paste chey):")
    print("=" * 70)
    print(f"""  🙏 మనవివాహం — TS-AP Telugu Matrimony ki swagatham!
  🆔 Profile ID search: {SITE}/search
  📝 3 min lo FREE register: {SITE}/register
  💰 ₹99 ke Sambandham — modati 3 numbers FREE
  🤖 Bot: {BOT_USERNAME}
  ⚠️ Advance money adigithe ventane report cheyyandi — mosam oddu!""")


def mark_live(key: str, live: bool = True):
    import pathlib
    path = pathlib.Path(__file__).with_name("channels_config.py")
    src = path.read_text()
    marker = f'"{key}": {{'
    idx = src.find(marker)
    if idx == -1:
        print(f"❌ key '{key}' registry lo ledu")
        return False
    end = src.find('"route"', idx)
    block = src[idx:end]
    if '"live": True' in block and live:
        print(f"ℹ️  {key} already LIVE")
        return True
    new_block = block.replace('"live": True', '"live": False') if not live else block.replace('"live": False', '"live": True')
    if new_block == block:
        # live field ledu (single-line dict) — add it
        new_block = block.rstrip()
    path.write_text(src[:idx] + new_block + src[end:])
    print(f"✅ {key} → live={live}  (channels_config.py updated)")
    return True


def check_telegram():
    """Telegram API tho: ee channel exist ah? Bot admin ah? (network kavali)"""
    try:
        import asyncio
        from aiogram import Bot
    except Exception as e:
        print(f"❌ aiogram ledu: {e}")
        return
    token = os.getenv("BOT_TOKEN", "")
    if not token:
        env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(env):
            for line in open(env):
                if line.startswith("BOT_TOKEN="):
                    token = line.strip().split("=", 1)[1]
    if not token:
        print("❌ BOT_TOKEN set cheyyi (env or backend/.env)")
        return

    async def run():
        bot = Bot(token=token)
        ok, missing = [], []
        for k, v in CHANNELS.items():
            try:
                chat = await bot.get_chat("@" + v["username"])
                me = await bot.get_chat_member("@" + v["username"], (await bot.get_me()).id)
                status = str(getattr(me, "status", ""))
                ok.append((k, "@" + v["username"], chat.title, chat.username, status))
            except Exception as e:
                missing.append((k, "@" + v["username"], str(e)[:70]))
        print(f"\n✅ FOUND / BOT ADMIN ({len(ok)}):")
        for k, u, title, uname, status in ok:
            print(f"   {u:34s} {title[:30]:32s} bot={status}   (key={k})")
        print(f"\n⬜ NOT CREATED YET ({len(missing)}):")
        for k, u, err in missing[:80]:
            print(f"   {u:34s} {err}")
        await bot.session.close()

    asyncio.run(run())


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args:
        check_telegram()
    elif "--mark-live" in args:
        k = args[args.index("--mark-live") + 1]
        mark_live(k, True)
    elif "--mark-not-live" in args:
        k = args[args.index("--mark-not-live") + 1]
        mark_live(k, False)
    else:
        wave = int(args[args.index("--wave") + 1]) if "--wave" in args else None
        key = args[args.index("--key") + 1] if "--key" in args else None
        plan(wave=wave, key=key)
