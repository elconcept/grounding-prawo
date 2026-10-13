---
name: pomoc-prawna-projekt-pisma
description: Dla punktów nieodpłatnej pomocy prawnej, klinik prawa, fundacji i NGO. Pierwszy szkic typowego pisma (pozew, wniosek, odpowiedź na pozew, wezwanie, odwołanie od decyzji) na podstawie notatki z wywiadu i wzorów organizacji. Każdy szkic oznaczony jako szkic, każdy cytat oznaczony do weryfikacji, każdy brakujący fakt oznaczony. NIE jest finalnym pismem ani nie składa pisma. Trigger - "projekt pisma", "szkic", "napisz pozew/wniosek/odwołanie", "pierwszy szkic".
---

# Projekt pisma (pierwszy szkic)

Tworzysz pierwszy szkic pisma do dalszej pracy prawnika. To punkt startowy, nie produkt końcowy.

## Najpierw przeczytaj konfigurację
Wczytaj `CLAUDE.md`: obszar, właściwość, właściwe sądy, wzory i szablony organizacji jeśli są, model nadzoru. Użyj wzorów organizacji jako podstawy. Jeśli organizacja nie ma wzoru dla danego pisma - oznacz `[DO WERYFIKACJI: brak wzoru organizacji - struktura orientacyjna, prawnik dostosowuje do wymogów formalnych]`.

## Wejścia
1. **Notatka z wywiadu** - fakty, strony, chronologia, dokumenty (ze skilla `pomoc-prawna-wywiad`)
2. **Typ pisma** - pozew, wniosek, odpowiedź, wezwanie, odwołanie od decyzji
3. **Wzór organizacji** - jeśli istnieje (z konfiguracji); brak -> struktura orientacyjna
4. **Cel pisma** - czego osoba żąda / co ma osiągnąć

Każdy fakt spoza notatki oznacz `[BRAK FAKTU: ...]`.

## RODO i poufność
`[OGRANICZENIE RODO/AI ACT: pismo zawiera dane stron i osoby korzystającej z pomocy - potwierdź zasady poufności z konfiguracji; pracuj na danych pseudonimizowanych (let-it-be), realne dane wstawia prawnik na końcu]`.

## Zasada cytatu (Artykuł III) - rama prawna
Każdy przepis, sygnatura orzeczenia i termin w szkicu MUSI nosić `[DO WERYFIKACJI: ...]`. Bez podłączonego konektora orzecznictwa traktuj wszystkie cytaty jako niezweryfikowane. Nie podawaj numerów artykułów jako pewnik - jeśli nie masz pewności, napisz `[POTRZEBNE BADANIE: podstawa prawna do ustalenia]` zamiast zgadywać.

## Zasada faktu
Każdy fakt, którego nie ma w notatce z wywiadu, oznacz `[BRAK FAKTU: ...]`. Nie wymyślaj danych stron, kwot, dat ani okoliczności.

## Struktura szkicu
1. `[SZKIC AI - wymaga analizy i nadzoru uprawnionego prawnika]` (etykieta przeglądu - usuń przed złożeniem)
2. Nagłówek / oznaczenie sądu i stron - z `[BRAK FAKTU: ...]` gdzie brak danych
3. Treść według typu pisma i wzoru organizacji
4. Podstawa prawna - każda pozycja `[DO WERYFIKACJI: ...]`
5. Wnioski / żądania
6. **Lista kontrolna dla prawnika:** braki faktów, cytaty do weryfikacji, wymogi formalne i terminy do sprawdzenia, oznaczenie czy w trybie nadzoru wymaga `SPRAWDŹ Z KOORDYNATOREM PRZED ZŁOŻENIEM`

## Czego ten skill NIE robi
- nie składa pisma i nie liczy terminów z daty zdarzenia
- nie podaje wiążących podstaw prawnych - wszystko do weryfikacji
- nie zastępuje oceny formalnych wymogów pisma przez prawnika
- nie wymyśla faktów ani danych stron

## Po szkicu
Weryfikacja cytatów: skill citation-grounding-pl. Analiza problemu: `pomoc-prawna-memo`. Archiwizacja śladu: legal-ai-audit-bundle. Ślad: zaloguj szkic, użyte źródła, kto przegląda (Artykuł V).
