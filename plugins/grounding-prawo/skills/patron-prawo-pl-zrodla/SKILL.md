---
name: patron-prawo-pl-zrodla
description: 'Źródła prawa i kolejność ich użycia: Repertorium, brzmienie przepisów (ustawy, Repertorium), komentarz do artykułu, SAOS i NSA, EUR-Lex; przez przeglądarkę sn.pl, orzeczenia.ms.gov.pl, TK i akty UE po CELEX; decyzje UODO. Używaj, gdy potrzebny przepis, orzeczenie lub weryfikowalne źródło.'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `ustawy`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# Źródła prawa PL i UE

Konektory działają przez portal MCP (`lex.xlap.pl/mcp`, plik `.mcp.json` pluginu). Narzędzia mają w hoście
nazwy z prefiksem portalu (np. `ustawy_artykul`, `nsa_search`); poniżej podano samą nazwę narzędzia.
Składnia zapytań, drabinka do tekstu jednolitego, pokrycie czasowe i standardy cytowania: `references/iura-metodyka.md`
oraz `shared/MOD-TEKST-JEDNOLITY.md`. Pełna ścieżka pracy nad sprawą: skill `prawny-router-v3` (mapa celów `shared/SCIEZKI-PRACY.md`).

## Kolejność obowiązkowa

Najpierw wyszukiwanie semantyczne ustaw i orzeczeń przez `repertorium_szukaj_repertorium`
(`q`: zagadnienie, `jurysdykcja`: `pl` albo `eu`), potem pełne brzmienie pozostałymi MCP.
Stosuj `shared/ZASADY-PLUGINU.md`, sekcja „Gdzie szukać”; poniższe ścieżki wykonuj po tym kroku.
Brak trafień lub awarię odnotuj i kontynuuj właściwym konektorem.

## Który konektor do czego

| Pytanie | Serwer | Narzędzia | Czego tu NIE ma |
|---|---|---|---|
| **Zawsze pierwsze:** semantyczne rozpoznanie ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK, decyzji UODO, PL i UE | `repertorium` | `szukaj_repertorium` (`jurysdykcja` `pl`/`eu`, kilka zapytań: zagadnienie, każda teza) | potwierdzenia kompletnego, aktualnego brzmienia cytatu |
| Orzeczenia SN, sądów powszechnych, TK, KIO | `saos` | `search`, `search_by_case`, `get_judgment`, `saos_cite_check` | WSA i NSA - brak orzecznictwa administracyjnego (podatki, UODO, decyzje organów) |
| Orzeczenia NSA i 16 WSA (CBOSA): administracja, podatki, cła, ochrona danych | `nsa` | `search`, `search_by_case`, `get_judgment` | sądy powszechne, SN |
| Akty prawne PL (Dz.U., M.P., od 1918 r.), status, nowelizacje | `ustawy` | `ustawy_akty`, `repertorium_szukaj_repertorium`, `ustawy_artykul` (przy `text_unavailable_use_pdf` adresy PDF: pobierz `curl`, odczytaj `pdftotext`) | treści PDF w odpowiedzi MCP, orzecznictwo, komentarze |
| Spółki w KRS | `krs` | `get_entity`, `get_entity_full`, `get_board` | CEIDG |
| Prawo UE, TSUE, decyzje organów ochrony danych (GDPRhub) | `eu-sparql` | `search_by_celex`, `search_by_date_range`, `search_cjeu`, `search_cjeu_by_ecli`, `search_gdprhub` | prawo krajowe |
| 14 regulacji UE offline (RODO, AI Act, DORA, NIS2, eIDAS 2.0, CRA, DSA, DMA, Data Act, DGA, LED, ePrivacy, Cybersecurity Act i in.) | `eu-compliance` | `eu_search`, `eu_article`, `eu_compare`, `eu_check_applicability`, `eu_evidence` | akty spoza korpusu |
| Brzmienie artykułu i komentarz: kodeksy i Konstytucja z git-as-law (tekst jednolity + każda nowelizacja, stan na dzień `stan_na`), pozostałe ustawy z komentarza według tekstu jednolitego | serwer `ustawy` (gdy jest w portalu) albo lokalnie `scripts/ustawy.py` | `artykul`, `cytat`, `szukaj` (`art <akt> <nr> --komentarz`) | nowelizacji wchodzących w życie po `stan_na` (sprawdź w `ustawy`); komentarz to opracowanie |

