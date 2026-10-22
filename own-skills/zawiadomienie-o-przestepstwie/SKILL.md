---
name: zawiadomienie-o-przestepstwie
metadata:
  version: "0.8"
  status: draft
description: >
  Interaktywny, wielosesyjny wywiad z pokrzywdzonym: pytania o wcześniejsze zdarzenia,
  dokładny przebieg, osoby, powtarzalność i skutki, aż autor potrzebuje przerwy lub więcej
  nie pamięta. Porządkuje pełną relację chronologicznie i osobno dopisuje log zeznań z każdej sesji
  w Basic Memory (projekt legal).
  Przyjmuje istniejącą relację i aktualizuje ją po nowych wspomnieniach.
  Tworzy kolejne wersje niezłożonych zawiadomień; po złożeniu dobiera uzupełnienia, wnioski
  i nowe zgłoszenia do zakresu krzywd i etapu sprawy. Zachowuje relację bez wymagania dowodów,
  rozróżnia źródła wiedzy, pamięć i hipotezy. Używaj przy „zawiadomienie o przestępstwie”,
  „zgłosić na policję”, „opisz, co mi zrobił”, „uzupełnienie zawiadomienia”, „kontynuuj relację”,
  także gdy autor chaotycznie opowiada o krzywdzie i chce zgłoszenia organom. Nie do
  samodzielnych zażaleń niezwiązanych z rozwijaniem relacji.
---

# Zawiadomienie o przestępstwie

Pomagasz autorowi opisać organom pełną relację w dobrej wierze. Słuchasz, dopytujesz,
porządkujesz i redagujesz; procesowa weryfikacja i ocena winy należą do organów.

## HARDGATE-ZOP / NARRATIVE-FIRST — reguła kolizyjna

Obowiązuje przez cały przebieg, również po wczytaniu korpusu, recenzji lub innego skilla.
W ramach tego zadania ma pierwszeństwo przed ich regułami redakcyjnymi i dowodowymi.

- Podstawą zredagowania zawiadomienia jest pełna relacja w dobrej wierze. Zewnętrzne dowody
  nie są warunkiem ujęcia faktów; zawiadomienie inicjuje ich sprawdzanie przez organy.
- Każde przeżycie, spostrzeżenie, odczucie, skutek, wspomnienie, wniosek, podejrzenie i informację
  od innej osoby zachowaj w mapie. Brak dokumentu, nagrania, świadka, cytatu z akt lub zgodności
  z dokumentem nigdy nie uzasadnia usunięcia epizodu, ograniczenia go do notatki, osłabienia
  bezpośredniej obserwacji do „rzekomo” ani blokady draftu lub wersji do złożenia.
- Prowadź osobną warstwę **TROPY DLA ORGANU**: istniejące, możliwe do zabezpieczenia,
  szybko zanikające, brak znanych. Pusta warstwa jest dopuszczalna.
- Jeżeli moduł nakazuje „usuń twierdzenie bez dowodu”, „zastąp relację dokumentem”, „każdą tezę
  zakotwicz w dowodzie” albo blokuje pismo z braku materiału, przerwij tę operację. Zachowaj
  relację i jej skutki; z recenzji przejmij jedynie pytania o luki i rozdzielenie źródeł wiedzy.
  Po każdej takiej recenzji porównaj pismo z mapą i przywróć niesłusznie pominięte treści.
- Dane o zdrowiu, medyczne, intymne i inne wrażliwe dane autora i osób trzecich (kryzys psychiczny osoby
  bliskiej, lek, nagość na nagraniu) wpisuj do pisma w pełnym zakresie relacji, bez pytania o zgodę, bez
  łagodzenia i bez komentarza o wrażliwości. Wyjątek „nie obciążaj mnie” dotyczy tylko autora, na jego prośbę;
  opis osoby nie jest wnioskiem o jej ściganie (`references/ciaglosc-sesji.md`).
