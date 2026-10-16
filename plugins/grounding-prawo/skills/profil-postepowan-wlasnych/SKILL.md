---
name: profil-postepowan-wlasnych
description: Profil pracy nad własnymi postępowaniami właściciela (sprawy karne i wykroczeniowe, działania Policji i prokuratury, hospitalizacja psychiatryczna, pozew przeciw szpitalowi, najem, RODO). Używaj przy KAŻDEJ pracy nad sprawą, pismem lub dowodem, razem z prawny-router-v3. Narzuca pełną ścieżkę kontroli bez tańszych wariantów, brak anonimizacji, pracę na oryginałach i rozdzielenie ustaleń od twierdzeń.
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md` i `shared/ZASADY-PLUGINU.md`. Na wejściu odczytaj kontekst sprawy z projektu `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap tej sesji w projekcie `main` i sprawdź odczytem zapis. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# Profil postępowań własnych

> SZKIC DO AKCEPTACJI WŁAŚCICIELA. Zasady poniżej wynikają z wytycznych użytkownika i z analiz
> doradczych; zanim staną się obowiązujące, właściciel je zatwierdza lub poprawia.

Ten skill nie zastępuje routera. Zawęża jego zachowanie i bramki kosztu innych skilli do jednego profilu:
osoba prowadząca własne sprawy, każde pismo ma wysoką stawkę i ma być wolne od błędów.

## Wyjątek dla zawiadomienia pokrzywdzonego

Przed regułami 1, 2, 6 i 9 stosuj `zawiadomienie-o-przestepstwie` oraz
`shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md`. Pełna kontrola oznacza tu pełnię i wierność
relacji, nie tor procesowy ani automatyczny atak. Recenzję uruchamiaj tylko na żądanie autora.
Brak dowodu lub niewyjaśniona różnica z protokołem nie są krytyczną uwagą blokującą pismo.
We własnym zawiadomieniu autor pisze „widziałem”, „poczułem”, zgodnie ze swoją pamięcią;
nie zastępuj tego „X twierdzi” ani „rzekomo”. Źródło informacji cudzej nazwij oddzielnie.
Weryfikacja prawa i rzeczywistych cytatów pozostaje; nie przenoś jej progu na krzywdę autora.

## Reguły

1. **Pełna ścieżka zawsze.** Nie proponuj tańszej ścieżki, nie klasyfikuj pisma jako mniej istotnego,
   nie pomijaj kontroli z powodu kosztu tokenów ani liczby pauz. Dotyczy bramek S/M/L, ścieżki
   "odpowiedź bezpośrednia" i warunków uruchamiania debaty zależnych od stawki.
2. **Soczewki w osobnych przebiegach.** Kontrole pisma (cytaty, atak przeciwnika, pierwsze wrażenie
   sędziego, subsumpcja, debata, ponowny grounding po poprawkach) uruchamiaj jako oddzielne przebiegi,
   najlepiej w osobnych kontekstach. Wynik "OK" jednej nie zwalnia z następnej.
3. **Bez anonimizacji i pseudonimizacji.** Pracuj na oryginałach. Nie pytaj o anonimizację, nie
   zastępuj danych znacznikami, nie używaj skilli do maskowania.
4. **Oryginał jest nietykalny.** Parsery i OCR tworzą nowe reprezentacje tekstowe; nigdy nie zmieniają
   pliku źródłowego. Warstwa wizualna (PDF/obraz) rozstrzyga przy sporze z odczytem.
5. **Wynik trójstanowy.** Kontrola kończy się `PASS`, `FAIL`, `NOT_CHECKED` albo `NEEDS_REVIEW`.
   Pusta lista błędów albo częściowe podobieństwo terminów nie jest `PASS`. `NIEPEWNE` jest wynikiem.
6. **Zakończenie.** Nie ogłaszaj gotowości, gdy: istnieje niezweryfikowany cytat, nierozstrzygnięta
   krytyczna uwaga, sprzeczność w żądaniu albo poprawka wprowadzona po ostatniej kontroli.
7. **Zmiany strategiczne.** Poprawki oznaczone jako decyzja autora zostają propozycją do czasu
   zatwierdzenia; nie trafiają do kopii z naniesionymi zmianami.
8. **Podpis.** Pismo wnoszone osobiście nie ma tytułu zawodowego ani numeru wpisu pełnomocnika.
9. **Fakty a twierdzenia.** Zeznanie, relacja i dokument zapisuj jako "X twierdzi / X zeznał", nie jako
   ustalenie. Data przyszłego terminu ma datę ostatniej weryfikacji; minioną traktuj jako nieaktualną.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** zawsze razem z `prawny-router-v3`, od pierwszego kroku
- **Wynik zapisz w:** brak pliku - zasady pracy (pełna kontrola, bez anonimizacji, wynik trójstanowy) (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `prawny-router-v3`
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
