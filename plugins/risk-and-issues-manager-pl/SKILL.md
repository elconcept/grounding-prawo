---
name: risk-and-issues-manager-pl
version: 0.1.0
description: Prowadzi rejestr RAID (Ryzyka / Zalozenia / Problemy / Decyzje) per sprawa w polskiej kancelarii. Konsumuje korespondencje, status raporty historyczne, notatki ze spotkan. Produkuje .xlsx rejestr RAID + opcjonalnie draft mailowy eskalacyjny do wspolnika/klienta gdy ryzyko poziomu Czerwony. Polskie realia: terminy procesowe (uchybienie = przewroniecie sprawy), zarzuty zazalenia, zawieszenia postepowania, art. 16 KEA, RODO incydenty, konflikt interesow. Uzywaj gdy uzytkownik mowi "rejestr ryzyk sprawy [X]", "RAID dla [matter]", "co moze pojsc zle w [Y]", "zaktualizuj ryzyka [X]", "draft eskalacji do wspolnika w sprawie [Y]". NIE uzywaj do raportu statusu (status-report-drafter-pl) ani scope change (scope-change-controller-pl). Czyta od status-report-drafter-pl (historia RAG i eskalacji) i scope-change-controller-pl (kazda zmiana scope to nowe ryzyko). Pisze do folderu sprawy + aktualizuje [Sprawa]_LPM_Memory.md (skladzia trendow ryzyk).
---

# Risk and Issues Manager (PL)

Skill prowadzi rejestr RAID per sprawa polskiej kancelarii. Wykrywa ryzyka ukryte w korespondencji - "wzmianka klienta o szybkim terminie", "biegly nie odpowiada", "kontrkancelaria zlozyla zazalenie". Klasyfikuje, mierzy, proponuje mitigacje i eskaluje gdy poziom Czerwony.

## 1. Kiedy uzywac

### Triggery

- "Rejestr ryzyk sprawy [X]"
- "RAID dla [matter]"
- "Co moze pojsc zle w [Y]"
- "Zaktualizuj ryzyka [X]"
- "Draft eskalacji do wspolnika w sprawie [Y]"
- "Czy ten termin to ryzyko?"
- "Zalozenia pod sprawa [X]"

### Kiedy NIE uzywac

