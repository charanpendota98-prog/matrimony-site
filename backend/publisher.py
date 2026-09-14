"""
Mana Vivaha — AUTO-PUBLISHER (Telegram + WhatsApp)
===================================================
Profile register avvagane / admin approve avvagane → related channels anni
chotaki automatic ga vellali. Idi aa engine.

Features:
  • Telegram: Bot API tho LIVE channels ki post (photo card unte sendPhoto)
  • WhatsApp: 2 modes —
        cloud_api → Meta WhatsApp Business Cloud API (official, opt-in numbers/broadcast)
        bridge    → local WhatsApp bridge (Baileys) — groups/newsletter ki post
  • Queue + retry (3 attempts, backoff) + per-channel rate limit (spam/429 safe)
  • Dry-run (tokens lekapothe message generate chesi log lo pettadam — crash ledu)
  • Duplicate protection (same tsap_id + channel malli post avvadu)
  • Publish log → backend/publish_log.jsonl (audit)

ENV:
  BOT_TOKEN                 — telegram bot token
  AUTO_POST_ON_REGISTER     — "true" ayithe register avvagane post (default true)
  PUBLISH_DRY_RUN           — "true" ayithe real post cheyyadu (default: tokens lekapothe auto-true)
  WHATSAPP_MODE             — off | cloud_api | bridge   (default off)
  WHATSAPP_TOKEN            — Meta Cloud API token
  WHATSAPP_PHONE_ID         — Meta Cloud API phone number id
  WHATSAPP_TO               — comma separated: 9198480xxxxx (opt-in users)
  WHATSAPP_BRIDGE_URL       — e.g. http://whatsapp-bridge:3000/send
  WHATSAPP_BRIDGE_TARGETS   — comma separated group/newsletter ids (bridge mode)
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

from channels_config import (
    CHANNELS, post_targets, build_caption, route_profile, channel_stats, SITE, BOT_USERNAME,
)

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish_log.jsonl")

# In-memory state (real lo Redis/DB)
PUBLISH_QUEUE: List[Dict] = []
PUBLISH_LOG: List[Dict] = []
_SEEN = set()          # (tsap_id, channel) duplicates block
_WORKER_TASK: Optional[asyncio.Task] = None


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def config() -> Dict:
    token = os.getenv("BOT_TOKEN", "").strip()
    wa_mode = os.getenv("WHATSAPP_MODE", "off").strip().lower()
    dry_default = not token  # token lekapothe default dry-run (crash avvakudadu)
    return {
        "bot_token": token,
        "auto_post_on_register": _env_bool("AUTO_POST_ON_REGISTER", True),
        "dry_run": _env_bool("PUBLISH_DRY_RUN", dry_default),
        "wa_mode": wa_mode if wa_mode in ("off", "cloud_api", "bridge") else "off",
        "wa_token": os.getenv("WHATSAPP_TOKEN", "").strip(),
        "wa_phone_id": os.getenv("WHATSAPP_PHONE_ID", "").strip(),
        "wa_to": [x.strip() for x in os.getenv("WHATSAPP_TO", "").split(",") if x.strip()],
        "wa_bridge_url": os.getenv("WHATSAPP_BRIDGE_URL", "").strip(),
        "wa_bridge_targets": [x.strip() for x in os.getenv("WHATSAPP_BRIDGE_TARGETS", "").split(",") if x.strip()],
        "retries": int(os.getenv("PUBLISH_RETRIES", "3")),
        "rate_limit_seconds": float(os.getenv("PUBLISH_RATE_LIMIT", "1.2")),
    }


def publish_status() -> Dict:
    c = config()
    st = channel_stats()
    return {
        "telegram": {"configured": bool(c["bot_token"]), "live_channels": st["live"]},
        "whatsapp": {
            "mode": c["wa_mode"],
            "cloud_api_ready": bool(c["wa_token"] and c["wa_phone_id"] and c["wa_to"]),
            "bridge_ready": bool(c["wa_bridge_url"] and c["wa_bridge_targets"]),
            "targets": len(c["wa_to"]) + len(c["wa_bridge_targets"]),
        },
        "dry_run": c["dry_run"],
        "auto_post_on_register": c["auto_post_on_register"],
        "queued": len(PUBLISH_QUEUE),
        "published_total": len([x for x in PUBLISH_LOG if x.get("ok")]),
        "registry": {"total": st["total"], "live": st["live"], "to_create": st["to_create"]},
    }


# ---------------------------------------------------------------------------
# MESSAGE BUILDERS
# ---------------------------------------------------------------------------
def build_whatsapp_text(profile: Dict, tsap_id: str, score: int = 92) -> str:
    """WhatsApp formatting (*bold* — Telegram ** kadu)."""
    r = route_profile(profile)
    reasons = "\n".join(f"✅ {x['telugu']}" for x in r["reasons"][:3])
    return (
        f"💍 *MANA VIVAHA* — TS-AP Telugu Matrimony\n"
        f"🆔 *{tsap_id}*  |  ⭐ *{score}% BEST MATCH*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 *{profile.get('full_name','—')}*  ({profile.get('age','—')} yrs)\n"
        f"📍 {profile.get('district','—')}, {profile.get('state','TS')}\n"
        f"💍 Caste: {profile.get('caste','—')}  |  Gothram: {profile.get('gothram','—')}\n"
        f"📏 Height: {profile.get('height','—')}  |  🩸 {profile.get('blood_group','—')}\n"
        f"🎓 {profile.get('education','—')} {profile.get('education_detail','')}\n"
        f"💼 {profile.get('job','—')} {profile.get('company','')}\n"
        f"💰 {profile.get('salary','—')}  |  📍 {profile.get('work_location','—')}\n"
        f"🌟 Star: {profile.get('star','—')}  |  Rasi: {profile.get('rasi','—')}\n"
        f"👨‍👩‍👧 {profile.get('father_name','—')} • {profile.get('family_type','—')} • {profile.get('native_place','—')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"*Enduku best match:*\n{reasons}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"{r['hashtags']}\n"
        f"🔍 Profile chudandi: {SITE}/search/{tsap_id}\n"
        f"📝 FREE register (3 min): {SITE}/register\n"
        f"🤖 Bot: {BOT_USERNAME}  •  ⚠️ Advance money adigithe report cheyyandi"
    )


def build_share_text(profile: Dict, tsap_id: str) -> str:
    """Profile owner WhatsApp/status lo share cheyyadaniki short text."""
    return (
        f"💍 Mana Vivaha — {profile.get('full_name','—')} ({profile.get('age','—')}y, "
        f"{profile.get('caste','—')}, {profile.get('district','—')})\n"
        f"🆔 {tsap_id} | {profile.get('education','')} {profile.get('job','')}\n"
        f"🔍 Chudandi: {SITE}/search/{tsap_id}\n"
        f"📝 Mee profile FREE: {SITE}/register"
    )


# ---------------------------------------------------------------------------
# LOW-LEVEL SENDERS
# ---------------------------------------------------------------------------
async def _send_telegram(chat: str, caption: str, photo_path: Optional[str], cfg: Dict) -> Dict:
    """Bot API sendPhoto/sendMessage — retry + rate-limit tho."""
    if cfg["dry_run"] or not cfg["bot_token"] or httpx is None:
        return {"ok": True, "dry_run": True, "detail": f"would post to {chat}"}
    url_base = f"https://api.telegram.org/bot{cfg['bot_token']}"
    last_err = ""
    for attempt in range(1, cfg["retries"] + 1):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                if photo_path and os.path.exists(photo_path):
                    with open(photo_path, "rb") as f:
                        resp = await client.post(
                            f"{url_base}/sendPhoto",
                            data={"chat_id": chat, "caption": caption[:1024], "parse_mode": "HTML"},
                            files={"photo": f},
                        )
                else:
                    resp = await client.post(
                        f"{url_base}/sendMessage",
                        data={"chat_id": chat, "text": caption[:4096], "disable_web_page_preview": True},
                    )
            data = resp.json()
            if data.get("ok"):
                return {"ok": True, "message_id": data["result"].get("message_id")}
            last_err = str(data)[:200]
            # 429 → retry_after wait
            retry_after = (data.get("parameters") or {}).get("retry_after")
            if retry_after:
                await asyncio.sleep(float(retry_after) + 1)
                continue
        except Exception as e:  # network / timeout
            last_err = f"{type(e).__name__}: {e}"[:200]
        await asyncio.sleep(1.5 * attempt)
    return {"ok": False, "error": last_err}


async def _send_whatsapp_cloud(text: str, cfg: Dict) -> List[Dict]:
    """Meta WhatsApp Business Cloud API — opt-in numbers ki (broadcast)."""
    results = []
    if cfg["dry_run"] or not (cfg["wa_token"] and cfg["wa_phone_id"]) or httpx is None:
        return [{"ok": True, "dry_run": True, "target": t} for t in cfg["wa_to"]] or \
               [{"ok": True, "dry_run": True, "target": "cloud_api (no numbers)"}]
    url = f"https://graph.facebook.com/v20.0/{cfg['wa_phone_id']}/messages"
    headers = {"Authorization": f"Bearer {cfg['wa_token']}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        for to in cfg["wa_to"]:
            payload = {"messaging_product": "whatsapp", "to": to,
                       "type": "text", "text": {"preview_url": True, "body": text[:4096]}}
            try:
                resp = await client.post(url, headers=headers, json=payload)
                results.append({"ok": resp.status_code < 300, "target": to, "status": resp.status_code})
            except Exception as e:
                results.append({"ok": False, "target": to, "error": str(e)[:150]})
            await asyncio.sleep(cfg["rate_limit_seconds"] / 2)
    return results


async def _send_whatsapp_bridge(text: str, cfg: Dict) -> List[Dict]:
    """Local bridge (Baileys) — WhatsApp groups/newsletter ki post."""
    results = []
    if cfg["dry_run"] or not cfg["wa_bridge_url"] or httpx is None:
        return [{"ok": True, "dry_run": True, "target": t} for t in cfg["wa_bridge_targets"]] or \
               [{"ok": True, "dry_run": True, "target": "bridge (no targets)"}]
    async with httpx.AsyncClient(timeout=45) as client:
        for target in cfg["wa_bridge_targets"]:
            try:
                resp = await client.post(cfg["wa_bridge_url"],
                                         json={"target": target, "text": text})
                results.append({"ok": resp.status_code < 300, "target": target, "status": resp.status_code})
            except Exception as e:
                results.append({"ok": False, "target": target, "error": str(e)[:150]})
            await asyncio.sleep(cfg["rate_limit_seconds"])
    return results


# ---------------------------------------------------------------------------
# MAIN PUBLISH
# ---------------------------------------------------------------------------
async def publish_profile(profile: Dict, tsap_id: str, score: int = 92,
                          photo_path: Optional[str] = None) -> Dict:
    """
    One profile → Telegram LIVE channels + WhatsApp (mode batti).
    Returns detailed per-channel result.
    """
    cfg = config()
    targets = post_targets(profile)
    caption = build_caption(profile, tsap_id, score)
    wa_text = build_whatsapp_text(profile, tsap_id, score)

    tg_results = []
    for chat in targets["ready"]:
        key = (tsap_id, chat)
        if key in _SEEN:
            tg_results.append({"channel": chat, "ok": True, "skipped": "duplicate"})
            continue
        res = await _send_telegram(chat, caption, photo_path, cfg)
        res["channel"] = chat
        tg_results.append(res)
        if res.get("ok") and not res.get("dry_run"):
            _SEEN.add(key)
        await asyncio.sleep(cfg["rate_limit_seconds"])

    wa_results = []
    if cfg["wa_mode"] == "cloud_api":
        wa_results = await _send_whatsapp_cloud(wa_text, cfg)
    elif cfg["wa_mode"] == "bridge":
        wa_results = await _send_whatsapp_bridge(wa_text, cfg)

    entry = {
        "tsap_id": tsap_id,
        "name": profile.get("full_name", ""),
        "score": score,
        "at": datetime.utcnow().isoformat(),
        "telegram": tg_results,
        "whatsapp": {"mode": cfg["wa_mode"], "results": wa_results},
        "pending_channels": targets["pending"],
        "hashtags": targets["hashtags"],
        "ok": all(x.get("ok") for x in tg_results) if tg_results else False,
        "dry_run": cfg["dry_run"],
    }
    PUBLISH_LOG.append(entry)
    _append_log_file(entry)
    return entry


def _append_log_file(entry: Dict):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_log(limit: int = 50) -> List[Dict]:
    if not os.path.exists(LOG_FILE):
        return PUBLISH_LOG[-limit:]
    try:
        lines = open(LOG_FILE, encoding="utf-8").read().strip().split("\n")
        return [json.loads(x) for x in lines[-limit:] if x.strip()]
    except Exception:
        return PUBLISH_LOG[-limit:]


# ---------------------------------------------------------------------------
# QUEUE (register endpoint block avvakunda background lo post)
# ---------------------------------------------------------------------------
def enqueue(profile: Dict, tsap_id: str, score: int = 92, photo_path: Optional[str] = None) -> Dict:
    job = {"profile": profile, "tsap_id": tsap_id, "score": score,
           "photo_path": photo_path, "queued_at": datetime.utcnow().isoformat()}
    PUBLISH_QUEUE.append(job)
    return {"queued": True, "position": len(PUBLISH_QUEUE), "tsap_id": tsap_id,
            "targets": post_targets(profile)["ready"]}


async def _worker_loop(interval: float = 2.0):
    while True:
        if PUBLISH_QUEUE:
            job = PUBLISH_QUEUE.pop(0)
            try:
                await publish_profile(job["profile"], job["tsap_id"], job["score"], job["photo_path"])
            except Exception as e:
                _append_log_file({"tsap_id": job["tsap_id"], "ok": False, "error": str(e)[:200],
                                  "at": datetime.utcnow().isoformat()})
        await asyncio.sleep(interval)


def start_worker() -> bool:
    """FastAPI startup lo call chey — background queue worker start avutundi."""
    global _WORKER_TASK
    try:
        loop = asyncio.get_event_loop()
        if _WORKER_TASK is None or _WORKER_TASK.done():
            _WORKER_TASK = loop.create_task(_worker_loop())
            return True
    except Exception:
        pass
    return False


def worker_running() -> bool:
    return _WORKER_TASK is not None and not _WORKER_TASK.done()


# ---------------------------------------------------------------------------
# TEST CLI — python publisher.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo = {"full_name": "Lakshmi Reddy", "gender": "Bride", "state": "TS", "caste": "Reddy",
            "age": 24, "height": "5'4\"", "blood_group": "O+", "education": "BTech",
            "education_detail": "CSE", "job": "Software Engineer", "company": "TCS",
            "salary": "8L", "work_location": "Hyderabad", "district": "Nalgonda",
            "gothram": "Bharadwaj", "star": "Rohini", "rasi": "Vrishabha",
            "father_name": "Ramesh Reddy", "family_type": "Nuclear", "native_place": "Miryalaguda"}

    async def _main():
        print("STATUS:", json.dumps(publish_status(), indent=2))
        print("\n--- TELEGRAM CAPTION ---")
        print(build_caption(demo, "TSAP-F-2025-5775", 92))
        print("\n--- WHATSAPP TEXT ---")
        print(build_whatsapp_text(demo, "TSAP-F-2025-5775", 92))
        print("\n--- PUBLISH (dry-run) ---")
        print(json.dumps(await publish_profile(demo, "TSAP-F-2025-5775", 92), indent=2, ensure_ascii=False))

    asyncio.run(_main())
