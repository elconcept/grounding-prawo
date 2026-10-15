# Test integracji zawiadomienia — wygenerowany plugin

Data: 2026-10-15. Katalog: `/workspace/synoprojects/grounding-prawo/plugins/grounding-prawo/skills`.

Zakres: rzeczywiste odpowiedzi tekstowe czterech zleconych prób, bez generowania DOCX, bez sieci i weryfikacji prawa, bez uruchamiania pełnego panelu recenzentów i skryptu syntezy. Test wykonuje ten sam niezależny agent, który zna wcześniejsze problemy i wprowadzone poprawki; nie jest to świeży ślepy runner. Oczekiwania i cel prób były podane w zleceniu. Nie edytowano repo.

Odczytano router i ZOP, następnie HYBRID, FAKTY, CLAIM, FSL oraz profil postępowań własnych — bramki celowo po ZOP. Odczytano wspólny kontrakt, wyjątki szturmu/ataku/adversarial i ich niższe, sprzeczne mandaty. Wcześniej odczytano audyt INBOX, patch 06 i źródła integracji; dostępne referencje ZOP poznano w poprzednim przebiegu. Dla kontroli routingu sprawdzono istnienie modułu zażalenia w `pisma-procesowe-v3/modules/typy/` i wejście skilla procesowego. Odczyty zbyt długie, które narzędzie skróciło, uzupełniono w zakresie potrzebnych wyjątków i konfliktowych reguł; nie deklaruję pełnego przejścia całego korpusu.

## 1. Szybki draft do DOCX, bramki wczytane po ZOP

### Wejście

„Przygotuj szybki draft do DOCX. Policjant wykręcił mi rękę, czułam ból i bałam się. W notatce twierdzi, że sam upadłam. Nie mam obdukcji ani nagrania. W pierwszym protokole nie opisałam bólu. Nie umiem wyjaśnić pominięcia. Nie żądam recenzji.”

### Faktyczna odpowiedź

⬛ [UZUPEŁNIJ: miejscowość i data pisma]
⬛ [UZUPEŁNIJ: imię, nazwisko i bezpieczne dane do korespondencji]
Do: ⬛ [UZUPEŁNIJ: nazwa i adres organu]
⬛ [UZUPEŁNIJ: sygnatura, jeżeli istnieje i jest znana]

**Zawiadomienie o popełnieniu przestępstwa**

Zawiadamiam o popełnieniu na moją szkodę przestępstwa polegającego na wykręceniu mi ręki przez policjanta i wnoszę o wszczęcie postępowania. Wnoszę o ściganie sprawcy opisanego czynu.

Policjant wykręcił mi rękę. Czułam ból i bałam się.

W notatce policjant twierdzi, że sama upadłam. Moja relacja o jego działaniu jest następująca: wykręcił mi rękę. W pierwszym protokole nie opisałam bólu. Teraz go opisuję. Nie umiem wyjaśnić wcześniejszego pominięcia.

Chcę brać udział w postępowaniu jako osoba pokrzywdzona.

⬛ [podpis]

---

**Status:** szybki draft; HARDGATE-A: DO DOPYTANIA. Wywiad nie został zakończony. Brakuje daty i miejsca zdarzenia, danych pozwalających ustalić policjanta, przebiegu przed wykręceniem ręki i po nim oraz czasu trwania bólu. Dane formalne pozostają do uzupełnienia; nie jest to jeszcze plik w pełni gotowy do podpisania i złożenia.

**AUDYT-B: częściowy.** Informacje o notatce i pierwszym protokole pochodzą z Twojej wiadomości; nie odczytano dokumentów. Zachowano treść notatki w opisie, a nie jako zweryfikowany cytat. Pominięcie bólu w pierwszym protokole nazwano bez wymyślania przyczyny. Nie dopisałam, że do upadku w ogóle nie doszło — Twoja wiadomość tego wprost nie rozstrzyga.

**Tropy dla organu:** wskazana notatka i pierwszy protokół, których dat i oznaczeń jeszcze nie podano. Nie masz obdukcji ani nagrania; nie trzeba ich dostarczać, by zachować opis bólu i strachu.

Najważniejsze kwestie do późniejszego uzupełnienia: kiedy i gdzie to się wydarzyło, co dokładnie policjant robił przed wykręceniem ręki i po nim, jak wyglądała sytuacja opisana w notatce jako upadek oraz jak długo bolała ręka. Czy jesteś teraz bezpieczna i czy nadal potrzebujesz pomocy medycznej?

Nie uruchamiam recenzji. W tej wersji nie podaję kwalifikacji, artykułów ani terminów bez ich sprawdzenia. Przed złożeniem uzupełnij nagłówek, datę i podpis oraz sprawdź właściwy sposób złożenia. Zachowaj kopię i poproś o potwierdzenie przyjęcia.

