---
name: case-risk
description: Wielodomenowa ocena ryzyk w sprawie — dowodowe, proceduralne, dokumentacyjno-medyczne, interwencji Policji/ZRM, karnoprocesowe, cywilne, ryzyko nadmiernego twierdzenia (overclaiming) i ryzyko strategicznego czasu. Integruje mapy UoOZP, KC, art. 192 k.k. i skargi nadzorczej. Używaj do oceny konkretnego zarzutu albo całościowego przeglądu materiału pod kątem ryzyka procesowego.
argument-hint: '<kwestia / zarzut / dokument do oceny ryzyka>'
---
# case-risk Wielodomenowa Ocena Ryzyk Procesowych

Oceń i sklasyfikuj ryzyka w sprawie obejmującej wątki psychiatryczne (UoOZP), cywilne (KC), karne (art. 192 k.k.) i nadzorcze (skarga do prezesa sądu). Skill scala kategorie ryzyk z wielu domen w jedną matrycę.

**Zastrzeżenie**: Ocena ryzyk nie zastępuje porady prawnej — jest narzędziem organizacji pracy.
**Zakres — uwaga metodyczna**: Skill obejmuje ryzyko interwencji Policji/ZRM (zakotwiczone w mapie cywilnej i UoOZP). Skill **nie** obejmuje odrębnej kategorii „ryzyko posiadania/naruszenia posiadania" — mapy źródłowe nie zawierają dla niej podstawy. Nie twórz tej kategorii bez dedykowanego materiału.

## Wywołanie

- "Oceń ryzyko procesowe braku zarzutów do opinii biegłego"  
- "Jakie ryzyko overclaimingu przy powołaniu art. 192 k.k. do obserwacji psychiatrycznej?"  
- "Przegląd ryzyk przed pozwem cywilnym o zadośćuczynienie"

---

## Matryca ryzyka

### Wymiar 1 — Waga (skutek, jeśli ryzyko się zmaterializuje)

| Poziom | Opis |
| :---- | :---- |
| 1 — Nieistotna | Drobna luka, bez wpływu na wynik |
| 2 — Niska | Osłabia argumentację, nie zmienia rozkładu sił |
| 3 — Średnia | Może wpłynąć na ocenę jednej przesłanki / jednej podstawy |
| 4 — Wysoka | Może przesądzić o niekorzystnym rozstrzygnięciu |
| 5 — Krytyczna | Zagraża pozycji w całej sprawie / utrata roszczenia lub zarzutu |

### Wymiar 2 — Prawdopodobieństwo

| Poziom | Opis |
| :---- | :---- |
| 1 — Odległe | Brak podstaw faktycznych |
| 2 — Mało prawdopodobne | Wymaga szczególnych okoliczności |
| 3 — Możliwe | Rozstrzygane różnie |
| 4 — Prawdopodobne | Materiał/orzecznictwo wskazuje ten kierunek |
| 5 — Niemal pewne | Wyraźna luka lub uchybienie |

### Wynik \= Waga × Prawdopodobieństwo

| Wynik | Poziom | Kolor |
| :---- | :---- | :---- |
| 1–4 | Niskie | ZIELONY |
| 5–9 | Średnie | ŻÓŁTY |
| 10–15 | Wysokie | POMARAŃCZOWY |
| 16–25 | Krytyczne | CZERWONY |


---

## Kategorie ryzyk (wielodomenowe)

### A. Ryzyka dowodowe

Luki w materiale: opinia biegłego bez osobistego badania; brak dokumentacji konkretnych zachowań; sprzeczności w dokumentacji szpitalnej; brak dokumentacji próby leczenia dobrowolnego; wydruk bez metadanych / brak audit trail EDM; skan zamiast dokumentu źródłowego. *Działanie:* wnioski o zobowiązanie szpitala do dokumentów; wykazanie sprzeczności; zabezpieczenie zapisu monitoringu izolacji.

### B. Ryzyka proceduralne (postępowanie sądowe i nadzorcze)

Naruszenie terminów (72h/48h); brak realnego wysłuchania uczestnika; rozprawa bez skutecznego zawiadomienia / bez dowodu doręczenia; zawiadomienie wysłane na adres domowy w czasie hospitalizacji lub nadane po terminie rozprawy; niekompletna dokumentacja w aktach sądu; **brak zastrzeżenia z art. 162 k.p.c. po oddaleniu wniosku dowodowego**; brak zarzutów do opinii biegłego mimo jej wad. *Uwaga:* materiał nadzorczy (skarga do prezesa, art. 41a–41b u.s.p.) dotyczy **realności** kontroli sądowej, nie zarzutu karnego wobec sędziego — nie mieszaj z petitum skargi.

### C. Ryzyka dokumentacyjno-medyczne

Brak karty przymusu bezpośredniego; brak kontroli co 15 minut; przedłużenie unieruchomienia bez badania; brak podstawy leczenia bez zgody (art. 33/34); dwie wersje kluczowego zawiadomienia różniące się podpisem; ta sama osoba w kilku rolach (współdecydujący lekarz / ordynator / podpisujący zawiadomienie).

### D. Ryzyka interwencji Policji / ZRM

Informacje od Policji lub ZRM **bez dokumentu źródłowego**; brak własnych obserwacji lekarza potwierdzających agresję (badanie oparte głównie na relacji osoby trzeciej); ocena, czy działanie władcze (przyjęcie, zatrzymanie, przymus) rodzi odpowiedzialność za wykonywanie władzy publicznej (art. 417 / 417² k.c.). *Uwaga:* traktuj relację osoby trzeciej jako oświadczenie, nie jako fakt udokumentowany.

