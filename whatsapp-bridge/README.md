# WhatsApp Bridge — Mana Vivaha

Telegram tho paatu **WhatsApp groups / community / newsletter** ki kooda auto-post cheyyadaniki.

## Enti cheyyagaladu
- Baileys (WhatsApp Web multi-device) — **personal number**, official API approval avasaram ledu
- Groups, Community announcement groups, aur direct numbers ki text + image (profile card) post
- Backend `publisher.py` tho connect: `WHATSAPP_MODE=bridge` + `WHATSAPP_BRIDGE_URL=http://whatsapp-bridge:3001/send`

## Start (server lo)
```bash
cd ~/matrimony-site
docker-compose up -d whatsapp-bridge      # docker-compose.yml lo comment teeyy / service add chey
docker logs -f matrimony-site_whatsapp-bridge_1
# Browser lo: http://140.245.216.16:3001/qr  → QR scan (WhatsApp → Linked Devices)
# Scan ayyaka: curl http://140.245.216.16:3001/status  → {"connected":true, "groupList":[...]}
```

## Group IDs teesukovadam
```bash
curl -s http://localhost:3001/status | python3 -m json.tool | grep -i '"id"\|"name"'
# id example: 120363xxxxxxxxxx@g.us → .env lo WHATSAPP_BRIDGE_TARGETS=120363...@g.us,<second>
```

## .env lo
```
WHATSAPP_MODE=bridge
WHATSAPP_BRIDGE_URL=http://whatsapp-bridge:3001/send
WHATSAPP_BRIDGE_TARGETS=120363xxxx@g.us,9198480xxxxx@s.whatsapp.net
```

## ⚠️ Important (ban risk taggadaniki)
- Spam cheyyaku: **roju 5-10 posts per group max**, same message 500 numbers ki pampaku
- Cold broadcast → WhatsApp ban chestundi. **Opt-in members** matrame (register appudu "WhatsApp lo updates kavali" checkbox)
- 30+ sec gap pettu posts madhya (`PUBLISH_RATE_LIMIT=30`)
- Business verify + WhatsApp Business API (Cloud API) unte inka safe — publisher.py lo `WHATSAPP_MODE=cloud_api` ready undi
