# 🚀 DEPLOY GUIDE (Telugu) — Mana Vivaha LIVE cheyyadam

> Site code 100% ready. Deploy ante: **server + domain + ee steps**. 1–2 hours lo live.

---

## 0. Meeku kavalsindi (mundu ready chesukondi)

| # | Item | Ekada? | Cost (approx) |
|---|---|---|---|
| 1 | **VPS server** (Ubuntu 22.04, 2GB RAM+) | Hostinger / DigitalOcean / Hetzner | ₹500–1000/nela |
| 2 | **Domain** (`manavivaha.in` lanti) | Hostinger / GoDaddy / Namecheap | ₹800/samvatsaram |
| 3 | **Razorpay account** | razorpay.com (KYC) | Free (per-payment cut) |
| 4 | **Telegram bot** | @BotFather (2 min) | Free |
| 5 | **SMS (OTP)** | MSG91 / Fast2SMS | ₹1000 nunchi |

Domain DNS lo: `A record → mee server IP` (vide: `@` + `www` rendu). 10–30 mins lo work avutundi.

---

## 1. Server setup (onetime, 15 min)

Server lo login ayyaka (SSH):

```bash
# Docker install
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER && newgrp docker

# Code download (mee branch)
git clone -b arena/01a0aaf1-matrimony-site https://github.com/charanpendota98-prog/matrimony-site.git
cd matrimony-site

# Env file ready
cp .env.example .env
nano .env   # kinda MUST values fill cheyandi (step 2)
```

---

## 2. `.env` lo MUST values (marchipokandi!)

```
TSAP_AUTH_MODE=on                    # prod = on (off ayithe security undadu!)
TSAP_API_KEY=<32+ random>            # openssl rand -hex 24
ADMIN_KEY=<32+ random>                # admin/owner key — secret!
JWT_SECRET=<32+ random>
CORS_ORIGINS=https://mee-domain.com
PUBLIC_SITE_URL=https://mee-domain.com
BOT_TOKEN=<@BotFather nunchi>
RAZORPAY_KEY_ID / _SECRET / WEBHOOK_SECRET
PAY_UPI_ID=mee-upi@bank
VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY  # push alerts (guide: PLAYSTORE-GUIDE)
NEXT_PUBLIC_SUPPORT_PHONE=91XXXXXXXXXX
```

Random keys generate: `openssl rand -hex 24` (server lo run cheyandi).

---

## 3. Site START (prod mode)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps   # anni Up undali
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f backend  # errors unte chudandi (Ctrl+C exit)
```

> ⚠️ **Eppudu prod file tho start cheyandi** (`-f ...prod.yml`) — lekunte dev
> mode (reload + demo data) lo nadustundi!

---

## 4. Domain + SSL (https, 10 min)

Easy way — **Caddy** (SSL automatic, free):

```bash
sudo apt install -y caddy
sudo tee /etc/caddy/Caddyfile <<'EOF'
mee-domain.com, www.mee-domain.com {
    reverse_proxy localhost:3000
}
EOF
sudo systemctl reload caddy
```

2 mins lo `https://mee-domain.com` green lock 🔒 tho open avutundi.

---

## 5. LIVE verify checklist (oka 10 min)

- [ ] `https://mee-domain.com` open + Telugu toggle
- [ ] Register → OTP → profile create (test number tho)
- [ ] `/api/health` → `{"success": true}` (browser lo `mee-domain.com/api/health`)
- [ ] Razorpay test payment ₹1 → credits padaya?
- [ ] `/owner` (admin key) → revenue/users kanipistunnaya?
- [ ] **Backup download** (`/owner` → 💾) → laptop + Drive lo pettandi
- [ ] Phone lo site open → 📲 install button → home screen icon

---

## 6. Updates (kottha features vachinappudu)

