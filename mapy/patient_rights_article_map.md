patient\_rights\_article\_map:

file\_role: name: "patient\_rights\_article\_map.md" purpose: - "mapowanie kluczowych przepisów ustawy o prawach pacjenta i Rzeczniku Praw Pacjenta" - "warstwa gwarancyjna dla analiz UoOZP, zwłaszcza art. 23, art. 18-18f, art. 33-34 oraz kontroli dokumentacji" - "identyfikacja praw pacjenta naruszonych równolegle do naruszeń szczególnych procedur psychiatrycznych" - "budowa checklisty dla analizy dokumentacji medycznej, przymusu, zgody, informacji, intymności, godności, kontaktu i ścieżki RPP"

not\_purpose:

- "nie zastępuje mapy UoOZP"

- "nie przesądza samodzielnie o legalności przyjęcia bez zgody"

- "nie zastępuje analizy kodeksu cywilnego, k.p.c., RODO ani regulaminu urzędowania sądów"

- "nie jest zbiorem pełnych cytatów ustawowych"

- "nie jest opinią medyczną ani wyliczeniem wartości roszczeń"



source\_act: name: "Ustawa o prawach pacjenta i Rzeczniku Praw Pacjenta" short\_name: "UPP\_RPP" source\_type: "ustawa" function\_in\_combined\_skill: - "warstwa praw pacjenta" - "warstwa dokumentacyjna" - "warstwa skargowa i RPP" - "warstwa godności, intymności, informacji i zgody" - "warstwa pomocnicza dla oceny szkody, winy i naruszenia standardu postępowania"

source\_status\_and\_use: preferred\_use: - "używać jako mapy analitycznej, a nie jako pełnego tekstu aktu" - "przed cytowaniem literalnym sprawdzić aktualne brzmienie przepisu w aktualnym tekście ustawy" - "w odpowiedziach analitycznych odróżniać parafrazę przepisu od cytatu" - "jeżeli użytkownik prosi o pismo procesowe, nie cytować automatycznie całych przepisów; używać tylko niezbędnych fragmentów" update\_warning: - "przepisy ustawy mogą się zmieniać" - "dla pism procesowych i terminów należy weryfikować aktualne brzmienie" - "mapa ma charakter roboczego modelu analizy"

legal\_hierarchy: primary\_order: - "1. Dokumentacja źródłowa i literalny stan akt" - "2. Przepisy szczególne UoOZP" - "3. Ustawa o prawach pacjenta i RPP jako warstwa gwarancyjna" - "4. Przepisy o dokumentacji medycznej i akty wykonawcze" - "5. Kodeks cywilny i reżimy odpowiedzialności" - "6. Kodeks postępowania cywilnego i przepisy procesowe" - "7. RODO i przepisy ochrony danych" - "8. Regulamin urzędowania sądów powszechnych i praktyka organizacyjna" - "9. Orzecznictwo i piśmiennictwo" - "10. Realistyczne alternatywne interpretacje, tylko jeśli wynikają z materiału"

lex\_specialis\_rules:

- "UoOZP jest przepisem szczególnym dla przyjęcia bez zgody, badania bez zgody, pobytu bez zgody i przymusu bezpośredniego"

- "ustawa o prawach pacjenta nie znosi szczególnych podstaw działania z UoOZP"

- "ustawa o prawach pacjenta uzupełnia UoOZP tam, gdzie chodzi o informację, godność, intymność, dokumentację, tajemnicę, kontakt i skargę"

- "jeżeli UoOZP dopuszcza przymus, nadal trzeba sprawdzić, czy sposób wykonania nie naruszał praw pacjenta"

- "jeżeli UoOZP wymaga dokumentacji, ustawa pacjencka wzmacnia znaczenie rzetelnego prowadzenia, przechowywania i udostępniania dokumentacji"



relation\_to\_uoopz: core\_relation: - "UoOZP odpowiada na pytanie: czy wolno było przyjąć bez zgody, leczyć bez zgody albo zastosować przymus" - "UPP\_RPP odpowiada na pytanie: czy przy tym uszanowano prawa pacjenta" - "naruszenie UoOZP i naruszenie praw pacjenta mogą występować równolegle" - "brak naruszenia jednej warstwy nie wyklucza naruszenia drugiej" examples: - "przyjęcie bez zgody może być materialnie zasadne, ale wadliwe informacyjnie lub dokumentacyjnie" - "przymus bezpośredni może mieć podstawę ustawową, ale zostać wykonany z naruszeniem godności lub intymności" - "hospitalizacja może być formalnie kontrolowana przez sąd opiekuńczy, ale nadal może istnieć spór o dostęp do dokumentacji albo prawo do informacji" - "brak zgody pacjenta w psychiatrii wymaga analizy UoOZP, ale nie zwalnia z testu informacji, dokumentacji i minimalizacji dolegliwości"

activation\_triggers: always\_use\_when: - "analiza dotyczy przyjęcia do szpitala psychiatrycznego bez zgody" - "analiza dotyczy przymusu bezpośredniego" - "analiza dotyczy leczenia bez zgody" - "analiza dotyczy zgody, odmowy zgody lub sprzeciwu pacjenta" - "analiza dotyczy dokumentacji medycznej, jej braków, wersji, udostępnienia lub retencji" - "analiza dotyczy prawa do informacji o stanie zdrowia, leczeniu lub prawach pacjenta" - "analiza dotyczy godności, intymności, obecności osób trzecich, czynności intymnych lub monitoringu" - "analiza dotyczy kontaktu pacjenta z rodziną, osobą bliską, pełnomocnikiem, RPP lub sądem" - "analiza dotyczy tajemnicy medycznej albo ujawniania informacji osobom trzecim" - "analiza dotyczy skargi do RPP lub Rzecznika Praw Pacjenta Szpitala Psychiatrycznego" - "analiza dotyczy roszczeń z tytułu naruszenia praw pacjenta"

use\_optionally\_when:

- "sprawa dotyczy ogólnej jakości świadczeń zdrowotnych"

- "sprawa dotyczy kosztów leczenia, rozstroju zdrowia lub zdarzenia medycznego"

- "sprawa dotyczy praktyki systemowej lub zbiorowych praw pacjentów"

- "sprawa dotyczy organizacji szpitala, regulaminów, procedur, pełnomocnika praw pacjenta lub skarg wewnętrznych"

do\_not\_overuse\_when:

- "pytanie dotyczy wyłącznie materialnych przesłanek art. 23 UoOZP i nie ma komponentu informacji, dokumentacji, zgody, godności ani skargi"

- "pytanie dotyczy wyłącznie technicznego porównania plików lub OCR"

- "pytanie dotyczy wyłącznie procedury cywilnej bez komponentu praw pacjenta"



issue\_taxonomy: information\_rights: label: "informacja" includes: - "informacja o stanie zdrowia" - "informacja o rozpoznaniu" - "informacja o proponowanych i możliwych metodach diagnostycznych lub leczniczych" - "informacja o następstwach zastosowania albo zaniechania metody" - "informacja o prawach pacjenta" - "informacja o rodzaju i zakresie świadczeń" typical\_documents: - "wpis lekarski" - "formularz zgody" - "pouczenie pacjenta" - "karta informacyjna" - "notatka pielęgniarska" - "regulamin oddziału" core\_questions: - "czy informacja została przekazana" - "czy była przystępna" - "czy była dostosowana do stanu pacjenta" - "czy pacjent mógł przedstawić swoje stanowisko" - "czy istnieje ślad dokumentacyjny"

consent\_and\_objection:

label: "zgoda / odmowa / sprzeciw"

includes:

- "zgoda na świadczenie"

- "odmowa zgody"

- "sprzeciw pacjenta"

- "zgoda przedstawiciela ustawowego"

- "zgoda na obecność osób trzecich"

- "zgoda na udzielanie informacji osobom trzecim"

typical\_documents:

- "formularz zgody"

- "wpis o odmowie"

- "wpis o sprzeciwie"

- "wpis o zdolności do świadomego wyrażenia zgody"

- "upoważnienie do informacji"

core\_questions:

- "czy zgoda była poprzedzona informacją"

- "czy pacjent miał dostateczne rozeznanie"

- "czy odmowę albo sprzeciw odnotowano"

- "czy istniała szczególna podstawa działania mimo braku zgody"

- "czy nie pomylono zgody na leczenie ze zgodą na hospitalizację albo zgodą na przekazanie informacji"

dignity\_and\_intimacy:

label: "godność i intymność"

includes:

- "czynności przy ciele pacjenta"

- "unieruchomienie"

- "izolacja"

- "przymusowe podanie leków"

- "cewnikowanie"

- "czynności higieniczne"

- "monitoring"

- "obecność osób trzecich"

typical\_documents:

- "karta przymusu"

- "wpis pielęgniarski"

- "wpis lekarski"

- "procedura oddziałowa"

- "zapis monitoringu"

- "notatka o obecności osób trzecich"

core\_questions:

- "czy ingerencja była konieczna"

- "czy wybrano sposób najmniej dolegliwy"

- "czy zapewniono osłonę, prywatność i minimum ekspozycji"

- "czy obecność osób trzecich była niezbędna"

- "czy pacjent wyraził zgodę na obecność osób trzecich, jeśli była wymagana"

documentation\_rights:

label: "dokumentacja"

includes:

- "prowadzenie dokumentacji"

- "minimalna treść dokumentacji"

- "ochrona danych w dokumentacji"

- "udostępnienie dokumentacji"

- "wykaz udostępnień"

- "retencja dokumentacji"

- "wersje dokumentacji"

- "dokumentacja indywidualna i zbiorcza"

typical\_documents:

- "historia choroby"

- "wpisy lekarskie"

- "wpisy pielęgniarskie"

- "karta przymusu"

- "rejestr przymusu"

- "rejestr przyjęć bez zgody"

- "zlecenia lekarskie"

- "wyniki badań"

- "formularze zgód"

- "wykaz udostępnień dokumentacji"

- "korespondencja z archiwum"

core\_questions:

- "czy dokument istnieje"

- "czy zawiera wymagane minimum"

- "czy pozwala ustalić kto, kiedy, dlaczego i na jakiej podstawie działał"

- "czy dokumentacja została wydana w pełnym zakresie"

- "czy występują niespójności między wersjami"

confidentiality\_and\_disclosure:

label: "tajemnica i ujawnianie informacji"

includes:

- "tajemnica medyczna"

- "zgoda na ujawnienie informacji"

- "ujawnienie osobie bliskiej"

- "ujawnienie organom"

- "ujawnienie policji, sądowi, prokuraturze lub RPP"

- "minimalizacja zakresu ujawnienia"

typical\_documents:

- "upoważnienie do informacji"

- "sprzeciw pacjenta"

- "korespondencja z osobami trzecimi"

- "notatka o rozmowie telefonicznej"

- "żądanie organu"

- "odpowiedź szpitala"

core\_questions:

- "komu ujawniono informację"

- "jaka była podstawa ujawnienia"

- "czy zakres ujawnienia był niezbędny"

- "czy istniała zgoda albo inna podstawa ustawowa"

- "czy zachowano tajemnicę wobec osób nieuprawnionych"

contact\_and\_family\_life:

label: "kontakt z innymi osobami"

includes:

- "kontakt osobisty"

- "kontakt telefoniczny"

- "kontakt korespondencyjny"

- "kontakt z osobą bliską"

- "kontakt z pełnomocnikiem"

- "kontakt z RPP"

- "odmowa kontaktu przez pacjenta"

- "ograniczenie kontaktu przez podmiot"

typical\_documents:

- "regulamin odwiedzin"

- "wpis o ograniczeniu kontaktu"

- "wpis o odmowie kontaktu"

- "korespondencja pacjenta"

- "notatki rozmów"

- "skarga pacjenta"

core\_questions:

- "czy pacjent miał realną możliwość kontaktu"

- "czy ograniczenie miało podstawę"

- "czy ograniczenie było proporcjonalne"

- "czy ograniczenie zostało udokumentowane"

- "czy pacjent sam odmówił kontaktu"

rpp\_and\_complaints:

label: "RPP / skargi / kontrola"

includes:

- "wniosek do RPP"

- "Rzecznik Praw Pacjenta Szpitala Psychiatrycznego"

- "postępowanie wyjaśniające"

- "żądanie dokumentów"

- "wystąpienie RPP"

- "praktyki naruszające zbiorowe prawa pacjentów"

- "udział RPP w sprawie cywilnej"

typical\_documents:

- "wniosek do RPP"

- "odpowiedź RPP"