- Status sprawy biezacy - `status-report-drafter-pl` (skill #1).
- Klasyfikacja nowego zadania klienta - `scope-change-controller-pl` (skill #2).
- Sprawdzenie zgodnosci RODO konkretnego dokumentu - to osobny przeplyw legal compliance.
- Pelny audyt prawny ryzyk dla zarzadu klienta - to oddzielny produkt MateMatic (`matematic-expert-panel`).

## 2. Metodyka rdzenia

### 2.1 RAID = cztery kategorie

Skill kazdy zdarzenie/wzmianke klasyfikuje:

- **R - Ryzyko** (Risk) - rzecz ktora MOZE sie wydarzyc, jeszcze nie nastapila. Ma prawdopodobienstwo i wplyw. Wymaga planu mitigacji.
- **Z - Zalozenie** (Assumption) - rzecz ktora przyjmujemy za prawde bez weryfikacji. Wymaga walidacji do okreslonej daty.
- **P - Problem** (Issue) - rzecz ktora **juz** sie wydarzyla i blokuje sprawe. Wymaga rozwiazania.
- **D - Decyzja** (Decision) - decyzja juz podjeta z konsekwencjami dla sprawy. Wymaga zapisu dla audytu i przyszlych raportow.

Skill NIE miesza kategorii. "Ryzyko ze biegly nie odpowie" = R (nie nastapilo). "Biegly nie odpowiedzial w 3 ponagleniu" = P (juz nastapilo).

### 2.2 Skala oceny ryzyka

Skill ocenia kazde R i P w dwoch wymiarach:

**Prawdopodobienstwo** (P):
- Niskie (<25%)
- Srednie (25-60%)
- Wysokie (>60%)
- Pewne (>90% lub juz nastapilo - klasyfikuj jako Problem)

**Wplyw** (W):
- Niski - nieznaczny wplyw na sprawe, mozemy ogarnac.
- Sredni - opoznienie milestone'u o 1-2 tyg, zmiana strategii ale dowieziemy.
- Wysoki - opoznienie miesieczne, zagrozenie wyniku sprawy, eskalacja do wspolnika.
- Krytyczny - utrata sprawy, naruszenie tajemnicy, RODO incydent, dyscyplinarka - eskalacja do klienta + zarzadzania.

**Iloczyn = poziom RAG**:
- Wpfyw niski OR Prawd. niski = Zielony.
- Wpfyw sredni + Prawd. srednie = Bursztynowy.
- Wpfyw wysoki AND Prawd. srednie+ = Czerwony.
- Wpfyw krytyczny = Czerwony bez wzgledu na prawd.

### 2.3 Typowe polskie ryzyka kancelaryjne

Skill rozpoznaje wzorce charakterystyczne dla polskiego systemu:

- **Termin procesowy** (rozprawa, apelacja 14 dni od doreczenia wyroku z uzasadnieniem, kasacja 2 miesiace, skarga konstytucyjna 3 miesiace od ostatecznego rozstrzygniecia, postepowanie administracyjne 14 dni odwolanie). Uchybienie = przewroniecie sprawy lub ograniczenie srodkow.
- **Biegly nie odpowiada** - czesty problem polskich postepowan, eskalacja przez wniosek o zmiane bieglej.
- **Zazalenie kontrkancelarii** na postanowienie sadu - zmiana harmonogramu.
- **Zawieszenie postepowania** - na wniosek stron lub z urzedu.
- **Konflikt interesow** - kancelaria reprezentuje strone z kolizja interesowna.
- **Tajemnica zawodowa** - ryzyko ujawnienia (przez bledny e-mail, przez wspolpracownika, przez chmurowe API).
- **RODO incydent** - wyciek danych klienta, ujawnienie osobom trzecim.
- **Dyscyplinarka** - skarga klienta do izby adwokackiej / radcowskiej.
- **Pactum de quota litis** - umowa wynagrodzeniowa naruszajaca art. 16 KEA.
- **Przedawnienie roszczenia** - klient nie zglosil sie wystarczajaco wczesnie.
- **Niezdolnosc procesowa klienta** (sm. choroba, ubezwlasnowolnienie) - zmiana strategii.

### 2.4 Eskalacja triage (jak w status-report)

R/P z RAG Czerwonym wymaga eskalacji. Skill klasyfikuje:

- **Poziom zespol** - aplikant/junior rozwiaze, bez eskalacji do wspolnika.
- **Poziom wspolnik** - wymaga decyzji wspolnika prowadzacego.
- **Poziom klient** - klient MUSI wiedziec i/lub zadzialac.

Test: **"Jezeli sprawa pojdzie zle a wspolnik/klient nie wiedzial - czy to nasza wina raportowa?"**.

## 3. Wejscie

### Pierwotne

- **Korespondencja sprawy** (mailowy watek + ewentualne odpowiedzi sadu/strony przeciwnej).
- **Notatki ze spotkan**.
- **Historia status raportow** z `[Sprawa]/raporty_status/`.

### Opcjonalne

- **Istniejacy RAID** z `[Sprawa]_RAID.xlsx` (jezeli juz prowadzony) - skill aktualizuje, nie nadpisuje.
- **Pierwotny zakres** (oferta/umowa) - kontekst do oceny ryzyka scope creep.
- **`[Sprawa]_LPM_Memory.md`** - historia ryzyk wczesniej zidentyfikowanych.

## 4. Wyjscie

### 4a. Glowny output - `[Sprawa]_RAID.xlsx`

Plik .xlsx w `[Sprawa]/raid/` lub `[Sprawa]_RAID.xlsx` w folderze sprawy.

Arkusze (template w `templates/raid_register_template.md`):

**Arkusz 1 - Ryzyka**
| ID | Data ident. | Opis ryzyka | Prawd. | Wplyw | RAG | Mitigacja | Wlasciciel | Termin walidacji | Status |
|---|---|---|---|---|---|---|---|---|---|

**Arkusz 2 - Zalozenia**
| ID | Data ident. | Opis zalozenia | Zrodlo zalozenia | Termin walidacji | Status walidacji | Notatki |
|---|---|---|---|---|---|---|

**Arkusz 3 - Problemy**
| ID | Data wystapienia | Opis problemu | Wplyw | Plan rozwiazania | Wlasciciel | Termin | Status |
|---|---|---|---|---|---|---|---|

**Arkusz 4 - Decyzje**
| ID | Data | Decyzja | Decydent | Uzasadnienie | Wplyw na sprawe | Notatki |
|---|---|---|---|---|---|---|

### 4b. Opcjonalny output - draft eskalacji

Gdy R/P z RAG Czerwonym - skill produkuje rownolegle:

**Plik**: `[Sprawa]_eskalacja_[YYYY-MM-DD].md` (markdown draft mailowy).

Zawartosc:
- Do: wspolnik prowadzacy / klient (zaleznie od poziomu).
- DW: wspolnik zarzadzajacy (jezeli klient).
- Tytul: "[Sprawa] - eskalacja: [opis ryzyka]"
- Tresc: kontekst sprawy, opis ryzyka, prawdopodobienstwo i wplyw, proponowana decyzja, deadline decyzji.

## 5. Workflow (5 krokow)

### Krok 1 - Identyfikacja sprawy i istniejacego RAID

- Nazwa sprawy + sciezka do folderu.
- Sprawdzenie czy istnieje `[Sprawa]_RAID.xlsx` - jezeli tak, ladowanie.
- Ladowanie `[Sprawa]_LPM_Memory.md` jezeli istnieje.

### Krok 2 - Ekstrakcja sygnalow z inputu

Skill parsuje korespondencje i wyciaga kazdy sygnal mogacy byc R/Z/P/D:

- "Klient wspomnial ze ma termin do polowy czerwca" - **Z** (zalozenie, walidacja: kiedy dokladnie?).
- "Bieglosc nie odpowiedziala na 3 ponaglenie" - **P** (problem, juz nastapilo).
- "Jezeli kontrkancelaria zlozy zazalenie, harmonogram sie zmieni" - **R** (ryzyko, jeszcze nie nastapilo).
- "Wspolnik prowadzacy zdecydowal zlozyc wniosek o przeprowadzenie dowodu z opinii innej bieglej" - **D** (decyzja podjeta).

### Krok 3 - Klasyfikacja i ocena

- Kazdemu sygnalowi przypisanie kategorii R/Z/P/D.
- Dla R i P - ocena prawd. i wplywu -> RAG.
- Dla Z - termin walidacji.
- Dla D - decydent + uzasadnienie.

### Krok 4 - Merge z istniejacym RAID

- Jezeli RAID istnieje - skill NIE usuwa pozycji, tylko aktualizuje status, dodaje nowe.
- Konflikty (np. ten sam R z innym RAG) - skill zostawia obie wersje z notatka i prosi o decyzje.

### Krok 5 - Output + eskalacje

- Zapis `[Sprawa]_RAID.xlsx`.
- Jezeli sa nowe R/P z RAG Czerwonym - skill produkuje draft eskalacji (4b) i WYWOLA `status-report-drafter-pl` z propozycja aktualizacji najblizszego status raportu.
- Update `[Sprawa]_LPM_Memory.md` z trendem ryzyk.

## 6. Cross-skill handoff

### Czyta od

- `status-report-drafter-pl` - historia RAG i eskalacji.
- `scope-change-controller-pl` - kazda zmiana scope = potencjalne nowe ryzyko (rejestrowane automatycznie).

### Pisze do

- `[Sprawa]_RAID.xlsx`.
- `[Sprawa]_eskalacja_[YYYY-MM-DD].md` (opcjonalnie).
- `[Sprawa]_LPM_Memory.md` (trend ryzyk).
- Sygnal do `status-report-drafter-pl` - jezeli RAG sie zmienil, najblizszy status raport powinien to odzwierciedlic.

### Handoff points

- Po identyfikacji R z RAG Czerwonym - skill PROPONUJE wywolanie `status-report-drafter-pl` (RAG sprawy moze sie zmienic).
- Po identyfikacji D z istotnym wplywem na zakres - skill PROPONUJE wywolanie `scope-change-controller-pl` (czy nie wymaga aneksu).

## 7. Kalibracja per sprawa

W `[Sprawa]_LPM_Memory.md`:

```markdown
## Trend RAID

### Aktywne ryzyka (na 2026-05-21)
- R-2026-05-001 (Czerwony): brak opinii bieglej -> termin pisma do WSA 5.06 zagrozony
- R-2026-04-014 (Bursztynowy): mozliwe zazalenie kontrkancelarii na postanowienie z 12.04
- R-2026-04-008 (Zielony): klient moze zmienic strategie po wyniku rozprawy 28.05

### Otwarte zalozenia
- Z-2026-05-003: klient ma wewnetrzny deadline biznesowy do 30.06 (walidacja: zapytac wprost)
- Z-2026-04-019: wspolnik prowadzacy ma dostepnosc w czerwcu (walidacja: kalendarz)

### Otwarte problemy
- P-2026-05-002: biegly nie odpowiada na 3 ponaglenie (od 28.04, eskalacja w 24.05)

### Ostatnie decyzje
- D-2026-05-001 (15.05): zlozenie repliki w wersji rozszerzonej, decydent: wspolnik
- D-2026-04-008 (22.04): rozszerzenie scope sprawy z akceptacja klienta (wniosek 22.04, akceptacja 28.04)

### Trend
- Sprawa miala RAG Zielony przez 6 tyg, w ostatnich 2 tyg Bursztynowy/Czerwony.
- Glowne ryzyko: brak wsparcia biegley.
```

## 8. Antywzorce (czego skill NIE robi)

### NIE klasyfikuje wszystkiego jako ryzyko

Sygnal nieklasyfikowany lepiej zostawic w "notatkach" niz wepchnac do RAID jako R. RAID przestaje byc uzyteczny gdy ma 200 ryzyk.

### NIE miesza Ryzyka z Problemem

R = nie nastapilo. P = juz nastapilo. Skill NIE klasyfikuje "biegly nie odpowiedzial" jako R - to P.

### NIE wstawia konkretnych kwot odpowiedzialnosci odszkodowawczej

Skill flaguje "ryzyko odszkodowania za przegrana sprawe" - bez liczby. Liczbe oblicza prawnik na podstawie wniosku pozwu.

### NIE klasyfikuje konfliktu interesow bez konsultacji

Konflikt = obligatoryjna konsultacja wspolnik zarzadzajacy. Skill flaguje + propozycja eskalacji, NIE rozstrzyga sam.

### NIE klasyfikuje RODO incydentu bez procedury

RODO incydent = procedura wewnetrzna kancelarii + ewentualne zgloszenie UODO w 72h. Skill flaguje + krytyczna eskalacja, NIE decyduje czy zglaszac do UODO.

### NIE nazywa konkretnych firm/osob

"Bieglosc nie odpowiada" - tak. "Mgr Iksinski sie miga" - nie. Skill operuje rola (biegla, wspolnik, klient), nie imieniem.

---

## Wymagane sprawdzenia (przed wyslaniem eskalacji)

```
PRZED WYSLANIEM ESKALACJI 5 PUNKTOW:

1. Otworz [Sprawa]_eskalacja_[YYYY-MM-DD].md i przejrzyj.
2. Sprawdz czy adresat eskalacji jest wlasciwy (zespol/wspolnik/klient).
3. Sprawdz czy poziom alarmu odpowiada faktycznemu ryzyku (nie krzyk wilkiem przy niskim).
4. Sprawdz czy nie wycieka tajemnica innej sprawy.
5. Sprawdz czy data deadline'u decyzji jest realna (klient potrzebuje czasu).

Skill jest ASYSTENTEM. Decyzja o wyslaniu - tylko prawnik.
```

---

## Dziennik szlifu

- **2026-05-21** v0.1.0 - pierwsza wersja. Skill #3 z MVP lpm-pl. Cztery kategorie RAID, dwuwymiarowa skala oceny (prawd. x wplyw), 11 typowych polskich ryzyk (termin procesowy, biegly, zazalenie, zawieszenie, konflikt, tajemnica, RODO, dyscyplinarka, pactum, przedawnienie, niezdolnosc procesowa). Cross-skill z status-report-drafter-pl (sygnal RAG) i scope-change-controller-pl (zmiana scope = nowe ryzyko).
