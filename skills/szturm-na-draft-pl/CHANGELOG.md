# Changelog - szturm-na-draft-pl

## 2026-10-10 - pliki inkrementalne
- Zapis według `shared/MOD-PLIKI-INKREMENTALNE.md`: katalog roboczy `RUN` = `_robocze/<rrrrMMdd>_<pismo>__szturm/`
  (zamiast `analiza/PRZEBIEG_<data>/`), REDLINE w `RUN`, wersja czysta `drafty/<pismo>/<rrrrMMdd>_<nazwa>_vN.docx`,
  dopisek przebiegu do `drafty/<pismo>/_PRZEBIEGI.md` obok tury w rejestrze stałym.

## 1.2.0 (2026-09-29)

Poprawki z testu akceptacyjnego §8 na CASE1 (TK6, ekspertyza v8; wynik: 5 z 6 kryteriów, 4. częściowo -
kotwica R5 czeka na decyzję autora; `00_sprawy/inwigilacja_zniszczenie_mienia_vs_MG/analiza/PRZEBIEG_20260928_SZTURM/00_AKCEPTACJA_P8.md`):
- `edycje`: jedno ustalenie z kilkoma edycjami (także w drugim dokumencie), jedna linia raportu, wspólne ID.
- `weryfikuj_wynik.py`: komentarze liczone po `w:commentReference`; TK6 z 25.09 miał 31 osieroconych wpisów
  w comments.xml, które zawyżały licznik; kopia z zastosowanymi zmianami nie może mieć żadnych wpisów.
- Raport: pytanie bez zmiany tekstu opisane jako „do rozstrzygnięcia przez autora”, nie „brak dowodu”.

## 1.1.0 (2026-09-28)

- Decyzja autora (odpowiedź na pytanie 1): szturm tworzy jednocześnie REDLINE (zmiany śledzone)
  i kopię z zastosowanymi WSZYSTKIMI zmianami, także DECYZJA_AUTORA. Kopia = `sanitize --accept-all`
  na REDLINE. Wycofane odstępstwo z 1.0.0 (wersja czysta bez DECYZJA_AUTORA).

## 1.0.1 (2026-09-28)

Trzy dziury w bramkach E6 wykryte przeglądem i potwierdzone testem przed poprawką:
- target zahaczający o brzeg faktu potwierdzonego (np. „z dźwiękiem w dniu …”) przechodził -
  teraz przecięcie zakresów w tekście dokumentu (fallback: wspólny brzeg > 6 znaków);
- `wyklucza` dopasowywane dosłownie („mikrofon mógł być wyłączony” omijało „wyłączony mikrofon”),
  a regex `mog…` nie łapał „mógł” - teraz rdzenie słów i `m[oó]g`, plus „być może”, „mógł być”;
- dopisanie karty akt jako źródła (REDAKCJA FAKT_BEZ_ZRODLA) było blokowane - blokada tylko dla
  zmiany/usunięcia istniejących sygnatur, kart i kwot; dopisanie wymaga tokenu w `dowod`.
- `--poprzednie`: stałe ID po target_text, nie po kotwicy z nazwą pliku (TK7 -> TK8 zmienia kotwicę).
- Test dymny: 3 nowe przypadki; SKILL.md: `fix_format.py` ustępuje decyzjom autora o formacie.

## 1.0.0 (2026-09-28)

Pierwsza wersja wg `dokumentacja/06-PLAN-SKILL-SZTURM-NA-DRAFT.md`.

- Workflow E0-E9, bramka kosztu S/M/L, rejestr stały zamiast katalogu raportów.
- `synteza.py`: bramki E6 i twarde zakazy wymuszone kodem (fakty potwierdzone, decyzje autora,
  wykluczone alternatywy, liczby bez źródła, sygnatury/karty/kwoty poza AUTO, konflikty kotwic).
- Odstępstwo od planu (§3 pkt 2): wersja czysta przyjmuje tylko AUTO i REDAKCJA. Zmiany
  DECYZJA_AUTORA zostają wyłącznie w REDLINE jako śledzone - `sanitize --accept-all` przyjąłby je
  bez autora. Stąd trzy pliki edycji: `edits.<DOK>.json`, `.decyzje.json`, `.redline.json`.
- `clean_targets.py`: adeu 1.30.0 dopasowuje markdown dosłownie (`**` w targecie wstawia gwiazdki
  do Worda) i odrzuca cały pakiet przy jednej nietrafionej edycji - zmierzone 28.09.
- `fix_format.py` odtwarza ręczną korektę formatu ekspertyzy v9 -> v10 z 28.09: 14 akapitów
  z nagłówka (11 z tekstem + 3 puste) i 17 podkreśleń (16 + 1 ujawnione po zdjęciu nagłówka).
- `metryki_stylu.py`: pauzy i podkreślenia zgodne z pomiarem 28.09 co do sztuki; podziału na zdania
  z 28.09 (ręczny, bez skryptu) nie da się odtworzyć - skrypt ustala nową, stałą bazę porównań.
- `tests/smoke_test.sh`: syntetyczne pismo (bez danych klienta), E0 -> E7 i kontrola wyniku.
- Kryteria akceptacji §8 (przebieg na CASE1) - NIE uruchomione; wymagają kopii rejestru i akt
  poza `cases/` oraz zgody autora (stawka L, materiał objęty tajemnicą).
