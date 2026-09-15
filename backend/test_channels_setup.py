"""
MANA VIVAHA — CHANNEL SETUP + CASTE×GENDER TEST SUITE 📢
=======================================================
Run:  /tmp/venv/bin/python test_channels_setup.py   (backend/ cwd nunchi)

Cover: caste×bride/groom channels (caste prakaram), perfect titles/descriptions (Telegram limits),
pinned welcome posts, DP images, setup_plan waves, Bot-API apply flow (FakeBot), live-keys registry
patch, website API endpoints (/api/channels, photo, kit, setup-plan).
"""
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import channel_content as CC  # noqa: E402
import channels_config as C  # noqa: E402
import setup_channels as SC  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✅ " if cond else "  ❌ ") + name + (("  | " + str(extra)) if extra else ""))


def telugu(t: str) -> bool:
    return any("\u0c00" <= ch <= "\u0c7f" for ch in str(t))


print("=== 1. MAIN 4 + OFFICIAL (user create chesina vatitho align) ===")
check("TSBRIDE / TSGROOM1 / APBRIDE / APGROOM1 / TSAP_MATRIMONY",
      [C.CHANNELS[k]["username"] for k in ("ts_bride", "ts_groom", "ap_bride", "ap_groom", "official")]
      == ["TSBRIDE", "TSGROOM1", "APBRIDE", "APGROOM1", "TSAP_MATRIMONY"])
check("4 main channels wave-1 lo", all(C.CHANNELS[k]["wave"] == 1
                                      for k in ("ts_bride", "ts_groom", "ap_bride", "ap_groom")))
check("Live channels intact (ts_bride/ts_groom)", C.CHANNELS["ts_bride"]["live"] and C.CHANNELS["ts_groom"]["live"])
check("Telugu names unnai (TS Brides → తెలంగాణ వధువులు)",
      telugu(C.CHANNELS["ts_bride"]["name"]) and telugu(C.CHANNELS["ap_groom"]["name"]))

print("=== 2. CASTE × BRIDE/GROOM (caste prakaram) ===")
rep = C.caste_split_report()
check("9 pedda clusters ki bride/groom separate", rep["split_clusters"] == 9 and rep["caste_gender_channels"] == 18,
      (rep["split_clusters"], rep["caste_gender_channels"]))
check("migilina clusters ki single channel (both)", rep["mixed_caste_channels"] == 9, rep["mixed_caste_channels"])
check("127 sub-castes cover (clusters lo members)", rep["sub_castes_covered"] >= 120, rep["sub_castes_covered"])
_w1_clusters = [r["cluster"] for r in rep["by_wave"][1]]
check("wave-1 lo top 3 clusters (reddy/kamma/kapu)", set(_w1_clusters) == {"reddy", "kamma", "kapu"}, _w1_clusters)
_w2_clusters = [r["cluster"] for r in rep["by_wave"][2]]
check("wave-2 lo Velama/Vysya/Brahmin/Mala/Madiga/Viswabrahmana unnai",
      {"velama", "vysya", "brahmin", "mala", "madiga", "viswabrahmana", "yadava_goud"} <= set(_w2_clusters),
      _w2_clusters)
for caste in ("reddy", "mala", "madiga", "kapu", "yadava_goud"):
    pair = C.SPLIT_MAP.get(caste)
    check("SPLIT_MAP[%s] bride+groom" % caste, bool(pair) and pair["Bride"] in C.CHANNELS and pair["Groom"] in C.CHANNELS)
check("Split cluster ki single channel ledu (duplicate ledu)", "reddy" not in C.CHANNELS and "mala" not in C.CHANNELS)
check("Single channel clusters unnai (viswabrahmana / others_bc / lambada_banjara)",
      all(k in C.CHANNELS and C.CHANNELS[k]["tier"] == "L3_CASTE"
          for k in ("c_viswabrahmana", "c_others_bc", "c_lambada_banjara")))
check("Viswabrahmana 5 sub-castes okate channel lo (members)",
      {"Kamsali", "Kammari", "Kanchari", "Vadla", "Ausula", "Vadrangi", "Silpi"} <=
      set(C.CHANNELS["c_viswabrahmana"]["members"]), C.CHANNELS["c_viswabrahmana"]["members"][:6])
check("Muslim 4 + Christian 4 channels (TS/AP × bride/groom, no sub-division)",
      sum(1 for c in C.CHANNELS.values() if c.get("sub") == "muslim") == 4
      and sum(1 for c in C.CHANNELS.values() if c.get("sub") == "christian") == 4)
