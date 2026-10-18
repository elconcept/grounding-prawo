# Ocena llm-wiki-plugin i integracji Basic Memory

Źródło: praneybehl/llm-wiki-plugin, commit
`32014c82da97d1b6a7e05bc685b256284d6b3a40` (MIT), szczególnie
`references/ingest-workflow.md`, `query-workflow.md`, `lint-workflow.md`.
Przegląd: 2026-10-18. Własna adaptacja procedur; bez kopiowania silnika wykonawczego.

| Element | Decyzja i miejsce |
|---|---|
| Rozpoznanie istniejących stron przed ingestem | Adaptacja w `shared/WIKI.md` i `ingest-wiki` |
| Aktualizacja fragmentów, sprzeczności z obydwoma źródłami | Adaptacja; pierwszeństwo oryginałów nad wcześniejszą parafrazą |
| Indeks, powiązania i źródła nowych stron | Istniejący `wiki_ingest index` i graf Basic Memory; instrukcja kontroli osieroconych notatek |
| Odpowiedź zapisana jako synteza | Nowy `wiki-basic-memory`, tylko dla nowych ustaleń/porównań |
| Lint strukturalny i semantyczny | Kontrola przez istniejące MCP, z jawnym zakresem; nie deklarujemy pełnego automatycznego skanu bazy |
| Osobny graph.sqlite, embedding cache, skrypty wyszukiwania | Pominięte: dublowałyby istniejący graf i wyszukiwarkę Basic Memory |
| Pętle evolve, lokalny CLI, pobieranie modeli | Pominięte: niepotrzebne do działania przez zdalne MCP |
| Limity 400/800 linii i sharding po 300 | Nie przeniesiono arbitralnych progów; dzielenie według tematów i zachowanie źródeł |
| Surowy sidecar uznany za źródło | Odrzucone dla PDF: osobna bramka porównania obrazów wszystkich stron |

Praneya workflow nie rozwiązuje automatycznie wierności OCR. Własna poprawka serwera
zatrzymuje zapis PDF do `dokumenty/`, dopóki model nie obejrzy stron przez MCP i nie
zatwierdzi poprawionej transkrypcji. Potwierdzenie jest związane z wersją PDF i sidecara.
To kontrola procesu; semantyczna trafność transkrypcji nadal zależy od oceny obrazów.

Reguły wykonawcze mają jedno źródło w `selection/overlay/shared/WIKI.md` i skillach.
README objaśnia funkcje użytkownikowi; build nie kopiuje całego README do promptu.
Mechanizm `add_session_protocol()` zapewnia odsyłacze do reguł wewnątrz paczki obu hostów.
Testy paczki nie są testem aktywacji na koncie użytkownika w aplikacjach przeglądarkowych.
