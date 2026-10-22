# Typ pisma: cofnięcie pozwu ze zrzeczeniem się roszczenia

> Moduł scalony ze skilla `cofniecie-pozwu-ze-zrzeczeniem-roszczenia` (IURA). Stosuj w W1/W2 jako wzorzec struktury i argumentacji dla tego typu pisma; bramki `pisma-procesowe-v3` obowiązują bez zmian.

> **Pliki przebiegu (reguła kanoniczna):** zapisuj według `shared/ARTEFAKTY-SPRAWY.md` - nowym plikiem jest
> tylko wersja wynikowa (`drafty/<pismo>/rrrrMMdd_<nazwa>_vN.*`); logi, raporty, ustalenia i recapy przebiegu
> dopisuj do istniejących plików inkrementalnych (`_PRZEBIEGI.md`, `_SUBSUMPCJA*.md`, `_FINDINGS.md` …), a pliki
> jednorazowe zostawiaj w `_robocze/` sprawy.

# Cofnięcie pozwu wraz ze zrzeczeniem się roszczenia

Skill generuje pismo procesowe strony powodowej o cofnięcie pozwu wraz ze zrzeczeniem się roszczenia, przeznaczone do złożenia w sądzie cywilnym. Pismo jest generowane w formacie `.docx` zgodnie ze standardami polskiej praktyki procesowej.

> **Wymagane narzędzia:** skill wymaga konektora MCP **ustawy + Repertorium** (`ustawy_akty`, `repertorium_szukaj_repertorium`, `ustawy_artykul` — Dziennik Ustaw przez Sejm ELI API) do weryfikacji aktualnego brzmienia KPC. Pomocniczo **SAOS** (`search`) dla praktyki orzeczniczej. Bez ELI **nie generuj pisma** — ryzyko powołania się na nieaktualne lub nieistniejące przepisy. Instalacja: `Codex mcp add isap -s user -- npx -y @matematicsolutions/ustawy`. Składnia zapytań i pułapki ELI: `patron-prawo-pl-zrodla` (referencja `iura-metodyka.md`).

---

## ZASADA FUNDAMENTALNA: Weryfikacja podstaw prawnych przed generowaniem

**ZAWSZE przed napisaniem pisma pobierz aktualny tekst KPC z ELI.** ELI **nie ma** parametru `in_force_as_of` i domyślnie serwuje **tekst ogłoszony** (brzmienie pierwotne z 1964 r.) — obowiązuje procedura trzykrokowa:

```
1. ustawy_akty(tytuł: "Kodeks postępowania cywilnego")
2. repertorium_szukaj_repertorium(eli: <akt bazowy>)  → weź NAJNOWSZY consolidated_text_eli
3. ustawy_artykul(eli: <tekst jednolity>, search_text: "Art. 203.")
```

Cytuj wyłącznie wtedy, gdy `structuredContent.text_version` = `tekst_jednolity` **i** `in_force` = `IN_FORCE`. Każdy inny wariant to materiał historyczny.

Dla głównych kodeksów `ustawy_artykul` na obowiązującym tekście jednolitym zwróci `text_unavailable_use_pdf` — to **sytuacja typowa**, nie awaria: świeże obwieszczenia publikowane są wyłącznie w PDF. **Nie schodź wtedy do starszego tekstu jednolitego** — sięgnij po PDF:

Narzędzie `ustawy_artykul` z `search_text: "Art. N."`; przy `text_unavailable_use_pdf` pobierz PDF tekstu jednolitego z adresu w odpowiedzi (`curl`) i odczytaj go przez `pdftotext -layout` (`shared/MOD-TEKST-JEDNOLITY.md`, szczebel 1).

PDF-y ELI mają prawdziwą warstwę tekstu, więc to zwraca brzmienie **obowiązujące dziś**. Cytuj tylko przy `status: FOUND` + `text_version: tekst_jednolity` + `status_obowiazywania: obowiazuje`; `status: AMBIGUOUS` oznacza, że trafiłeś na akt bazowy (brzmienie pierwotne) — powtórz z ELI z pola `uzyj_zamiast`. Cytat dosłowny zweryfikuj wzrokowo w PDF (ekstrakcja gubi pojedyncze spacje; w `--find` podawaj zwykłe `Art. 205.`, nie `Art. 205¹.`). Gdy PDF niedostępny — plan B to starszy tekst jednolity z HTML, zacytowany z **wyraźną datą** i adnotacją o późniejszych nowelizacjach. Pełna drabinka: `patron-prawo-pl-zrodla` (referencja `iura-metodyka.md`), sekcja 4.

