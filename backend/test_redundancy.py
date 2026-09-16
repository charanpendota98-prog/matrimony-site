"""
MANA VIVAHA — BOT + WHATSAPP FAILOVER TEST SUITE 🔁
===================================================
Run:  /tmp/venv/bin/python test_redundancy.py   (backend/ cwd nunchi)

Rule: **"okati fail aina inkokati pampali"** — ee suite adi proof chestundi.

Cover:
  • Bot pool: primary → backup → alert order, 429 rate-limit failover, 401 dead token,
    channel-permission error (bot cooldown ledu), anni fail → caller ki attempts list
  • WA pool: instance failover (duplicate ledu), per-instance daily caps, auth/down cooldowns,
    load balancing (least-sent), lane routing (requests lane), dead-letter + requeue
  • Publisher: bot pool tho telegram post, WA pool tho deliver, worker retry (3) + alert
  • API: /api/system/health, /api/bots/health, /api/wa/dead(+requeue), /api/wa/status instances
"""
import asyncio
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bot_pool  # noqa: E402
import wa_pool  # noqa: E402
import publisher  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✅ " if cond else "  ❌ ") + name + (("  | " + str(extra)) if extra else ""))


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def B(name, token="tok-" + "x" * 20, roles=None):
    return bot_pool.BotSpec(name, token, roles or ["post", "alert"])


def I(name, url="", lane="both", cap=60):
    return wa_pool.WAInstance(name, url or ("http://%s:3000" % name), lane, cap)


print("=== 1. BOT POOL — FAILOVER ORDER ===")
bots = [B("primary"), B("backup"), B("alert", roles=["alert"])]
pool = bot_pool.BotPool(bots)
check("post order = primary → backup (alert lekunda)", [b.name for b in pool.order("post")] == ["primary", "backup"],
      [b.name for b in pool.order("post")])
check("alert order = alert mundu", pool.order("alert")[0].name == "alert")
h = pool.health()
check("health lo failover + recommended", "failover" in h and "3 bots" in h["recommended"])
check("3 bots configured", h["configured"] == 3 and h["available"] == 3)

print("=== 2. BOT POOL — PRIMARY FAIL → BACKUP POST CHESTUNDI ===")
calls = []


async def sender_primary_down(bot, chat_id, text, photo_path, parse_mode):
    calls.append(bot.name)
    if bot.name == "primary":
        return {"ok": False, "error_code": 429, "description": "Too Many Requests: retry after 25",
                "retry_after": 25}
    return {"ok": True, "message_id": 777}


p2 = bot_pool.BotPool([B("primary"), B("backup")], sender=sender_primary_down)
res = run(p2.post("@TSBRIDE", "test caption"))
check("backup tho post ayyindi", res["ok"] and res["bot"] == "backup", res)
check("fallback_used = True", res["fallback_used"] is True)
check("rendu bots try ayyayi (order lo)", calls == ["primary", "backup"], calls)
check("primary 429 cooldown lo", p2.bots[0].status == "rate_limited" and p2.bots[0].cooldown_until > 0,
      p2.bots[0].status)
check("backup healthy ga undi (sent +1)", p2.bots[1].sent == 1 and p2.bots[1].status == "ok")
check("attempts log lo primary fail reason", res["attempts"][0]["kind"] == "rate_limited"
      and res["attempts"][0]["cooldown_s"] == 25, res["attempts"])

print("=== 3. BOT POOL — DEAD TOKEN / CHANNEL ERROR CLASSIFICATION ===")
check("401 → dead + 1h cooldown", bot_pool.BotPool.classify({"error_code": 401}) == ("dead", 3600))
check("403 'not enough rights' → channel problem (cooldown ledu)",
      bot_pool.BotPool.classify({"error_code": 403, "description": "Bad Request: not enough rights"}) == ("channel", 0))
check("'chat not found' → channel problem",
      bot_pool.BotPool.classify({"description": "Bad Request: chat not found"})[0] == "channel")
check("timeout → transient 30s", bot_pool.BotPool.classify({"network_error": True}) == ("transient", 30))

# channel problem unte bot healthy ga ne untundi (channel lo admin cheyyali — bot tappu kaadu)
async def sender_channel_problem(bot, chat_id, text, photo_path, parse_mode):
    if bot.name == "primary":
        return {"ok": False, "error_code": 403, "description": "Bad Request: not enough rights to send"}
    return {"ok": True, "message_id": 1}


p3 = bot_pool.BotPool([B("primary"), B("backup")], sender=sender_channel_problem)
res3 = run(p3.post("@c_reddy_bride", "x"))
check("channel problem tho kooda backup post chesindi", res3["ok"] and res3["bot"] == "backup")
check("primary cooldown ledu (channel issue)", p3.bots[0].cooldown_until == 0 and p3.bots[0].status == "channel_problem",
      p3.bots[0].status)