- "wezwanie RPP do szpitala"

- "wyjaśnienia szpitala"

- "wystąpienie RPP"

- "informacja o działaniach naprawczych"

- "wniosek o ponowne rozpatrzenie"

core\_questions:

- "czy sprawa dotyczy indywidualnego naruszenia"

- "czy sprawa ma potencjał systemowy"

- "czy RPP powinien żądać dokumentów"

- "czy RPP powinien zbadać sprawę na miejscu"

- "czy istnieje podstawa do działań naprawczych lub dyscyplinarnych"



severity\_model: high\_weight: definition: "naruszenia bezpośrednio ingerujące w wolność, integralność, godność, możliwość obrony praw lub dostęp do dokumentacji" examples: - "brak informacji o prawach przy przyjęciu bez zgody" - "brak dokumentacji przymusu bezpośredniego" - "odmowa pełnej dokumentacji pacjentowi lub organowi uprawnionemu" - "naruszenie godności i intymności przy unieruchomieniu, izolacji lub czynności intymnej" - "ujawnienie informacji medycznych osobie nieuprawnionej" - "ograniczenie kontaktu bez podstawy" - "brak dostępu do Rzecznika Praw Pacjenta Szpitala Psychiatrycznego" - "systemowy wzorzec naruszeń praw pacjenta"

medium\_weight:

definition: "naruszenia istotne, ale zwykle wymagające powiązania z konkretną szkodą, krzywdą lub skutkiem procesowym"

examples:

- "brak wpisu o żądaniu konsultacji"

- "brak wpisu o odmowie obecności osoby bliskiej"

- "niepełne pouczenie"

- "brak wykazu udostępnień"

- "niejasny zakres wydanej dokumentacji"

- "brak spisu rzeczy pacjenta"

- "brak informacji o osobie udostępniającej dokumentację"

contextual:

definition: "okoliczności, które same nie przesądzają naruszenia, ale wzmacniają albo osłabiają ocenę"

examples:

- "stan pacjenta utrudniający rozumienie informacji"

- "konflikt rodzinny"

- "wiele wersji dokumentacji"

- "sprzeczność między relacją pacjenta a wpisami"

- "opóźniona skarga"

- "brak zachowanych nagrań"

- "brak wcześniejszego leczenia psychiatrycznego"



evidence\_model: evidence\_priority: - "1. Dokument źródłowy z datą, autorem i treścią wpisu" - "2. Dokumentacja indywidualna pacjenta" - "3. Dokumentacja zbiorcza i rejestry" - "4. Zlecenia, karty przymusu, karty kontroli, formularze zgody" - "5. Zawiadomienia do sądu, RPP, organów i odpowiedzi" - "6. Monitoring, logi systemowe, wykazy udostępnień" - "7. Zeznania i oświadczenia" - "8. Relacje pośrednie" - "9. Interpretacje i hipotezy"

documentation\_assumptions:

- "brak dokumentu wymaganego prawem nie jest neutralny"

- "pusty formularz nie dowodzi wykonania czynności"

- "sam fakt istnienia procedury nie dowodzi jej zastosowania"

- "późniejsza dokumentacja nie zastępuje braku wpisu z czasu czynności"

- "jeżeli dokumentacja powinna pozwalać ustalić przebieg czynności, a nie pozwala, jest to samodzielna czerwona flaga"

- "rozbieżności między wersjami dokumentacji należy opisywać jako fakt, nie jako błąd systemu, chyba że materiał wskazuje na błąd systemu"

fact\_interpretation\_split:

facts:

- "co wynika literalnie z dokumentu"

- "kto podpisał albo sporządził wpis"

- "kiedy wpis został sporządzony"

- "jaka podstawa prawna została wskazana"

- "czego dokument nie zawiera"

interpretations:

- "czy opis spełnia przesłankę ustawową"

- "czy brak dokumentu jest istotny"

- "czy naruszenie ma charakter indywidualny lub systemowy"

- "czy powstaje podstawa roszczenia"

forbidden\_shortcuts:

- "nie zakładaj, że czynność wykonano, jeśli jedynym dowodem jest ogólna praktyka oddziału"

- "nie zakładaj, że pacjent został poinformowany, jeśli nie ma treści lub śladu informacji"

- "nie zakładaj zgody z milczenia, gdy stan pacjenta wymaga analizy zdolności rozumienia"

- "nie usprawiedliwiaj braku dokumentu hipotezą techniczną bez konkretnej przesłanki"



analysis\_sequence: step\_1\_context: label: "ustal kontekst" questions: - "czy sprawa dotyczy psychiatrii, SOR, ZRM, oddziału somatycznego czy archiwum dokumentacji" - "czy występuje przyjęcie bez zgody, przymus, leczenie bez zgody albo ograniczenie kontaktu" - "czy pacjent kwestionuje przebieg czynności, dokumentację, informację, zgodę, godność albo dostęp do praw"

step\_2\_uoopz\_first:

label: "najpierw UoOZP, jeśli dotyczy"

questions:

- "czy zachodzi szczególny reżim art. 21, 23, 24, 28, 33, 34 albo 18-18f UoOZP"

- "czy przesłanki materialne i proceduralne UoOZP zostały odrębnie sprawdzone"

- "czy dokumentacja psychiatryczna spełnia wymagania szczególne"

step\_3\_patient\_rights\_layer:

label: "następnie prawa pacjenta"

questions:

- "które prawa pacjenta zostały uruchomione"

- "które prawa pacjenta mogły zostać naruszone"

- "czy naruszenie wynika bezpośrednio z dokumentacji"

- "czy naruszenie wynika z braku dokumentacji"

- "czy naruszenie ma charakter gwarancyjny, materialny, dokumentacyjny, organizacyjny czy skargowy"

step\_4\_evidence\_and\_gaps:

label: "dowody i luki"

questions:

- "jakie dokumenty potwierdzają realizację prawa"

- "jakich dokumentów brakuje"

- "czy brak dokumentu jest brakiem formalnym, dowodowym czy materialnym"

- "czy istnieją rozbieżności między wersjami dokumentacji"

- "czy potrzebne są dokumenty z RPP, sądu, archiwum, rejestru albo monitoringu"

step\_5\_claim\_or\_remedy\_mapping:

label: "mapowanie skutków"

questions:

- "czy naruszenie uzasadnia skargę do RPP"

- "czy naruszenie ma znaczenie dla roszczenia z art. 4 ust. 1 ustawy pacjenckiej"

- "czy naruszenie może wspierać roszczenie z art. 444-445 k.c."

- "czy naruszenie może być elementem odpowiedzialności z art. 417 k.c."

- "czy sprawa może mieć komponent praktyki naruszającej zbiorowe prawa pacjentów"



cross\_module\_links: uoopz\_article\_map: use\_when: - "przyjęcie bez zgody" - "badanie bez zgody" - "przymus bezpośredni" - "leczenie bez zgody" - "kontrola sądu opiekuńczego" relation: - "patient\_rights\_article\_map jest warstwą uzupełniającą"

civil\_liability\_and\_litigation\_risk\_map:

use\_when:

- "analiza dotyczy roszczeń, zadośćuczynienia, szkody, winy lub odpowiedzialności podmiotu"

- "trzeba rozdzielić art. 4 ust. 1 ustawy pacjenckiej, art. 444-445 k.c. i art. 417 k.c."

- "pojawia się opinia biegłego, zastrzeżenia do opinii albo art. 162 k.p.c."

relation:

- "patient\_rights\_article\_map identyfikuje naruszone prawo; civil\_liability mapuje podstawę roszczenia"

gdpr\_rodo\_map:

status: "planned"

use\_when:

- "analiza dotyczy danych osobowych, danych medycznych, dostępu do EDM, logów, upoważnień, administratora, podmiotu przetwarzającego, naruszenia poufności lub retencji"

relation:

- "RODO nie zastępuje prawa dostępu do dokumentacji medycznej, ale reguluje ochronę danych i legalność przetwarzania"

kpc\_and\_court\_rules\_map:

status: "planned"

use\_when:

- "analiza dotyczy sądu opiekuńczego, rozprawy, protokołu, opinii biegłego, terminów, doręczeń, akt sądowych, zastrzeżeń procesowych lub organizacji sekretariatu"

relation:

- "KPC reguluje czynności procesowe; regulamin urzędowania sądów reguluje wybrane kwestie organizacyjno-techniczne"



red\_flag\_handling\_rules: - "każdą czerwoną flagę przypisz do konkretnego prawa pacjenta albo konkretnego obowiązku podmiotu" - "nie twórz czerwonej flagi wyłącznie z niekomfortowego faktu; musi istnieć norma, obowiązek lub standard" - "oznacz wagę czerwonej flagi: high\_weight, medium\_weight, contextual" - "dla high\_weight zawsze wskaż dokument, którego brak albo który potwierdza naruszenie" - "dla naruszeń dokumentacyjnych wskaż, czy brak dotyczy istnienia dokumentu, treści dokumentu, daty, autora, podpisu, podstawy prawnej czy zakresu udostępnienia" - "dla naruszeń informacji i zgody wskaż, czy problem dotyczy braku informacji, nieprzystępności, braku zdolności pacjenta, braku zgody, sprzeciwu czy braku udokumentowania"

output\_contract: required\_sections\_when\_used: - "warstwa praw pacjenta" - "naruszone albo potencjalnie naruszone prawa" - "dowody źródłowe" - "braki dokumentacyjne" - "czerwone flagi" - "znaczenie dla UoOZP" - "znaczenie dla RPP lub roszczeń" - "dokumenty do pozyskania"

preferred\_language:

- "dokumentacja wskazuje"

- "brak dokumentacji potwierdzającej"

- "wymaga wyjaśnienia przez podmiot"

- "naruszenie ma charakter gwarancyjny"

- "naruszenie ma charakter dokumentacyjny"

- "naruszenie może wspierać roszczenie, ale wymaga odrębnego wykazania szkody lub krzywdy"

- "materiał nie pozwala tego przesądzić"

avoid\_language:

- "na pewno doszło do błędu systemu"

- "prawdopodobnie ktoś zapomniał"

- "to tylko formalność"

- "brak dokumentu nie ma znaczenia"

- "skoro pacjent był w psychiatrii, to prawa ogólne nie mają zastosowania"

- "skoro był przymus, to godność i intymność nie mają znaczenia"



document\_request\_defaults: general: - "pełna dokumentacja medyczna" - "wykaz udostępnień dokumentacji" - "formularze zgody i odmowy" - "pouczenia o prawach pacjenta" - "wpisy o przekazaniu informacji" - "wpisy lekarskie i pielęgniarskie" - "zlecenia lekarskie" - "korespondencja z pacjentem, osobą upoważnioną, sądem albo RPP" - "regulaminy i procedury oddziałowe" - "skargi, odpowiedzi na skargi i działania naprawcze"

psychiatric\_context:

- "informacja o Rzeczniku Praw Pacjenta Szpitala Psychiatrycznego"

- "dokumentacja przyjęcia bez zgody"

- "karta przymusu bezpośredniego"

- "rejestr przymusu"

- "rejestr przyjęć bez zgody"

- "zawiadomienie sądu"

- "wpisy dotyczące kontaktu z rodziną lub osobą bliską"

- "wpisy dotyczące ograniczenia kontaktu"

- "monitoring, jeżeli dotyczy izolacji lub zdarzenia"



quality\_control: before\_final\_answer: - "sprawdź, czy nie pomieszano UoOZP z ustawą pacjencką" - "sprawdź, czy każde naruszone prawo ma przypisany fakt albo brak dokumentu" - "sprawdź, czy nie przypisano skutku roszczeniowego bez podstawy" - "sprawdź, czy nie użyto hipotezy technicznej bez materiału" - "sprawdź, czy wskazano dokumenty potrzebne do weryfikacji" - "sprawdź, czy rozdzielono fakt, interpretację i wniosek" - "sprawdź, czy wnioski są proporcjonalne do materiału"

article\_map:

source\_act: name: "Ustawa o prawach pacjenta i Rzeczniku Praw Pacjenta" relation\_to\_uoopz: - "ustawa działa jako warstwa gwarancyjna wobec UoOZP" - "nie zastępuje szczególnego reżimu UoOZP dla przyjęcia bez zgody i przymusu bezpośredniego" - "uzupełnia analizę o prawa pacjenta: informacja, zgoda, godność, intymność, dokumentacja, tajemnica, kontakt, Rzecznik Praw Pacjenta" - "stosować zwłaszcza wtedy, gdy dokumentacja psychiatryczna wskazuje na przyjęcie bez zgody, leczenie bez zgody, przymus bezpośredni, ograniczenie kontaktu, spór o dokumentację lub skargę pacjenta"