```bash
cd matrimony-site
git pull origin arena/01a0aaf1-matrimony-site
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Data (`backend/*.json`) volumes lo safe — build aina potadu. Bhayam unte
mundu `/owner` nunchi backup zip download chesukondi.

**Rollback** (edo problem vasthe): `git log --oneline -3` →
`git checkout <old-commit>` → same `up -d --build`.

---

## 7. Bhadratha (security — chala important)

1. `ADMIN_KEY` + `.env` **evariki ivvakandi** (developer ki kuda avasaram ayithe thappa)
2. `/admin` + `/owner` links public lo ekkada levu — ala ne unchandi
3. Server SSH: password kadu, **key-only** login pettandi
4. `sudo ufw allow 22,80,443 && sudo ufw enable` (firewall)
5. Backup zip **weekly** download (laptop + Drive)

---

## 8. Cost + scale (future)

- Start: 1 VPS (2GB) chalu — 1000s users, 10000s page views
- Periginappudu: VPS upgrade (4GB) — code marchalsina avasaram ledu
- Users 50k+ ayyaka: Postgres shift (data export script ready cheskovachu)

---

## 9. MilesWeb vallaki SPECIAL (domain + hosting)

**Meedaggara MilesWeb PREMIUM (shared/cPanel) + manavivaha.in unte:**

| Item | Verdict |
|---|---|
| MilesWeb shared PREMIUM hosting | ❌ **App RUN AVVADU** — Docker/Node/Python server process lu shared hosting lo work avvavu. Adi WordPress/PHP sites ke. |
| manavivaha.in domain (MilesWeb lone) | ✅ **Perfect** — DNS akkade manage cheyandi, chalu. |
| Kavalsindi | ✅ **VPS** (Ubuntu 22.04, 2GB RAM+) — MilesWeb lone VPS order cheyochu (same account, support easy) leda DigitalOcean/Hetzner. ~₹600–1000/nela. |

**DNS steps (MilesWeb client area → Domains → manavivaha.in → DNS Management):**

| Type | Host | Value |
|---|---|---|
| A | `@` | mee VPS IP (ex: `123.45.67.89`) |
| A | `www` | mee VPS IP (same) |

10–30 mins lo `http://manavivaha.in` VPS ki vastundi → Step 4 (Caddy) tho
`https://` green lock 🔒 automatic.

> Shared premium hosting waste kadu — future lo blog/landing pages ki, leda
> email accounts ki vadukovachu. Kani APP matram VPS meeda.

---

## 10. Oracle Cloud FREE Tier (₹0 — RECOMMENDED!)

Meedaggara Oracle Cloud account unte — **dabbulu avasaram ledu**, free tier lone
site full run avutundi. Domain MilesWeb lone unchandi (DNS akkade).

**Step 1 — Free VM create (OCI Console → Compute → Create Instance):**

| Setting | Value |
|---|---|
| Image | **Ubuntu 22.04 Minimal** (aarch64/ARM) |
| Shape | **Ampere A1 (ARM)** — 4 OCPU + 24GB RAM (Always Free limit lopale) |
| VCN | Default VCN + **public subnet** + **public IP assign** ✅ |
| SSH key | Mee laptop nunchi `.pub` key paste (`ssh-keygen` lekapothe) |
| Boot volume | 50GB chalu (200GB free limit lopale) |

> ⚠️ AMD shape (1GB RAM) **tiskokandi** — adi chalu kadu. Ampere ARM ey best.
> Mana Docker images (Python + Node) ARM lo perfect ga work avutayi.

**Step 2 — Reserved IP (mundu cheyandi!):**

VM stop/start aithe normal IP maripotundi → site down! So:
`OCI → Networking → Public IPs → Reserve` → VM VNIC ki attach.
(VM ki attach ayi unte **free**.)

**Step 3 — Firewall open (MARCHIPOKANDI — 90% mandi ikkade stuck!):**

OCI VCN → Security List → **Add Ingress Rules**:
- Source `0.0.0.0/0`, port **80** (TCP)
- Source `0.0.0.0/0`, port **443** (TCP)
- (22 SSH already untundi)

VM lopala kuda:
```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save 2>/dev/null || sudo apt install -y iptables-persistent
```

**Step 4 — Server ready (copy-paste):**

```bash
sudo apt update && sudo apt install -y git caddy
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER && newgrp docker
git clone -b arena/01a0aaf1-matrimony-site https://github.com/charanpendota98-prog/matrimony-site.git
cd matrimony-site && cp .env.example .env && nano .env   # step 2 values!
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
sudo cp Caddyfile.example /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

**Step 5 — MilesWeb DNS → Oracle IP:**

MilesWeb → manavivaha.in → DNS: `A @ → OCI reserved IP`, `A www → OCI reserved IP`.
30 mins lo `https://manavivaha.in` 🔒 LIVE!

**Oracle gotchas (telusukondi):**

1. Account ki **card verify** kavali (charge avvadu, ₹0/hold only)
2. Nela ki okasari console lo **login** avvandi (idle accounts meeda strict)
3. **Backup zip weekly** download (`/owner` → 💾) — free tier aina data mee చేతిలో safe
4. Boot volume backup (OCI console → monthly once, free limit lopale)

**Doubt unte developer ni adagandi — deploy day roju pakkana undandi. All the best! 🙏**
