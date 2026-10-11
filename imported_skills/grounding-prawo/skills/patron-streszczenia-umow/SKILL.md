---
name: patron-streszczenia-umow
description: Streszczenie prawne jednej umowy według stałej listy punktów - umowa kredytowa (21 punktów), umowa wspólników lub inwestycyjna (15 punktów) - albo lista warunków zawieszających (CP checklist) z umowy finansowania; z odesłaniami do klauzul i oznaczeniem postanowień nietypowych lub rynkowo niekorzystnych. Użyj, gdy użytkownik prosi o streszczenie, term sheet albo checklistę CP konkretnej umowy.
---

# Streszczenia umów

Dla każdego punktu: kluczowe postanowienia, odesłanie do klauzuli lub załącznika dosłownie
(„§ 7 ust. 2”, „Clause 22.1”, „Załącznik nr 3”) i oznaczenie postanowień nietypowych,
uciążliwych albo odbiegających od standardu rynkowego. Czego w umowie nie ma - „brak w umowie”.
Pisz w języku użytkownika; nazwy instytucji rynkowych (drag-along, margin ratchet) zostaw
w oryginale. Domyślnie wynik w czacie; plik (Markdown, Word przez pandoc) tylko na prośbę.
Wiele umów naraz według tych samych pytań - skill `patron-przeglad-tabelaryczny`.

## Umowa kredytowa (21 punktów)
1. **Kredytodawcy** - wszyscy kredytodawcy lub członkowie konsorcjum: pełna nazwa i rola
   (mandated lead arranger, original lender, bank agent).
2. **Kredytobiorcy** - pełna nazwa i jurysdykcja utworzenia.
3. **Gwaranci** - pełna nazwa i zakres zobowiązania gwarancyjnego.
4. **Inne strony** - agent kredytu, agent zabezpieczeń, kontrahenci transakcji zabezpieczających,
   bank wystawiający; ich role.
5. **Data umowy.**
6. **Kredyty** - każdy kredyt (RCF, Term Loan A/B/C): rodzaj, transza, kluczowe cechy.
7. **Kwota** - łączna kwota zobowiązania, waluta, podział na transze.
8. **Cel** - na co można przeznaczyć środki i jakie są ograniczenia.
9. **Oprocentowanie** - stawka referencyjna (WIBOR/WIRON, EURIBOR, SOFR), marża, margin ratchet,
   okresy odsetkowe.
10. **Prowizja od niewykorzystanej kwoty** (commitment / utilisation fee) - stawka, sposób
    liczenia, podstawa.
11. **Harmonogram spłaty** - raty czy spłata jednorazowa (bullet), daty i kwoty.
12. **Ostateczny termin spłaty** - dla każdego kredytu.
13. **Zabezpieczenia** - każda kategoria (zastaw na udziałach, zastaw rejestrowy, hipoteka,
    zastaw na rachunkach, przelew wierzytelności) i ich przedmiot.
14. **Gwarancje** - gwaranci, zakres, ograniczenia (up-stream guarantee limitations,
    guarantor coverage test).
15. **Kowenanty finansowe** - wskaźnik (dźwignia, pokrycie odsetek, pokrycie przepływów), test,
    częstotliwość, equity cure.
16. **Przypadki naruszenia (Events of Default)** - okresy naprawcze, progi istotności,
    cross-default.
17. **Przeniesienie praw** - ograniczenia po stronie kredytodawców (white/blacklist, zgoda
    kredytobiorcy) i kredytobiorcy.
18. **Zmiana kontroli** - definicja, skutki (obowiązkowa przedpłata, anulowanie, zgoda
    kredytodawców), okres naprawczy.
19. **Opłata za wcześniejszą spłatę** - prepayment fee, make-whole, soft-call: stawka, okres,
    wyjątki (środki z ubezpieczenia, ze zbycia aktywów).
20. **Prawo właściwe.**
21. **Rozstrzyganie sporów** - sąd czy arbitraż, forum lub siedziba, poddanie jurysdykcji.

## Umowa wspólników / inwestycyjna (15 punktów)
1. **Strony i udziały** - pełne nazwy, role, klasy udziałów lub akcji, procent (w pełni
   rozwodniony, jeśli podany).
2. **Klasy udziałów i uprawnienia** - dla każdej klasy: głos, dywidenda, uprzywilejowanie przy
   likwidacji, zamiana lub umorzenie.
3. **Zarząd, rada i ład korporacyjny** - liczba członków, prawo powoływania (i progi udziałowe
   do jego utrzymania), kworum, głos decydujący.
4. **Sprawy zastrzeżone** - decyzje wymagające kwalifikowanej większości, jednomyślności lub
   zgody konkretnego wspólnika; próg i czyja zgoda.
5. **Pierwszeństwo objęcia nowych udziałów** - kto, procedura, terminy, wyjątki (programy
   motywacyjne).
6. **Ograniczenia zbywania** - lock-up, zakazy, zbycia dozwolone (np. do podmiotów powiązanych),
   wymagane zgody.
7. **Prawo pierwokupu / pierwszeństwa przy zbyciu** - przesłanki, procedura, cena, wyjątki.
8. **Drag-along** - kto, próg, warunki (cena minimalna, niezależna wycena), ochrona mniejszości.
9. **Tag-along** - kto, próg, procedura, cena i warunki.
10. **Ochrona przed rozwodnieniem** - rodzaj (full ratchet, średnia ważona), przesłanki,
    mechanika, wyjątki.
11. **Dywidendy** - obowiązek lub cel wypłat, uprzywilejowanie, ograniczenia.
12. **Wyjście i płynność** - ścieżki (sprzedaż, IPO, drag), terminy, preferencje likwidacyjne.
13. **Pat decyzyjny** - definicja, eskalacja, mechanizmy (russian roulette, opcje put/call),
    skutki braku rozwiązania.
14. **Zakaz konkurencji i przejmowania pracowników lub klientów** - kogo wiąże, zakres
    przedmiotowy i terytorialny, czas, wyjątki.
15. **Prawo właściwe i spory** - prawo, forum, sąd czy arbitraż, obowiązkowe etapy przedsądowe.

## Lista warunków zawieszających (CP checklist)
Z umowy kredytowej lub innego dokumentu finansowania. Sekcja na każdą kategorię warunków
(korporacyjne, finansowe, prawne, zabezpieczenia...), w każdej tabela z dokładnie czterema
kolumnami w tej kolejności: **Lp.** (od 1 w obrębie kategorii) | **Nr klauzuli** |
**Warunek** (zwięzły opis) | **Status** (puste - do uzupełnienia przez użytkownika).

Przed oddaniem sprawdź: każda tabela ma te cztery nagłówki w tej kolejności, każdy wiersz ma
cztery komórki, numeracja jest ciągła od 1, w komórkach nie ma markdownu, znaków nowej linii
ani placeholderów (Status jest pusty). Domyślnie plik (`pandoc checklista.md -o checklista.docx`,
orientację poziomą ustaw w Wordzie) albo tabela Markdown w czacie, jeśli użytkownik woli.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/builtinWorkflows.ts` oraz
`frontend/src/app/components/workflows/builtinWorkflows.ts` (Credit Agreement Summary,
Shareholder Agreement Summary, Generate CP Checklist).
