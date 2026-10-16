---
name: prowadnik-grounding-prawo
description: "Skill wejściowy pluginu grounding-prawo: ustala cel użytkownika (analiza akt i dowodów, napisanie pisma, doskonalenie pisma, pytanie o przepis lub orzeczenie, umowa, RODO, dokumenty), wskazuje właściwą ścieżkę i kolejne skille oraz pliki wynikowe. Używaj na początku pracy nad sprawą, gdy nie wiadomo, od którego skilla zacząć, gdy model się gubi między skillami albo gdy pytanie dotyczy tego, co plugin potrafi."
---

# Prowadnik grounding-prawo

Ten skill nie wykonuje analizy prawnej. Wybiera ścieżkę i podaje następny skill. Pełny opis ścieżek, skilli i konektorów: `PRZEWODNIK.md` w katalogu spraw (`legal`), jeśli jest w zasięgu; komendy `/sprawa`, `/pismo`, `/kontrola` w tym katalogu prowadzą tymi ścieżkami.
Zawsze razem z `profil-postepowan-wlasnych`. Przed pierwszą czynnością przeczytaj `shared/ZASADY-PLUGINU.md` (model dowodowy, zasada „brak numeru lepszy niż błędny numer”, kolejność źródeł, człowiek decyduje) - marketplace nie instaluje CLAUDE.md, więc te reguły są częścią pluginu.

## Krok 1: ustal cel i stan materiału

Zapytaj jednym pytaniem, tylko jeśli odpowiedzi nie da się wyczytać z rozmowy:

1. Co ma powstać: odpowiedź na pytanie, analiza, nowe pismo, poprawa istniejącego pisma, przegląd umowy?
2. Jakie materiały są: pliki (skany czy tekst), draft pisma, sama relacja użytkownika?
3. Czy jest folder sprawy (`analiza/`, `drafty/`)? Jeśli nie, zaproponuj go (reguła: `shared/ARTEFAKTY-SPRAWY.md`).

## Krok 2: wybierz ścieżkę

| Cel | Ścieżka (kolejność skilli) | Pliki |
|---|---|---|
| **A. Analiza akt i dowodów** | `the-ocr` → `akta-przeszukiwalne-pl` → `chronologia-sprawy-v1` → `analizator-dowodow-v3` → `analizator-przepisow-v2` → `analiza-sadowa-v6` (+ `case-risk`, `medical-consent`, `uoozp-compliance`, `patron-analiza-akt-karnych` wg tematu) | `analiza/_dokumenty.md`, `_chronologia.md`, `_dowody-i-przepisy.md`, `_podsumowanie.md` |
| **B. Nowe pismo** | `prawny-router-v3` → `pisma-procesowe-v3` (typ z tabeli) albo `pisma-proste-v2` albo `zawiadomienie-o-przestepstwie` albo `rodo-dsar-pl`; pomocniczo `kalkulatory-procesowe-pl`, `terminy-procesowe-pl` | `drafty/<pismo>/rrrrMMdd_<nazwa>_v1`, `_SUBSUMPCJA.md`, `_PRZEBIEGI.md` |
| **C. Doskonalenie pisma** | domyślnie `szturm-na-draft-pl`; ręcznie: `ekstraktor-cytatow-pl` → `citation-grounding-pl` → `subsumpcja-pl` → `pierwsze-wrazenie-sedziego-pl` → `atak-przeciwnika-pl` → `adversarial-legal-review-pl` → `deliverable-fidelity-pl` → `pisz-po-polsku` | kolejne `_vN`, `_FINDINGS.md`, `_PRZEBIEGI.md` |
| **D. Pytanie o prawo** | `patron-prawo-pl-zrodla` (wybór konektora) → `orzeczenia-sadowe-v2` / `analizator-przepisow-v2` / `struktura-wyroku-pl`; poza MCP: `webwright-legal-pl` | odpowiedź; do sprawy dopisek w `_dowody-i-przepisy.md` |
| **E. Umowy, RODO, dokumenty** | `analizator-umow-v1` → `klauzule-kontraktowe-pl` → `redline-docx-pl`; wiele dokumentów: `patron-przeglad-tabelaryczny`; podpis PDF: `waliduj-podpis-pdf-pl` | `analiza/_podsumowanie.md`, redline w `_robocze/` |

Ścieżki łączą się: po A idzie B, po B idzie C. Wynik jednej ścieżki jest wejściem następnej - nie zaczynaj od zera.

## Krok 3: zasady przejść

- Każdy skill ma na końcu sekcję **MOST** (wejście, wynik, następny krok, czego nie dublować). Idź za nią.
- Nowe pliki tylko według `shared/ARTEFAKTY-SPRAWY.md`. Wiedza do doskonalenia kolejnych pism trafia do `_wiedza.md`.
- Przepisy i orzeczenia tylko z narzędzi MCP portalu (`patron-prawo-pl-zrodla`); brzmienie przepisu wg `shared/MOD-TEKST-JEDNOLITY.md`.
- Gdy dwa skille pokrywają to samo, wybierz wg kolumny „Nie dubluj” w MOST: wyspecjalizowany skill wygrywa z ogólnym, a skill-orkiestrator (`szturm-na-draft-pl`, `analiza-sadowa-v6`) z ręcznym przepuszczaniem soczewek.
- Domeny poza zakresem pluginu (prawo pracy, podatki, zamówienia publiczne, samorząd, budownictwo, compliance): powiedz to wprost i użyj źródeł z MCP zamiast zgadywać.
- Wynik kontroli to `PASS`, `FAIL`, `NOT_CHECKED` albo `NEEDS_REVIEW`; nie ogłaszaj gotowości pisma przy niezweryfikowanym cytacie.