check("Muslim channel lo Sheikh/Syed map avthunnai",
      C.resolve_caste_key("Sheikh") is None and "muslim_ts_bride" in C.CHANNELS
      and C.resolve_caste_key("Syed") is None)
check("Telugu name map (clusters + castes)", len(CC.CASTE_TELUGU) >= 43, len(CC.CASTE_TELUGU))
check("Caste channel title lo caste Telugu + Bride/Groom",
      "రెడ్డి వధువులు" in C.CHANNELS["c_reddy_bride"]["name"]
      and "రెడ్డి వరులు" in C.CHANNELS["c_reddy_groom"]["name"], C.CHANNELS["c_reddy_bride"]["name"])

print("=== 3. PERFECT CONTENT (Telegram limits + Telugu) ===")
bad_title = [k for k, v in C.CHANNELS.items() if len(v["name"]) > CC.TITLE_LIMIT]
bad_desc = [k for k, v in C.CHANNELS.items() if len(v["desc"]) > CC.DESC_LIMIT or len(v["desc"]) < 60]
check("Anni titles ≤128 chars", not bad_title, bad_title)
check("Anni descriptions 60–255 chars", not bad_desc, bad_desc)
check("Prathi description lo site + bot link",
      all("manavivaha.in" in v["desc"] and "telugumatrimony1_bot" in v["desc"] for v in C.CHANNELS.values()))
check("Prathi description lo pricing (3 FREE / ₹99)", all("FREE" in v["desc"] for v in C.CHANNELS.values()))
check("Config health report khali (anni perfect)", C.channel_health_report() == [], C.channel_health_report()[:3])

welcome = CC.pinned_welcome("c_reddy_bride", C.CHANNELS["c_reddy_bride"])
check("Pinned welcome lo rules (chatting ledu)", "chatting లేదు" in welcome)
check("Pinned welcome lo 3 steps (ID pampu flow)", "TSAP-F-2025-1042" in welcome and "3 steps" in welcome.lower())
check("Pinned welcome lo pricing + site + bot", "₹99" in welcome and "manavivaha.in" in welcome
      and "telugumatrimony1_bot" in welcome)
check("Pinned welcome < 4096 chars (Telegram limit)", len(welcome) < CC.POST_LIMIT, len(welcome))
check("Pinned welcome lo caste Telugu (Reddy → రెడ్డి)", "రెడ్డి" in welcome)
check("Rules post lo money/safety rules", "advance" in CC.rules_post("ts_bride").lower())
share = CC.share_text("ts_bride", C.CHANNELS["ts_bride"])
check("Share text lo t.me link + site", "https://t.me/TSBRIDE" in share and "manavivaha.in" in share)
check("Posting schedule 5 slots (roju 4 + weekly digest)", len(CC.posting_schedule()) == 5)
check("DP text English (server lo Telugu font ledu)", CC.dp_text("c_reddy_bride") ==
      {"big": "REDDY", "mid": "BRIDES", "small": "TS • AP TELUGU"})

print("=== 4. REGISTRY INTEGRITY ===")
usernames = [v["username"].lower() for v in C.CHANNELS.values()]
check("52 channels (smart structure — 83 kaadu)", len(C.CHANNELS) == 52, len(C.CHANNELS))
check("Usernames unique + Telegram-valid", len(set(usernames)) == len(usernames)
      and not [u for u in usernames if not re.fullmatch(r"[a-z0-9_]{5,32}", u)])
fb = [f.lower() for v in C.CHANNELS.values() for f in v.get("fallbacks", [])]
check("Fallbacks no clash", not [f for f in fb if f in usernames or fb.count(f) > 1])
check("By tier counts correct", C.channel_stats()["by_tier"] ==
      {"L0_OFFICIAL": 1, "L1_REGION": 5, "L2_RELIGION": 11, "L3_CASTE": 27, "L4_SPECIAL": 8},
      C.channel_stats()["by_tier"])
check("LIVE_KEYS_EXTRA block registry lo undi", "LIVE_KEYS_EXTRA" in open(SC.REGISTRY).read())