## Struktura sądownictwa - nie myl pionów
- Sądy powszechne: rejonowe, okręgowe, apelacyjne. Sprawy cywilne, karne, rodzinne, prawa
  pracy i ubezpieczeń społecznych, gospodarcze.
- Sąd Najwyższy (SN): nadzoruje orzecznictwo sądów powszechnych i wojskowych; Izby Cywilna,
  Karna, Pracy i Ubezpieczeń Społecznych, Kontroli Nadzwyczajnej i Spraw Publicznych.
  SN NIE jest sądem administracyjnym.
- Sądy administracyjne to ODRĘBNY pion: WSA i NSA. Kontrolują administrację publiczną,
  w tym decyzje Prezesa UODO - orzecznictwo o ochronie danych osobowych zapada w WSA/NSA.
- Trybunał Konstytucyjny (TK): zgodność prawa z Konstytucją. KIO: zamówienia publiczne.

## Typowe ścieżki
- **Znana sygnatura:** „I ACa 772/13”, „IV CSK 123/15”, „KIO 100/12” → `saos` `search_by_case`;
  „II FSK 1234/20”, „II SA/Wa 100/26” → `nsa` `search_by_case`. Brak wyniku - spróbuj drugiej
  bazy. Pion rozpoznasz skryptem `pl_entities.py extract` (skill `citation-grounding-pl`, moduł `citation-grounding-pl/modules/patron-identyfikatory-pl`).
- **Czy wyrok „żyje”:** `saos_cite_check` - późniejsze orzeczenia cytujące sygnaturę. Przeczytaj,
  w jakim kontekście ją przywołują (aprobata, krytyka, odmienny pogląd).
- **Treść przepisu:** `ustawy` `ustawy_akty` (fragment tytułu, rok, status) → `repertorium_szukaj_repertorium` (ELI,
  np. `DU/2018/1000`: status obowiązywania, wejście w życie, linki do tekstu) → `ustawy_artykul`
  stronami (`page`, aż `has_more=false`) do szukanego artykułu. Sprawdź, czy akt obowiązuje
  i czy to tekst jednolity.
- **Prawo UE:** artykuł z 14 regulacji → `eu_article` (dosłowny tekst offline) zamiast pamięci;
  ten sam obowiązek w kilku aktach → `eu_compare` (np. zgłaszanie incydentu: DORA vs NIS2 vs CRA);
  czy regulacja dotyczy sektora → `eu_check_applicability` (wskazówka, nie wiążąca ocena);
  jakie dowody zgodności → `eu_evidence`. Inne akty i wyroki → `eu-sparql` `search_by_celex`
  (np. `32016R0679` RODO, `62018CJ0311` Schrems II) albo `search_cjeu_by_ecli`.
- **Spółka:** kto reprezentuje → `krs` `get_board`; pełne dane (kapitał, PKD, status) →
  `get_entity`; historia zarządów i wpisów → `get_entity_full`.
- **Komentarz do artykułu:** `python3 scripts/ustawy.py art kk 148 --komentarz` (indeks: `ustawy.py buduj` w repo
  `grounding-prawo`, akty z `vendor/law/`). Komentarz cytuj jako opracowanie, nigdy jako treść przepisu.
- **Orzeczenia spoza konektorów** (SN po 2016 spoza dumpu SAOS, orzeczenia.ms.gov.pl, TK, akt UE po CELEX):
  moduł `webwright-legal-pl` (komendy `orzeczenie`, `szukaj`, `eurlex` w jego katalogu). W kontenerze na NAS przy
  blokadzie (CGNAT) uruchom `shared/scripts/tor_rotator.sh`. Wynik zapisz w `_robocze/` teczki z prefiksem
  `rrrrMMdd_hhmm_`, w odpowiedzi podaj URL źródła i datę pobrania.
