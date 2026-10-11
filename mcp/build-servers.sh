#!/usr/bin/env bash
# Przebudowa mcp/servers/*.cjs (pojedyncze pliki bez node_modules) ze submodulow mcp/mcp-*.
# Uzycie: bash mcp/build-servers.sh [isap saos ...]
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p servers
for s in ${@:-eu-compliance eu-sparql eureka isap krs nsa saos}; do
  src="mcp-$s"
  [ -d "$src/node_modules" ] || (cd "$src" && npm ci --no-audit --no-fund)
  npx --yes esbuild@0.28 "$src/src/index.ts" --bundle --platform=node --format=cjs \
    --target=node18 --log-level=warning --outfile="servers/$s.cjs"
  echo "servers/$s.cjs <- $src $(node -p "require('./$src/package.json').version")"
done
# repertorium: ESM (stan limitu w import.meta.url -> servers/.limit-state.json)
npx --yes esbuild@0.28 repertorium-mcp/index.js --bundle --platform=node --format=esm --target=node18 \
  --log-level=warning --banner:js="import { createRequire as __cr } from 'node:module'; const require = __cr(import.meta.url);" \
  --outfile=servers/repertorium.mjs
echo "servers/repertorium.mjs <- repertorium-mcp"
