---
name: medical-consent
description: Analizuj czynność medyczną wykonaną bez zgody lub mimo sprzeciwu pod kątem art. 192 k.k. oraz równoległych skutków pacjenckich i cywilnych. Filtr karnoprawny (Stępniak/Wala/Sułkowski-Bargiel) — rozdziela brak świadomej zgody, brak zgody, sprzeciw aktualny i sprzeciw pro futuro. Używaj przy świadczeniu, zabiegu, iniekcji, farmakoterapii lub procedurze wykonanej bez zgody. Wnioski karne formułuje ostrożniej niż cywilne.
metadata:
  argument-hint: <czynność / dokument / stan faktyczny do analizy zgody>
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Na wejściu odczytaj adekwatny kontekst z projektu `model-memory` i sprawy z `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap w `model-memory` i sprawdź odczytem. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# /tk-medical-consent-check — Filtr Zgody i Odpowiedzialności Karnej (art. 192 k.k.)

Analizuj, czy konkretna czynność medyczna wykonana bez skutecznej zgody albo mimo sprzeciwu może mieć znaczenie karnoprawne (art. 192 k.k.), oraz jakie są równoległe skutki w warstwie praw pacjenta i odpowiedzialności cywilnej.

&nbsp;

**Zastrzeżenie**: Analiza służy organizacji pracy nad sprawą, nie zastępuje analizy karnistycznej pełnomocnika. Skill NIE formułuje automatycznie zawiadomienia o przestępstwie i NIE przesądza winy.

&nbsp;

**Reguła nadrzędna — ostrożność karnoprawna**: Wnioski z art. 192 k.k. formułuj ostrożniej niż wnioski cywilne i pacjenckie. Nie utożsamiaj automatycznie: braku świadomej zgody z art. 192 k.k., braku podpisu z brakiem zgody, każdego świadczenia zdrowotnego z zabiegiem leczniczym, hospitalizacji psychiatrycznej z zabiegiem leczniczym, ani UoOZP z nieograniczoną zgodą na leczenie bez zgody.

## Wywołanie

```
/tk-medical-consent-check $ARGUMENTS
```

&nbsp;

Przykłady:

&nbsp;

- "Podano lek psychotropowy bez zgody pacjenta na oddziale — czy to art. 192 k.k.?"  
- "Pacjent podpisał formularz blankietowy — oceń skuteczność zgody"  
- "Wykonano cewnikowanie mimo ustnego sprzeciwu odnotowanego przez personel"  
- "Czy obserwacja psychiatryczna jest zabiegiem leczniczym?"

&nbsp;

Jeśli brak czynności do analizy — poproś o opis konkretnej czynności medycznej.

&nbsp;

---

## Krok 1: Ustal konkretną czynność (zawsze najpierw)

Nie analizuj „leczenia" ani „hospitalizacji" jako całości. Wyodrębnij **jedną, konkretną czynność**:

&nbsp;

- co dokładnie wykonano,  
- kiedy,  
- kto wykonał i jaki miał status zawodowy,  
- czy ingerowano w ciało pacjenta.

&nbsp;

---

## Krok 2: Filtr „zabieg leczniczy" (filtr Stępniaka) — brama art. 192 k.k.

Pojęcie *zabiegu leczniczego* z art. 192 § 1 k.k. **nie ma definicji legalnej**. Nie utożsamiaj go automatycznie ze *świadczeniem zdrowotnym* (pojęcie szersze) ani nie zawężaj wyłącznie do operacji.

&nbsp;

Roboczy filtr zawężający (za B. Świątek, przywołaną przez Stępniaka):

&nbsp;

1. **Interwencja w ciało** — czy czynność ingeruje w ciało / integralność cielesną?  
2. **Cel leczniczy** — czy celem jest niweczenie skutków choroby lub stanu pourazowego?

&nbsp;

Jeśli **brak ingerencji w ciało → art. 192 k.k. wymaga szczególnej ostrożności.**

&nbsp;

| Silni kandydaci (zabieg leczniczy) | Słabi / wykluczeni kandydaci |
| :---- | :---- |
| zabieg operacyjny/chirurgiczny; inwazyjna procedura diagnostyczna lub terapeutyczna; wkłucie, kaniulacja, cewnikowanie, pobranie materiału; iniekcja / podanie substancji jako wyodrębniona czynność; rozszerzenie zakresu zabiegu poza zgodę | sama obserwacja; sam wywiad; sama konsultacja; badanie dokumentacji; monitorowanie bez ingerencji; wydanie opinii/orzeczenia; ogólny proces diagnostyczny lub leczniczy jako całość; czynności administracyjne |

&nbsp;

**Reguła celu**: nie zakładaj celu leczniczego tylko dlatego, że czynność wykonał personel medyczny albo odbyła się w szpitalu — ustal cel z dokumentacji (możliwy też cel: diagnostyczny, profilaktyczny, rehabilitacyjny, opiekuńczy, zabezpieczający/przymusowy).

&nbsp;

---

## Krok 3: Taksonomia zgody — oddziel cztery konfiguracje

| Konfiguracja | Waga dla art. 192 k.k. | Reguła |
| :---- | :---- | :---- |
| **Brak zgody** (brak jakiejkolwiek zgody osoby uprawnionej) | Wysoka, jeśli zabieg leczniczy i brak wyjątku ustawowego | Analizuj pełny filtr |
| **Zgoda wadliwa / nieobjaśniona** (formalny podpis, ale bez świadomości, informacji, konkretności) | Ostrożnie — **najpierw UPP i KC** | art. 192 k.k. dopiero po ustaleniu, że wadliwość \= brak zgody na tę czynność |
| **Sprzeciw aktualny** (świadoma, dobrowolna odmowa) | **Bardzo wysoka** — silniejsza konfiguracja niż zgoda nieobjaśniona | Nie oceniaj racjonalności decyzji pacjenta |
| **Sprzeciw pro futuro** (uprzednie oświadczenie na wypadek utraty przytomności) | Wysoka, jeśli skuteczny | Sprawdź aktywację warunków |

&nbsp;

**Sprzeciw pro futuro — warunki skuteczności**: pacjent nie ma aktualnej możliwości decyzji; zaszły okoliczności z oświadczenia; oświadczenie jednoznaczne, wiarygodne, złożone swobodnie i świadomie. Forma aktu notarialnego mocniejsza dowodowo niż zwykła pisemna. Pacjent **nie ma obowiązku uzasadniać** sprzeciwu; motyw religijny/światopoglądowy nie jest warunkiem skuteczności. (SN, postanowienie z 27.10.2005 — oświadczenie pro futuro wiąże, jeśli wyraźne i jednoznaczne.)

&nbsp;

**Ważna zgoda wymaga** (SN III KK 14/15): własnej decyzji pacjenta, świadomości, zdolności psychofizycznej, rozważenia przesłanek, swobody, dobrowolności, braku błędu i przymusu. Formalny podpis nie wystarcza. Formularz jest dowodem, ale nie zastępuje rozmowy; ciężar wykazania obowiązku informacyjnego spoczywa na podmiocie powołującym się na zgodę.

&nbsp;

---

## Krok 4: Filtr obligatoryjny art. 192 k.k. (11 kroków)

1. Konkretna czynność medyczna  
2. Czy była świadczeniem zdrowotnym  
3. Czy była **zabiegiem leczniczym** w sensie art. 192 k.k. (Krok 2\)  
4. Kto wykonał i jaki status zawodowy  
5. Czy była zgoda  
6. Czy zgoda była świadoma, dobrowolna, konkretna i obejmowała tę czynność  
7. Czy był sprzeciw aktualny albo pro futuro  
8. Czy zachodził ustawowy wyjątek od zgody  
9. Czy wyjątek został udokumentowany  
10. Czy wykonawca wiedział o braku zgody albo godził się z jej możliwym brakiem (umyślność — możliwy zamiar bezpośredni lub ewentualny)  
11. Czy wymagany jest i czy złożono **wniosek o ściganie** (tryb wnioskowy; po złożeniu — z urzędu)

&nbsp;

**Podmiot (spór doktrynalny)**: art. 192 § 1 k.k. używa zaimka „kto". Nie wykluczaj automatycznie sprawcy niebędącego lekarzem, ale przy wykonawcy spoza zawodu medycznego **oznacz podwyższoną niepewność kwalifikacji**. Zawsze ustal, kto faktycznie wykonał czynność i czy miał uprawnienia.

&nbsp;

---

## Krok 5: Wyjątki działania bez zgody

Działanie bez zgody wymaga **konkretnej podstawy ustawowej**; nagłość nie może być domniemana; okoliczności muszą być opisane w dokumentacji.

&nbsp;

**Czerwone flagi (wyjątek nienależycie zastosowany):**

&nbsp;

- brak adnotacji o przyczynie działania bez zgody  
- brak uzasadnienia nagłości  
- brak próby kontaktu z przedstawicielem ustawowym lub sądem, gdy była możliwa  
- brak konsultacji z drugim lekarzem bez wyjaśnienia  
- **działanie mimo wcześniejszego wyraźnego sprzeciwu przytomnego pacjenta**  
- rozszerzenie zakresu zabiegu bez nagłej konieczności i bez adnotacji o przyczynie

&nbsp;

Stan wyższej konieczności **nie jest** ogólną podstawą obejścia świadomego sprzeciwu pacjenta. Dobre intencje i interes zdrowotny nie zastępują zgody.

&nbsp;

---

## Krok 6: UoOZP jako lex specialis (psychiatria przymusowa)

W psychiatrii przymusowej **najpierw** badaj podstawę szczególną UoOZP (art. 21, 23, 24, 29, 33, 34), dopiero potem art. 192 k.k.

&nbsp;

- Jeśli UoOZP daje podstawę szczególną i została prawidłowo zastosowana → sama niezgoda pacjenta nie przesądza art. 192 k.k.  
- Jeśli przesłanki UoOZP nie zostały spełnione ani udokumentowane → brak zgody odzyskuje znaczenie pacjenckie, cywilne i potencjalnie karne.

&nbsp;

Nie kwalifikuj całej hospitalizacji/obserwacji/badania psychiatrycznego jako zabiegu leczniczego bez wskazania konkretnej czynności. Przymusowe podanie leków, cewnikowanie, wkłucie, iniekcja lub inwazyjna procedura somatyczna wymagają osobnej analizy — najpierw reżim UoOZP.

&nbsp;

**Czerwone flagi UoOZP:** leczenie bez zgody powołane ogólnie, bez wskazania art. 33/34; przymusowe leki bez dokumentacji przymusu; brak związku leczenia z usunięciem przyczyn przyjęcia; użycie UoOZP jako ogólnej zgody na dowolne leczenie.

&nbsp;

---

## Krok 7: Skutki równoległe (pacjenckie i cywilne)

Niepowodzenie kwalifikacji karnej **nie wyłącza** roszczeń cywilnych ani skargi pacjenckiej:

&nbsp;

- prawa pacjenta (informacja, zgoda) są szersze niż zakres art. 192 k.k.,  
- wadliwa zgoda może wspierać art. 4 ustawy pacjenckiej, art. 23–24–448 k.c. lub art. 444–445 k.c.,  
- ustalenia o braku zgody wzmacniają bezprawność i krzywdę,  
- ważna zgoda oznacza przyjęcie **tylko** typowego, przewidywalnego ryzyka, o którym pacjent był poinformowany — nie obejmuje błędu medycznego.

&nbsp;

---

## Czerwone flagi

**Wysoka waga:**

&nbsp;

- wykonanie zabiegu mimo wyraźnego sprzeciwu świadomego pacjenta  
- wykonanie zabiegu mimo skutecznego sprzeciwu pro futuro  
- zabieg bez zgody i bez udokumentowanego wyjątku ustawowego  
- przymusowe leczenie/podanie leków bez podstawy szczególnej lub bez kwalifikacji jako przymus bezpośredni  
- zabieg operacyjny / metoda podwyższonego ryzyka bez pisemnej zgody i bez innego jednoznacznego dowodu zgody  
- rozszerzenie zakresu zabiegu bez warunków ustawowych  
- zgoda podpisana w stanie wyłączającym świadome rozeznanie  
- brak wniosku o ściganie przy zamiarze uruchomienia ścieżki karnej

&nbsp;

**Średnia waga:** brak informacji o istotnym ryzyku; niejasny zakres zgody; formularz bez identyfikacji procedury; **zgoda blankietowa**; zgoda dorozumiana wywiedziona z biernego zachowania; niejasny status osoby wyrażającej zgodę.

&nbsp;

**Kontekstowe:** nieprzytomność; zatrucie/sedacja; kryzys psychiatryczny; małoletniość; ubezwłasnowolnienie; brak przedstawiciela ustawowego; sprzeczne wpisy; podanie leków wpływających na świadomość przed uzyskaniem zgody.

&nbsp;

---

## Model dowodowy — dokumenty do pozyskania

Formularz zgody; formularz odmowy/sprzeciwu; oświadczenie pro futuro; wpis o rozmowie informacyjnej; wpis o stanie świadomości i rozeznaniu; opis procedury planowanej vs faktycznie wykonanej; zlecenia lekarskie; protokół zabiegu; dokumentacja przyczyny działania bez zgody i nagłości; adnotacja o konsultacji z drugim lekarzem; dokumentacja przymusu bezpośredniego; wpisy pielęgniarskie; wpisy o lekach wpływających na świadomość; opinia biegłego o charakterze czynności i zgodzie.

&nbsp;

---

## Format wyjściowy (output contract)

Gdy materiał dotyczy art. 192 k.k. i problemu zgody, odpowiedź MUSI zawierać:

&nbsp;

```
## Analiza zgody — [Czynność] — [Data]