integration\_principles: - "najpierw stosuj przepisy szczególne UoOZP dla przyjęcia bez zgody i przymusu bezpośredniego" - "następnie sprawdzaj, czy równolegle naruszono ogólne prawa pacjenta" - "nie mieszaj przesłanek legalności art. 23 UoOZP z ogólnym prawem do świadczeń zdrowotnych" - "używaj ustawy o prawach pacjenta jako testu gwarancyjnego: czy pacjent był poinformowany, czy uszanowano jego godność, czy dokumentacja jest dostępna i rzetelna, czy zachowano tajemnicę, czy miał realną ścieżkę skargową" - "jeżeli UoOZP wymaga dokumentacji określonej czynności, a ustawa o prawach pacjenta wymaga rzetelnego prowadzenia i udostępniania dokumentacji, traktuj braki dokumentacyjne jako problem podwójny: szczególny i ogólnopacjencki"

recommended\_statutory\_chain: description: "Łańcuch pomocniczy dla analizy art. 23 UoOZP i przymusu bezpośredniego." articles: - "art. 1" - "art. 2" - "art. 3" - "art. 4" - "art. 5" - "art. 6" - "art. 7" - "art. 8" - "art. 9" - "art. 11" - "art. 12" - "art. 12a" - "art. 13" - "art. 14" - "art. 15" - "art. 16" - "art. 17" - "art. 18" - "art. 19" - "art. 20" - "art. 20a" - "art. 21" - "art. 22" - "art. 23" - "art. 24" - "art. 25" - "art. 26" - "art. 27" - "art. 28" - "art. 29" - "art. 30" - "art. 30a" - "art. 31" - "art. 32" - "art. 33" - "art. 34" - "art. 35" - "art. 39" - "art. 40" - "art. 40a" - "art. 41" - "art. 42" - "art. 47" - "art. 47a" - "art. 50" - "art. 51" - "art. 52" - "art. 53" - "art. 55" - "art. 56" - "art. 59" - "art. 61" - "art. 64" - "art. 67q-67zd" - "art. 68" - "art. 69" - "art. 69a" - "art. 70"

article\_map:

art\_1:

role: "zakres ustawy"

importance: "fundamentalny kontekst"

relevance:

- "ustawa określa prawa pacjenta"

- "ustawa określa zasady udostępniania dokumentacji medycznej"

- "ustawa określa obowiązki podmiotów udzielających świadczeń zdrowotnych związane z prawami pacjenta"

- "ustawa określa kompetencje Rzecznika Praw Pacjenta"

- "ustawa określa postępowanie w sprawach praktyk naruszających zbiorowe prawa pacjentów"

use\_in\_analysis:

- "używaj jako podstawy do wskazania, że analiza nie kończy się na UoOZP"

- "w sprawach psychiatrycznych stosuj jako ogólny katalog gwarancji pacjenckich"

red\_flags:

- "analiza szpitala ograniczona wyłącznie do formalnego trybu UoOZP, bez oceny praw pacjenta"

- "pomijanie prawa do dokumentacji, informacji, godności i skargi"

art\_2:

role: "obowiązek przestrzegania praw pacjenta"

importance: "centralny gwarancyjnie"

relevance:

- "przestrzeganie praw pacjenta jest obowiązkiem organów władzy publicznej właściwych w zakresie ochrony zdrowia"

- "obowiązek dotyczy NFZ"

- "obowiązek dotyczy podmiotów udzielających świadczeń zdrowotnych"

- "obowiązek dotyczy osób wykonujących zawód medyczny"

- "obowiązek dotyczy innych osób uczestniczących w udzielaniu świadczeń zdrowotnych"

use\_in\_analysis:

- "ustal, kto uczestniczył w udzielaniu świadczeń i czy jego działanie mieściło się w standardzie praw pacjenta"

- "stosuj wobec personelu medycznego, podmiotu leczniczego i osób pomocniczych"

red\_flags:

- "przerzucanie odpowiedzialności wyłącznie na pojedynczego lekarza, gdy naruszenie ma charakter organizacyjny"

- "brak procedury zapewniającej respektowanie praw pacjenta przy przymusie"

art\_3:

role: "definicje"

importance: "centralny pomocniczo"

relevance:

- "definiuje pacjenta"

- "definiuje osobę bliską"

- "definiuje opiekuna faktycznego"

- "definiuje podmiot udzielający świadczeń zdrowotnych"

- "definiuje świadczenie zdrowotne"

- "definiuje wyciąg, odpis i kopię dokumentacji medycznej"

- "definiuje zdarzenie medyczne"

use\_in\_analysis:

- "ustal, czy dana osoba jest pacjentem w rozumieniu ustawy"

- "ustal, czy osoba trzecia mieści się w definicji osoby bliskiej albo opiekuna faktycznego"

- "używaj przy sporach o dokumentację, kopie, odpisy i wyciągi"

- "używaj przy kwalifikacji zdarzenia medycznego w ścieżce kompensacyjnej"

red\_flags:

- "udzielanie informacji osobie trzeciej bez ustalenia jej statusu"

- "odmowa dokumentacji z pomieszaniem pojęć kopii, odpisu, wyciągu lub skanu"

- "pomijanie statusu opiekuna faktycznego przy pacjencie niezdolnym do samodzielnego działania"

art\_4:

role: "zadośćuczynienie za zawinione naruszenie praw pacjenta"

source: "art. 4 ust. 1 ustawy o prawach pacjenta i Rzeczniku Praw Pacjenta"

importance: "centralny roszczeniowo"

relevance:

- "w razie zawinionego naruszenia praw pacjenta sąd może przyznać poszkodowanemu odpowiednią sumę tytułem zadośćuczynienia pieniężnego"

- "przepis działa niezależnie od szczegółowego reżimu UoOZP"

- "przepis odsyła do art. 448 Kodeksu cywilnego"

- "może obejmować naruszenia prawa do informacji, zgody, dokumentacji, godności, intymności, kontaktu, tajemnicy i dostępu do RPP"

- "ustawa wskazuje wyjątki, do których ten mechanizm nie ma zastosowania"

use\_in\_analysis:

- "sprawdź, które konkretne prawo pacjenta zostało naruszone"

- "sprawdź, czy naruszenie było zawinione"

- "oddziel naruszenie prawa pacjenta od szkody na osobie z art. 444-445 k.c."

- "stosuj jako osobną podstawę przy naruszeniach gwarancyjnych, nawet gdy nie ma trwałego uszczerbku somatycznego"

- "stosuj przy kwalifikacji skutków naruszeń praw pacjenta"

red\_flags:

- "brak pouczenia o prawach przy przyjęciu bez zgody"

- "brak informacji o rozpoznaniu, przyczynach przyjęcia, leczeniu lub skutkach przymusu"

- "naruszenie godności i intymności przy unieruchomieniu, izolacji, cewnikowaniu albo czynnościach pielęgnacyjnych"

- "odmowa lub niepełne wydanie dokumentacji"

- "brak dostępu do Rzecznika Praw Pacjenta Szpitala Psychiatrycznego"

- "ujawnienie informacji medycznych osobie trzeciej bez podstawy"

- "traktowanie każdego braku dokumentacyjnego automatycznie jako podstawy zadośćuczynienia bez analizy zawinienia"

- "pominięcie art. 4 przy naruszeniach godności, informacji, zgody lub intymności"

output\_style:

- "wskazuj konkretnie naruszone prawo pacjenta"

- "nie pisz ogólnie: naruszono prawa pacjenta; wskaż prawo, fakt i dokument"

- "jeżeli brak dokumentacji realizacji prawa, oznacz to jako problem dowodowy wysokiej wagi"

art\_5:

role: "ograniczenie korzystania z praw pacjenta"

importance: "istotny przy ograniczeniach kontaktu i organizacji"

relevance:

- "kierownik podmiotu lub upoważniony lekarz może ograniczyć korzystanie z praw pacjenta w przypadku zagrożenia epidemicznego"

- "ograniczenie może nastąpić ze względu na bezpieczeństwo zdrowotne pacjentów"

- "w zakresie prawa do kontaktu osobistego, telefonicznego lub korespondencyjnego także ze względu na możliwości organizacyjne podmiotu"

use\_in\_analysis:

- "sprawdź, czy ograniczenie prawa pacjenta miało podstawę ustawową"

- "sprawdź, czy ograniczenie było wydane przez uprawnioną osobę"

- "sprawdź, czy ograniczenie nie zostało użyte jako nieformalna sankcja"

red\_flags:

- "ograniczenie kontaktu bez wskazania podstawy"

- "ograniczenie praw pacjenta uzasadniane ogólnym porządkiem oddziału bez konkretnej przesłanki"

- "brak śladu decyzji kierownika lub upoważnionego lekarza"

art\_6:

role: "prawo do świadczeń zgodnych z aktualną wiedzą medyczną i prawo żądania opinii"

importance: "centralny standard jakościowy"

relevance:

- "pacjent ma prawo do świadczeń zdrowotnych odpowiadających wymaganiom aktualnej wiedzy medycznej"

- "pacjent może żądać, aby lekarz zasięgnął opinii innego lekarza lub zwołał konsylium"

- "pacjent może żądać, aby pielęgniarka zasięgnęła opinii innej pielęgniarki"

- "żądanie i odmowę odnotowuje się w dokumentacji medycznej"

use\_in\_analysis:

- "oceniaj jakość diagnostyki, leczenia, farmakoterapii i monitorowania"

- "sprawdź, czy żądanie drugiej opinii/konsylium zostało odnotowane"

- "łącz z UoOZP, gdy art. 23 wymaga opinii drugiego psychiatry albo psychologa w miarę możliwości"

red\_flags:

- "brak reakcji na żądanie konsultacji"

- "odmowa konsultacji bez wpisu w dokumentacji"

- "leczenie lub przymus bez widocznego odniesienia do aktualnej wiedzy medycznej"

- "brak drugiej opinii tam, gdzie była realnie możliwa i istotna"

art\_7:

role: "prawo do natychmiastowego świadczenia przy zagrożeniu zdrowia lub życia"

importance: "istotny kontekst ratunkowy"

relevance:

- "pacjent ma prawo do natychmiastowego udzielenia świadczeń zdrowotnych ze względu na zagrożenie zdrowia lub życia"

use\_in\_analysis:

- "stosuj przy ocenie interwencji nagłych, SOR, ZRM, zagrożenia życia lub zdrowia"

- "odróżniaj obowiązek natychmiastowego świadczenia od automatycznej podstawy przymusu psychiatrycznego"

red\_flags:

- "używanie samego stanu nagłego jako zamiennika przesłanek art. 23 UoOZP"

- "brak adekwatnej reakcji na somatyczne zagrożenie zdrowia lub życia"

art\_8:

role: "należyta staranność i warunki fachowe/sanitarne"

importance: "centralny standard staranności"

relevance:

- "pacjent ma prawo do świadczeń udzielanych z należytą starannością"

- "świadczenia mają być udzielane w warunkach odpowiadających wymaganiom fachowym i sanitarnym"

- "osoby wykonujące zawód medyczny kierują się zasadami etyki zawodowej"

use\_in\_analysis:

- "stosuj jako ogólny standard oceny wykonania świadczenia"

- "łącz z oceną przymusu bezpośredniego, sedacji, unieruchomienia, monitorowania i dokumentowania"

red\_flags:

- "chaotyczne, nieudokumentowane lub niestaranne prowadzenie pacjenta"

- "brak monitorowania po środkach farmakologicznych"

- "warunki zastosowania przymusu naruszające standard fachowy lub sanitarny"

- "wpisy dokumentacyjne sprzeczne, nieczytelne lub retrospektywne bez wyjaśnienia"

art\_9:

role: "prawo pacjenta do informacji o stanie zdrowia"

importance: "centralny"

relevance:

- "pacjent ma prawo do informacji o swoim stanie zdrowia"

- "pacjent lub przedstawiciel ustawowy mają prawo do przystępnej informacji o stanie zdrowia, rozpoznaniu, proponowanych i możliwych metodach diagnostycznych i leczniczych"

- "informacja obejmuje dające się przewidzieć następstwa zastosowania metod albo ich zaniechania, wyniki leczenia i rokowanie"

- "pacjent może wyrazić zgodę na udzielenie informacji innym osobom"

- "pacjent ma prawo przedstawić swoje zdanie po uzyskaniu informacji"

