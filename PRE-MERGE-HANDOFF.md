# Manavivaha — pre-merge handoff and deployment status

Updated: 2026-09-19
Branch: `arena/01a0b9af-shubhalagnam`
Latest commit: `53b9806 ops: harden production deployment configuration`

## Current checkpoint

The branch contains the current professional pass. It has been pushed to the Arena branch and is ready for review before merge.

The supplied VM log showed an earlier deployment on a different Arena branch (`arena/01a0b4e9-shubhalagnam`) at commit `4c5775c`. That VM initially had a frontend restart loop because the development `./frontend:/app` host volume hid the image's `.next` production build. Removing that host mount and restarting the frontend restored HTTP 200. The deployment script now supports an explicit `DEPLOY_BRANCH` so pre-merge staging cannot silently deploy an unrelated branch.

### Implemented

- Cinematic wedding homepage section:
  - scroll-driven wedding story
  - mandapam, couple, lighting, petals and fire layers
  - desktop drag and mobile swipe rotation effect
  - mobile responsive layout
  - reduced-motion fallback
  - real register and matches CTAs remain usable
- Private operations portal:
  - `/control/login`
  - owner and worker roles
  - HttpOnly SameSite session cookie
  - PBKDF2 password hashes
  - login throttling and session expiry
  - CSRF-protected logout
  - backend role enforcement
  - worker-safe profile review queue
  - owner-only sensitive operations
- Control access tooling:
  - `backend/provision_control.py`
  - `CONTROL-ACCESS.md`
  - no default owner or worker password is stored in Git
- Channel operations:
  - bride/groom/shared audience labels
  - region/religion/caste/special filters
  - Telegram and WhatsApp link fields beside each channel
  - active toggle and save action
  - bulk import preview and apply
  - live/coverage/gap indicators
  - only explicitly mapped or live Telegram links are shown as publishable
- WhatsApp lanes:
  - OTP lane
  - channel-post lane
  - personal/support lane
  - random gaps, daily caps, cooldowns, retries and failover
  - admin pause/resume/health view
- OTP safety:
  - HMAC OTP storage instead of plaintext storage
  - exact-current-code verification
  - invalid OTP response
  - expiry and one-time use
  - five-attempt lock
  - production `OTP_DEV_MODE=false`
  - no fake success when no real provider is configured
- Production configuration:
  - mandatory production secrets
  - no hardcoded PostgreSQL password
  - production compose override
  - persistent production volumes
  - Caddy configuration for public and control hosts
  - `PRODUCTION-DEPLOY.md`
- Frontend dependency upgrade:
  - Next.js `16.3.5`
  - npm audit passed with zero reported vulnerabilities at the time of the check

## Validation completed

- Python compile checks passed.
- `git diff --check` passed.
- Frontend production build passed.
- Branch pushed to origin.

## Production deployment target

The supplied deployment target is an Oracle/Ubuntu VM:

```text
ubuntu@144.24.144.218
```

The SSH key remains on the operator's machine and must not be committed or pasted into chat. Use the operator's secure SSH environment or Arena server integration.

Recommended hosts:

```text
manavivaha.in
www.manavivaha.in
control.manavivaha.in
```

## Required server-side configuration before live

Configure these in a server-only secret file or secret manager; never commit them:

```env
APP_ENV=production
POSTGRES_PASSWORD=<random value>
TSAP_AUTH_SECRET=<32+ random characters>
ADMIN_KEY=<32+ random characters>
TSAP_API_KEY=<32+ random characters>
CONTROL_ACCOUNTS_JSON=<owner and worker password hashes>
CORS_ORIGINS=https://manavivaha.in,https://www.manavivaha.in,https://control.manavivaha.in
PUBLIC_SITE_URL=https://manavivaha.in
OTP_DEV_MODE=false
```

Also required for real operations:

- PostgreSQL and Redis availability
- MSG91/Fast2SMS or approved WhatsApp OTP provider
- Razorpay live keys and webhook secret
- Telegram bot token(s) and channel admin permissions
- Three separate WhatsApp sessions and QR scans
- Actual channel links entered from the owner control portal
- DNS records and HTTPS certificate

## Deployment command

On the VM, after the secret file is ready:

```bash
docker compose --env-file .env.production \
  -f docker-compose.yml -f docker-compose.prod.yml \
  up -d --build
```

Then configure/reload Caddy using `Caddyfile.example`.

## Required pre-merge/live smoke checks

1. `GET /api/health` returns healthy.
2. Owner can sign in at `/control/login` and reaches `/control`.
3. Worker can sign in and reaches `/control/workspace`.
4. Worker receives 403 for owner-only payments, exports, backups and staff actions.
5. Worker queue has no phone, email, payment or document values.
6. Wrong OTP returns `invalid_otp`.
7. Exact OTP verifies only once and cannot be replayed.
8. OTP provider failure returns a provider error, not a fake success.
9. WhatsApp OTP/channel/personal lanes report correct health and caps.
10. Telegram and WhatsApp links are real and verified before activation.
11. Razorpay webhook replay is rejected.
12. Backup restore succeeds on a temporary database.
13. Mobile homepage, register, search and matches work through the public HTTPS host.

## Important remaining engineering item

The existing application still has legacy in-memory/JSON-backed modules. PostgreSQL and Redis services are present in compose, but a complete data-layer migration and production restore drill must be completed and verified before claiming full enterprise production readiness. Do not merge that claim as complete merely because containers start.

## Security note

An EarnKaro JWT/API token was pasted into chat during the work. Treat it as compromised: revoke it and issue a replacement before production. Never put tokens, passwords or SSH keys in this repository or in chat.