**Nigdy nie zgaduj brzmienia z samego linku do PDF i nigdy nie podstawiaj aktu bazowego** (KPC z 1964 r.) jako brzmienia obowiązującego.

Zweryfikuj tak brzmienie przepisów dotyczących:

1. **Cofnięcia pozwu i zrzeczenia się roszczenia** — `ustawy_artykul(search_text: "Art. 203.")`, a dla umorzenia `search_text: "Art. 355."`
2. **Wymogów formalnych pisma procesowego** — `ustawy_artykul(search_text: "Art. 126.")`
3. **Doręczenia odpisu pisma pełnomocnikowi strony przeciwnej** — `ustawy_artykul(search_text: "Art. 132.")`

Numery artykułów powyżej to **hipotezy do sprawdzenia**, nie podstawa prawna pisma: dopiero tekst zwrócony przez `ustawy_artykul` potwierdza, że przepis brzmi tak, jak zakładasz, i nie został przeniesiony ani uchylony. Pisownia w `search_text` musi mieć polskie znaki — ELI jest na to wrażliwy.

Opcjonalnie (praktyka orzecznicza kosztów przy cofnięciu): SAOS `search(courtType: "COMMON", legalBase: "art. 203 kpc", all: "zrzeczenie się roszczenia")` — sprawdzone, zwraca orzeczenia z 2026 r. W SN `legalBase` nie działa, a pokrycie SAOS dla SN kończy się na 2016 r.

Dopiero po potwierdzeniu brzmienia przepisów przystąp do generowania pisma. Powołuj się wyłącznie na przepisy potwierdzone tekstem aktu.

---

## Zbieranie danych od użytkownika

Przed wygenerowaniem pisma musisz ustalić z użytkownikiem następujące dane. Jeśli użytkownik nie podał ich w swojej wiadomości, zapytaj o brakujące elementy. Poniżej podano każdy element z adnotacją, czy jest wymagany, czy opcjonalny:

### Dane identyfikujące sprawę

