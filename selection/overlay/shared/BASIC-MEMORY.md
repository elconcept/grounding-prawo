# Pamięć sesji i sprawy

Basic Memory działa na własnym serwerze (`https://bm.xlap.pl/mcp`, OAuth) z jednym projektem `main`. Konektor
i cykl sesji dostarcza plugin `basic-memory-nas` (`elconcept/basic-memory-plugin`): skille `bm-orient`, `bm-checkpoint`,
`bm-decide`, `bm-remember`, schematy `session`, `decision`, `task` i brief na starcie sesji. Ten plik dokłada wyłącznie
reguły prawnicze. Konfiguracja repozytorium (`.claude/settings.json` → `basicMemory`, `.codex/basic-memory.json`) ma
pierwszeństwo przed przykładami poniżej. Zawsze podawaj `project` jawnie.

| Miejsce w `main` | Zawartość | `type` |
|---|---|---|
| `legal/sessions/` | Checkpointy i recapy sesji: cel, działania, decyzje, wyniki, błędy, otwarte sprawy, następny krok | `session` |
| `legal/decyzje/` | Decyzje autora z uzasadnieniem i co najmniej jedną obserwacją `- [decision] ...` | `decision` |
| `legal/zadania/` | Zadania i terminy z `status` | `task` |
| `legal/bm-remember/` | Krótkie, trwałe ustalenia i preferencje warte zapamiętania między sesjami i modelami | `note` |
| `legal/sprawy/<katalog>/` | Teczki spraw, pisma, ustalenia, relacje i ich źródła | według treści |
| `legal/dokumenty/`, `legal/postepowania/`, `legal/orzeczenia/`, `legal/relacje/<autor-slug>/` | Dokumenty źródłowe, przebieg postępowań, zweryfikowane orzeczenia, relacje autorów | według treści |

Nie twórz projektów ani folderów spoza tej mapy (`checkpoints/`, `sesje/`, `model-memory`, osobny projekt `legal`).
Pliki repozytorium `legal` (pisma, PDF, `relacje/*.md`) przywołuj zwykłym linkiem Markdown albo polem
`source_path` we frontmatterze. `[[...]]` jest zarezerwowane dla notatek, które istnieją w Basic Memory;
odnośnik do pliku repozytorium jako relacja grafu pozostaje nierozwiązany.

Narzędzia serwera: `bm_project`, `bm_search`, `bm_find`, `bm_list`, `bm_read`, `bm_context`, `bm_write`, `bm_edit`,
`bm_move`, `bm_delete`, `bm_schema`, `bm_man` (prefiks hosta może się różnić). Dawne nazwy (`write_note`, `read_note`,
`search_notes`, `build_context`, `list_directory`, `list_memory_projects`) już nie istnieją.

## Dostęp i początek pracy

1. Użyj konektora Basic Memory (Claude Code: plugin `basic-memory-nas`; ChatGPT: aplikacja Basic Memory (NAS)).
   `bm_project(command="list")` musi pokazać projekt `main`.
2. Przed pierwszą odpowiedzią merytoryczną wykonaj `bm-orient` albo co najmniej:
   `bm_search(project="main", note_types=["session"], path="legal/sessions", since="3d")`, aktywne zadania
   (`note_types=["task"]`, `filters={"status": "active"}`) i świeże decyzje. Przeczytaj najnowszy właściwy checkpoint.
3. Dla sprawy odczytaj teczkę `legal/sprawy/<katalog>/`, jej relacje i lekcje (`bm_read`, `bm_context`,
   `bm_search` po sygnaturze). Brak teczki: utwórz przed analizą.
4. Dla ingestu przeczytaj metodykę ingestu i zasady języka wiki (`bm_search` po tytule). Jeśli nie istnieje,
   nie udawaj jej odczytu.
5. Wznowienie zaczynaj od zaległych zapisów i stanu pisma. Wiki wskazuje źródła; nie zastępuje akt ani aktualnego prawa.

## Ingest PDF — wyłącznie przez model LLM

Zasady wiki (źródła, syntezy, kontrola jakości): `shared/WIKI.md`.

Ingest do `legal/` prowadzi wyłącznie model, wykonując po jednej stronie PDF:
`wiki-basic-memory/modules/ingest-wiki` → `the-ocr-ingest-page` (Google Vision/Azure) → kontrola OCR i obrazu
→ ewentualnie ponowny odczyt Datalab/LlamaParse → zatwierdzenie strony.
Nie korzystaj z `wiki_ingest` (refresh, start, extract, index) ani
kolejki z dawnych bind mountów. Na serwerze Basic Memory nie ma już
`/dokumentacja`, a model tworzy źródła Markdown tylko po weryfikacji
całego PDF. Rozdziel dokumenty zawarte w jednym PDF na osobne notatki;
źródłowy tekst pozostaje bez modyfikacji i każdą stronę zaczyna
`==< plik.pdf (Page n/total_document_pages) >==`.

Binarne PDF nie trafiają do Basic Memory: model wysyła niezmieniony PDF
do prywatnego bucketu Cloudflare R2 (`the-ocr-archive`) i dopiero po
potwierdzeniu kopii zapisuje Markdown jako notatkę źródłową w `main`, folder `legal/dokumenty/`.
PDF trafia wyłącznie do R2, Markdown wyłącznie do Basic Memory.
Notatki wtórne tworzy lub aktualizuje osobno i łączy linkami do źródła.
`wiki_plan` pozostaje niezależnym narzędziem planowania, nie uruchamia OCR.

Niedostępność OCR, obrazów lub kopii źródła w R2 oznacza przerwany
ingest, nie status „zweryfikowany”. Wymagaj faktycznego zapisu
`bm_write` i kontroli przez `bm_read`.


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