### 1. Konkretna czynność i jej kwalifikacja
- Czynność / świadczenie zdrowotne / zabieg leczniczy w sensie art. 192 k.k.?
- Argumenty ZA i PRZECIW kwalifikacji jako zabieg leczniczy
- Jednostkowa / wyodrębniona / inwazyjna? Cel czynności?

### 2. Wykonawca
- Kto wykonał, status zawodowy, uprawnienia

### 3. Zgoda
- Czy była; świadoma/dobrowolna/konkretna; forma (pisemna/ustna/dorozumiana/blankietowa)
- Sprzeciw aktualny? Sprzeciw pro futuro? Zdolność psychofizyczna do decyzji?

### 4. Wyjątki i podstawy szczególne
- Wyjątek ustawowy? Udokumentowany? Zgoda sądu opiekuńczego wymagana?
- UoOZP jako lex specialis — czy zastosowana i udokumentowana?

### 5. Strona podmiotowa i tryb
- Czy wykonawca wiedział o braku zgody / godził się z jej brakiem?
- Czy złożono / należy złożyć wniosek o ściganie?

### 6. Skutki równoległe
- Prawa pacjenta i roszczenia cywilne niezależnie od kwalifikacji karnej

### 7. Czerwone flagi
[z podziałem waga wysoka / średnia / kontekstowe — każda z dokumentem lub brakiem dokumentu]

