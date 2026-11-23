# Grounding Prawo — rebuild (2026-11-23)

**Status: ETAP 1 wykonany; referencyjne suity uruchomione, testy adaptowanego pluginu do podlaczenia; zaden nowy skill nie jest zatwierdzony.**

Nowa wersja ma byc budowana od zera. Poprzednia architektura generowanego `grounding-prawo` i oddzielnego `LEXMACHINA-CHAT` nie jest podstawa nowych decyzji projektowych. Istniejacy kod i archiwa to tylko material do selektywnego odczytu; historia Git pozostaje, bez kopiowania starego bundle jako nowego pluginu.

## Kanoniczne submoduly

- `vendor/packs/awesome-matematic-skills` — `matematicsolutions/awesome-matematic-skills-pl` (ORYGINALNY upstream MateMatic), pinned commit `7e15bbea11c2fb8862a965505d86a7d0de3fd92d`. Starego gitlinka nie dublujemy.
- `vendor/benchmarks/lawbenchmark` — `apiotrowski-afk/lawbenchmark`, pinned commit `c16ae2ea9ce8ac31d9f1eee0b3acb6d230995b9b`.

Tylko te submoduly sa potrzebne do referencyjnej bramki. Nie inicjalizujemy bez potrzeby pozostalych 74 katalogow vendor.

## Twarda zasada zmiany

1. Przed **kazda** zmiana SKILL.md, modulu, routera, patcha, selekcji albo buildera: wykonaj komplet MateMatic (oryginalne pytest + fixtures, grounding, let-it-be, marketplace, audyt cytowan, attribution, legal accuracy, preflight, DOCX engine) i LawBenchmark (160 odpowiedzi/klucze/karty, judge comparisons, evaluation of verification layer). Zapamietaj wynik i przypiete SHA.
2. Po zbudowaniu faktycznego pluginu przez `scripts/build.py` uruchom na nim wszystkie dostepne testy komponentow, walidacje manifestow i martwych odwolan. Testy wykonane w katalogu `vendor/` nie zastępuja testu po overlayu, a workflow dziala tylko wtedy, gdy zielone sa wszystkie te zadania.
3. Dodatkowo wykonaj **rzeczywisty benchmark A/B tego samego modelu**: BASE = bez nowego skilla, CANDIDATE = z nowym skladem skilli; te same pytania i ustawienia, prawnicza ocena przez niezaleznego sedziego oparta na kluczach LawBenchmark. Nie przeliczaj cudzych 160 odpowiedzi zamiast uruchomienia wlasnego pipeline.
4. Przed modyfikacja materialu spraw i skilli zapisz wynik bazowy; po zmianie uruchom identyczny pipeline, wykryj regresje. Brak dostepu do modelu, sedziego, pelnych zrodel albo wyniku = BLOCKED, nigdy PASS.
5. Dopiero po obu rzeczywistych przebiegach i braku regresji commit/push bezposrednio na `main`. Zero PR, branchy i worktree. Nie przenos tajnych danych spraw do tego publicznego repozytorium.
6. Nie zadeklaruj "testy zaliczone", kiedy jedynie workflow odtworzyl historyczne karty. Publikowany LawBenchmark jest zbiorem kalibracyjnym, nie niezaleznym holdoutem.

`.github/workflows/benchmark-gate.yml` uruchamia suity upstream oraz LawBenchmark, a etap `post-overlay` po nich musi zbudowac i przetestowac dokladnie `plugins/grounding-prawo`. Do czasu podlaczenia LIVE A/B nadal nie wolno twierdzic, ze udowodniono poprawe jakosci odpowiedzi modelu.

## Zakres nowego pluginu

- Jeden prywatnie uzywany plugin ChatGPT Chat, trzy tryby: **AUDYT**, **NAPISZ**, **DOSKONAL**.
- Jedyna bramka prawna: `lex.xlap.pl/mcp`. Wczytuj istniejace sidecary Markdown w `elconcept/legal`, nie uruchamiaj ponownie OCR.
- Bez automatycznego uprzywilejowania wersji urzedowej; kazde twierdzenie oceniamy wedlug materialu, rozdzielajac obserwacje, wersje stron, interpretacje i hipotezy.
- Pierwszy wybór istniejącego skilla ze zrodel MateMatic, minimalna adaptacja tylko na podstawie mierzalnej poprawy. Zadnej reimplementacji gotowych fixtures.
- Oddzielaj kontrole wlasciwego przepisu, wersji czasowej, tozsamosci orzeczenia, doslownego cytatu i poparcia tezy. Nie zamieniaj czesciowego sprawdzenia w zielony PASS.
- Z kazdej iteracji zachowaj poprzednie rozstrzygniete RED i oceniaj regresje v1/v2/v3 oraz DOCX.
- Nie instaluj, nie publikuj ani nie promuj nieprzetestowanego bundle.

## Kolejne etapy

A. Wpiac i faktycznie uruchomic dwie referencyjne suity w CI. B. Zbudowac adapter LIVE A/B dla konkretnego harnessu i jego oceniajacego modelu, bez tworzenia fikcyjnego benchmarku. C. Dopiero po zaliczeniu pelnej bramki wycofac stare skille/plugin i zbudowac nowe kanoniczne wejscie; jedna zmiana, pelna ewaluacja, commit, kolejna zmiana. D. Zwalidowac instalacje i E2E w Chat, a nie jedynie poprawny manifest.