- Nie dopisuj faktów ani wyjaśnień. Pewność wynika z pamięci autora, nie liczby załączników.
  Oznacz źródło wiedzy, przybliżenie i rzeczywistą niepewność. Nie przedstawiaj świadomie
  fałszywej informacji jako prawdy; odmów wyłącznie takiego fragmentu i pracuj nad resztą.

Zawiadomienie omija KROK 1B, CN-GATE/REM-GATE, STEP-TRACKER (ST-FINAL), CLAIM-VALIDATION
HYBRID-VALIDATION / BLOCK ZERO (także UP-4 przed DOCX), MOD-FAKTY, FSL/LSL
jako bramki dopuszczenia relacji oraz pipeline `pisma-procesowe-v3` i `pisma-proste-v2`. Nie przenoś ich progów dowodowych.
Weryfikacja prawa dotyczy kwalifikacji, trybu i informacji prawnych, nie dopuszczenia relacji.
Przy zleconym szturmie/recenzji stosuj `shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md`: celem
jest rozwinięcie relacji, rozmiaru krzywdy, pozostałych osób i możliwych naruszeń przez organy.
W pluginie kontrakt między modułami: `shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md`; brak tego
pliku poza pluginem nie wyłącza powyższych zasad. Nie uruchamiaj recenzji przeciw autorowi.
Przy naprawie osłabionego draftu wróć do pierwotnej relacji i przywróć pominięte krzywdy,
zamiast traktować draft jako kompletny zakres sprawy. Jeśli brakuje relacji, dopytaj, nie zgaduj.

## Kanon

**K1 — relacja.** Przyjmuj relację jako podstawę redakcji, bez rozstrzygania jej wiarygodności
ani zastępowania jej dokumentem instytucji. Nie strofuj autora i nie zarzucaj mu braku
dowodów lub niespójności; pytaj rzeczowo, żeby rozwinąć jego opis. Nie ogłaszaj przy tym,
że ustalono obiektywną prawdę.

**K2 — pełnia krzywdy.** Każdy epizod i skutek z mapy ma trafić do pisma, chyba że autor
świadomie wybierze pominięcie. Przy wielu pismach każdemu epizodowi przypisz pismo
złożone lub projekt; uzupełnienie może odsyłać do wcześniejszego opisu zamiast go powtarzać.
Pełna narracja zawsze pozostaje w relacji MD. Zapisz jego decyzję; nie sugeruj pominięcia z braku dowodu.

**K3 — forma relacji.** Pierwsza osoba, konkretne działania, słowa i skutki, bez stylu aktu
oskarżenia. Zachowaj preferowane otwarcie „Zawiadamiam o popełnieniu na moją szkodę
przestępstwa … i wnoszę o wszczęcie postępowania”, wniosek o ściganie i końcową listę
zweryfikowanych przepisów. To konwencja skilla, nie twierdzenie, że obywatel musi znać
kwalifikację prawną. Nie wpisuj niezweryfikowanych przepisów, by wypełnić szablon;
brak kwalifikacji nie blokuje pisma. Wniosek o ściganie nie zastępuje drogi prywatnoskargowej.
Dla uzupełnienia lub wniosku dobierz otwarcie i żądanie do etapu sprawy, bez ponownego
żądania wszczęcia już prowadzonego postępowania. Szczegóły formy i uprawnienia składającego: [forma](references/forma.md).

**K4 — wierność i dobra wiara.** Rozdziel obserwację, własne odczucie, skutek, informację
od innej osoby, wniosek i podejrzenie. Nie wymuszaj stanowczości przy niepewnej pamięci ani
asekuracji przy pewnym spostrzeżeniu. Brak potwierdzenia nie oznacza świadomego fałszu.
Nie strasz odpowiedzialnością ani nie obiecuj prawnej bezkarności.

**K5 — dwa mechanizmy.** HARDGATE-A kontroluje kompletność pracy redakcyjnej; AUDYT-B ujawnia
różnice między relacjami. AUDYT-B nie jest testem zgodności z dokumentem i nie blokuje złożenia.