- **Decyzje Prezesa UODO:** konektor `uodo`, weryfikacja według modułu `uodo-grounding-pl`.

## Dyscyplina
- Sygnaturę, sąd i datę podawaj DOSŁOWNIE z wyniku narzędzia. Nigdy nie wymyślaj sygnatury
  ani nie uzupełniaj jej z pamięci.
- Przy każdym przywołanym orzeczeniu podaj link z wyniku narzędzia (SAOS, CBOSA, EUR-Lex).
- Nie podawaj orzeczenia jako trafienia, jeśli nie dotyczy meritum pytania. Sprawa, w której
  szukana fraza pada ubocznie w wątku proceduralnym, nie jest odpowiedzią. Brak trafienia na
  temat - powiedz to zamiast podawać sprawę poboczną.
- Ochrona danych osobowych i decyzje UODO → orzecznictwo szukaj w `nsa`, nie w SAOS.
- Daty w SAOS bywają zniekształcone przez OCR (np. rok 3013) - zaznacz niewiarygodną datę.
- Konektory mogą mieć opóźnienie względem Dziennika Ustaw. Przed cytowaniem przepisu w piśmie
  zaznacz, że bieżące brzmienie trzeba potwierdzić w oficjalnym źródle.
- Cytat dosłowny (blockquote, cudzysłów) bierz z tego, co narzędzie faktycznie zwróciło. Wynik
  narzędzia możesz zapisać do pliku i sprawdzić cytaty skryptem modułu `citation-grounding-pl/modules/patron-weryfikacja-cytatow` skilla `citation-grounding-pl`
  (tryb `--quotes`).
- Treści GDPRhub mają licencję CC BY-NC-SA 4.0 - zaznacz to przy dłuższych cytatach.

## Format odwołań
- Akt: pełna nazwa + (Dz.U. ROK poz. NUMER) przy pierwszym przywołaniu, dalej skrót
  („art. 6 ust. 1 lit. f RODO”, „art. 415 k.c.”). ELI z wyniku `ustawy` jako referencja.
- Orzeczenie: „wyrok NSA z 12.05.2026 r., III OSK 1377/23” + link.
- Akt UE: „rozporządzenie 2016/679 (RODO)” + link EUR-Lex.
- Daty w treści: DD.MM.RRRR r.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/chat/prompts.ts`
(COURTS_PL, SAOS_DISCIPLINE_PL, DRAFTING_PL), `docs/BAZA_WIEDZY.md`. Konektory MCP: MIT.

## MODUŁY SCALONE

Ten skill obejmuje funkcje dawnych osobnych skilli. Wczytaj moduł, gdy zadanie go dotyczy; reguły tego skilla obowiązują także w module.

| Moduł | Zastosowanie | Plik |
|---|---|---|
| `uodo-grounding-pl` | decyzje Prezesa UODO: wyszukiwanie i weryfikacja w sprawach RODO | `modules/uodo-grounding-pl/MODULE.md` |
| `webwright-legal-pl` | orzeczenia i akty spoza MCP przez przeglądarkę: sn.pl, orzeczenia.ms.gov.pl, trybunal.gov.pl, EUR-Lex po CELEX | `modules/webwright-legal-pl/MODULE.md` |

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** każde pytanie o przepis, orzeczenie, KRS, prawo UE, interpretację
- **Wynik zapisz w:** odpowiedź ze źródłem; do sprawy: dopisek do `analiza/_dowody-i-przepisy.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `orzeczenia-sadowe-v2`, `analizator-przepisow-v2`
- **Basic Memory (`legal`):** najpierw `orzeczenia/`, `ustawy/`, `zagadnienia/`; zweryfikowane orzeczenie przydatne w innych sprawach zapisz w `orzeczenia/` (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