use\_in\_analysis:

- "sprawdź, czy pacjent został poinformowany o rozpoznaniu i leczeniu"

- "sprawdź, czy informacja była przystępna"

- "sprawdź, czy pacjent mógł przedstawić swoje zdanie"

- "łącz z art. 23 UoOZP, gdzie lekarz ma wyjaśnić przyczyny przyjęcia bez zgody i poinformować o prawach"

red\_flags:

- "brak wpisu o informacji przekazanej pacjentowi"

- "informacja tylko formalna, bez wskazania treści"

- "brak informacji o skutkach leków, sedacji, unieruchomienia lub diagnostyki"

- "udzielanie informacji osobom trzecim bez zgody pacjenta albo bez innej podstawy"

art\_10:

role: "informacja o odstąpieniu od leczenia"

importance: "pomocniczy"

relevance:

- "pacjent, przedstawiciel ustawowy lub opiekun faktyczny mają prawo do dostatecznie wczesnej informacji o zamiarze odstąpienia przez lekarza od leczenia i wskazania możliwości uzyskania świadczenia u innego lekarza lub podmiotu"

use\_in\_analysis:

- "stosuj przy przerwaniu leczenia, odmowie kontynuacji lub przekierowaniu pacjenta"

red\_flags:

- "nagłe odstąpienie od leczenia bez informacji i wskazania alternatywy"

art\_11:

role: "prawo do informacji o prawach pacjenta"

importance: "centralny gwarancyjnie"

relevance:

- "pacjent ma prawo do informacji o prawach pacjenta określonych w ustawie oraz w przepisach odrębnych"

- "podmiot udostępnia informację pisemnie w miejscu ogólnodostępnym"

- "pacjentowi niemogącemu się poruszać informację udostępnia się w sposób umożliwiający zapoznanie się z nią w pomieszczeniu, w którym przebywa"

use\_in\_analysis:

- "sprawdź, czy pacjent miał realny dostęp do informacji o prawach"

- "łącz z UoOZP art. 23 ust. 3 i art. 10a, gdy pacjent jest w szpitalu psychiatrycznym"

red\_flags:

- "brak pouczenia o prawach przy przyjęciu bez zgody"

- "pacjent unieruchomiony lub izolowany bez realnej możliwości zapoznania się z prawami"

- "informacja o prawach tylko formalnie wywieszona, bez realnej dostępności dla pacjenta"

art\_12:

role: "prawo do informacji o rodzaju i zakresie świadczeń"

importance: "istotny"

relevance:

- "pacjent ma prawo do informacji o rodzaju i zakresie świadczeń zdrowotnych udzielanych przez podmiot"

- "pacjent ze szczególnymi potrzebami ma prawo do otrzymania informacji w zrozumiały sposób"

use\_in\_analysis:

- "sprawdź, czy pacjent wiedział, jaki oddział i jaki zakres świadczeń go dotyczy"

- "stosuj przy pacjentach z ograniczeniami poznawczymi, komunikacyjnymi lub w stanie utrudniającym rozumienie informacji"

red\_flags:

- "brak dostosowania komunikacji do stanu pacjenta"

- "informowanie językiem niezrozumiałym lub wyłącznie formularzowo"

art\_12a:

role: "prawo zgłaszania działań niepożądanych produktów leczniczych"

importance: "istotny przy farmakoterapii i przymusowym podaniu leków"

relevance:

- "pacjent, przedstawiciel ustawowy albo opiekun faktyczny ma prawo zgłaszania działań niepożądanych produktów leczniczych osobom wykonującym zawód medyczny, Prezesowi URPL lub podmiotowi odpowiedzialnemu"

use\_in\_analysis:

- "stosuj przy podaniu leków psychotropowych, sedacji, benzodiazepinach, neuroleptykach i przymusowym zastosowaniu leków"

- "sprawdź, czy działania niepożądane zgłaszane przez pacjenta były odnotowane i ocenione"

red\_flags:

- "brak reakcji na zgłoszone objawy po lekach"

- "brak odnotowania działań niepożądanych"

- "traktowanie objawów polekowych jako wyłącznie objawów psychiatrycznych bez weryfikacji"

art\_13:

role: "prawo do tajemnicy informacji związanych z pacjentem"

importance: "centralny"

relevance:

- "pacjent ma prawo do zachowania w tajemnicy informacji z nim związanych, uzyskanych w związku z wykonywaniem zawodu medycznego"

use\_in\_analysis:

- "sprawdź, komu ujawniano informacje o pacjencie"

- "stosuj przy kontaktach z rodziną, policją, sądem, pracodawcą, osobami trzecimi"

red\_flags:

- "ujawnienie informacji osobie trzeciej bez podstawy"

- "niekontrolowane przekazywanie informacji w konflikcie rodzinnym"

- "mieszanie zgody na kontakt z upoważnieniem do informacji medycznej"

art\_14:

role: "obowiązek zachowania tajemnicy i wyjątki"

importance: "centralny"

relevance:

- "osoby wykonujące zawód medyczny są obowiązane zachować w tajemnicy informacje związane z pacjentem"

- "tajemnica obejmuje w szczególności stan zdrowia pacjenta"

- "wyjątki obejmują m.in. przepisy odrębnych ustaw, niebezpieczeństwo dla życia lub zdrowia pacjenta lub innych osób, zgodę pacjenta albo przekazanie niezbędnych informacji innym osobom medycznym uczestniczącym w świadczeniach"

- "ujawnienie tajemnicy może nastąpić wyłącznie w niezbędnym zakresie"

use\_in\_analysis:

- "weryfikuj podstawę ujawnienia informacji"

- "sprawdź, czy zakres ujawnienia był niezbędny"

- "łącz z UoOZP art. 50-52"

red\_flags:

- "ujawnienie szersze niż niezbędne"

- "brak zgody pacjenta przy informowaniu osoby bliskiej"

- "powoływanie się na bezpieczeństwo bez konkretnej przesłanki"

- "ujawnianie informacji osobom uczestniczącym w konflikcie, bez weryfikacji upoważnienia"

art\_15:

role: "relacja prawa zgody do ustaw odrębnych"

importance: "centralny dla styku z UoOZP"

relevance:

- "przepisy rozdziału o zgodzie stosuje się do zgody lub odmowy zgody, jeżeli przepisy odrębnych ustaw nie stanowią inaczej"

use\_in\_analysis:

- "przy psychiatrii zawsze sprawdzaj, czy UoOZP jako ustawa szczególna modyfikuje ogólny reżim zgody"

- "nie stosuj automatycznie ogólnej zgody z ustawy pacjenckiej, jeśli UoOZP ma przepis szczególny"

red\_flags:

- "uzasadnianie przyjęcia bez zgody wyłącznie ogólnymi przepisami o zgodzie"

- "pominięcie UoOZP jako lex specialis"

art\_16:

role: "prawo zgody lub odmowy po uzyskaniu informacji"

importance: "centralny"

relevance:

- "pacjent ma prawo wyrazić zgodę na określone świadczenia zdrowotne albo odmówić takiej zgody po uzyskaniu informacji z art. 9"

use\_in\_analysis:

- "sprawdź, czy zgoda lub odmowa były poprzedzone informacją"

- "stosuj przy leczeniu, diagnostyce, farmakoterapii i zabiegach"

- "odróżniaj zgodę na hospitalizację od zgody na konkretne świadczenie"

red\_flags:

- "zgoda bez uprzedniej informacji"

- "brak udokumentowania odmowy"

- "traktowanie braku sprzeciwu jako zgody mimo stanu pacjenta uniemożliwiającego świadome stanowisko"

art\_17:

role: "zgoda na badanie i świadczenia; sprzeciw pacjenta z dostatecznym rozeznaniem"

importance: "centralny"

relevance:

- "pacjent, w tym małoletni od 16 lat, ma prawo wyrazić zgodę na badanie lub inne świadczenia"

- "przedstawiciel ustawowy może wyrazić zgodę za pacjenta małoletniego, całkowicie ubezwłasnowolnionego lub niezdolnego do świadomego wyrażenia zgody"

- "pacjent chory psychicznie lub upośledzony umysłowo, lecz dysponujący dostatecznym rozeznaniem, ma prawo do sprzeciwu mimo zgody przedstawiciela"

- "zgoda i sprzeciw mogą być wyrażone ustnie albo przez zachowanie niebudzące wątpliwości"

use\_in\_analysis:

- "sprawdź, czy pacjent miał dostateczne rozeznanie"

- "sprawdź, czy sprzeciw został rozpoznany i odnotowany"

- "stosuj przy badaniach, leczeniu, diagnostyce i czynnościach pielęgnacyjnych"

red\_flags:

- "ignorowanie sprzeciwu pacjenta chorego psychicznie, mimo że mógł mieć dostateczne rozeznanie"

- "brak analizy zdolności do świadomego wyrażenia zgody"

- "brak dokumentacji zachowania pacjenta, z którego wywodzono zgodę lub odmowę"

art\_18:

role: "pisemna zgoda na zabieg operacyjny lub metodę podwyższonego ryzyka"

importance: "wysoki przy procedurach ryzykownych"

relevance:

- "przy zabiegu operacyjnym albo metodzie leczenia lub diagnostyki stwarzającej podwyższone ryzyko zgoda wymaga formy pisemnej"

- "przed wyrażeniem zgody pacjent ma prawo do informacji z art. 9 ust. 2"

use\_in\_analysis:

- "sprawdź, czy procedura była podwyższonego ryzyka"

- "sprawdź formę zgody"

- "sprawdź, czy informacja poprzedzała zgodę"

red\_flags:

- "brak pisemnej zgody przy procedurze podwyższonego ryzyka"

- "formularz zgody z pustymi polami lub bez informacji o ryzykach"

- "zgoda podpisana przy stanie świadomości podważającym rozeznanie"

art\_19:

role: "odesłanie do zasad świadczeń mimo braku zgody lub wobec sprzeciwu"

importance: "pomocniczy, ale ważny systemowo"

relevance:

- "zasady przeprowadzenia badania lub udzielenia świadczeń mimo braku zgody albo wobec sprzeciwu określają przepisy ustaw zawodowych, m.in. ustawy o zawodach lekarza i lekarza dentysty, ustawy o zawodzie ratownika medycznego, ustawy o zawodach pielęgniarki i położnej oraz ustawy o medycynie laboratoryjnej"

use\_in\_analysis:

- "gdy świadczenie wykonano mimo sprzeciwu, sprawdź nie tylko UoOZP i ustawę pacjencką, lecz także właściwą ustawę zawodową"

- "stosuj przy czynnościach somatycznych, ratunkowych, pielęgniarskich i laboratoryjnych"

red\_flags:

- "wykonanie świadczenia mimo sprzeciwu bez wskazania szczególnej podstawy"

- "automatyczne powołanie się na art. 23 UoOZP dla czynności, która wymaga oceny na gruncie ustawy zawodowej"

art\_20:

role: "prawo do poszanowania intymności i godności"

importance: "centralny przy przymusie"

relevance:

- "pacjent ma prawo do poszanowania intymności i godności, w szczególności w czasie udzielania świadczeń zdrowotnych"

use\_in\_analysis:

- "stosuj przy unieruchomieniu, izolacji, przymusowym podaniu leków, czynnościach higienicznych, cewnikowaniu, badaniach, obecności osób trzecich"

- "łącz z UoOZP art. 12, art. 18 ust. 9, art. 18d i art. 18e"

red\_flags:

- "unieruchomienie bez osłony od innych osób"

- "ekspozycja ciała bez konieczności"

- "czynności intymne przy nieuprawnionych osobach"

- "monitoring lub nadzór naruszający intymność ponad konieczność"

- "przymus zastosowany w sposób poniżający"

art\_20a:

role: "prawo do leczenia bólu"

importance: "istotny przy urazach, unieruchomieniu i procedurach somatycznych"

relevance:

- "pacjent ma prawo do leczenia bólu"

- "podmiot ma obowiązek określenia stopnia natężenia bólu, leczenia bólu i monitorowania skuteczności leczenia"

use\_in\_analysis:

- "sprawdź ocenę bólu przy urazach, unieruchomieniu, cewnikowaniu, wkłuciach, procedurach i powikłaniach"

- "sprawdź monitorowanie skuteczności leczenia bólu"

red\_flags:

- "brak skali bólu mimo dolegliwości"

- "brak leczenia bólu po przymusie lub procedurze"

- "brak monitorowania skuteczności leczenia bólu"

art\_21:

role: "obecność osoby bliskiej przy świadczeniach"

importance: "istotny"