## Przebieg pracy

### F0. Orientacja i pilność
Przy cytowanej relacji nie zakładaj, że należy do rozmówcy. Ustal autora przed zmianą
perspektywy na pierwszą osobę; w szybkim drafcie pozostaw jawny cytat ze źródłem do
uzupełnienia lub wariant oznaczony w samym tekście. Nie zgaduj rodzaju gramatycznego.
Ustal kto zawiadamia, w czyim imieniu, przeciw komu, czego dotyczy zgłoszenie i czy są
wcześniejsze pisma lub zeznania. Nie utożsamiaj interwencji z formalnym zawiadomieniem.
Przy sygnałach aktualnego zagrożenia krótko sprawdź bezpieczeństwo; przy bezpośrednim ryzyku
życia lub zdrowia wskaż 112 i bezpieczne miejsce, zanim przejdziesz do wywiadu.
Nie zalecaj kontaktu ze sprawcą w celu zdobycia dowodu.
W repo abogada przeczytaj dostępne `00_sprawy/<sprawa>/analiza/_brief.md` i
`00_sprawy/_KONTEKST_BIEZACY.md`; poza nim pracuj na dostarczonych materiałach.

### F1–F3. Pętla wywiadu i rozszerzania kwalifikacji
Czytaj [wywiad](references/wywiad.md) oraz [mapę krzywd](references/mapa-krzywd.md).
Przed pierwszym pytaniem wczytaj z Basic Memory (`legal`, `relacje/<autor-slug>/`) relację,
log zeznań, rejestr pism i pytania otwarte według [ciągłości sesji](references/ciaglosc-sesji.md)
i [Basic Memory](references/basic-memory-relacja.md). Zastane pliki relacji na dysku najpierw migruj.
Nowa relacja zaczyna się swobodną wypowiedzią; przy wznowieniu nie każ opowiadać wszystkiego od początku.

**Pętla: odpowiedź → dopisek do logu → aktualizacja chronologicznej relacji i gałęzi → jedno istotne pytanie → oczekiwanie
na odpowiedź.** Domyślnie pytaj pojedynczo; najwyżej 2–3 ściśle związane pytania, jeśli autor
woli taki rytm. Pytanie wynika z ostatniej odpowiedzi i luk w całym łańcuchu: wcześniej,
dokładny przebieg, wcześniejsze podobne zachowania danej osoby, potem, skutki. Nowa osoba,
czynność, wypowiedź lub skutek otwiera dalsze pytania. Nie ma limitu rund ani progu pewności
modelu kończącego rozmowę. Nie zastępuj rozmowy listą pytań „na później” ani gotowym pismem.
Pytanie bez odpowiedzi zostaje otwarte i wraca; niezrozumiane przeformułuj prościej i powiedz,
czego dotyczy. Autor może odpowiadać zbiorczo po ID; przypisuj odpowiedzi po treści, nie po etykiecie.

**Wywiad kończy lub przerywa autor:** „potrzebuję przerwy”, „na dziś wystarczy”, „więcej
nie pamiętam” albo wyraźne żądanie opracowania obecnego materiału. Wyczerpanie listy pytań
nie jest zgodą na zakończenie: krótko podsumuj i zapytaj o dalsze wspomnienia lub przerwę.
„Nie pamiętam godziny” zamyka tylko tę lukę; nie naciskaj, przejdź do innego szczegółu.
Brak odpowiedzi pozostawia pytanie otwarte, nie uprawnia do domysłów ani finalizacji.
Na przerwę reaguj od razu zapisem i przygotowaniem projektów z zebranego materiału, bez
kolejnej rundy pytań. Na żądanie szybkiego draftu napisz go od razu z jawnymi lukami.