## Zapis w `legal/` po każdym zakończonym etapie

- **Dokument:** przetwarzaj pojedynczo. Sprawdź istniejący wpis po identyfikatorze źródła i ścieżce.
  Zapisz tożsamość dokumentu, pełną transkrypcję w wiki, strony/segmenty, jakość odczytu i powiązania.
  Pełny tekst i wyciąg zapisuj według odczytanej metodyki ingestu; nie zastępuj źródła streszczeniem.
- **Ustalenie:** wskaż dokument i stronę/blok albo autora i datę relacji. Oddziel twierdzenie strony od ustalenia,
  zachowaj sprzeczności. Przebieg postępowania zapisuj w `legal/postepowania/`, nie tylko w recapach.
- **Teczka `legal/sprawy/<katalog>/`:** Stan, Terminy, Decyzje użytkownika, Lekcje, Pisma, Relacje.
- **Pismo `legal/sprawy/<katalog>/pisma/`:** wersja, ścieżka, runda, otwarte uwagi, pytania, wyniki kontroli i status.
- **Orzeczenie:** zweryfikowane źródło, sygnatura i relacja do sprawy; sprawdź `legal/orzeczenia/` przed kolejnym researchem.
- **Relacja pokrzywdzonego / świadka:** nie jest w Basic Memory. Relacja zdarzeń, log zeznań, rejestr pism i zgłoszenia
  są w repozytorium `elconcept/legal`, katalog `relacje/<autor-slug>/` (nie w katalogu sprawy ani w projekcie claude.ai).
  Szczegóły: skill `zawiadomienie-o-przestepstwie`, `references/relacje-repo.md`.

Nie kończ ingestu na „zgłoszeniu do ingestu”. Zakończenie oznacza zapis dokumentu, ustaleń i relacji oraz odczyt
potwierdzający. Gdy brakuje metodyki lub źródła, oznacz etap NIEZAKOŃCZONY i zapisz dokładnie zaległą czynność.

## Checkpoint sesji w `legal/sessions/`

Checkpoint pisz skillem `bm-checkpoint` (plugin `basic-memory-nas`): `type: session`, folder `legal/sessions/`,
format, sekcje i metadane według tego skilla (`agent`, `session_id` hosta, `status`). Każdy checkpoint to nowa
notatka; poprzednich nie nadpisuj. Checkpoint powstaje tylko w dwóch sytuacjach, jak w upstreamie Basic Memory:
po kompakcji kontekstu (brief `basic-memory-nas` zastępuje hook PreCompact) i na wyraźną prośbę użytkownika
(„checkpoint”, „podsumuj sesję”, „przekaż dalej”). Nie zapisuj checkpointu ani recapu po każdej odpowiedzi,
po etapie ani przed odpowiedzią końcową.

Treść: cel użytkownika; wykonane działania; decyzje i ich przyczyny; pliki/wyniki ze ścieżkami repozytorium;
kontrole faktycznie wykonane; nierozstrzygnięte kwestie; następny krok; odnośniki do notatek w `legal/`.
Checkpoint nie zastępuje zapisu ustaleń w `legal/sprawy/` ani ingestu. Istotną, trwałą decyzję autora
(nie każdą preferencję w rozmowie) zapisz osobno skillem `bm-decide` w `legal/decyzje/`; jedna notatka na decyzję.

## Trwałe ustalenia w `legal/bm-remember/` — tylko gdy naprawdę warto

Nie zapisuj tu przebiegu sesji. Gdy sesja ujawniła trwałą, istotną informację dla przyszłej pracy (potwierdzoną
preferencję autora, przyjętą zasadę, decyzję o długim horyzoncie), zapisz ją skillem `bm-remember`; najpierw
wyszukaj istniejącą notatkę i uzupełnij ją zamiast tworzyć kopię. Bez takiej informacji nie zapisuj niczego.
Nie przenoś całych podsumowań, logów, transkryptów ani sekretów.

## Potwierdzenie i awaria

Zapisy tylko przez MCP (`bm_write`, `bm_edit`). Przed zmianą istniejącej notatki odczytaj ją (`bm_read`) i przekaż
`expected_checksum`; stosuj dopisek lub zmianę sekcji, nie nadpisuj cudzych ustaleń. Przed ponowieniem niepewnego
zapisu sprawdź, czy już istnieje. Po zapisie wykonaj `bm_read` i sprawdź treść. Sukces to odczyt zgodny
z zamierzeniem, nie samo wywołanie. Po zapisie notatki ze schematem uruchom `bm_schema(command="validate", identifier=...)`.

Gdy zapis się nie udał, powiedz to wprost (`NIEZAPISANE` i przyczyna). Nie dopisuj do odpowiedzi rutynowego statusu pamięci.
Zaległość dopisz do `_PRZEBIEGI.md` pisma lub `_robocze/pamiec-zalegle.md` w folderze sprawy, z folderem,
identyfikatorem notatki i treścią do zapisu. Przy następnym wejściu ponów po sprawdzeniu duplikatów.
Można kontynuować pracę merytoryczną; nie deklaruj pełnego zakończenia ingestu ani skutecznego zapisu pamięci.

## Przenośność i hooki

Claude Code: brief na starcie sesji i polecenie checkpointu po kompakcji daje hook pluginu `basic-memory-nas`;
hook tego pluginu tylko odsyła do tego pliku. ChatGPT nie ma hooków: orientację i checkpoint wywołuje model
albo użytkownik (`@bm-orient`, `@bm-checkpoint`). **Wbudowana Memory ChatGPT nie może zostać przekierowana na MCP.**
Nie synchronizuj automatycznie całych rozmów ani sekretów.
