# LEXMACHINA-CHAT

**LexMachina w trybie ChatGPT CHAT:** 12 współpracujących skilli do analizy akt, dowodów, chronologii, umów, raportowania i audytu. Osobny pakiet w marketplace [Grounding Prawo](https://github.com/elconcept/grounding-prawo), niezależny od istniejącego pluginu Claude.

[![CHAT validation](https://github.com/elconcept/grounding-prawo/actions/workflows/validate-chat-plugin.yml/badge.svg?branch=main)](https://github.com/elconcept/grounding-prawo/actions/workflows/validate-chat-plugin.yml)
[![Marketplace build](https://github.com/elconcept/grounding-prawo/actions/workflows/build-plugin.yml/badge.svg?branch=main)](https://github.com/elconcept/grounding-prawo/actions/workflows/build-plugin.yml)

| Wydanie | Zawartość | Integracje |
|---|---|---|
| **1.0.1** | **12 skilli** | MCP, Basic Memory i lokalna powłoka **nie są warunkiem startu** |

## Jak działa

Zadanie trafia do `chat-router-akta-i-dowody`, który kieruje je do **oryginalnego** `prawny-router-v3`. Pozostaje jedna macierz kwalifikacyjna [1]–[11]; adapter CHAT nie buduje konkurencyjnego routera. Następnie uruchamiany jest właściwy skill oraz potrzebne mu pliki `references/`, `modules/` i `shared/`.

Skille rozdzielają trzy role: analizę merytoryczną, przygotowanie raportów oraz kontrolę systemu. Cytowane przepisy i orzeczenia wymagają rzeczywistej weryfikacji. Sam zapis w dokumencie urzędowym nie jest automatycznym potwierdzeniem prawdziwości zawartej w nim relacji. Niewykonane sprawdzenia są oznaczane jako `NOT_CHECKED` / `NOT_RUN`.

## Skille w pakiecie

| Obszar | Skill | Zastosowanie |
|---|---|---|
| Wejście CHAT | `chat-router-akta-i-dowody` | Adapter wejścia; nie zastępuje routera źródłowego |
| Routing | `prawny-router-v3` | Pierwotny podział na 11 kategorii |
| Domeny prawa | `prawo-polskie-v2` | Fasada dziedzin i mapa DR |
| Prowadzenie | `przewodnik-prawny-v2` | Gospodarz sesji i fallback |
| Reguły wspólne | `shared` | Wspólny kanon i kontrole |
| Analiza akt | `analiza-sadowa-v6` | Wieloprzebiegowa analiza sprawy |
| Ocena materiału | `analizator-dowodow-v3` | Sprzeczności, pochodzenie i siła dowodów |
| Umowy | `analizator-umow-v1` | Analiza, redakcja i negocjowanie umów |
| Oś zdarzeń | `chronologia-sprawy-v1` | Chronologia zdarzeń i rozbieżności |
| Stan sprawy | `raport-sytuacyjny-v2` | Raport sytuacyjny po analizie lub na żądanie |
| Raport zewnętrzny | `raport-klienta-v1` | Raport IND/BIZ, zmiany i ryzyka |
| Kontrola biblioteki | `audyt-systemu-v4` | Audyt struktury, odwołań i reguł |

To **wybrany rdzeń**, nie cała LexMachina, nie komplet wszystkich modułów DR i nie zapowiedź automatycznej dostępności dowolnego innego skilla.

## Instalacja i nazwa

Nazwa prezentowana użytkownikowi to **LEXMACHINA-CHAT**. Techniczny identyfikator `lexmachina-chat` pozostaje małymi literami ze względu na konwencję identyfikatorów, ścieżki Git i kompatybilność marketplace.

- **Repozytorium:** `elconcept/grounding-prawo`, gałąź `main`.
- **Pozycja marketplace:** `.agents/plugins/marketplace.json` → `plugins/lexmachina-chat`.
- **Manifesty pakietu:** `plugin.json` i `.codex-plugin/plugin.json`.
- **Claude:** odrębny wpis `grounding-prawo` w `.claude-plugin/marketplace.json`, bez zastępowania go przez CHAT.

W klientach obsługujących GitHub marketplace wybierz pozycję **LEXMACHINA-CHAT** ze źródła `elconcept/grounding-prawo`. Samo wypchnięcie plików na GitHub **nie instaluje** wtyczki w koncie ChatGPT i nie potwierdza jej publicznego wpisu w katalogu ChatGPT. Osobisty plugin źródłowy w Plugin Creator pozostaje odrębnym obiektem.

## Skąd pochodzą skille?

Źródłem merytorycznym jest projekt `elconcept/LexMachina`. Jego skille były adaptowane w **ośmiu etapach** do trybu ChatGPT CHAT i testowane jako osobisty plugin `akta-i-dowody`, wydanie **1.0.0**. Wariant marketplace składa tę adaptację z zachowanymi zasobami wspólnymi i plikami odziedziczonymi z generatora `grounding-prawo`. W pakiecie zachowano źródłowe treści i dołożono warstwę obsługi funkcji hosta tam, gdzie była potrzebna.

Przebieg migracji, źródła, ograniczenia porównania plików oraz mapa katalogów repozytorium są udokumentowane w **[PROVENANCE.md](PROVENANCE.md)**. Identyfikatory wydania i pełna lista skilli znajdują się w **[SOURCE-RELEASE.json](SOURCE-RELEASE.json)**.

## Struktura pakietu

`plugins/lexmachina-chat/`

| Plik lub katalog | Rola |
|---|---|
| `plugin.json` | Manifest pluginu ChatGPT/Agent Plugins |
| `.codex-plugin/plugin.json` | Manifest zgodności Codex |
| `SOURCE-RELEASE.json` | Maszynowy zapis źródła wersji 1.0.0 |
| `PROVENANCE.md` | Powstanie skilli, ograniczenia, mapa repo |
| `skills/<nazwa>/SKILL.md` | Instrukcje 12 skilli |
| `skills/<nazwa>/references/` | Reguły, adaptery CHAT, źródła pomocnicze |
| `skills/<nazwa>/modules/` | Moduły dziedzinowe, tam gdzie występują |
| `skills/<nazwa>/assets/` | Oryginalne statyczne widgety i inne zasoby |

W odróżnieniu od `plugins/grounding-prawo/` ten katalog **nie jest generowany przez `scripts/build.py`**. Zmiany w jego adaptacjach i dokumentacji należy kontrolować osobno, bez nadpisywania drugiego pluginu.

## Kontrole jakości

Z katalogu głównego repozytorium:

```bash
python3 scripts/validate_chat_plugin.py
python3 scripts/validate_marketplace.py
python3 -I scripts/build.py
python3 -I scripts/lint_refs.py
```

- `validate-lexmachina-chat` sprawdza komplet 12 skilli, metadane, adaptery, struktury i brak obowiązkowego rootowego MCP.
- `build-plugin` odtwarza **oddzielny** plugin `grounding-prawo`, sprawdza kompatybilność marketplace i testy oraz zgodność wygenerowanych plików z repozytorium.
- Statyczny **PASS** nie oznacza pełnego E2E w interfejsie ChatGPT: aktywacja skilli, wyświetlanie widgetów i wyszukiwanie źródeł wymagają oddzielnego sprawdzenia.

**Zmiany wydania:** tylko `main`; bez branchy, worktree i PR. Commit i push po testach. Nie dodawać do publicznego repozytorium prywatnych akt, danych spraw ani sekretów.

---

[Repozytorium](https://github.com/elconcept/grounding-prawo) · [Przebieg walidacji CHAT](https://github.com/elconcept/grounding-prawo/actions/workflows/validate-chat-plugin.yml) · [Pochodzenie i architektura](PROVENANCE.md)