| Element | Wymagany? | Opis |
|---------|-----------|------|
| Nazwa sądu | TAK | Pełna nazwa sądu i wydziału (np. „Sąd Rejonowy dla m.st. Warszawy, XII Wydział Gospodarczy") |
| Adres sądu | TAK | Ulica i kod pocztowy sądu |
| Sygnatura akt | TAK | Numer sygnatury sprawy (np. „XII GC 1234/25") |

### Dane strony powodowej

| Element | Wymagany? | Opis |
|---------|-----------|------|
| Nazwa/imię i nazwisko | TAK | Pełna nazwa firmy lub imię i nazwisko osoby fizycznej |
| Adres | TAK | Adres siedziby lub zamieszkania |
| PESEL / KRS / NIP | TAK | Identyfikator — PESEL dla osób fizycznych, KRS i/lub NIP dla podmiotów gospodarczych |
| E-mail | NIE | Adres e-mail strony (jeśli dostępny) |
| Pełnomocnik | NIE | Tylko gdy stronę reprezentuje pełnomocnik: imię i nazwisko |
| E-mail pełnomocnika | NIE | Adres e-mail pełnomocnika |
| Telefon pełnomocnika | NIE | Numer telefonu do kontaktu z sądem |
| Adres do doręczeń | NIE | Jeśli inny niż adres strony (zwykle adres kancelarii pełnomocnika) |

### Dane strony pozwanej

| Element | Wymagany? | Opis |
|---------|-----------|------|
| Nazwa/imię i nazwisko | TAK | Pełna nazwa firmy lub imię i nazwisko osoby fizycznej |
| Adres | TAK | Adres siedziby lub zamieszkania |
| KRS / NIP / PESEL | TAK | Identyfikator strony pozwanej |
| Pełnomocnik | NIE | Jeśli strona pozwana jest reprezentowana przez pełnomocnika |
| Adres do doręczeń pełnomocnika | NIE | Adres kancelarii pełnomocnika strony pozwanej |

### Okoliczności cofnięcia

| Element | Wymagany? | Opis |
|---------|-----------|------|
| Przyczyna cofnięcia | TAK | Np. zawarcie ugody, spełnienie świadczenia, utrata interesu prawnego, inna przyczyna |
| Data zdarzenia uzasadniającego | NIE | Data zawarcia ugody, spełnienia świadczenia itp. |
| Numer/oznaczenie umowy będącej przedmiotem sporu | NIE | Jeśli spór dotyczył konkretnej umowy |
| Czy zrzeczenie obejmuje koszty procesu? | TAK | Czy powód zrzeka się także roszczeń o zwrot kosztów procesu i zastępstwa procesowego |
| Sposób doręczenia odpisu | TAK | Poczta tradycyjna (operator wyznaczony) lub doręczenie elektroniczne |
| Etap postępowania | NIE | Czy odbyła się już rozprawa — ma znaczenie dla wymogu zgody pozwanego przy cofnięciu bez zrzeczenia |
| Załączniki | NIE | Lista dokumentów dołączanych do pisma (np. ugoda) |

---

## Struktura pisma — wzorzec obowiązkowy

Pismo MUSI zachować dokładnie poniższą strukturę i kolejność elementów. Jest to wzorzec oparty na polskiej praktyce procesowej — każdy element pełni określoną funkcję proceduralną.

### 1. NAGŁÓWEK — data i miejscowość

Prawy górny róg: `[Miejscowość], [data]`

Miejscowość to miasto, w którym działa pełnomocnik (lub strona, jeśli działa bez pełnomocnika). Data to dzień sporządzenia pisma.

### 2. OZNACZENIE SĄDU

Pełna nazwa sądu z wydziałem i adresem. Sąd jest adresatem pisma — umieszczany na początku, w konwencji korespondencji urzędowej.

### 3. OZNACZENIE STRON

Kolejność: **najpierw strona powodowa, potem strona pozwana.** Każda strona formatowana jest jako odrębny blok z wcięciami. Formatowanie musi odzwierciedlać następujący wzorzec wizualny:

```
Strona Powodowa: [Pełna nazwa / imię i nazwisko]
  Ul. [Adres]
  PESEL: [numer] / KRS: [numer] / NIP: [numer]
  e-mail: [adres e-mail]

reprezentowany przez:
  [imię i nazwisko pełnomocnika]
  e-mail pełnomocnika: [adres]
  tel. do kontaktu z sądem: [numer]

adres dla doręczeń:
  [adres kancelarii pełnomocnika]
```

Każdy element (imię, adres, identyfikator, e-mail, dane pełnomocnika, adres do doręczeń) umieszczaj w **osobnym wierszu** z wcięciem. Fraza „reprezentowany przez:" poprzedza dane pełnomocnika. Fraza „adres dla doręczeń:" poprzedza adres do korespondencji.

Oznaczenie stron musi być zgodne z wymogami formalnymi pisma procesowego wynikającymi z przepisów KPC (zweryfikuj przez `ustawy_artykul` na tekście jednolitym KPC, `search_text: "Art. 126."`).

### 4. SYGNATURA AKT

`Sygn. akt: [sygnatura]`

### 5. TYTUŁ PISMA — dwuczłonowy

Tytuł składa się z dwóch linii:
```
PISMO STRONY POWODOWEJ
COFNIĘCIE POZWU WRAZ Z ZRZECZENIEM SIĘ ROSZCZENIA
```

Pierwsza linia identyfikuje rodzaj pisma procesowego i autora (stronę). Druga linia precyzuje czynność procesową. Taka dwuczłonowa konwencja jest standardem polskiej praktyki sądowej — ułatwia sądowi klasyfikację pisma.

### 6. TREŚĆ MERYTORYCZNA — petitum i uzasadnienie

To najważniejsza część pisma. Treść formułowana jest jako **jedno zwięzłe oświadczenie procesowe**, które łączy w sobie elementy opisane poniżej w mechanizmie argumentacji.

#### 6.1 Mechanizm argumentacji prawniczej

Treść pisma o cofnięcie pozwu opiera się na następującym schemacie argumentacyjnym — jest to zwięzły, jednoparagrafowy wywód procesowy, w którym każdy element pełni określoną funkcję:

**a) Legitymacja do działania** — zdanie otwierające musi wskazać, w czyim imieniu pełnomocnik działa i na jakiej podstawie:
> „Działając w imieniu Strony Powodowej, na podst. pełnomocnictwa znajdującego się w aktach sprawy, …"

Funkcja: Potwierdza umocowanie procesowe — sąd musi mieć pewność, że osoba składająca oświadczenie jest uprawniona do dokonywania czynności dyspozytywnych w imieniu strony.

**b) Przyczyna cofnięcia** — bezpośrednio po legitymacji, wskazanie okoliczności faktycznej uzasadniającej cofnięcie:
> „…w związku z zawarciem w dniu [data] ugody ze Stroną Pozwaną, dotyczącej [oznaczenie przedmiotu sporu], …"

