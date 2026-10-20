# Soczewki szturmu - mandat, wejście, co zwracają

## Wybór mandatu przed soczewkami

Dla zawiadomienia pokrzywdzonego stosuj ZOP-R z
[recenzja-zawiadomienia.md](recenzja-zawiadomienia.md) i
`shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md`. Poniższe ogólne mandaty E2/E3,
„sam draft”, „akta rozstrzygają”, „kategoryczne bez dowodu”, „prokurator jako przeciwnik”
i mapa FAKT_BEZ_ZRODLA nie obowiązują w ZOP-R. Role dostają pełną relację i zwracają
pytania o pominięte osoby, zdarzenia, skutki, prawa i działania organów; pytania zapisują
poza wejściem skryptu syntezy. Prawo/cytaty/format kontroluj bez cenzury relacji.
Dalsza część opisuje zwykły szturm dla pozostałych pism.


Każda soczewka czyta draft innym okiem i dlatego łapie inne błędy (dane z przebiegów 25.09 i 28.09:
to samo ustalenie zgłaszały 2-4 skille, a część skilli nie dała żadnego unikalnego). Soczewka
**nie pisze raportu**. Zwraca listę ustaleń w schemacie `schemat-ustalenia.json` do pliku
`<katalog_przebiegu>/ustalenia/<NN>_<soczewka>.json`. Synteza, deduplikacja i decyzja o edycji
należą do `scripts/synteza.py`, nie do soczewki.

Wspólne reguły dla wszystkich soczewek:
- **Kotwica** = `plik:linia` z `<nazwa>.clean.nl.txt` z E0. Bez kotwicy ustalenie odpada w syntezie.
- **target_text** to dosłowny fragment jednego akapitu, z takim kontekstem, żeby wystąpił raz.
  Nie przepisuj go z pamięci - kopiuj z `.clean.md`.
- **Nie wolno** proponować zmian w `fakty_potwierdzone` i `decyzje_autora` ani dopisywać wyjaśnień,
  które te rejestry wykluczają. Jeżeli soczewka uważa, że fakt klienta jest sprzeczny z aktami,
  zgłasza SPRZECZNOSC z `naprawa: DECYZJA_AUTORA` i dowodem - nie „łagodzi” tekstu.
- **Pisz do tezy.** `teza_nadrzedna` to cel procesowy. Ustalenie, które poprawia zdanie kosztem
  tezy (np. dopisuje „niewinne” wyjaśnienie, osłabia własny dowód), to błąd soczewki, nie poprawka.
- **Liczba w new_text** tylko z pomiarem albo źródłem w polu `dowod`.
- Soczewka, która nic nie znalazła, zapisuje pustą listę `[]`. „OK” bez listy nie istnieje.

Jeżeli środowisko ma subagentów, soczewki E3 uruchamiaj równolegle, każdą z samym jej wejściem
(niezależność jest celem - soczewka, która widzi cudze ustalenia, powtarza je zamiast szukać).

---

## E1 - warstwa obiektywna (deterministyczna, zawsze)

