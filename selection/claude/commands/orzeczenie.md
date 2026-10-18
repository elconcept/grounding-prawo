---
description: Pobierz orzeczenie spoza MCP (sn.pl, orzeczenia.ms.gov.pl, trybunal.gov.pl) po sygnaturze.
argument-hint: <sygnatura> [sąd]
---

Użyj skilla `grounding-prawo:webwright-legal-pl`, komenda `orzeczenie` (jej instrukcja: `commands/orzeczenie.md` w katalogu skilla), z argumentami: $ARGUMENTS

Najpierw sprawdź, czy wystarczy MCP portalu `lex` (`saos`, `nsa`, `eu-sparql`, `isap`) - webwright tylko dla zakresu bez konektora
(np. SN po 2016 spoza dumpu SAOS, orzeczenia.ms.gov.pl, TK). W kontenerze na NAS przy blokadzie (CGNAT) uruchom skrypt `shared/scripts/tor_rotator.sh` z katalogu zainstalowanego pluginu grounding-prawo.
Wynik zapisz w teczce sprawy w `_robocze/` (z prefiksem `rrrrMMdd_hhmm_`), a w odpowiedzi podaj URL źródła i datę pobrania.
