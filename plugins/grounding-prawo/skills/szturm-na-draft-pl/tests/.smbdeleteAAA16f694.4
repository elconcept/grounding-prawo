#!/usr/bin/env bash
# Test dymny szturmu na syntetycznym pismie (bez danych klienta): cykl z shared/ARTEFAKTY-SPRAWY.md -
# DOCX w output z redline autora -> accept-all -> snapshot MD -> E5/E6 -> E7 (dwie rundy) -> jeden DOCX w output.
# Wymaga: uv/uvx (adeu==1.30.0, python-docx przez uv run), python3. Sieć tylko przy pierwszym pobraniu pakietów.
#   bash tests/smoke_test.sh [KATALOG_ROBOCZY]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SZ="$HERE/../scripts"
W="${1:-$(mktemp -d)}"
mkdir -p "$W/RUN/ustalenia" "$W/output" "$W/drafty/PISMO"
ADEU=(uvx --from adeu==1.30.0 adeu)
ok() { echo "OK   $*"; }
zle() { echo "ZLE  $*"; exit 1; }

uv run -q "$HERE/make_fixture.py" "$W/RUN/_fixture.docx"
# poprzednia sesja zostawila w output DOCX ze zmiana sledzona autora, ktorej nikt nie zaakceptowal
echo '[{"type":"modify","target_text":" z tej samej kamery.","new_text":" z tej samej kamery monitoringu.","comment":"autor"}]' > "$W/RUN/_autor.json"
"${ADEU[@]}" apply "$W/RUN/_fixture.docx" "$W/RUN/_autor.json" -o "$W/output/20260101_PISMO_v1.docx" --author "Autor" >/dev/null 2>&1
"${ADEU[@]}" accept-all "$W/output/20260101_PISMO_v1.docx" -o "$W/RUN/PISMO_v1.docx" >/dev/null 2>&1
bash "$SZ/extract_all_pages.sh" "$W/RUN/PISMO_v1.docx" "$W/RUN" >/dev/null
[ -s "$W/RUN/PISMO_v1.clean.md" ] && ok "E0 accept-all + extract" || zle "E0 extract"
cp "$W/RUN/PISMO_v1.clean.md" "$W/drafty/PISMO/20260102_PISMO_v2.md"
grep -q "kamery monitoringu" "$W/drafty/PISMO/20260102_PISMO_v2.md" && ok "snapshot MD zawiera zmiane autora" || zle "snapshot bez zmiany autora"

cp "$HERE/fixture_rejestry.json" "$W/RUN/rejestry.json"
cp "$HERE/fixture_ustalenia.json" "$W/RUN/ustalenia/01_test.json"
set +e
python3 "$SZ/synteza.py" "$W/RUN/ustalenia" --rejestry "$W/RUN/rejestry.json" \
  --md PISMO="$W/RUN/PISMO_v1.clean.md" -o "$W/RUN" > "$W/RUN/synteza.log"
rc=$?
set -e
[ $rc -eq 0 ] && ok "E5 synteza (exit 0)" || { cat "$W/RUN/synteza.log"; zle "E5 synteza exit $rc"; }

python3 - "$W/RUN/ustalenia.scalone.json" <<'EOF' || exit 1
import json, sys
G = json.load(open(sys.argv[1]))
g = {x["kotwica"]: x for x in G if x["klasa"] != "LOGIKA" or x["kotwica"] != "PISMO_v1.clean.md:7"}
oczek = {
    "PISMO_v1.clean.md:5": ("WPROWADZONE", "AUTO"),         # data wyroku z tresci, E1 + dowod, dwie soczewki
    "PISMO_v1.clean.md:7": ("WSTRZYMANE", "DECYZJA_AUTORA"), # dotyka faktu potwierdzonego
    "PISMO_v1.clean.md:9": ("ZABLOKOWANE", None),          # alternatywa wykluczona rejestrem
    "PISMO_v1.clean.md:11": ("ZABLOKOWANE", None),          # nowa liczba bez dowodu
    "PISMO_v1.clean.md:13": ("ZMIANA_DO_DECYZJI", "DECYZJA_AUTORA"),  # STRATEGIA
    "PISMO_v1.clean.md:15#1": ("WPROWADZONE", "AUTO"),      # klamra STYL, edycja 1 z 2
    "PISMO_v1.clean.md:25": ("WPROWADZONE", "AUTO"),        # ta sama klamra, edycja 2 (jedno ustalenie)
    "PISMO_v1.clean.md:21": ("ZABLOKOWANE", None),          # wykluczona alternatywa w innej formie gramatycznej
    "PISMO_v1.clean.md:23": ("WPROWADZONE", "REDAKCJA"),    # dopisanie karty akt jako zrodla (z dowodem)
}
bledy = 0
for k, (stan, naprawa) in oczek.items():
    x = g.get(k)
    if not x or x["stan"] != stan or (naprawa and x["naprawa"] != naprawa):
        print(f"ZLE  bramka {k}: oczekiwano {stan}/{naprawa}, jest {x and (x['stan'], x['naprawa'])}")
        bledy += 1
x = next((v for v in G if v["kotwica"] == "PISMO_v1.clean.md:7" and v["klasa"] == "LOGIKA"), None)
if not x or x["stan"] != "WSTRZYMANE":   # target czesciowo nachodzi na fakt potwierdzony
    print(f"ZLE  bramka czesciowe nachodzenie na fakt: {x and x['stan']}"); bledy += 1
