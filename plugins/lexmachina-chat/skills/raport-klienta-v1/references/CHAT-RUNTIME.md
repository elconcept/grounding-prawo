# CHAT-RUNTIME — raport-klienta-v1 v1.9 / bundle 0.9.0

## Model wykonania i źródła
1. Otrzymaj wynik rzeczywiście przeprowadzonej analizy sprawy. Nie twierdź, że `raport-sytuacyjny-v2` lub `prawny-router-v3` zostały wykonane, jeżeli nie było faktycznego odczytu/analizy; raport klienta jest **postprocesorem** i nie klasyfikuje sprawy ponownie.
2. Ustal tryb sytuacji przed profilem odbiorcy: `standard`, `brak_nowosci`, `zle_wiadomosci` albo `ograniczenie_szkod`. Profil IND lub BIZ wynika z odbiorcy/polecenia, nie z autorytetu ani z wymuszania nowej ankiety. Nie nazywaj „brak nowości” sytuacji, gdy nie masz poprzedniego raportu.
3. Przeczytaj `references/BLUEPRINT-SCHEMA.md` i `references/jezyk-klienta.md`. Dla BIZ koniecznie `references/sekcje-biznesowe.md`. Zachowaj kompletny schemat i źródłowe wymagania; klauzule NDA/ekspozycja finansowa/ryzyka w raporcie BIZ uwzględniaj tylko na podstawie rzeczywistych danych.
4. Nie zmieniaj oryginalnej metodologii, punktów wywołania, self-check, sekcji `delta` i ograniczeń przy złych wiadomościach. `ograniczenie_szkod` może wymagać realnej kontroli wyczerpania środków zaskarżenia i terminów, bez wymyślania hipotetycznych wariantów.

## Poufność klienta, symetria i czysty raport
- Obserwacja bezpośrednia, relacja uczestnika, dokument i twierdzenia w dokumencie — to osobne typy danych. Status urzędowy nie nadaje automatycznej prawdziwości jego narracji. Relacje TK/NC nie są z definicji słabsze niż twierdzenia Policji/szpitala; ocena faktograficzna opiera się na konkretnych podstawach i równym standardzie krytycyzmu.
- Raport do wysłania jest **zewnętrzny**: usuń uwagi kancelaryjne, procesowe słabości i niewymagane wrażliwe szczegóły; nie wysyłaj go samodzielnie. Zachowaj jedynie potrzebne, uzasadnione informacje o stanie sprawy i kolejnych krokach.
- Wszelkie akty prawa, orzecznictwo, daty, terminy i procenty wymagają rzeczywistej podstawy. Przy brakach nie dopisuj wartości 0 ani wymyślonej prognozy; `NOT_CHECKED` przy niesprawdzonych przepisach i terminach. Nie deklaruj, że kontrola `JUR:*` została wykonana przez samo przytoczenie nazwy.

## Native ChatGPT UI i artefakty
- Oryginalny plik `assets/widget-raport-klienta.html` pozostaje nienaruszony dla kompatybilnego hosta. W CHAT stosuj wyłącznie realnie dostępny renderer, z wymaganym blueprintem; jeżeli go brak, pełny raport tekstowy, nie pseudo-widget.
- Eksport PDF, edycja inline, import i potwierdzenie odbioru działają tylko po rzeczywistym utworzeniu/wykonaniu. Nie udawaj wysłania klientowi, eksportu czy automatycznej aktualizacji danych.
- Zachowaj scenariusze IND/BIZ, złe wiadomości, ograniczenie szkód i brak zmian. Datę poprzedniego raportu, `delta`, historię, zgody i źródła wskazuj tylko gdy dostępne.
- Statusy audytu na końcu: `INPUT_ANALYSIS_READ/NOT_READ`, `LEGAL_VERIFIED/NOT_CHECKED`, `BLUEPRINT_COMPLETE/PARTIAL`, `RENDERED/TEXT_FALLBACK`, `ARTIFACT_CREATED/NOT_CREATED`, `DELTA_COMPARED/NO_BASELINE`.
