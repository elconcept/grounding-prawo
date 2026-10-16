# 0.3.0 — dokumenty, routing i pamięć

- Jeden skill odczyt-dokumentow: narzędzie the-ocr, biblioteka kontraktu, PDF tekstowy przez PyMuPDF,
  MarkItDown dla formatów biurowych/HTML, manifest jakości i duplikatów. Oryginały nie są modyfikowane.
- Wybrane --provider datalab / azure-di / google-vision bez wymuszonego przejścia przez Datalab.
- Brak Tesseract/LiteParse/local OCR w nowej ścieżce. Kontrakt zachowuje null dla nieznanej confidence/bbox.
- Prowadnik scalony z routerem; protokół main/legal jest odczytywany również przy bezpośrednim wywołaniu skilla.
- Preflight źródeł przed usunięciem poprzedniego wyniku; walidator wykrywa brak źródła przy istniejącym buildzie.
- Zewnętrzne skille projektowe w .agents/skills, wskazywane z .claude/skills i .opencode/skills.

Weryfikacja: 10 testów pytest; 36 testów citation-grounding; build, validate_marketplace, lint_refs,
walidatory sześciu skilli, Claude plugin validate (ostrzeżenie o braku version jest zamierzone).
Google Vision: udany test na żywo z syntetycznym jednokartkowym dokumentem; Datalab i Azure: adaptery
sprawdzone na reprezentatywnych odpowiedziach, bez testów na żywo (brak konfiguracji w tej sesji).

Rozważono docOCR (https://github.com/riddleling/docOCR): Swift/Vapor i Apple Vision, macOS 26+.
Wybrano wspólną funkcję read_documents z CLI, dostępną do późniejszego wystawienia przez MCP.
Nie uruchomiono nowego serwera ani nie dodano nieistniejącego endpointu do portalu.

Skille nie zapewniają technicznej gwarancji zapisu przy nagłym zamknięciu hosta. Checkpointy i potwierdzenia
MCP obowiązują w instrukcjach; hook Claude w repo legal dodatkowo kontroluje projekt i odczyt zapisu.
Synchronizacja ChatGPT Desktop Work wymaga potwierdzenia w nowej sesji właściwego hosta.