| Soczewka | Wejście | Sprawdza | Klasa | Uwagi |
|---|---|---|---|---|
| `citation-grounding-pl/modules/ekstraktor-cytatow-pl` | `.clean.md` | wszystkie sygnatury, ECLI, Dz.U., ELI, przepisy, odwołania skrótowe | - | front-end: lista do sprawdzenia, sam nie zgłasza ustaleń |
| `citation-grounding-pl` (`node <skille>/citation-grounding-pl/scripts/ground-citations.mjs`) | cytaty + źródła z akt | cytat istnieje dosłownie (ISTNIENIE/TREŚĆ/FRAGMENT) | CYTAT | 🔴 gdy cytat przypisany karcie, na której go nie ma |
| `citation-grounding-pl/modules/patron-weryfikacja-cytatow` (`python3 <skille>/citation-grounding-pl/modules/patron-weryfikacja-cytatow/scripts/verify_citations.py`) | pismo + `--source` karty akt `.md` | cytaty z akt i załączników, liczby narzędzi | CYTAT, FAKT_BEZ_ZRODLA | liczby „z raportu narzędzia” muszą być w załączniku |
| MCP `saos` (lex.xlap.pl/mcp, lokalny dump) | sygnatury z ekstraktora | sygnatura istnieje; **data i skład z treści orzeczenia**, nie z metadanych | SYGNATURA | metadane SAOS potrafią mieć złą datę - źródłem jest treść |
| MCP `isap` (lex.xlap.pl/mcp) (`shared/MOD-TEKST-JEDNOLITY.md`) | powołane przepisy | brzmienie obowiązujące | PRZEPIS | cytowalne tylko FOUND + tekst_jednolity + obowiązuje |
| `citation-grounding-pl/modules/patron-identyfikatory-pl` (`pl_entities.py extract`) | `.clean.md` | PESEL/NIP/REGON sumy, format sygnatur | SYGNATURA | tani, zawsze |

Wynik E1 jest binarny. 🔴 z E1 blokuje wysyłkę, dopóki E8 nie potwierdzi naprawy ponownym przebiegiem.
Konektor offline i brak cache -> ustalenie z `naprawa: DOWOD` i komentarzem „NIEPEWNE - źródło
niedostępne (data próby)”. Nigdy „OK”.

## E2 - spójność (zawsze, pełna)

| Soczewka | Mandat | Klasa |
|---|---|---|
| metoda `dr-16-pisma-strategia-dowody-orzecznictwo` + `analizator-dowodow-v3` | każde twierdzenie faktyczne -> karta akt albo „wiedza strony” (wtedy musi być tak nazwane w tekście); pismo ↔ załączniki ↔ akta: te same daty, liczby, nazwy, opisy | FAKT_BEZ_ZRODLA, SPRZECZNOSC |
| `deliverable-fidelity-pl` (`node scripts/fidelity-check.mjs` z katalogu tego skilla - w projekcie albo w pluginie `fundament-weryfikacyjny`) | czy flagi RED z rejestru FINDINGS nie wypadły z pisma | KOMPLETNOSC |

Typowe trafienia: „z materiału sprawy wynika” bez karty; „jedyny dowód” vs inny dokument w aktach;
opis tego samego zdarzenia inaczej w piśmie i w ekspertyzie.

## E3 - soczewki ataku (niezależne; IZOLOWANA = widzi tylko draft, bez akt)

| Soczewka | Rola | Stawka | Mandat | Klasy |
|---|---|---|---|---|
| `pierwsze-wrazenie-sedziego-pl` | IZOLOWANA, neutralna | M, L | sędzia czyta na zimno: czy teza jest na pierwszej stronie, czy wniosek odpowiada na pytanie, które sąd rozstrzyga | LOGIKA, STRATEGIA |
| `atak-przeciwnika-pl` | IZOLOWANA, wroga | S, M, L | rdzeń teorii ataku; zdania, które osłabiają własny dowód; przyznania | LOGIKA, STRATEGIA, SPRZECZNOSC |
| `shared/MOD-ATAK-NA-DRAFT.md` D1-D5 | pełnomocnik przeciwnika | M, L | D1 kategoryczne bez dowodu, D2 macierz FAKT/PRAWO/LOGIKA/PROCES, D3 sprzeczności międzyakapitowe, D4 luki dowodowe, D5 własne ryzyka | wg macierzy |
| `zarzuty-do-opinii-bieglego` w trybie odwrotnym | biegły/przeciwnik czyta NASZ załącznik techniczny | L (i M, gdy jest załącznik techniczny) | metodologia, odtwarzalność pomiarów, pytania do biegłego podsuwające niewinne wyjaśnienie | LOGIKA, FAKT_BEZ_ZRODLA |
| `subsumpcja-pl` | sylogizm | L | przesłanka mniejsza pełna? pominięty fakt istotny dla znamienia (np. umyślność) | KOMPLETNOSC, LOGIKA |
| `adversarial-legal-review-pl` (4 role + panel rozbieżności) | czerwony zespół | L | filary tezy: przetrwał / osłabiony / NIEPEWNE / obalony | STRATEGIA |

