# CHAT-RUNTIME — raport-sytuacyjny-v2 v2.13 / plugin 0.8.0

## Routing i wyzwalacze
- Tryb A: finalny raport po przejściu wszystkich właściwych kroków analizy konkretnej sprawy. Nie przerywaj analizy ani nie zastępuj raportem pisma.
- Tryb B: po nowym materiale najpierw przeanalizuj materiał; na końcu **tylko zaproponuj** raport. Milczenie nie jest zgodą na widget.
- Tryb C: żądanie „raport sytuacyjny”, „stan sprawy”, „co ustaliliśmy” itp. uruchamia raport od razu, bez resetu historii znanych danych.
- To jest postprocesor oryginalnego `prawny-router-v3` (kategorie [1]–[11] oraz PRIMARY/SECONDARY/FALLBACK pozostają nienaruszone); `prawo-polskie-v2` nadal dobiera dziedzinę DR.

## Niezmienny model raportu
Zbuduj schemat `BLUEPRINT JSON` z oryginału, włącznie z `chronologia[]`, `sources[]`, `dowody[]`, `risk_map[]`, `conflicts[]`, `procedural_recommendations[]`, `priorytetyAspektow` i `historiaStrategii`. Zachowaj 7 zakładek / sekcji w kolejności: Sprawa; Chronologia; Źródła; Ryzyka; Luki i sprzeczności; Rekomendacje; Historia strategii. Zwaliduj pola obowiązkowe, status GOTOWY/CZĘŚCIOWY/ROBOCZY, zgodność danych między sekcjami i bramki prawne.

* W przypadku `null` nie zakładaj wartości 0. Bez podstaw źródłowych niedopuszczalne są arbitralne `p1pct`, `p2pct`, `confidence` czy numeryczne `poziomPewnosciRaportu`; pozostaw `null` i opisz ograniczenia. Nie zmieniaj istniejącego kontraktu pól; nieznaną wartość przedstawiaj jako `null` zgodnie z regułą źródła.
* Factual A–E to oś **rodzaju materiału i konfliktu**, a nie hierarchia prawdziwości. Przy dokumentach odróżnij dowód wpisu od dowodu zdarzenia opisanego w wpisie; osobno oceniaj niezależne bezpośrednie relacje i nagrania. Ten sam próg krytycyzmu stosuj wobec twierdzeń obu stron. Zdania użytkownika opisujące bezpośrednio przeżycia traktuj jako podane fakty sprawy, bez fikcyjnego obciążania obowiązkiem powtarzania dowodów.
* Legal source status (`VERIFIED`, `OFFICIAL_ANCHOR`, `NOT_CHECKED`) jest drugą niezależną osią. Cytat ustawowy, przepis, termin, sygnatura lub skutek prawny — tylko po odpowiednim rzeczywistym sprawdzeniu albo jawnie `NOT_CHECKED`. Nigdy nie deklaruj kontroli `JUR:*` tylko z uwagi na referencję w historycznym źródle.

## Rendering w ChatGPT CHAT
1. Preferuj faktycznie dostępne natywne elementy interaktywne, gdy w danej odpowiedzi mają dostęp do pełnego modelu danych. Zachowany oryginalny widget HTML (`../assets/widget-raport-sytuacyjny.html`) to szablon wyłącznie dla hosta wspierającego rzeczywiste pokazanie pliku z blueprintem; nie wklejaj nieufnych danych do kodu i nie udawaj mechanizmu `show_widget`.
2. Gdy nie ma pełnego renderera, zwróć rzetelny raport z siedmioma nagłówkami; nie nazywaj go interaktywnym. Nie deklaruj przycisków `sendPrompt`, edycji inline, importu JSON, zapisu historii, PDF, exportu ani undo/redo, chyba że host rzeczywiście je zapewnił.
3. Jeśli żądane są gotowe PDF/DOCX/JSON, utwórz je wyłącznie gdy rzeczywiście działa odpowiedni generator; inaczej dostarcz pełny tekst/JSON do skopiowania i oznacz stan `NOT_CREATED`.
4. Przy brakach: `ROBOCZY` lub `CZĘŚCIOWY`, ale bez zatrzymywania części wykonalnej. Użytkownik może skorygować dane; korekty aplikuj jawnie, nie zmyślaj automatycznego odświeżenia snapshotu.

## Obsługa zależności
`shared` to sibling `skills/shared`. Wczytaj tylko niezbędne pliki (np. `PRAWO-HARDGATE.md`, `SELF-CHECK-ANTY-FASADA.md`, `HYBRID-VALIDATION.md`, `MOD-PRIORYTETY-ASPEKTOW.md`), jeżeli istnieją i są dostępne w tej sesji. Źródłowe `JUR:weryfikacja-przepisow-kanon`, `JUR:liczenie-terminow`, `JUR:tryby-procesowe`, `JUR:prekluzja-dowodowa` i `JUR:umowy-shared-orzecznictwo-umow` są historycznymi aliasami. Nie zamieniaj ich fikcyjnym wywołaniem; korzystaj z faktycznie odczytanych kanonicznych źródeł odpowiedniej funkcji lub oznacz `NOT_AVAILABLE`. Podobnie pierwotny `show_widget(data=...)` nie jest natywnym wywołaniem ChatGPT.

## Końcowe QA
Zapisz statusy `INPUT_READ`, `SOURCES_VERIFIED`/`NOT_CHECKED`, `BLUEPRINT_VALIDATED`/`PARTIAL`, `RUNTIME_RENDERED`/`TEXT_FALLBACK`, `ARTIFACT_CREATED`/`NOT_CREATED`, `HISTORY_READ`/`NO_HISTORY`; odróżniaj test statyczny pakietu od E2E rzeczywistej sprawy.
