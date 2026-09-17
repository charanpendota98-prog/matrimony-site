# 💾 BACKUP + RESTORE GUIDE (Telugu) — Mana Vivaha

> **Bhayam vaddu.** Data anni simple files lo untundi. Crash ayina, server
> maripoyina — backup zip + code + `.env` unte site **5–10 mins lo malli ready**.

---

## 1. Data EKKADA store avutundi?

| Data | File (server lo) | Vivaranam |
|---|---|---|
| 👥 Users (register ayina profiles) | `backend/data_db.json` | **CORE — chala important** |
| 💌 Interests/requests | `backend/data_db.json` (lopale) | Core lopale untundi |
| 💰 Payments/orders | `backend/data_db.json` (lopale) | Core lopale untundi |
| 📋 Number unlocks | `backend/unlocks12.json` | Credits count |
| 💳 Razorpay orders | `backend/paypro14.json` | Online payments |
| 🤝 Referral wallet | `backend/referral_state.json` | ₹50 rewards |
| 📢 Channel mapping | `backend/chanmap15.json` | Telegram/WhatsApp links |
| 🔔 Push subs | `backend/push_state.json` | Bell subscribers |
| 📲 WA queue | `backend/wa_state.json` | WhatsApp messages |
| 📸 CMS/stories/ads | `backend/cms15.json`, `stories_state.json`, `ads13.json` | Website content |

Anni **JSON text files** — database server avasaram ledu. `backend/` folder lopale.

---

## 2. Backup DOWNLOAD cheyyadam (weekly once cheyandi!)

1. Browser lo open: `https://mee-site.com/owner`
2. Admin key vesi **View** → kinda **💾 Backup / Restore** card
3. **⬇️ బ్యాకప్ download** → `mana-vivaha-backup.zip` vastundi
4. Ee zip ni **2 chotla dachukondi**: mee laptop + Google Drive

> Server prathi restart ki **automatic snapshot** kuda teeskuntundi
> (`backend/backups/startup-*.zip`, last 10 untayi). Kani adi server lone
> untundi — **manual download mee daggara pettukovadam BEST.**

---

## 3. Crash / server poyindi? RESTORE steps

**Kottha server (leda same server fix ayyaka):**

```
Step 1: Code malli pettandi (git clone — developer chestharu)
Step 2: backend/ folder loki backup zip nunchi *.json/*.jsonl copy cheyandi
        (leda /owner page lo ⬆️ Restore(zip) tho upload cheyandi)
Step 3: .env file (API keys) malli pettandi — adi backup lo UNDADU!
Step 4: backend restart → site live ✅
```

**Restore 2 rakalu:**
- **Easy:** `/owner` page → ⬆️ Restore (zip) → file select → done (old data ki
  auto `pre-restore-*.zip` snapshot kuda untundi — tappu file pettina venakki vachochu)
- **Manual:** zip open chesi files ni `backend/` loki copy + restart

---

## 4. Admin panel MALLI setup ante?

Admin panel = **code + data + keys**, 3 parts:

| Part | Ela vastundi? |
|---|---|
| Code (admin pages) | Git nunchi (developer) — `arena/...` branch |
| Data (users/payments) | Backup zip nunchi restore |
| Keys (`.env`: Razorpay, Telegram, admin key) | **Mee daggara unna `.env` copy nunchi** |

⚠️ **`.env` file backup zip lo UNDADU** (security kosam) — daanini separate ga
safe chotla dachukondi. Adi lekunte payments/bot panicheyyavu.

---

## 5. Telegram/WhatsApp channels IPPUDU ivvala?

**Avasaram LEDU ippudu.** Admin panel lo **Channels** section lo eppudaina
links add cheyochu. Links lenappudu system **dry-run mode** lo perfect ga
nadustundi (posts queue avutayi, links vachaka live avutayi). `/owner` page lo
**📢 Channels** card lo gap kanipistundi — adi fill ayyaka anni live.

---

## 6. Checklist (nela ki okasari)

- [ ] `/owner` nunchi backup zip download → laptop + Drive
- [ ] `.env` copy safe ga unda chudandi
- [ ] `/owner` page anni greenENA chudandi (revenue, users, system)
- [ ] Razorpay test payment okati vesi chudandi

**Anni perfect ga unte — tension vaddu, site safe! 🙏**
