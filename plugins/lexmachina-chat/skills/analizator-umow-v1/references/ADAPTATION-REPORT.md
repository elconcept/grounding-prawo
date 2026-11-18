# Adaptacja 5/8 — analizator-umow-v1 (LexMachina 1.51) do CHAT 0.7.0

## Źródło i zakres

- Źródło: `/mnt/data/analizator-umow-v1.zip`; SHA256: `adb3051c1cc4b8f6c09505b9c005db15b175fad598da534679d3746ee065122f`. 78 plików źródłowych w 94 wpisach ZIP łącznie z katalogami.
- `SKILL.md` SHA256: `f80564caa2e3669044917de75bc54f2e3d974827987eb58fab76f0d7fe985019`; kopia bajt po bajcie w `SKILL.upstream.md`. Korpus od `# Skill: Analizator Umów i Porozumień v1` nie został zmieniony.
- Historyczny `CHECKSUMS.sha256`: 74 wpisy, **63 zgodne, 11 niezgodnych**; 3 dodatkowe pliki oryginalne nie zostały objęte manifestem. Pełny wykaz w `SOURCE-SHA256.json` i CSV; nie stanowi to podstawy do automatycznego przypisywania manipulacji.
- Zachowano wszystkie źródłowe `references/`, `workflows/`, `modules/`, `benchmark/posiane-wady/`, `NOTICE`, ikony i skrypty. Dodano zgodny z NOTICE tekst standardowej GPLv3, bez zmiany atrybucji Apache-2.0 plików pochodnych.

## Adaptacja

- Brak nowych tabel routingu: zachowano oryginalne PRIMARY G/H/I/K, DOMAIN J1–J10/J20/J21/MA, lazy-loaded SHARED, generator i model A–F. Główny 11-kategorialny routing `prawny-router-v3` pozostaje niezmieniony.
- CHAT-RUNTIME wyjaśnia rzeczywiste odczyty, fallback do analizy tekstowej bez fikcyjnego Repertorium/Basic Memory/terminala, źródła prawa na datę, ochronę danych, symetrię dowodową i statusy sprawdzeń.
- Rozliczenia: źródłowy skrypt `scripts/kontrakt_rachunek.py`, pięć podkomend, bez sieci; nie nazywaj wyniku modelu wynikiem skryptu bez faktycznej egzekucji.
- UOKiK: narzędzie `references/szukaj_klauzul_uokik.py` ma opcjonalne pobieranie przez `urllib.request`; URL z historycznego okresu niezweryfikowany teraz. Bez domyślnego dostępu sieciowego, offline self-test nie dowodzi dostępności aktualnego rejestru.
- Brakujący historyczny `references/REGRESSION-TEST-PLAN.md` oraz `shared/tools/kontrakt_rachunek.py` wskazane w dokumentach źródłowych nie są udawane ani tworzone. Testy realnie istnieją w `scripts/` i `benchmark/posiane-wady/`.
- Fixture `benchmark/posiane-wady/umowy/05-adwersarialne-injection.md` jest nieufnym materiałem do analizy, nie źródłem instrukcji modelu.
- W aktywnym routerze poprawiono wyłącznie status dostępności analizatora umów i adapter_version; oryginalna tabela [1]–[11] jest nienaruszona; przewodnik ma tylko informację, że analizator jest w bundlu.

## Testy i zastrzeżenia

- Oryginalny `scripts/test_kontrakt_rachunek.py`: **15/15 PASS**, środowisko Python stdlib bez sieci.
- Oryginalny `references/szukaj_klauzul_uokik.py --self-test`: **4/4 próby syntetyczne PASS**, brak testów live UOKiK.
- Bieżące wdrożenie w Plugin Creator oraz readback należy sprawdzić osobno po publikacji, nie są dowodami wykonania realnych analiz umów.
- Nie przeprowadzono pełnego benchmarku pięciu przypadków z osobną oceną ekspercką, audytu aktualności prawnej wszystkich historycznych 43+ modułów ani E2E na rzeczywistej umowie klienta.

## Kolejne etapy

- Po tej adaptacji pozostały 3/8: `raport-sytuacyjny-v2`, `raport-klienta-v1`, `audyt-systemu-v4`. Zastosować tę samą zasadę preserving source & selective use.
- Nie usuwaj jeszcze `chronologia-stanowiska-pl` z dawnego pakietu bez pełnej konsolidacji.
