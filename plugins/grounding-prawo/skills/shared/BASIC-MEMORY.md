# Pamięć sesji i sprawy

Dwa projekty mają odrębne role. Zawsze podawaj projekt jawnie; domyślny projekt serwera nie rozstrzyga miejsca zapisu.

| Projekt | Zawartość |
|---|---|
| `main` | Recap sesji: cel, wykonane działania, decyzje, wyniki kontroli, pliki, otwarte kwestie i następny krok |
| `legal` | Dokumenty źródłowe, postępowania, zdarzenia, osoby, teczki spraw, pisma, ustalenia i ich źródła |

## Dostęp i początek pracy

1. Użyj dostępnego konektora Basic Memory. Gdy nie jest widoczny, wyszukaj narzędzia `basic-memory` w portalu Lex.
   Nazwa hosta/prefix narzędzia może się różnić. `list_memory_projects` potwierdza `main` i `legal`.
2. W `main` wyszukaj ostatni recap dotyczący zadania; w `legal` odczytaj teczkę `sprawy/<katalog>/`, jej relacje
   i lekcje (`read_note`, `build_context`, `search_notes` po sygnaturze). Brak teczki: utwórz przed analizą.
3. Dla ingestu przeczytaj w `legal` `_metodologia/Metodologia ingestu` i `_metodologia/Zasady języka wiki`.
   Jeśli nazwa nie rozwiązuje się, wyszukaj notatkę. Nie udawaj odczytu niedostępnej metodyki.
4. Wznowienie zaczynaj od zaległych zapisów i stanu pisma. Wiki wskazuje źródła; nie zastępuje akt ani aktualnego prawa.

## Ingest wykonywany na serwerze

Pełny przebieg prowadzi skill `ingest-wiki` przez narzędzia `wiki_ingest` i `wiki_plan`.
Odczytaj podręcznik serwera `man(page="wiki-ingest")`; zawiera aktualny kontrakt.
Źródła, kolejka, OCR, weryfikacja zapisu i plany są dostępne przez MCP również w
claude.ai i chatgpt.com. Katalog projektu legal nie dostarcza silnika wykonawczego.
Submoduł `vendor/mcp/basic-memory` w repo pluginu przypina kompatybilne źródło
serwera; uruchomienie i aktualizacja serwera pozostają osobnym krokiem wdrożenia.

Rozbieżność techniczną wyjaśnij najpierw samodzielnie dostępnymi narzędziami i źródłami
(np. Git, gh, konfiguracja, logi). Pytaj autora dopiero, gdy nie udało się jej rozstrzygnąć.
Kanoniczne repozytorium to `elconcept/basic-memory`; `elconcept/mcp-basic-memory` jest starą nazwą.

## Samowystarczalność wiki

Biblioteka źródeł na serwerze jest wejściem do ingestu, nie miejscem docelowym cytowań.
W trakcie ingestu porównaj transkrypcję z każdą stroną oryginału; po potwierdzeniu
zapisz pełną treść w Basic Memory ze statusem weryfikacji (`stan_ingestu: pdf_reviewed`
dla PDF). Samo istnienie sidecara ani import historycznej notatki nie potwierdza weryfikacji.

Po ukończeniu ingestu odczyt, cytowanie i analiza dokumentu korzystają z zapisanej
transkrypcji w wiki. Linki źródłowe prowadzą do jej `[[permalink]]` i strony/bloku,
bez linków do zewnętrznych PDF, sidecarów, dysków NAS ani plików klienta. Ścieżka
pochodzenia i hash mogą zostać technicznymi metadanymi ingestu; nie zastępują treści.
Wiki musi pozostać użyteczna po odłączeniu biblioteki źródeł. Ponowna weryfikacja
jest potrzebna przy nowej wersji dokumentu lub konkretnej wykrytej rozbieżności,
nie przy każdym odczycie zweryfikowanej transkrypcji.

