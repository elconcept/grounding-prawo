---
name: rodo-dsar-pl
description: 'Żądania z art. 15-22 RODO: dostęp, sprostowanie, usunięcie, ograniczenie, sprzeciw; terminy i odmowa. Używaj przy własnym żądaniu wobec administratora i ocenie odpowiedzi.'
license: Apache-2.0
allowed-tools:
- Read
metadata:
  author: Wiesław Mazur / MateMatic
  version: 1.3.0
  companion_skills: patron-prawo-pl-zrodla/modules/uodo-grounding-pl, gaius-api-anonymization
  parity: gdpr-dsar-en
  data-residency: local
  requires-human-approval: 'true'
  pii-egress: none
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `ustawy`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# RODO DSAR PL - obsługa żądań podmiotów danych (art. 12, 15-22)

## Filozofia

Żądanie podmiotu to zegar + ocena prawna, nie automat. Skill klasyfikuje, pilnuje terminu i składa
**draft** - decyzję o realizacji/odmowie i wysyłkę podejmuje administrator. Usunięcie/eksport danych
to akt nieodwracalny/na zewnątrz => zawsze człowiek (granica governance).

## Krok 0 - Tożsamość i termin

- **Weryfikacja tożsamości** (art. 12 ust. 6) - przy uzasadnionych wątpliwościach żądaj dodatkowych
  informacji. To NIE zawiesza biegu bezwarunkowo: wg Wytycznych EROD 01/2022 zawieszenie wchodzi w grę
  **tylko**, gdy informacja jest niezbędna do potwierdzenia tożsamości ORAZ administrator zażądał jej
  bez zbędnej zwłoki. Datę wpływu zachowaj w rejestrze zawsze - spóźnione lub nieproporcjonalne żądanie
  tożsamości nie przedłuża terminu, a weryfikacja nie służy do obstrukcji.
- **TERMIN: bez zbędnej zwłoki, a w każdym razie w ciągu miesiąca od otrzymania żądania**
  (art. 12 ust. 3) - miesiąc to granica. Przedłużenie o **kolejne 2 miesiące** w razie potrzeby, z
  uwagi na skomplikowany charakter żądania lub liczbę żądań - poinformuj osobę w ciągu pierwszego
  miesiąca, z podaniem przyczyn opóźnienia. Skill liczy `deadline_1_month` i
  `deadline_extended_3_months`.
- **Co do zasady bezpłatnie** (art. 12 ust. 5). Rozsądna opłata albo odmowa tylko gdy żądanie jest
  **ewidentnie nieuzasadnione lub nadmierne** (w szczególności ustawiczne) - obowiązek wykazania
  spoczywa na administratorze.

## Krok 1 - Klasyfikacja prawa

| Art. | Prawo | Klucz |
|---|---|---|
| 15 | Dostęp + kopia | zakres informacji, kopia danych, prawa osób trzecich |
| 16 | Sprostowanie | dane nieprawidłowe/niekompletne |
| 17 | Usunięcie ("zapomnienie") | przesłanki ust. 1 vs **wyjątki ust. 3**: wolność wypowiedzi i informacji, obowiązek prawny lub zadanie publiczne, zdrowie publiczne, cele archiwalne/badawcze/statystyczne, roszczenia |
| 18 | Ograniczenie | "zamrożenie" zamiast usunięcia |
| 20 | Przenoszenie | tylko zgoda/umowa + przetwarzanie zautomatyzowane; format ustrukturyzowany |
| 21 | Sprzeciw | uzasadniony interes / marketing (marketing = bezwzględny) |
| 22 | Decyzje zautomatyzowane | prawo pierwotne = **niepodleganie** decyzji opartej wyłącznie na zautomatyzowanym przetwarzaniu wywołującej skutki prawne/istotne; wyjątki ust. 2 (umowa, przepis, wyraźna zgoda) => zabezpieczenia ust. 3: interwencja ludzka, własne stanowisko, zakwestionowanie |

## Krok 2 - Bramki i podstawy odmowy

Sprawdź wyjątki specyficzne dla prawa (zwłaszcza art. 17 ust. 3 i ograniczenia krajowe). Gdy
administrator nie podejmuje działań, informuje osobę niezwłocznie, najpóźniej w ciągu miesiąca od
otrzymania żądania, o powodach oraz o możliwości skargi do UODO i drodze sądowej (art. 12 ust. 4). Powołania na
decyzje UODO => [[patron-prawo-pl-zrodla/modules/uodo-grounding-pl]].

## Krok 3 - Draft odpowiedzi + rejestr

Skill składa odpowiedź (język prosty, art. 12 ust. 1), dopasowaną do powołanego prawa. Przy art. 15
to **kopia danych osobowych pobrana z systemów operacyjnych**, które je faktycznie przechowują, plus
dostępne informacje o źródle danych (art. 15 ust. 1 lit. g) - RCP ([[rodo-ropa-dpa-pl (poza pluginem)]]) dostarcza
tylko ogólnych informacji o przetwarzaniu (cele, kategorie, odbiorcy), nie danych osoby. Do tego wpis
do rejestru żądań (data wpływu, typ, termin, rozstrzygnięcie).

## Narzędzie - kalkulator terminu (deterministyczny, offline)

Terminu miesięcznego nie licz w pamięci - arytmetyka miesiąca ma pułapki (wpływ 31 stycznia => koniec 28/29 lutego, wg rozporządzenia (EWG, Euratom) nr 1182/71). Użyj skryptu (zero zależności, offline):

```bash
python scripts/gdpr_deadlines.py dsar --from 2026-01-31 --extend
```

Zwraca `deadline_1_month` oraz (z `--extend`) `deadline_extended_3_months`. Skrypt nie przesuwa
daty, która wypada w sobotę, niedzielę lub święto (art. 3 ust. 4 rozporządzenia (EWG, Euratom) nr 1182/71), więc
jego wynik może wypaść wcześniej niż termin prawny, nigdy później. Wklej go do odpowiedzi i rejestru.

## Granica governance

Skill: klasyfikuje, liczy terminy, składa draft, prowadzi rejestr. Człowiek: weryfikuje tożsamość,
decyduje o realizacji/odmowie, **wykonuje usunięcie/eksport**, wysyła odpowiedź. Akty nieodwracalne i
na zewnątrz nigdy nie są automatyczne.

## Companion

Rejestr czynności (skąd dane): [[rodo-ropa-dpa-pl (poza pluginem)]].
Parytet: `gdpr-dsar-en`.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** żądanie dotyczące własnych danych (dostęp, sprostowanie, usunięcie)
- **Wynik zapisz w:** `<sprawa>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` (tylko MD) w teczce sprawy, której dotyczą dane (gdy niejednoznaczna: pytanie do autora), jeden DOCX w `legal/output/` (`shared/format-pisma/wersja_pisma.py`), wpis w `_PRZEBIEGI.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `kalkulatory-procesowe-pl`, `pisz-po-polsku`
- **Basic Memory (`legal`):** czytaj teczkę sprawy; decyzje i stan zapisz w teczce (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
