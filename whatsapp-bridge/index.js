/**
 * Mana Vivaha — WhatsApp Bridge (optional service)
 * ===============================================
 * Baileys tho WhatsApp Web session — groups / newsletter / community ki post cheyyadaniki.
 *
 * Endpoints:
 *   POST /send        { target, text, typingMs? }   → composing presence + text
 *   POST /send-image  { target, caption, imagePath | imageUrl, typingMs? }
 *   POST /presence    { target, state: composing|paused }  → "type chesthunnattu" simulation
 *   GET  /status      { connected, groups, sent, uptimeSec }
 *   GET  /qr          → QR page (login scan cheyyadaniki)
 *
 * NOTE (anti-ban): delay logic Python side lo undi (backend/wa_antiban.py) — bridge ki
 * 'typingMs' vaste, aa time antha "composing" presence chupistundi (manishi la kanipistundi).
 *
 * Startup:
 *   docker-compose up -d whatsapp-bridge
 *   → logs lo QR vasthundi → WhatsApp lo scan → session save (./session volume)
 *
 * Env:
 *   PORT=3001   SESSION_DIR=./session
 */
const express = require("express");
const fs = require("fs");
const path = require("path");
const QRCode = require("qrcode");
const pino = require("pino");
const {
  default: makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
} = require("@whiskeysockets/baileys");

const PORT = process.env.PORT || 3001;
const SESSION_DIR = process.env.SESSION_DIR || path.join(__dirname, "session");

const app = express();
app.use(express.json({ limit: "2mb" }));

let sock = null;
let connected = false;
let lastQR = null;
let groups = [];
let sentCount = 0;
const startedAt = Date.now();

// presence simulate — "type chesthunnattu" (manishi la kanipinchadaniki)
async function simulateTyping(jid, ms) {
  const wait = Math.min(Math.max(Number(ms) || 0, 0), 15000);
  if (!wait) return;
  try {
    await sock.presenceSubscribe(jid);
    await sock.sendPresenceUpdate("composing", jid);
    await new Promise((r) => setTimeout(r, wait));
    await sock.sendPresenceUpdate("paused", jid);
  } catch (e) {
    console.log("[WA] presence skip:", e.message);
  }
}

async function loadImage({ imagePath, imageUrl }) {
  if (imagePath && fs.existsSync(imagePath)) return fs.readFileSync(imagePath);
  if (imageUrl) {
    const res = await fetch(imageUrl);
    if (!res.ok) throw new Error(`imageUrl fetch failed: ${res.status}`);
    return Buffer.from(await res.arrayBuffer());
  }
  return null;
}

async function startSock() {
  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
  const { version } = await fetchLatestBaileysVersion();

  sock = makeWASocket({
    version,
    auth: state,
    logger: pino({ level: "silent" }),
    printQRInTerminal: false,
    browser: ["Mana Vivaha", "Chrome", "1.0.0"],
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async (u) => {
    const { connection, lastDisconnect, qr } = u;
    if (qr) {
      lastQR = qr;
      const dataUrl = await QRCode.toDataURL(qr);
      fs.writeFileSync(path.join(__dirname, "qr.html"),
        `<html><body style="font-family:sans-serif;text-align:center;background:#FFF8E7">
         <h2 style="color:#7A0C2E">Mana Vivaha — WhatsApp Login</h2>
         <p>WhatsApp → Linked Devices → Link a Device → ee QR scan chey</p>
         <img src="${dataUrl}" style="width:320px;border:6px solid #D4AF37;border-radius:16px"/>
         <p style="color:#666;font-size:12px">Scan ayyaka ee page refresh chey</p></body></html>`);
      console.log("[WA] QR ready → http://<server>:3001/qr  (qr.html)");
    }
    if (connection === "open") {
      connected = true;
      console.log("[WA] ✅ Connected to WhatsApp");
      try {
        const all = await sock.groupFetchAllParticipating();
        groups = Object.values(all).map((g) => ({ id: g.id, name: g.subject }));
        console.log(`[WA] ${groups.length} groups kanipisthunnayi`);
      } catch (e) {
        console.log("[WA] group list error:", e.message);
      }
    }
    if (connection === "close") {
      connected = false;
      const code = lastDisconnect?.error?.output?.statusCode;
      const retry = code !== DisconnectReason.loggedOut;
      console.log(`[WA] closed (code=${code}) retry=${retry}`);
      if (retry) setTimeout(startSock, 4000);
    }
  });
}

function normalizeTarget(target) {
  if (!target) return target;
  if (target.includes("@")) return target;
  const digits = target.replace(/[^0-9]/g, "");
  return `${digits}@s.whatsapp.net`;
}

app.post("/send", async (req, res) => {
  const { target, text, typingMs } = req.body || {};
  if (!connected) return res.status(503).json({ ok: false, error: "WhatsApp not connected — QR scan chey" });
  if (!target || !text) return res.status(400).json({ ok: false, error: "target + text kavali" });
  try {
    const jid = normalizeTarget(target);
    await simulateTyping(jid, typingMs);
    const r = await sock.sendMessage(jid, { text });
    sentCount += 1;
    res.json({ ok: true, id: r?.key?.id, target, sent: sentCount });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.post("/presence", async (req, res) => {
  const { target, state } = req.body || {};
  if (!connected) return res.status(503).json({ ok: false, error: "not connected" });
  try {
    const jid = normalizeTarget(target);
    await sock.presenceSubscribe(jid);
    await sock.sendPresenceUpdate(state === "paused" ? "paused" : "composing", jid);
    res.json({ ok: true, target, state: state || "composing" });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.post("/send-image", async (req, res) => {
  const { target, imagePath, imageUrl, caption, typingMs } = req.body || {};
  if (!connected) return res.status(503).json({ ok: false, error: "WhatsApp not connected" });
  if (!target) return res.status(400).json({ ok: false, error: "target kavali" });
  try {
    const image = await loadImage({ imagePath, imageUrl });
    if (!image) return res.status(400).json({ ok: false, error: "imagePath leda imageUrl kavali" });
    const jid = normalizeTarget(target);
    await simulateTyping(jid, typingMs);
    const r = await sock.sendMessage(jid, { image, caption: caption || "" });
    sentCount += 1;
    res.json({ ok: true, id: r?.key?.id, target, withImage: true, sent: sentCount });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.get("/status", (req, res) => res.json({
  connected,
  groups: groups.length,
  groupList: groups.slice(0, 50),
  sent: sentCount,
  uptimeSec: Math.floor((Date.now() - startedAt) / 1000),
}));
app.get("/groups", (req, res) => res.json({ connected, count: groups.length, groups }));
app.get("/qr", (req, res) => {
  const f = path.join(__dirname, "qr.html");
  if (fs.existsSync(f) && !connected) return res.sendFile(f);
  res.send(connected
    ? `<h2 style="color:green;font-family:sans-serif">✅ WhatsApp connected!</h2>`
    : `<h2 style="font-family:sans-serif">QR inka ready ledu — 5 sec tarvata refresh chey</h2>`);
});

app.listen(PORT, "0.0.0.0", () => console.log(`[WA] bridge listening on 0.0.0.0:${PORT}`));
startSock().catch((e) => console.error("[WA] start error:", e));
