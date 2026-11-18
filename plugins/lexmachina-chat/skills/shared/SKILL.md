---
name: shared
description: "Biblioteka kanonicznych bramek i modułów LexMachina. Używana przez router i skille wykonawcze; nie wywoływać jako osobnej analizy sprawy."
metadata:
  version: '3.99.48'
  type: library
  profile: 'CHAT/host-neutral'
  original_version: '3.99.47'
---

# Shared LexMachina — biblioteka dla bundla CHAT

Nie jest osobnym generatorem pism ani odrębnym routerem. **Orkiestruje `prawny-router-v3`** i **wybiera domenę `prawo-polskie-v2`**. Nie zastępuj ich nową macierzą. Wykorzystuj wyłącznie moduły faktycznie aktywowane przez te skille, bez wczytywania całego `shared` naraz.

## Obowiązująca hierarchia instrukcji

1. [CHAT-RUNTIME](references/CHAT-RUNTIME.md) — techniczne mapowanie operacji, dostępności narzędzi i zasobów (nadrzędne wobec historycznych ścieżek, shell i MCP).
2. [CHAT-EVIDENCE-MODEL](references/CHAT-EVIDENCE-MODEL.md) — rozdzielenie bezpośredniej relacji, treści dokumentu, obserwacji, faktu procesowego i wniosku; symetryczna ocena źródeł.
3. [CHAT-CANON](references/CHAT-CANON.md) — lista skilli z zatwierdzonego bundla i statusy. Nie traktuj katalogu historycznego jako dowodu instalacji.
4. [UNIVERSAL-RUNTIME-ADAPTER](UNIVERSAL-RUNTIME-ADAPTER.md), [ZASADY-PLUGINU](ZASADY-PLUGINU.md) i [INDEKS-SKILLI](INDEKS-SKILLI.md) — obecne pliki systemowe; ich legacy polecenia wykonuj tylko poprzez kontrakt CHAT.
5. Dokumenty dziedzinowe `MOD-*`, `PRAWO-HARDGATE*`, `FAKTY_v2`, `FACT-SOURCE-LOCK`, `CLAIM-VALIDATION`, `LEGAL-STATUS-LOCK` i inne: czytaj selektywnie w chwili wyzwolenia przez router/skill.

## Wejście do analizy

- Ustal zadanie i tryb za pomocą **istniejącego** `prawny-router-v3`; `prawo-polskie-v2` dobiera DR; przewodnik jest wyłącznie fallbackiem zgodnie ze źródłem.
- `view shared/<plik>` oznacza odczyt **`skills/shared/<plik>` w tym samym wydaniu bundla**. Nie łącz ze starą kopią `shared` z innej wtyczki. Na zewnątrz tego bundla odczyt wymaga rzeczywiście dostępnego skilla lub narzędzia.
- Brak obowiązkowego dokumentu merytorycznego zgłoś jako brak konkretnego zasobu; brak zewnętrznego MCP, Basic Memory, narzędzia shell lub możliwości zapisu **nie blokuje analizy możliwej na dostępnych danych**.
- Prawo: źródło urzędowe, wersja na datę, tekst artykułu i właściwy zakres; nie nazywaj wyniku wyszukiwania dosłownym cytatem. Nieprzeprowadzone kontrole oznacz `NOT_CHECKED`.
- Dowody: bezpośrednie doświadczenia TK/NC (wyłącznie gdy ich sprawa jest analizowana) przyjmuj jako przekazany kanon sprawy, nie przyjmuj automatycznie prawdziwości wpisów Policji, lekarzy czy prokuratorów. Nie uznawaj statusu autora za wartość dowodową, porównaj niezależne podstawy i oceniaj łącznie.
- Nigdy nie deklaruj działań subagenta, multi-modelu, aktualizacji bazy, walidacji kryptograficznej, zapisu pliku, CLI lub weryfikacji online bez rzeczywistego wykonania i wyniku.
- Dane wrażliwe: żadne przeszukanie publiczne, endpoint, widget ani OCR zewnętrzny nie otrzymuje automatycznie treści akt. Używaj tylko rzeczywiście autoryzowanego kanału w odpowiedniej sprawie.

## Zgodność i historia

Oryginalny plik wejściowy: [SKILL.upstream.md](references/upstream/SKILL.md). Oryginały innych zmienionych plików znajdują się w `references/upstream/`. Hashy źródłowych nie nadpisano: `references/SOURCE-SHA256.json`. Kontrole pakietu: `references/ADAPTATION-REPORT.md`; historyczny `CHECKSUMS.sha256` zachowano jako `references/upstream/CHECKSUMS.sha256`. Żaden skrypt w katalogu `tools/` nie uruchamia się samoczynnie.