relevance:

- "na życzenie pacjenta przy udzielaniu świadczeń może być obecna osoba bliska"

- "odmowa obecności osoby bliskiej może nastąpić przy prawdopodobieństwie zagrożenia epidemicznego lub ze względu na bezpieczeństwo zdrowotne pacjenta"

- "odmowę odnotowuje się w dokumentacji medycznej"

use\_in\_analysis:

- "sprawdź, czy pacjent żądał obecności osoby bliskiej"

- "sprawdź, czy odmowę odnotowano"

- "stosuj przy badaniu, przyjęciu, czynnościach intymnych i sytuacjach konfliktowych"

red\_flags:

- "odmowa obecności osoby bliskiej bez wpisu"

- "brak uzasadnienia bezpieczeństwem zdrowotnym"

- "wyłączenie osoby bliskiej przy czynności, w której pacjent potrzebował wsparcia komunikacyjnego"

art\_22:

role: "obowiązek zapewnienia intymności i godności; obecność osób trzecich"

importance: "centralny przy czynnościach z udziałem personelu i osób trzecich"

relevance:

- "osoba wykonująca zawód medyczny ma obowiązek postępować w sposób zapewniający poszanowanie intymności i godności pacjenta"

- "osoby inne niż udzielające świadczeń uczestniczą tylko wtedy, gdy jest to niezbędne ze względu na rodzaj świadczenia lub czynności kontrolne"

- "obecność innych osób wymaga zgody pacjenta albo właściwego przedstawiciela"

- "do tych osób stosuje się odpowiednio przepisy o tajemnicy"

use\_in\_analysis:

- "sprawdź, kto był obecny przy świadczeniu"

- "sprawdź, czy obecność była niezbędna"

- "sprawdź, czy była zgoda pacjenta"

- "stosuj przy przymusie, badaniach, cewnikowaniu, czynnościach higienicznych, monitoringu i asyście ochrony"

red\_flags:

- "obecność osób nieudzielających świadczeń bez zgody i bez konieczności"

- "brak odnotowania przyczyny obecności dodatkowych osób"

- "czynności intymne wykonywane przy osobach trzecich"

art\_23:

role: "prawo dostępu do dokumentacji medycznej"

importance: "centralny dowodowo"

relevance:

- "pacjent ma prawo dostępu do dokumentacji medycznej dotyczącej jego stanu zdrowia i udzielonych mu świadczeń"

- "dane w dokumentacji podlegają ochronie"

use\_in\_analysis:

- "stosuj przy każdym sporze o dokumentację"

- "sprawdź, czy pacjent uzyskał pełną dokumentację dotyczącą przyjęcia, leczenia i przymusu"

red\_flags:

- "odmowa dostępu bez podstawy"

- "wydanie tylko części dokumentacji"

- "brak dokumentów kluczowych: karta przymusu, rejestr, zlecenia, ocena zasadności, zgody, zawiadomienia"

art\_24:

role: "obowiązek prowadzenia, przechowywania, udostępniania i ochrony dokumentacji"

importance: "centralny dowodowo"

relevance:

- "podmiot ma obowiązek prowadzić, przechowywać i udostępniać dokumentację medyczną zgodnie z ustawą i ustawą o systemie informacji w ochronie zdrowia"

- "podmiot ma zapewnić ochronę danych zawartych w dokumentacji"

- "określa krąg osób uprawnionych do przetwarzania danych w dokumentacji"

- "osoby pomocnicze i techniczne mają obowiązek tajemnicy"

use\_in\_analysis:

- "sprawdź kompletność dokumentacji"

- "sprawdź bezpieczeństwo i uprawnienia dostępu"

- "stosuj przy systemach EDM, HIS, audytach dostępu i sporach o integralność dokumentacji"

red\_flags:

- "brak dokumentacji czynności istotnej prawnie"

- "brak ochrony danych"

- "dostęp osób nieuprawnionych"

- "zakłócenie dostępu do dokumentacji przez podmiot przetwarzający"

- "niewyjaśnione różnice między wersjami dokumentacji"

art\_25:

role: "minimalna treść dokumentacji medycznej"

importance: "centralny formalnie"

relevance:

- "dokumentacja zawiera co najmniej oznaczenie pacjenta"

- "dokumentacja zawiera oznaczenie podmiotu i komórki organizacyjnej"

- "dokumentacja zawiera opis stanu zdrowia pacjenta lub udzielonych świadczeń zdrowotnych"

- "dokumentacja zawiera datę sporządzenia"

- "w dokumentacji zamieszcza się informację o wydaniu opinii albo orzeczenia, o których mowa w art. 31 ust. 1"

use\_in\_analysis:

- "sprawdź, czy każdy dokument zawiera minimum ustawowe"

- "sprawdź, czy opis stanu zdrowia i świadczeń jest wystarczający"

- "sprawdź datę sporządzenia i identyfikację komórki"

red\_flags:

- "brak daty sporządzenia"

- "brak opisu świadczenia albo stanu zdrowia"

- "brak oznaczenia komórki organizacyjnej"

- "wpis niepozwalający ustalić, co faktycznie wykonano"

- "brak informacji o opinii/orzeczeniu mającym wpływ na prawa pacjenta"

art\_26:

role: "podmioty uprawnione do uzyskania dokumentacji"

importance: "centralny dla dostępu i kontroli"

relevance:

- "dokumentację udostępnia się pacjentowi, przedstawicielowi ustawowemu albo osobie upoważnionej przez pacjenta"

- "po śmierci pacjenta dokumentacja może być udostępniana wskazanym osobom, z uwzględnieniem sprzeciwu"

- "dokumentacja jest udostępniana m.in. Rzecznikowi Praw Pacjenta, Rzecznikowi Praw Pacjenta Szpitala Psychiatrycznego, sądom, prokuraturom i innym organom w zakresie wynikającym z zadań"

use\_in\_analysis:

- "ustal, czy żądający miał status uprawniony"

- "sprawdź, czy dokumentacja została udostępniona właściwemu organowi"

- "stosuj przy wnioskach do RPP, sądu, prokuratury i Rzecznika Praw Pacjenta Szpitala Psychiatrycznego"

red\_flags:

- "odmowa dokumentacji pacjentowi"

- "odmowa dokumentacji RPP lub sądowi mimo ustawowej podstawy"

- "udostępnienie osobie trzeciej bez upoważnienia"

- "brak weryfikacji sprzeciwu pacjenta lub osoby bliskiej po śmierci pacjenta"

art\_27:

role: "formy udostępniania dokumentacji i wykaz udostępnień"

importance: "centralny technicznie i dowodowo"

relevance:

- "dokumentacja może być udostępniona do wglądu, przez wyciąg, odpis, kopię, wydruk, oryginał, środki komunikacji elektronicznej albo nośnik danych"

- "podmiot prowadzi wykaz udostępnianej dokumentacji"

- "wykaz obejmuje m.in. sposób, zakres, osobę lub organ, osobę udostępniającą i datę udostępnienia"

use\_in\_analysis:

- "sprawdź, w jakiej formie wydano dokumentację"

- "sprawdź wykaz udostępnień"

- "porównaj zakres wydanej dokumentacji z zakresem żądania"

red\_flags:

- "brak wykazu udostępnień"

- "wydanie dokumentacji bez wskazania zakresu"

- "niezgodność między żądanym a wydanym zakresem"

- "brak podpisu osoby udostępniającej"

- "odmowa zdjęć/notatek przy wglądzie"

art\_28:

role: "opłaty za udostępnienie dokumentacji"

importance: "pomocniczy"

relevance:

- "podmiot może pobierać opłatę za niektóre formy udostępnienia dokumentacji"

- "opłaty nie pobiera się przy pierwszym udostępnieniu pacjentowi albo przedstawicielowi ustawowemu w żądanym zakresie i określonej formie"

- "ustawa określa maksymalne limity opłat"

use\_in\_analysis:

- "sprawdź, czy pobrano opłatę zasadnie"

- "sprawdź, czy pierwsze udostępnienie było bezpłatne"

red\_flags:

- "opłata za pierwsze udostępnienie pacjentowi"

- "opłata używana jako bariera dostępu"

- "opłata przekraczająca limit ustawowy"

art\_29:

role: "okresy przechowywania dokumentacji"

importance: "centralny dla zabezpieczenia dowodów"

relevance:

- "zasadniczy okres przechowywania dokumentacji wynosi 20 lat od końca roku kalendarzowego ostatniego wpisu"

- "dla dokumentacji w przypadku zgonu wskutek uszkodzenia ciała lub zatrucia okres wynosi 30 lat"

- "ustawa przewiduje szczególne okresy dla określonych rodzajów dokumentacji"

- "po upływie okresów dokumentacja jest niszczona w sposób uniemożliwiający identyfikację pacjenta"

use\_in\_analysis:

- "stosuj przy żądaniu zabezpieczenia dokumentacji"

- "sprawdź, czy dokumentacja nie została zniszczona przedwcześnie"

- "odróżniaj dokumentację medyczną od nagrań i danych, które mogą mieć odrębne okresy retencji"

red\_flags:

- "twierdzenie o braku dokumentacji mimo obowiązku przechowywania"

- "zniszczenie dokumentacji bez podstawy"

- "brak procedury zabezpieczenia dokumentacji w sporze"

art\_30:

role: "delegacja do rozporządzenia o dokumentacji medycznej"

importance: "centralny dla rzetelności dokumentacji"

relevance:

- "minister określa rodzaje i zakres dokumentacji medycznej oraz sposób jej przetwarzania"

- "delegacja uwzględnia konieczność realizacji prawa dostępu, rzetelnego prowadzenia dokumentacji, ochrony danych oraz jednolitych wzorów dokumentacji"

use\_in\_analysis:

- "zawsze sprawdź właściwe rozporządzenie o dokumentacji medycznej"

- "porównaj dokumentację szpitala z wymaganym rodzajem, zakresem i sposobem prowadzenia"

red\_flags:

- "dokumentacja niezgodna z wymaganym zakresem"

- "brak rzetelności wpisów"

- "brak danych wymaganych przez rozporządzenie"

- "niejednolite lub pozasystemowe formularze bez podstawy"

art\_30a:

role: "postępowanie z dokumentacją po zaprzestaniu działalności"

importance: "kontekstowy, ale ważny przy archiwum"

relevance:

- "w razie zaprzestania działalności dokumentacja musi być przekazana w sposób zabezpieczający przed zniszczeniem, uszkodzeniem, utratą i dostępem osób nieuprawnionych"

- "ustawa określa podmioty odpowiedzialne za przechowywanie i udostępnianie dokumentacji"

- "do tych podmiotów stosuje się odpowiednio przepisy o tajemnicy, dokumentacji i jej udostępnianiu"

use\_in\_analysis:

- "stosuj przy problemach z archiwum, likwidacją podmiotu, zmianą operatora lub przejęciem dokumentacji"

red\_flags:

- "brak ustalenia podmiotu odpowiedzialnego za dokumentację"

- "utrata dokumentacji przy reorganizacji"

- "odmowa archiwum bez wskazania podstawy"

art\_31:

role: "sprzeciw wobec opinii albo orzeczenia lekarza"

importance: "wysoki przy opiniach wpływających na prawa pacjenta"

relevance:

- "pacjent lub przedstawiciel ustawowy mogą wnieść sprzeciw wobec opinii albo orzeczenia lekarza, jeżeli opinia albo orzeczenie ma wpływ na prawa lub obowiązki pacjenta wynikające z przepisów prawa"

- "sprzeciw wnosi się do Komisji Lekarskiej przy RPP za pośrednictwem RPP"

- "termin wynosi 30 dni od dnia wydania opinii albo orzeczenia"

- "sprzeciw wymaga uzasadnienia i wskazania przepisu prawa"

- "Komisja wydaje orzeczenie na podstawie dokumentacji i w miarę potrzeby po badaniu"

- "orzeczenie wydaje się niezwłocznie, nie później niż w terminie 30 dni od wniesienia sprzeciwu"

use\_in\_analysis:

- "rozważ, czy opinia lub orzeczenie psychiatryczne wpływało na prawa pacjenta"

- "sprawdź, czy pacjent mógł skorzystać ze sprzeciwu"

- "stosuj ostrożnie, bo przepis nie zastępuje trybów odwoławczych z UoOZP i KPC"

red\_flags:

- "brak informacji o możliwości sprzeciwu wobec opinii/orzeczenia"

- "opinia wpływająca na prawa pacjenta bez realnej ścieżki zakwestionowania"