### E. Ryzyka karnoprocesowe (art. 192 k.k.)

Tryb **wnioskowy** — brak wniosku o ściganie przy zamiarze uruchomienia ścieżki karnej; niepewność co do podmiotu (wykonawca spoza zawodu medycznego); niepewność kwalifikacji czynności jako zabiegu leczniczego. → szczegółowo w `/tk-medical-consent-check`.

### F. Ryzyka cywilne (podstawy roszczeń)

Mechaniczne kumulowanie podstaw bez rozdzielenia funkcji; powołanie art. 445 k.c. bez rozstroju zdrowia; powołanie art. 417 k.c. bez analizy władztwa publicznego; powołanie art. 448 k.c. bez wskazania dobra osobistego; **przedawnienie** (art. 442¹ k.c. — data zdarzenia, dowiedzenia się o szkodzie i osobie zobowiązanej; wpływ zbrodni/występku na termin). *Wskaźnik silnego roszczenia:* prawomocne postanowienie o braku zasadności przyjęcia; udokumentowane uchybienia art. 23 ust. 2–5 UoOZP; naruszenie prawa pacjenta \+ wina \+ krzywda; uszkodzenie ciała/rozstrój zdrowia po przymusie; brak dokumentacji przymusu; władcza czynność szpitala niezgodna z prawem.

### G. Ryzyko nadmiernego twierdzenia (overclaiming)

Najważniejsza kategoria kontrolna wobec preferencji użytkownika:

- utożsamianie braku świadomej zgody z art. 192 k.k.,  
- utożsamianie braku podpisu z brakiem zgody,  
- utożsamianie każdego świadczenia zdrowotnego z „zabiegiem leczniczym",  
- utożsamianie hospitalizacji psychiatrycznej z zabiegiem leczniczym,  
- traktowanie UoOZP jako nieograniczonej zgody na leczenie bez zgody,  
- utożsamianie każdego naruszenia prawa pacjenta z automatycznym zadośćuczynieniem,  
- formułowanie zarzutu karnego wobec sędziego w module skargi administracyjnej. *Skutek overclaimingu:* osłabienie wiarygodności całej argumentacji i ryzyko procesowe. Oznacz jako ryzyko WYSOKIE, gdy pismo zawiera takie utożsamienie.

### H. Ryzyko strategicznego czasu

Upływ terminu zażalenia (7 dni od doręczenia); upływ terminu zastrzeżenia art. 162 k.p.c.; przedawnienie roszczeń cywilnych; nieoptymalna kolejność wniosków (wyłączenie biegłego → nowy biegły → zarzuty do opinii); przedwczesne ujawnienie dowodów. *Reguła:* jeżeli termin jeszcze biegnie — rekomenduj natychmiastową reakcję i eskalację do pełnomocnika.

---

## Format wyjściowy

```
## Ocena ryzyka — [Kwestia] — [Data]

### 1. Opis ryzyka i domena
[A–H; jeśli wielodomenowe — wskaż główną i poboczne]

### 2. Analiza
**Waga**: [1–5] — [uzasadnienie]
**Prawdopodobieństwo**: [1–5] — [uzasadnienie]
**Wynik**: [n] — [ZIELONY / ŻÓŁTY / POMARAŃCZOWY / CZERWONY]

### 3. Czynniki zwiększające / zmniejszające ryzyko

### 4. Opcje działania
| Opcja | Skuteczność | Priorytet |
|---|---|---|

### 5. Rekomendacja i ryzyko rezydualne

### 6. Dalsze kroki (z terminami)
```

&nbsp;

**Język preferowany:** „materiał wspiera" / „materiał nie wystarcza jeszcze do" / „wysokie ryzyko procesowe" / „należy oddzielić" / „alternatywna podstawa odpowiedzialności".

&nbsp;

**Język zakazany:** „każde przyjęcie bez zgody jest bezprawne" / „każda wada dokumentacji oznacza szkodę zdrowotną" / „każde naruszenie prawa pacjenta automatycznie daje zadośćuczynienie" / „art. 445 k.c. stosuje się bez rozstroju zdrowia" / „art. 417 k.c. zawsze zastępuje odpowiedzialność szpitala".

&nbsp;

---

## Kiedy eskalować do adwokata / radcy prawnego

**Bezwzględnie:** zbliżający się termin zażalenia lub zastrzeżenia art. 162 k.p.c.; wynik CZERWONY w kategorii proceduralnej, karnoprocesowej lub cywilnej; zbliżające się przedawnienie; planowana ścieżka karna z art. 192 k.k. **Silnie rekomendowane:** wynik POMARAŃCZOWY/CZERWONY w dowolnej kategorii; opinia biegłego bez osobistego badania.

## Wskazówki

- Zawsze rozdziel bezzasadność (materialne podstawy) od bezprawności (uchybienia formalne) — to zmienia siłę wniosku.  
- Ryzyko overclaimingu oceniaj przy KAŻDYM zarzucie karnym — ono najszybciej osłabia całą sprawę.  
- Terminy sprawdzaj natychmiast i zakreślaj osobno.

&nbsp;

## Źródła map

`civil_liability_and_litigation_risk_map.md` (claim_taxonomy, mandatory_three_axis_test, conclusion_logic, przedawnienie)
`criminal_liability_medical_consent_map.md` (tryb wnioskowy, caution)
`court_administrative_supervision_map.md` (red_flag_taxonomy, realność kontroli)
`mental_health_article_map.md` (bezzasadność/bezprawność, red flags Policja/ZRM)

Na podstawie kanonicznego Anthropic`legal-risk-assessment` (art. 23)
