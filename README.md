# grounding-prawo

Prywatny marketplace z jednym pluginem do praktyki prawa polskiego (Claude Desktop, Cowork, Code; ChatGPT/Codex). Łączy silnik
Lex Machina, skille weryfikacji MateMatic, skille własne i wiedzę z pluginu IURA; zasada: **źródłem tezy o przepisie lub orzeczeniu
jest narzędzie MCP albo dokument, nigdy pamięć modelu.**

To repo służy do rozwijania pluginu. **Jak pracować ze skillami nad sprawą** (ścieżki A-E, katalog skilli, konektory MCP, kolizje,
komendy): `legal/PRZEWODNIK.md` i `legal/AGENTS.md` w katalogu spraw. Wejście do pracy prawnej: `prawny-router-v3`. Reguły, które model dostaje razem z pluginem:
`plugins/grounding-prawo/skills/shared/ZASADY-PLUGINU.md`, `ARTEFAKTY-SPRAWY.md`, `FORMAT-PISMA.md`.

Plugin jest **generowany** - nie edytuj `plugins/grounding-prawo/` ręcznie (sekcja [Utrzymanie](#utrzymanie)); zasady pracy nad repo: `AGENTS.md`.

## 1. Instalacja

Repozytorium jest prywatnym marketplace z jednym pluginem (`grounding-prawo`). Wersja semver (tylko manifest Codex): `selection/selection.yaml`.

| Klient | Jak |
|---|---|
| **Claude Code** | `claude plugin marketplace add elconcept/grounding-prawo`, potem `claude plugin install grounding-prawo@grounding-prawo` |
| **Claude Desktop / Cowork** | Ustawienia organizacji → Plugins → dodaj marketplace z GitHub (repo `elconcept/grounding-prawo`; repo prywatne, więc wymaga autoryzacji GitHub). Po synchronizacji plugin pojawia się w katalogu konta. Wymaga uprawnień zarządzania pluginami. |
| **ChatGPT / Codex** | `codex plugin marketplace add elconcept/grounding-prawo --ref main --sparse .agents/plugins --sparse plugins/grounding-prawo`, potem `codex plugin add grounding-prawo@grounding-prawo`. Aplikacja ChatGPT korzysta z tego samego manifestu `.codex-plugin`. |

Po instalacji sprawdź w **nowej rozmowie**: „Użyj prawny-router-v3 i powiedz, co potrafi plugin”. Skille z błędem
ładowania nie pojawią się na liście.

Konektory prawnicze ładuje `.mcp.json` pluginu: jeden serwer `lex` → `https://lex.xlap.pl/mcp` (portal Cloudflare z
logowaniem OAuth). Przy pierwszym użyciu host poprosi o autoryzację. Bez niej skille działają, ale nie mogą podawać
przepisów ani sygnatur (zob. [10. Problemy](#10-rozwiązywanie-problemów)).

Pełna lista kontroli instalacji i granice testów: `_log/marketplace-validation.md`. Test CLI nie dowodzi synchronizacji konta
Claude/Cowork ani aktywacji w ChatGPT - to potwierdza dopiero odczyt skilla w nowej rozmowie.

### Aktualizacje

- Manifest pluginu nie ma pola `version`, więc każda zmiana na `main` to nowa wersja (SHA commita).
- Claude Desktop / Cowork (marketplace w claude.ai): aktualizacja automatyczna; nowa wersja działa w nowej rozmowie.
- Claude Code z marketplace GitHub: auto-update jest domyślnie **wyłączony** dla marketplace spoza Anthropic. Włącz: `/plugin` →
  Marketplaces → grounding-prawo → Enable auto-update, albo `"autoUpdate": true` przy `grounding-prawo` w `extraKnownMarketplaces`
  (`~/.claude/settings.json`). Ręcznie: `claude plugin update grounding-prawo@grounding-prawo`.

---

## Utrzymanie

```bash
python3 -I scripts/build.py              # generuje plugins/grounding-prawo z selekcji
python3 -I scripts/validate_marketplace.py
python3 -I scripts/lint_refs.py          # martwe odwołania do skilli i plików
node plugins/grounding-prawo/skills/citation-grounding-pl/scripts/test-grounding.mjs
claude plugin validate plugins/grounding-prawo
```

| Co zmienić | Gdzie |
|---|---|
| lista skilli, wersja | `selection/selection.yaml` |
| przepływ i mosty między skillami | `selection/bridges.yaml` |
| skill własny, typ pisma | `own-skills/<nazwa>/` (+ wpis `fold_into` w selekcji dla typów pism) |
| plik dopisany do pluginu (np. `shared/ARTEFAKTY-SPRAWY.md`) | `selection/overlay/` |
| zmiana skilla z upstreamu | `selection/patches/NN-*.patch` (nigdy w `vendor/`) |
| reguła generująca (np. oznaczanie odwołań) | `scripts/build.py` |

Historia selekcji: `_log/selekcja.md`, `_log/skill-triage.md`, `_log/source-map.md`.

## Odczyt dokumentów i pamięć

Jedyny punkt wyboru ścieżki: `prawny-router-v3`. Mapa celów dawnego prowadnika jest jego referencją
`shared/SCIEZKI-PRACY.md`. Dokumenty obsługuje `odczyt-dokumentow`: konwersja do Markdown,
kontrakt JSON, duplikaty i raport jakości. `the-ocr` (repo `elconcept/the-ocr`, submoduł `vendor/docs/the-ocr`) jest
kopiowany przez `build.py` do skilla jako `tools/the-ocr` (sam kod i README, bez `.env`/`.secrets`).
Datalab, Azure DI i Google Vision kończą się wspólnym kontraktem; lokalne silniki OCR nie są dołączane.
PDF z tekstem odczytuje PyMuPDF, formaty biurowe i HTML — MarkItDown. Nieobsługiwane formaty zgłaszają błąd.

Basic Memory: recap każdej sesji/etapu do `main`, dokumenty i ustalenia do `legal`. Każdy skill
wczytuje protokół przed pracą i wymaga potwierdzenia zapisu. Instrukcje nie zastępują hooków hosta;
przerwanie aplikacji nadal może przerwać bieżący zapis. Aktualizacja pluginu wymaga nowej sesji.

`own-skills` oznacza źródła utrzymywane lokalnie (także adaptacje i scalenia), `vendor` — przypięty upstream,
`plugins` — wynik budowania. Typy pism z `fold_into` są modułami, nie dodatkowymi skillami do wyboru.

## Skille do rozwijania tego repo

W `.agents/skills/`: OpenAI `skill-creator`, `plugin-creator`; Anthropic `plugin-structure`,
`skill-development`, `mcp-integration`; enhance-workflows `feature-factory`,
`peer-agent-collaboration`, `whitepaper-audit` i `release`. `.claude/skills/` i
`.opencode/skills/` wskazują te same źródła.
Pochodzenie, przypięte commity i lokalne dostosowania: `.agents/skills/SOURCES.json`.
To narzędzia pracy nad repo, nie składniki publikowanego pluginu prawniczego.
Ocena pozostałych kandydatów z enhance-workflows: `docs/enhance-workflows-assessment.md`.

Walidacja odczytu: `python3 -m pytest -q tests/`. Testy providerów używają reprezentatywnych odpowiedzi;
wywołania usług na żywo wymagają skonfigurowanego konta. Nie są częścią automatycznych testów.

### Codex: brak katalogu pluginu po aktualizacji

Jeśli aktualizacja zgłasza `plugin source path is not a directory`, sprawdź zakres sparse checkout marketplace.
Musi obejmować zarówno `.agents/plugins`, jak i `plugins/grounding-prawo`. Starszą konfigurację pobierającą
same manifesty można zastąpić: `codex plugin marketplace remove grounding-prawo`, następnie ponownie
wykonać powyższe `marketplace add` z oboma `--sparse` i `plugin add`. To konfiguracja źródła marketplace;
nie zmienia połączeń ani uprawnień konektorów. Potwierdź wersję w wyniku instalacji i rozpocznij nową sesję.

## Wiki Karpathy w Basic Memory

Wiki ma trzy warstwy: dokument pierwotny, opracowane notatki z odwołaniami do źródeł
oraz indeks/graf do nawigacji. `legal` przechowuje wiedzę spraw; `main` przechowuje
recapy. Silnik serwerowy `wiki_ingest` utrzymuje kolejkę, odczyt porcjami, kontrolę
kompletności i powiązań, OCR brakujących sidecarów oraz indeks. `wiki_plan` przechowuje
stan planu niezależnie od klienta. Kontrakt narzędzi: `man(page="wiki-ingest")`.

Stan ingestu jest w Basic Memory i skaluje się do całego korpusu (~8,6 tys. źródeł): mała notatka
`_ingest/wiki-ingest-state` (aktywny dokument i offsety), inwentarz w 64 shardach `_ingest/inventory/`.
`refresh` hashuje tylko nowe lub zmienione pliki i kończy po ok. 40 s z `complete: false` — wtedy
wywołaj go ponownie. Dawne lokalne migawki wiki, plany i narzędzia z `legal` są w `_ingest/legacy/`
(typ `legacy_snapshot`, dosłownie, z `source_path` i SHA-256); lokalne katalogi usunięto 18.10.2026.

- **Dokumenty:** skill `ingest-wiki`. Przed zapisem ustaleń wyszukuje istniejące
  osoby i tematy, aktualizuje właściwe notatki, zachowuje sprzeczne wersje ze źródłami.
- **PDF i sidecar Markdown:** sidecar to robocza transkrypcja. Serwer wymaga obrazu
  każdej strony (`inspect_page`) i poprawionej transkrypcji (`verify_page`). Dopiero
  potem `start` publikuje źródło w wiki. Komentarze nieobecne na PDF pozostają poza
  transkrypcją; dopiski widoczne na PDF są częścią dokumentu. Oryginalny sidecar nie
  jest nadpisywany. Serwer sprawdza pokrycie stron i wersje plików; zgodność treści
  ocenia model oglądający obrazy. Bez obsługi obrazów klient zatrzymuje publikację.
- **Pytania, syntezy i jakość:** skill `wiki-basic-memory` korzysta z indeksu,
  `search_notes` i `build_context`; wraca do źródeł, zapisuje nowe syntezy i sprawdza
  brakujące odnośniki, duplikaty, sprzeczności oraz luki w materiale.

Adaptacja workflow Praneya Behla (`praneybehl/llm-wiki-plugin`, MIT): rozpoznanie
wpływu nowego źródła, aktualizacja powiązanych stron, jawne sprzeczności, zapis syntez
oraz rozdzielenie kontroli struktury i treści. Nie kopiujemy lokalnego silnika
wyszukiwania, drugiej bazy grafu ani pętli uruchamiających zewnętrzne modele — te
zadania obsługują istniejące MCP i Basic Memory. Ocena: `docs/llm-wiki-assessment.md`.

Źródła przypięte jako submoduły: `vendor/general/llm-wiki-plugin` oraz
`vendor/general/basic-memory` (repo `elconcept/basic-memory`; przeniesione z
`vendor/mcp/basic-memory`). Aktualizacja pluginu nie wdraża serwera. Bramka PDF
wymaga serwera z akcjami `inspect_page` i `verify_page` oraz zależnością PyMuPDF.
Wcześniej ukończone błędne importy wymagają osobnej naprawy; nie zmieniamy ich automatycznie.

### Co dociera przez marketplace do claude.ai i chatgpt.com

**Nie ma automatycznej synchronizacji całego README.md do kontekstu modelu.**
Manifesty obu klientów wskazują katalog `plugins/grounding-prawo`; samo README
repozytorium nie jest instrukcją sesji. Mechanizm dystrybucji reguł już istnieje:

1. `scripts/build.py` kopiuje `own-skills/` oraz `selection/overlay/` do skilli pluginu.
2. `add_session_protocol()` dodaje do skilli polecenie odczytu `shared/BASIC-MEMORY.md`
   i `shared/ZASADY-PLUGINU.md`. Protokół pamięci kieruje operacje wiki do `shared/WIKI.md`.
3. `ingest-wiki` i `wiki-basic-memory` dostarczają właściwe procedury. Zasady opisane
   powyżej są więc także w instalowanej paczce, bez zależności od lokalnego README.

To instrukcje odczytywane przy użyciu skilla, nie gwarantowany hook każdej rozmowy.
Konektor Lex wymaga autoryzacji; dostępność serwera i obrazy MCP zależą od klienta.
Walidacja paczki sprawdza dostarczenie plików i odsyłaczy. Aktywację na konkretnym
koncie potwierdza dopiero nowa rozmowa w claude.ai/chatgpt.com: wywołaj `ingest-wiki`,
poproś o regułę porównania sidecara z PDF i sprawdź dostępność `inspect_page`.