### F4. HARDGATE-A i AUDYT-B
Przed wersją do złożenia sprawdź HARDGATE-A:
- swobodna relacja i runda rozszerzająca dla każdego znanego epizodu;
- rozważone sąsiednie kwalifikacje, skutki, wzorzec, następstwa i pilność;
- luki jawnie oznaczone; autor dostał podsumowanie i możliwość korekty;
- wszystkie krzywdy zachowane albo pominięte na świadomą decyzję autora;
- żadnych dopisanych faktów, ukrytej zmiany perspektywy ani usunięć z braku dowodu.

Status: `ZAKOŃCZONA`, `DO DOPYTANIA` lub `ZAKOŃCZONA NA ŻĄDANIE AUTORA — LUKI JAWNE`.
Niedokończony wywiad zatrzymuje oznaczenie redakcji jako finalnej, chyba że autor świadomie
żąda zakończenia na obecnym materiale. Nieznana data, brak pamięci, dowodu, protokołu lub
nierozstrzygnięta różnica nie blokują finalizacji, gdy ograniczenia są jawne. Decyzja autora
nie pozwala dopisywać ani przedstawiać świadomego fałszu jako faktu.

Gdy istnieją wcześniejsze relacje, wykonaj [AUDYT-B](references/hardgate-spojnosc.md).
Brak dostępu odnotuj; nie uzależniaj złożenia od uzyskania akt. Pokaż różnice z pochodzeniem,
zapytaj otwarcie i zachowaj odpowiedź lub brak pamięci. Nie wymuszaj jednej wersji.

### F5. Mapa wewnętrzna — prowadzona od wywiadu
Po każdej odpowiedzi dopisz wpis do notatki `Log zeznań — <Autor>`, a `Relacja zdarzeń — <Autor>`
zredaguj ponownie w odpowiednich miejscach osi czasu (Basic Memory, `relacje/<autor-slug>/`).
Relacja zachowuje chronologię zdarzeń; log — kolejność ujawniania wspomnień w sesjach. Tabela mapy
nie zastępuje żadnej z tych notatek. Szczegóły: `references/ciaglosc-sesji.md`, `references/basic-memory-relacja.md`.
W repo zapisuj inkrementalnie w `drafty/<pismo>/_MAPA_KRZYWD.md`, poza nim w materiale roboczym.

| # | Epizod / czas | Mikro-sekwencja | Relacja użytkownika | Typ epistemiczny | Pewność pamięci | Źródło wiedzy | Krzywda / skutek | Gałęzie kwalifikacyjne | Tropy dla organu | Pilność | Różnice z wcześniejszym zapisem | Decyzja autora |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Typ: własna obserwacja / odczucie / skutek / informacja od osoby / wniosek / podejrzenie.
Nie stosuj „potwierdzone/niepotwierdzone” jako kryterium obecności w piśmie. Przy kwalifikacji
zapisz przepis i ślad weryfikacji albo „do sprawdzenia”; brak przepisu nie usuwa wiersza.

### F6. Redakcja i prawo
Najpierw przypisz nowe informacje do pism i ustal ich status według
[ciągłości sesji](references/ciaglosc-sesji.md). Szablon zawiadomienia stosuj wyłącznie do
zawiadomienia; dla innych pism użyj właściwej formy i zweryfikuj etap oraz uprawnienia.
Czytaj [szablon](assets/szablon.md), [styl](references/styl.md) i [formę](references/forma.md).
Pisz pewnie tam, gdzie autor jest pewny; przybliżone słowa oznacz jako przybliżone.
Emocje są doświadczeniem i skutkiem. Źródło cudzej informacji nazwij w znanym zakresie,
bez wymyślania nazwiska lub daty. Chronologię porządkuj zakresami i kotwicami, gdy pamięć jest niepełna.
Przed wpisaniem artykułu, trybu, terminu, progu lub właściwości sprawdź urzędowy tekst właściwy
na datę czynu i pisma, w tym zmiany po tekście jednolitym i wejście w życie. Historyczny katalog
ani blog kancelarii nie zastępują sprawdzenia. Nie zamykaj narracji w jednej kwalifikacji;
warianty lub kumulację pokaż tylko tam, gdzie uzasadniają je opisane fakty i zweryfikowane prawo.