Funkcja: Wskazuje przyczynę czynności procesowej. Sąd bada, czy cofnięcie pozwu nie jest sprzeczne z prawem, zasadami współżycia społecznego ani nie zmierza do obejścia prawa — dlatego podanie przyczyny, choć nie zawsze wymagane formalnie, wzmacnia pozycję procesową i przyspiesza rozpoznanie wniosku.

**c) Oświadczenie o cofnięciu pozwu ze zrzeczeniem się roszczenia** — rdzeń pisma:
> „…niniejszym cofam Pozew wraz z zrzeczeniem się roszczenia dochodzonego w niniejszej sprawie, …"

Funkcja: Jest to czynność dyspozytywna strony powodowej — połączenie cofnięcia pozwu z zrzeczeniem się roszczenia ma kluczowe znaczenie procesowe, ponieważ eliminuje konieczność uzyskania zgody strony pozwanej na cofnięcie (zweryfikuj aktualne brzmienie przez `ustawy_artykul` na tekście jednolitym KPC, `search_text: "Art. 203."`). Bez zrzeczenia się roszczenia, po rozpoczęciu rozprawy wymagana jest zgoda pozwanego.

**d) Rozstrzygnięcie o kosztach** — opcjonalne, ale rekomendowane:
> „…jak również zrzekam się roszczeń dotyczących zwrotu przez Stronę Pozwaną kosztów procesu i zastępstwa procesowego."

Funkcja: Zrzeczenie się roszczeń kosztowych zapobiega sporowi o koszty po umorzeniu postępowania. Jeśli strony zawarły ugodę regulującą koszty — oświadczenie powinno być z nią spójne.

#### 6.2 Uwagi stylistyczne dotyczące treści merytorycznej

