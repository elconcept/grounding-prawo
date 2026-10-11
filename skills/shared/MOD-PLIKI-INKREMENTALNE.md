# MOD-PLIKI-INKREMENTALNE - jak przebieg draftowania lub analizy zapisuje pliki

Reguła kanoniczna (decyzja autora repo abogada, 10.10.2026). Obowiązuje każdy skill, który draftuje pismo
albo robi analizę w teczce sprawy: `szturm-na-draft-pl`, `pisma-procesowe-v3`, `pisma-proste-v2`,
`patron-pismo-procesowe-pl`, rodzina IURA, `zawiadomienie-o-przestepstwie`, `analiza-sadowa-v6`,
`analizator-dowodow-v3`, `chronologia-sprawy-v1`, `subsumpcja-pl`, skille kontroli tekstu i pozostałe.

Cel: mniej szumu. Kolejny przebieg nie tworzy kolejnego logu, recapu ani raportu obok poprzednich - dopisuje
do plików, które już istnieją.

## Trzy rodzaje plików

| Rodzaj | Gdzie | Zasada |
|---|---|---|
| **Wersja wynikowa** pisma lub analizy | `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.docx` (albo `.md`) | Jedyny plik, który każdy przebieg tworzy na nowo: kolejna wersja z podbitym `vN`. |
| **Pliki inkrementalne** (prefiks `_`) | `drafty/<pismo>/_*.md` (dla pisma), `analiza/_*.md` (dla sprawy) | Tworzone raz, potem **tylko uzupełniane** dopiskiem przebiegu. Nigdy kopia, nigdy `_v2`, nigdy nowy plik z datą. |
| **Pliki jednorazowe** przebiegu | `_robocze/` sprawy | Workspace modelu: wyciągi, JSON-y, raporty skilli, redline'y, notatki robocze. Nikt ich nie czyta - z nich model zbiera esencję do plików inkrementalnych. |

## Pliki inkrementalne

Standardowe (nazwy kanoniczne w repo):
- `_PRZEBIEGI.md` - rejestr przebiegów: data, cel, wynik (która wersja), decyzje autora, wskaźnik do `_robocze/`.
- `_SUBSUMPCJA*.md` - rejestr stały sprawy (tezy, przesłanki, dowody, kotwice; format w `szturm-na-draft-pl/references/rejestr-staly.md`).
- `_brief.md`, `_podsumowanie.md`, `_dokumenty.md` - pliki rdzeniowe sprawy w `analiza/`.

Nowy plik inkrementalny wolno założyć, gdy przebieg wytwarza **inny rodzaj informacji**, który będzie
uzupełniany w kolejnych przebiegach - np. `_FINDINGS.md` (lista nieprawidłowości), `_PYTANIA.md` (pytania do
autora), `_MAPA_KRZYWD.md`, `_HARDGATE.md`. Dobierz zestaw do pisma lub analizy. Nie zakładaj pliku
inkrementalnego na jednorazową treść - ta idzie do `_robocze/`.

Format dopisku: sekcja z datą i numerem przebiegu (`## Przebieg 3 - 2026-10-03`), na końcu pliku (rejestry,
logi) albo w miejscu tematycznym z adnotacją daty (pliki stanu, np. `_FINDINGS.md`: pozycja zmienia status,
nie jest duplikowana). Pozycje mają stałe ID (`[n]`, `F-12`), żeby kolejne przebiegi mogły je aktualizować.

## Przykład (od autora)

| Przebieg | Nowa wersja | Pliki inkrementalne | `_robocze/` |
|---|---|---|---|
| 1 | `20261001_pismo_procesowe_v1.docx` | utworzone `_SUBSUMPCJA.md`, `_PRZEBIEGI.md` | wyciągi, raporty skilli |
| 2 | `20261002_pismo_procesowe_v2.docx` | dopisano do `_SUBSUMPCJA.md`, `_PRZEBIEGI.md` | j.w. |
| 3 | `20261003_pismo_procesowe_v3.docx` | utworzono `_FINDINGS.md` (wydzielona lista nieprawidłowości); dopisano do `_SUBSUMPCJA.md`, `_PRZEBIEGI.md` | j.w. |
| 4 | `20261004_pismo_procesowe_v4.docx` | dopisano do `_SUBSUMPCJA.md`, `_PRZEBIEGI.md`, `_FINDINGS.md` | j.w. |

## Zakazy

- Plik logu, recapu, „summary”, „finding_przebiegN”, „LOG_PRZEBIEGU”, „issues”, raportu tury itp. poza
  `_robocze/` - zamiast tego dopisek do pliku inkrementalnego.
- Katalogi `PRZEBIEG_*`, `RUN/`, `out/` w `analiza/` lub `drafty/`. Katalog roboczy narzędzia (gdy narzędzie
  wymaga katalogu): `_robocze/rrrrMMdd_<pismo>__<narzędzie>/`.
- Kopie „(2)”, „_kopia”, `__dup`, `.md.md` - duplikaty się usuwa.

## Koniec przebiegu - kontrola

1. Esencja z `_robocze/` jest w plikach inkrementalnych (ustalenia, decyzje, pytania, stan kotwic).
2. Nowe pliki poza `_robocze/`: tylko wersja wynikowa (+ ewentualnie nowy plik inkrementalny, z jednym
   zdaniem uzasadnienia w `_PRZEBIEGI.md`).
3. `_PRZEBIEGI.md` ma wpis przebiegu ze wskaźnikiem do plików w `_robocze/`.
