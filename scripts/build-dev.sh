#!/usr/bin/env bash
# build-dev.sh - przygotowanie checkoutu po `git clone` albo `git pull` na nowym hoście.
#
#   scripts/build-dev.sh            submoduły na przypiętych commitach + build, walidacja, lint
#   scripts/build-dev.sh --remote   jak wyżej, ale submoduły podbite do upstreamu (jak job upstream-bump)
#   scripts/build-dev.sh --no-build tylko submoduły
#
# Prywatne submoduły (the-ocr, mcp-ip-rotator, mcp-repertorium) wymagają dostępu do organizacji elconcept
# (`gh auth login` + `gh auth setup-git` albo klucz SSH). Brak dostępu nie przerywa: submoduł jest pomijany
# z ostrzeżeniem. Ustawia też `submodule.recurse=true`, więc kolejne `git pull` aktualizuje submoduły samo.
set -uo pipefail

remote="" build=1
for a in "$@"; do
  case "$a" in
    --remote) remote="--remote" ;;
    --no-build) build=0 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "nieznana opcja: $a" >&2; exit 2 ;;
  esac
done

cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 1
git config submodule.recurse true
git submodule sync -q --recursive

export GIT_TERMINAL_PROMPT=0
skipped=()
for p in $(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  git submodule update -q --init --recursive $remote -- "$p" 2>/dev/null || skipped+=("$p")
done
echo "submoduły: $(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | wc -l), pominięte: ${#skipped[@]}"
for p in "${skipped[@]}"; do echo "  bez dostępu: $p" >&2; done

[ "$build" = 1 ] || exit 0
python3 -c 'import yaml' 2>/dev/null || pip install -q --user pyyaml 2>/dev/null || pip install -q --break-system-packages pyyaml
python3 scripts/build.py && python3 scripts/validate_marketplace.py && python3 scripts/lint_refs.py
