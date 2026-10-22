# Rejestr stały sprawy - format dopisków E9

Każda sprawa ma pięć stałych plików w `00_sprawy/<sprawa>/analiza/`. Przebieg szturmu **dopisuje** do nich
turę. Nie tworzy nowego katalogu z raportami per skill (nikt ich potem nie czyta), nie tworzy kopii
„(2)”, „(3)” ani wersji w innym miejscu: jeden plik, jedno miejsce.

E0 czyta te pliki **przed** draftem: stan sprawy, decyzje autora, otwarte kotwice, numer ostatniej
tury i ostatniej pozycji `[n]`. Jeżeli plików nie ma, E0 pyta autora, czy je założyć (szablony niżej).

| Plik | Co dopisuje przebieg |
|---|---|
| `_SUBSUMPCJA_LOG_PRZEBIEGU.md` | `## TURA N - <co> (<data>)` + `## STATUS TURY N` |
| `_SUBSUMPCJA_FINDINGS.md` | pozycje `### [n]` + `## TURA N - ZMIANY W PISMACH` + karta ocena-outputu-pl z linią REWIZJA + pytania do autora |
| `_SUBSUMPCJA_GROUNDING.md` | sekcja tury: przepisy (t.j., gdzie zweryfikowano), orzecznictwo, cytaty, blokady |
| `_SUBSUMPCJA_ADVERSARIAL.md` | `## ADDENDUM - tura N`: werdykty rund, ciosy przeciwnika i ich stan, `WERDYKT PO TURZE N` |
| `_SUBSUMPCJA.md` | `## ANEKS - tura N`: wpływ tury na sylogizm + aktualny status w nagłówku pliku |

Pliki robocze przebiegu (wyciągi `.clean.md`, `ustalenia/*.json`, `edits.*.json`, `raport_synteza.md`,
REDLINE, obrazy, skrypty pomiarowe) idą do `<sprawa>/_robocze/<rrrrMMdd>_<pismo>__szturm/`. Rejestr odsyła do
nich ścieżką; nie kopiuje ich treści. Zasada ogólna: `shared/ARTEFAKTY-SPRAWY.md`.

## Szablony dopisków

### _SUBSUMPCJA_LOG_PRZEBIEGU.md

```markdown
## TURA N - szturm na draft: <DOKUMENT(Y)> (<dd.mm.rrrr>)

Polecenie: „<dosłownie, jedno zdanie>”. Stawka: <S|M|L>. Teza nadrzędna: <jedno zdanie>.
Wejście: <draft.docx> (+ <załączniki>), akta <katalog>, rejestry: fakty_potwierdzone <k>, decyzje_autora <k>.
Soczewki: E1 <lista> | E2 <lista> | E3 <lista> | E4 <lista>. Nieuruchomione i dlaczego: <…>.
Wynik: ustaleń <x> -> po deduplikacji <y>; WPROWADZONE <a>, ZMIANA_DO_DECYZJI <b>, PYTANIE/WSTRZYMANE <c>, ZABLOKOWANE <d>.
Rundy E8: <r>; wynik_zbiorczy <v1> -> <vN>; stan końcowy <GOTOWE|NIEGOTOWE>; pytania zadane/odpowiedziane <k>/<m>.
Pliki: historia `drafty/<pismo>/<rrrrMMdd>_<nazwa>_vN.md`, DOCX tylko najnowszej wersji oraz jego
kopia w `output/`; robocze: `_robocze/<rrrrMMdd>_<pismo>__szturm/` (REDLINE, wyciągi, JSON-y).

## STATUS TURY N: ZAKOŃCZONA - <y> pozycji [p]-[q]. Łącznie w sprawie: <q> pozycji. Obowiązuje: <plik(i)> (do decyzji autora: <k> pytań w FINDINGS, tura N).
```

### _SUBSUMPCJA_FINDINGS.md

```markdown
### [n] <S-ID>: <klasa> <waga> - <jedno zdanie ustalenia> (<soczewki>)
Kotwica: <plik:linia>. Dowód: <…>. Działanie: <AUTO|REDAKCJA|DECYZJA_AUTORA|DOWOD> -> <stan>.

## TURA N - ZMIANY W PISMACH (zmiany śledzone z komentarzem przy każdej)
- Snapshot `drafty/<pismo>/<wersja>.md`; DOCX `legal/output/<wersja>.docx`: <k> zmian (w:ins <i> / w:del <d>), autor „<etykieta>”.
- Zmiany nieśledzone (fix_format.py): <lista: akapit, zmiana>.
- Karta ocena-outputu-pl: <WARSTWA 1 / 2 / KOTWICE / DECYZJA>
  REWIZJA #<r>: decyzja <X> -> <Y>. <uzasadnienie albo odrzucone podniesienie>.

Pytania do autora (tylko DECYZJA_AUTORA i DOWOD):
1. <S-ID> …
```

### _SUBSUMPCJA_GROUNDING.md

```markdown
## Tura N - grounding <DOKUMENT> (<data>)
Przepisy: <art. …> - ✅ t.j. <ELI> (ustawy/ELI, pobrano <data>) | ❌ <…>
Orzecznictwo: <sygn.> - data i skład z treści (<źródło>, cache <data>) | NIEPEWNE: <konektor offline, brak cache>
Cytaty z akt: <k> sprawdzonych, <m> 🔴 (-> S-ID)
Blokady: <co zostało otwarte i dlaczego>
```

### _SUBSUMPCJA_ADVERSARIAL.md

```markdown
## ADDENDUM - tura N (<data>)
Werdykty rund: v1 <FAIL|WYŚLIJ_WARUNKOWO|PASS> (<score>) -> vN <…>.
Ciosy przeciwnika i stan: 1. <cios> - unieszkodliwiony / osłabiony / otwarty (S-ID).
### WERDYKT PO TURZE N: **<…>** - warunki: <…>
```

### _SUBSUMPCJA.md

```markdown
## ANEKS - tura N (<data>)
Wpływ na sylogizm: przesłanka większa <bez zmian | …>; mniejsza <…>; wniosek <…>.
Nowe słabe ogniwa: <…>. Zamknięte: <…>.
```
(i zaktualizuj linię statusu w nagłówku pliku)

## Commit

Po dopiskach: `git add` **jawnie** pięć plików rejestru, nowe wersje dokumentów i katalog przebiegu.
Nigdy `git add -A` w repozytorium z aktami - nieśledzone katalogi dowodów trafiłyby do historii.
