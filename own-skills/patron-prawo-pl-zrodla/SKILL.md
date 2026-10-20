---
name: patron-prawo-pl-zrodla
description: Research prawa polskiego i unijnego przez konektory MCP (Repertorium, SAOS, NSA/CBOSA, USTAWY, ELI/ISAP, KRS, EUR-Lex SPARQL, EU-Compliance offline). Użyj, gdy pytanie dotyczy orzecznictwa, treści przepisu, aktu prawnego, danych spółki z KRS, prawa UE lub TSUE albo gdy trzeba podać weryfikowalne źródło (sygnatura, ELI, CELEX, link).
---

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
| Semantyczne rozpoznanie ustaw i orzeczeń PL/UE | `repertorium` | `szukaj_repertorium` | potwierdzenia kompletnego, aktualnego brzmienia cytatu |
| Orzeczenia SN, sądów powszechnych, TK, KIO | `saos` | `search`, `search_by_case`, `get_judgment`, `saos_cite_check` | WSA i NSA - brak orzecznictwa administracyjnego (podatki, UODO, decyzje organów) |
| Orzeczenia NSA i 16 WSA (CBOSA): administracja, podatki, cła, ochrona danych | `nsa` | `search`, `search_by_case`, `get_judgment` | sądy powszechne, SN |
| Polskie akty z korpusu 37 ustaw: przepis, komentarz i cytat | `ustawy` | `akty`, `szukaj`, `artykul`, `cytat` | nowelizacji ogłoszonych po zindeksowanym t.j.; aktów poza korpusem |
| Akty poza korpusem i kontrola aktualnego publikatora (Dz.U., M.P.) | `isap` / ELI | `search_acts`, `get_act`, `get_act_text`, `api.sejm.gov.pl/eli` | komentarza autorskiego |
| Spółki w KRS | `krs` | `get_entity`, `get_entity_full`, `get_board` | CEIDG |
| Prawo UE, TSUE, decyzje organów ochrony danych (GDPRhub) | `eu-sparql` | `search_by_celex`, `search_by_date_range`, `search_cjeu`, `search_cjeu_by_ecli`, `search_gdprhub` | prawo krajowe |
| 14 regulacji UE offline (RODO, AI Act, DORA, NIS2, eIDAS 2.0, CRA, DSA, DMA, Data Act, DGA, LED, ePrivacy, Cybersecurity Act i in.) | `eu-compliance` | `eu_search`, `eu_article`, `eu_compare`, `eu_check_applicability`, `eu_evidence` | akty spoza korpusu |
| Komentarz do artykułu ustawy (37 ustaw: kodeksy, Konstytucja, ustawy ustrojowe, PPSA, koszty sądowe, prawo medyczne i konsumenckie, lokatorzy, Policja) | baza lokalna `scripts/ustawy.py` | `art <akt> <nr> --komentarz`, `szukaj` | brzmienia urzędowego (komentarz to opracowanie) |

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
  bazy. Pion rozpoznasz skryptem `pl_entities.py extract` (skill `citation-grounding-pl`, moduł `patron-identyfikatory-pl`).
- **Czy wyrok „żyje”:** `saos_cite_check` - późniejsze orzeczenia cytujące sygnaturę. Przeczytaj,
  w jakim kontekście ją przywołują (aprobata, krytyka, odmienny pogląd).
- **Treść przepisu:** w korpusie 37 aktów wywołaj `ustawy_artykul(akt, art, komentarz=false)`;
  gdy nie znasz artykułu, najpierw `ustawy_szukaj(q, akt?)`. Cytat dosłowny sprawdź
  `ustawy_cytat(akt, art, fragment)`. Sprawdź `tekst_jednolity` i `eli` z wyniku.
  **Baza nie uwzględnia późniejszych nowelizacji:** przed użyciem jako aktualnego prawa
  zweryfikuj zmiany po dacie t.j. w ELI (`api.sejm.gov.pl/eli`) i w razie zmian odczytaj
  aktualne brzmienie z publikatora. Gdy akt nie należy do korpusu (OUT_OF_SCOPE),
  użyj `isap` (`search_acts`, `get_act`, `get_act_text`) i/lub API ELI. Komentarz
  jest opracowaniem, nie brzmieniem urzędowym.
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
  narzędzia możesz zapisać do pliku i sprawdzić cytaty skryptem modułu `patron-weryfikacja-cytatow` skilla `citation-grounding-pl`
  (tryb `--quotes`).
- Treści GDPRhub mają licencję CC BY-NC-SA 4.0 - zaznacz to przy dłuższych cytatach.

## Format odwołań
- Akt: pełna nazwa + (Dz.U. ROK poz. NUMER) przy pierwszym przywołaniu, dalej skrót
  („art. 6 ust. 1 lit. f RODO”, „art. 415 k.c.”). ELI z wyniku `ustawy` lub `isap` jako referencja; status i nowelizacje zawsze potwierdź w ELI.
- Orzeczenie: „wyrok NSA z 12.05.2026 r., III OSK 1377/23” + link.
- Akt UE: „rozporządzenie 2016/679 (RODO)” + link EUR-Lex.
- Daty w treści: DD.MM.RRRR r.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/chat/prompts.ts`
(COURTS_PL, SAOS_DISCIPLINE_PL, DRAFTING_PL), `docs/BAZA_WIEDZY.md`. Konektory MCP: MIT.
