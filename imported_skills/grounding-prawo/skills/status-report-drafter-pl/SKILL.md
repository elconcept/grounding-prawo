---
name: status-report-drafter-pl
version: 0.1.0
description: Tworzy cotygodniowy lub comiesieczny status raport sprawy dla polskiej kancelarii. Konsumuje wklejony watek mailowy / korespondencje z klientem / notatki ze spotkan. Produkuje gotowy do wyslania .docx z naglowkiem kancelarii zawierajacy ocene RAG (Czerwony/Bursztynowy/Zielony) forward-looking, postep z datami, aktywnosc bez postepu, luki, akcje z terminami twardymi, eskalacje. Email-first input, polskie realia billingu (stawki godzinowe / ryczalt / success fee), bez named-firm atrybucji. Uzywaj gdy uzytkownik mowi "zrob status dla sprawy [X]", "raport tygodniowy [klient]", "podsumuj sprawe [X] dla wspolnika", "zaktualizuj status [matter]". NIE uzywaj do raportow finansowych kancelarii (od tego jest billing-cycle-manager), do oferty dla nowego klienta (od tego jest matter-intake-scoping), do raportow strategicznych portfolio (od tego jest daily-briefing). Czyta opcjonalnie z risk-and-issues-manager-pl (rejestr ryzyk per sprawa) i scope-change-controller-pl (zmiany scope w okresie). Pisze do folderu sprawy + aktualizuje [Sprawa]_LPM_Memory.md.
---

# Status Report Drafter (PL)

Skill produkuje gotowy do wyslania status raport polskiej kancelarii. Nie sumaryzator - skill rozumie roznice miedzy postepem a aktywnoscia, traktuje cisze jako sygnal, ocenia RAG patrzac w przyszlosc, eskaluje rzeczy o ktorych klient nie wie a powinien.

## 1. Kiedy uzywac

### Triggery (jezyk uzytkownika)

- "Zrob status dla sprawy [X]"
- "Raport tygodniowy [klient]"
- "Podsumuj sprawe [X] dla wspolnika"
- "Zaktualizuj status [matter ref]"
- "Co sie dzialo na [klient] w tym tygodniu"
- "Przygotuj raport miesieczny [X]"

### Kiedy NIE uzywac

- Raporty finansowe / billing dla zarzadu - to dziedzina `billing-cycle-manager-pl` (faza 3).
- Ocena nowej sprawy / oferta dla klienta - `matter-intake-scoping-pl` (faza 3).
- Przeglad portfela 40 spraw rownoczesnie - `daily-briefing-pl` (faza 3).
- Notatka ze spotkania bez kontekstu sprawy - zwykle podsumowanie wystarczy.

## 2. Metodyka rdzenia (judgment calls)

Skill kieruje sie 5 zasadami. Te zasady SA wlasciwa wartoscia skilla - to NIE jest sumaryzator.

### 2.1 Postep vs aktywnosc

Postep ma date i mierzalny rezultat. Aktywnosc ma tylko liczbe.

- **Postep**: "27.02 zlozono apelacje w SA Warszawa. 01.03 otrzymano postanowienie o przyjeciu do rozpoznania."
- **Aktywnosc**: "12 telefonow w tym tygodniu, dwie konferencje, korespondencja z 3 swiadkami."

Aktywnosc bez postepu przez 2+ okresy raportowe = sygnal eskalacji. Skill wpisuje aktywnosc do sekcji "Aktywnosc bez postepu" z pytaniem "co blokuje milestone".

### 2.2 Cisza jako sygnal

Brak update'u to status, nie luka inputu. Skill raportuje cisze.

- "Od 14 dni brak odpowiedzi z sadu na wniosek z 5.02." - raportowalne.
- "Bieglosc nie odpowiedziala na piate ponaglenie." - raportowalne i eskaluje.
- "Klient nie potwierdzil stanowiska z 20.02." - raportowalne, eskaluje do partnera.

### 2.3 Kazda akcja ma date twarda + eskalacja

Skill NIE akceptuje akcji bez daty. Format obowiazkowy:

> "Skontaktowac sie z bieglym **do piatku 28.02**; jezeli brak odpowiedzi - **eskalacja do wspolnika w poniedzialek 3.03**."

Bez tych dwoch dat skill wpisuje akcje jako WADLIWA i prosi uzytkownika o uzupelnienie.

### 2.4 RAG forward-looking, nie historyczne

RAG nie ocenia tego co bylo w ostatnich 2 tygodniach. RAG ocenia ryzyko ze sprawa nie dowiezie milestone'ow w nastepnych 2 tygodniach.

