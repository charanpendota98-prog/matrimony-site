# LIVE CHANNELS CONFIG — Actual Channels Created ✅

## User Created Channels (Live)

| # | Channel Name | Link | Username | Type | Status |
|---|---|---|---|---|---|
| 1 | TS BRIDE | https://t.me/TSBRIDE | @TSBRIDE | TS Brides | ✅ Created, Bot Admin |
| 2 | TS GROOM | https://t.me/TSGROOM1 | @TSGROOM1 | TS Grooms | ✅ Created, Bot Admin |
| 3 | AP Brides (Next) | t.me/APBRIDE (suggest) | @APBRIDE | AP Brides | ⏳ To Create |
| 4 | AP Grooms (Next) | t.me/APGROOM1 (suggest) | @APGROOM1 | AP Grooms | ⏳ To Create |
| 5 | Official Hub | t.me/TSAP_MATRIMONY (suggest) | @TSAP_MATRIMONY | Official | ⏳ To Create |

**Current: 2 channels chalu — ippudu 2 tho start, taruvata AP + Official add cheddam — user cheppinattu.**

## Bot Live

| Item | Value |
|---|---|
| Bot Username | @telugumatrimony1_bot |
| Bot Link | https://t.me/telugumatrimony1_bot |
| Token | `8844112261:AAH...` (stored securely in backend/.env — NOT in git) |
| Status | ✅ Admin in 2 channels |
| Deep Links | `t.me/telugumatrimony1_bot?start=ch_tsbride`, `t.me/telugumatrimony1_bot?start=ch_tsgroom1` |

## Backend Config Updated

**File: `backend/.env`**
```
BOT_TOKEN=8844112261:AAH...
BOT_USERNAME=@telugumatrimony1_bot
CHANNELS=TSBRIDE,TSGROOM1
MAIN_CHANNELS=@TSBRIDE,@TSGROOM1
```

**File: `backend/main.py` — channels() endpoint updated to return live channels**

**Frontend: `src/app/channels/page.tsx` — will show live channels TSBRIDE, TSGROOM1**

## Auto-Router Logic for Live Channels

```yaml
# Live routing (2 channels now)
TS + Bride → @TSBRIDE
TS + Groom → @TSGROOM1
AP + Bride → @TSBRIDE (temp, until APBRIDE created) + tag #AP
AP + Groom → @TSGROOM1 (temp, until APGROOM1 created) + tag #AP

# After AP channels created:
TS + Bride → @TSBRIDE
TS + Groom → @TSGROOM1
AP + Bride → @APBRIDE
AP + Groom → @APGROOM1

# Caste channels (future): @tsap_reddy etc — after Main 4 stable
```

## How Bot Will Post (Pin-to-Pin)

1. User registers via website/bot → Backend generates ID `TSAP-F-2025-1042` + Card
2. Admin approves via bot button → `POST /api/admin/approve/{id}` → 
   - Determine channels: TS Bride → @TSBRIDE
   - Bot API call: `sendPhoto` to @TSBRIDE with card + caption + hashtags + footer + deep link
   - Save to DB posts
   - User gets Top 3 FREE with reason
3. Test command (when network allows):
```bash
curl -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
  -d chat_id=@TSBRIDE \
  -d text="🎉 Test — TSAP Matrimony Bot LIVE! First profile coming soon — @telugumatrimony1_bot"
```

## Next Steps for Channels

- [x] 2 channels created + bot admin
- [ ] DP + Description + Pinned Post (templates in MAIN-4-CHANNELS-CHECKLIST.md)
- [ ] Seed 20 profiles per channel (friends/brokers nunchi)
- [ ] Test auto-post (backend will post when approve)
- [ ] Create AP channels + Official when TS channels reach 100 members
- [ ] WhatsApp Community + Channel (mirror)

## Security

- Token stored in `backend/.env` — gitignore lo undi, git lo commit kaadhu
- Never share token publicly — user already shared once, but we secured
- If token leak → BotFather lo /revoke

## Frontend Update Needed

- Update channels page to show live links t.me/TSBRIDE, t.me/TSGROOM1
- Update home page main channels to live usernames
- Add bot link t.me/telugumatrimony1_bot everywhere
