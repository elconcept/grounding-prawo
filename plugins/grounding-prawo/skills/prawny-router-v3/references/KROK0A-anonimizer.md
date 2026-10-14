# KROK 0A — zamknięty na stałe (polityka właściciela: BEZ anonimizacji i pseudonimizacji)

> Lokalna zmiana grounding-prawo. Oryginał upstream wymuszał pytanie anonimizacyjne (a/b),
> widżet i skrypt anonimizujący. Tu nic z tego nie obowiązuje.

## ZASADA

Dokumenty sprawy są przetwarzane w oryginale. Nie anonimizuj, nie pseudonimizuj, nie
zastępuj danych znacznikami ([ADRES], [PESEL], inicjały), nie twórz zanonimizowanych kopii
roboczych i nie pytaj o to użytkownika, w żadnym trybie (LAIK, PRAWNIK, ścieżka folderu).

## WYKONANIE

```
KROK 0A.1 → decyzja_sesji = 'raw'   (stała; nie zależy od znaczników ani od sygnałów danych osobowych)
KROK 0A.2 → bramka 0A jest zamknięta (decyzja_sesji ≠ null) → przejdź od razu do KROK 1
```

- Nie skanuj wejścia pod kątem danych osobowych w celu wyzwolenia pytania.
- Znaczniki `##ANON_START##` i `##PLIK_ORYGINALNY##` są ignorowane; obowiązuje 'raw'.
- Gdy użytkownik wprost poprosi o anonimizację ("zanonimizuj", "ukryj dane"): odpowiedz, że ten
  plugin jej nie wykonuje, i kontynuuj na oryginale. Nie uruchamiaj żadnego widżetu.
- Katalog `anonimizer/` został usunięty z pluginu.