- "pomieszanie sprzeciwu do RPP z kontrolą sądu opiekuńczego w trybie UoOZP"

art\_32:

role: "Komisja Lekarska przy RPP"

importance: "pomocniczy dla art. 31"

relevance:

- "Komisja Lekarska składa się z trzech lekarzy powołanych przez RPP"

- "dwóch lekarzy ma być tej samej specjalności co lekarz, który wydał opinię albo orzeczenie"

use\_in\_analysis:

- "stosuj przy ocenie mechanizmu sprzeciwu wobec opinii lub orzeczenia"

red\_flags:

- "brak właściwej specjalności przy ocenie opinii"

- "brak realnego rozpoznania sprzeciwu"

art\_33:

role: "prawo do kontaktu osobistego, telefonicznego i korespondencyjnego"

importance: "centralny przy hospitalizacji"

relevance:

- "pacjent podmiotu stacjonarnego i całodobowego ma prawo do kontaktu osobistego, telefonicznego lub korespondencyjnego z innymi osobami"

- "pacjent ma prawo odmówić kontaktu"

use\_in\_analysis:

- "sprawdź, czy pacjent miał kontakt z rodziną, pełnomocnikiem, osobami bliskimi, RPP lub sądem"

- "łącz z UoOZP art. 13, który szczególnie wzmacnia prawo komunikacji w szpitalu psychiatrycznym"

red\_flags:

- "odcięcie telefonu bez podstawy"

- "brak możliwości kontaktu z bliskimi lub pełnomocnikiem"

- "kontakt ograniczony faktycznie mimo braku formalnej decyzji"

- "kontakt wymuszany mimo odmowy pacjenta"

art\_34:

role: "prawo do dodatkowej opieki pielęgnacyjnej"

importance: "pomocniczy"

relevance:

- "pacjent ma prawo do dodatkowej opieki pielęgnacyjnej"

- "dodatkowa opieka nie polega na udzielaniu świadczeń zdrowotnych"

use\_in\_analysis:

- "stosuj, gdy pacjent wymaga wsparcia osoby bliskiej lub opiekuna"

- "odróżniaj opiekę pielęgnacyjną od świadczeń medycznych"

red\_flags:

- "nieuzasadnione wyłączenie osoby wspierającej pacjenta"

- "mylenie obecności opiekuna z udzielaniem świadczeń medycznych"

art\_35:

role: "koszty kontaktu i dodatkowej opieki"

importance: "pomocniczy"

relevance:

- "pacjent ponosi koszty realizacji praw z art. 33 i 34, jeśli skutkują kosztami dla podmiotu"

- "informacja o wysokości opłaty i sposobie jej ustalenia jest jawna"

use\_in\_analysis:

- "stosuj przy sporach o koszty kontaktu lub opieki"

red\_flags:

- "opłaty niejawne"

- "opłaty używane jako bariera dla kontaktu lub opieki"

art\_39:

role: "depozyt rzeczy wartościowych"

importance: "istotny przy przyjęciu i przymusie"

relevance:

- "pacjent przebywający w podmiocie stacjonarnym i całodobowym ma prawo do przechowywania rzeczy wartościowych w depozycie"

use\_in\_analysis:

- "sprawdź, co stało się z rzeczami pacjenta przy przyjęciu, przymusie, izolacji lub unieruchomieniu"

- "łącz z UoOZP art. 18a ust. 2, gdy odebrano przedmioty niebezpieczne"

red\_flags:

- "brak spisu rzeczy odebranych pacjentowi"

- "brak depozytu lub potwierdzenia odbioru"

- "mieszanie odebrania przedmiotów niebezpiecznych z depozytem rzeczy wartościowych"

art\_40:

role: "delegacja do rozporządzenia o depozycie"

importance: "pomocniczy"

relevance:

- "minister określa zakres spisu przedmiotów oddawanych do depozytu, sposób zabezpieczenia oraz prowadzenia księgi depozytów"

use\_in\_analysis:

- "sprawdź rozporządzenie i procedurę depozytową"

red\_flags:

- "brak księgi depozytów"

- "brak spisu przedmiotów"

- "brak zabezpieczenia rzeczy pacjenta"

art\_40a:

role: "pełnomocnik do spraw praw pacjenta w podmiocie"

importance: "istotny organizacyjnie"

relevance:

- "kierownik podmiotu może utworzyć stanowisko pełnomocnika do spraw praw pacjenta"

- "pełnomocnik wspiera realizację obowiązku przestrzegania praw pacjenta"

- "zadania obejmują udział w rozpatrywaniu skarg, analizę nieprawidłowości i proponowanie działań naprawczych oraz szkolenia"

- "RPP współpracuje z pełnomocnikami"

use\_in\_analysis:

- "sprawdź, czy podmiot miał pełnomocnika i czy skarga została do niego skierowana"

- "stosuj przy naruszeniach organizacyjnych i powtarzalnych"

red\_flags:

- "brak analizy nieprawidłowości po skardze"

- "brak działań naprawczych"

- "pełnomocnik łączy funkcje w sposób budzący obawy co do bezstronności"

art\_41:

role: "ustanowienie Rzecznika Praw Pacjenta"

importance: "centralny dla ścieżki RPP"

relevance:

- "w celu ochrony praw pacjenta ustanawia się Rzecznika Praw Pacjenta"

use\_in\_analysis:

- "stosuj jako punkt wyjścia dla skargi do RPP"

red\_flags:

- "pomijanie ścieżki RPP w sprawach praw pacjenta"

art\_42:

role: "status Rzecznika Praw Pacjenta"

importance: "centralny ustrojowo"

relevance:

- "Rzecznik jest centralnym organem administracji rządowej właściwym w sprawach ochrony praw pacjentów"

- "Rzecznik wykonuje zadania przy pomocy Biura RPP"

use\_in\_analysis:

- "stosuj przy określaniu właściwego organu dla skargi pacjenckiej"

red\_flags:

- "kierowanie sprawy wyłącznie do podmiotu leczniczego mimo potrzeby zewnętrznej kontroli RPP"

art\_47:

role: "zadania Rzecznika Praw Pacjenta"

importance: "centralny"

relevance:

- "Rzecznik prowadzi postępowania w sprawach praktyk naruszających zbiorowe prawa pacjentów"

- "Rzecznik prowadzi postępowania wyjaśniające"

- "Rzecznik wykonuje zadania w sprawach cywilnych"

- "Rzecznik chroni prawa pacjentów korzystających ze świadczeń szpitala psychiatrycznego"

- "to zadanie realizuje w szczególności przy pomocy Rzeczników Praw Pacjenta Szpitala Psychiatrycznego"

- "Rzecznik analizuje skargi pacjentów w celu identyfikacji zagrożeń i obszarów wymagających naprawy"

use\_in\_analysis:

- "stosuj przy decyzji, czy kierować sprawę do RPP"

- "łącz z UoOZP art. 10a-10d i art. 56 ustawy pacjenckiej"

- "w sprawach psychiatrycznych rozważ równolegle RPP ogólnego i Rzecznika Praw Pacjenta Szpitala Psychiatrycznego"

red\_flags:

- "brak kontaktu z Rzecznikiem Praw Pacjenta Szpitala Psychiatrycznego mimo hospitalizacji psychiatrycznej"

- "brak reakcji RPP/pełnomocnika na skargę dotyczącą przymusu"

- "traktowanie sprawy jako wyłącznie indywidualnego sporu mimo możliwych problemów systemowych"

art\_47a:

role: "przetwarzanie danych przez RPP"

importance: "istotny dla skargi i dokumentów"

relevance:

- "Rzecznik może przetwarzać informacje, w tym dane osobowe niezbędne do realizacji ustawowych zadań"

- "Rzecznik przetwarza dane szczególnych kategorii wyłącznie w celu ochrony praw pacjentów przy realizacji zadań ustawowych"

- "dane podlegają zabezpieczeniom"

use\_in\_analysis:

- "stosuj przy przekazywaniu dokumentacji i danych do RPP"

- "sprawdź, czy obawy o dane osobowe nie są niezasadnie używane do blokowania postępowania"

red\_flags:

- "odmowa przekazania RPP informacji z powołaniem na ochronę danych mimo ustawowej podstawy"

- "brak zabezpieczenia danych w postępowaniu"

art\_50:

role: "wszczęcie postępowania wyjaśniającego przez RPP"

importance: "centralny proceduralnie"

relevance:

- "Rzecznik wszczyna postępowanie wyjaśniające, gdy poweźmie wiadomość co najmniej uprawdopodabniającą naruszenie praw pacjenta"

- "wiadomość obejmuje w szczególności oznaczenie wnioskodawcy, oznaczenie pacjenta i zwięzły opis stanu faktycznego"

- "wniosek do Rzecznika jest wolny od opłat"

- "Rzecznik może wszcząć postępowanie z własnej inicjatywy"

use\_in\_analysis:

- "przygotuj stan faktyczny pod kątem uprawdopodobnienia naruszenia"

- "nie przeciążaj wniosku hipotezami; wskaż konkretne prawa i dokumenty"

red\_flags:

- "brak oznaczenia pacjenta albo stanu faktycznego"

- "wniosek zbudowany wyłącznie na ocenach, bez faktów i dokumentów"

- "pominięcie możliwości działania RPP z urzędu przy sprawie poważnej lub systemowej"

art\_51:

role: "decyzje RPP po zapoznaniu się z wnioskiem"

importance: "procesowy"

relevance:

- "RPP może podjąć sprawę"

- "RPP może wskazać środki prawne"

- "RPP może przekazać sprawę według właściwości"

- "RPP może nie podjąć sprawy"

use\_in\_analysis:

- "przygotuj wniosek tak, aby minimalizować ryzyko potraktowania sprawy jako nieodpowiedniej dla RPP"

- "wskazuj naruszenia praw pacjenta, nie tylko spór medyczny"

red\_flags:

- "wniosek nie identyfikuje praw pacjenta"

- "brak żądania adekwatnego do kompetencji RPP"

art\_52:

role: "uprawnienia RPP w postępowaniu wyjaśniającym"

importance: "centralny dowodowo"

relevance:

- "RPP może samodzielnie prowadzić postępowanie wyjaśniające"

- "RPP może zwrócić się o zbadanie sprawy do organów nadzoru, prokuratury, kontroli państwowej, zawodowej lub społecznej"

- "RPP może zbadać sprawę na miejscu, nawet bez uprzedzenia"

- "RPP może żądać wyjaśnień i dostępu do dokumentów od podmiotów udzielających świadczeń"

- "RPP może żądać informacji o stanie spraw prowadzonych przez sądy, prokuraturę i inne organy po zakończeniu postępowania"

- "RPP może zlecać ekspertyzy i opinie"

use\_in\_analysis:

- "wskazuj dokumenty, których RPP powinien zażądać"

- "przy poważnych brakach dokumentacyjnych wnioskuj o zbadanie sprawy na miejscu"

- "stosuj przy przymusie, dokumentacji, monitoringu, rejestrach i procedurach"

red\_flags:

- "podmiot odmawia dokumentów lub wyjaśnień"

- "brak kontroli na miejscu mimo zarzutów dotyczących dokumentacji i przymusu"

- "brak żądania dokumentów kluczowych dla oceny przymusu"

art\_53:

role: "wynik postępowania RPP"

importance: "centralny dla skutków skargi"

relevance:

- "RPP może stwierdzić brak naruszenia"

- "RPP może skierować wystąpienie do podmiotu, organu, organizacji lub instytucji, gdzie stwierdził naruszenie"

- "RPP może zwrócić się do organu nadrzędnego o zastosowanie środków przewidzianych prawem"

- "w wystąpieniu RPP formułuje opinie lub wnioski co do sposobu załatwienia sprawy"

- "RPP może żądać wszczęcia postępowania dyscyplinarnego lub zastosowania sankcji służbowych"

- "adresat wystąpienia ma obowiązek poinformować RPP o działaniach lub stanowisku nie później niż w terminie 30 dni"

- "wnioskodawcy przysługuje wniosek o ponowne rozpatrzenie sprawy przy niestwierdzeniu naruszenia"

- "po utrzymaniu rozstrzygnięcia przysługuje skarga do sądu administracyjnego"

use\_in\_analysis:

- "formułuj żądania tak, aby RPP mógł wskazać działania naprawcze"

- "śledź termin 30 dni na odpowiedź adresata wystąpienia"

- "przy negatywnym rozstrzygnięciu rozważ wniosek o ponowne rozpatrzenie"

red\_flags:

- "wystąpienie RPP bez realnych działań naprawczych"

