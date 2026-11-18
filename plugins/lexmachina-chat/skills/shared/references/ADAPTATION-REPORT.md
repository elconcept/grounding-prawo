# LexMachina `shared`: szczegółowy audyt i adaptacja CHAT — etap 1

**Stan wejścia:** `shared.zip` zawiera 193 pliki i 2 396 561 bajtów; `shared/SKILL.md` deklaruje wersję 3.99.47. **Wydanie adaptacyjne:** 3.99.48 (CHAT). Zasada: nie odtwarzamy routerów. W tej fazie zaadaptowano bibliotekę wspólną i nie publikowano jeszcze kompletnego 26-skillowego bundla.

## Podstawowe ustalenia

1. `shared` jest istniejącym skillem-biblioteką, a nie katalogiem bez `SKILL.md`.
2. Source `CHECKSUMS.sha256` ma 175 wpisów, z których 129 pasuje do aktualnych bajtów, a **46 nie pasuje**. To wada integralności manifestu wejściowego; bez danych o historii wersji nie wyciągamy wniosku o przyczynie. Nowa suma źródłowa każdego z 193 plików jest zapisana w `SOURCE-SHA256.json`, historyczny manifest w `references/upstream/CHECKSUMS.sha256`.
3. 2 pliki `.pyc` wyłączono z przenośnego pakietu (nie są kodem źródłowym i nie powinny być dystrybuowane jako utrwalony bytecode). Wszystkie inne zasoby pozostają w strukturze `shared`.
4. Poprawiono **18 plików**, a ich oryginały zachowano byte-for-byte w `references/upstream/` (nie zastąpiono żadnego tekstu źródłowego bez śladu). Historyczne instrukcje są podporządkowane `references/CHAT-RUNTIME.md` i `references/CHAT-EVIDENCE-MODEL.md`.
5. Kontrola programowa: testy unitowe `tools` wykonały 63 przypadki w `LEX_LIVE=0`: **60 passed, 3 skipped**, 0 failed. Skrypty skompilowano statycznie, bez wykonywania integracji sieciowych. Pełna weryfikacja prawna treści historycznych aktów i rzeczywisty E2E bundla są `NOT_CHECKED`.

## Mapa zmian

| Plik aktywny | Zmiana | Archiwalna kopia |
|---|---|---|
| `ACTIVATION-MATRIX.md` | Rozgraniczenie historycznej mapy i faktycznie zatwierdzonego składu bundla. | `references/upstream/ACTIVATION-MATRIX.md` |
| `BASIC-MEMORY.md` | Pamięć NAS opcjonalna, brak automatycznych odczytów i zapisów i fałszywych potwierdzeń. | `references/upstream/BASIC-MEMORY.md` |
| `CLAIM-VALIDATION.md` | CLAIM-FIRST tylko do przesłanek prawnych/dopisków modelu, bez automatycznej degradacji relacji użytkownika. | `references/upstream/CLAIM-VALIDATION.md` |
| `FACT-SOURCE-LOCK.md` | Naprawa automatycznej wyższości dokumentu urzędowego; oddzielenie metadanych i twierdzeń, bezpośrednich relacji i wniosków. | `references/upstream/FACT-SOURCE-LOCK.md` |
| `FAKTY_v2.md` | Nie klasyfikuj użytkownikowych doświadczeń jako fikcyjnych bez urzędowego potwierdzenia. | `references/upstream/FAKTY_v2.md` |
| `HIERARCHIA-ZRODEL.md` | Oddzielenie hierarchii publikatorów od oceny twierdzeń stron i instytucji. | `references/upstream/HIERARCHIA-ZRODEL.md` |
| `INDEKS-SKILLI.md` | Indeks historyczny oddzielony od faktycznie bundled skilli. | `references/upstream/INDEKS-SKILLI.md` |
| `LEGAL-STATUS-LOCK.md` | Usunięcie ryzyka automatycznej prawomocności przy niepełnej teczce źródeł. | `references/upstream/LEGAL-STATUS-LOCK.md` |
| `MOD-MACIERZ-DOWOD-TEZA.md` | Macierz nie zeruje relacji użytkownika i nie klasyfikuje urzędowych zapisów jako najsilniejszych z automatu. | `references/upstream/MOD-MACIERZ-DOWOD-TEZA.md` |
| `MOD-METODY-BADAWCZE.md` | Analiza konkurujących hipotez bez symulowanych alternatyw zwalniających organy. | `references/upstream/MOD-METODY-BADAWCZE.md` |
| `MOD-SKAN-DOWODOW-KOMPLETNY.md` | Brak automatycznej prawdziwości zeznań tylko przez status protokołu sądowego. | `references/upstream/MOD-SKAN-DOWODOW-KOMPLETNY.md` |
| `PRAWO-HARDGATE.md` | Źródła prawa na datę bez obligatoryjnego Repertorium; brak kontroli jawnie raportowany. | `references/upstream/PRAWO-HARDGATE.md` |
| `SCIEZKI-PRACY.md` | Zachowanie routingu przy wyłączeniu automatycznych zapisów NAS/Git. | `references/upstream/SCIEZKI-PRACY.md` |
| `SKILL.md` | Zastąpienie historycznej ciężkiej instrukcji lekkim entrypointem CHAT; oryginał bez zmian zachowany. | `references/upstream/SKILL.md` |
| `UNIVERSAL-RUNTIME-ADAPTER.md` | CHAT resolver zamiast lokalnej powłoki i mieszania kopii, klasyfikacja braków narzędzi. | `references/upstream/UNIVERSAL-RUNTIME-ADAPTER.md` |
| `WERYFIKACJA-SLAD.md` | Jawne statusy wywołań i źródeł bez fikcyjnych logów w CHAT. | `references/upstream/WERYFIKACJA-SLAD.md` |
| `ZASADY-PLUGINU.md` | Nadrzędny profil źródeł, dowodów i redakcji wykonalny w ChatGPT CHAT. | `references/upstream/ZASADY-PLUGINU.md` |
| `agents/openai.yaml` | Usunięto historyczne pola ikon spoza obsługiwanych metadanych agenta; oryginał zachowany. | `references/upstream/agents/openai.yaml` |

