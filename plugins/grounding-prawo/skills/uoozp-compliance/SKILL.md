---
name: uoozp-compliance
description: Rozszerzona kontrola zgodności hospitalizacji psychiatrycznej z UoOZP — obejmuje przyjęcie bez zgody (art. 23/24), przymus bezpośredni (art. 18–18f), leczenie bez zgody (art. 33–34) i kontrolę sądową (art. 42–49). Rozdziela przyjęcie bez zgody od leczenia bez zgody oraz zasadność (bezzasadność) od legalności (bezprawność). Używaj do audytu protokołu przyjęcia, karty przymusu, planu leczenia lub całej hospitalizacji.
metadata:
  argument-hint: ''
---

# /tk-uoopz-compliance-check — Rozszerzona Kontrola UoOZP (przyjęcie, przymus, leczenie, sąd)

Sprawdź zgodność hospitalizacji psychiatrycznej bez zgody z pełnym reżimem UoOZP: przesłanki materialne, wymogi proceduralne, przymus bezpośredni, leczenie bez zgody i kontrolę sądową. Fork rozszerzający zakres poza samo przyjęcie z art. 23\.

&nbsp;

**Zastrzeżenie**: Analiza służy organizacji pracy, nie zastępuje porady prawnej.

&nbsp;

**Dwie reguły nadrzędne:**

&nbsp;

1. **Oddziel przyjęcie bez zgody (art. 23/24) od leczenia bez zgody (art. 33/34).** To odrębne podstawy z odrębnymi przesłankami — nie mieszaj ich.  
2. **Oddziel bezzasadność od bezprawności.** Bezzasadność \= problem materialnych podstaw przyjęcia/pobytu. Bezprawność \= niezgodność z prawem (materialna, proceduralna lub dokumentacyjna). Postanowienie sądu o zasadności przyjęcia nie zawsze wyczerpuje analizę wszystkich uchybień formalnych dla potrzeb roszczeń cywilnych.

## Wywołanie

```
/tk-uoopz-compliance-check $ARGUMENTS
```

&nbsp;

Przykłady:

&nbsp;

- "Sprawdź kartę przymusu bezpośredniego z \[data\]"  
- "Czy leczenie farmakologiczne miało podstawę w art. 33?"  
- "Oceń zgodność unieruchomienia — kontrole co 15 minut i przedłużenia"  
- "Czy zastosowano art. 33 wobec pacjenta przyjętego w trybie art. 24?"

&nbsp;

Analizuj tylko terminy właściwe dla danego stanu faktycznego (48h, 72h, 4h, 6h, 24h, 15 min).

&nbsp;

---

## Moduł A: Przyjęcie bez zgody (art. 23 / art. 24\)

### Art. 23 — przesłanki materialne

