# MOD-TEKST-JEDNOLITY — dojście do obowiązującego brzmienia przepisu

> Moduł wspólny (GROUNDING-PRAWO, 2026-09-13, plan integracji P4). Wyjęty ze skilla `iura`
> §4, żeby tę samą procedurę stosowały rodzina `iura`, moduły DR, `shared/ISAP-METRYKI-AKTOW.md`
> i `shared/AKTY-PRAWNE-MASTER.md`. Czytaj przed każdym dosłownym cytatem przepisu.

## Kolejność źródeł brzmienia

0. **Repertorium** (`repertorium_szukaj_repertorium`, portal `lex`): opisz zagadnienie; trafienia wskażą akt, artykuł
   i najnowsze obwieszczenie tekstu jednolitego (`document_id: eli:DU/rrrr/poz`). To krok wyszukania, nie cytat.
1. **Baza `ustawy`** (gdy portal ją udostępnia; narzędzia `artykul`, `cytat`, `szukaj`). Kodeksy i Konstytucja
   (`zrodlo: git-as-law`): tekst jednolity i każda późniejsza nowelizacja jako osobny commit, gałąź główna = stan
   prawny na dzień `stan_na`. To brzmienie obowiązujące, nie „tekst jednolity do sprawdzenia”: cytuj je ze stanem
   na `stan_na` i sprawdź w ISAP tylko akty zmieniające wchodzące w życie po tej dacie (`isap_search_acts`, tytuł
   „o zmianie ustawy - <Kodeks>”, rok, oraz nowe obwieszczenie). Ustawy z `zrodlo: komentarz` mają brzmienie
   tekstu jednolitego z pola `tekst_jednolity`; nowelizacje po nim sprawdź tak samo.
2. **ISAP** (`isap_*`, procedura poniżej): akt spoza bazy `ustawy`, nowelizacja po `stan_na`, spór o brzmienie.

Konektor `cite` (`cite_verify_article`, `cite_list_acts`) nie działa i nie obejmował części kodeksów: nie wołaj go.

## Problem
Sejm ELI serwuje pod HTML **tekst ogłoszony**, czyli brzmienie z dnia ogłoszenia, a nie stan
na dziś. Akt bazowy zwraca brzmienie **pierwotne**: Kodeks cywilny (`DU/1964/93`) odda art. 118
w wersji z 1964 r. („jednostki gospodarki uspołecznionej”, termin dziesięcioletni), podczas gdy
obowiązuje „sześć lat”. To błąd, który przechodzi do pisma, jeśli nie wiesz, którą wersję czytasz.

## Która to wersja tekstu
Nie ma parametru „stan na dzień”. Procedura dwukrokowa:

1. `search_acts` → `get_act` na akcie bazowym.
2. Weź **najnowszy** ELI z pola `consolidated_text_eli` (lista od najnowszego - pierwszy element).
3. `get_act_text` na **tym** ELI.
4. Sprawdź `structuredContent.text_version`:

| `text_version` | Znaczenie | Cytować jako obowiązujące? |
|---|---|---|
| `tekst_jednolity` + `in_force: IN_FORCE` | brzmienie na dziś | **TAK** - tylko ta kombinacja |
| `tekst_jednolity_nieaktualny` | wyszło nowsze obwieszczenie (`superseded_by_eli`) | nie - pobierz nowsze |
| `tekst_ogloszony_istnieje_nowszy_jednolity` | wersja pierwotna, istnieje jednolity | nie - pobierz jednolity |
| `tekst_ogloszony` | brzmienie z dnia ogłoszenia | tylko jako materiał historyczny, z adnotacją |

Ostrzeżenia, które konektor wypisuje w treści, przepisz użytkownikowi.

Szybsza ścieżka: `search_acts(title: "<Kodeks>", publisher: "DU", type: "Obwieszczenie")` -
wyniki od najnowszego; szukasz „…w sprawie ogłoszenia jednolitego tekstu ustawy — <Kodeks>”
ze statusem `IN_FORCE`.