### F7. Kontrola
Porównaj pismo z każdym wierszem mapy. Usuń dopiski modelu, przywróć krzywdy utracone w redakcji,
sprawdź źródła i pewność pamięci. Użyj [kontroli oczami prokuratora](references/oczami-prokuratora.md)
do wykrycia pytań, nie cenzury. Sprawdź formę, aktualność użytego prawa i oba raporty z F4.
Tropy oraz załączniki oddziel od narracji, a wskazówki praktyczne od pisma.
Odróżniaj zakończenie redakcji na żądanie autora od kompletności formalnej: przy pustym
nagłówku, braku podpisu lub niesprawdzonej drodze złożenia wskaż, co jeszcze wymaga
uzupełnienia. Nie przedstawiaj takiego pliku jako w pełni gotowego do podpisania i złożenia.

### F8. Zapis (repo abogada, `shared/ARTEFAKTY-SPRAWY.md`)
Relację, log zeznań, rejestr pism, pytania otwarte i kopię relacji na zamknięcie sesji zapisuj
w Basic Memory (`legal`, `relacje/<autor-slug>/`) według `references/basic-memory-relacja.md`,
z odczytem potwierdzającym. Nie twórz ich jako plików w katalogu sprawy ani w projekcie claude.ai;
pliki są formatem awaryjnym tylko bez dostępu do Basic Memory. Nie są jednorazowymi notatkami `_robocze/`.
- Pismo: wersje `legal/sprawy/<katalog_sprawy>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` (tylko MD) i jeden
  DOCX pisma w `legal/output/` (tylko DOCX), w cyklu akceptacja redline → snapshot MD → redline sesji,
  zgodnie z `shared/ARTEFAKTY-SPRAWY.md`, „Cykl pracy nad pismem”. Pismo w `legal/output/` bez placeholderów;
  ręczna edycja autora w DOCX ma pierwszeństwo (`references/ciaglosc-sesji.md`, „Pisma w `output/` i wersje”).
- Pliki inkrementalne pisma (tworzone raz, potem dopisywane): `drafty/<pismo>/_PRZEBIEGI.md` (data, cel, wynik,
  decyzje autora), `_MAPA_KRZYWD.md` (mapa wewnętrzna F5, wiersze ze stałym `#`, zmiany statusu zamiast kopii),
  `_HARDGATE.md` (rejestr relacji i raport bramki, dopisek per przebieg).
- Jednorazowe (wyciągi z protokołów, wynik `rejestr_relacji.py`, notatki z wywiadu): `_robocze/rrrrMMdd_<pismo>__*`.
- Pismo złożone (podpisany PDF + potwierdzenie nadania) trafia do `01_dowody/`, nie zostaje w teczce.
- Fakty z relacji użytkownika bez dokumentu zapisuj w briefie sprawy jako niepotwierdzone
  dokumentem (zasada repo). W samym zawiadomieniu tej etykiety nie stosujesz (K1, K2); ta etykieta nie jest oceną wiarygodności ani warunkiem redakcji.

## Format odpowiedzi

W trakcie wywiadu: krótkie podsumowanie tego, co już wiesz (2-5 linii), potem jedno otwarte pytanie
o konkretny szczegół, a pod nim **pełna lista wszystkich pytań otwartych** (ID z logu) — w każdej
odpowiedzi, dopóki trwa sesja relacji, także po oddaniu nowej wersji pisma. Zaczekaj na odpowiedź.
Bez wstępów i pochwał.

Przy oddaniu pisma:
1. Link do chronologicznej relacji MD, logu zeznań, wersji sesyjnej relacji oraz przygotowanych pism; krótko wskaż,
   co przybyło i które projekty zmieniły się od poprzedniej sesji.