**Tryb przeciwnika dobierz do sprawy.** W sprawie karnej/wykroczeniowej, w której pokrzywdzony nie
jest oskarżycielem posiłkowym, przeciwnikiem jest oskarżyciel publiczny, nie pełnomocnik pokrzywdzonego.
W cywilnej - pełnomocnik drugiej strony. Soczewka wroga dostaje tę rolę wprost w poleceniu.

Soczewki E3 częściej niż inne proponują „wyjaśnienia alternatywne”. To ich zadanie jako ataku,
ale **nie jako poprawki**: ustalenie typu „przeciwnik powie X” zapisuj z `naprawa: DECYZJA_AUTORA`
i propozycją zdania uprzedzającego, które X obala - nie zdania, które X przyznaje.

## E4 - styl i format

| Soczewka | Narzędzie | Klasa, typowa naprawa |
|---|---|---|
| `marko-pl-content` | werdykt + lista zarzutów `plik:linia`; `python3 <skille>/szturm-na-draft-pl/modules/marko-pl-content/scripts/skan_pisowni.py` (kandydaci, nie werdykty) | STYL 🟡/🟢 AUTO |
| format .docx | `uv run scripts/fix_format.py draft.docx` | FORMAT: tekst w stylu nagłówka, podkreślenia w tekście ciągłym, puste nagłówki |

Typografia pauz (—) i inne konwencje zmieniaj tylko wtedy, gdy `decyzje_autora` nie rozstrzyga ich
inaczej. Pytania do biegłego i pozycje petitum to jedna jednostka - nie dziel ich na zdania.

---

## Soczewki tylko na żądanie (bez unikalnego ustalenia w przebiegach 25.09 i 28.09)

`prawny-router-v3`,
`patron-prawo-pl-zrodla` (mapa źródeł), `dr-11-cyfrowe-cyber-ai-dane-ip`, `kalkulatory-procesowe-pl/modules/terminy-procesowe-pl` (tylko gdy pismo liczy
terminy), `chronologia-sprawy-v1` (tylko gdy oś czasu jest sporna), `patron-pismo-procesowe-pl (poza pluginem)`
(forma), .

## Mapowanie klasa -> kto zwykle znajduje -> dopuszczalna naprawa

| Klasa | Kto | Najwyżej |
|---|---|---|
| CYTAT | citation-grounding, citation-grounding-pl/modules/patron-weryfikacja-cytatow | AUTO (🔴 z dowodem E1) |
| SYGNATURA | mcp-saos, patron-identyfikatory | AUTO (🔴 z dowodem E1, data z treści) |
| PRZEPIS | MCP isap | AUTO (🔴 z dowodem E1, t.j.) |
| FAKT_BEZ_ZRODLA | citation-grounding-pl/modules/patron-weryfikacja-cytatow, analizator-dowodow, MOD-ATAK D4 | REDAKCJA (dodać źródło albo nazwać wiedzę strony) |
| SPRZECZNOSC | analizator-dowodow, adversarial, fidelity | REDAKCJA, gdy akta rozstrzygają; DECYZJA_AUTORA, gdy dotyka faktu klienta |
| LOGIKA | atak-przeciwnika, pierwsze-wrażenie, MOD-ATAK D1/D2 | REDAKCJA |
| STRATEGIA | atak-przeciwnika, analizator-przepisow, orzeczenia | DECYZJA_AUTORA |
| KOMPLETNOSC | subsumpcja, fidelity | DECYZJA_AUTORA albo DOWOD |
| STYL | marko, humanizer, pisz-po-ludzku | AUTO (🟡/🟢) |
| FORMAT | fix_format.py | AUTO (🟡/🟢), zmiany nieśledzone - jawnie w raporcie |