### 8. Wniosek ostrożny
[brak podstaw / słaby kandydat / wymaga wyjaśnienia / silny kandydat / wysokie ryzyko art. 192 k.k.]
```

&nbsp;

**Język preferowany**: „materiał wskazuje na możliwy problem skutecznej zgody"; „należy odróżnić zgodę wadliwą informacyjnie od braku zgody"; „wykonanie zabiegu mimo świadomego sprzeciwu jest silniejszą konfiguracją art. 192 k.k."; „brak formy pisemnej nie oznacza automatycznie braku zgody".

&nbsp;

**Język zakazany**: „każda zgoda nieobjaśniona to art. 192 k.k."; „brak podpisu zawsze oznacza brak zgody"; „każde świadczenie bez zgody to art. 192 k.k."; „tylko operacja może być zabiegiem leczniczym"; „skoro była hospitalizacja, był zabieg leczniczy"; „obserwacja psychiatryczna to zabieg leczniczy"; „ratowanie życia zawsze usprawiedliwia działanie wbrew sprzeciwowi"; „nieprzytomność oznacza zgodę domniemaną"; „UoOZP pozwala na dowolne leczenie bez zgody"; „brak art. 192 k.k. oznacza brak naruszenia".

&nbsp;

---

## Wskazówki

- Zawsze najpierw uruchom filtr Stępniaka (zabieg leczniczy vs świadczenie zdrowotne), potem oddziel brak świadomej zgody od braku zgody i sprzeciwu.  
- Sprzeciw aktualny i skuteczny sprzeciw pro futuro to najsilniejsze konfiguracje — nie osłabiaj ich hipotezami bez podstawy w materiale.  
- Jeśli filtr art. 192 k.k. nie przechodzi, przenieś analizę do praw pacjenta, KC lub UoOZP — nie porzucaj sprawy.  
- Jeśli użytkownik chce ścieżkę karną, upewnij się, że pismo zawiera jednoznaczny wniosek o ściganie osoby uprawnionej.

&nbsp;

**Źródła map**: `legal/skill_polish_law_articles_map/criminal_liability_medical_consent_map.md`, `informed_consent_notes.md`, `patient_rights_article_map.md` (art. 9, 15–19 UPP), `mental_health_article_map.md` (art. 21, 23, 24, 29, 33, 34 UoOZP — lex specialis).

&nbsp;

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** dokumentacja medyczna po OCR, chronologia
- **Wynik zapisz w:** ocena art. 192 k.k. w `analiza/_podsumowanie.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `uoozp-compliance`, `zawiadomienie-o-przestepstwie`, `pisma-procesowe-v3`
- **Basic Memory (`legal`):** czytaj teczkę sprawy (`build_context`) i notatki wiki po sygnaturze i nazwiskach; zapisz stan sprawy i terminy w teczce, nowe fakty z akt zgłoś do ingestu (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