### Ścieżka i ocena

Router → wyjątek ZOP → szybki draft z jawnymi lukami → kontrola integralności/AUDYT-B. Żądanie DOCX nie włączyło HYBRID BLOCK ZERO ani ścieżki procesowej. Późniejszy odczyt FAKTY/CLAIM/FSL i profilu nie zamienił relacji na „według twierdzeń” lub „rzekomo”. Brak obdukcji/nagrania nie został sklasyfikowany jako czerwony lub żółty błąd. Ból i strach pozostały w piśmie. Nie wyjaśniono pominięcia traumą lub pomyłką policjanta. Nie włączono szturmu bez żądania. Odróżniono relację o dokumencie od odczytanego cytatu. Poprawiono oczywistą niezgodność rodzaju „sam upadłam” do „sama upadłam” w parafrazie, bez twierdzenia o dosłownym cytacie.

Ograniczenie: tekst nie dopisuje stanowczego zaprzeczenia upadkowi, bo opis wykręcania ręki sam w sobie nie wyklucza upadku. To zachowanie wierności, nie nadanie pierwszeństwa notatce. Brak rzeczywistego DOCX zgodny z zakresem testu; eksport i zachowanie treści po konwersji pozostają NOT_CHECKED.

## 2. Jawna recenzja, przywrócenie relacji i 500 zł

### Wejście

Relacja: „Policjant wykręcił rękę, bolało, boję się. Zapłaciłam 500 zł za leczenie; nie mam rachunku”.
Osłabiony draft: „Mogło dojść do kontaktu. Brak udokumentowanej szkody”.
Żądanie: przywrócić wszystkie krzywdy, przenieść 500 zł do akapitu skutków. Komentarz syntezy: „Brak dowodu/źródła — uzupełnić albo usunąć?”.

### Faktyczna odpowiedź

**Co się wydarzyło**

Policjant wykręcił mi rękę.

**Skutki**

Czułam ból. Boję się. Za leczenie zapłaciłam 500 zł.

---

Przywróciłam konkretne działanie policjanta, ból, trwający strach i koszt leczenia z Twojej relacji. Kwota 500 zł jest teraz w akapicie skutków. Brak rachunku pozostaje informacją o dostępnych materiałach; nie usuwa kosztu z opisu.

Komentarz syntezy nie uzasadnia usunięcia tych zdań. Źródłem zmiany jest przytoczona relacja autorki, w szczególności zdanie „Zapłaciłam 500 zł za leczenie”, a nie nieistniejący rachunek. Takie pochodzenie należy zapisać przy proponowanej edycji. Nie oznaczam kwoty jako ustalonej na podstawie akt.

Do rozszerzenia pozostają czas i miejsce zdarzenia, przebieg wykręcania ręki, czas trwania bólu oraz rodzaj i termin leczenia. Nie dopisuję diagnozy ani nie twierdzę, że koszt jest potwierdzony dokumentem.

### Ścieżka i ocena

Jawnie żądana recenzja → mandat ochrony pełnej relacji dla wszystkich ról → porównanie ze źródłową relacją, nie wyłącznie z osłabionym draftem → odrzucenie nieuprawnionego skreślenia → korekta fragmentu.

Zachowano cztery elementy: wykręcenie ręki, ból, strach, 500 zł. Nie pozostawiono „mogło dojść” ani „brak udokumentowanej szkody” w zastępstwie relacji. Kwota nie została uznana za nowy domysł modelu. Brak rachunku nie stał się warunkiem dalszej pracy. Sama treść nie wiąże wydatku z konkretną diagnozą ani rodzajem zabiegu.

Nie uruchomiono skryptu syntezy i redline; sprawdzono reakcję na dostarczony komunikat oraz tekst wynikowy. Twarda ochrona kodowa, liczbowe bramki skryptu i przekazanie mandatu faktycznym izolowanym subagentom pozostają NOT_CHECKED, nie PASS.

## 3. Kontrola routingu zażalenia

### Wejście

„Chcę zażalenie na odmowę wszczęcia”.

### Faktyczna odpowiedź

Przygotuję zażalenie na odmowę wszczęcia. Potrzebuję treści postanowienia wraz z uzasadnieniem i pouczeniem oraz daty i sposobu jego doręczenia. Napisz też, z czym się nie zgadzasz i co, Twoim zdaniem, pominięto.

Najpierw ustalę właściwy tryb i termin na podstawie tych danych i aktualnych przepisów. Nie będę zakładać terminu ani treści uzasadnienia z pamięci.

### Ścieżka i ocena