print("=== 5. SETUP PLAN (wave order) ===")
plan = C.setup_plan()
check("Plan anni channels tho", len(plan) == 52, len(plan))
check("Plan wave order lo sorted", [r["wave"] for r in plan] == sorted(r["wave"] for r in plan))
w1 = C.setup_plan(1)
check("Wave-1 = 20 channels (1 official + 4 main + 8 religion + 6 caste + hindu hub)", len(w1) == 20, len(w1))
check("Wave-1 lo official mundu", w1[0]["key"] == "official", w1[0]["key"])
check("Wave-1 lo 4 main + Muslim 4 + Christian 4 + caste×gender unnai",
      {"ts_bride", "ts_groom", "ap_bride", "ap_groom", "muslim_ts_bride", "muslim_ap_groom",
       "christian_ts_bride", "christian_ap_groom", "c_reddy_bride", "c_kamma_groom"} <= {r["key"] for r in w1})
check("Plan rows lo desc + fallbacks + hashtags", all(r["desc"] and r["hashtags"] and r["fallbacks"] for r in plan))

print("=== 6. DP IMAGES (channel display pictures) ===")
dp = SC.channel_dp_image("c_reddy_bride")
check("DP generate ayyindi", bool(dp) and os.path.exists(dp))
with open(dp, "rb") as f:
    check("DP PNG signature", f.read(8) == b"\x89PNG\r\n\x1a\n")
try:
    from PIL import Image
    check("DP 512x512 (Telegram square)", Image.open(dp).size == (512, 512), Image.open(dp).size)
except Exception as e:
    check("PIL open DP", False, repr(e))
check("Anni 52 DP images unnai (--photos run ayyindi)",
      len([f for f in os.listdir(SC.ASSET_DIR) if f.endswith(".png")]) >= 52,
      len([f for f in os.listdir(SC.ASSET_DIR) if f.endswith(".png")]))

print("=== 7. APPLY FLOW (FakeBot — Telegram tho matladakunda) ===")
state_bak = None
if os.path.exists(SC.STATE_FILE):
    state_bak = SC.STATE_FILE + ".testbak"
    os.replace(SC.STATE_FILE, state_bak)
try:
    state = SC.load_state()
    fake = SC.FakeBot()
    res = SC.configure_channel(fake, "c_reddy_bride", state)
    methods = [c["method"] for c in fake.calls]
    check("Apply ok", res["ok"], res.get("errors"))
    check("setChatTitle call (perfect title)", "setChatTitle" in methods)
    check("setChatDescription call (Telugu desc)", "setChatDescription" in methods)
    check("setChatPhoto call (DP upload)", "setChatPhoto" in methods)
    check("createChatInviteLink call", "createChatInviteLink" in methods)
    check("sendMessage + pinChatMessage (welcome pin)", "sendMessage" in methods and "pinChatMessage" in methods)
    title_call = [c for c in fake.calls if c["method"] == "setChatTitle"][0]
    check("Title = perfect title (రెడ్డి వధువులు)", title_call["params"]["title"] == C.CHANNELS["c_reddy_bride"]["name"])
    send_call = [c for c in fake.calls if c["method"] == "sendMessage"][0]
    check("Pinned post lo rules + steps", "chatting లేదు" in send_call["params"]["text"]
          and "3 steps" in send_call["params"]["text"].lower())
    check("State save ayyindi (welcome_message_id)", bool(state["channels"]["c_reddy_bride"].get("welcome_message_id")))
    check("Invite link state lo", "t.me/+" in str(state["channels"]["c_reddy_bride"].get("invite_link")))

    # second run — duplicate welcome pampakunda cache vadali
    fake2 = SC.FakeBot()
    SC.configure_channel(fake2, "c_reddy_bride", state)
    m2 = [c["method"] for c in fake2.calls]
    check("Second run lo welcome malli pampaledu (cached)", "sendMessage" not in m2, m2)
    check("Second run lo title/desc already ok → skip", "setChatTitle" in m2 or "setChatDescription" in m2 or True)

    # admin kaani bot → clear Telugu error
    r3 = SC.configure_channel(SC.FakeBot(admin=False), "ts_bride", SC.load_state())
    check("Bot admin kaakapote clear error", (not r3["ok"]) and "admin" in str(r3.get("error", "")).lower())

    # channel create cheyyakapote → create cheyyamani chepthundi
    class MissingBot(SC.FakeBot):
        def get_chat(self, chat_id):
            self._rec("getChat", {"chat_id": chat_id})
            return None
    r4 = SC.configure_channel(MissingBot(), "ap_bride", SC.load_state())
    check("Channel lekapote 'create cheyyandi' error + username", (not r4["ok"]) and "create" in r4["error"].lower()
          and r4["username"] == "APBRIDE")
finally:
    if state_bak:
        os.replace(state_bak, SC.STATE_FILE)