- **Zielony**: wszystkie milestone'y w okresie nastepnych 2 tyg wygladaja na pewne. Brak otwartych eskalacji.
- **Bursztynowy**: jeden lub wiecej milestone'ow w zagrozeniu. Skill MUSI dolaczyc "plan powrotu do Zielonego" (co konkretnie zrobic by milestone byl pewny).
- **Czerwony**: milestone'y nie do dowiezienia bez interwencji wspolnika lub klienta. Skill MUSI dolaczyc "sciezke eskalacji" (kto, kiedy, jaka decyzja).

"Na dobrym kursie" bez wskazania milestone'u i terminu - to opinia, nie pomiar. Skill NIE akceptuje.

### 2.5 Eskalacja triage

Skill kazda otwarta sprawe klasyfikuje jako:

- **Poziom zespol** - aplikant/junior to ogarnie. NIE eskalujemy do partnera.
- **Poziom wspolnik** - wymaga uwagi wspolnika prowadzacego, decyzji strategicznej.
- **Poziom klient** - klient musi zadzialac lub wiedziec.

Test eskalacyjny: **"Jezeli sprawa pojdzie zle a partner / klient nie wiedzial - czy to nasza wina raportowa?"**. Jezeli tak - eskalujemy.

## 3. Wejscie

### Pierwotne (email-first)

Uzytkownik wkleja:
- Watek mailowy z Outlooka / Gmail (Ctrl+A, Ctrl+C w widoku watku - skill akceptuje "From: ... Sent: ... To: ... Subject: ..." sklejone razem).
- Korespondencje z klientem (z systemu kancelaryjnego, np. Mecenas, LEX Kancelaria, Comarch IBARD - eksport jako tekst).
- Notatki ze spotkan (markdown, tekst, doc).
- Transkrypcje (z LEX Whisper, Otter, Whisper API).

### Wzbogacenie (opcjonalnie)

Uzytkownik wskazuje sciezke do folderu sprawy. Skill czyta:
- `.docx` (przez markitdown lub bezposrednio jezeli LLM ma dostep).
- `.xlsx` (rejestr godzin / budzet).
- `.pdf` (orzeczenia, postanowienia, pisma sadowe).

### Kalibracja (opcjonalnie)

Plik `[Sprawa]_LPM_Memory.md` w folderze sprawy. Skill go laduje i stosuje preferencje:
- Jak partner nazywa etapy sprawy.
- Preferowany ton (formalny vs zwiezly).
- Progi RAG (czy konserwatywne czy luzne).
- Historia RAG poprzednich okresow (do trendu).
- Pola obowiazkowe dla tego konkretnego klienta.

## 4. Wyjscie

### Format

**Plik .docx** w folderze sprawy:

```
[Sprawa]_status_[YYYY-MM-DD].docx
```

Np: `Klient-ABC_v_Skarb-Panstwa_status_2026-05-21.docx`.

Format .docx jest OBOWIAZKOWY. Bez wyjatkow opartych o "zwiezlosc" / "tylko bullety do partnera" / "klient lubi markdown". Wyjatek tylko gdy EXPLICIT prompt: "daj mi bullety w czacie", "tylko streszczenie do okna".

Wczesniejsze preferencje uzytkownika do markdown w innych skillach NIE sa wystarczajace.

### Struktura sekcji (template w `templates/status_report_template.md`)

1. **Naglowek**: klient | sprawa | okres raportowy | autor | data.
2. **Ocena RAG** (Czerwony / Bursztynowy / Zielony) z uzasadnieniem "patrzac na nastepne 2 tyg".
3. **Postep w okresie** - mierzalne dowiezienia z datami.
4. **Aktywnosc bez postepu** - jezeli sa (sygnal eskalacji).
5. **Luki i cisze** - brak update'ow, czego czekamy, od kiedy.
6. **Akcje na nastepny okres** - kazda z data twarda + eskalacja gdy brak.
7. **Eskalacje** - poziom zespol / wspolnik / klient.
8. **Budzet** (jezeli sa dane): % spalenia ryczaltu lub stawki godzinowej, prognoza-do-konca, ostrzezenia overrun.

### Sciezka zapisu

Domyslnie: `<folder sprawy>/raporty_status/[Sprawa]_status_[YYYY-MM-DD].docx`.

Jezeli folder nie istnieje - skill tworzy.

## 5. Workflow (6 krokow)

### Krok 1 - Identyfikacja sprawy

- Skill prosi o nazwe sprawy lub kod (np. "Klient-ABC v Skarb-Panstwa", "MAT-2026-014").
- Sprawdza czy istnieje folder sprawy / `[Sprawa]_LPM_Memory.md`.
- Jezeli tak - laduje preferencje (Art. 3 Konstytucji, RODO - tylko jezeli uzytkownik EXPLICIT wskazal sciezke).
- Identyfikuje okres raportowy (z kontekstu prompta - "tygodniowy" = ostatnie 7 dni; "miesieczny" = ostatnie 30 dni; albo zapytaj).