Router [3] → `pisma-procesowe-v3` → `pisma-procesowe-v3/modules/typy/zazalenie-na-postanowienie-prokuratora.md`. Wyjątek ZOP nie przenosi się na nowy dokument. Odczyt literalnej ścieżki samodzielnego skilla zażalenia zwrócił brak pliku, ale routing pluginu jawnie scala go w module typów; znaleziono ten moduł i nie potraktowano braku dawnej ścieżki jako blokera.

Test dotyczy wyłącznie wyboru ścieżki i wstępnej odpowiedzi, nie zakończenia zażalenia ani zgodności całego pipeline’u. Nie odczytano i nie wykonano wszystkich procesowych bramek, ponieważ nie zlecono realnej sprawy ani nie dostarczono postanowienia. Wyjątek nie posłużył do deklaracji, że zażalenie może pominąć swoją kontrolę prawa/terminu/dokumentu.

## 4. Niejasne autorstwo cytatu i nieznana data relacji

### Wejście

„Napisz dziś szybki draft na podstawie cytatu: «Wczoraj sąsiad kopnął moje auto i wgniótł drzwi». Nie wiadomo, kiedy napisano tę wiadomość ani kto jest jej autorem.”

### Faktyczna odpowiedź

**Fragment roboczy — źródło i osoba zgłaszająca do ustalenia**

W przekazanym materiale znajduje się relacja [autor i źródło do ustalenia]: „Wczoraj sąsiad kopnął moje auto i wgniótł drzwi” [data pierwotnej wiadomości nieznana; data zdarzenia do ustalenia].

Nie wiadomo jeszcze, czy jest to własna relacja osoby składającej zawiadomienie, czy informacja od kogoś innego. Przed przekształceniem jej w osobiste zawiadomienie trzeba ustalić autora oraz to, kto składa pismo i w czyim imieniu. „Wczoraj” nie zostało przeliczone względem dzisiejszej daty redakcji.

### Ścieżka i ocena

F0 zastosowano przed przejściem na pierwszą osobę. Nie przypisano samochodu rozmówcy, nie wybrano rodzaju gramatycznego, nie dodano wniosku o ściganie jako pochodzącego od nieustalonego pokrzywdzonego. Znacznik autora i kotwicy daty znajduje się przy cytacie, a nie tylko poza pismem. Wynik jawnie nazwano fragmentem roboczym. Problem wcześniejszego retestu autorstwa nie wystąpił.

## Wynik integracji i materialne luki

W tych czterech przebiegach nie ujawniła się materialna luka integracji narracyjnej. Wyjątki przetrwały odczyt późniejszych sprzecznych bramek. Nie zablokowano draftu z braku dokumentów, nie zredukowano krzywd, nie zastąpiono przeżycia notatką i nie uruchomiono automatycznej recenzji. Kontrola prawa i rzeczywistych cytatów pozostała odrębna. Zażalenie wróciło do zwykłego routingu.

W audycie statycznym pozostają niższe mandaty w referencjach soczewek („kategoryczne bez dowodu”, „akta rozstrzygają”, oskarżyciel publiczny jako przeciwnik). Nowy wyjątek je nadpisuje i wymaga przekazania ochrony każdej roli. Nie stwierdzam ich skutecznej kolizji w tych tekstowych próbach. Ponieważ nie uruchamiano osobnych recenzentów, odporność rzeczywistej delegacji na zgubienie wyjątku pozostaje nieprzetestowana.

Nie przeprowadzano walidacji sankcji i znamion z A1 audytu, napraw technicznych DOCX/adeu z A4–A5 ani mechanicznego retestu A6. Ten raport nie jest potwierdzeniem naprawy całego audytu INBOX.

## Uzupełnienie walidacji przez agenta głównego

Poza powyższą próbą tekstową uruchomiono rzeczywistą funkcję `bramki` z
`szturm-na-draft-pl/scripts/synteza.py` na dwóch wejściach:
- 500 zł w akapicie skutków, z pochodzeniem „Relacja autora, akapit 1: Zapłaciłam 500 zł za leczenie.” → `WPROWADZONE`;
- identyczna nowa kwota bez źródła → `ZABLOKOWANE`.

Pełne wejścia i wyniki: [20261015-synteza-adapter.json](20261015-synteza-adapter.json).
To potwierdza działanie opisanego adaptera źródła, nie zmianę ogólnej logiki skryptu ani
naprawę wszystkich przypadków A6. Nie uruchamiano konwersji DOCX ani adeu.

Walidacja strukturalna: quick_validate dla źródła i wygenerowanej kopii skilla, validate_plugin
całego pluginu, poprawność linków lokalnych i JSON scenariuszy oraz zastosowanie patchy
repo w odizolowanym katalogu build. Zmiany źródłowe utrwalono w own-skills, overlay i patchach;
manifest i marketplace nie były zmieniane w ramach tego refaktoru.
