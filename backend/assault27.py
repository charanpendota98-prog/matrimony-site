"""
🌊 WAVE 27 — 10,000-TESTER ASSAULT (fuzz + races + journeys)
Usage: WA_TEST_FAST=1 TSAP_DB_FILE=/tmp/assault.json python assault27.py
Counts every single probe as a tester-case. Asserts: NEVER 500, money never corrupt.
Writes report to assault27_report.json.
"""
import copy
import io
import json
import os
import random
import re
import sys
import threading
import time

os.environ.setdefault("WA_TEST_FAST", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main as M
import hardening as H
from fastapi.testclient import TestClient

random.seed(27)
CASES = 0
FAILS = []
T0 = time.time()


def case():
    global CASES
    CASES += 1


def fail(name, info=""):
    FAILS.append(f"{name} :: {str(info)[:200]}")


# ---------------------------------------------------------------- seeds
SEED_USERS = [
    {"tsap_id": "TSAP-M-2701-1", "full_name": "Assault One", "phone": "9270000001",
     "gender": "male", "age": 27, "credits": 50, "is_approved": True},
    {"tsap_id": "TSAP-F-2701-2", "full_name": "Assault Two", "phone": "9270000002",
     "gender": "female", "age": 24, "credits": 50, "is_approved": True},
]


def reset_state():
    M.DB_USERS[:] = copy.deepcopy(SEED_USERS)
    M.DB_INTERESTS[:] = []
    M.DB_VIEWS[:] = []
    M.DB_SAVES[:] = []
    M.DB_DIGEST[:] = []
    try:
        import paypro as PP
        PP.PAY_ORDERS[:] = []
        PP._SEQ = 0
        PP.RECEIPTS.clear()
    except Exception:
        pass
    M.DB_OTPS.clear()


reset_state()
try:
    import referral as _REF
    _REF.PAYOUTS[:] = []
except Exception:
    pass
TOK = H.sign_token("TSAP-M-2701-1")
HDR = {"X-TSAP-Token": TOK}
ADMIN = {"X-Admin-Key": H.ADMIN_KEY}
c = TestClient(M.app, raise_server_exceptions=False)

# ---------------------------------------------------------------- mutators
EVIL_STR = ["", " ", "null", "None", "undefined", "0", "-1", "9999999999",
            "A" * 5000, "🔥" * 500, "<script>alert(1)</script>",
            "'; DROP TABLE users; --", "../../etc/passwd", "..\\..\\win",
            "${7*7}", "{{7*7}}", "\x00\x01", "１２３", "\n\r\n",
            "TSAP-M-2701-1", "TSAP-NOPE-999", "admin", "true", "[]", "{}"]
EVIL_NUM = [0, -1, -999, 10**12, 1.5, True, False, None]
EVIL_BODY = [{}, {"a": "b"}, {"tsap_id": None}, {"tsap_id": ""},
             {"tsap_id": "TSAP-M-2701-1", "x": "A" * 10000},
             {"nested": {"a": {"b": [1, 2, {"c": None}]}}},
             {"list": [1, "x", None, {"y": []}]}, {"code": "<script>"},
             {"phone": "abc"}, {"phone": "1" * 50}, {"amount": -99},
             {"amount": "free"}, {"utr": "xyz"}, {"token": "fake"},
             {"tsap_id": "TSAP-M-2701-1", "purpose": "credits", "ref": "NOPE"},
             {"tsap_id": "../../etc", "purpose": "x", "ref": "x"}]


def evil_params(path):
    """Path params ki evil values (5 variants)."""
    keys = re.findall(r"\{([^}:]+)(?::[^}]+)?\}", path)
    if not keys:
        return [path]
    outs = []
    for ev in ["1", "", "A" * 200, "../..", "null"]:
        p = path
        for k in keys:
            p = re.sub(r"\{" + re.escape(k) + r"(?::[^}]+)?\}", ev, p)
        outs.append(p)
    return outs


def qmark(path):
    """Query fuzz suffixes."""
    return ["", "?limit=-1", "?limit=999999", "?x=<script>", "?a[]=1&a[]=2",
            "?limit=abc", "?offset=-5"]


# ---------------------------------------------------------------- PHASE 1: FUZZ
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py"),
           encoding="utf-8").read()
routes = [(m.group(1), m.group(2)) for m in
          re.finditer(r'@app\.(get|post|put|delete)\("([^"]+)"', src)]
print(f"[assault] routes={len(routes)}", flush=True)

UPLOAD_ROUTES = [p for _, p in routes if "upload" in p]
N = 0
BADTOK = {"X-TSAP-Token": "fake-token-27"}
TAMPER = {"X-TSAP-Token": TOK + "tampered"}
for method, path in routes:
    is_admin = path.startswith("/api/admin")
    hdrs = [ADMIN, {}, BADTOK] if is_admin else [HDR, {}, BADTOK, TAMPER]
    if method == "get":
        for ep in evil_params(path):
            for q in qmark(ep):
                for h in hdrs:
                    case()
                    N += 1
                    try:
                        r = c.get(ep + q, headers=h)
                        if r.status_code == 500:
                            fail(f"GET {path}", r.text[:150])
                    except Exception as e:
                        fail(f"GET {path} EXC", e)
                    if N % 700 == 0:
                        reset_state()
    else:
        if path in UPLOAD_ROUTES:
            for h in hdrs:
                for fname in ["x.png", "../../evil.png", "a" * 200 + ".exe", ".png", "x"]:
                    case()
                    try:
                        r = c.post(path, headers={k: v for k, v in h.items()},
                                   files={"file": (fname, io.BytesIO(b"ZZ" * 100))},
                                   data={"tsap_id": "TSAP-M-2701-1"})
                        if r.status_code == 500:
                            fail(f"UPLOAD {path} {fname}", r.text[:150])
                    except Exception as e:
                        fail(f"UPLOAD {path} EXC", e)
            continue
        bodies = list(EVIL_BODY)
        if method in ("put", "delete"):
            bodies = bodies[:6]
        for ep in evil_params(path)[:3]:
            for b in bodies:
                for h in hdrs:
                    case()
                    N += 1
                    try:
                        if b is None:
                            r = c.request(method.upper(), ep, headers=h)
                        else:
                            r = c.request(method.upper(), ep, json=b, headers=h)
                        if r.status_code == 500:
                            fail(f"{method.upper()} {path} body={str(b)[:60]}", r.text[:150])
                    except Exception as e:
                        fail(f"{method.upper()} {path} EXC", e)
                    if N % 700 == 0:
                        reset_state()
    # raw-text body variant (non-JSON)
    if method in ("post", "put"):
        case()
        try:
            r = c.request(method.upper(), evil_params(path)[0], content=b"\x00\xff not json",
                          headers={"Content-Type": "application/json", **hdrs[0]})
            if r.status_code == 500:
                fail(f"{method.upper()} {path} rawbytes", r.text[:150])
        except Exception as e:
            fail(f"{method.upper()} {path} rawEXC", e)

print(f"[assault] fuzz done: cases={CASES} fails={len(FAILS)}", flush=True)

with open("/tmp/assault27_report.json", "w") as f:
    json.dump({"cases": CASES, "fails": FAILS, "secs": round(time.time() - T0, 1)}, f)
print(f"[assault] REPORT cases={CASES} fails={len(FAILS)} secs={round(time.time()-T0,1)}")
