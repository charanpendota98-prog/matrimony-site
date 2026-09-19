# Private control access

The public website has no Admin or Worker link. Both roles use one private portal:

```text
https://control.manavivaha.in/login
```

For the current single-domain deployment, the same route is available at:

```text
https://manavivaha.in/control/login
```

After login, the server role decides the destination:

- `owner` → `/control`
- `worker` → `/control/workspace`

## Create accounts safely

There are intentionally **no default usernames or passwords**. Do not put credentials in source code, chat, GitHub, browser localStorage, or `.env.example`.

On a secure server, run:

```bash
python backend/provision_control.py --role owner --username owner@your-domain.com
python backend/provision_control.py --role worker --username reviewer@your-domain.com
```

The command asks for the password without echoing it and prints a PBKDF2 password hash. Put the resulting account JSON in the deployment secret manager as `CONTROL_ACCOUNTS_JSON`, for example:

```json
{"owner":{"username":"owner@your-domain.com","password_hash":"pbkdf2_sha256$210000$..."},"worker":{"username":"reviewer@your-domain.com","password_hash":"pbkdf2_sha256$210000$..."}}
```

Use separate invite-only accounts. Never share an owner account with a worker.

## Permissions

Workers can use review queues and masked operational data. The backend does not return worker phone numbers, emails, payment values, exports, backups, secrets, or staff-management data. Owner-only actions remain protected server-side even when a worker manually enters an owner URL.

Production startup refuses to run without:

- `TSAP_AUTH_SECRET` (32+ random characters)
- `ADMIN_KEY` (legacy endpoint compatibility during migration)
- at least one control account
- a real OTP provider (WhatsApp bridge or SMS provider)

## Launch checklist

1. Configure DNS for `control.manavivaha.in` and HTTPS.
2. Put account hashes and secrets in the VM secret manager.
3. Start the backend with `APP_ENV=production`.
4. Open `/control/login` and test one owner and one worker account.
5. Confirm a worker receives `403` for owner-only money/export endpoints.
6. Confirm OTP with a real phone: wrong code must return `invalid_otp`; only the exact current code verifies.
7. Rotate any token accidentally pasted into chat or logs before marketing or launch.