### Krok 2 - Ekstrakcja signals

Z inputu wyciaga (per email/notatka):
- Kto co zrobil (rola: aplikant / junior / wspolnik / klient / kontrkancelaria / biegly / sad / inny organ).
- Kiedy (DATA TWARDA, nie "w zeszlym tygodniu").
- Jaki rezultat (mierzalny - postep) vs jaka aktywnosc (bez rezultatu).
- Co czeka (na czyje dzialanie).
- Od kiedy czeka.

Skill kategoryzuje kazdy signal jako: postep / aktywnosc / luka / eskalacja.

### Krok 3 - Identyfikacja luk

Co NIE wynika z inputu ale POWINNO sie pojawic:
- Brak update'u z X od Y dni (X = strona / sad / biegly / klient).
- Brak odpowiedzi na pismo z dnia Z.
- Brak potwierdzenia od klienta na stanowisko z dnia W.

Skill formuluje luki jako pytania w raporcie: "Czy wniosek z 5.02 zostal odebrany? Potwierdzenie zwrotne nie wplynelo do 21.05."

### Krok 4 - Ocena RAG forward-looking

Patrzac na nastepne 2 tyg:
- Jakie milestone'y zaplanowane (rozprawa, termin pisma, deadline klienta).
- Co moze pojsc nie tak (otwarte eskalacje, cisze, scope creep).
- Czy potrzebna interwencja wspolnika / klienta.

Decyzja RAG:
- **Zielony**: milestone'y pewne, brak eskalacji.
- **Bursztynowy**: 1+ milestone w zagrozeniu, MA plan powrotu do Zielonego.
- **Czerwony**: bez interwencji wspolnika/klienta milestone nie do dowiezienia, MA sciezke eskalacji.

Uzasadnienie ZAWSZE pisemne, nie sam kolor.

### Krok 5 - Draft

Wypelnia szablon .docx (`templates/status_report_template.md` -> renderowanie do .docx z naglowkiem kancelarii). Sprawdza per akcja: czy ma date twarda + eskalacje. Brak = oznaczenie WADLIWA i prosba o uzupelnienie.

### Krok 6 - Review checklist

Przed zapisem skill wyswietla uzytkownikowi 6-punktowa checkliste:

```
[ ] Czy RAG ma uzasadnienie "patrzac na nastepne 2 tyg"?
[ ] Czy kazda akcja ma date twarda + eskalacje?
[ ] Czy luki sa nazwane (nie ukryte)?
[ ] Czy nie ma named-firm atrybucji (CMS, Wardynski, etc.)?
[ ] Czy nie ma konkretnych stawek (X PLN/h)?
[ ] Czy zwroty grzecznosciowe pasuja do tonu klienta z [Sprawa]_LPM_Memory.md?
```

Jezeli 6/6 PASS - zapis .docx. Jezeli NIE - skill wymaga uzupelnienia.

Po zapisie skill aktualizuje `[Sprawa]_LPM_Memory.md` o 1-2 linie obserwacji (RAG byl X, glowna eskalacja byla Y, do sledzenia w przyszlym okresie Z).

## 6. Cross-skill handoff

### Czyta od

- `risk-and-issues-manager-pl` - jezeli istnieje rejestr ryzyk dla sprawy, aktywne ryzyka (poziom Czerwony/Bursztynowy) sa zaciagniete do RAG reasoning. Plik: `[Sprawa]_RAID.xlsx` w folderze sprawy.
- `scope-change-controller-pl` - jezeli istnieje rejestr zmian scope w okresie, sa raportowane pod "Budzet" (wplyw na koszt sprawy) i "Eskalacje" (wymagane potwierdzenia klienta).

### Pisze do

- Folder sprawy: `.docx` raport.
- `[Sprawa]_LPM_Memory.md` - aktualizacja po raporcie.
- Opcjonalnie: feed do `daily-briefing-pl` (jezeli istnieje - portfela poziom).

### Handoff points

- Po draft (krok 5) - przed review checklist - skill MOZE wywolac `risk-and-issues-manager-pl` jezeli wykryl nowe ryzyko (np. termin sadowy mijajacy bez przygotowania, kontrkancelaria nieoczekiwany ruch).
- Po review checklist (krok 6) - jezeli RAG Czerwony - skill PROPONUJE wywolanie `scope-change-controller-pl` (czesto Czerwony = scope creep).

## 7. Kalibracja per sprawa - `[Sprawa]_LPM_Memory.md`

Plik trzyma per-sprawa preferencje. Skill go aktualizuje po kazdym raporcie.

Szablon:

```markdown
# [Sprawa] - LPM Memory

## Etapy sprawy (jak partner je nazywa)
- Etap 1: due diligence prawne / faza I
- Etap 2: negocjacje umowy / faza II
- Etap 3: zamkniecie / faza III

## Ton raportow do klienta
- Formalny / zwiezly / techniczny / hybrydowy

## Progi RAG (jezeli klient ma specyfike)
- Zielony: brak otwartych ryzyk poziomu wspolnik+
- Bursztynowy: 1 otwarte ryzyko poziomu wspolnik
- Czerwony: 1+ otwarte ryzyko poziomu klient LUB termin sadowy < 7 dni bez przygotowania

## Pola obowiazkowe dla tego klienta
- Sekcja "Budzet" obowiazkowa (klient ABC chce widziec % spalenia kazdy raport)
- Sekcja "Aktywnosc bez postepu" zawsze (klient XYZ liczy efektywnosc)

## Historia RAG
- 2026-05-21: Bursztynowy (eskalacja: brak odpowiedzi z sadu na wniosek z 5.02)
- 2026-05-14: Zielony
- 2026-05-07: Zielony

## Notatki do sledzenia w przyszlych raportach
- Sprawdzic czy biegly odpowiedzial na 6 ponaglenie (deadline 28.05).
- Klient prosil o eskalacje gdy budzet > 70% (obecnie 62%).
```

## 8. Antywzorce (czego skill NIE robi)

### NIE nazywamy kontrkancelarii imieniem firmowym

ZLE: "CMS w odpowiedzi z 15.02 odrzucil propozycje."
DOBRZE: "Kontrkancelaria w odpowiedzi z 15.02 odrzucila propozycje."

Rygor: skill NIE wie ile pobierajaca firma kosztuje, jakie ma policies, kto tam pracuje. Wstawianie nazwy = ryzyko reputacyjne.

### NIE wstawiamy konkretnych stawek

ZLE: "Wspolnik prowadzacy fakturuje 1200 PLN/h."
DOBRZE: "Wspolnik prowadzacy fakturuje wedle stawki kancelarii (potwierdzic w polityce rozlicen)."

### NIE wymyslamy faktow

Jezeli czegos nie ma w inputcie - sekcja "Luki" jest miejscem na to. NIE wnioskujemy "prawdopodobnie sad odpisze do konca tygodnia". Wnioskujemy "Sad nie odpisal od 14 dni. Sledzic do 28.05; jezeli brak - eskalacja wspolnik".

### NIE proponujemy markdown w czacie zamiast .docx

Konstytucja Art. 3. Status raport jest dokumentem kancelarii. Wyjatek tylko gdy uzytkownik EXPLICIT prosi "daj bullety w czacie".

### NIE pomijamy luki bo "wyglada zle"

Luki sa wartoscia raportu. Partner ktory dostaje raport bez luki ma zlusiona swiadomosc. Skill NIE upiekszna obrazu sprawy.

### NIE oceniamy RAG patrzac wstecz

"W tym tygodniu duzo sie dzialo - Zielony" jest WADLIWE. Skill wymaga: jakie milestone'y w nastepnych 2 tyg, czy zagrozone, czy MA plan.

### NIE proponujemy pactum de quota litis bez ostrzezenia

Polskie prawo (KEA art. 16, KEZRP) ogranicza success fee. Skill NIE proponuje "weznmy 30% od zasadzonego" bez ostrzezenia o ograniczeniach. Decyzja zawsze nalezy do prawnika.

---

## Wymagane sprawdzenia po wygenerowaniu (przed wyslaniem partnerowi)

Skill na koniec wyswietla:

```
PRZED WYSLANIEM PARTNEROWI - 6 PUNKTOW:

1. Otworz [Sprawa]_status_[YYYY-MM-DD].docx i przejrzyj.
2. Sprawdz czy klient i nazwa sprawy sa poprawne (skill mogl zalapac z innego watku).
3. Sprawdz uzasadnienie RAG - czy patrzysz w przyszlosc czy w przeszlosc.
4. Sprawdz akcje - czy kazda ma terminy.
5. Sprawdz tajemnice zawodowa - czy nie wyciekly dane innej sprawy.
6. Zaakceptuj badz odrzuc per sekcja.

Skill jest ASYSTENTEM. Decyzja o wyslaniu - tylko prawnik.
```

---

## Dziennik szlifu

- **2026-05-21** v0.1.0 - pierwsza wersja. Cherry-pick struktury z legalopsconsulting/lpm-skills status-report-drafter v2.2.0. Skrocenie 11 H2 do 8 H2 (wyciety M365 connected mode, output templates do osobnego folderu, Memory Store wbudowane w sekcje 7 kalibracja). Polskie realia: stawki godzinowe / ryczalt / success fee z ograniczeniami; brak AFA; brak phase-based budgets; named-firm rule; .docx z brand szablonem kancelarii.
