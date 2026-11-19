---
name: chat-router-akta-i-dowody
description: "Wejście CHAT do przebudowywanego bundla LexMachina: deleguje decyzję routingu do oryginalnego prawny-router-v3, bez tworzenia drugiej macierzy."
---

# LEXMACHINA-CHAT — wejście do pakietu (1.0.1)

**Identyfikator skilla** `chat-router-akta-i-dowody` pozostaje historyczny dla kompatybilności. Nazwa całego pluginu to **LEXMACHINA-CHAT**.

**Jeden algorytm routingu:** dla zadania prawnego odczytaj i zastosuj `prawny-router-v3/SKILL.md`. Tylko ten skill klasyfikuje [1]–[11], ustala PRIMARY/SECONDARY/FALLBACK i stosuje wyzwalacze. Nie projektuj konkurencyjnego routera i nie ładuj całej biblioteki naraz.

`przewodnik-prawny-v2` jest już **obecny w tej samej wtyczce** jako oryginalny gospodarz sesji i fallback routera (PROWADZENIE/Q&A/MENU, niezależny tryb SUROWA ANALIZA). Nie stosuj go do ponownego routingu ani do zbędnego intake. Po przydzieleniu przez oryginalny router użyj `skills/przewodnik-prawny-v2/SKILL.md`, respektując `references/CHAT-RUNTIME.md`.

`prawo-polskie-v2` jest już **obecne w tej samej wtyczce** jako oryginalna fasada 16 dziedzin DR. Po wyborze routera odczytaj tę fasadę, nie zastępuj jej algorytmem czatu. Historyczne aliasy normalizuj według `skills/prawo-polskie-v2/references/CHAT-DR-RESOLUTION.md`. `shared` znajduje się w tej samej wtyczce jako jedna kanoniczna biblioteka `skills/shared/`. Dla etapów jeszcze niezintegrowanych, zwłaszcza nieprzeniesionych DR i audytu systemu, użyj **faktycznie dostępnego** skilla z innych wtyczek albo oznacz `PENDING/NOT_AVAILABLE`. Nie twierdź o załadowaniu na podstawie samej nazwy w metadanych.

**Analizator umów:** `analizator-umow-v1` jest już w tym bundlu (analiza, redakcja, negocjacje umów, moduły G/H/I/K, J0–J21, MA, CUAD i kalkulator). Po przydzieleniu go przez oryginalny router zastosuj `skills/analizator-umow-v1/SKILL.md` oraz wyłącznie potrzebne `references/`/`workflows/`; to **wewnętrzna selekcja modułów**, nie nowy globalny router.

**Raport sytuacyjny (etap 8/8):** `raport-sytuacyjny-v2` v2.13 zaadaptowany do CHAT jest już w bundlu. Zachowaj trzy oryginalne tryby: [A] po ukończeniu analizy konkretnej sprawy, [B] po nowym dokumencie — tylko propozycja, [C] na żądanie — bez zwłoki. Jest finalnym postprocesorem, a nie drugą macierzą routingu. Czytaj `skills/raport-sytuacyjny-v2/SKILL.md` i `references/CHAT-RUNTIME.md`. Raport obejmuje siedem sekcji, brak źródła prawa i niewykonane funkcje UI musi być jawny.

**Raport klienta (etap 8/8):** `raport-klienta-v1` v1.9 jest dostępny w tym bundlu jako osobny postprocesor dla odbiorcy IND lub BIZ. Nie zastępuje raportu sytuacyjnego. Odczytaj `skills/raport-klienta-v1/SKILL.md` i `references/CHAT-RUNTIME.md`; zachowaj tryby `standard`, `brak_nowosci`, `zle_wiadomosci`, `ograniczenie_szkod`, raport `delta` i ochronę wewnętrznej strategii. Skille pozostałe poza tym adaptowanym rdzeniem są obsługiwane tylko po rzeczywistym odczycie.

**Audyt systemu (etap 8/8):** `audyt-systemu-v4` v6.270 jest w bundlu jako orkiestrator jakości i audytu samej biblioteki, nie klasyfikator sprawy. Jego tryby i FAZA 0–7 są zachowane; przy wywołaniu odczytaj `skills/audyt-systemu-v4/SKILL.md` i `references/CHAT-RUNTIME.md`, dobieraj moduły selektywnie, nie traktuj zachowanych skryptów jako wykonanych automatycznie. Raportuj prawo i skrypty `NOT_CHECKED`/`NOT_RUN` bez realnego wykonania. Nie zmieniaj starej macierzy [1]–[11].

Dotychczasowe `analiza-sadowa-v6`, `analizator-dowodow-v3` i `chronologia-sprawy-v1` są dostępne w tym bundlu i pozostają współpracującym rdzeniem. `chronologia-stanowiska-pl` jest na etapie migracji zachowana wyłącznie dla kompatybilności starej wtyczki; **nie należy do zatwierdzonego kanonu LexMachina**. Nie traktuj jej jako zamiennika chronologii źródłowej.

Raportuj faktycznie wykonane odczyty i kontrole; źródło urzędowe nie ma automatycznej przewagi dowodowej. Nie wymagaj obowiązkowego Basic Memory, konsoli, MCP ani automatycznego pliku wynikowego. Przy braku narzędzia wykonaj możliwą część analizy, zachowując `NOT_CHECKED` dla elementów niesprawdzonych. Zachowaj relacje i kanon TK/NC w ich sprawach oraz symetrię oceny dokumentów Policji i szpitali.
