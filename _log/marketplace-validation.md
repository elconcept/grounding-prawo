# Walidacja marketplace grounding-prawo

## Naprawa 0.1.1 (2026-10-15)

W wersji 0.1.0 walidator pluginów OpenAI odrzucał paczkę:

- 17 skilli miało `disable-model-invocation: true`, w tym zależności routera.
- 24 pliki `agents/openai.yaml` zawierały niedozwolone `policy.products`.
- Manifest OpenAI nie zawierał wymaganych pól interfejsu.
- `doc-intel-contract-pl` miał opis długości 1068 znaków, powyżej limitu 1024.
- W katalogach skilli znajdowały się manifesty osobnych pluginów upstreamu.

Generator normalizuje frontmatter do przenośnego formatu, przenosząc adnotacje
upstreamu do `metadata` (wartości tekstowe, struktury jako JSON). Nie usuwa treści
procedur. Kontrola zależności odbywa się przed normalizacją. Moduły `internal`
pozostają dostępne dla modelu. Manifest OpenAI jawnie wskazuje `.mcp.json`.

## Kontrola przed publikacją

```bash
python3 -I scripts/build.py
python3 -I scripts/validate_marketplace.py
node plugins/grounding-prawo/skills/citation-grounding-pl/scripts/test-grounding.mjs
claude plugin validate .
claude plugin validate plugins/grounding-prawo
```

Workflow `build-plugin.yml` uruchamia walidację paczki przed publikacją wyniku.
Walidacja obejmuje oba katalogi marketplace, manifesty pluginu, cały zestaw skilli
z selekcji, nazwy, opisy, frontmatter, polityki agentów, zależności i ikony.

## Dowody i granice testów

W środowisku naprawy:

- 59/59 skilli przeszło `skill-creator/scripts/quick_validate.py`.
- Paczka przeszła `plugin-creator/scripts/validate_plugin.py`.
- Testy cytowań: 36/36.
- Czyste profile Claude Code i Codex zainstalowały plugin 0.1.1.
- Codex app-server `skills/list` zwrócił 59 skilli pluginu, wszystkie `enabled`,
  z pustą listą błędów ładowania.
- Porównanie z 0.1.0 potwierdziło identyczną treść wszystkich 59 procedur
  poniżej frontmatter. Zmiany dotyczą opakowania i metadanych.

**Nie jest to dowód synchronizacji konta Claude/Cowork ani aktywacji w ChatGPT.**
Te operacje wykonują usługi zdalne z uprawnieniami konta. Przeglądarka dostępna
podczas naprawy zatrzymała się na weryfikacji Cloudflare przed claude.ai.
Wyszukiwarka pluginów dostępna w sesji nie zwróciła tego prywatnego marketplace.
Nie wolno przedstawiać sukcesu instalacji CLI jako sukcesu synchronizacji konta.

Do pełnego potwierdzenia potrzebne są: wynik zdalnej synchronizacji tego commita,
wersja 0.1.1 w katalogu konta oraz odczyt i użycie skilla w nowej rozmowie.
W przypadku błędu Claude istotny jest szczegół `failed_content`/`plugins[].error`
z odpowiedzi synchronizacji lub logu aplikacji, a nie tylko komunikat ogólny.
Nie należy zmieniać widoczności prywatnego repozytorium, by ominąć błąd.

## Dokumentacja formatów

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/build/plugins