- [ ] Wskazano **chorobę psychiczną** (nie tylko „zaburzenia psychiczne")  
- [ ] Opisano **konkretne dotychczasowe zachowanie**  
- [ ] Zagrożenie było **bezpośrednie** (życiu własnemu / życiu lub zdrowiu innych)  
- [ ] Wykazano **związek** zagrożenia z chorobą psychiczną  
- [ ] Lekarz wyznaczony **osobiście zbadał** pacjenta  
- [ ] Zasięgnięto opinii drugiego lekarza psychiatry albo psychologa (w miarę możliwości) / wyjaśniono jej brak

### Art. 24 — przyjęcie obserwacyjne (do 10 dni)

- [ ] Zachodziła **wątpliwość diagnostyczna**, czy osoba jest chora psychicznie  
- [ ] Nie zastosowano art. 23 tam, gdzie właściwy był art. 24  
- [ ] Pobyt obserwacyjny nie przekroczył 10 dni

&nbsp;

**Czerwone flagi (wysoka waga):** zastosowanie art. 23 przy stanie wątpliwości właściwym dla art. 24; brak osobistego badania; brak choroby psychicznej jako podstawy art. 23; ogólnikowy opis agresji/zagrożenia bez konkretnego zachowania.

### Terminy przyjęcia

- [ ] Zatwierdzenie ordynatora w **48 h**  
- [ ] Zawiadomienie sądu opiekuńczego w **72 h** (od przyjęcia)  
- [ ] Odnotowanie czynności w dokumentacji, wpis w rejestrze osób przyjętych bez zgody

&nbsp;

---

## Moduł B: Przymus bezpośredni (art. 18–18f)

- [ ] Wskazano **konkretną formę** przymusu (przytrzymanie / przymusowe podanie leków / unieruchomienie / izolacja)  
- [ ] Wskazano **przesłankę ustawową** zastosowania  
- [ ] Wskazano, **kto zdecydował** (lekarz / pielęgniarka / kierujący akcją medycznych czynności ratunkowych) i kto nadzorował  
- [ ] Pacjenta **uprzedzono** / odnotowano przyczynę odstąpienia od uprzedzenia  
- [ ] Wybrano **środek najmniej uciążliwy**; szczególna ostrożność; dobro pacjenta  
- [ ] Przeprowadzono **ocenę zasadności** przymusu w terminie  
- [ ] Sporządzono kartę zastosowania przymusu bezpośredniego

### Unieruchomienie / izolacja

- [ ] Zlecenie na maksymalnie **4 h**  
- [ ] Kontrola stanu fizycznego **co 15 minut** (udokumentowana)  
- [ ] Przedłużenie po **osobistym badaniu**; kolejne przedłużenia z opinią innego lekarza psychiatry  
- [ ] Powiadomienie ordynatora po **24 h**  
- [ ] Warunki pomieszczenia (jednoosobowe/osłona; godność i intymność; monitoring izolacji i retencja zapisu)

&nbsp;

**Czerwone flagi (wysoka waga):** brak dokumentacji przymusu; brak oceny zasadności; brak kontroli co 15 minut; przedłużenie unieruchomienia bez wymaganego osobistego badania; brak opinii innego psychiatry przy przedłużeniu; brak dokumentacji przymusowego podania leków.

&nbsp;

---

## Moduł C: Leczenie bez zgody (art. 33 / art. 34\) — odrębne od przyjęcia

- [ ] Pacjent był **przyjęty bez zgody** (warunek stosowania art. 33\)  
- [ ] Czynność była **niezbędna** i służyła **usunięciu przyczyn przyjęcia bez zgody**  
- [ ] Pacjenta **zapoznano z planowanym postępowaniem** leczniczym  
- [ ] Art. 33 **nie został użyty wobec osoby przyjętej w trybie art. 24** (wyłączenie)  
- [ ] Przymus z art. 34 miał **związek z czynnościami leczniczymi z art. 33** (lub zapobieżeniem samowolnemu opuszczeniu szpitala)

&nbsp;

**Czerwone flagi (wysoka waga):** brak podstawy prawnej leczenia bez zgody; leczenie bez zgody powołane ogólnie bez wskazania art. 33/34; przymusowe podanie leków bez dokumentacji przymusu; brak związku leczenia z usunięciem przyczyn przyjęcia; użycie art. 33 wobec pacjenta z art. 24; inwazyjna procedura somatyczna w trakcie hospitalizacji psychiatrycznej bez zgody i bez wyjątku ustawowego.

&nbsp;

> Uwaga na styk z prawem karnym: konkretna inwazyjna czynność wykonana bez zgody może wymagać odrębnej analizy — użyj `/tk-medical-consent-check`. Nie kwalifikuj całej hospitalizacji jako „zabiegu leczniczego".

&nbsp;

---

## Moduł D: Kontrola sądowa i gwarancje (art. 42–49)

- [ ] Sąd zawiadomiony w terminie; ustalona **data otrzymania** zawiadomienia przez sąd  
- [ ] Wysłuchanie pacjenta w **48 h od otrzymania** zawiadomienia  
- [ ] Realna reprezentacja (pełnomocnik z urzędu, jeśli uzasadnione)  
- [ ] Niezależna opinia biegłego psychiatry; sąd badał (oczywistą) bezzasadność  
- [ ] Szpital **wykonał postanowienie** sądu; obowiązek wypisu przy braku podstaw

&nbsp;

**Czerwone flagi (wysoka waga):** brak sądowej kontroli w wymaganym trybie; niewykonanie postanowienia sądu; brak realnej reprezentacji; kontynuowanie pobytu bez zgody po cofnięciu zgody bez trybu ustawowego.

&nbsp;

---

## Model zasadność vs legalność (obowiązkowy)

Zawsze rozdziel dwa pytania i opisz oba poziomy oddzielnie:

&nbsp;

- **Zasadność (materialna)**: czy istniały przesłanki przyjęcia/pobytu (choroba psychiczna, bezpośrednie zagrożenie, związek).  
- **Legalność (bezprawność)**: czy dochowano wymogów formalnych, proceduralnych i dokumentacyjnych.

&nbsp;

Reguły:

&nbsp;

- Brak przesłanek materialnych → wniosek silniejszy niż samo uchybienie formalne.  
- Spełnienie przesłanek materialnych \+ naruszenie procedury → opisz oba poziomy oddzielnie.  
- Brak dokumentacji uniemożliwiający ocenę → wskaż **lukę dowodową** i obowiązek wyjaśnienia przez szpital (nie domniemuj na korzyść szpitala).

&nbsp;

---

## Format wyjściowy

```
## Kontrola UoOZP — [Dokument / Aspekt] — [Data]

### Wynik ogólny
[ZGODNE / NIEZGODNE / NIEWERYFIKOWALNE — z uzasadnieniem]

### Ocena ryzyka: [ZIELONY / ŻÓŁTY / POMARAŃCZOWY / CZERWONY]

### 1. Deklarowana podstawa prawna vs rzeczywista kwalifikacja
### 2. Oś czasu (tylko terminy właściwe dla stanu faktycznego)
### 3. Przesłanki materialne (zasadność)
### 4. Wymogi proceduralne i dokumentacja (legalność)
### 5. Przymus bezpośredni — jeżeli dotyczy
### 6. Leczenie bez zgody (art. 33/34) — jeżeli dotyczy
### 7. Kontrola sądowa i gwarancje
### 8. Czerwone flagi
| Uchybienie | Charakter (materialny/proceduralny/dokumentacyjny) | Podstawa prawna | Waga |
|---|---|---|---|
### 9. Dokumenty brakujące (do pozyskania)
### 10. Wnioski stanowcze
### 11. Realistyczne alternatywy wymagające wyjaśnienia
```

&nbsp;

**Dokumenty do pozyskania** (dobierz do modułu): karta przymusu bezpośredniego, zlecenia lekarskie, karty kontroli co 15 minut, przedłużenia unieruchomienia, opinie drugiego psychiatry, plan leczenia i informacja o zapoznaniu pacjenta, uzasadnienie niezbędności czynności leczniczych, zawiadomienie sądu i data jego otrzymania, protokół wysłuchania, opinia biegłego, dowód doręczenia postanowienia szpitalowi.

&nbsp;

**Język preferowany:** „dokumentacja wskazuje" / „dokumentacja nie potwierdza" / „brak podstawy w dokumentacji" / „wymaga wyjaśnienia przez szpital" / „tworzy poważną lukę legalności" / „naruszenie ma charakter proceduralny/materialny/dokumentacyjny".

&nbsp;

**Język zakazany:** „to tylko formalność" / „pewnie wpisano później przez system" / „skoro pacjent był w psychiatrii, przymus był oczywisty" / „skoro była Policja, przesłanki były spełnione" / „skoro lekarz podpisał, badanie musiało być" / „brak dokumentu nie ma znaczenia".

&nbsp;

---

## Kontrola jakości (przed odpowiedzią)

- czy oddzielono fakty od interpretacji  
- czy nie pomieszano art. 23 z art. 24  
- czy nie pomieszano **przyjęcia bez zgody z leczeniem bez zgody**  
- czy nie pomieszano przymusu z farmakoterapią za zgodą  
- czy nie pomieszano zasadności z bezprawnością  
- czy każda czerwona flaga ma dokument lub udokumentowany brak dokumentu  
- czy terminy 48h/72h/4h/6h/24h/15min analizowane tylko gdy dotyczą stanu faktycznego  
- czy alternatywy są realistyczne, technicznie możliwe i zakotwiczone w materiale (bez hipotetycznych „ratowania" braków dokumentacji)

## Wskazówki

- Brak osobistego badania i brak dokumentacji przymusu to najsilniejsze wskaźniki bezprawności — waliduj najpierw.  
- Termin 72 h liczy się od momentu przyjęcia; termin 48 h wysłuchania — od otrzymania zawiadomienia przez sąd.  
- Konkretną inwazyjną czynność bez zgody przekaż do `/tk-medical-consent-check`; ryzyko procesowe całości — do `/tk-case-risk`.

&nbsp;

**Źródła map**: `legal/skill_polish_law_articles_map/mental_health_article_map.md` (art. 18–18f, 21–34, 42–49; model bezzasadność/bezprawność; red\_flag\_taxonomy; documents\_to\_request). Fork rozszerzający istniejący, kanoniczny skill `compliance-check` (art. 23\) — kanoniczny plik pozostaje nietknięty.

&nbsp;

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** dokumentacja hospitalizacji psychiatrycznej, chronologia
- **Wynik zapisz w:** kontrola zgodności w `analiza/_podsumowanie.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pisma-procesowe-v3`, `zawiadomienie-o-przestepstwie`
- **Mapa ścieżek:** skill `prowadnik-grounding-prawo`.
