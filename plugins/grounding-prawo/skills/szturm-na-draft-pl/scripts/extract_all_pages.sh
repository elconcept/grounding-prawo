#!/usr/bin/env bash
# E0 szturmu: .docx -> Markdown CALEGO dokumentu (adeu --page all) + wersja z numerami linii.
#
#   bash extract_all_pages.sh DRAFT.docx [KATALOG_PRZEBIEGU]
#
# Tworzy w KATALOG_PRZEBIEGU (domyslnie katalog pliku) - nigdy nie nadpisuje <nazwa>.md autora:
#   <nazwa>.extract.md   pelny tekst z CriticMarkup (istniejace zmiany sledzone i komentarze widoczne)
#   <nazwa>.clean.md     tekst "zaakceptowany" (--clean-view) - baza kotwic plik:linia i clean_targets.py
#   <nazwa>.clean.nl.txt ta sama tresc z numerami linii (kotwice dla soczewek)
#
# Dlaczego --page all: adeu dzieli dokument na syntetyczne strony dlugosci kontekstu LLM, a domyslnie
# zwraca tylko strone 1. Czesciowy wyciag nie nadaje sie do apply (adeu go odrzuca) i gubi kotwice.
# Wersja adeu przypieta jak w redline-docx-pl (1.30.0) - podniesienie pinu to swiadoma decyzja.
set -euo pipefail
ADEU=(uvx --from adeu==1.30.0 adeu)
[ $# -ge 1 ] || { echo "uzycie: $0 DRAFT.docx [KATALOG]" >&2; exit 2; }
src="$1"
[ -f "$src" ] || { echo "BLAD: brak pliku $src" >&2; exit 2; }
case "$src" in *.docx) ;; *) echo "BLAD: adeu czyta tylko .docx (.odt/.doc -> soffice --convert-to docx)" >&2; exit 2;; esac
out="${2:-$(dirname "$src")}"
mkdir -p "$out"
stem="$(basename "$src" .docx)"

err="$(mktemp)"; trap 'rm -f "$err"' EXIT
"${ADEU[@]}" extract "$src" --page all -o "$out/$stem.extract.md" >"$err" 2>&1 || { cat "$err" >&2; exit 1; }
"${ADEU[@]}" extract "$src" --page all --clean-view -o "$out/$stem.clean.md" >"$err" 2>&1 || { cat "$err" >&2; exit 1; }

for f in "$out/$stem.extract.md" "$out/$stem.clean.md"; do
  if grep -qiE 'page [0-9]+ of [0-9]+' "$f"; then
    echo "BLAD: $f wyglada na wyciag czesciowy (page N of M) - sprawdz wersje adeu" >&2; exit 1
  fi
done
awk '{printf "%5d\t%s\n", NR, $0}' "$out/$stem.clean.md" > "$out/$stem.clean.nl.txt"

zmiany=$({ grep -oE '\{\+\+|\{--|\{~~' "$out/$stem.extract.md" || true; } | wc -l | tr -d ' ')
komentarze=$({ grep -oE '\{>>' "$out/$stem.extract.md" || true; } | wc -l | tr -d ' ')
echo "$stem: $(wc -l < "$out/$stem.clean.md" | tr -d ' ') linii | zmiany sledzone w pliku: $zmiany | komentarze: $komentarze"
if [ "$zmiany" != "0" ]; then
  echo "UWAGA: draft ma nieprzyjete zmiany sledzone - redline z przebiegu nalozy sie na nie. Ustal z autorem, czy baza to wersja przyjeta." >&2
fi