- Każda fraza treści merytorycznej to **jedno nieprzerwane zdanie** — nie rozbijaj na osobne akapity ani punkty. Zwięzłość i ciągłość wywodu świadczą o profesjonalizmie. Taki styl — długi okres zdaniowy z rozbudowanymi okolicznikami — jest typowy dla polskiego stylu pism procesowych.
- Używaj wielkiej litery dla ról procesowych: „Strona Powodowa", „Strona Pozwana", „Pozew".
- Skrót „podst." zamiast „podstawie" jest dopuszczalny w pismach procesowych.
- „r." jako skrót od „roku" — standardowy zapis daty w pismach sądowych (np. „w dniu 15 marca 2026 r.").
- „k.p.c." — standardowy skrót Kodeksu postępowania cywilnego.
- Zwrot „niniejszym cofam" — tryb oznajmujący, nie „wnoszę o cofnięcie" (bo cofnięcie to czynność strony, nie wniosek do sądu).

#### 6.3 Wzorcowe frazy treści merytorycznej — warianty

Poniższe frazy są sparametryzowane — elementy w nawiasach kwadratowych `[...]` zastąp danymi od użytkownika. Każda fraza została skonstruowana według schematu argumentacyjnego: **legitymacja → przyczyna → oświadczenie o cofnięciu → koszty**. Zachowaj ciągłość zdania.

##### Wariant A: Cofnięcie po ugodzie (z pełnomocnikiem, ze zrzeczeniem kosztów)

Przyczyna: zawarcie ugody (sądowej lub pozasądowej). Załącznik: kopia ugody.

```
Działając w imieniu Strony Powodowej, na podst. pełnomocnictwa znajdującego się w aktach sprawy, w związku z zawarciem w dniu [DATA UGODY] r. ugody ze Stroną Pozwaną, dotyczącej [OZNACZENIE PRZEDMIOTU SPORU, np. „Umowy nr XYZ z dnia ..."] będącej przedmiotem niniejszego sporu, niniejszym cofam Pozew wraz z zrzeczeniem się roszczenia dochodzonego w niniejszej sprawie, jak również zrzekam się roszczeń dotyczących zwrotu przez Stronę Pozwaną kosztów procesu i zastępstwa procesowego.
```

##### Wariant B: Cofnięcie po spełnieniu świadczenia (z pełnomocnikiem, BEZ zrzeczenia kosztów)

Przyczyna: pozwany spełnił dochodzone świadczenie. Rozważenie: powód wygrał merytorycznie — może żądać kosztów.

```
Działając w imieniu Strony Powodowej, na podst. pełnomocnictwa znajdującego się w aktach sprawy, wobec spełnienia przez Stronę Pozwaną w dniu [DATA SPEŁNIENIA] r. świadczenia dochodzonego w niniejszym postępowaniu, niniejszym cofam Pozew wraz z zrzeczeniem się roszczenia dochodzonego w niniejszej sprawie.
```

Uwaga: W tym wariancie powód nie zrzeka się roszczeń o koszty, ponieważ pozwany spełnił świadczenie dopiero po wytoczeniu powództwa — powód wygrał merytorycznie i może żądać kosztów.

##### Wariant C: Cofnięcie z innej przyczyny (z pełnomocnikiem, ze zrzeczeniem kosztów)

Przyczyna: utrata interesu prawnego, zmiana okoliczności, decyzja biznesowa.

```
Działając w imieniu Strony Powodowej, na podst. pełnomocnictwa znajdującego się w aktach sprawy, wobec [OPIS PRZYCZYNY, np. „utraty interesu prawnego w dalszym dochodzeniu roszczenia" / „zmiany okoliczności faktycznych" / „podjęcia decyzji o zakończeniu sporu"], niniejszym cofam Pozew wraz z zrzeczeniem się roszczenia dochodzonego w niniejszej sprawie, jak również zrzekam się roszczeń dotyczących zwrotu przez Stronę Pozwaną kosztów procesu i zastępstwa procesowego.
```

##### Wariant D: Cofnięcie częściowe (z pełnomocnikiem)

Cofnięcie dotyczy tylko części roszczenia. Treść musi precyzyjnie wskazać, która część roszczenia jest cofana, a która podtrzymywana. Zrzeczenie się roszczenia dotyczy tylko cofniętej części.

```
Działając w imieniu Strony Powodowej, na podst. pełnomocnictwa znajdującego się w aktach sprawy, w związku z [PRZYCZYNA CZĘŚCIOWEGO COFNIĘCIA], niniejszym cofam Pozew w części dotyczącej [PRECYZYJNE OKREŚLENIE COFNIĘTEJ CZĘŚCI ROSZCZENIA, np. „roszczenia o zapłatę kwoty X zł tytułem ..." / „roszczenia o ..."], wraz z zrzeczeniem się roszczenia w tym zakresie, podtrzymując Pozew w pozostałej części, tj. w zakresie [PRECYZYJNE OKREŚLENIE PODTRZYMANEJ CZĘŚCI ROSZCZENIA].
```

##### Wariant E: Cofnięcie bez pełnomocnika (strona działa osobiście)

Strona działa we własnym imieniu — brak frazy o pełnomocnictwie. W kosztach brak „zastępstwa procesowego", bo strona nie jest reprezentowana przez profesjonalnego pełnomocnika.

```
W związku z [PRZYCZYNA COFNIĘCIA, np. „zawarciem w dniu [DATA] r. ugody ze Stroną Pozwaną, dotyczącej ..."], niniejszym cofam Pozew wraz z zrzeczeniem się roszczenia dochodzonego w niniejszej sprawie, jak również zrzekam się roszczeń dotyczących zwrotu przez Stronę Pozwaną kosztów procesu.
```

**WAŻNE O ETAPIE POSTĘPOWANIA:** Połączenie cofnięcia pozwu ze zrzeczeniem się roszczenia jest kluczowe procesowo — eliminuje wymóg zgody pozwanego niezależnie od etapu postępowania. Jeśli jednak użytkownik chce cofnąć pozew **bez** zrzeczenia się roszczenia, poinformuj go, że po rozpoczęciu rozprawy wymagana będzie zgoda pozwanego (zweryfikuj aktualne brzmienie przez `ustawy_artykul`, `search_text: "Art. 203."`). Skill domyślnie generuje wariant **ze** zrzeczeniem się roszczenia — chyba że użytkownik wyraźnie poprosi o inny wariant.

### 7. OŚWIADCZENIE O DORĘCZENIU

Osobny akapit zawierający oświadczenie o wysłaniu odpisu pisma stronie przeciwnej lub jej pełnomocnikowi. Konkretny artykuł KPC zweryfikuj przez `ustawy_artykul` na tekście jednolitym KPC (`search_text: "Art. 132."`, ewentualnie `"operator pocztowy"`). Nie wpisuj artykułu z pamięci — hipoteza wolno, cytat dopiero po potwierdzeniu tekstem.

Wybierz odpowiedni wariant oświadczenia o doręczeniu w zależności od okoliczności:

#### Do pełnomocnika strony pozwanej (z załącznikami):
```
Oświadczam, że odpis niniejszego pisma wraz z załącznikiem/załącznikami został nadany pełnomocnikowi Strony Pozwanej za pośrednictwem operatora, o którym mowa w art. [X] § [Y] k.p.c.
```

#### Bezpośrednio do strony pozwanej (bez pełnomocnika, z załącznikami):
```
Oświadczam, że odpis niniejszego pisma wraz z załącznikiem/załącznikami został nadany Stronie Pozwanej za pośrednictwem operatora, o którym mowa w art. [X] § [Y] k.p.c.
```

#### Bez załączników:
```
Oświadczam, że odpis niniejszego pisma został nadany pełnomocnikowi Strony Pozwanej za pośrednictwem operatora, o którym mowa w art. [X] § [Y] k.p.c.
```

#### Doręczenie elektroniczne:
```
Oświadczam, że odpis niniejszego pisma wraz z załącznikiem/załącznikami został doręczony pełnomocnikowi Strony Pozwanej drogą elektroniczną na adres e-mail: [EMAIL].
```

Dostosowania wariantowe:
- **Strona pozwana bez pełnomocnika** — zamień „pełnomocnikowi Strony Pozwanej" na „Stronie Pozwanej"
- **Pismo bez załączników** — usuń frazę „wraz z załącznikiem/załącznikami"
- **Jeden załącznik** — użyj formy „wraz z załącznikiem"; **wiele załączników** — „wraz z załącznikami"

### 8. PODPIS

Linia podpisu zawiera:
- Kreskę/linię na podpis
- Imię i nazwisko podpisującego (strona działająca osobiście: bez tytułu zawodowego i numeru wpisu)

### 9. LISTA ZAŁĄCZNIKÓW

Na końcu pisma, po podpisie:
```
Załącznik:
1. [nazwa dokumentu] z dnia [data]
```

Lub w przypadku wielu załączników:
```
Załączniki:
1. [nazwa dokumentu 1]
2. [nazwa dokumentu 2]
```

---

## Adaptacja do stanu faktycznego

Pismo musi być **dopasowane do konkretnej sytuacji** użytkownika. Mechanizm adaptacji:

1. **Przyczyna cofnięcia** kształtuje zdanie uzasadniające w treści merytorycznej — zamień wzorcową frazę „w związku z zawarciem ugody" na frazę odpowiadającą rzeczywistej przyczynie (dobierz odpowiedni wariant A–E z sekcji 6.3)
2. **Strona bez pełnomocnika** — pomiń sekcje dotyczące pełnomocnika, legitymację formułuj w pierwszej osobie („niniejszym cofam Pozew") bez odwołania do pełnomocnictwa (wariant E)
3. **Strona z pełnomocnikiem** — legitymację formułuj przez odwołanie do pełnomocnictwa w aktach (warianty A–D)
4. **Osoba fizyczna vs. podmiot gospodarczy** — dostosuj identyfikatory (PESEL vs. KRS/NIP)
5. **Koszty procesu** — jeśli użytkownik nie chce zrzekać się kosztów, pomiń fragment o zrzeczeniu się roszczeń kosztowych (wariant B)
6. **Cofnięcie częściowe** — dodaj precyzyjne określenie zakresu cofnięcia (wariant D)

---

## Generowanie dokumentu .docx

Po zebraniu danych i weryfikacji podstaw prawnych, wygeneruj pismo w formacie `.docx` korzystając z instrukcji ze skilla `docx`.

### Wytyczne formatowania:
- **Czcionka**: Georgia 10 pt albo krój zbliżony; nadawca i organ 14 pt. Wygląd pliku: `shared/FORMAT-PISMA.md` (ma pierwszeństwo) - wynik to DOCX z sidecarem .md, bez PDF; Georgia 10 pt, nadawca i organ 14 pt, wydział 12 pt, adresat do prawej, adres w jednej linii, telefon i e-mail nadawcy, pogrubienie i podkreślenie tylko dla tez; plik generuje `shared/format-pisma/render_pismo.py`.
- **Marginesy**: 2,5 cm ze wszystkich stron
- **Odstęp między wierszami**: 1,5 wiersza w treści merytorycznej, 1,0 w nagłówku i oznaczeniu stron
- **Wyrównanie**: nagłówek (data) — do prawej; oznaczenie sądu — do lewej; oznaczenie stron — do lewej; tytuł — wycentrowany, rozstrzelone wersaliki, bez pogrubienia; treść — wyjustowana; podpis — do prawej
- **Styl**: formalny, profesjonalny, bez emotikon, bez kolokwializmów
- **Kodowanie polskich znaków**: upewnij się, że czcionka obsługuje polskie znaki diakrytyczne (ą, ę, ć, ń, ó, ś, ź, ż, ł)

---

## Schemat wywoływania narzędzi — podsumowanie

```
1. ustawy_akty(tytuł: "Kodeks postępowania cywilnego")
   → ELI aktu bazowego

2. repertorium_szukaj_repertorium(eli: <akt bazowy>)
   → NAJNOWSZY consolidated_text_eli (obwieszczenie z tekstem jednolitym)

3. ustawy_artykul(eli: <jednolity>, search_text: "Art. 203.")     → cofnięcie + zrzeczenie
   ustawy_artykul(eli: <jednolity>, search_text: "Art. 355.")     → umorzenie postępowania
   ustawy_artykul(eli: <jednolity>, search_text: "Art. 126.")     → wymogi formalne pisma
   ustawy_artykul(eli: <jednolity>, search_text: "Art. 132.")     → doręczenie odpisu
   → za każdym razem sprawdź text_version = tekst_jednolity oraz in_force = IN_FORCE

4. (opcjonalnie) saos: search(courtType: "COMMON", legalBase: "art. 203 kpc")
   → praktyka orzecznicza, m.in. koszty przy cofnięciu

5. Potwierdzone przepisy → wstaw do treści pisma (numery artykułów, paragrafy)
6. Wygeneruj .docx zgodnie ze strukturą powyżej
```

**NIGDY nie wpisuj numerów artykułów z pamięci jako podstawy prawnej.** Pamięć wolno użyć tylko do postawienia hipotezy, który artykuł sprawdzić — treść przepisu w piśmie musi pochodzić z `ustawy_artykul` na tekście jednolitym.

---

## Checklist kontrolny przed wydaniem pisma użytkownikowi

Przed zapisaniem finalnego pliku sprawdź:

- [ ] Pobrano tekst jednolity KPC z ELI i potwierdzono brzmienie każdego powołanego artykułu (`text_version = tekst_jednolity`, `in_force = IN_FORCE`)
- [ ] Wszystkie pola wymagane zostały uzupełnione danymi od użytkownika
- [ ] Struktura pisma jest zgodna z wzorcem (9 elementów w prawidłowej kolejności)
- [ ] Treść merytoryczna stanowi zwięzłe, ciągłe oświadczenie procesowe (jedno nieprzerwane zdanie)
- [ ] Schemat argumentacji zachowany: legitymacja → przyczyna → oświadczenie o cofnięciu → koszty
- [ ] Użyto odpowiedniego wariantu frazy (A–E) dopasowanego do okoliczności
- [ ] Wielkie litery dla ról procesowych: „Strona Powodowa", „Strona Pozwana", „Pozew"
- [ ] Numery artykułów KPC potwierdzone tekstem z `ustawy_artykul`, nie wpisane z pamięci
- [ ] W piśmie podano adres publikacyjny KPC z ELI/`display_address` zwróconym przez ELI
- [ ] Oświadczenie o doręczeniu jest spójne z okolicznościami (pełnomocnik vs. strona, załączniki vs. brak, poczta vs. elektronicznie)
- [ ] Formatowanie .docx jest zgodne z wytycznymi
- [ ] Polskie znaki diakrytyczne wyświetlają się poprawnie
