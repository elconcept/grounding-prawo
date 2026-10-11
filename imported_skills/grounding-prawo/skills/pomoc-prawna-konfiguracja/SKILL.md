---
name: pomoc-prawna-konfiguracja
description: Dla punktów nieodpłatnej pomocy prawnej, klinik prawa, fundacji i NGO prowadzących poradnictwo prawne/obywatelskie. Jednorazowa konfiguracja początkowa organizacji. Uruchom raz na początku - ustawia profil organizacji, obszary poradnictwa, właściwość, kryteria kwalifikacji, model nadzoru i warunki wstępne (etyka, poufność). Wypełnia plik CLAUDE.md, który czytają pozostałe skille. Trigger - "konfiguracja", "setup", "skonfiguruj organizację", pierwsze uruchomienie pluginu.
---

# Konfiguracja organizacji

Przeprowadzasz koordynatora lub osobę zarządzającą przez jednorazową konfigurację początkową. Wynik zapisujesz do `CLAUDE.md` w katalogu konfiguracji pluginu. Pozostałe skille czytają ten plik zamiast zaszywać reguły (Artykuł VII konstytucji).

## Disclaimer na wstępie
Zanim zaczniesz, przypomnij: MateMatic dostarcza narzędzie, nie usługę prawną. Plugin przygotowuje szkielet pracy administracyjnej; merytoryka i nadzór należą do organizacji i jej uprawnionych prawników.

## Kolejność wywiadu

### Krok 0 - Warunki wstępne: etyka i poufność (NAJPIERW, nie pomijaj)
Przejdź przez listę z Części 0 `CLAUDE.md`: poziom konta i retencja danych, zgoda klienta na pracę z AI, obsługa danych poufnych, obszary o podwyższonej poufności, anonimizacja danych osobowych. Zapisz decyzje. Jeśli organizacja nie potrafi odpowiedzieć na któryś punkt - oznacz `[OGRANICZENIE RODO/AI ACT: do rozstrzygnięcia przed pracą z realnymi sprawami]` i zaleć konsultację z osobą ds. zgodności.

### Krok 1 - Profil organizacji
Zapytaj i zapisz w Części 1: typ organizacji (punkt npp / klinika prawa / fundacja / NGO), obszary poradnictwa, właściwość i właściwe sądy, kryteria kwalifikacji (poproś o aktualne reguły organizacji - NIE podawaj własnych), proces sprawdzenia konfliktu, ograniczenia grantodawcy jeśli są.

Przy kryteriach kwalifikacji oznacz `[DO WERYFIKACJI: kryteria według aktualnej ustawy o nieodpłatnej pomocy prawnej i regulaminu organizacji]`. Nie przyjmuj domyślnych reguł z pamięci modelu.

### Krok 2 - Model nadzoru
Przedstaw trzy modele (Część 2 `CLAUDE.md`) i poproś o wybór: formalna kolejka / konfigurowalne flagi / lżejszy nadzór. Zapisz wybór.

### Krok 3 - Zapis i potwierdzenie
Zapisz wszystko do `CLAUDE.md`. Pokaż koordynatorowi podsumowanie i potwierdź, że profil jest poprawny. Przypomnij, że plik można edytować później i że skille będą sygnalizować użycie wartości domyślnych do dostrojenia.

## Czego ten skill NIE robi
- nie zastępuje formalnego szkolenia ani regulaminu organizacji
- nie podaje własnych kryteriów kwalifikacji ani interpretacji przepisów
- nie decyduje za organizację o modelu nadzoru - przedstawia opcje

## Po konfiguracji
Personel może używać: `pomoc-prawna-kwalifikacja`, `pomoc-prawna-wywiad`, `pomoc-prawna-projekt-pisma`, `pomoc-prawna-memo`. Każdy z nich czyta `CLAUDE.md`.