- "brak odpowiedzi podmiotu w terminie"

- "brak wykorzystania wniosku o ponowne rozpatrzenie mimo słabego rozstrzygnięcia"

art\_55:

role: "udział RPP w sprawach cywilnych"

importance: "wysoki procesowo"

relevance:

- "w sprawach cywilnych dotyczących naruszenia praw pacjenta RPP może z urzędu lub na wniosek żądać wszczęcia postępowania albo brać udział w toczącym się postępowaniu na prawach prokuratora"

use\_in\_analysis:

- "rozważ wniosek o udział RPP w postępowaniu cywilnym, gdy sprawa dotyczy naruszenia praw pacjenta"

- "stosuj przy naruszeniach godności, informacji, zgody, dokumentacji i praw psychiatrycznych"

red\_flags:

- "sprawa cywilna prowadzona bez rozważenia wsparcia RPP, mimo silnego komponentu praw pacjenta"

art\_56:

role: "Rzecznicy Praw Pacjenta Szpitala Psychiatrycznego jako pracownicy Biura RPP"

importance: "centralny dla psychiatrii"

relevance:

- "Rzecznicy Praw Pacjenta Szpitala Psychiatrycznego są pracownikami Biura RPP"

- "wykonują swoje zadania przy pomocy Biura RPP"

use\_in\_analysis:

- "łącz z UoOZP art. 10a-10d"

- "ustal, czy pacjent psychiatryczny miał realny dostęp do właściwego rzecznika"

red\_flags:

- "brak informacji o Rzeczniku Praw Pacjenta Szpitala Psychiatrycznego"

- "brak możliwości kontaktu z rzecznikiem"

- "skarga psychiatryczna potraktowana jak zwykła skarga administracyjna bez uwzględnienia szczególnej roli rzecznika psychiatrycznego"

art\_59:

role: "praktyka naruszająca zbiorowe prawa pacjentów"

importance: "wysoki przy problemach systemowych"

relevance:

- "praktyką naruszającą zbiorowe prawa pacjentów są bezprawne zorganizowane działania lub zaniechania podmiotów udzielających świadczeń zdrowotnych mające na celu pozbawienie pacjentów praw lub ograniczenie tych praw"

- "zakazane jest stosowanie praktyk naruszających zbiorowe prawa pacjentów"

- "suma praw indywidualnych nie jest zbiorowym prawem pacjentów"

use\_in\_analysis:

- "stosuj, gdy materiał wskazuje na procedurę, wzorzec, systemową praktykę albo powtarzalny model naruszeń"

- "odróżniaj indywidualny błąd od zorganizowanego działania lub zaniechania"

red\_flags:

- "powtarzalny brak kart przymusu"

- "systemowy brak pouczeń o prawach"

- "rutynowe ograniczanie kontaktu"

- "procedura oddziałowa ograniczająca prawa pacjentów ponad ustawę"

art\_61:

role: "żądanie dokumentów i informacji w sprawie praktyk zbiorowych"

importance: "dowodowy przy naruszeniach systemowych"

relevance:

- "w postępowaniu dotyczącym praktyk naruszających zbiorowe prawa pacjentów RPP może żądać dokumentów i informacji dotyczących okoliczności stosowania praktyk"

- "termin na udzielenie informacji nie może być dłuższy niż 30 dni"

- "żądanie powinno wskazywać zakres informacji, cel, termin i pouczenie o sankcjach"

use\_in\_analysis:

- "stosuj przy wnioskach o zbadanie wzorca działania szpitala"

- "wskazuj konkretne dokumenty: procedury, rejestry, wzory kart, szkolenia, audyty"

red\_flags:

- "brak odpowiedzi na żądanie RPP"

- "odpowiedź ogólnikowa bez dokumentów"

- "informacje nieprawdziwe lub wprowadzające w błąd"

art\_64:

role: "decyzja RPP w sprawie praktyki naruszającej zbiorowe prawa pacjentów"

importance: "wysoki przy działaniach naprawczych"

relevance:

- "RPP w decyzji nakazuje zaniechanie praktyki albo wskazuje działania niezbędne do usunięcia skutków naruszenia"

- "decyzji nadaje się rygor natychmiastowej wykonalności"

- "RPP może nałożyć obowiązek składania informacji o realizacji działań"

- "ciężar udowodnienia zaprzestania praktyki spoczywa na podmiocie"

use\_in\_analysis:

- "stosuj przy żądaniu działań naprawczych wobec podmiotu leczniczego"

- "ważne, gdy problem nie dotyczy tylko jednego pacjenta"

red\_flags:

- "podmiot deklaruje zmianę praktyki bez dowodów"

- "brak informacji o wykonaniu działań naprawczych"

- "brak usunięcia skutków naruszenia"

art\_67q\_67zd:

role: "świadczenie kompensacyjne za zdarzenie medyczne"

importance: "kontekstowy, ale potencjalnie istotny przy szkodzie medycznej"

relevance:

- "rozdział dotyczy zdarzeń medycznych zaistniałych w trakcie udzielania albo w efekcie udzielenia lub zaniechania udzielenia świadczeń opieki zdrowotnej finansowanych ze środków publicznych w szpitalu"

- "świadczenie kompensacyjne może dotyczyć zakażenia, uszkodzenia ciała, rozstroju zdrowia albo śmierci pacjenta"

- "wniosek składa się do RPP"

- "do wniosku dołącza się posiadaną dokumentację medyczną i inne dokumenty potwierdzające stan faktyczny albo informację o ich braku"

- "RPP ma dostęp do dokumentacji medycznej niezbędnej do rozpatrzenia wniosku"

- "RPP może żądać informacji, wyjaśnień i dokumentów od podmiotu udzielającego świadczeń"

- "po wypłacie świadczenia podmiot analizuje przyczyny źródłowe zdarzenia i wdraża zalecenia poprawy jakości i bezpieczeństwa"

use\_in\_analysis:

- "stosuj tylko wtedy, gdy poza naruszeniem praw pacjenta występuje szkoda kwalifikowalna jako zdarzenie medyczne"

- "nie myl ścieżki kompensacyjnej z kontrolą legalności art. 23 UoOZP"

- "może być przydatne przy urazach, rozstroju zdrowia, powikłaniach przymusu, braku diagnostyki albo błędach leczenia"

red\_flags:

- "skupienie wyłącznie na kompensacji, gdy główny problem dotyczy legalności przymusu"

- "brak dokumentacji medycznej dołączonej do wniosku albo brak informacji o jej braku"

- "podmiot nie analizuje przyczyn źródłowych po zdarzeniu"

art\_68:

role: "kara za niewykonanie decyzji RPP dotyczącej praktyki zbiorowej"

importance: "egzekucyjny"

relevance:

- "RPP nakłada karę pieniężną do 500 000 zł w przypadku niepodjęcia działań określonych w decyzji z art. 64 ust. 1"

use\_in\_analysis:

- "stosuj przy niewykonaniu decyzji dotyczącej praktyki zbiorowej"

red\_flags:

- "podmiot ignoruje decyzję RPP"

- "brak działań w terminie wskazanym w decyzji"

art\_69:

role: "kara za nieprzekazanie dokumentów lub informacji RPP"

importance: "egzekucyjny i dowodowy"

relevance:

- "RPP nakłada karę pieniężną do 50 000 zł za nieprzekazanie dokumentów lub informacji, o których mowa w art. 61 lub art. 67z ust. 1 pkt 2"

use\_in\_analysis:

- "stosuj przy odmowie dokumentów w sprawie praktyk zbiorowych albo świadczenia kompensacyjnego"

red\_flags:

- "podmiot nie przekazuje żądanych dokumentów"

- "podmiot opóźnia lub utrudnia dostęp do informacji"

art\_69a:

role: "kara za naruszenia dotyczące dokumentacji po zaprzestaniu działalności"

importance: "kontekstowy dla archiwizacji"

relevance:

- "kara dotyczy niedopełnienia obowiązków z art. 30a w zakresie postępowania z dokumentacją medyczną po zaprzestaniu działalności"

- "organ uwzględnia rodzaj i wagę naruszeń"

use\_in\_analysis:

- "stosuj przy problemach z archiwum, likwidacją, utratą dokumentacji lub brakiem podmiotu odpowiedzialnego"

red\_flags:

- "brak zabezpieczenia dokumentacji po zmianach organizacyjnych"

- "utrata dokumentacji w archiwum"

- "brak podmiotu odpowiedzialnego za udostępnienie dokumentacji"

art\_70:

role: "kryteria wysokości kar pieniężnych"

importance: "pomocniczy"

relevance:

- "przy ustalaniu wysokości kar z art. 68 i 69 uwzględnia się okres, stopień i okoliczności naruszenia oraz uprzednie naruszenie przepisów ustawy"

use\_in\_analysis:

- "stosuj przy ocenie wagi uporczywego lub powtarzalnego naruszenia"

red\_flags:

- "długotrwałe utrudnianie dostępu do dokumentów"

- "powtarzalne naruszenia mimo wcześniejszych skarg"



crosswalk\_with\_uoopz:

art23\_uoopz\_admission\_without\_consent:

patient\_rights\_articles:

- "art. 2"

- "art. 6"

- "art. 8"

- "art. 9"

- "art. 11"

- "art. 15"

- "art. 16"

- "art. 17"

- "art. 23"

- "art. 24"

- "art. 25"

- "art. 26"

- "art. 31"

- "art. 47"

- "art. 50-53"

- "art. 56"

analysis\_questions:

- "czy pacjent został poinformowany o stanie zdrowia, rozpoznaniu i prawach"

- "czy tryb bez zgody był jasno odróżniony od trybu zgody"

- "czy dokumentacja zawiera minimalne ustawowe elementy"

- "czy pacjent miał dostęp do dokumentacji i ścieżki skargowej"

- "czy opinia/orzeczenie wpływające na prawa pacjenta mogło być kwestionowane właściwą ścieżką"

direct\_coercion:

patient\_rights\_articles:

- "art. 2"

- "art. 6"

- "art. 8"

- "art. 9"

- "art. 12a"

- "art. 13"

- "art. 14"

- "art. 20"

- "art. 20a"

- "art. 21"

- "art. 22"

- "art. 23"

- "art. 24"

- "art. 25"

- "art. 27"

- "art. 30"

- "art. 39"

- "art. 40"

analysis\_questions:

- "czy zastosowanie przymusu było udokumentowane jako świadczenie/czynność dotycząca stanu zdrowia"

- "czy zachowano godność i intymność"

- "czy ograniczono obecność osób trzecich do niezbędnego minimum"

- "czy monitorowano ból i skutki farmakoterapii"

- "czy odebrane rzeczy zostały zabezpieczone lub zdeponowane"

- "czy pacjent ma dostęp do pełnej dokumentacji przymusu"

treatment\_without\_consent:

patient\_rights\_articles:

- "art. 6"

- "art. 8"

- "art. 9"

- "art. 12a"

- "art. 15"

- "art. 16"

- "art. 17"

- "art. 18"

- "art. 19"

- "art. 20"

- "art. 23-30"

analysis\_questions:

- "czy świadczenie było objęte szczególną podstawą z UoOZP lub ustawy zawodowej"

- "czy pacjent otrzymał informację"

- "czy leczenie odpowiadało aktualnej wiedzy medycznej"

- "czy zgłoszone działania niepożądane zostały odnotowane"

- "czy dokumentacja pozwala odtworzyć decyzję, wskazania, ryzyka i wykonanie"

documentation\_dispute:

patient\_rights\_articles:

- "art. 3"

- "art. 23"

- "art. 24"

- "art. 25"

- "art. 26"

- "art. 27"

- "art. 28"

- "art. 29"

- "art. 30"

- "art. 30a"

- "art. 52"

- "art. 69"

- "art. 69a"

analysis\_questions:

- "czy dokumentacja została wydana pacjentowi w pełnym zakresie"

- "czy dokumentacja zawiera minimalne ustawowe elementy"

- "czy istnieje wykaz udostępnień"

- "czy podmiot prowadził i przechowywał dokumentację zgodnie z obowiązkiem"

- "czy RPP może żądać dokumentów lub zbadać sprawę na miejscu"

contact\_and\_family:

patient\_rights\_articles:

- "art. 3"

- "art. 5"

- "art. 9"

- "art. 13"

- "art. 14"

- "art. 21"

- "art. 22"

- "art. 33"

- "art. 34"

- "art. 35"

analysis\_questions:

- "czy osoba kontaktująca się była osobą bliską, opiekunem faktycznym lub osobą upoważnioną"

