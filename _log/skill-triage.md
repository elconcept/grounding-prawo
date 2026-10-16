# Triage skilli — grounding-prawo

Stan audytu: 2026-10-11.

## Aktywny podział pluginu

| Warstwa | Zakres | Przykładowe skille |
|---|---|---|
| `source-routing` | wybór właściwej bazy i hierarchia źródeł | `hierarchia-zrodel-pl`, `patron-prawo-pl-zrodla`, `legal-request-router-pl` |
| `primary-law` | obowiązujące brzmienie ustaw, rozporządzeń i aktów normatywnych | `lexcache`, `prawo-polskie-v2`, `dr-01`…`dr-16`, `eu-sparql-search` |
| `case-law` | orzeczenia PL/UE, wyszukiwanie, identyfikacja i analiza | `saos-orzecznictwo`, `szukaj-orzeczen-v2`, `orzeczenia-sadowe-v2`, `webwright-legal-pl` |
| `interpretations` | interpretacje podatkowe i decyzje organów | MCP `eureka`, `uodo-grounding-pl` |
| `grounding` | ekstrakcja oraz mechaniczna weryfikacja cytatów | `ekstraktor-cytatow-pl`, `citation-grounding-pl`, `patron-weryfikacja-cytatow` |
| `document-ingest` | OCR i przygotowanie materiału do researchu | `the-ocr`, `ugh-ocr`, `akta-przeszukiwalne-pl`, `doc-intel-*`, `patron-skan-dokumentu` |
| `domain-routing` | kierowanie do domeny prawa polskiego | `prawny-router-v3`, `prawo-polskie-v2`, moduły `dr-01`…`dr-16` |

## Deduplikacja i merge

W aktywnym pluginie nie wykryto identycznych katalogów skillowych. Zidentyfikowane
duplikaty między pipeline’ami mają jedną kopię kanoniczną w
`plugins/grounding-prawo/skills/`; identyczne kopie przeniesiono do
`archive/duplicates/` wraz z ich plikami towarzyszącymi.

### Zestawienia wymagające decyzji użytkownika

Poniższe pary są podobne, lecz nieidentyczne. Nie zostały automatycznie scalone,
bo konflikt dotyczy zakresu lub wersji, a nie samego formatowania:

1. `saos-orzecznictwo` ↔ `szukaj-orzeczen-v2` — adapter API vs. pełny workflow raportu;
2. `iura` ↔ `patron-prawo-pl-zrodla` — SAOS/ISAP vs. wieloźródłowy router MCP;
3. `citation-grounding-pl` ↔ `patron-weryfikacja-cytatow` — silnik gradientu vs. format CITATIONS;
4. `the-ocr` ↔ `ugh-ocr` — różne pipeline’y OCR i fallbacki;
5. `analiza-sadowa-v6`, `analizator-dowodow-v3`, `analizator-przepisow-v2`,
   `analizator-umow-v1` — wersje raportowe i analityczne z odmiennymi kontraktami;
6. `prawny-router-v3` ↔ `prawo-polskie-v2` — router wykonawczy vs. fasada domenowa;
7. `uodo-grounding-pl` ↔ ogólny `citation-grounding-pl` — weryfikator domenowy vs. silnik ogólny.

## Archiwum

Do `archive/skills/` przeniesiono 17 skilli organizacyjnych, compliance i
operacyjnych poza zakresem groundingu. Do `archive/duplicates/` przeniesiono 9
identycznych kopii z pipeline’ów źródłowych. Nic nie jest usuwane. Przed ich ewentualnym przywróceniem trzeba sprawdzić
odwołania w `companion_skills`.
