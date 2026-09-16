"""
💾 WAVE 22 — CORE DB PERSISTENCE (atomic JSON)
================================================
Mundu DB_USERS/DB_INTERESTS/DB_PAYMENTS anni pure in-memory — server restart
aithe REGISTER ayina users + payments + interests ANNI Poyevvi (data loss!).
Ippudu: prathi mutation tarvata (debounced) atomic save + startup lo auto-load.
(Postgres vachhe varaku idi production-safe — tmp+rename, corrupt-proof.)
"""
import json
import os
import time

DB_FILE = os.getenv("TSAP_DB_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_db.json")
_last_save = 0.0
SAVE_DEBOUNCE_S = 5.0


def load() -> dict:
    """Startup load — file lekapoina/corrupt aina khali DB (crash avvadu)."""
    try:
        if not os.path.exists(DB_FILE):
            return {}
        with open(DB_FILE, encoding="utf-8") as f:
            d = json.load(f) or {}
        return d if isinstance(d, dict) else {}
    except Exception as e:
        print(f"[DB] load skip ({str(e)[:80]}) — fresh start")
        return {}


def save(payload: dict, force: bool = False) -> bool:
    """Atomic save (tmp + rename) — half-write/corrupt avvadhu."""
    global _last_save
    now = time.time()
    if not force and (now - _last_save) < SAVE_DEBOUNCE_S:
        return False
    _last_save = now
    try:
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        os.replace(tmp, DB_FILE)
        return True
    except Exception as e:
        print(f"[DB] save fail: {str(e)[:100]}")
        return False


def snapshot(users, interests, payments, otps, verified_phones, views, saves, digest) -> dict:
    return {
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "users": users or [],
        "interests": interests or [],
        "payments": payments or [],
        "otps": otps or {},
        "verified_phones": sorted(verified_phones or []),
        "views": views or [],
        "saves": saves or [],
        "digest": digest or [],
    }
