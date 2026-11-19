# Pochodzenie skilli i architektura LEXMACHINA-CHAT

Ten dokument jest zapisem sposobu powstania **konkretnego wydania** `plugins/lexmachina-chat` w repozytorium `elconcept/grounding-prawo`. Oddziela kanon źródłowy, adaptację do hosta ChatGPT, składanie pakietu i kontrolę publikacji.

## 1. Łańcuch źródła

```text
elconcept/LexMachina
  └─ Wersja rozwojowa rozpakowana/
       ├─ SKILL.md, moduły, referencje, oryginalne widgety
       └─ wspólne reguły i mapy dziedzinowe
                    ↓ adaptacja do trybu CHAT (8 etapów)
Plugin Creator: osobisty plugin akta-i-dowody 1.0.0
  ├─ oryginalne treści źródłowe
  ├─ adaptery CHAT i profile wykonawcze
  └─ testy offline, walidacje i odczyt aktualnego release
                    ↓ wydanie dla osobnego marketplace
grounding-prawo/plugins/lexmachina-chat/
  ├─ 12 skilli, manifesty ChatGPT/Codex, SOURCE-RELEASE.json
  └─ część wspólnych zasobów z wygenerowanego drzewa
     plugins/grounding-prawo (bez jego zastępowania)
                    ↓ GitHub main, CI
elconcept/grounding-prawo → marketplace
```

**Upstream merytoryczny:** `elconcept/LexMachina`, `Wersja rozwojowa rozpakowana/`. Adaptacja nie jest samodzielnym projektem nowego routera: zachowuje macierz [1]–[11] skilla `prawny-router-v3`, rolę `prawo-polskie-v2` i kanoniczną bibliotekę `shared`.

**Etapy adaptacji:** osiem iteracji w trybie ChatGPT CHAT. W ostatnich etapach dostosowano raporty `raport-sytuacyjny-v2` i `raport-klienta-v1` oraz audyt `audyt-systemu-v4`. Przygotowano profile wykonawcze i `references/CHAT-RUNTIME.md` tam, gdzie zachodziła różnica między możliwościami oryginalnego hosta a ChatGPT. Pozostałe podstawowe skille obejmują analizę sądową, dowodową, umowy i chronologię.

**Źródło pakietu marketplace:** osobisty backend Plugin Creator (oryginalna nazwa `akta-i-dowody`), release `pluginrel_6afdb8ff27688191aa4ce96949c98dfa`, wersja `1.0.0`. To **źródło adaptacji**, a nie drugi identyfikator dystrybucyjny. Osobisty plugin oraz instalacja pakietu z GitHuba są rozdzielne.

**Sposób złożenia:** przystosowane `SKILL.md` i adaptery CHAT pochodzą z release Plugin Creator; część wspólnych i niezmienianych zasobów pomocniczych odziedziczono z katalogu `plugins/grounding-prawo/skills`, wcześniej generowanego ze źródeł LexMachina, MateMatic i skilli autorskich. Dwa skille raportowe zmaterializowano z wydania Plugin Creator. W miejscach, w których dołączono `SKILL.upstream.md` lub `SOURCE-SHA256.json`, zachowano dodatkowy ślad oryginału.

**Uczciwa granica integralności:** historyczne testy potwierdzały zgodność i zachowanie źródeł dla konkretnych etapów. Nie wykazano jednak bajtowej identyczności *wszystkich* wspólnych plików pakietu GitHub i pełnego archiwum backendowego. Nie należy prezentować takiej zgodności jako dowiedzionej. Z `lexmachina-chat` usunięto przykładowe serwery Node/MCP (w tym historyczne `mcp-servers/` oraz rootowy `.mcp.json`), które nie należały do docelowego wydania ChatGPT CHAT.

## 2. Który katalog za co odpowiada?

Mapa **całego repozytorium** `grounding-prawo`:

| Katalog | Znaczenie i sposób utrzymania |
|---|---|
| `plugins/lexmachina-chat/` | **Osobna dystrybucja CHAT**; 12 skilli, dwa manifesty, dokumentacja pochodzenia. Nie jest wyjściem `scripts/build.py` |
| `plugins/grounding-prawo/` | **Wygenerowana** dystrybucja Claude/Codex; wynik `scripts/build.py`. Nie edytować ręcznie |
| `selection/selection.yaml` | Lista skilli, pochodzenie `lex`/`awe`/`own`/`vendor`, zasady `merge_into` / `fold_into` dla drugiego pluginu |
| `selection/patches/` | Patche na **kopię** przypiętego upstreamu, nie na `vendor/` |
| `selection/overlay/` | Własne zasoby nakładane przez generator `grounding-prawo` |
| `selection/mcp.json` | Opcjonalna konfiguracja portalu MCP drugiego pluginu |
| `own-skills/` | Autorskie skille i moduły używane przez generator |
| `vendor/packs/LexMachina/` | Przypięty submoduł źródłowej LexMachina |
| `vendor/packs/awesome-matematic-skills/` | Zewnętrzne skille MateMatic dla generatora |
| `vendor/docs/`, `vendor/general/` | Materiały i narzędzia ogólne |
| `vendor/law/`, `vendor/law-git/` | Materiały prawne i historia kodeksów, nie źródło automatycznie aktualnego prawa |
| `vendor/mcp/` | Źródła niezależnych serwerów MCP |
| `scripts/build.py` | Składa **tylko** `plugins/grounding-prawo` i aktualizuje jego wpisy marketplace |
| `scripts/validate_chat_plugin.py` | Statyczna kontrola dedykowanego pakietu CHAT |
| `scripts/validate_marketplace.py`, `scripts/lint_refs.py` | Walidacja całego marketplace i referencji generowanej dystrybucji |
| `.agents/plugins/marketplace.json` | Dwie pozycje dla ekosystemu Codex: `grounding-prawo`, `lexmachina-chat` |
| `.claude-plugin/marketplace.json` | Niezmieniony, osobny wpis Claude: `grounding-prawo` |
| `.github/workflows/` | Niezależny test CHAT i pełny pipeline generowanego pluginu |
| `archive/` | Archiwum wcześniejszych wariantów i wyłączonych patchy |
| `docs/`, `_log/`, `tests/` | Dokumentacja operacyjna, raporty i testy |
| `deploy/` | Materiały wdrożeniowe infrastruktury MCP, nie część CHAT |

**Istotne rozróżnienie:** `plugins/lexmachina-chat/` i `plugins/grounding-prawo/` są **dwoma pakietami**, a nie kopią 1:1. Obydwa występują w tym samym repo/marketplace, lecz mają inne zasady generowania, zakres skilli i wymagania integracyjne. Zmiana jednego nie powinna nadpisywać drugiego.

## 3. Nazwy i manifesty

- **LEXMACHINA-CHAT** — prezentowana nazwa w `plugin.json` i `.codex-plugin/plugin.json`.
- `lexmachina-chat` — niezmienny, małoliterowy techniczny `name` w obu manifestach, wpisie marketplace, nazwie katalogu i skryptach walidujących.
- `chat-router-akta-i-dowody` — historyczny identyfikator skilla adaptera. Pozostawiono go dla kompatybilności; jego nazwa nie wyznacza marki całego pluginu.
- `akta-i-dowody` — nazwa osobistego pluginu źródłowego w Plugin Creator. Nie oznacza, że jego instalacja automatycznie zmienia się po commicie GitHub.

## 4. Zasady adaptacji i testów

1. **Kanon:** aktualne źródła w `LexMachina` i archiwum release Plugin Creator; nie rekonstruować brakujących fragmentów z pamięci modelu.
2. **Zachowanie semantyki:** oryginalny router [1]–[11], mapy, moduły i metodologie nie są zastępowane prostszymi algorytmami CHAT.
3. **Portabilność:** instrukcje `view`, `show_widget`, shell, CI, serwery MCP i mechanizmy magazynowania nie oznaczają wykonania operacji w ChatGPT. Własne adaptery umożliwiają tylko działania obsługiwane przez bieżącego hosta.
4. **Minimalny zestaw:** pakiet zawiera 12 skilli, bez obowiązkowego serwera MCP i bez automatycznej migracji wszystkich dziedzin DR; pozostałe bundle są odrębnymi pracami.
5. **Testy źródła:** `python3 scripts/validate_chat_plugin.py` bada 12 skilli, manifesty, adaptery, widgety i zakaz zależności od rootowego MCP.
6. **Testy marketplace:** `python3 scripts/validate_marketplace.py` pilnuje obecności obu wpisów Codex i braku zmian wpisu Claude; `build-plugin` dodatkowo odtwarza generowaną dystrybucję.
7. **Wydanie:** praca wyłącznie na `main`, commit + push. Potwierdzić rzeczywisty odczyt ze zdalnego GitHuba i wynik dwóch workflow. Jeżeli potrzebny gitlink w `elconcept/legal`, zaktualizować osobnym commitem w prywatnym repo.

### Czego testy nie potwierdzają

**Static QA** i zielony GitHub Actions nie stanowią dowodu pełnej aktywacji każdego skilla w ChatGPT, zgodności interaktywnych widgetów, logowania do MCP, działania z prawdziwymi aktami ani automatycznej synchronizacji wtyczki do konta. Takie wyniki należy osobno oznaczać `LIVE_E2E_NOT_CHECKED`, dopóki nie zostaną rzeczywiście wykonane.

## 5. Punkty kontrolne

- [Lista plików i release źródłowego](SOURCE-RELEASE.json)
- [README i zawartość pakietu](README.md)
- [Walidacja pakietu CHAT](https://github.com/elconcept/grounding-prawo/actions/workflows/validate-chat-plugin.yml)
- [Pełny build marketplace](https://github.com/elconcept/grounding-prawo/actions/workflows/build-plugin.yml)
- [Instrukcje pracy nad repo](../../AGENTS.md)

Dokument opisuje **pochodzenie kodu i ograniczenia testów**, nie dokumenty konkretnych spraw prawnych. Prywatne materiały pozostają poza publicznym marketplace.
