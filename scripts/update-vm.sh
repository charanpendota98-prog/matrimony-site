#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# 💍 మనవివాహం — VM UPDATE (one command)
# ═══════════════════════════════════════════════════════════════════
# VM (Oracle, manavivaha.in) meeda run cheyandi:
#
#   bash update-vm.sh
#
# Em chestundi:
#   1. Data backup (backend/*.json + .env) — timestamp tar
#   2. Kotha code: kotha repo (shubhalagnam) + branch (arena/01a0b4e9-shubhalagnam)
#   3. Frontend image rebuild MATRAME (backend volume-mounted — rebuild avvadu, fast)
#   4. Containers restart + health check
#
# Data (data_db.json, payments, referral wallet...) — volume lo safe, touch cheyyam.
# Rollback: `bash update-vm.sh rollback`  (last backup nunchi data restore)
# ═══════════════════════════════════════════════════════════════════
set -uo pipefail

REPO_NEW="https://github.com/charanpendota98-prog/shubhalagnam.git"
BRANCH="arena/01a0b4e9-shubhalagnam"
TS=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="vm-backups"
STAMP="[$(date +%H:%M:%S)]"

say() { echo -e "$STAMP $1"; }

# ---- 0. clone dir detect (script ni repo lopala unna run chestaru) ----
cd "$(dirname "$0")/.." || { say "❌ repo dir dorakaledu"; exit 1; }
say "📁 Repo dir: $(pwd)"

mkdir -p "$BACKUP_DIR"

# ---- rollback mode ----
if [ "${1:-}" = "rollback" ]; then
    LATEST=$(ls -1t "$BACKUP_DIR"/data-*.tar.gz 2>/dev/null | head -1)
    [ -z "$LATEST" ] && { say "❌ backup file levdu"; exit 1; }
    say "↩️ Restoring: $LATEST"
    tar xzf "$LATEST" || { say "❌ restore fail"; exit 1; }
    docker compose -f docker-compose.yml -f docker-compose.prod.yml restart backend frontend
    say "✅ Data restore aindi + containers restart"
    exit 0
fi

# ---- 1. DATA BACKUP (mundu — eppudu) ----
say "💾 1/5 Data backup..."
tar czf "$BACKUP_DIR/data-$TS.tar.gz" \
    backend/*.json backend/*.jsonl .env 2>/dev/null || true
[ -f "$BACKUP_DIR/data-$TS.tar.gz" ] && say "   ✅ backup: $BACKUP_DIR/data-$TS.tar.gz ($(du -h "$BACKUP_DIR/data-$TS.tar.gz" | cut -f1))" \
    || say "   ⚠️ backup file raledu (data files levu anukunta — proceed)"

# ---- 2. KOTHA CODE ----
say "⬇️ 2/5 Kotha code (kotha repo + branch)..."
# remote switch (pata repo: matrimony-site → kotha repo: shubhalagnam)
CUR_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ "$CUR_URL" != "$REPO_NEW" ]; then
    say "   remote switch: $CUR_URL → $REPO_NEW"
    git remote set-url origin "$REPO_NEW" 2>/dev/null || git remote add origin "$REPO_NEW"
fi
git fetch origin "$BRANCH" || { say "❌ git fetch fail (internet/permissions check)"; exit 1; }
# tracked files local mods (audit logs lanti) — discard (backup lo unnayi).
# -B: local branch ni FETCH_HEAD ki set (untracked .env + gitignored data SAFE).
git checkout -f -B "$BRANCH" FETCH_HEAD
say "   ✅ code: $(git rev-parse --short HEAD) — $(git log -1 --format=%s | head -c 70)"

# ---- 3. FRONTEND REBUILD (backend volume-mounted — rebuild avvadu) ----
say "🔨 3/5 Frontend image rebuild (package.json same → npm ci cached, fast)..."
if ! docker compose -f docker-compose.yml -f docker-compose.prod.yml build frontend; then
    say "❌ frontend build fail — logs chudandi. Pata version inka nadustundi (down avvaledu)."
    exit 1
fi

# ---- 4. RESTART ----
say "🔄 4/5 Containers up..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d || { say "❌ up fail"; exit 1; }

# ---- 5. HEALTH CHECK ----
say "🩺 5/5 Health check (30s wait)..."
sleep 30
OK=0
for i in 1 2 3 4 5 6; do
    if curl -sf --max-time 10 http://localhost:8000/api/health >/dev/null 2>&1; then OK=1; break; fi
    say "   wait... ($i)"
    sleep 15
done
if [ "$OK" = "1" ]; then
    say "✅ Backend OK"
else
    say "❌ Backend health fail — logs: docker compose -f docker-compose.yml -f docker-compose.prod.yml logs --tail 50 backend"
    say "   Data backup unnadi: $BACKUP_DIR/data-$TS.tar.gz (rollback: bash update-vm.sh rollback)"
    exit 1
fi

FR_OK=0
for i in 1 2 3 4 5 6 7 8; do
    if curl -sf --max-time 10 -o /dev/null http://localhost:3000/; then FR_OK=1; break; fi
    sleep 10
done
[ "$FR_OK" = "1" ] && say "✅ Frontend OK" || say "⚠️ Frontend inka warm-up lo undocchu — 2-3 nimishalu tarvata https://manavivaha.in chudandi"

echo ""
say "🎉 UPDATE COMPLETE!"
say "   → https://manavivaha.in (phone lo cache clear chesi reload: chrome://... leda private tab)"
say "   → Kotha features: pricing minimal, మనవివాహం branding + logo, referral leaderboard LIVE"
say "   → Problem vaste: bash update-vm.sh rollback"
