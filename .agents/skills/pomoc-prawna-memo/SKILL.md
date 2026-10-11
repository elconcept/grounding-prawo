---
name: pomoc-prawna-memo
description: Dla punktów nieodpłatnej pomocy prawnej, klinik prawa, fundacji i NGO. Szkielet analizy sprawy w schemacie IRAC (problem - reguła - zastosowanie - wniosek), poprzedzonym stanem faktycznym jako wsadem. Buduje SZKIELET - miejsca na reguły oznacza jako luki badawcze, zastosowanie i wniosek zostawia puste do wypełnienia przez prawnika. NIE pisze analizy za prawnika - daje uporządkowaną ramę. Trigger - "memo", "analiza sprawy", "IRAC", "szkielet analizy", "rama do opinii".
---

# Memo (szkielet IRAC)

Budujesz szkielet analizy, nie analizę. Wypełniasz to, co bezpieczne (stan faktyczny, ramowanie problemu, kierunki poszukiwań), a miejsca wymagające osądu prawnika zostawiasz jawnie puste z markerami. Wzorzec: reguły = luka badawcza, zastosowanie i wniosek = miejsce prawnika.

IRAC to cztery elementy: Issue (problem), Rule (reguła), Application (zastosowanie), Conclusion (wniosek). Stan faktyczny nie jest elementem IRAC - to wsad, który porządkujesz przed analizą.

## Najpierw przeczytaj konfigurację
Wczytaj `AGENTS.md`: obszar, właściwość, model nadzoru. Dobierz ramowanie do obszaru sprawy.

## Wejścia
1. **Stan faktyczny** - z notatki z wywiadu (wsad, nie element IRAC)
2. **Problem do analizy** - pytanie prawne, jeśli już sformułowane; jeśli nie - pomożesz je ująć
3. **Obszar sprawy** - z konfiguracji; dobiera ramowanie

Luki w faktach oznacz `[BRAK FAKTU: ...]`.

## RODO i poufność
`[OGRANICZENIE RODO/AI ACT: stan faktyczny może zawierać dane wrażliwe - pracuj na danych pseudonimizowanych (let-it-be); analizę na realnych danych prowadzi prawnik]`.

## Struktura
1. `[SZKIC AI - wymaga analizy i nadzoru uprawnionego prawnika]`
2. **Stan faktyczny (wsad)** - z notatki z wywiadu; luki jako `[BRAK FAKTU: ...]`
3. **Problem (Issue)** - sformułowanie pytania prawnego; jeśli niejasne `[NIEPEWNE: ...]`
4. **Reguła (Rule)** - NIE podajesz przepisów jako pewnik. Każdy blok reguły = `[POTRZEBNE BADANIE: podstawa prawna i orzecznictwo do ustalenia - obszar/kierunek poszukiwań]`. Możesz wskazać kierunek (np. "ustawa właściwa dla obszaru X"), ale jako trop, nie cytat.
5. **Zastosowanie (Application)** - `[ANALIZA PRAWNIKA: subsumpcja faktów pod regułę - do wypełnienia]` (puste z założenia)
6. **Wniosek (Conclusion)** - `[WNIOSEK PRAWNIKA: do wypełnienia po analizie]` (pusty z założenia)
7. **Luki i następne kroki** - zbiorcza lista `[POTRZEBNE BADANIE]`, `[BRAK FAKTU]`, `[DO WERYFIKACJI]`

## Zasady
- Reguły to tropy, nie autorytatywne cytaty (Artykuł III). Bez konektora orzecznictwa wszystko `[DO WERYFIKACJI]`.
- Zastosowanie i wniosek są puste celowo - to praca prawnika, nie modelu.
- Ufaj flagom bardziej niż ich brakowi.

## Czego ten skill NIE robi
- nie pisze analizy ani wniosku za prawnika
- nie podaje przepisów ani orzeczeń jako pewnik
- nie ocenia szans sprawy

## Po memo
Weryfikacja cytatów: citation-grounding-pl. Stress-test argumentacji (sprawy wysokiej stawki): adversarial-legal-review-pl. Archiwizacja: legal-ai-audit-bundle. Ślad: zaloguj szkielet i kto wypełnia oraz przegląda (Artykuł V).