print("=== 4. BOT POOL — ANNI FAIL → CALLER KI ATTEMPTS (retry ki) ===")
async def sender_all_fail(bot, chat_id, text, photo_path, parse_mode):
    return {"ok": False, "network_error": True, "description": "ConnectTimeout"}


p4 = bot_pool.BotPool([B("primary"), B("backup")], sender=sender_all_fail)
res4 = run(p4.post("@TSBRIDE", "x"))
check("anni fail → ok False + attempts 2", (not res4["ok"]) and len(res4["attempts"]) == 2, res4["attempts"])
check("hint lo em cheyyalo undi", "admin" in res4["hint"].lower())
check("rendu bots transient cooldown", all(b.status == "transient" for b in p4.bots))

print("=== 5. BOT POOL — DRY RUN + NO TOKEN ===")
pd = bot_pool.BotPool([B("primary")], sender=sender_all_fail)
rd = run(pd.post("@TSBRIDE", "x", dry_run=True))
check("dry_run lo API call ledu + ok True", rd["ok"] and rd["dry_run"] and rd["bot"] == "primary")
pz = bot_pool.BotPool([bot_pool.BotSpec("primary", "")])
rz = run(pz.post("@TSBRIDE", "x"))
check("token ledu → clear Telugu hint", (not rz["ok"]) and "BOT_TOKEN" in rz["hint"], rz["error"])

