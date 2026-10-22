---
name: pisz-po-polsku
description: 'Redakcja tekstów po polsku: naturalnie, konkretnie, bez manier stylu AI, z zachowaniem faktów, cytatów, przepisów i sygnatur. Nie zmienia petitum, zarzutów ani ustaleń faktycznych.'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `ustawy`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# Pisz po polsku

## Zawiadomienie pokrzywdzonego — pełnia opisu

Przy zleconej recenzji zawiadomienia stosuj `shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md`:
rola skutków i szczegółów. Pytaj o konkretne doznania, słowa, czas, nasilenie i wpływ na życie,
gdy autor podał skrót; nie dopisuj odpowiedzi. Zachowaj obszerność potrzebną do przedstawienia
całej krzywdy i epizodów. Usuwaj puste powtórzenia, nie fakty, emocje i odrębne skutki.
Sama korekta językowa nie uruchamia pełnej recenzji ani nie rozszerza zlecenia na inne pisma.


Jeden skill redakcji polskiego tekstu. Zastępuje `humanizer-pl`, `patron-pisz-po-ludzku` i `naturalne-pisanie`.
Poprawia sposób wypowiedzi, nigdy treść stanowiska.

## Zasada nadrzędna: minimalna potrzebna ingerencja

Najpierw wykonaj polecenie użytkownika. Potem poprawiaj tylko to, co realnie pogarsza tekst.
Zachowuj trafne, charakterystyczne sformułowania autora. Fragment naturalny i precyzyjny zostaw bez zmian;
brak zmiany jest prawidłowym wynikiem redakcji. Nie obiecuj niewykrywalności dla detektorów AI.

## Reguły twarde (zawsze)

- Zachowaj bez zmian: daty, kwoty, numery przepisów, sygnatury, cytaty, nazwy własne, terminologię prawną.
- Zachowaj siłę twierdzeń: nie osłabiaj kategorycznego sformułowania i nie wzmacniaj ostrożnego.
- Nie wymyślaj faktów, cytatów, źródeł, danych ani doświadczeń autora.
- Nie humanizuj przez celowe błędy, literówki ani przypadkowe kolokwializmy.
- Nie zastępuj naturalnego słowa rzadszym synonimem dla pozornej różnorodności.
- Nie ruszaj petitum, zarzutów, wniosków dowodowych ani ustaleń faktycznych w piśmie. Redagujesz uzasadnienie i opis, nie stanowisko.
- W zawiadomieniu o przestępstwie nie usuwaj, nie łagodź i nie uogólniaj danych o zdrowiu, intymnych ani innych wrażliwych danych autora i osób trzecich (`shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md`).

Przy redakcji pisma wczytaj `shared/STYLE.md`; jego rejestr formalny doprecyzowuje poniższe tryby.

## Tryby

| Tryb | Kiedy | Co robisz |
|---|---|---|
| Redakcja | użytkownik daje tekst | rozpoznaj, co warto zachować; popraw tylko realne wady; zwróć wersję i krótką listę zmian, jeśli o nią poprosi |
| Pisanie od zera | użytkownik daje materiał | najpierw treść i kolejność, potem szlif; `references/naturalny-styl.md` |
| Pismo prawnicze | pismo procesowe, uzasadnienie, relacja | `references/tekst-prawniczy.md`; formuły procesowe („wnoszę o", „powód") zostają, to nie slop |
| Relacja pokrzywdzonego | zawiadomienie o przestępstwie | formuły procesowe są tu wadą; rządzi `zawiadomienie-o-przestepstwie` (references/styl.md) |

## Kolejność pracy

1. Rozpoznaj gatunek, odbiorcę i rejestr; to wyznacza, co jest wadą.
2. Przeczytaj tekst i zaznacz, co zostaje.
3. Przejdź `references/katalog-wzorcow-humanizer.md` (36 wzorców: inflacja znaczenia, slop-słownictwo PL, imiesłowy pozornej głębi,
   reguła trójki, negatywne paralelizmy, strona bierna ukrywająca sprawcę, kalki z angielskiego, wypełniacze, artefakty czatbota,
   monotonny rytm, typografia PL). Pojedynczy sygnał (myślnik, „kluczowy", lista trzech) to nie wada; reaguj na skupiska i niedopasowanie do gatunku.
4. Polszczyznę sprawdzaj wg `references/polszczyzna.md` (reforma pisowni 2026, interpunkcja, cudzysłowy „…", łącznik zamiast pauzy).
5. **Bramka po przepisaniu** (obowiązkowa dla pism): `python3 scripts/audyt_po_przepisaniu.py <przed> <po>` sprawdza, czy nie zginęły
   daty, kwoty, przepisy, sygnatury, cytaty i siła twierdzeń. Wynik FAIL lub NEEDS_REVIEW = popraw przepisanie, nie bramkę.
6. Po redakcji pisma wraca kontrola merytoryczna (cytaty, subsumpcja); redakcja nie zwalnia z niej.

## Pliki

| Plik | Kiedy |
|---|---|
| `references/naturalny-styl.md`, `references/polszczyzna.md`, `references/polszczyzna-przyklady.md` | pisanie od zera, wątpliwości językowe |
| `references/tekst-prawniczy.md` | teksty prawnicze |
| `references/katalog-wzorcow-humanizer.md` | redakcja: lista kontrolna wzorców |
| `references/skrot-patron.md` | krótka wersja zasad do szybkiej redakcji |
| `scripts/audyt_po_przepisaniu.py`, `tests/` | bramka wierności po przepisaniu |

Pochodzenie: humanizer-pl (MIT, MateMatic), naturalne-pisanie (elconcept), pisz-po-ludzku (Patron, AGPL-3.0). Zob. pliki NOTICE-*.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** pismo po kontroli merytorycznej (ostatni szlif; nie zmienia faktów, cytatów ani sygnatur)
- **Wynik zapisz w:** nowa wersja `drafty/<pismo>/..._vN+1.md` (tylko MD); DOCX dopiero redline końca sesji (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `redline-docx-pl`, `szturm-na-draft-pl`
- **Basic Memory (`legal`):** czytaj lekcje teczki i notatkę pisma (stan pętli); po każdej rundzie zapisz w notatce pisma wersję, otwarte uwagi i pytania, lekcje w `## Lekcje` (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