## Zapis w `legal` po każdym zakończonym etapie

- **Dokument:** przetwarzaj pojedynczo. Sprawdź istniejący wpis po identyfikatorze źródła i ścieżce.
  Zapisz tożsamość dokumentu, pełną transkrypcję w wiki, strony/segmenty, jakość odczytu i powiązania.
  Pełny tekst i wyciąg zapisuj według odczytanej metodyki ingestu; nie zastępuj źródła streszczeniem.
- **Ustalenie:** wskaż dokument i stronę/blok albo autora i datę relacji. Oddziel twierdzenie strony od ustalenia,
  zachowaj sprzeczności. Przebieg postępowania zapisuj w `postepowania/`, nie tylko w recapach.
- **Teczka `sprawy/<katalog>/`:** Stan, Terminy, Decyzje użytkownika, Lekcje, Pisma, Relacje.
- **Pismo `sprawy/<katalog>/pisma/`:** wersja, ścieżka, runda, otwarte uwagi, pytania, wyniki kontroli i status.
- **Orzeczenie:** zweryfikowane źródło, sygnatura i relacja do sprawy; sprawdź `orzeczenia/` przed kolejnym researchem.

Nie kończ ingestu na „zgłoszeniu do ingestu”. Zakończenie oznacza zapis dokumentu, ustaleń i relacji oraz odczyt
potwierdzający. Gdy brakuje metodyki lub źródła, oznacz etap NIEZAKOŃCZONY i zapisz dokładnie zaległą czynność.

## Recap w `main` — przed każdą odpowiedzią kończącą etap

Użyj jednej notatki sesji w `sesje/grounding-prawo/`: tytuł `RRRR-MM-DD — <temat> — <id sesji>`.
Użyj identyfikatora hosta, jeśli dostępny; w przeciwnym razie utwórz stabilny identyfikator przy pierwszym zapisie
(np. znacznik czasu UTC) i zachowaj go w kolejnych aktualizacjach. Przy wznowieniu odszukaj istniejącą notatkę.

Zapisz: cel użytkownika; wykonane działania; decyzje i ich przyczyny; pliki/wyniki z odnośnikami;
kontrole faktycznie wykonane; nierozstrzygnięte kwestie; następny krok; odnośniki do notatek `legal`.
Aktualizuj tę samą notatkę po istotnym etapie, przed długą operacją i przed odpowiedzią końcową.
Nie czekaj na komendę „zamknij” ani na zakończenie aplikacji. Sam recap nie zastępuje ingestu do `legal`.

## Potwierdzenie i awaria

Zapisy tylko przez MCP (`write_note`, `edit_note`). Przed zmianą istniejącej notatki odczytaj ją; stosuj dopisek
lub zmianę konkretnej sekcji, nie nadpisuj cudzych ustaleń. Przed ponowieniem niepewnego zapisu sprawdź, czy już istnieje.
Po zapisie wykonaj `read_note` i sprawdź treść ostatniej zmiany. Sukces to odczyt zgodny z zamierzeniem, nie samo wywołanie.

W odpowiedzi końcowej podaj krótko: `Pamięć: main — zapisano <identyfikator>; legal — zapisano <identyfikator>
/albo bez nowych ustaleń`. Gdy zapis się nie udał, podaj `NIEZAPISANE` i przyczynę.
Zaległość dopisz do `_PRZEBIEGI.md` pisma lub `_robocze/pamiec-zalegle.md` w folderze sprawy, z projektem,
identyfikatorem notatki i treścią do zapisu. Przy następnym wejściu ponów po sprawdzeniu duplikatów.
Można kontynuować pracę merytoryczną; nie deklaruj pełnego zakończenia ingestu ani skutecznego zapisu pamięci.
Nagłe zamknięcie procesu może uniemożliwić zapis; checkpointy ograniczają tę stratę, instrukcja nie jest hookiem hosta.