if g["PISMO_v1.clean.md:5"]["pewnosc"] != 2:
    print("ZLE  deduplikacja: pewnosc != 2"); bledy += 1
if len(G) != 12:
    print(f"ZLE  edycji po deduplikacji {len(G)} != 12"); bledy += 1
r19 = [v for v in G if v["kotwica"] == "PISMO_v1.clean.md:19"]
if len(r19) != 2 or len({v["id"] for v in r19}) != 1 or any(v["stan"] != "WPROWADZONE" for v in r19):
    print(f"ZLE  regresja: dwie edycje z ta sama kotwica -> {[(v['id'], v['stan']) for v in r19]}"); bledy += 1
if g["PISMO_v1.clean.md:15#1"]["id"] != g["PISMO_v1.clean.md:25"]["id"]:
    print("ZLE  edycje jednego ustalenia maja rozne ID"); bledy += 1
if len({x["id"] for x in G}) != 10:
    print(f"ZLE  ustalen {len({x['id'] for x in G})} != 10"); bledy += 1
print("OK   E6 bramki i deduplikacja" if not bledy else "")
sys.exit(1 if bledy else 0)
EOF

# poprawki formatu na bazie, przed zmianami sledzonymi (fix_format nie widzi tekstu wewnatrz w:ins)
uv run -q "$SZ/fix_format.py" "$W/RUN/PISMO_v1.docx" --apply -o "$W/RUN/_fmt.docx" --json > "$W/RUN/format.json"
mv "$W/RUN/_fmt.docx" "$W/RUN/PISMO_v1.docx"
python3 -c "import json,sys; z=json.load(open(sys.argv[1]))['zmiany_niesledzone']; t={x['typ'] for x in z}; sys.exit(0 if {'NAGLOWEK_TEKST','PODKRESLENIE'}<=t else 1)" "$W/RUN/format.json" \
  && ok "E7 fix_format (naglowek z tekstem + podkreslenie)" || zle "fix_format nie znalazl wad formatu z fixture"

A="Szturm test"
"${ADEU[@]}" apply "$W/RUN/PISMO_v1.docx" "$W/RUN/edits.PISMO.redline.json" -o "$W/RUN/runda1.docx" --author "$A" >/dev/null 2>&1
# runda 2 naklada sie na redline rundy 1 (zmiany sesji kumuluja sie w jednym pliku)
echo '[{"type":"modify","target_text":"PISMO TESTOWE - STANOWISKO","new_text":"PISMO TESTOWE - STANOWISKO STRONY","comment":"[S-99 | STYL | AUTO] runda 2"}]' > "$W/RUN/edits.runda2.json"
"${ADEU[@]}" apply "$W/RUN/runda1.docx" "$W/RUN/edits.runda2.json" -o "$W/RUN/runda2.docx" --author "$A" >/dev/null 2>&1
ok "E7 adeu apply, dwie rundy"


cp "$W/RUN/runda2.docx" "$W/output/20260102_PISMO_v2.docx"
cmp -s "$W/RUN/runda2.docx" "$W/output/20260102_PISMO_v2.docx" && rm "$W/output/20260101_PISMO_v1.docx"
python3 "$SZ/weryfikuj_wynik.py" --redline "$W/output/20260102_PISMO_v2.docx" \
  --edits "$W/RUN/edits.PISMO.redline.json" "$W/RUN/edits.runda2.json" --katalog "$W/output" --drafty "$W/drafty/PISMO" \
  > "$W/RUN/weryfikacja.txt" \
  && ok "E7 struktura redline obu rund, placeholdery, brak PDF, brak DOCX w drafty" || { cat "$W/RUN/weryfikacja.txt"; zle "weryfikuj_wynik"; }
[ "$(ls "$W/output")" = "20260102_PISMO_v2.docx" ] && ok "output: jeden DOCX pisma" || zle "output: $(ls "$W/output")"
[ -z "$(ls "$W/drafty/PISMO" | grep -v '\.md$')" ] && ok "drafty: tylko MD" || zle "drafty: pliki inne niz MD"

"${ADEU[@]}" accept-all "$W/output/20260102_PISMO_v2.docx" -o "$W/RUN/nastepna_baza.docx" >/dev/null 2>&1
bash "$SZ/extract_all_pages.sh" "$W/RUN/nastepna_baza.docx" "$W/RUN" >/dev/null
B="$W/RUN/nastepna_baza.clean.md"
grep -q "14 marca 2024" "$B" && ok "nastepna sesja: poprawka AUTO przyjeta" || zle "brak poprawki AUTO"
grep -q "Wniosek dowodowy obejmuje porównawczego nagrania" "$B" && ok "regresja: obie edycje z ta sama kotwica przyjete" || zle "regresja: zgubiona edycja przy wspolnej kotwicy"
grep -q "strategię obrony" "$B" && ok "nastepna sesja: nieodrzucona DECYZJA_AUTORA przyjeta" || zle "DECYZJA_AUTORA zgubiona"
grep -q "STANOWISKO STRONY" "$B" && ok "nastepna sesja: zmiana rundy 2 przyjeta" || zle "zgubiona zmiana rundy 2"
grep -q "kamery monitoringu" "$B" && ok "zmiana autora z poprzedniej sesji zachowana" || zle "zgubiona zmiana autora"
python3 "$SZ/metryki_stylu.py" "$B" >/dev/null && ok "E4 metryki_stylu"
echo "WSZYSTKO OK ($W)"
