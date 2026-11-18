# Profil wykonawczy CHAT v0.2 — Akta i Dowody

## Zakres i pierwszeństwo

Ten profil jest integralną częścią SKILL.md w wydaniu CHAT. Ma pierwszeństwo **wyłącznie w kwestiach technicznych** (odczyt plików, pamięć, źródła, zapisy, skrypty, renderowanie, routing) przed legacy fragmentami źródłowymi i skopiowanymi dokumentami `shared/`. Metodologia oceny dowodów i prawo właściwe pozostają bez zmian. Archiwum `SKILL.upstream.md` pozostaje niezmienione.

## Zasada zero wymuszonych integracji

- **Nie wymagaj Basic Memory ani projektów `main`, `legal`, `model-memory`**. Kontynuuj wyłącznie na podstawie obecnego dialogu, dostępnych załączników i rzeczywiście odczytanych źródeł. Zachowuj podane przez użytkownika wcześniejsze ustalenia bez sztucznego resetu, ale nie deklaruj odczytu nieużytego źródła. W razie potrzeby sporządź w odpowiedzi zwarty `STAN-SPRAWY` (sygnatura, ostatnia czynność, ustalenia, źródła, otwarte punkty) — bez domniemanego trwałego zapisu.
- **Nie wymagaj żadnego określonego MCP**, portalu, serwera, skilla spoza tej wtyczki ani własnej powłoki; użyj tylko faktycznie udostępnionych funkcji. Brak narzędzia nie blokuje ekstrakcji, analizy źródłowej i syntezy. Gdy aktualna norma albo orzeczenie są kluczowe, sprawdź ich tekst przez dostępne narzędzia lub oficjalne źródła internetowe; jeżeli odczyt jest niemożliwy, nie cytuj niezweryfikowanego brzmienia i oznacz część prawną `NOT_CHECKED` (nie ocenę dowodów jako całość).
- **Odczyt dokumentu**: użyj widocznego tekstu/załącznika lub funkcji odczytu pliku faktycznie dostępnej w sesji. Rozdziel transkrypcję, cytat, obserwację i wniosek. Nie wymyślaj strony, cytatu, sygnatury, metadanych, daty sprawdzenia lub wyniku narzędzia. Dokument z nieprzeczytaną stroną ma lukę pokrycia.
- **Ścieżki `shared/X.md`** odnoszą się do `shared/X.md` skopiowanego do folderu bieżącego skilla; to zasób tej wtyczki, nie niezainstalowana zewnętrzna wtyczka. Historyczne `/mnt/skills/user/shared/X.md` rozumiej tak samo. `view`, `Read`, `web_search`, `show_widget`, `present_files` to nazwy dawnych operacji — nie żądaj literalnych komend. Jeżeli obowiązkowego pliku rzeczywiście brakuje, wskaż brak konkretnego zasobu; nie przypisuj mu rzekomej treści.
- **Brak wymuszonego wykonywania Python, shell, Playwright, API Anthropic, OCR w osobnym skillu, zapisu JSON/DOCX albo HTML-widgetu.** Zamieniaj dostępne etapy na jawne działania tekstowe: tabela oś czasu, macierz dowód–teza, graf Mermaid, rejestr etapów, lista nieprzeczytanych stron i cytatów. Skrypty oraz interaktywne widoki są opcjonalną techniką *tylko gdy rzeczywiste narzędzie i wejście istnieją*. Nie twierdź, że wynik przeszedł walidację maszynową, nie został zapisany jako plik ani zsynchronizowany.
- **Wynik i ciągłość**: domyślnie przedstaw gotowy wynik w rozmowie z identyfikatorami wierszy, lokatorami i podsumowaniem pokrycia; plik zapisuj jedynie gdy użytkownik tego chce i narzędzie rzeczywiście go tworzy. Żadne domyślne `legal/output/`, `analiza/_...md` i backend wiki nie są wymagane.
- **Routing**: w tej wtyczce `chat-router-akta-i-dowody` zastępuje nieobecny historyczny `prawny-router-v3`. Gdy zakres wykracza poza nią, wykonaj możliwą część lub sięgnij do innego skilla tylko gdy jest rzeczywiście dostępny; nie przerywaj całej pracy.

## Granice prawne i dowodowe

Przyjęte fakty i bezpośrednie doświadczenia użytkownika to materiał odniesienia w jego sprawie. Wpis organu lub lekarza pozostaje twierdzeniem autora; nie otrzymuje przewagi przez samą rangę dokumentu. Tezy każdej strony sprawdzaj według tego samego standardu; najpierw kontroluj źródła twierdzeń obciążających użytkownika, następnie oceniaj łącznie materiał korzystny. Nie wymyślaj obrony organu ani intencji sprawcy. Rozdziel fakt źródłowy, relację, interpretację i hipotezę. Przy zawiadomieniu pokrzywdzonego nie wymagaj udowodnienia jego relacji ani nie stosuj reżimu pisma procesowego.

## Statusy minimalne

- `ODCZYT`: `PEŁNY` / `CZĘŚCIOWY` / `BRAK` — dla materiałów dostarczonych w sesji.
- `PRAWO`: `VERIFIED` (realny odczyt aktualnego źródła) / `NOT_CHECKED` (brak sprawdzenia).
- `SKRYPTY`: `NIEURUCHOMIONE`, chyba że narzędzie rzeczywiście je uruchomi i da rezultat.
- `ZAPIS`: `W ROZMOWIE` lub `PLIK POTWIERDZONY` wraz ze wskazaniem realnego artefaktu.

Wspomniane w archiwalnych sekcjach „HARD GATE” nadal oznaczają wymaganą kontrolę merytoryczną, **nie nakaz dostępu do nieistniejących usług**. Dla nieweryfikowalnej informacji nie przypisuj pozytywnego wyniku bramki; jawnie pokaż jej zakres i ograniczenie.