## Zakresy kontroli i ograniczenia

- **Router:** pozostaje oryginalny `prawny-router-v3`; fasada `prawo-polskie-v2` nadal wybiera dziedzinę. Nie załączamy konkurencyjnego routera i nie modyfikujemy 16-DR-owej historycznej mapy źródłowej. `CHAT-CANON.md` opisuje zatwierdzone 26 skilli, lecz **nie** twierdzi, że wszystkie są już opublikowane w obecnym wydaniu pluginu.
- **Odczyt i zasoby:** `shared/X` mapowane do `skills/shared/X` w tej samej wersji; brak źródła wewnętrznego blokuje **tylko zależny wniosek**, a brak Basic Memory, Repertorium, shell czy subagentów nie blokuje analiz wykonalnych w CHAT.
- **Dowody:** dawny FSL-A preferował protokoły i dokumenty urzędowe bez oceny ich treści; rozdzielono metadane, twierdzenie dokumentu, doświadczenie użytkownika i wniosek. Prawomocność nie wynika automatycznie z braku apelacji w niepełnych aktach. Zawiadomienie nie jest testowane standardem udowodnienia winy.
- **Terminy i treść prawa:** historyczne kwoty, daty, sygnatury i `VER` mogą służyć za indeks do weryfikacji, nigdy za dowód bieżącej aktualności bez odczytu właściwego źródła.
- **Prywatność:** historyczne twierdzenie o lokalnym przetwarzaniu dotyczy wywołań lokalnych skryptów, nie stanowi gwarancji braku transferu danych w rozmowie cloud. Nie przekazuj danych spraw do publicznego API przez domniemanie.
- **Testy:** 60/63 przeszło, 3 pominięto. Testy live MCP, prawdziwych dokumentów, cytatów i całego łańcucha `router → DR → analizator → pismo → raport` nie wykonane.

## Pełna ewidencja 193 plików

Plik `shared-file-by-file-audit.csv` zawiera dla każdego źródła: ścieżkę, rozmiar, SHA-256, klasę ingerencji, flagi ryzyka (MCP/HOST_IO/LAW/EVIDENCE) oraz stan historycznego manifestu sum. **Flagi są wynikiem statycznego skanowania, nie równoważnikiem ludzkiej recenzji 193 dokumentów.** Głęboką korektę wykonano dla 18 plików krytycznych. Każda zmiana ma oryginał, powód i test strukturalny.
