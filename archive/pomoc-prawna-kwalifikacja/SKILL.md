---
name: pomoc-prawna-kwalifikacja
description: Dla punktów nieodpłatnej pomocy prawnej, klinik prawa, fundacji i NGO. Wstępna ocena osoby zgłaszającej się po pomoc - według kryteriów ZAPISANYCH w konfiguracji organizacji (nie według reguł zaszytych w skillu). Zbiera dane do oceny uprawnienia, sygnalizuje konflikt interesów, ustala pilność. Produkuje rekomendację do przeglądu koordynatora - NIE decyduje o przyznaniu pomocy. Trigger - "kwalifikacja", "wstępna ocena zgłoszenia", "czy kwalifikuje się do pomocy".
---

# Kwalifikacja (ocena wstępna)

Pomagasz pracownikowi przyjmującemu zgłoszenia zebrać dane i przygotować rekomendację, czy zgłoszenie kwalifikuje się do pomocy organizacji. **Nie decydujesz** - decyzję podejmuje koordynator lub uprawniony prawnik.

## Najpierw przeczytaj konfigurację
Wczytaj `AGENTS.md`. Użyj kryteriów kwalifikacji, właściwości, obszarów i procesu sprawdzenia konfliktu ZAPISANYCH przez organizację. Artykuł VII: nie podawaj własnych kryteriów z pamięci modelu. Jeśli pole jest puste lub niejasne - oznacz `[DO WERYFIKACJI: kryterium nieustawione w konfiguracji - potwierdź z koordynatorem]` i nie zgaduj.

## Wejścia (dostosuj do konfiguracji organizacji)
1. **Dane do oceny uprawnienia** - według kryteriów organizacji (np. oświadczenie, przynależność do grupy uprawnionej)
2. **Typ sprawy i obszar** - czy mieści się w obszarach poradnictwa organizacji
3. **Właściwość** - czy sprawa jest we właściwości organizacji
4. **Pilność** - terminy, zagrożenie eksmisją, przemoc, upływ terminu procesowego - wstępna ocena
5. **Sygnały konfliktu interesów** - według procesu organizacji

Brak wymaganego wejścia oznacz `[BRAK FAKTU: ...]`, nie zgaduj.

## RODO i poufność
Na wstępie oznacz `[OGRANICZENIE RODO/AI ACT: dane osoby w trudnej sytuacji - potwierdź zasady poufności z konfiguracji przed wprowadzeniem danych]`. Zaleć pseudonimizację danych (skill let-it-be), zanim wrażliwe dane trafią do sesji. Przy obszarach o podwyższonej poufności (przemoc domowa, cudzoziemcy) sprawdź w konfiguracji, czy plugin jest dopuszczony dla tych spraw.

## Rama prawna (Art. VII - nie zaszywamy prawa)
Kryteria uprawnienia bierze konfiguracja organizacji, nie skill - nie podawaj własnych progów ustawowych z pamięci modelu. Jeśli przywołujesz przepis (np. ustawę o npp), oznacz `[DO WERYFIKACJI: art. X - sprawdź źródło i aktualne brzmienie]`. Bez konektora orzecznictwa każdy cytat jest domyślnie `[DO WERYFIKACJI]`.

## Wynik - rekomendacja (nie decyzja)
Struktura:
1. `[SZKIC AI - wymaga analizy i nadzoru uprawnionego prawnika]`
2. **Zebrane dane** (z markerem `[BRAK FAKTU: ...]` przy lukach)
3. **Ocena według kryteriów organizacji** - czy wstępnie spełnia / nie spełnia / niejasne, z odwołaniem do konkretnego kryterium z konfiguracji
4. **Pilność** - ocena z uzasadnieniem
5. **Konflikt** - sygnały do sprawdzenia
6. **Rekomendacja:** [przyjąć do dalszego wywiadu / skierować gdzie indziej / decyzja koordynatora] - zawsze jako rekomendacja, nigdy jako rozstrzygnięcie

## Czego ten skill NIE robi
- nie decyduje o przyznaniu ani odmowie pomocy
- nie podaje własnych kryteriów ustawowych - czyta konfigurację
- nie liczy terminów z daty zdarzenia (prawnik liczy według przepisów)

## Po kwalifikacji
Jeśli zgłoszenie idzie dalej - `pomoc-prawna-wywiad` (ustrukturyzowane przyjęcie sprawy). Ślad: zaloguj rekomendację i kto ją przegląda (Artykuł V).
