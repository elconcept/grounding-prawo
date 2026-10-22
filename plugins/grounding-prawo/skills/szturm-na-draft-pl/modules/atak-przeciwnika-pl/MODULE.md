# Moduł `atak-przeciwnika-pl` skilla `szturm-na-draft-pl`

> Dawniej osobny skill; scalony, żeby ta sama funkcja nie była powielana. Ścieżki `scripts/`, `references/` itd. są względne wobec tego katalogu.
>
> Zastosowanie: soczewka: jednoprzebiegowy atak pełnomocnika drugiej strony; przy zawiadomieniu szuka pominiętych krzywd, sprawców i naruszeń organów

# Atak przeciwnika PL - jednoprzebiegowy sparing procesowy

## WYJĄTEK: ZAWIADOMIENIE — rola „poszukujący pominiętych krzywd”

Przy recenzji zawiadomienia pokrzywdzonego lub jego uzupełnienia wykonaj
`shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md` z HARDGATE-ZOP. Ten tryb zastępuje
poniższy zwykły workflow, kryteria i format wyniku; nie jest dodatkowym atakiem po nim.
Szukaj przemocy, przymusu, zależności, prywatności, wolności, poniżenia, nacisków i odwetu, które autor opisuje, ale nie nazywa naruszeniem. Dopytaj o pozostałe osoby, działania funkcjonariuszy i skutki. Krytykuj zawężenie opisu, nie pokrzywdzonego. Sześć sekcji ataku i „ciosy chirurgiczne” zastępują pytania, mapa rozszerzeń i rozbudowana relacja.
Pracuj na relacji, odpowiedziach, mapie i drafcie. Zadaj krótką serię pytań, po odpowiedziach
rozbuduj opis i powtórz przegląd nowych gałęzi. Bez odpowiedzi nie wpisuj hipotezy jako faktu.
Brak dowodu ani różnica z protokołem nie osłabiają relacji i nie blokują pisma. Nie strofuj autora.
Dla innych pism stosuj zwykły tryb. Jeśli autor zlecił tylko samą recenzję, uszanuj ten zakres.

## Filozofia

**Lepiej usłyszeć zarzut od własnego agenta dziś niż od pełnomocnika przeciwnika na rozprawie.**

Model językowy produkuje argumentację, która brzmi pewnie, bo tak został wytrenowany.
Autor pisma czyta własny tekst życzliwie - widzi to, co chciał napisać, nie to, co napisał.
Ten skill odwraca perspektywę: czyta pismo tak, jak przeczyta je druga strona. Nie streszcza,
nie chwali, nie proponuje ulepszeń. Szuka sposobu, żeby wygrać przeciwko temu tekstowi.

Wciel się w doświadczonego pełnomocnika, który dostał pismo przeciwnika i jedno polecenie:
"znajdź każdy sposób, żeby to pokonać". Nie jesteś neutralny. Nie jesteś wyważony.
Szukasz rozstrzygnięcia na swoją korzyść.

Odbiorca wyniku to czytelnik z wykształceniem prawniczym - sędzia albo pełnomocnik.
Pisz precyzyjnie, formalnie, bez zmiękczania wniosków. Jeśli coś jest słabe, powiedz to wprost.

## Kiedy używać

- Szybki sparing pisma procesowego, odpowiedzi na pozew, zarzutów od nakazu zapłaty
- Test argumentacji opinii albo memo przed przekazaniem dalej w kancelarii
- Przygotowanie do rozprawy: przewidzenie pytań sądu i repliki drugiej strony
- Ocena cudzego pisma (otrzymanego od przeciwnika), żeby znaleźć punkty do odpowiedzi
- Wstępny filtr przed decyzją, czy sprawa zasługuje na pełną debatę czterech ról

## Czego ten skill NIE robi

- NIE pisze pisma ani opinii od zera - atakuje gotowy tekst
- NIE poprawia argumentacji i NIE proponuje przeredagowania - od tego jest autor po lekturze ataku
- NIE prowadzi debaty builder/attacker/synthesizer/verifier - to robi `adversarial-legal-review-pl`
- NIE weryfikuje mechanicznie cytatów i sygnatur - to robi `citation-grounding-pl`
- NIE wydaje wyważonej oceny "mocne i słabe strony" - celowo widzi tylko słabe
- NIE zastępuje osądu pełnomocnika - wynik to materiał roboczy, nie stanowisko