## Pułapka: obowiązujący tekst jednolity kodeksu bywa tylko w PDF
Sprawdzone 11.09.2026: dla KC, KPC, KPK i KP obowiązujący tekst jednolity nie ma HTML -
`get_act_text` zwraca `text_unavailable_use_pdf`. Świeże obwieszczenie ≈ tylko PDF; konkretnych
ELI nie cytuj z pamięci, wylistuj je na bieżąco.

## Drabinka przy `text_unavailable_use_pdf` (kolejność wiążąca)

**Szczebel 1 - PDF obowiązującego tekstu jednolitego (jedyny dowód brzmienia na dziś).**
PDF-y ISAP mają warstwę tekstu, OCR jest zbędny. Wywołaj MCP `isap_get_act_text` na ELI aktualnego tekstu
jednolitego (z `search_text: "Art. 118."`). MCP `isap` nie zwraca treści PDF: przy `text_unavailable_use_pdf`
podaje adresy plików. Pobierz „PDF (tekst jednolity)” (zapasowo „PDF (domyślny)”) i odczytaj tekst lokalnie:

```bash
mkdir -p <sprawa>/_robocze/isap
curl -sSL -o <sprawa>/_robocze/isap/DU_2025_383.pdf "https://api.sejm.gov.pl/eli/acts/DU/2025/383/text/T/D20250383L.pdf"
pdftotext -layout <sprawa>/_robocze/isap/DU_2025_383.pdf <sprawa>/_robocze/isap/DU_2025_383.txt
```

Artykuł znajdź w pliku `.txt` (numer linii), a brzmienie przeczytaj w całości narzędziem odczytu pliku od nagłówka
artykułu do następnego; cytat bierz z tego odczytu, nie z wyniku wyszukiwania. Bez powłoki: MCP `ocr`
(`ocr_parse_document` z treścią PDF). To wciąż szczebel 1: liczy się źródło, nie narzędzie.

Cytowalne wyłącznie przy `status: FOUND` **i** `text_version: tekst_jednolity` **i**
`status_obowiazywania: obowiazuje`. `status: AMBIGUOUS` z `tekst_ogloszony_istnieje_nowszy_jednolity`
oznacza ELI aktu bazowego - powtórz z ELI z pola `uzyj_zamiast`. W śladzie weryfikacji podaj ELI i datę odczytu.

Cytat dosłowny sprawdź wzrokowo w PDF: ekstrakcja gubi pojedyncze spacje, a artykuły z indeksem
górnym wychodzą jako `Art. 205[1]` - w `search_text` podawaj `Art. 205.`.

**Szczebel 2 - starszy tekst jednolity z HTML (plan B, materiał pomocniczy).**
Zejdź listą obwieszczeń do pierwszego tekstu jednolitego z HTML (`text_version =
tekst_jednolity_nieaktualny`). Podając z niego przepis, napisz datę tego tekstu jednolitego
i że późniejsze nowelizacje nie są uwzględnione; sprawdź ustawy „o zmianie ustawy — <Kodeks>”
z lat po dacie t.j.

**Szczebel 3 - przyznaj brak.** Nie zgaduj i nigdy nie podstawiaj aktu bazowego jako brzmienia
obowiązującego.

> W piśmie procesowym, w którym brzmienie przepisu jest sporne, przechodzisz na szczebel 1 albo
> przyznajesz brak - szczebel 2 nie wystarczy.

## Konkretny artykuł i status aktu
`get_act_text` z `search_text: "Art. 118."` (numer z kropką, z polskimi znakami) zwraca fragment
wokół pierwszego trafienia; bez `search_text` iteruj `page`, aż `pagination.has_more = false`.
Status aktu (obowiązujący / uchylony) jest obowiązkowym elementem odpowiedzi.
