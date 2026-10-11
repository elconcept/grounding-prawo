---
name: scope-change-controller-pl
version: 0.1.0
description: Wykrywa scope creep w korespondencji z klientem polskiej kancelarii i klasyfikuje nowe zadania jako (a) miesci sie w pierwotnej ofercie/umowie, (b) jest poza zakresem - wymaga wniosku o rozszerzenie, (c) niejasne - wymaga interpretacji prawnika. Konsumuje pierwotna oferte/umowe + biezacy watek mailowy z klientem. Produkuje albo .docx "Wniosek o rozszerzenie zakresu sprawy" do wyslania klientowi albo notatke wewnetrzna "Mieści sie w pierwotnym zakresie" dla wspolnika prowadzacego. Polskie realia: stawki godzinowe / ryczalt / success fee bez AFA. Uzywaj gdy uzytkownik mowi "klient prosi o X poza zakresem?", "scope creep w sprawie [Y]", "wniosek o rozszerzenie [matter]", "czy to bylo w ofercie", "zmiana zakresu [X]". NIE uzywaj do oceny nowej sprawy (od tego matter-intake-scoping w fazie 3), do raportu finansowego (billing-cycle-manager w fazie 3). Czyta od status-report-drafter-pl (kontekst sprawy z poprzednich raportow), pisze do folderu sprawy + aktualizuje [Sprawa]_LPM_Memory.md (historia scope changes).
---

# Scope Change Controller (PL)

Skill wykrywa scope creep zanim wybuchnie konflikt o fakture. Klasyfikuje nowe zadania, kalkuluje wplyw na budzet i termin, produkuje wniosek do klienta lub notatke wewnetrzna.

## 1. Kiedy uzywac

### Triggery (jezyk uzytkownika)

- "Klient prosi o X w sprawie [Y] - to jeszcze w zakresie?"
- "Scope creep w [matter]"
- "Wniosek o rozszerzenie zakresu sprawy [X]"
- "Czy to bylo w pierwotnej ofercie?"
- "Zmiana zakresu [X]"
- "Klient dodal nowy watek - co zrobic?"

### Kiedy NIE uzywac

