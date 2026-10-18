# Pamięć sesji i sprawy

Trzy projekty pełnią odrębne role. Projekt `model-memory` jest współdzielony pomiędzy modelami, ale nie zastępuje natywnej pamięci ChatGPT ani Claude. Zawsze podawaj projekt jawnie; domyślny projekt serwera nie rozstrzyga miejsca zapisu.

| Projekt | Zawartość |
|---|---|
| `main` | Projekt starszych recapów (odczyt archiwalny, nie zapisuj nowych). |
| `model-memory` | Przekrojowe preferencje użytkownika, decyzje, kontekst techniczny, cele i recapy sesji różnych modeli; bez powielania akt i materiałów źródłowych. |
| `legal` | Dokumenty źródłowe, postępowania, zdarzenia, osoby, teczki spraw, pisma, ustalenia i ich źródła |

## Dostęp i początek pracy

1. Użyj dostępnego konektora Basic Memory. Gdy nie jest widoczny, wyszukaj narzędzia `basic-memory` w portalu Lex.
   Nazwa hosta/prefix narzędzia może się różnić. `list_memory_projects` powinno potwierdzić `model-memory`, `main` i `legal`.
2. W `model-memory` wyszukaj ostatni recap i wspólne preferencje dotyczące zadania; starsze recapy można doczytać z `main`. W `legal` odczytaj teczkę `sprawy/<katalog>/`, jej relacje
   i lekcje (`read_note`, `build_context`, `search_notes` po sygnaturze). Brak teczki: utwórz przed analizą.
3. Dla ingestu przeczytaj w `legal` `_metodologia/Metodologia ingestu` i `_metodologia/Zasady języka wiki`.
   Jeśli nazwa nie rozwiązuje się, wyszukaj notatkę. Nie udawaj odczytu niedostępnej metodyki.
4. Wznowienie zaczynaj od zaległych zapisów i stanu pisma. Wiki wskazuje źródła; nie zastępuje akt ani aktualnego prawa.

## Ingest wykonywany na serwerze

Pełny przebieg prowadzi skill `ingest-wiki` przez narzędzia `wiki_ingest` i `wiki_plan`.
Odczytaj podręcznik serwera `man(page="wiki-ingest")`; zawiera aktualny kontrakt.
Źródła, kolejka, OCR, weryfikacja zapisu i plany są dostępne przez MCP również w
claude.ai i chatgpt.com. Katalog projektu legal nie dostarcza silnika wykonawczego.
Submoduł `vendor/general/basic-memory` w repo pluginu przypina kompatybilne źródło
serwera; uruchomienie i aktualizacja serwera pozostają osobnym krokiem wdrożenia.

Rozbieżność techniczną wyjaśnij najpierw samodzielnie dostępnymi narzędziami i źródłami
(np. Git, gh, konfiguracja, logi). Pytaj autora dopiero, gdy nie udało się jej rozstrzygnąć.
Kanoniczne repozytorium to `elconcept/basic-memory`; `elconcept/mcp-basic-memory` jest starą nazwą.

Przy ingescie, pytaniach do wiki i kontroli jej jakości przeczytaj `shared/WIKI.md`.

## Zapis w `legal` po każdym zakończonym etapie

- **Dokument:** przetwarzaj pojedynczo. Sprawdź istniejący wpis po identyfikatorze źródła i ścieżce.
  Zapisz tożsamość dokumentu, ścieżkę oryginału i Markdown, strony/segmenty, jakość odczytu i powiązania.
  Pełny tekst i wyciąg zapisuj według odczytanej metodyki ingestu; nie zastępuj źródła streszczeniem.
- **Ustalenie:** wskaż dokument i stronę/blok albo autora i datę relacji. Oddziel twierdzenie strony od ustalenia,
  zachowaj sprzeczności. Przebieg postępowania zapisuj w `postepowania/`, nie tylko w recapach.
- **Teczka `sprawy/<katalog>/`:** Stan, Terminy, Decyzje użytkownika, Lekcje, Pisma, Relacje.
- **Pismo `sprawy/<katalog>/pisma/`:** wersja, ścieżka, runda, otwarte uwagi, pytania, wyniki kontroli i status.
- **Orzeczenie:** zweryfikowane źródło, sygnatura i relacja do sprawy; sprawdź `orzeczenia/` przed kolejnym researchem.

Nie kończ ingestu na „zgłoszeniu do ingestu”. Zakończenie oznacza zapis dokumentu, ustaleń i relacji oraz odczyt
potwierdzający. Gdy brakuje metodyki lub źródła, oznacz etap NIEZAKOŃCZONY i zapisz dokładnie zaległą czynność.

## Recap w `model-memory` — przed każdą odpowiedzią kończącą etap

Użyj jednej notatki sesji w projekcie `model-memory`, katalog `sesje/grounding-prawo/`: tytuł `RRRR-MM-DD — <temat> — <id sesji>`.
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

W odpowiedzi końcowej podaj krótko: `Pamięć: model-memory — zapisano <identyfikator>; legal — zapisano <identyfikator>
/albo bez nowych ustaleń`. Gdy zapis się nie udał, podaj `NIEZAPISANE` i przyczynę.
Zaległość dopisz do `_PRZEBIEGI.md` pisma lub `_robocze/pamiec-zalegle.md` w folderze sprawy, z projektem,
identyfikatorem notatki i treścią do zapisu. Przy następnym wejściu ponów po sprawdzeniu duplikatów.
Można kontynuować pracę merytoryczną; nie deklaruj pełnego zakończenia ingestu ani skutecznego zapisu pamięci.
Nagłe zamknięcie procesu może uniemożliwić zapis; checkpointy ograniczają tę stratę, instrukcja nie jest hookiem hosta.

## Przenośność i hooki

Reguły odczytu/zapisu są konfigurowane per klient lub w pluginie. Na starcie każdej sesji host, który ma dostęp do MCP, powinien wyszukać odpowiedni kontekst `model-memory`; po istotnych zmianach zapisywać notatki i sprawdzać odczytem. Dla Claude Code można dołożyć hook z poleceniem odczytu/zapisu, ale sam plik instrukcji nie uruchamia hooka. **Wbudowana Memory ChatGPT nie może zostać przekierowana na MCP**; można ją uzupełniać o Basic Memory, o ile narzędzia są dostępne. Nie synchronizuj automatycznie całych rozmów ani sekretów.
