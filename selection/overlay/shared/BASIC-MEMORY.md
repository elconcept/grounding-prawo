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

## Ingest PDF — wyłącznie przez model LLM

Ingest do `legal` prowadzi wyłącznie model, wykonując po jednej stronie PDF:
`ingest-wiki` → `the-ocr` (Google Vision/Azure) → kontrola OCR i obrazu
→ ewentualnie ponowny odczyt Datalab/LlamaParse → zatwierdzenie strony.
Nie korzystaj z `wiki_ingest` (refresh, start, extract, index) ani
kolejki z dawnych bind mountów. Na serwerze Basic Memory nie ma już
`/dokumentacja`, a model tworzy źródła Markdown tylko po weryfikacji
całego PDF. Rozdziel dokumenty zawarte w jednym PDF na osobne notatki;
źródłowy tekst pozostaje bez modyfikacji i każdą stronę zaczyna
`==< plik.pdf (Page n/total_document_pages) >==`.

Binarne PDF nie trafiają do Basic Memory: model wywołuje archiwizację
niezmienionego źródła do dwóch prywatnych bucketów MinIO i R2 i dopiero
po potwierdzeniu obu kopii zapisuje notatkę źródłową w `legal/dokumenty`.
Notatki wtórne tworzy lub aktualizuje osobno i łączy linkami do źródła.
`wiki_plan` pozostaje niezależnym narzędziem planowania, nie uruchamia OCR.

Niedostępność OCR, obrazów lub jednej z kopii źródła oznacza przerwany
ingest, nie status „zweryfikowany”. Wymagaj faktycznego zapisu
`write_note` i kontroli przez `read_note`.


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
