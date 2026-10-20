# WIKI — ingest wyłącznie PDF przez model

Nie uruchamiaj kolejek ani `wiki_ingest refresh/index` na dawnych mountach. Każdy nowy dokument źródłowy wymaga kontroli OCR strona po stronie przez LLM, powtórnego odczytu podejrzanych stron, potwierdzenia kopii oryginału PDF w Cloudflare R2 oraz odczytowego potwierdzenia zapisu pełnego Markdown w Basic Memory. Szczegóły: `wiki-basic-memory/modules/ingest-wiki`.

# Wiki oparta na źródłach w Basic Memory

Model Karpathy LLM Wiki: oryginały, opracowane notatki i nawigacja tworzą odrębne
warstwy. Projekt `legal` przechowuje źródła i wiedzę spraw, `main` — recapy sesji.
Pełna transkrypcja dokumentu pozostaje oddzielona od ustaleń, komentarzy i syntez.
PDF rozstrzyga zgodność transkrypcji: wykonaj kontrolę stron według `wiki-basic-memory/modules/ingest-wiki`.

## Ingest: rozpoznaj wpływ przed zapisem

1. Odczytaj metodologię projektu. Wyszukaj po sygnaturze, osobie, dacie i temacie;
   odczytaj pasujące notatki. Wynik wyszukiwania służy do wyboru, nie zastępuje lektury.
2. Ustal listę: notatki do aktualizacji, nowe notatki, sprzeczności. Porównuj tezy
   z dokumentami pierwotnymi, nie tylko z wcześniejszymi streszczeniami.
3. Aktualizuj właściwe sekcje istniejących notatek. Nowa notatka tematyczna musi
   wskazywać źródło i stronę/blok oraz mieć odnośnik z teczki albo istniejącego tematu.
4. Sprzeczność zapisz wraz z obydwoma źródłami, datami i zakresem rozbieżności.
   Rozróżniaj zmianę stanu faktycznego, wersję strony i błąd odczytu. Nie wybieraj
   jednej wersji bez podstaw. Nowa relacja grafu wymaga oparcia w treści dokumentu.
5. Po zatwierdzeniu przez LLM wszystkich stron PDF i potwierdzeniu kopii PDF w R2 zapisz źródło Markdown oraz notatki wtórne; recap wymienia zmienione
   notatki, sprzeczności i zaległości. Zabroniony jest automatyczny batch ingest oraz skan folderów.

## Pytanie i synteza

Zacznij od teczki i wyszukiwania istniejących notatek w `legal/dokumenty`; uzupełnij nawigację
przez `search_notes` i `build_context`. Czytaj tylko trafne notatki i ich istotne
powiązania. Dla tezy prawnej lub faktycznej wróć do dokumentu pierwotnego i konkretnej
strony/bloku; aktualne prawo sprawdź odpowiednim MCP. Relacja grafu pomaga znaleźć
materiał, ale sama nie dowodzi tezy. Brak wyników nazwij luką, nie dowodem nieistnienia.

Nowe porównanie lub ustalenie łączące kilka dokumentów zapisz jako syntezę według
metodologii projektu. Zapisz pytanie, datę, źródła, wnioski, sprzeczności i niepewności.
Najpierw sprawdź, czy podobna synteza istnieje; aktualizuj ją zamiast tworzyć duplikat.
Połącz syntezę z teczką/tematem. Proste odszukanie faktu pozostaje w odpowiedzi i recapie.

## Kontrola jakości

Uruchom na żądanie albo po zakończeniu partii ingestu. Sprawdź zmienione notatki
oraz wskazujące na nie teczki i tematy. Rozdziel:

- struktura: niedziałające odnośniki, brak źródła lub strony, duplikaty osób/tematów,
  nowe notatki bez odnośnika z teczki, nieaktualny indeks;
- treść: sprzeczności, dopiski w transkrypcji nieobecne w oryginale, wnioski
  pozbawione podstaw, nieaktualne syntezy po zmianie źródła, brakujące strony.

Raport podaje zakres (notatki i dokumenty), problem, źródło i poprawkę. Kontrola
wybranych notatek nie jest audytem całej bazy. Poprawiaj oczywiste błędy w ramach
zleconej pracy; zachowaj odmienne wersje faktów i historię źródeł. Scalanie/usuwanie
notatek wymaga jawnego zlecenia oraz aktualizacji wszystkich znanych odnośników.
Przy dużej notatce wydziel spójny podtemat z zachowaniem źródeł i nawigacji.

Inspiracja: Praney Behl, llm-wiki-plugin (MIT): ingest-workflow, query-workflow,
lint-workflow. Adaptacja używa istniejącego grafu i wyszukiwania Basic Memory;
nie wymaga lokalnych skryptów, dodatkowego modelu ani terminala klienta.
