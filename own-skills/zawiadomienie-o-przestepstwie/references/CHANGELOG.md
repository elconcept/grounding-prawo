# Historia zmian

## v0.4 (2026-10-15) — integralność narracji
- Dokończenie po przerwanej sesji Astry: przywrócone frazy wyzwalające w opisie skilla; tabela skilli pomocniczych kieruje szturm/atak/adversarial do recenzji rozszerzającej (R4a: czyny i naruszenia praw, których autor nie nazwał, także przez organy) zamiast mandatu przeciwnika.
- Uzupełnienie po audycie `INBOX/20261010_AUDYT_SKILLI_kolizje_zawiadomienia.md`: zamknięta kolizja A2 (HYBRID/BLOCK ZERO), doprecyzowane A3 (draft a dane formalne), A6 (pochodzenie edycji/kwoty z relacji), A7 (brak repo nie blokuje). Wbrew dawnemu zaleceniu A9 „bez zmian” dodano ochronę także w punktach wejścia recenzji zgodnie z późniejszą instrukcją użytkownika.
- Kontrakt między modułami w `shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md`, źródło `selection/overlay/shared/`; wyjątki w routerze i patchu 06 dla HYBRID, FAKTY, CLAIM, FSL/LSL, ataku, adversarial i kwalifikatora. Szturm oraz profil mają własny warunek wejścia; most nie wymusza automatycznej recenzji.
- Poprawki po testach: data względna zakotwiczona w relacji, kontrola przesłanki pytania o wcześniejszy zapis, bez domyślnego autorstwa cytatu; formalna gotowość oddzielona od zakończenia redakcji.
- HARDGATE-ZOP chroni relację także po recenzji lub załadowaniu korpusu dowodowego. Brak zewnętrznego dowodu nie usuwa ani nie osłabia epizodu.
- HARDGATE-A kontroluje kompletność wywiadu z możliwością świadomego zakończenia przez autora; AUDYT-B ujawnia różnice bez blokady złożenia. Zastępuje blokujący K5 z v0.3.
- Wywiad adaptacyjny, gałęzie KWALIFIKACJA+, przegląd skutków/wzorca/następstw/instytucji/pilności, podsumowanie do korekty; bez zgadywania cudzej perspektywy.
- Rozdzielone narracja, tropy i informacje praktyczne; mapa zawiera źródło i pewność pamięci. Prawo z historycznego katalogu wymaga ponownej weryfikacji dla sprawy.
- Zachowane preferencje autora dotyczące pierwszej osoby, otwarcia, wniosku o ściganie i listy przepisów; wyjaśniono ich zakres i brak blokady przy niezweryfikowanej kwalifikacji.
- Pochodzenie: [pochodzenie i memo researchowe](research.md) (38 pozycji, w tym duplikaty). Narracja/tropy: źródła 1–4, 8, 14; wywiad/skutki: 1–10, 12, 15–17, 24, 27, 30, 34–36; bezpieczeństwo: 7, 12, 23, 36; routing/aktualność: 13, 18–22, 25–26, 28–29, 32–33, 37. Blogi służą projektowaniu pytań, nie ustalaniu aktualnego prawa.
- Rozszerzone evale behawioralne do 21 scenariuszy. [Forward-test](../evals/20261015-forward-test.md): 11 dokładnych promptów i 6 wariantów pokrywających 17 ID, z jawnymi błędami oraz retestami. [Test integracji](../evals/20261015-integration-test.md): cztery próby po audycie, zakres i ograniczenia oraz rzeczywisty test adaptera syntezy. Nie deklaruje pełnego testu DOCX ani wielokrotnej stabilności modelu.

## v0.3 (2026-10-10)
- Zapis według `shared/ARTEFAKTY-SPRAWY.md`: mapa krzywd i raport HARDGATE jako pliki inkrementalne pisma
  (`_MAPA_KRZYWD.md`, `_HARDGATE.md`), jednorazowe pliki w `_robocze/`.

## v0.2.1 (2026-10-10)
- Wspólne pożycie: uchwała 7 sędziów SN z 25.02.2016, I KZP 20/15 i postanowienie SN z 4.03.2015,
  IV KO 98/14 - zweryfikowane w SAOS przez Tor (rotator), citator ręczny; doktryna: M. Kubica,
  OSAP XV/3 (2017), OCR w `04_opracowania/` (the-ocr, Azure DI). task014 zamknięty.

## v0.2 (2026-10-09) - decyzje autora
- Nazwa: `zawiadomienie-o-przestepstwie` (bez `-pl`).
- Otwarcie jak we wzorze Policji (gov.pl): „Zawiadamiam o popełnieniu na moją szkodę przestępstwa …
  i wnoszę o wszczęcie postępowania”; tytuł „Zawiadomienie o popełnieniu przestępstwa”; bez
  „podejrzenia” i „możliwości popełnienia”.