- "czy pacjent wyraził zgodę na przekazanie informacji"

- "czy pacjent miał kontakt telefoniczny, osobisty lub korespondencyjny"

- "czy ograniczenie kontaktu miało podstawę i było proporcjonalne"

- "czy odmowę obecności osoby bliskiej odnotowano"

rpp\_path:

patient\_rights\_articles:

- "art. 40a"

- "art. 41"

- "art. 42"

- "art. 47"

- "art. 47a"

- "art. 50"

- "art. 51"

- "art. 52"

- "art. 53"

- "art. 55"

- "art. 56"

- "art. 59"

- "art. 61"

- "art. 64"

- "art. 68"

- "art. 69"

- "art. 70"

analysis\_questions:

- "czy sprawa dotyczy indywidualnego naruszenia praw pacjenta"

- "czy sprawa może wskazywać na praktykę naruszającą zbiorowe prawa pacjentów"

- "czy RPP powinien żądać dokumentów, wyjaśnień, kontroli na miejscu lub opinii"

- "czy istnieje potrzeba działań naprawczych, dyscyplinarnych lub udziału RPP w sprawie cywilnej"



patient\_rights\_red\_flag\_taxonomy:

high\_weight:

- "brak informacji pacjenta o stanie zdrowia, rozpoznaniu, proponowanym leczeniu lub prawach przy jednoczesnym trybie przymusowym"

- "świadczenie wykonane mimo sprzeciwu bez jasnej szczególnej podstawy"

- "przymus lub czynności intymne wykonane z naruszeniem godności i intymności"

- "brak dokumentacji czynności istotnej dla wolności, zgody, leczenia lub przymusu"

- "odmowa dostępu do dokumentacji pacjentowi albo uprawnionemu organowi"

- "dokumentacja nie zawiera minimalnych elementów z art. 25"

- "ograniczenie kontaktu pacjenta bez podstawy, bez proporcjonalności albo bez dokumentacji"

- "ujawnienie informacji medycznych osobie trzeciej bez zgody lub innej podstawy"

- "brak reakcji na zgłoszone działania niepożądane leków"

- "ignorowanie prawa pacjenta z dostatecznym rozeznaniem do sprzeciwu"

- "brak możliwości kontaktu z Rzecznikiem Praw Pacjenta Szpitala Psychiatrycznego"

- "systemowa praktyka ograniczająca prawa pacjentów ponad ustawę"

medium\_weight:

- "brak wpisu o żądaniu konsultacji lub odmowie konsultacji"

- "brak wpisu o odmowie obecności osoby bliskiej"

- "brak wykazu udostępnień dokumentacji"

- "niepełna informacja o prawach pacjenta"

- "opłaty za dokumentację stosowane jako bariera dostępu"

- "brak spisu rzeczy pacjenta lub dokumentacji depozytu"

- "brak informacji o osobie udostępniającej dokumentację"

- "brak jasnego rozróżnienia zgody na hospitalizację, zgody na leczenie i zgody na przekazanie informacji"

contextual:

- "spór rodzinny wpływający na obieg informacji medycznej"

- "pacjent w stanie utrudniającym rozumienie informacji bez dostosowania komunikacji"

- "wiele wersji dokumentacji bez wyjaśnienia"

- "skarga pacjenta rozpatrzona wyłącznie formalnie"

- "naruszenie indywidualne mogące wskazywać na praktykę systemową"

- "zdarzenie mogące równolegle stanowić naruszenie praw pacjenta i zdarzenie medyczne"



analysis\_workflow\_extension:

step\_1\_identify\_patient\_rights\_layer:

question: "Które prawa pacjenta są uruchomione przez stan faktyczny?"

possible\_rights:

- "prawo do świadczeń zgodnych z aktualną wiedzą medyczną"

- "prawo do należytej staranności"

- "prawo do informacji"

- "prawo do informacji o prawach pacjenta"

- "prawo do zgody albo odmowy"

- "prawo do sprzeciwu"

- "prawo do godności i intymności"

- "prawo do leczenia bólu"

- "prawo do tajemnicy"

- "prawo do kontaktu z innymi osobami"

- "prawo do dokumentacji medycznej"

- "prawo do skargi do RPP"

required\_output:

- "wymień prawa bezpośrednio dotknięte"

- "wymień prawa pośrednio dotknięte"

- "oddziel prawa z ustawy pacjenckiej od szczególnych praw z UoOZP"

step\_2\_information\_and\_consent\_test:

questions:

- "czy pacjent uzyskał informację z art. 9"

- "czy pacjent uzyskał informację o prawach z art. 11"

- "czy zgoda lub odmowa były świadome"

- "czy sprzeciw pacjenta został rozpoznany"

- "czy stan pacjenta pozwalał na dostateczne rozeznanie"

- "czy UoOZP lub ustawy zawodowe przewidywały wyjątek od zgody"

required\_output:

- "status informacji"

- "status zgody"

- "status sprzeciwu"

- "podstawa odstąpienia od zgody, jeśli wystąpiła"

step\_3\_dignity\_and\_intimacy\_test:

questions:

- "czy czynności naruszały intymność lub godność"

- "czy obecność osób trzecich była niezbędna"

- "czy była zgoda na obecność innych osób"

- "czy zapewniono osłonę, prywatność i minimalną dolegliwość"

- "czy działania były proporcjonalne do celu medycznego"

required\_output:

- "opis czynności ingerujących w godność/intymność"

- "osoby obecne"

- "podstawa obecności"

- "ocena proporcjonalności"

step\_4\_documentation\_test:

questions:

- "czy dokumentacja istnieje"

- "czy dokumentacja jest kompletna"

- "czy zawiera minimum z art. 25"

- "czy została udostępniona pacjentowi lub uprawnionemu podmiotowi"

- "czy istnieje wykaz udostępnień"

- "czy dokumentacja pozwala odtworzyć decyzje, osoby, godziny i podstawy prawne"

required\_output:

- "lista dokumentów dostępnych"

- "lista dokumentów brakujących"

- "niespójności wersji"

- "wnioski dowodowe"

step\_5\_confidentiality\_and\_contact\_test:

questions:

- "komu ujawniono informacje"

- "czy pacjent upoważnił tę osobę"

- "czy ujawnienie miało inną podstawę"

- "czy zakres ujawnienia był niezbędny"

- "czy pacjent miał możliwość kontaktu osobistego, telefonicznego lub korespondencyjnego"

- "czy ograniczenia kontaktu były udokumentowane"

required\_output:

- "mapa ujawnień informacji"

- "status upoważnień"

- "ograniczenia kontaktu"

- "naruszenia tajemnicy"

step\_6\_rpp\_route\_test:

questions:

- "czy sprawa nadaje się do wniosku do RPP"

- "czy sprawa dotyczy pacjenta psychiatrycznego i wymaga zaangażowania Rzecznika Praw Pacjenta Szpitala Psychiatrycznego"

- "czy są podstawy do postępowania wyjaśniającego"

- "czy są podstawy do kontroli na miejscu"

- "czy są podstawy do żądania dokumentów i wyjaśnień"

- "czy problem może mieć charakter praktyki zbiorowej"

required\_output:

- "rekomendowana ścieżka RPP"

- "dokumenty do zażądania"

- "potencjalne działania RPP"

- "czy sprawa jest indywidualna, systemowa czy mieszana"



documents\_to\_request\_patient\_rights\_layer:

information\_and\_consent:

- "formularze zgody"

- "wpisy o przekazaniu informacji pacjentowi"

- "pouczenia o prawach pacjenta"

- "pouczenia z UoOZP"

- "wpisy o odmowie zgody lub sprzeciwie"

- "wpisy o zdolności pacjenta do świadomego wyrażenia zgody"

- "wpisy o żądaniu konsultacji lub konsylium"

- "wpisy o odmowie konsultacji"

dignity\_intimacy\_and\_contact:

- "wpisy pielęgniarskie"

- "wpisy lekarskie opisujące czynności intymne"

- "dokumentacja obecności osób trzecich"

- "odmowa obecności osoby bliskiej"

- "decyzje lub wpisy o ograniczeniu kontaktu"

- "regulamin oddziału"

- "procedury odwiedzin i telefonów"

- "dokumentacja depozytu rzeczy"

- "spis przedmiotów odebranych pacjentowi"

documentation\_access:

- "wniosek o dokumentację"

- "potwierdzenie wydania dokumentacji"

- "wykaz udostępnień dokumentacji"

- "zakres wydanej dokumentacji"

- "korespondencja z archiwum"

- "informacja o podmiocie odpowiedzialnym za przechowywanie dokumentacji"

- "audyt dostępu do EDM/HIS, jeśli dostępny"

- "wersje dokumentacji wydane w różnych datach"

rpp\_route:

- "wniosek do RPP"

- "odpowiedź RPP"

- "wezwania RPP do podmiotu"

- "wyjaśnienia podmiotu dla RPP"

- "wystąpienie RPP"

- "informacja podmiotu o działaniach po wystąpieniu RPP"

- "wniosek o ponowne rozpatrzenie"

- "skarga do sądu administracyjnego, jeśli dotyczy"

- "korespondencja z Rzecznikiem Praw Pacjenta Szpitala Psychiatrycznego"



output\_format\_for\_combined\_skill: recommended\_sections: - "1. Tryb UoOZP" - "2. Warstwa praw pacjenta" - "3. Informacja, zgoda i sprzeciw" - "4. Godność, intymność i obecność osób trzecich" - "5. Przymus bezpośredni i skutki medyczne" - "6. Dokumentacja medyczna i dostęp" - "7. Tajemnica i kontakt z osobami bliskimi" - "8. RPP / Rzecznik Praw Pacjenta Szpitala Psychiatrycznego" - "9. Czerwone flagi wysokiej wagi" - "10. Wnioski stanowcze" - "11. Dokumenty do pozyskania" - "12. Realistyczne alternatywy wymagające wyjaśnienia"

conclusion\_logic: strong\_patient\_rights\_violation\_indicator: if\_any: - "brak informacji pacjenta przy istotnej decyzji medycznej" - "brak realnej zgody lub zignorowany sprzeciw" - "brak dokumentacji czynności ingerującej w prawa pacjenta" - "naruszenie godności lub intymności przy przymusie albo czynności intymnej" - "odmowa dokumentacji bez podstawy" - "ujawnienie informacji osobie trzeciej bez zgody lub podstawy" - "ograniczenie kontaktu bez podstawy" - "brak możliwości kontaktu z RPP lub Rzecznikiem Praw Pacjenta Szpitala Psychiatrycznego" output\_style: - "formułuj wniosek stanowczo, jeśli dokumenty są jednoznaczne" - "używaj języka: naruszenie prawa pacjenta, brak udokumentowania realizacji prawa, brak podstawy w dokumentacji, wymaga wyjaśnienia przez podmiot" - "nie ratuj dokumentacji hipotezami technicznymi bez przesłanki"

combined\_uoopz\_patient\_rights\_indicator:

if:

- "ten sam stan faktyczny narusza szczególny wymóg UoOZP i ogólne prawo pacjenta"

output\_style:

- "wskaż oba poziomy naruszenia osobno"

- "najpierw opisz naruszenie szczególnego reżimu UoOZP"

- "następnie opisz naruszenie ogólnej gwarancji pacjenckiej"

- "nie mieszaj podstaw prawnych w jednym zdaniu bez rozdzielenia funkcji norm"

insufficient\_material\_indicator:

if:

- "brak dokumentacji pozwalającej ocenić realizację prawa pacjenta"

output\_style:

- "nie przesądzaj ponad materiał"

- "wskaż dokładnie, którego dokumentu brakuje"

- "oznacz brak jako problem dowodowy"

- "jeśli obowiązek dokumentacyjny wynika z ustawy, wskaż brak jako czerwoną flagę"



factual\_guardian\_limited\_consent: rule: - "opiekun faktyczny może wyrazić zgodę na badanie tylko w określonych sytuacjach" - "opiekun faktyczny nie zastępuje przedstawiciela ustawowego przy zgodzie na świadczenia zdrowotne wykraczające poza badanie" - "zgoda opiekuna faktycznego na procedurę medyczną, do której nie jest uprawniony, jest prawnie irrelewantna" red\_flags: - "świadczenie wykonane u małoletniego na podstawie zgody osoby będącej tylko opiekunem faktycznym" - "brak ustalenia statusu osoby wyrażającej zgodę" - "zgoda babci/dziadka/osoby towarzyszącej potraktowana jak zgoda przedstawiciela ustawowego"
