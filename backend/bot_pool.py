"""
MANA VIVAHA — TELEGRAM BOT POOL + FAILOVER 🤖
=============================================
"Okati fail aina inkokati pampali" — anduke **bot pool**:

  BOT_TOKEN           → PRIMARY  (users bot + channel posting)
  BOT_TOKEN_BACKUP    → BACKUP   (channels lo admin undali — primary fail/rate-limit aithe idi post chestundi)
  BOT_TOKEN_ALERT     → ALERT    (admin alerts, namaste, follow-up — user bot rate limit valla aagakudadu)

Pani ela chestundi:
  1. `post()` → healthy bots ni order lo try chestundi (primary → backup → alert)
  2. Error classify chestundi:
       • 401 / unauthorized        → bot token **dead** (1h cooldown, inka try cheyyadu)
       • 429 / too many requests   → **rate_limited** (retry_after cooldown → pakka bot post chestundi)
       • 403 bot not a member /
         not enough rights /
         chat not found            → **channel problem** (bot cooldown ledu — channel lo admin cheyyali)
       • timeout / network          → **transient** (30s cooldown)
  3. Okka bot post chesina chalu → `ok` + `bot` (e bot vellindo log lo untundi)
  4. Antha fail aithe → caller ki `ok: False` + attempts list (publisher queue lo retry + alert)

ENV:
  BOT_TOKEN, BOT_TOKEN_BACKUP (leka BOT_TOKEN_2), BOT_TOKEN_ALERT
  BOT_POOL_JSON   — advanced: [{"name":"b1","token":"...","roles":["post","user"]}, ...]
  PUBLISH_DRY_RUN — "true" ayithe API call cheyyadu (message preview matrame)

Telegram limits (design lo respect chestham): okka channel ki ~20 messages/minute,
bot mottham ~30 messages/second. Pool valla rate-limit ayithe pakka bot ki maruthundi.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Dict, List, Optional

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

DEFAULT_COOLDOWNS = {"dead": 3600, "rate_limited": 30, "transient": 30, "error": 60, "channel": 0}


# --------------------------------------------------------------------------- specs
class BotSpec:
    def __init__(self, name: str, token: str, roles: Optional[List[str]] = None):
        self.name = name
        self.token = token or ""
        self.roles = list(roles or ["post"])
        # health
        self.status = "ok" if self.token else "no_token"
        self.failures = 0
        self.sent = 0
        self.fail_count = 0
        self.last_error = ""
        self.last_used = ""
        self.cooldown_until = 0.0

    @property
    def configured(self) -> bool:
        return bool(self.token)

    def available(self, now: float) -> bool:
        return self.configured and now >= self.cooldown_until and self.status not in ("dead",)

    def as_dict(self, now: Optional[float] = None) -> Dict:
        now = now or time.time()
        return {"name": self.name, "roles": self.roles, "configured": self.configured,
                "status": self.status, "sent": self.sent, "failures": self.fail_count,
                "last_error": self.last_error, "last_used": self.last_used,
                "cooldown_s": max(0, int(self.cooldown_until - now))
                if self.cooldown_until > now else 0,
                "available": self.available(now)}


def _bot_from_env() -> List[BotSpec]:
    """Env nunchi bot pool (JSON leda simple tokens)."""
    raw = os.getenv("BOT_POOL_JSON", "").strip()
    if raw:
        try:
            data = json.loads(raw)
            bots = [BotSpec(d.get("name", "bot%d" % i), d.get("token", ""), d.get("roles"))
                    for i, d in enumerate(data)]
            if bots:
                return bots
        except Exception:
            pass
    primary = os.getenv("BOT_TOKEN", "").strip()
    backup = (os.getenv("BOT_TOKEN_BACKUP") or os.getenv("BOT_TOKEN_2") or "").strip()
    alert = (os.getenv("BOT_TOKEN_ALERT") or os.getenv("BOT_TOKEN_3") or "").strip()
    bots = [BotSpec("primary", primary, ["post", "user", "alert"])]
    if backup and backup != primary:
        bots.append(BotSpec("backup", backup, ["post", "alert"]))
    if alert and alert not in (primary, backup):
        bots.append(BotSpec("alert", alert, ["alert", "post"]))
    return bots


# --------------------------------------------------------------------------- pool
class BotPool:
    def __init__(self, bots: Optional[List[BotSpec]] = None, sender=None, clock=None):
        self.bots = bots if bots is not None else _bot_from_env()
        self._sender = sender          # injectable: sender(bot, chat_id, text, photo_path, parse_mode)
        self._clock = clock or time.time

    # ---- health
    def order(self, role: str = "post") -> List[BotSpec]:
        now = self._clock()
        pool = [b for b in self.bots if role in b.roles]
        if not pool:
            pool = list(self.bots)
        # 🎯 ee role ki **dedicated** bot mundu (alert bot alerts ki, post bot post ki) → rate limits tagguthayi
        return sorted(pool, key=lambda b: (b.roles[0] != role, not b.available(now), b.sent))

    def health(self) -> Dict:
        now = self._clock()
        return {"bots": [b.as_dict(now) for b in self.bots],
                "configured": len([b for b in self.bots if b.configured]),
                "available": len([b for b in self.bots if b.available(now)]),
                "post_order": [b.name for b in self.order("post")],
                "alert_order": [b.name for b in self.order("alert")],
                "failover": "primary → backup → alert (okati fail aithe pakkadi ventane try avutundi)",
                "recommended": "3 bots: primary (users+post) • backup (post) • alert (admin notifications)"}

    # ---- failure bookkeeping
    def note_success(self, bot: BotSpec) -> None:
        bot.sent += 1
        bot.status = "ok"
        bot.last_error = ""
        bot.cooldown_until = 0.0
        bot.last_used = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self._clock()))

    def note_failure(self, bot: BotSpec, kind: str, error: str = "", retry_after: float = 0) -> None:
        bot.fail_count += 1
        bot.failures += 1
        bot.last_error = (error or kind)[:180]
        cool = float(retry_after or DEFAULT_COOLDOWNS.get(kind, 30))
        if kind == "dead":
            bot.status = "dead"
        elif kind == "channel":
            bot.status = "channel_problem"        # bot lo tappu ledu — channel permission
            return                                 # cooldown ledu (pakka bot kooda try avutundi)
        else:
            bot.status = kind
        if cool > 0:
            bot.cooldown_until = self._clock() + cool

    @staticmethod
    def classify(result: Dict) -> tuple:
        """{'ok':False,'error_code':..,'description':..,'retry_after':..} → (kind, retry_after)"""
        code = result.get("error_code") or result.get("status")
        desc = str(result.get("description") or result.get("error") or "").lower()
        retry = float(result.get("retry_after") or 0)
        if code == 401 or "unauthorized" in desc:
            return "dead", 3600
        if code == 429 or "too many requests" in desc or "flood" in desc:
            return "rate_limited", retry or 30
        if any(x in desc for x in ("not enough rights", "bot is not a member", "chat not found",
                                   "chat_admin_required", "not a member of", "not enough permissions",
                                   "bot was kicked", "no rights to send")):
            return "channel", 0
        if result.get("network_error"):
            return "transient", 30
        if code and int(code) >= 500:
            return "transient", 30
        return "error", 60

    # ---- sending
    async def _send_via_api(self, bot: BotSpec, chat_id: str, text: str,
                            photo_path: Optional[str], parse_mode: Optional[str]) -> Dict:
        if httpx is None:
            return {"ok": False, "network_error": True, "description": "httpx install ledu"}
        base = "https://api.telegram.org/bot%s" % bot.token
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                if photo_path and os.path.exists(photo_path):
                    with open(photo_path, "rb") as f:
                        resp = await client.post("%s/sendPhoto" % base,
                                                 data={"chat_id": chat_id, "caption": text[:1024],
                                                       **({"parse_mode": parse_mode} if parse_mode else {})},
                                                 files={"photo": f})
                else:
                    resp = await client.post("%s/sendMessage" % base,
                                             data={"chat_id": chat_id, "text": text[:4096],
                                                   "disable_web_page_preview": True,
                                                   **({"parse_mode": parse_mode} if parse_mode else {})})
            data = resp.json()
        except Exception as e:
            return {"ok": False, "network_error": True, "description": "%s: %s" % (type(e).__name__, e)}
        if data.get("ok"):
            return {"ok": True, "message_id": (data.get("result") or {}).get("message_id")}
        params = data.get("parameters") or {}
        return {"ok": False, "error_code": data.get("error_code"), "description": data.get("description", ""),
                "retry_after": params.get("retry_after", 0)}

    async def post(self, chat_id: str, text: str, photo_path: Optional[str] = None,
                   role: str = "post", parse_mode: Optional[str] = None,
                   dry_run: bool = False, max_bots: int = 3) -> Dict:
        """Pool lo healthy bots try chesi post cheyyi. Returns {ok, bot, attempts, ...}."""
        sender = self._sender or self._send_via_api
        attempts: List[Dict] = []
        candidates = [b for b in self.order(role) if b.configured][:max_bots]
        if not candidates:
            return {"ok": False, "bot": "", "attempts": attempts,
                    "error": "BOT_TOKEN(s) set cheyyaledu", "hint": "env lo BOT_TOKEN + BOT_TOKEN_BACKUP pettu"}
        if dry_run:
            b = candidates[0]
            return {"ok": True, "dry_run": True, "bot": b.name, "detail": "would post to %s" % chat_id,
                    "attempts": [{"bot": b.name, "ok": True, "dry_run": True}]}
        for bot in candidates:
            try:
                if self._sender is None:
                    res = await sender(bot, chat_id, text, photo_path, parse_mode)
                else:
                    res = sender(bot, chat_id, text, photo_path, parse_mode)
                    if asyncio.iscoroutine(res):
                        res = await res
            except Exception as e:
                res = {"ok": False, "description": "%s: %s" % (type(e).__name__, e), "network_error": True}
            if res.get("ok"):
                self.note_success(bot)
                return {"ok": True, "bot": bot.name, "message_id": res.get("message_id"),
                        "attempts": attempts + [{"bot": bot.name, "ok": True}],
                        "fallback_used": bool(attempts)}
            kind, retry = self.classify(res)
            self.note_failure(bot, kind, res.get("description") or res.get("error", ""), retry)
            attempts.append({"bot": bot.name, "ok": False, "kind": kind,
                             "error": (res.get("description") or res.get("error") or "")[:160],
                             "cooldown_s": int(retry)})
        return {"ok": False, "bot": "", "attempts": attempts, "error": "anni bots fail ayyayi",
                "hint": "primary/backup bots ni channels lo admin cheyyandi + tokens check cheyyandi"}

    async def send_alert(self, text: str, chat_id: str = "", parse_mode: Optional[str] = None) -> Dict:
        """Admin alert (namaste/interest/monitor) — alert bot mundu, tarvata primary."""
        target = chat_id or os.getenv("ADMIN_CHAT_ID", "") or os.getenv("ADMIN_WHATSAPP_NUMBER", "")
        if not target:
            return {"ok": False, "error": "ADMIN_CHAT_ID ledu"}
        return await self.post(target, text, role="alert", parse_mode=parse_mode)


_POOL: Optional[BotPool] = None
_POOL_ENV_SIG = None


def get_pool(force_reload: bool = False) -> BotPool:
    """Singleton pool — env tokens marchithe auto reload."""
    global _POOL, _POOL_ENV_SIG
    sig = (os.getenv("BOT_TOKEN", ""), os.getenv("BOT_TOKEN_BACKUP", ""), os.getenv("BOT_TOKEN_2", ""),
           os.getenv("BOT_TOKEN_ALERT", ""), os.getenv("BOT_POOL_JSON", ""))
    if force_reload or _POOL is None or sig != _POOL_ENV_SIG:
        _POOL = BotPool()
        _POOL_ENV_SIG = sig
    return _POOL


def bot_health() -> Dict:
    return get_pool().health()