- Lista przepisów na końcu pisma: numer ze zweryfikowanego t.j. + prosty opis, stanowczo („Uważam,
  że opisane zachowania są przestępstwami określonymi w …”). W narracji nadal bez przepisów.
- Wniosek o ściganie zawsze i obowiązkowo.
- HARDGATE obejmuje też relacje innych osób (źródło szczegółów, zakres informacyjny); każda
  informacja od innej osoby w piśmie ma wskazane źródło. Nowa klasa „rozbieżność pozorna” i test
  pozornej sprzeczności; wzorzec błędu N.C. „partner” / „obcy” (art. 115 § 11 k.k., trzy więzi
  wspólnego pożycia); zakaz strofowania autora.
- K4: przepisy o fałszywym zawiadomieniu / zeznaniu / oskarżeniu zweryfikowane (art. 238, 233, 234,
  8, 9 § 1 k.k.).
- Katalog krzywd: przepisy i tryb ścigania zweryfikowane w Kodeksie karnym t.j. Dz.U. 2025 poz. 383
  (baza `mcp/cache/kodeks/kodeks_karny.md`); przepisy k.p.k. (12, 17, 49, 119, 303-307, 325a)
  z t.j. Dz.U. 2026 poz. 490 (PDF z ISAP, odczyt PyMuPDF).
- Evals: dodany przypadek 4 (pozorna sprzeczność) i asercje dla decyzji.

## v0.1 (2026-10-09)
- Scaffolding: SKILL.md (kanon K1-K5, przebieg F0-F8, kolizje z innymi skillami), references
  (wywiad, mapa-krzywd, hardgate-spojnosc, styl, oczami-prokuratora, forma), assets/szablon.md,
  scripts/rejestr_relacji.py, evals/evals.json.
- K4 według korekty autora: przed odpowiedzialnością za fałszywe zawiadomienie chroni dobra wiara,
  nie ostrożność sformułowań; rozróżnienie fakt / wniosek / hipoteza służy czytelności.
- Plan i materiał źródłowy: `dokumentacja/20261009_plan_skill_zawiadomienie_o_przestepstwie.md`.

## 0.5 — 2026-10-17

- Pojedyncze pytania i zapis po odpowiedzi; wywiad trwa do decyzji autora o przerwie,
  braku dalszych wspomnień lub opracowaniu obecnego materiału.
- Trwała pełna relacja MD, wejście z istniejącego pliku, historia korekt i wersje sesyjne.
- Rejestr pism: nowe wersje niezłożonych projektów, uzupełnienia i wnioski po złożeniu,
  osobne zgłoszenia nowych krzywd; dobór do rzeczywistego etapu sprawy.

## 0.7 — 2026-10-18 (decyzje autorki z sesji relacji N.C.)

- Basic Memory jako baza danych relacji: `legal`, `relacje/<autor-slug>/` (relacja, log, rejestr,
  pytania otwarte, wersje, archiwum); pliki relacji tylko awaryjnie bez dostępu do bazy; procedura
  migracji plików. Nowy plik `references/basic-memory-relacja.md`.
- Pełna lista pytań otwartych w każdej odpowiedzi sesji relacji; ponawianie i przeformułowanie
  pytań bez odpowiedzi; odpowiedzi zbiorcze przypisywane po treści.
- Pisma w `output/` bez placeholderów: najbardziej prawdopodobna wartość danej formalnej i pytanie;
  luk faktów nie zapełnia się domysłem. Jedna wersja w `output/`, usunięcie po `cmp` z `drafty/`.
- Ręczna edycja autora w `.docx` ma pierwszeństwo; zachowanie edytowanego pliku w `drafty/`.
- „Nie obciążaj mnie”, dane o zdrowiu osób trzecich tylko za zgodą, skutki w każdym piśmie, którego dotyczą.
- Pisma towarzyszące torem procesowym (weryfikacja przepisów); zawiadomienie bez HYBRID-VALIDATION.
- `forma.md`: oświadczenie o zgodzie na e-doręczenia (art. 119 § 1 pkt 2 lit. a k.p.k.) dopiero od wejścia w życie brzmienia.

## 0.6 — 2026-10-17

- Rozdzielenie chronologicznej relacji i dopisywanego logu zeznań z sesji.
- Nowe wspomnienia porządkują całą oś czasu; stałe ID pozostają po przeniesieniu epizodów.
- Korekty zachowują historię w logu; import starszych relacji bez fikcyjnych dat sesji.