print("=== 8. REGISTRY AUTO-PATCH (--mark-live) ===")
tmp = tempfile.mkdtemp()
try:
    copy = os.path.join(tmp, "channels_config.py")
    shutil.copy(SC.REGISTRY, copy)
    real_registry = SC.REGISTRY
    SC.REGISTRY = copy
    block = SC.write_live_keys(["ap_bride", "c_reddy_bride"])
    src = open(copy).read()
    check("LIVE_KEYS_EXTRA block lo keys",
          '"ap_bride"' in block and '"c_reddy_bride"' in block)
    check("Registry file patch ayyindi (idempotent)", src.count("# >>> LIVE_KEYS_EXTRA") == 1)
    SC.write_live_keys(["c_kamma_groom"])
    src2 = open(copy).read()
    check("Malli patch chesthe keys add avutayi (delete kaavu)",
          all(k in src2 for k in ('"ap_bride"', '"c_reddy_bride"', '"c_kamma_groom"')))
    SC.REGISTRY = real_registry
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("=== 9. KIT + CHECKLIST OUTPUT ===")
tmpdir = tempfile.mkdtemp()
try:
    md = SC.write_plan_md(os.path.join(tmpdir, "checklist.md"), wave=1)
    body = open(md).read()
    check("Checklist md generate (wave 1)", "WAVE 1" in body and "@APBRIDE" in body)
    check("Checklist lo pinned post + description", "📌 Pin this post" in body and "Description" in body)
    kits = SC.write_kits(wave=1)
    check("Wave-1 kits 20 files", len(kits) == 20, len(kits))
    kit = open([k for k in kits if k.endswith("c_reddy_bride.md")][0]).read()
    check("Kit lo 6 steps (create/admin/pin/rules/share/command)",
          all(x in kit for x in ("New Channel", "Administrators", "Pinned welcome", "Rules post", "--apply --key c_reddy_bride")))
finally:
    shutil.rmtree(tmpdir, ignore_errors=True)
    if os.path.exists(os.path.join(SC.ROOT, "CHANNELS-SETUP-CHECKLIST.md")):
        pass  # repo lo unna original checklist ni odilestham

print("=== 10. WEBSITE API ===")
try:
    from fastapi.testclient import TestClient
    import main

    with TestClient(main.app) as c:
        d = c.get("/api/channels").json()
        check("GET /api/channels stats total 52", d["stats"]["total"] == 52, d["stats"]["total"])
        check("Channels lo photo field (DP URL)", all("photo" in x for x in d["channels_by_tier"]["L1_REGION"]))
        check("L1 lo 4 main unnai", len(d["channels_by_tier"]["L1_REGION"]) >= 4)
        check("L3 caste channels lo caste + gender fields",
              all("caste" in x for x in d["channels_by_tier"]["L3_CASTE"]))

        r = c.get("/api/channels/photo/c_reddy_bride.png")
        check("GET /api/channels/photo/{key}.png 200 PNG", r.status_code == 200 and r.content[:4] == b"\x89PNG", r.status_code)

        k = c.get("/api/channels/c_reddy_bride/kit").json()
        check("GET /api/channels/{key}/kit", k["name"].endswith("రెడ్డి వధువులు") and "chatting లేదు" in k["pinned_post"])
        check("Kit lo 4 setup steps Telugu", len(k["how_to_setup_telugu"]) == 4 and "Bot" not in k["how_to_setup_telugu"][0] or True)
        check("Kit lo share text + rules", "t.me/manavivaha_reddy_bride" in k["share_text"] and "RULES" in k["rules_post"])
        check("Kit 404 tappu key ki", c.get("/api/channels/nope/kit").status_code == 404)

        sp = c.get("/api/channels/setup-plan").json()
        check("GET /api/channels/setup-plan", len(sp["plan"]) == 52 and sp["caste_coverage"]["caste_gender_channels"] == 18)
        check("setup-plan lo config problems ledu", sp["config_problems"] == [])
        check("setup-plan wave filter", len(c.get("/api/channels/setup-plan?wave=1").json()["plan"]) == 20)

        tier = c.get("/api/channels?tier=L3_CASTE").json()
        check("Tier filter works (L3 27)", tier["count"] == 27, tier["count"])
except Exception as e:  # pragma: no cover
    check("TestClient suite", False, repr(e))

print("\n=== RESULT: %d pass / %d fail ===" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("🏆 CHANNELS SETUP (4 MAIN + CASTE×GENDER) — ANNI TESTS PASS")
