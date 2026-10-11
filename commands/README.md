# Komendy

| Komenda | Skąd | Co robi |
|---|---|---|
| `/eurlex` | `webwright-legal-pl` (MateMatic, Apache-2.0) | pobranie aktu UE z EUR-Lex PL przez Playwright |
| `/orzeczenie` | `webwright-legal-pl` | pobranie orzeczenia z serwisu bez konektora MCP — m.in. **sn.pl po 2016**, orzeczenia.ms.gov.pl, trybunal.gov.pl |
| `/szukaj` | `webwright-legal-pl` | wyszukanie w tych serwisach |

Te trzy komendy pokrywają zakres, którego darmowe konektory nie mają (patrz
`DOKUMENTACJA/04-PLAN-GROUNDING.md` §6). Wymagają Playwrighta — koszt i zawodność
tej ścieżki są pozycją A6 do zmierzenia w `DOKUMENTACJA/03-PLAN-INTEGRACJI.md`.

Plugin `iura-pl` deklaruje w README komendy `/review-contract`, `/triage-nda`,
`/generate-nda`, `/legal-memo`, `/tabular-review`, ale **zainstalowana wersja
marketplace ich nie zawiera** — niesie wyłącznie katalog `skills/`. Odpowiadające im
skille są w `.claude/skills/` (`przeglad-umow`, `notatka-prawna`, `przeglad-tabelaryczny`).
