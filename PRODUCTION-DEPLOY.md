# Production deployment checklist

This project will refuse to boot as production when mandatory secrets, control accounts, or a real OTP provider are missing.

## 1. Prepare a server secret file

Copy `.env.example` to a server-only file. Do not commit it:

```bash
cp .env.example .env.production
chmod 600 .env.production
```

Set at minimum:

```env
APP_ENV=production
POSTGRES_PASSWORD=<random 32+ chars>
TSAP_AUTH_SECRET=<random 32+ chars>
ADMIN_KEY=<random 32+ chars>
TSAP_API_KEY=<random 32+ chars>
CONTROL_ACCOUNTS_JSON=<generated account JSON>
CORS_ORIGINS=https://manavivaha.in,https://www.manavivaha.in,https://control.manavivaha.in
PUBLIC_SITE_URL=https://manavivaha.in
OTP_DEV_MODE=false
```

Use a real SMS provider or WhatsApp bridge. Never use `OTP_DEV_MODE=true` in production.

## 2. Start the production stack

```bash
docker compose --env-file .env.production \
  -f docker-compose.yml -f docker-compose.prod.yml \
  up -d --build
```

Do not expose PostgreSQL or Redis publicly. They should be reachable only by the backend network.

## 3. Reverse proxy

Use `Caddyfile.example` as the starting point and add the control host:

```text
manavivaha.in, www.manavivaha.in {
    reverse_proxy 127.0.0.1:3000
    encode gzip
}

control.manavivaha.in {
    reverse_proxy 127.0.0.1:3000
    encode gzip
}
```

The control hostname is not a security boundary; the session/RBAC checks remain mandatory.

## 4. Smoke test before marketing

```bash
curl -fsS https://manavivaha.in/api/health
curl -i https://manavivaha.in/api/control/me
```

Then verify manually:

- Owner can sign in at `/control/login`.
- Worker can sign in at `/control/login`.
- Worker is redirected to `/control/workspace`.
- Worker receives 403 for owner-only exports/payments/backups.
- Wrong OTP returns `invalid_otp`.
- Exact OTP verifies once, then cannot be replayed.
- A real Razorpay webhook is accepted once and rejected on replay.
- WhatsApp lanes show healthy, paused, or unavailable rather than pretending to send.
- Backup restore succeeds on a separate temporary database.

Only after these checks should paid marketing or channel promotion start.
