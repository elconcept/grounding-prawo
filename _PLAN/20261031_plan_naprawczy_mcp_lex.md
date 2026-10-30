# USTAWY — plan stabilizacji bazy ustaw i komentarzy oraz interfejsu PL

> Audyt 2026-10-31: testy narzędzi przez portal `lex`, wywołania bezpośrednie w kontenerach, inspekcja kodu elconcept. **Plan**, nie wdrożenie. **POTWIERDZONE** = fakt testowy lub z kodu; **DO SPRAWDZENIA** = hipoteza.

## Reguły wdrożeniowe
- Polskie zapytania, polska treść, polskie tytuły i polskie błędy. Brak selektora języka w publicznym MCP. Identyfikatory (CELEX/ELI/ECLI, sygnatury, techniczne nazwy) pozostają zgodne ze źródłem.
- `content` i `structuredContent` muszą być zachowane przez kontener, Cloudflare, portal `lex` i klienta. Tekst urzędowy należy oddzielić od komentarza, a stan prawny oznaczyć datą/źródłem.
- Przed produkcyjnym wdrożeniem: test fixture i regresja → staging → smoke end-to-end → kopia stanu → bezpieczny rollout i rollback. Nie ujawniać danych identyfikujących, tokenów ani pełnych logów dostępu.

## Materiał dowodowy
- **POTWIERDZONE:** `ustawy_akty()` zwróciło 37 aktów. `ustawy_szukaj(q='przesłuchanie',akt='kpk',zakres='przepisy')` znalazło m.in. art. 371, 185e i 185a k.p.k.
- **POTWIERDZONE:** `ustawy_artykul(akt='uozp',art='23',komentarz=true)` zwróciło `status='FOUND'`, pełny tekst art. 23 i komentarz (1781 znaków); `ustawy_artykul(kpk,171,true)` również `FOUND`. `ustawy_szukaj(q='dotychczasowe zachowanie',akt='uozp',zakres='komentarze')` znalazło komentarze do art. 23 i 29.
- **POTWIERDZONE:** `ustawy_cytat(uozp,23,'zagraża bezpośrednio własnemu życiu')` i test cytatu z art. 171 k.p.k. zwróciły `FOUND`, fikcyjna fraza — `NOT_FOUND`.
- **OBJAW WCZEŚNIEJSZY, NIEPOWTÓRZONY:** przy wcześniejszym teście `ustawy_artykul(uozp,23,false)` było `OUT_OF_SCOPE`, a `ustawy_cytat` — `Error executing tool cytat`; późniejszy retest obu działał. Przyczyna czasowej niespójności **nie została ustalona**.
- **POTWIERDZONE W KODZIE:** `own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py` buduje lokalny indeks SQLite FTS5 z submodułów `vendor/law` (brzmienie+komentarz) i `vendor/law-git` (wybrane akty git-as-law); `deploy/mcp-ustawy/Dockerfile` buduje indeks przy tworzeniu obrazu, a `LAW_REFRESH` wymusza ponowne pobranie. Komentarz jest opracowaniem, nie źródłem urzędowym. Serwer `ustawy_mcp.py` zwraca struktury `akty`, `szukaj`, `artykul`, `cytat`.

## Plan
1. **P0 — analiza niestabilności:** zablokować wersję obrazu i zapisać checksum indeksu `ustawy.sqlite`, rozmiar, datę budowy, commit submodułów, liczbę aktów/artykułów/komentarzy i status kontenera. Powtarzać sekwencję `akty→artykul(uozp,23)→cytat→komentarz` 10× bez równoległego redeployu; prześledzić błąd `OUT_OF_SCOPE` przez logi (bez danych osobowych).
2. **P0 — spójność danych:** w `/healthz` poza liczbą aktów uwzględnić integralność indeksu i próbki 3 znanych artykułów, w tym `uozp:23`, oraz kompletność komentarzy. Brak indeksu lub brak danego aktu po wdrożeniu to błąd, nie pozorny stan `healthy`.
3. **P1 — wersjonowanie prawa:** jawny manifest źródeł `akt, ELI, tekst_jednolity, stan_na, ostatnia_zmiana, commit, checksum`; porównanie z aktualnymi publikatorami ELI i zmianami po tekście jednolitym. Brzmienie z komentarza nie może być opisane jako na pewno aktualne, jeśli nie ma kontroli późniejszych nowelizacji.
4. **P1 — trafność polska i obsługa komentarzy:** testy `szukaj` dla fleksji, odmiany i diakrytyków, wyszukiwania `zakres=przepisy|komentarze`, artykułów z literą i indeksami górnymi. Wynik `artykul(...komentarz=true)` ma wyraźnie oddzielone pola `tekst` i `komentarz`, informację o autorstwie/źródle opracowania; `cytat` kontroluje wyłącznie urzędowy tekst, nie komentarz.
5. **P1 — schema/result:** kody `FOUND/NOT_FOUND/OUT_OF_SCOPE` + polski komunikat, stałe `content` i `structuredContent` w ścieżce portalu; testy przy błędach indeksu i przeciążeniu. Nie dodawać selektora języka.
6. **P2 — release i rollback:** CI z manifestem pinned submodułów, build odtwarzalny, canary testy `uozp 23`, `kpk 171`, `kpc`; snapshot poprzedniego indeksu przed przebudową. Nie mieszać wersji dokumentów z różnymi datami bez adnotacji.

## Akceptacja
- Identyczny zestaw 37 aktów i przynajmniej kontrolnych artykułów po restarcie oraz po odtworzeniu obrazu; brak losowego `OUT_OF_SCOPE` przy istniejącym akcie.
- `uozp:23` i `kpk:171` przechodzą odczyt, komentarz, szukanie, FOUND/NOT_FOUND cytatu. Pełne polskie pola dostępne także przez `lex`.
- Każda odpowiedź mówi, skąd pochodzi brzmienie i na jaką datę je zweryfikowano; komentarz wyraźnie nie ma statusu prawa powszechnie obowiązującego.

## Pliki / dowody
`own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py`, `ustawy_mcp.py`, `deploy/mcp-ustawy/Dockerfile`, `clone_law.py`, `compose.yaml`, `.gitmodules` i repo komentarzy prawa.
