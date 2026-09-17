"""
📡 WAVE 15 — CHANNEL MAPPER (admin: links + bulk import + coverage)
====================================================================
User (owner) Telegram/WhatsApp channel links istharu → perfect mapping:
  • effective(): CHANNELS + admin overrides (telegram/whatsapp links, active, note)
  • set_link(): per-channel links edit (URL validate)
  • import_bulk(): paste list (`label | tg-link | wa-link`) → fuzzy match → 1-click apply
  • coverage(): tier-wise live counts + critical gaps (TS/AP × Bride/Groom, religions…)
Overrides chanmap15.json lo persist (base CHANNELS code ni touch cheyyamu).
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_FILE = os.path.join(BASE_DIR, "chanmap15.json")

OVERRIDES: Dict[str, Dict] = {}


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


def _persist() -> None:
    try:
        with open(PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump(OVERRIDES, f, ensure_ascii=False)
    except Exception:
        pass


def _restore() -> None:
    try:
        if os.path.exists(PERSIST_FILE):
            d = json.load(open(PERSIST_FILE, encoding="utf-8")) or {}
            OVERRIDES.update(d if isinstance(d, dict) else {})
    except Exception:
        pass


_restore()

_URL_OK = re.compile(r"^https?://\S+$", re.I)


def _channels():
    from channels_config import CHANNELS  # lazy (import-time weight thagginchataniki)
    return CHANNELS


def effective() -> List[Dict]:
    """అన్నీ channels + admin links merged (admin table + public links కి)."""
    out = []
    for key, c in _channels().items():
        o = OVERRIDES.get(key, {})
        tg = (o.get("telegram_link") or "").strip()
        if not tg and c.get("username"):
            tg = f"https://t.me/{c['username']}"
        out.append({"key": key, "tier": c.get("tier", ""), "name": c.get("name", key),
                    "username": c.get("username", ""), "live": bool(c.get("live", False)),
                    "route": c.get("route", ""), "desc": (c.get("desc", "") or "")[:200],
                    "telegram": tg, "whatsapp": (o.get("whatsapp_link") or "").strip(),
                    "active": o.get("active", True), "note": o.get("note", ""),
                    "customized": key in OVERRIDES})
    return out


def public_links() -> Dict[str, Dict]:
    """/channels page Join buttons కి (active + link ఉన్న vi మాత్రమే)."""
    return {e["key"]: {"telegram": e["telegram"], "whatsapp": e["whatsapp"]}
            for e in effective() if e["active"] and (e["telegram"] or e["whatsapp"])}


def set_link(key: str, telegram_link: str = "", whatsapp_link: str = "",
             active: bool = True, note: str = "") -> Dict:
    key = str(key or "").strip()
    if key not in _channels():
        return {"success": False, "message_telugu": "⚠️ Channel key దొరకలేదు"}
    tg, wa = str(telegram_link or "").strip(), str(whatsapp_link or "").strip()
    for u, label in ((tg, "Telegram"), (wa, "WhatsApp")):
        if u and not _URL_OK.match(u):
            return {"success": False, "message_telugu": f"⚠️ {label} link http(s) URL ఇవ్వండి"}
        if u and len(u) > 300:
            return {"success": False, "message_telugu": f"⚠️ {label} link too long"}
    OVERRIDES[key] = {"telegram_link": tg, "whatsapp_link": wa, "active": bool(active),
                      "note": str(note or "").strip()[:200], "updated_at": _now()}
    _persist()
    return {"success": True, "channel": next(e for e in effective() if e["key"] == key),
            "message_telugu": f"✅ {key} links save అయ్యాయి"}


def _score(label: str, entry: Dict) -> float:
    """Fuzzy match score (0–1): name + username + key tokens."""
    lab = re.sub(r"[^a-z0-9 ]", " ", str(label or "").lower())
    hay = f"{entry.get('name','')} {entry.get('username','')} {entry.get('key','')}".lower()
    hay = re.sub(r"[^a-z0-9 ]", " ", hay)
    lt = [w for w in lab.split() if len(w) > 2]
    if not lt:
        return 0.0
    hit = sum(1 for w in lt if w in hay)
    base = hit / len(lt)
    seq = SequenceMatcher(None, lab, hay).ratio()
    return 0.7 * base + 0.3 * seq


def import_bulk(text: str, auto_apply: bool = False, threshold: float = 0.45) -> Dict:
    """
    Bulk paste parse:
      Label | https://t.me/xxx | https://whatsapp.com/channel/yyy
    (pipe/comma/tab split; 2nd col tg, 3rd col wa — order auto-detect kooda)
    → matched (score>=threshold) / unmatched. auto_apply → links save.
    """
    entries = effective()
    matched, unmatched, applied = [], [], []
    lines = [l.strip() for l in str(text or "").splitlines() if l.strip() and not l.strip().startswith("#")]
    if not lines:
        return {"success": False, "message_telugu": "⚠️ Lines లేవు — `Label | tg-link | wa-link` format లో paste చెయ్యండి"}
    if len(lines) > 200:
        return {"success": False, "message_telugu": "⚠️ ఒక్క సరి 200 lines max"}
    for ln in lines[:200]:
        parts = [p.strip() for p in re.split(r"\s*\|\s*|\t", ln) if p.strip()]
        if len(parts) < 2:
            parts = [p.strip() for p in ln.split(",") if p.strip()]
        label, tg, wa = parts[0] if parts else ln, "", ""
        for p in parts[1:]:
            pl = p.lower()
            if "whatsapp" in pl or "wa.me" in pl:
                wa = wa or p
            elif "t.me" in pl or "telegram" in pl:
                tg = tg or p
            elif not tg:
                tg = p
            elif not wa:
                wa = p
        best, score = None, 0.0
        for e in entries:
            sc = _score(label, e)
            if sc > score:
                best, score = e, sc
        if best and score >= threshold and (tg or wa):
            row = {"label": label, "key": best["key"], "name": best["name"],
                   "score": round(score, 2), "telegram": tg, "whatsapp": wa}
            matched.append(row)
            if auto_apply:
                r = set_link(best["key"], tg or best["telegram"], wa or best["whatsapp"],
                             True, f"bulk import ({label[:60]})")
                if r.get("success"):
                    applied.append(best["key"])
        else:
            unmatched.append({"label": label, "telegram": tg, "whatsapp": wa,
                              "hint": f"best guess: {best['key']} ({round(score,2)})" if best else "no guess"})
    _persist()
    return {"success": True, "matched": matched, "unmatched": unmatched, "applied": applied,
            "message_telugu": f"✅ {len(matched)} match • {len(unmatched)} manual కావాలి" + (f" • {len(applied)} save" if auto_apply else "")}


CRITICAL_KEYS = ["official", "ts_bride", "ts_groom", "ap_bride", "ap_groom", "nri_global",
                 "hindu", "muslim_ts_bride", "christian_ts_bride"]


def coverage() -> Dict:
    """Tier-wise live/active + critical gaps — admin dashboard కి."""
    eff = effective()
    by_tier: Dict[str, Dict] = {}
    for e in eff:
        t = by_tier.setdefault(e["tier"] or "?", {"total": 0, "live": 0, "with_wa": 0,
                                                  "inactive": 0, "pending_keys": []})
        t["total"] += 1
        if e["live"]:
            t["live"] += 1
        if e["whatsapp"]:
            t["with_wa"] += 1
        if not e["active"]:
            t["inactive"] += 1
        elif not e["live"] and len(t["pending_keys"]) < 30:
            t["pending_keys"].append(e["key"])
    by_key = {e["key"]: e for e in eff}
    gaps = [k for k in CRITICAL_KEYS if not (by_key.get(k) or {}).get("live")]
    return {"success": True, "total": len(eff),
            "live": sum(1 for e in eff if e["live"]),
            "with_whatsapp": sum(1 for e in eff if e["whatsapp"]),
            "customized": sum(1 for e in eff if e["customized"]),
            "by_tier": by_tier, "critical_gaps": gaps,
            "message_telugu": f"📡 {len(eff)} channels • {sum(1 for e in eff if e['live'])} live" + (f" • gaps: {', '.join(gaps)}" if gaps else " • critical అన్నీ live ✅")}
