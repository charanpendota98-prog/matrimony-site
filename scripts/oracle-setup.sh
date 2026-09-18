#!/usr/bin/env bash
# MANA VIVAHA — Oracle VM first-time setup (docker + caddy + git + firewall 80/443)
# Run on FRESH Ubuntu 22.04 VM as ubuntu user:
#   curl -sSL https://raw.githubusercontent.com/charanpendota98-prog/matrimony-site/arena/01a0aaf1-matrimony-site/scripts/oracle-setup.sh | bash
# Idempotent — malli run chesina safe. Secrets emi adagadu (aa step tarvata).
set -euo pipefail

echo "== 1/4 apt: git + caddy + iptables =="
sudo apt update
sudo apt install -y git caddy iptables-persistent

echo "== 2/4 docker =="
if ! command -v docker >/dev/null 2>&1; then
    curl -fsSL https://get.docker.com | sh
else
    echo "docker already installed"
fi
sudo usermod -aG docker "$USER" || true

echo "== 3/4 firewall: open 80 + 443 =="
sudo iptables -C INPUT -p tcp --dport 80 -j ACCEPT 2>/dev/null \
    || sudo iptables -I INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -C INPUT -p tcp --dport 443 -j ACCEPT 2>/dev/null \
    || sudo iptables -I INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

echo "== 4/4 versions =="
docker --version
caddy version
git --version

echo ""
echo "OK DONE — logout + login cheyandi (docker group kosam): exit → ssh malli."
echo "Tarvata deploy: git clone + .env + docker compose (DEPLOY-GUIDE-TELUGU.md Step 4)."
