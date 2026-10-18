#!/usr/bin/env bash
# Tor jako rotator IP dla SAOS i innych serwisów (CGNAT: zewnętrzne IP współdzielone z innymi abonentami
# bywa blokowane). Instaluje Tora, jeśli go brak (kontener HolyClaude: passwordless sudo; instalacja
# nie przetrwa przebudowy kontenera), i uruchamia SOCKS5 na 127.0.0.1:9050. Idempotentny.
# Użycie: bash shared/scripts/tor_rotator.sh  (tylko kontener HolyClaude na NAS: CGNAT blokuje SAOS, orzeczenia.ms, sn.pl przy webwright),
# a ręcznie: curl --socks5-hostname "r$RANDOM:p$RANDOM@127.0.0.1:9050" <url>  (losowe dane = nowy obwód).
set -euo pipefail
if ! command -v tor >/dev/null 2>&1; then
  sudo -n apt-get update -qq >/dev/null
  sudo -n DEBIAN_FRONTEND=noninteractive apt-get install -y -qq tor >/dev/null
fi
if (exec 3<>/dev/tcp/127.0.0.1/9050) 2>/dev/null; then
  echo "tor: SOCKS5 127.0.0.1:9050 już działa"; exit 0
fi
DATA="${TOR_DATA_DIR:-/tmp/tor-data}"; LOG="${TOR_LOG:-/tmp/tor.log}"
mkdir -p "$DATA"; chmod 700 "$DATA"
tor --SocksPort 9050 --DataDirectory "$DATA" --Log "notice file $LOG" --RunAsDaemon 1
for _ in $(seq 1 60); do grep -q "Bootstrapped 100" "$LOG" 2>/dev/null && break; sleep 2; done
if grep -q "Bootstrapped 100" "$LOG"; then
  echo "tor: gotowy (SOCKS5 127.0.0.1:9050)"
else
  echo "tor: brak bootstrapu, zob. $LOG" >&2
  exit 1
fi