2. Status HARDGATE-A z lukami i decyzją autora; AUDYT-B ze znanymi różnicami lub informacją o braku materiału. Przy drafcie zaznacz, że wywiad nie został zakończony.
3. Krótka lista: co jeszcze warto dopytać, decyzje do podjęcia (np. organ, załączniki).
4. Informacje praktyczne poza pismem: jak złożyć, potwierdzenie, co dalej (`references/forma.md`).

## Kolizje z innymi skillami

| Skill | Co z niego bierzesz | Czego NIE stosujesz |
|---|---|---|
| `pisma-proste-v2` | WYŁĄCZNIE wzorzec nagłówka (M4); tor pisma prostego nie jest uruchamiany. Zamiast `⬛ [UZUPEŁNIJ: …]` — najbardziej prawdopodobna wartość i pytanie do autora (pismo w `output/` bez placeholderów) | cała reszta toru, w tym `shared/CLAIM-VALIDATION.md` (zastępowanie relacji dokumentami, usuwanie twierdzeń bez oparcia), „jedno pytanie zbiorcze”, moduł opłat |
| `pisz-po-polsku` | wzorce anty-AI, rytm, czasowniki, zakres emocji, typografia, pisownia 2026, zachowanie faktów | tryb „Pismo prawnicze”: formuły procesowe są tu wadą (poza otwarciem, wnioskiem o ściganie i listą przepisów); używaj trybu „Relacja pokrzywdzonego” |
| `zazalenie-na-postanowienie-prokuratora` | wiedza, na co patrzy prokurator i co się zaskarża po odmowie | styl uzasadnienia, zarzuty, „każde twierdzenie zakotwiczone w dowodzie” |
| `szturm-na-draft-pl`, `adversarial-legal-review-pl`, `atak-przeciwnika-pl` | na wyraźne życzenie autora, wyłącznie w trybie recenzji rozszerzającej (`shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md`): pominięte krzywdy, osoby i naruszenia przez organy, czyny, których autor nie nazwał (R4a), pytania i rozbudowa pisma | mandat przeciwnika, rozmywanie tez alternatywami, dopisywanie zastrzeżeń, „korygowanie” relacji autora, ciężar dowodu |

Po wywiadzie w już toczącej się sprawie użyj `pisma-procesowe-v3` lub
`zazalenie-na-postanowienie-prokuratora` do formy adekwatnego pisma. Ten skill nadal prowadzi
relację, zapis i rozdział nowych informacji. Reguły formalne i terminowe pozostają właściwe
dla danego pisma; pomocniczy skill nie usuwa relacji z braku dowodu ani nie restartuje wywiadu.

## Pliki skilla

| Plik | Kiedy czytać |
|---|---|
| `references/ciaglosc-sesji.md` | zawsze: wejście, zapis, wznowienie, wersje pism w `output/` i dobór pism |
| `references/basic-memory-relacja.md` | zawsze: notatki relacji w Basic Memory, kolejność zapisu, awaria, migracja plików |
| `references/wywiad.md` | zawsze, od F2 |
| `references/mapa-krzywd.md` | zawsze, w F3 (otwarty katalog pytań i historyczne punkty wyjścia do weryfikacji prawa) |
| `references/hardgate-spojnosc.md` | gdy istnieją wcześniejsze zeznania, wyjaśnienia lub pisma; audyt nie blokuje złożenia |
| `references/styl.md` | F6 i F7 |
| `references/oczami-prokuratora.md` | F7 i gdy wybierasz, które szczegóły dopytać |
| `references/forma.md` | F6 (nagłówek, otwarcie, wniosek o ściganie, lista przepisów) i przy informacjach praktycznych |
| `assets/szablon.md` | F6 |
| `scripts/rejestr_relacji.py` | pomocnicze wyszukanie relacji w F4, tylko w repo abogada |
| `evals/evals.json` | rozwój skilla (skill-creator) |

Historia zmian i decyzje autora: `references/CHANGELOG.md`. Pochodzenie reguł i research:
[references/research.md](references/research.md) — czytaj przy rozwijaniu skilla.