- Ocena nowej sprawy / oferta dla nowego klienta - `matter-intake-scoping-pl` (faza 3).
- Raporty finansowe kancelarii - `billing-cycle-manager-pl` (faza 3).
- Status raport sprawy - `status-report-drafter-pl` (skill #1).
- Renegocjacja capu budzetu bez zmiany zakresu - to osobna rozmowa biznesowa.

## 2. Metodyka rdzenia (judgment calls)

### 2.1 Trzy klasy kazdego nowego zadania

Skill kazde nowe zadanie klasyfikuje:

- **W zakresie** - mieści sie w literalnym brzmieniu oferty/umowy. Skill produkuje notatke wewnetrzna z cytatem klauzuli umownej. NIE eskalujemy do klienta.
- **Poza zakresem** - nowe zadanie nie wynika z oferty/umowy. Skill produkuje wniosek o rozszerzenie zakresu do akceptacji klienta PRZED przystapieniem do pracy.
- **Niejasne** - zadanie moze byc interpretowane w obie strony. Skill produkuje notatke decyzyjna dla wspolnika prowadzacego z lista argumentow "za" i "przeciw" + rekomendacja.

Domyslna postawa: w razie watpliwosci klasyfikuj jako **niejasne** + decyzja wspolnika. NIE zalozenie domyslnie "w zakresie" (ryzyko spalonych godzin).

### 2.2 Klauzule zakresu w polskich umowach kancelaryjnych

Skill czyta typowe sformulowania:

- "Reprezentacja w postepowaniu przed sadem I instancji" - zakres I instancji, NIE obejmuje apelacji ani kasacji.
- "Doradztwo prawne w sprawach gospodarczych klienta" - szeroka klauzula, ale skill flaguje jako wymagajaca interpretacji.
- "Sporzadzenie i negocjacja umowy [X]" - jednorazowy zakres, kazdy aneks lub zmiana = poza.
- "Stala obsluga prawna" - hurtowa formula, kazda nowa sprawa per faktura wymaga lookupu.
- "Wynagrodzenie ryczaltowe za rozwiazanie sprawy" - ryczalt obejmuje tylko ten zakres, kazda dodatkowa = poza.

### 2.3 Zmiana zakresu vs eskalacja sprawy

Skill rozroznia:

- **Rozszerzenie zakresu (scope change)** - dodanie nowych zadan/obszarow. Wymaga wniosku do klienta.
- **Eskalacja sprawy (matter escalation)** - sprawa wymaga wiecej zasobow niz zakladano ale w obrebie pierwotnego zakresu. Wymaga renegocjacji budzetu/terminu, NIE zakresu.

Test rozroznienia: **"Czy klauzula umowna pokrywa to zadanie?"**. Jezeli tak -> eskalacja (renegocjacja budzetu). Jezeli nie -> scope change (wniosek o rozszerzenie).

### 2.4 Polskie ograniczenia ustawowe

Skill flaguje sytuacje wymagajace ostrzezenia:

- **Pactum de quota litis** (art. 16 KEA, KEZRP) - jezeli klient proponuje rozszerzenie ze success fee wylacznym - ostrzezenie o ograniczeniach.
- **Konflikt interesow** - jezeli nowy zakres dotyka strony z inna sprawa kancelarii - obligatoryjne sprawdzenie.
- **Termin procesowy** - jezeli rozszerzenie wymaga interwencji w postepowaniu z terminem - flag "pilne, klient musi zaakceptowac do [data]".

## 3. Wejscie

### Wymagane

- **Pierwotny zakres**: oferta podpisana / umowa o swiadczenie pomocy prawnej / oferta cenowa. Format: .docx / .pdf / wkleony tekst.
- **Korespondencja z klientem**: watek mailowy gdzie klient prosi o nowe zadanie. Wklejony tekst lub eksport z systemu.

### Opcjonalne

- **Historia scope changes** z `[Sprawa]_LPM_Memory.md`.
- **Status raporty** z `[Sprawa]/raporty_status/` - kontekst budzetu i postepu.

## 4. Wyjscie

Skill produkuje JEDEN z trzech outputow w zaleznosci od klasyfikacji:

### 4a. "W zakresie" - notatka wewnetrzna

**Plik**: `[Sprawa]_scope_check_[YYYY-MM-DD].md` (markdown, NIE .docx bo to wewnetrzne).

Zawartosc:
- Cytat klauzuli umownej.
- Cytat zapytania klienta.
- Uzasadnienie dlaczego sie miesci.
- Rekomendacja: kontynuuj prace, oznacz godziny standardowo.

### 4b. "Poza zakresem" - wniosek do klienta

**Plik**: `[Sprawa]_wniosek_rozszerzenie_[YYYY-MM-DD].docx` (z naglowkiem kancelarii).

Sekcje (template w `templates/scope_change_request_template.md`):

1. Naglowek - klient, sprawa, data.
2. Pierwotny zakres - cytat klauzuli.
3. Nowe zadanie - opis o co klient prosi.
4. Klasyfikacja - "wykracza poza pierwotny zakres umowy z dnia [X]".
5. Proponowany rozszerzony zakres - co dokladnie dolaczamy.
6. Wplyw budzetowy:
   - Szacowane godziny (jezeli stawka).
   - Dodatkowa kwota (jezeli ryczalt).
   - Success fee z capem (jezeli hybryda).
   - Ostrzezenie o ograniczeniach KEA jezeli pactum de quota litis.
7. Wplyw terminowy - czy zmienia milestone'y sprawy.
8. Decyzja klienta - akceptacja / odrzucenie / negocjacja. Do dnia [X].
9. Klauzula odpowiedzialnosci - skill draft, decyzja wspolnik prowadzacy.

### 4c. "Niejasne" - notatka decyzyjna dla wspolnika

**Plik**: `[Sprawa]_decyzja_scope_[YYYY-MM-DD].md` (markdown wewnetrzny).

Zawartosc:
- Cytat klauzuli.
- Cytat zapytania klienta.
- Argumenty "w zakresie" - lista.
- Argumenty "poza zakresem" - lista.
- Rekomendacja skilla - z uzasadnieniem.
- Pytanie do wspolnika - "Jaka decyzja? [W zakresie | Poza | Drobny aneks bez wniosku formalnego]".

## 5. Workflow (5 krokow)

### Krok 1 - Identyfikacja sprawy + pobranie pierwotnego zakresu

- Skill prosi o nazwe sprawy + sciezke do oferty/umowy.
- Ekstrakcja klauzul zakresu z dokumentu (przez markitdown jezeli .docx).

### Krok 2 - Ekstrakcja zadania z korespondencji

- Skill parsuje watek mailowy.
- Wyciaga: kto prosil (klient / przedstawiciel klienta), o co dokladnie, kiedy, deadline.
- Jezeli watek niejasny - skill prosi o doprecyzowanie ZANIM klasyfikuje.

### Krok 3 - Klasyfikacja

- Porownanie zadania z klauzulami zakresu.
- Sprawdzenie czy nie ma czerwonych flag (konflikt, pactum, termin pilny).
- Decyzja: w zakresie / poza / niejasne.

### Krok 4 - Wybor outputu

- W zakresie -> notatka wewnetrzna (4a).
- Poza -> wniosek do klienta (4b).
- Niejasne -> notatka decyzyjna dla wspolnika (4c).

### Krok 5 - Zapis + aktualizacja kalibracji

- Zapis pliku w folderze sprawy.
- Update `[Sprawa]_LPM_Memory.md` - sekcja "Historia scope changes" z wpisem (data, klasyfikacja, decyzja).
- Jezeli output 4b (wniosek) - skill PROPONUJE wywolanie `status-report-drafter-pl` do aktualizacji najblizszego raportu statusu (scope changed = istotny event).

## 6. Cross-skill handoff

### Czyta od

- `status-report-drafter-pl` - poprzednie raporty statusu (kontekst budzetu, otwartych eskalacji).
- `[Sprawa]_LPM_Memory.md` - historia scope changes.

### Pisze do

- Folder sprawy: `.docx` (wniosek) albo `.md` (notatka).
- `[Sprawa]_LPM_Memory.md` - sekcja "Historia scope changes".
- Opcjonalnie: feed do `risk-and-issues-manager-pl` (kazda zaakceptowana zmiana scope = ryzyko bazowe do RAID).

### Handoff points

- Po klasyfikacji jako "poza zakresem" - skill PROPONUJE update statusu sprawy (RAG moze zmienic kolor).
- Po klasyfikacji jako "niejasne" + decyzja wspolnika "w zakresie" - skill aktualizuje `LPM_Memory` z interpretacja na przyszlosc.

## 7. Kalibracja per sprawa

W `[Sprawa]_LPM_Memory.md` skill trzyma:

```markdown
## Historia scope changes

- 2026-05-14: niejasne, decyzja wspolnika "w zakresie" (klient prosil o konsultacje przed terminem rozprawy; ujeto w klauzuli "doradztwo procesowe")
- 2026-04-22: poza zakresem, klient zaakceptowal rozszerzenie (+15h, kwota X PLN, termin do 2026-05-30)
- 2026-04-05: w zakresie, kontynuacja bez wniosku
```

Skill uczy sie ze ten klient/wspolnik ma okreslony stylem interpretacji klauzul. Przy kolejnych zapytaniach proponuje pierwsze klasyfikacje na podstawie historii.

## 8. Antywzorce (czego skill NIE robi)

### NIE proponuje "w razie watpliwosci w zakresie"

Domyslna postawa: niejasne -> decyzja wspolnika. NIE zakladamy domyslnie "w zakresie" bo to ryzyko spalonych godzin.

### NIE wystawia faktury / cennika konkretnego

Skill nie wie ile fakturuje kancelaria. Mowi "stawka godzinowa kancelarii" / "polityka rozlicen kancelarii". Konkretne liczby - wspolnik prowadzacy uzupelnia recznie.

### NIE wysyla wniosku do klienta samodzielnie

Output skilla to .docx ZAPISANY w folderze sprawy. Wyslanie - decyzja prawnika po przegladzie.

### NIE proponuje pactum de quota litis

Polskie prawo (art. 16 KEA, KEZRP) ogranicza success fee. Skill NIE proponuje "wezmemy 30% od zasadzonego" bez ostrzezenia. Jezeli wykryje w propozycji klienta - flag czerwony.

### NIE pomija konfliktu interesow

Jezeli nowy zakres dotyka strony przeciwnej z innej sprawy kancelarii - obligatoryjne sprawdzenie. Skill NIE klasyfikuje bez tej weryfikacji.

### NIE klasyfikuje gdy korespondencja jest niejasna

Jezeli klient prosi "rozumiesz mnie, ogarniecie?" bez konkretu - skill PROSI o doprecyzowanie ZANIM klasyfikuje. Bez konkretu nie ma scope change do oceny.

---

## Wymagane sprawdzenia (przed wyslaniem wniosku klientowi)

```
PRZED WYSLANIEM 4-PUNKTY:

1. Otworz [Sprawa]_wniosek_rozszerzenie_[YYYY-MM-DD].docx i przejrzyj.
2. Sprawdz czy cytat klauzuli umownej jest doslowny.
3. Sprawdz czy zaproponowany budzet rozszerzenia jest realny (uzgodnij z partnerem).
4. Sprawdz czy nie ma konfliktu interesow w nowym zakresie.

Skill jest ASYSTENTEM. Decyzja o wyslaniu - tylko prawnik.
```

---

## Dziennik szlifu

- **2026-05-21** v0.1.0 - pierwsza wersja. Skill #2 z MVP lpm-pl. Trzy klasy zadania (w zakresie / poza / niejasne), trzy outputy (notatka / wniosek / decyzja). Polskie realia: art. 16 KEA, konflikt interesow, brak AFA. Cross-skill z status-report-drafter-pl (kontekst sprawy) i risk-and-issues-manager-pl (zmiany scope -> ryzyka).
