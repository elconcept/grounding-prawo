# Pochodzenie refaktoru v0.4

Podstawą jest memo `docs/20261015_memo-astra-zawiadomienie-hardgate.md` w repo grounding-prawo,
odczytane w całości przy refaktorze 2026-10-15. Memo zawiera dziennik 38 pozycji (dwie duplikują
wcześniejsze źródła), syntezę i scenariusze oceny. Niniejszy plik zapewnia pochodzenie reguł
również w samodzielnie dystrybuowanym folderze skilla; pełny dziennik pozostaje w repo.

| Decyzja | Podstawa z memo / źródła |
|---|---|
| Relacja bez uprzednich zewnętrznych dowodów; tropy osobno | Pozycje 1–4, 8, 14: [wzór WUW](https://www.poznan.uw.gov.pl/system/files/zalaczniki/zawiadomienie_przestepstwo_0.pdf), [Słupińska](https://slupinska.eu/blog/zawiadomienie-o-mozliwosci-popelnienia-przestepstwa/), [Murdza](https://www.adwokatmurdza.pl/zawiadomienie-o-popelnieniu-przestepstwa/), [wzór kancelaryjny](https://sprawy-karne.biz.pl/zawiadomienie-o-mozliwosci-popelnienia-przestepstwa-wzor/). |
| Mikro-sekwencja, skutki i otwarty bank kwalifikacyjny | Pozycje 3, 5–11, 15–17, 24, 27, 30, 34–36: m.in. [przywłaszczenie](https://sprawy-karne.biz.pl/jak-udowodnic-przywlaszczenie-mienia/), [groźby](https://sprawy-karne.biz.pl/grozby-karalne-art-190-kk/), [oszustwo](https://sprawy-karne.biz.pl/oszustwo-art-286-kk/), [stalking](https://sprawy-karne.biz.pl/stalking-ofiara/). |
| Bezpieczeństwo i instytucje | Pozycje 7, 12, 23, 36: m.in. [Niebieska Karta](https://sprawy-karne.biz.pl/niebieska-karta/), [pomoc](https://sprawy-karne.biz.pl/pomoc-dla-pokrzywdzonego/). |
| Nowe szczegóły i audyt różnic bez automatycznej blokady | Synteza memo, pozycje 8, 10 i wcześniejszy przypadek potocznego „partnera” w hardgate-spojnosc.md. Rozdzielenie A/B jest decyzją projektową, nie cytatem z ustawy ani diagnozą traumy. |
| Routing i aktualność prawa | Pozycje 13, 18–22, 25–26, 28–29, 32–33, 37; źródła o późniejszych środkach obrończych nie rozszerzają zakresu skilla. |
| Zwięzły rdzeń, szczegóły w references, ocena zachowania | Instrukcje skill-creator odczytane przy refaktorze; wymagania syntezy memo. |

Materiały kancelaryjne inspirują pytania, ale nie są dowodem aktualnego stanu prawa.
Nie przejęto marketingowych twierdzeń, że pokrzywdzony „musi udowodnić” relację, ani zalecenia
usuwania emocji. Weryfikacja artykułów i trybów dla konkretnej sprawy wymaga urzędowych źródeł.

## Uzupełnienie po audycie kolizji

Po pierwszym przebiegu refaktoru użytkownik wskazał
`INBOX/20261010_AUDYT_SKILLI_kolizje_zawiadomienia.md`. A2 ujawnił wejście HYBRID/BLOCK ZERO
przez router UP-4, mimo wyłączenia CLAIM-VALIDATION. A3 dotyczył znaczników danych formalnych,
A6 źródła przenoszonej kwoty, A7 pracy bez repo. Te punkty uzasadniają kontrakt integracyjny
`shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md` i wyjątki w punktach wejścia modułów.
Dawne A9 „bez zmian” nie ogranicza późniejszej instrukcji użytkownika: ochrona musi działać
również przy ataku i syntezie. Sankcje z A1 oraz techniczne błędy formatowania A4/A5 nie były
przedmiotem tego refaktoru i nie są tu oznaczane jako naprawione.