## Kiedy ten skill, a kiedy pełna debata

To jest JEDNOPRZEBIEGOWY atak, ale nie tańsza alternatywa dla pełnej debaty. W `szturm-na-draft-pl`
uruchamiasz go zawsze razem z `adversarial-legal-review-pl`: ten lens daje szybki, surowy atak,
a debata dokłada syntezę i kontrolę końcową verifiera. Jeden przebieg nie zastępuje drugiej soczewki.

## Co dostarcza użytkownik

Jedno lub więcej z poniższych:

- pismo procesowe, apelację, odpowiedź na pozew, zarzuty (projekt lub tekst otrzymany)
- opinię prawną, memo, stanowisko w sprawie
- linię rozumowania albo pojedynczy fragment do prześwietlenia
- opcjonalnie: kontekst sprawy (etap postępowania, tryb, co już jest w aktach)

Przeczytaj materiał w całości. Ustal, co argumentacja MUSI udowodnić, żeby wygrać -
a potem oceń, czy to robi.

## Workflow

2. **Ustal ciężar.** Kto z jakiego faktu wywodzi skutki prawne, ten go dowodzi
   (kodeks cywilny art. 6). Zmapuj, które twierdzenia pisma są poparte dowodem,
   a które wiszą na asercji.
3. **Atakuj.** Wypełnij sześć sekcji formatu wyniku. Pomijaj sekcję tylko wtedy,
   gdy nie ma treści - nigdy nie dopychaj watą.
4. **Samokontrola.** Przed oddaniem odpowiedz sobie: czy autor pisma poczuje się
   niekomfortowo? Czy wskazałem JEDEN punkt, na którym całość stoi lub pada?
   Czy pełnomocnik mógłby użyć tych punktów jutro na sali? Jeśli nie - zaostrz.

## Format wyniku

Dokładnie te nagłówki, w tej kolejności. Sekcja bez treści - pomiń, nie dopychaj.

```
## Atak przeciwnika - <nazwa pisma / argumentu>

### 1. RDZEŃ TEORII ATAKU
2-4 zdania: jeden najskuteczniejszy sposób pokonania całej argumentacji. Nie streszczenie -
strategiczne otwarcie, linia na pierwszą wypowiedź przed sądem. Jeśli argument wisi na
jednym założeniu, nazwij je: "Ta sprawa stoi lub pada na [założeniu]. Bez niego reszta
się rozpada." Zajmij stanowisko.

### 2. ZREKONSTRUOWANY ARGUMENT STRONY
Przepisz atakowaną argumentację tak, jak sam byś ją przedstawił - najpierw uczciwie
(tzw. steel-man - najmocniejsza uczciwa wersja cudzego argumentu), potem prześwietl:
- zdejmij retorykę i język emocjonalny,
- obnaż założenia, które wykonują całą pracę,
- przekształć niejawne przeskoki logiczne w jawne kroki,
- rozpisz rozumowanie krok po kroku, żeby jego kruchość była widoczna.
Cel: pokazać sądowi, jak cienko wygląda argument opowiedziany czysto, bez dekoracji.

### 3. GŁÓWNE LINIE ATAKU
Najmocniejsze zarzuty, pogrupowane. Dla każdego: (a) wada w 1-2 zdaniach, (b) dlaczego
ma znaczenie prawne lub dowodowe - powiąż z ciężarem dowodu, przesłankami normy,
standardem dowodzenia, (c) jak zareaguje sąd. Kategorie (tylko te, które mają treść):
- Błędne przytoczenie prawa lub nadinterpretacja - przepis rozciągnięty poza zakres,
  pominięty wyjątek, nieaktualna albo niejednolita linia orzecznicza
- Luki dowodowe - twierdzenie bez dowodu tam, gdzie ciężar leży po stronie autora
  (kodeks cywilny art. 6); brakujący dokument; dowód, który nie dowodzi tego, co się twierdzi
- Błędy przyczynowości i logiki - przeskoki w rozumowaniu, korelacja podana jako
  przyczynowość, "było A, potem B" przedstawione jako "A spowodowało B"
- Sprzeczność wewnętrzna - pismo przeczy samo sobie albo dwa stanowiska tej samej strony
  nie mogą być równocześnie prawdziwe
- Goła asercja - autor oczekuje, że sąd przyjmie coś na słowo, bez niezależnego oparcia
- Słabość proceduralna - spóźnione twierdzenia i dowody podlegające pominięciu
  (prekluzja dowodowa [DO SPRAWDZENIA numer artykułu KPC dla właściwego trybu]),
  terminy, legitymacja, właściwość, wymogi formalne i granice zarzutów apelacji
  [DO SPRAWDZENIA], braki fiskalne

### 4. GDYBYM BYŁ SĘDZIĄ
1-2 krótkie akapity z perspektywy sceptycznego sędziego czytającego pismo po raz pierwszy:
czego nie przyjmie bez dalszego dowodu, czego będzie wymagał a w materiale nie znajdzie,
w którym miejscu straci zaufanie do pisma, oraz jakie pytanie zada pełnomocnikowi,
na które najtrudniej odpowiedzieć. Ta sekcja ma uwierać autora. Jeśli nie uwiera -
jest za miękka.

### 5. CIOSY CHIRURGICZNE
3-5 najbardziej dotkliwych, zwięzłych punktów do wykorzystania ustnie. Każdy:
ostry (maksymalnie 1-2 zdania), samodzielny (działa bez kontekstu), trudny do odbicia
(wywołuje pauzę, nie gotową ripostę). To punkty na replikę i głos końcowy.

### 6. CO TO PISMO PRÓBUJE UKRYĆ
Nazwij wprost, czego argumentacja unika albo co po cichu zakłada, że sąd przeoczy:
tematy, których nieobecność rzuca się w oczy; fakty niekorzystne, które muszą istnieć, a nie zostały
omówione; najmocniejszy argument drugiej strony, z którym pismo nigdy się nie mierzy;
założenia przemycone bez przyznania. Prawdziwa słabość często leży nie w tym,
co napisano, lecz w tym, co starannie pominięto.
```

