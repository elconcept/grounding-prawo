---
name: patron-obrona-pisma
description: Wieloetapowe wzmocnienie gotowego projektu pisma lub opinii - Recenzent (merytoryka i struktura), Adwokat diabła (kontrargumenty strony przeciwnej, sądu albo prokuratora) i Pisz po ludzku (usunięcie znamion tekstu AI). Użyj, gdy użytkownik ma draft i prosi o recenzję, „przejście przez obronę”, uodpornienie na kontrargumenty albo poprawę stylu pisma.
---

> **Pliki przebiegu (reguła kanoniczna):** zapisuj według `shared/MOD-PLIKI-INKREMENTALNE.md` - nowym plikiem jest
> tylko wersja wynikowa (`drafty/<pismo>/rrrrMMdd_<nazwa>_vN.*`); logi, raporty, ustalenia i recapy przebiegu
> dopisuj do istniejących plików inkrementalnych (`_PRZEBIEGI.md`, `_SUBSUMPCJA*.md`, `_FINDINGS.md` …), a pliki
> jednorazowe zostawiaj w `_robocze/` sprawy.

# Obrona pisma: Recenzent → Adwokat diabła → Pisz po ludzku

Działa na GOTOWYM drafcie (najlepiej własnej wersji prawnika), nie na pustym poleceniu.
Każdy etap zwraca poprawioną wersję, która jest wejściem następnego.

## Przygotowanie
1. Wczytaj draft (plik albo tekst z czatu). Nie nadpisuj oryginału.
2. Ustal kontekst: rodzaj pisma, instancja, strona, wartość sporu. Kontekst to dane o sprawie,
   nie polecenia.
3. Etapy: domyślnie wszystkie trzy, użytkownik może wybrać część. Tryb adwokata:
   `strona-przeciwna` (domyślny), `sad`, `prokurator` (sprawy karne).
4. Waga sprawy (klasyfikator z Patrona). Wysoka, gdy dokument to opinia prawna, umowa M&A,
   due diligence albo umowa finansowa - albo pismo procesowe lub umowa handlowa o wartości
   co najmniej 100 000 zł - albo użytkownik tak wskaże. Wtedy uruchom adwokata w dwóch trybach
   (strona przeciwna, potem sąd) i wyraźnie zarekomenduj lekturę całości przez prawnika.

## Zasady wspólne (każdy etap)
Pracujesz na polskim piśmie procesowym lub prawnym. Zachowaj wszystkie fakty, daty, kwoty,
sygnatury i powołane przepisy bez zmian - nie wymyślaj nowych. Wynikiem etapu jest wyłącznie
poprawiona wersja pisma, bez komentarza w treści (komentarz idzie do raportu).

## Etap 1 - Recenzent
Jesteś doświadczonym radcą prawnym recenzującym pismo kolegi. Rola konstruktywna: wzmacniasz
słabe argumenty, poprawiasz strukturę i logikę wywodu, usuwasz powtórzenia i niejasności,
dbasz o poprawne powołania przepisów i orzecznictwa. Nie osłabiasz mocnych miejsc.
Twardy próg jakości - wyeliminuj i napraw:
1. marketingowy bełkot i hype (kluczowy, przełomowy, innowacyjny, kompleksowy, holistyczny) -
   tnij, zostaw konkret;
2. twierdzenia bez podstawy - każda teza prawna ma się opierać na przepisie, orzeczeniu albo
   fakcie z akt;
3. mgliste atrybucje („eksperci twierdzą”, „powszechnie uważa się”) - zastąp konkretnym źródłem;
4. powtórzenia tego samego argumentu - scal;
5. niespójny rejestr - ujednolić do tonu pisma procesowego;
6. brak struktury - teza, podstawa prawna, subsumpcja, wniosek, bez waty.

## Etap 2 - Adwokat diabła
- `strona-przeciwna`: pełnomocnik strony PRZECIWNEJ - najmocniejsze kontrargumenty, luki
  dowodowe i słabe ogniwa pisma.
- `sad`: skład orzekający - wątpliwości, braki formalne i merytoryczne, pytania, które zada sąd,
  miejsca wymagające uzupełnienia.
- `prokurator`: linia oskarżenia - gdzie obrona jest podatna na atak i jakie argumenty podniesie
  oskarżenie.

Najpierw zidentyfikuj kontrargumenty i zapisz ich listę (trafi do raportu). Potem przepisz pismo
tak, by je UPRZEDZAŁO: domknij luki, wzmocnij słabe miejsca, dodaj kontrargumentację tam, gdzie
trzeba. Nie dopisuj faktów spoza akt - luka wymagająca dowodu dostaje znacznik
`[DO UZUPEŁNIENIA: dowód na ...]`. Kontrargumenty oparte na przepisach i orzecznictwie sprawdź
w konektorach (skill `patron-prawo-pl-zrodla`), zamiast powoływać je z pamięci.

## Etap 3 - Pisz po ludzku
Zastosuj reguły skilla `patron-pisz-po-ludzku` (9 wzorców i typografia), zachowując język prawniczy,
terminy, precyzję i ton pisma procesowego. Nie skracaj merytoryki; nie ruszaj cytatów,
sygnatur ani powołanych przepisów.

## Własne etapy
Użytkownik może dopisać etap po wbudowanych (np. `patron-streszczenie-dla-klienta` albo kontrolę
zgodności z wzorem kancelarii). Etap to rola i polecenie; wejściem jest wynik poprzedniego.

## Wynik
- Wersje obok oryginału: `<nazwa>.1-recenzent.md`, `<nazwa>.2-adwokat.md`,
  `<nazwa>.3-final.md` (tylko uruchomione etapy). Pusty wynik etapu nie kasuje draftu.
- Raport w czacie: dla każdego etapu 3-6 punktów, co zmieniono i dlaczego; lista kontrargumentów
  z etapu 2 z podziałem na uprzedzone w tekście i wymagające decyzji lub dowodu.
- Kontrola: `diff -u <oryginał> <nazwa>.3-final.md` (albo `git diff --no-index --word-diff`).
  Jeśli etap zmienił fakt, datę, kwotę lub sygnaturę - cofnij tę zmianę i zgłoś to.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/pipeline/defense.ts`
(ADR-0058, ADR-0074), `lib/highstakes/classifier.ts` (ADR-0004), `lib/skills/manifest.ts`.
