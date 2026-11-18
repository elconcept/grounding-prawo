---
name: wiki-basic-memory
description: 'Wiki sprawy w Basic Memory: ingest PDF, pytania, syntezy, kontrola jakości notatek. Używaj przy dodawaniu dokumentów do wiki i pracy na notatkach sprawy.'
---

## Pamięć (Basic Memory)

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Basic Memory: projekt `main`, sprawy pod `legal/`. Na wejściu wykonaj `bm-orient` (ostatni checkpoint z `legal/sessions/`, aktywne zadania, świeże decyzje) i odczytaj teczkę sprawy z `legal/sprawy/<katalog>/`; checkpoint (`bm-checkpoint`, `legal/sessions/`, type: session) tylko na prośbę użytkownika albo po kompakcji kontekstu, nigdy po każdej odpowiedzi. Trwałe ustalenia tylko przez `bm-remember` (`legal/bm-remember/`), istotne decyzje przez `bm-decide` (`legal/decyzje/`); nigdy logu sesji. Dokumenty i ustalenia ze spraw zapisuj w `legal/` w ramach ingestu według `shared/BASIC-MEMORY.md`. Nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `ustawy`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# Pytania i utrzymanie wiki

Przeczytaj `shared/WIKI.md` i `shared/BASIC-MEMORY.md`. Wybierz gałąź: pytanie,
synteza lub kontrola jakości. Korzystaj z istniejących narzędzi Basic Memory przez
portal Lex; odkryj aktualny schemat narzędzia przed wywołaniem. Projekt podawaj jawnie.

Odpowiedź zakończ źródłami i zakresem rzeczywiście sprawdzonego materiału.
Przy kontroli jakości podaj znalezione problemy, wykonane poprawki i pozostałe braki.

## MODUŁY SCALONE

Ten skill obejmuje funkcje dawnych osobnych skilli. Wczytaj moduł, gdy zadanie go dotyczy; reguły tego skilla obowiązują także w module.

| Moduł | Zastosowanie | Plik |
|---|---|---|
| `ingest-wiki` | ingest PDF do Basic Memory strona po stronie przez model; oryginał PDF do R2 | `modules/ingest-wiki/MODULE.md` |

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** pytanie do wiki, synteza lub kontrola jakości
- **Wynik zapisz w:** istniejąca notatka tematyczna, źródło Markdown w `legal/dokumenty` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `analizator-dowodow-v3`, `chronologia-sprawy-v1`
- **Basic Memory (`main`, `legal/`):** źródła odpowiedzi, synteza, sprzeczności i wykryte braki (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