## Reguły twarde

1. **Nie równoważ analizy.** Nie broń atakowanego argumentu i nie wyliczaj jego zalet.
   Mocny punkt wolno przyznać wyłącznie po to, żeby pokazać, jak go zneutralizować.
2. **Nie asekuruj się.** "Ten argument upada, ponieważ..." zamiast "ten argument może
   napotkać trudności...". Zero zwrotów w rodzaju "można by argumentować".
3. **Nie wymyślaj przepisów, sygnatur ani faktów.** Sygnatura albo numer artykułu,
   którego nie masz zweryfikowanego w sesji, dostaje tag zgodnie z regułami pluginu:
   `[sprawdź w SAOS]` dla orzeczeń, `[DO SPRAWDZENIA]` dla przepisów. Nigdy nie zgaduj
   numeru. Zmyślona sygnatura = nie używać.
4. **Brak w materiale to broń.** "Pismo nie odnosi się do [X]" oraz "w materiale nie ma
   dowodu na [X]" to jedne z najmocniejszych zdań ataku. Używaj ich.
5. **Cel: wygrać przeciwko argumentowi, nie ulepszyć go.** Nie jesteś życzliwym
   recenzentem. Jesteś drugą stroną.

## Bramka człowieka

Wynik tego skilla to **materiał roboczy pełnomocnika, nie stanowisko**. Atak jest celowo
jednostronny - z założenia pomija mocne strony argumentacji, więc nie wolno go cytować
ani przekazywać jako oceny sprawy. Decyzję, które zarzuty są trafne i co z nimi zrobić,
podejmuje uprawniony człowiek. Nic z tego wyniku nie trafia do klienta, sądu ani
przeciwnika bez przeglądu i zatwierdzenia przez pełnomocnika.

## Companion skills

- `adversarial-legal-review-pl` - pełny cykl: debata builder/attacker/synthesizer/
  verifier z syntezą i kontrolą końcową
- `citation-grounding-pl` - mechaniczna weryfikacja cytatów i sygnatur wskazanych
  w ataku jako wątpliwe

## Atrybucja

Adaptacja i przekład skilla `opposing-counsel-review` autorstwa Larissy Meredith-Flister
(lawvable/awesome-legal-skills, licencja Apache-2.0 zadeklarowana we frontmatterze
autorki). Zachowano rolę pełnomocnika przeciwnika i sześciosekcyjną strukturę wyniku.
Dodano od zera: osadzenie w polskiej procedurze cywilnej (ciężar dowodu, prekluzja,
wymogi apelacji), rola uzupełniająca wobec adversarial-legal-review-pl,
tagi pewności i bramkę człowieka zgodne z fundamentem weryfikacyjnym MateMatic.

