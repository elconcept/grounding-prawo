---
description: Zapisz transkrypcję sesji do doskonalenia skilli (prompty, odpowiedzi, skille, artefakty; bez reasoningu).
argument-hint: [krótki tytuł sesji]
---

Transkrypcja sesji: $ARGUMENTS

Zapisz plik `grounding-prawo/INBOX/$(date +%Y%m%d_%H%M)_transkrypcja_<sprawa>_<temat>.md` (repo `grounding-prawo` obok `legal`:
katalog repozytorium określ na podstawie bieżącego workspace albo jawnej ścieżki od użytkownika; nie zakładaj stałej lokalizacji na dysku. `INBOX/` pozostaje poza gitem).

Zawartość - wyłącznie:
1. Każdy prompt użytkownika dosłownie (`## Prompt użytkownika N`).
2. Odpowiedzi tekstowe modelu dosłownie (`### Odpowiedź modelu`).
3. Każde wywołanie skilla: nazwa i argumenty (`> **Skill #N:** \`nazwa\``).
4. Na końcu tabela: `# | skill | inicjator (model/użytkownik) | artefakt (ścieżka pliku)`, oraz zdanie, czy skill wejściowy
   `prawny-router-v3` został wywołany, i co zrobiono bez skilla.

Bez reasoningu modelu, bez wyników narzędzi, bez wstawek systemowych. Nie skracaj promptów ani odpowiedzi.
