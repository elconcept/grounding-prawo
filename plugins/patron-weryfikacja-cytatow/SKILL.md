---
name: patron-weryfikacja-cytatow
description: Cytowanie dokumentów w formacie [N] + blok <CITATIONS> i mechaniczna (bez LLM) weryfikacja, czy cytaty z odpowiedzi, z przeglądu tabelarycznego albo z wyników konektorów MCP naprawdę występują w tekście źródłowym. Użyj, gdy odpowiedź opiera się na dokumentach, przed wykorzystaniem cytatów w piśmie albo gdy użytkownik prosi „zweryfikuj cytaty”.
---

# Weryfikacja cytatów

Skrypt: `scripts/verify_citations.py` w katalogu tego skilla (Python 3, bez zależności).
Źródła: `.md` (np. po OCR; frontmatter pomijany), `.txt`, `.docx`, `.pdf` przez `pdftotext` -
a gdy obok PDF leży `.md` o tej samej nazwie, brany jest `.md`.

## 1. Jak cytować dokumenty
Twierdzenie o treści dokumentu dostaje znacznik `[1]`, `[2]`... w prozie, a na końcu odpowiedzi
blok:

```
<CITATIONS>
[
  {"ref": 1, "doc_id": "umowa.pdf", "page": 3, "quote": "dosłowny fragment dokumentu"},
  {"ref": 2, "doc_id": "wyrok.pdf", "page": "41-42", "quote": "zdanie przechodzące [[PAGE_BREAK]] na następną stronę"}
]
</CITATIONS>
```

- `[N]` to numer wpisu w bloku, nie numer strony ani paragrafu. Numeruj 1, 2, 3 w kolejności
  wystąpienia; każdy `[N]` ma swój wpis.
- Cytuj wyłącznie tekst dosłownie obecny w dokumencie. Krótko (do ~25 słów) i wąsko - tylko słowa
  wspierające dane twierdzenie; jedno twierdzenie, jeden cytat.
- `page` to kolejny znacznik `[Page N]` w tekście (skrypt `doc_to_text.py` ze skilla
  `patron-przeglad-tabelaryczny`), nie numer wydrukowany w stopce. Zdanie na dwóch stronach:
  `"page": "N-M"` i `[[PAGE_BREAK]]` w cytacie. Pominięty fragment: `[...]`.
- `doc_id` to identyfikator, który zmapujesz na plik w `--source` (najprościej nazwa pliku).
- Blok na samym końcu odpowiedzi; bez cytatów - pomiń go.

## 2. Weryfikacja
Zapisz odpowiedź do pliku (np. `odpowiedz.md`) i uruchom:

```bash
python3 scripts/verify_citations.py odpowiedz.md --source umowa.pdf=teczka/umowa.pdf --source wyrok.pdf=teczka/wyrok.pdf
```

- Przegląd tabelaryczny (`[[page:N||quote:...]]`, także pliki `.jsonl`):
  `--tabular --source teksty/umowa.txt`
- Cytaty z wyników konektorów MCP (blockquote `> ...` i fragmenty w cudzysłowach od 5 słów):
  zapisz wynik narzędzia do pliku i `--quotes --source wynik_saos.txt`.
- Pojedynczy cytat: `--quote "..." --source plik.txt`.
- `--json` - wynik maszynowy. Kod wyjścia 1 = co najmniej jeden cytat NIEZWERYFIKOWANY lub
  BRAK_ZRODLA.

## 3. Interpretacja

| Status | Znaczenie | Co zrobić |
|---|---|---|
| ZWERYFIKOWANY | cytat jest w źródle (po ujednoliceniu cudzysłowów, myślników, wielkości liter, spacji i dzielenia wyrazów) | można użyć |
| ZMODYFIKOWANY | drobne różnice, do 15% znaków (interpunkcja, ucięcie) | popraw cytat do brzmienia oryginału |
| NIEZWERYFIKOWANY | brak trafienia - możliwa halucynacja | usuń albo znajdź prawdziwy fragment; nie używaj w piśmie |
| BRAK_ZRODLA | nie podano tekstu źródła dla `doc_id` | dodaj `--source` |

Skrypt wypisuje też odwołania z prozy bez cytatu (art., §, sygn.) z oznaczeniem
„[model - zweryfikuj]” - sprawdź je w konektorach (skill `patron-prawo-pl-zrodla`).

## Granice
Skrypt sprawdza ISTNIENIE tekstu w źródle, nie to, czy cytat wspiera tezę. Po pozytywnym wyniku
oceń sam, czy fragment rzeczywiście mówi to, co mu przypisujesz (kontekst, zaprzeczenia,
wyjątki). Brak tekstu źródła nigdy nie oznacza potwierdzenia.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/citation/grounding.ts`
(ADR-0005), `mcp-grounding.ts` (ADR-0146), `heuristicCitations.ts`; format cytatów z
`lib/chat/prompts.ts`.
