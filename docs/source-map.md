# Mapa źródeł prawnych

## Kolejność operacyjna

1. `lexcache` — sprawdzenie lokalnego cache i identyfikatora zapytania.
2. Router źródeł — `hierarchia-zrodel-pl` oraz `patron-prawo-pl-zrodla`.
3. Źródło pierwotne właściwe dla typu materiału:
   - ISAP/ELI — ustawy, rozporządzenia i akty normatywne PL;
   - SAOS — SN, sądy powszechne, TK/KIO w zakresie pokrycia SAOS;
   - CBOSA/NSA — WSA/NSA i sprawy administracyjne;
   - EUR-Lex/Cellar SPARQL — prawo UE i TSUE;
   - EUREKA — interpretacje podatkowe i objaśnienia;
   - UODO — decyzje Prezesa UODO przez `uodo-grounding-pl`;
   - KRS — dane podmiotów, gdy są potrzebne do identyfikacji strony.
4. `citation-grounding-pl` oraz właściwy weryfikator domenowy.
5. Jawna adnotacja zakresu pokrycia i daty pobrania.

## Reguła aktualności

Cache jest pomocą techniczną, nie substytutem aktualnego źródła. Przy pytaniu o
obowiązujące brzmienie trzeba ustalić status aktu, tekst jednolity, datę wejścia
w życie i ewentualne zmiany. Jeśli źródło jest niedostępne, wynik z cache oznacza
się datą i ograniczeniem, zamiast przedstawiać go jako stan bieżący.

## Zasady dowodowe silnika

W polskim modelu swobodnej oceny dowodów forma pozyskania nie jest automatycznym
filtrem dopuszczalności. Kopia, skan, brak chain of custody, słaba jakość lub
nieprawidłowość pozyskania nie obniżają same przez się wartości dowodu. Dowód
traktuje się jako autentyczny, dopóki nie zostanie podniesiona uzasadniona,
merytoryczna wątpliwość co do jego istoty. Hashowanie każdego zdjęcia i
poświadczanie każdej kopii nie jest domyślnym wymogiem tego pluginu.