print("=== 6. WA POOL — INSTANCE FAILOVER ===")
tmp = tempfile.mkdtemp()
try:
    state = os.path.join(tmp, "wa_state.json")
    insts = [I("wa1"), I("wa2"), I("wa3", lane="requests")]
    wp = wa_pool.WAPool(insts, state_file=state)
    sent_to = []

    def deliverer(inst, item):
        sent_to.append(inst.name)
        if inst.name == "wa1":
            return {"ok": False, "status": 500, "error": "bridge down"}
        return {"ok": True, "target": item["target"], "with_image": True}

    item = {"target": "@reddy_group", "text": "hello", "priority": 1, "kind": "channel_post"}
    r = run(wp.deliver(item, lane="post", deliverer=deliverer))
    check("wa1 fail → wa2 tho pampindi", r["ok"] and r["instance"] == "wa2", r.get("instance"))
    check("fallback_used flag", r["fallback_used"] is True)
    check("duplicate ledu (okate instance success)", sent_to.count("wa2") == 1, sent_to)
    check("wa1 cooldown lo (down)", wp.instances[0].status == "down" and wp.instances[0].cooldown_until > 0)
    check("wa2 sent_today +1", wp.instances[1].sent_today == 1)

    # anni down → attempts list (worker retry ki)
    def all_down(inst, item):
        return {"ok": False, "status": 502, "error": "bad gateway"}

    wp2 = wa_pool.WAPool([I("wa1"), I("wa2")], state_file=os.path.join(tmp, "s2.json"))
    r2 = run(wp2.deliver(item, lane="post", deliverer=all_down))
    check("anni instances fail → ok False + attempts 2", (not r2["ok"]) and len(r2["attempts"]) == 2, r2.get("attempts"))
    check("hint lo bridge QR check cheyyamani", "QR" in r2["hint"] or "bridge" in r2["hint"].lower())

    print("=== 7. WA POOL — LANE + LOAD BALANCE + CAPS ===")
    wp3 = wa_pool.WAPool([I("wa1"), I("wa2"), I("wa3", lane="requests")], state_file=os.path.join(tmp, "s3.json"))
    check("post lane lo wa3 (requests-only) ledu", [i.name for i in wp3.order("post")] == ["wa1", "wa2"],
          [i.name for i in wp3.order("post")])
    check("requests lane lo wa3 mundu", wp3.order("requests")[0].name == "wa3", [i.name for i in wp3.order("requests")])
    wp3.instances[0].sent_today = 10
    wp3.instances[1].sent_today = 3
    check("load balance — thakkuva sent instance mundu", wp3.order("post")[0].name == "wa2",
          wp3.order("post")[0].name)
    wp3.instances[1].sent_today = 60
    check("daily cap ayyaka aa number skip", wp3.order("post")[0].name != "wa2", [i.name for i in wp3.order("post")])
    check("capacity_left + health lo sent/cap", wp3.instances[1].capacity_left() == 0
          and wp3.health()["instances"][1]["daily_cap"] == 60)

    print("=== 8. WA POOL — AUTH (401) + PER-NUMBER ANTI-BAN ENGINES ===")
    wp4 = wa_pool.WAPool([I("wa1"), I("wa2")], state_file=os.path.join(tmp, "s4.json"))

    def auth_fail(inst, item):
        if inst.name == "wa1":
            return {"ok": False, "status": 401, "error": "unauthorized"}
        return {"ok": True}

    run(wp4.deliver(item, lane="post", deliverer=auth_fail))
    check("401 → auth status + 1h cooldown (malli try avvadu)",
          wp4.instances[0].status == "auth" and wp4.instances[0].cooldown_until > 0)
    check("auth unna instance available kaadu", wp4.instances[0].available(wp4.instances[0].cooldown_until + 1) is False)
    e1 = wa_pool.engine_for("wa1")
    e2 = wa_pool.engine_for("wa2")
    check("per-number anti-ban engines separate", e1 is not None and e2 is not None and e1 is not e2)
    check("engine state files separate", os.path.basename(getattr(e1, "state_file", "")) !=
          os.path.basename(getattr(e2, "state_file", "")))
    check("okate name ki okate engine (cached)", wa_pool.engine_for("wa1") is e1)

    print("=== 9. PUBLISHER — POOL INTEGRATION ===")
    os.environ["WA_INSTANCES"] = ('[{"name":"wa1","url":"http://wa1:3000","lane":"both","daily_cap":5},'
                                  '{"name":"wa2","url":"http://wa2:3000","lane":"both","daily_cap":5}]')
    wa_pool._POOL = None
    pool_from_env = wa_pool.get_pool()
    check("publisher env nunchi WA_INSTANCES chaduvutundi", len(pool_from_env.instances) == 2,
          [i.name for i in pool_from_env.instances])
    check("publisher._wa_lane — W21 lanes (otp/personal/channels)", publisher._wa_lane({"priority": 0, "kind": "otp"}) == "otp"
          and publisher._wa_lane({"priority": 0, "kind": "interest_accepted"}) == "personal"
          and publisher._wa_lane({"priority": 1}) == "channels"
          and publisher._wa_lane({"priority": 0, "kind": "post"}) == "channels")
    check("dead_letters + requeue functions unnai", callable(publisher.dead_letters) and callable(publisher.requeue_dead))

    publisher.WA_QUEUE.clear()
    publisher.WA_DEAD.clear()
    publisher.WA_DEAD.append({"at": "now", "target": "@g1", "text": "hi", "priority": 0,
                              "kind": "interest", "attempts": [{"instance": "wa1"}]})
    req = publisher.requeue_dead(10)
    check("requeue_dead → dead letter queue lo malli vachhindi",
          req["requeued"] == 1 and req["dead_left"] == 0 and len(publisher.WA_QUEUE) == 1
          and publisher.WA_QUEUE[0]["requeued_from_dead"] is True, req)
    check("requeue ayyina item priority/lane intact", publisher.WA_QUEUE[0]["priority"] == 0
          and publisher.WA_QUEUE[0]["kind"] == "interest")
    check("dead_letters() shape + Telugu message", publisher.dead_letters()["count"] == 0
          and "QR" in publisher.dead_letters()["message_telugu"])
    os.environ.pop("WA_INSTANCES", None)
    wa_pool._POOL = None

    print("=== 10. API ENDPOINTS ===")
    from fastapi.testclient import TestClient
    import main

    with TestClient(main.app) as c:
        sh = c.get("/api/system/health").json()
        check("GET /api/system/health 200", isinstance(sh, dict) and "bots" in sh and "whatsapp" in sh)
        check("health lo queue + dead letters + Telugu status", "queue" in sh and "message_telugu" in sh)
        check("problems list (configure kaakapote chepthundi)", isinstance(sh["problems"], list))
        bh = c.get("/api/bots/health").json()
        check("GET /api/bots/health — failover order", bh["ok"] and "post_order" in bh and "recommended" in bh)
        ws = c.get("/api/wa/status").json()
        check("GET /api/wa/status lo instances + per_number", "instances" in ws and "per_number" in ws)
        dl = c.get("/api/wa/dead").json()
        check("GET /api/wa/dead shape", "count" in dl and "items" in dl and "message_telugu" in dl)
        rq = c.post("/api/wa/dead/requeue?limit=5").json()
        check("POST /api/wa/dead/requeue", "requeued" in rq and "queue" in rq)
        pst = c.get("/api/publish/status").json()
        check("publish/status lo bots + whatsapp_instances + dead_letters",
              "bots" in pst and "whatsapp_instances" in pst and "dead_letters" in pst)
        check("publish/status failover line", "failover" in pst["order"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n=== RESULT: %d pass / %d fail ===" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("🏆 FAILOVER (BOTS + WHATSAPP NUMBERS) — ANNI TESTS PASS")
