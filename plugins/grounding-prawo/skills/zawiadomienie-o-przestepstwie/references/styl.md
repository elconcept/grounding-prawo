# Styl zawiadomienia (F6-F7)

Cel: pismo, które prokurator przeczyta do końca i po którym będzie wiedział, co się stało, komu,
kto to zrobił, co autor widział, a co z tego wnosi. Prosto, ale nie prostacko. Wartko, bez lania wody.

## Zasady

1. **Pierwsza osoba, strona czynna, sprawca jako podmiot.** „M.G. uderzył mnie pięścią w twarz.”,
   nie „Doszło do uderzenia pokrzywdzonego.”
2. **Chronologia.** Przy kilku epizodach: podtytuł z datą i miejscem, potem narracja.
3. **Konkret zmysłowy.** Co widziałem, słyszałem, czułem. Dosłowne słowa sprawcy w cudzysłowie „…”.
4. **Fakt, wniosek, hipoteza rozróżnione językiem, nie tagami:**
   - fakt: „widziałem”, „słyszałem”, „poczułem”, „powiedział: «…»”, „wiem od X, że …”;
   - wniosek: „dlatego uważam, że …”, „z tego, co widziałem, wynika dla mnie, że …”;
   - hipoteza: „podejrzewam, że …”, „przypuszczam”, „wydaje mi się” - **raz, przy tezie**.
   Rozróżnienie służy czytelności, nie asekuracji (K4). Fakt podawaj stanowczo.
5. **Pewność tam, gdzie autor jest pewny.** Bez „rzekomo”, „prawdopodobnie miało miejsce”,
   „w mojej subiektywnej ocenie mogło dojść do”.
6. **Emocje i skutki to treść.** „Od tamtej nocy nie śpię przy zgaszonym świetle.” mówi organowi
   więcej niż „doznałem cierpień psychicznych”.
7. **Rytm.** Krótkie zdania po długich. Czasowniki zamiast rzeczowników odczasownikowych.
8. **Każde zdanie coś wnosi:** zdarzenie, skutek, osobę, ślad albo rozbieżność. Reszta wylatuje.
9. **Rozbieżności nazywaj wprost** (dokumenty instytucji, wcześniejsze zeznania), bez przepraszania.
10. **Informacja od innej osoby zawsze ze źródłem**: kto, kiedy, jak („X powiedziała mi przez
    telefon następnego dnia, że …”, „Jak zeznał X przed [organ] w dniu […], …”). Bez źródła taka
    informacja wygląda jak własna obserwacja autora - a nią nie jest.
11. **Przepisy tylko w liście na końcu** (K3): numer + prosty opis. W narracji ani jednego „art.”.

## Anty-wzorce (zły → dobry)

| Zły | Dlaczego | Dobry |
|---|---|---|
| „Sprawca dopuścił się naruszenia mojej nietykalności cielesnej.” | żargon, akt oskarżenia | „Popchnął mnie na ścianę.” |
| „Zachowanie to wyczerpuje znamiona art. … k.k.” | kwalifikacja w narracji (K3) | w narracji: „Pobił mnie.”; przepis w liście na końcu: „art. 158 § 1 k.k. - pobicie przez dwie osoby” |
| „Zawiadamiam o możliwości popełnienia przestępstwa”, „o podejrzeniu”, „mogło dojść do” | asekuracja w otwarciu | „Zawiadamiam o popełnieniu na moją szkodę przestępstwa …” |
| „Ponoć mnie obrażał.”, „Słyszałem, że …” (bez źródła) | informacja od innych bez źródła | „N.N. powiedziała mi 28 sierpnia, że słyszała, jak mnie obrażał.” |
| „Pani wcześniej zeznała, że to obca osoba, więc …” | strofowanie autora, pozorna sprzeczność (HARDGATE) | (nie pisz; zob. `hardgate-spojnosc.md`, test pozornej sprzeczności) |
| „Wnoszę o przeprowadzenie dowodu z przesłuchania świadka X oraz zabezpieczenie monitoringu.” | lista czynności (K3) | „Wszystko widziała sąsiadka, X. Nad wejściem do sklepu jest kamera.” |
| „Z ostrożności procesowej wskazuję …”, „niniejszym”, „przedmiotowy”, „ww.” | formuły procesowe | (usuń) |
| „Rzekomo miał przy sobie nóż.” | asekuracja faktu | „Widziałem w jego ręce nóż.” albo „Wydawało mi się, że trzyma nóż - widziałem błysk ostrza.” |
| „Pokrzywdzony odczuwał silny lęk.” | trzecia osoba o sobie | „Bałem się, że mnie zabije.” |
| „Nie dysponuję dowodami, jednakże …” | samoosłabianie (K2) | (usuń; opisz zdarzenie) |
| „Doszło do zniszczenia mienia.” | strona bierna ukrywa sprawcę | „Kopnął w drzwi mojego auta i wgniótł je.” |
| „W dniu dzisiejszym”, „w chwili obecnej”, „w związku z powyższym” | wypełniacze | „dziś”, „teraz”, (usuń) |

## Pass anty-AI

Po redakcji przejdź `humanizer-pl` (wzorce 1-34 i 43: pisownia 2026) i zadaj pytanie „co tu wciąż
zdradza AI?”. Wyjątki dla zawiadomienia:
- `humanizer-pl` #33 (zakres emocji) stosuj mocno: strach, złość, upokorzenie są dozwolone.
- `patron-pisz-po-ludzku`, sekcja „Teksty prawnicze”, **nie obowiązuje**: formuły procesowe usuwasz (zostają tylko otwarcie, wniosek o ściganie i lista przepisów).
- Typografia: łącznik „-” (nie pauza), polskie cudzysłowy „…”.

## TODO v0.3
- Przykład pełnego akapitu przed i po (z draftu z repo, za zgodą autora).
- Lista żargonu do mechanicznej kontroli (do `scripts/`).
