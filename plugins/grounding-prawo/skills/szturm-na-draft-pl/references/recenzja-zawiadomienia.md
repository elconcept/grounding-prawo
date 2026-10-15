# ZOP-R — wykonanie w szturmie

Pełny protokół, role i pytania: `shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md`.
Przeczytaj go przed przydzieleniem soczewek. Jeśli pracujesz poza pluginem i pliku brak,
stosuj poniższy samodzielny mandat; brak biblioteki nie blokuje wywiadu.

## Sekwencja i materiały

1. Ustal epizody, osoby i źródła wiedzy z relacji, odpowiedzi i draftu. Przywróć pominięcia.
2. Rozdziel przegląd na: mikro-sekwencję; rozmiar krzywdy i skutki; pozostałe osoby;
   prawa pokrzywdzonego oraz zachowanie każdego organu/funkcjonariusza; możliwe inne kwalifikacje;
   pokrycie całości w tekście. Żadna rola nie atakuje autora ani nie wymaga dowodu krzywdy.
3. Każdy recenzent dostaje relację + odpowiedzi + mapę + draft + mandat. W osobnym kontekście
   odizoluj cudze wnioski, nie te materiały. Bez subagentów wykonaj odrębne przeglądy samodzielnie.
4. Zbierz pytania, wybierz zwykle 3–6 o jednym epizodzie, zapytaj autora. Reszta pozostaje
   w mapie do kolejnych rund. Deduplikuj tylko tę samą okoliczność tej samej osoby/zdarzenia.
5. Po odpowiedzi dopisz szczegóły do mapy i tekstu, otwórz nowe gałęzie. Pytaj o konkrety:
   słowa, gesty, działania przed/w trakcie/po, reakcje i skutki. Nie sugeruj faktów, diagnoz,
   porozumienia sprawców ani przyczyny rozbieżności. Nie ponawiaj zamkniętych pytań bez nowego sygnału.
6. Zweryfikuj ewentualne dodatkowe kwalifikacje. Uchybienie procesowe/dyscyplinarne nie jest
   automatycznie przestępstwem. Niekorzystna decyzja nie dowodzi winy funkcjonariusza;
   pytaj o konkretne czynności, wiedzę, zgłoszenia i skutki. Brak przepisu nie usuwa krzywdy.
   Powiedz autorowi wprost, które opisane zachowania (także innych osób, funkcjonariuszy i organów)
   mogą być osobnym czynem lub naruszeniem jego praw, choć sam ich tak nie nazwał, i jakie pytanie
   to ustali (R4a w protokole). Przepis tylko po sprawdzeniu w t.j.; inaczej „do sprawdzenia”.
7. Domknij po odpowiedziach i podsumowaniu do korekty albo świadomej decyzji autora o zakończeniu.
   Nie ma limitu rund wywiadu. Przy braku odpowiedzi przygotuj możliwe rozszerzenia z dostępnej
   relacji i jawną listę pytań; nie wpisuj odpowiedzi za autora.

## Pytania i edycje to różne artefakty

Pytania/gałęzie zapisuj w `RUN/rozszerzenia/` według
[schemat-rozszerzenia.json](schemat-rozszerzenia.json); stan utrzymuj w istniejącej mapie krzywd.
Nie wymagaj linii draftu dla epizodu, którego w nim nie ma. Wystarczy rzeczywisty fragment
relacji, identyfikator odpowiedzi lub jawny brak kontekstu. Bez repo wybierz lokalny katalog roboczy.

Pytania NIE są wejściem `synteza.py`: brak targetu lub odpowiedzi nie może zmienić ich
w „brak dowodu — usuń”. Dopiero odpowiedź/już dostępna relacja daje gotową edycję. Gotowe
edycje można przekazać istniejącej syntezie i E7 redline, z dosłownym targetem i rzeczywistym
źródłem. Samo pytanie nie trafia do pisma jako fakt ani jako śledzona propozycja nowego zdarzenia.
Bez zmian merytorycznych E1 i techniczne E4 sprawdzają wyłącznie użyte prawo, cytaty i format.

Rejestr chroni wszystkie relacjonowane krzywdy, skutki i źródła wiedzy, także bez dokumentu;
nazwa techniczna `fakty_potwierdzone` nie oznacza zewnętrznego potwierdzenia. W `zrodlo` wpisz
rzeczywistą relację i jej lokalizację, `z_akt: false`. Nie zmieniaj przypuszczenia w obserwację.
Pole `dowod` w ustaleniu syntezy oznacza pochodzenie proponowanej edycji: może wskazywać
relację autora albo fragment bieżącego pisma zawierający przenoszoną kwotę, nie tylko załącznik.
Nigdy nie fabrykuj kotwicy. Nowa liczba wymyślona przez model pozostaje niedopuszczalna.

Wynik `synteza.py` blokuje co najwyżej konkretną nieuprawnioną edycję, nie złożenie relacji.
Komunikat „brak dowodu — uzupełnić albo usunąć twierdzenie?” nie obowiązuje w tym trybie:
nie pokazuj go jako zarzutu autorowi ani nie realizuj skreślenia. Zachowaj tekst, ustal źródło
proponowanej zmiany i ponów poprawną edycję. Odrzuć propozycję usunięcia/osłabienia z braku
dowodu przed syntezą; sam status DECYZJA_AUTORA nie czyni takiej propozycji dopuszczalną.
Po redline porównaj relację źródłową i mapę z wynikiem; przywróć straty narracji, również
te odziedziczone po wcześniejszym osłabionym drafcie. Brak repo lub `_SUBSUMPCJA_*` nie blokuje:
pracuj na dostępnej relacji i plikach, zapisując rejestr przy materiale roboczym.



## Warunek wyniku i jakość

Nie mierz sukcesu liczbą zarzutów, skreśleń lub stron. Sprawdź pokrycie wszystkich epizodów,
osób, skutków oraz adekwatnych gałęzi instytucjonalnych i prawnych. Nie skracaj powtarzalnych
zachowań do jednej ogólnej etykiety, jeśli poszczególne zdarzenia mają odrębne znaczenie.
Raportuj, które role wykonano i jakie pytania/uzupełnienia wniosły; „nie dotyczy” wymaga
krótkiej podstawy. Puste wyniki jednej soczewki nie dowodzą kompletności całego zawiadomienia.

Wynik dla autora: rozszerzone pismo lub fragmenty zgodnie ze zleceniem; co przywrócono i dodano
z odpowiedzi; następna krótka seria pytań; lista możliwych dodatkowych czynów i naruszeń praw
pokrzywdzonego (R4a); otwarte kwalifikacje i formalności poza pismem.
Pytania o pilne bezpieczeństwo mają pierwszeństwo, bez konfrontacji w celu zdobycia dowodu.
