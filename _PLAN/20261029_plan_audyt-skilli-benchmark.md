# Audyt skilli i plan przebudowy z benchmarkiem (29.10.2026)

Źródło: 11 zgłoszeń właściciela z 29.10.2026. Każdy punkt: stan zastany (z dowodem), diagnoza, plan, kryterium
ukończenia. Kolejność wykonania i decyzje do podjęcia na końcu.

Zasada nadrzędna tego planu: **żadna zmiana skilla nie idzie na `main` bez przebiegu benchmarku** (pkt 11).
Push na `main` jest wydaniem (klienci aktualizują się po SHA), więc benchmark musi stać przed przebudową, nie po niej.

---

## 1. `case-risk`: scaffolding wpięty jako pełny skill

**Stan.** `own-skills/case-risk/SKILL.md` (8,9 KB) to matryca waga × prawdopodobieństwo, kategorie A-H po 2-3
zdaniach i szablon raportu. Scalone moduły `medical-consent` (art. 192 k.k.) i `uoozp-compliance` (UoOZP) są
pełniejsze od samego hosta. Brak: powiązania z `analizator-dowodow-v3` (siła dowodowa A-D), z `chronologia-sprawy-v1`,
z Basic Memory (rejestr ryzyk w teczce), brak skali kalibracyjnej na przykładach, brak testów i evals.
Router wpina go jako etap oceny szans, choć `analiza-sadowa-v6` ma własną ocenę szans: dwa źródła tej samej oceny.

**Plan.**
1. Ustalić jedną funkcję: rejestr ryzyk sprawy (żywy, w teczce BM, pozycje ze stałym ID `R-n` jak `F-n` w
   `ARTEFAKTY-SPRAWY.md`), a nie kolejna analiza szans. Ocena szans zostaje w `analiza-sadowa-v6`.
2. Wejście: mapa faktów i dowodów z `analizator-dowodow-v3`, oś z `chronologia-sprawy-v1`; wyjście: rejestr ryzyk
   z właścicielem, terminem i działaniem (spina się z pkt 2: ryzyko terminowe trafia do rejestru terminów).
3. Kategorie A-H rozpisać na listy kontrolne pod profil spraw (wykroczenia i karne z udziałem Policji, prokuratura,
   hospitalizacja psychiatryczna, dokumentacja medyczna, RODO po stronie podmiotu), każda z przykładem kalibracji.
4. Evals: 3 sprawy wzorcowe (anonimizacja niewymagana, ale bez sprawy w toku jako jedynego wzorca) z oczekiwanym
   rejestrem; wejście do benchmarku (pkt 11, zadanie B4).

**Gotowe, gdy:** rejestr ryzyk ma schemat, zapis w BM, evals przechodzą, benchmark nie pokazuje regresji oceny szans.

---

## 2. `kalkulatory-procesowe-pl`: rejestr sprawy i terminów w Basic Memory

**Stan.** Skill liczy (opłaty, WPS, odsetki, przedawnienie, moduł `terminy-procesowe-pl`), ale nic nie utrzymuje.
`shared/BASIC-MEMORY.md:69` przewiduje w teczce sekcję „Terminy”, bez schematu i bez skilla, który ją pisze.
Upstream ma gotowy przepis agenta tła `vendor/packs/awesome-matematic-skills/przepisy-agentow/wachta-terminow/`
(czytelnik akt → licznik terminów → redaktor alertów, data zawsze „kandydat do sprawdzenia”), nie wpięty w selekcję.

**Plan.**
1. Schemat notatki `sprawy/<katalog>/_stan` w BM (frontmatter + sekcje): sygnatury (Policja, prokuratura, sąd,
   UODO, inne organy; z datą nadania i źródłem), organy i referenci, terminy rozpraw/posiedzeń, pisma złożone
   (data nadania, data doręczenia, sposób, UPO/nadawczy), terminy zakreślone zarządzeniem (treść, data doręczenia
   zarządzenia, termin, rygor), terminy ustawowe (podstawa, zdarzenie wyzwalające, data doręczenia, czy zawity,
   skutek uchybienia, wniosek o przywrócenie), status każdego terminu (`otwarty`/`dochowany`/`uchybiony`/`nieaktualny`).
2. Każdy termin powstaje wyłącznie z karty terminu (moduł `terminy-procesowe-pl`): zdarzenie, dokument i strona,
   podstawa z `ustawy_artykul`, sposób liczenia (art. 111-115 KC, art. 165 KPC, art. 123 KPK, art. 38 KPW),
   wynik oznaczony do sprawdzenia przez użytkownika. Nigdy z pamięci modelu.
3. Wyzwalacze zapisu: ingest nowego dokumentu (`wiki-basic-memory`, `odczyt-dokumentow`), złożenie pisma
   (`pisma-*`, `zawiadomienie-o-przestepstwie`), wejście routera (odczyt `_stan` i przypomnienie terminów ≤ 7 dni
   i zawitych ≤ 14 dni na starcie każdej sesji w sprawie).
4. Przypomnienia poza sesją: przepis `wachta-terminow` jako zaplanowany agent (hook lub routine) czytający `_stan`
   wszystkich spraw i zapisujący alert do BM (`main/alerty/`), bez wysyłki zewnętrznej bez zgody.
5. Nazwa: funkcja przekracza „kalkulatory”. Zgodnie z zasadą „nowa funkcja do istniejącego skilla” rejestr jest
   modułem `kalkulatory-procesowe-pl/modules/rejestr-sprawy`, a opis skilla dostaje wyzwalacze „terminy sprawy”,
   „sygnatury”, „co mam złożyć”, „przypomnij terminy”. Alternatywa do decyzji: osobny skill `stan-sprawy`.
6. Migracja: jednorazowe wypełnienie `_stan` dla spraw w `legal/sprawy/` z istniejących akt (okładki, zarządzenia,
   pisma) z kartą terminu przy każdej pozycji; wynik do przeglądu użytkownika.

**Gotowe, gdy:** każda sprawa ma `_stan` w BM, router pokazuje zbliżające się terminy na starcie, test na fixture
(zarządzenie z terminem 7 dni, doręczenie zastępcze, termin zawity na zażalenie) daje poprawne daty z kartą.

---

## 3. `odczyt-dokumentow`: z konwertera w normalizator gotowego Markdown

**Stan.** `own-skills/odczyt-dokumentow/SKILL.md` opisuje OCR (`the-ocr-ingest-page`, łańcuch providerów, konektor
`ocr`), a `references/opendataloader-pdf.md` jest sprzeczny z nim: „Część skilla `the-ocr`” (skill usunięty),
Windows (`opendataloader-pdf.exe`, `Scripts/`, „Eclipse Adoptium JDK 17”), katalog `Konwerter/` i
„Batch > 10 PDF → zapytaj Wiesława przed startem” (linia 70, artefakt upstreamu MateMatic). `pdftotext` jest
zalecany w `patron-przeglad-tabelaryczny/scripts/doc_to_text.py:92`, `patron-weryfikacja-cytatow`
i `cofniecie-pozwu-ze-zrzeczeniem-roszczenia` (dla PDF tekstu jednolitego). Brak jakiejkolwiek reguły struktury MD.

Rzeczywisty przepływ: OCR do MD robi użytkownik przy każdym nowym dokumencie; model dostaje gotowy MD. Przykład
z akt (`legal/sprawy/III_Ko_96_26_pobicie_noc_27sie/akta/AKTA_II_W_1342_26.md`) ma defekty, które skill powinien
wyłapać: znacznik `k2-3_..._protokol_zawiadomienia.pdf (Page 1/4)`, a strony 2-4 jako `k2_...` (niespójna nazwa),
`(Page 1-4/4)` zamiast znacznika na każdej stronie, brak znormalizowanego frontmattera.

**Docelowy kontrakt MD (do zatwierdzenia):**
- frontmatter: `title`, `type: dokument`, `sprawa`, `sygnatury[]`, `data_dokumentu`, `autor/organ`, `zrodlo_pdf`,
  `strony` (liczba), `ocr` (provider, data), `stan_normalizacji` (`surowy`/`znormalizowany`/`zweryfikowany_z_pdf`),
- każdy dokument w pliku: otwiera `## <document_name>`, zamyka `---`,
- każda strona: `==< <document_name> (Page x/y) >==`, gdzie `document_name` = nazwa pliku PDF, `x` kolejny od 1,
  `y` stałe w obrębie dokumentu i równe liczbie stron PDF.

**Plan.**
1. Nowy SKILL.md: normalizacja i walidacja MD; OCR tylko jako ścieżka awaryjna („brak MD: poproś użytkownika
   o OCR albo użyj konektora `ocr`”). Usunąć `references/opendataloader-pdf.md` i opis `the-ocr-ingest-page`
   z treści głównej; ingest PDF zostaje w `wiki-basic-memory`.
2. Skrypt `scripts/normalizuj_md.py` (deterministyczny, z testami w `tests/`): sprawdza nagłówek, zamknięcie,
   ciągłość `x`, stałość `y`, zgodność nazwy w znaczniku z nagłówkiem, frontmatter; tryb `--fix` dla poprawek
   mechanicznych (rozbicie `Page 1-4/4` wymaga PDF), raport JSON z listą stron do porównania z PDF.
3. Porównanie z PDF przy wątpliwości: liczba stron (PyMuPDF), tekst warstwy (MarkItDown/PyMuPDF zamiast
   `pdftotext`), a dla skanów obraz strony do oceny przez model; korekta MD z oznaczeniem w frontmatterze.
4. Ujednolicić ekstrakcję tekstu w całym pluginie: MarkItDown/PyMuPDF zamiast `pdftotext` (3 miejsca wyżej) albo
   świadoma decyzja, gdzie `pdftotext -layout` zostaje (PDF tekstu jednolitego z tabelami).
5. Fixtures: wycinek prawdziwego `AKTA_*.md` z defektami i oczekiwanym raportem.

**Gotowe, gdy:** skrypt wykrywa wszystkie defekty z fixture, `lint_refs.py` czysty, w pluginie nie ma `Wiesław`,
`Konwerter/`, `.exe`, `the-ocr` jako skilla.

---

## 4. `patron-przeglad-tabelaryczny`: generyczny szablon kancelaryjny

**Stan.** Opis: „umowy, NDA, SPA, najmy, umowy o pracę, kredytowe… due diligence, change of control review”.
`references/szablony-kolumn.json` (58 KB): 11 szablonów po angielsku (`coc-dd` „Change of Control Review”,
praktyka „Corporate”, kolumny „Parties”, prompty po angielsku). `doc_to_text.py` używa `pdftotext`.
Równolegle w archiwum jest `przeglad-tabelaryczny` z IURA (14 KB) i w selekcji `drop` z powodem „kancelaria”.

**Plan.** Dwie opcje (decyzja D4):
- **A (zalecana).** Przebudowa pod akta: szablony PL dla dokumentów spraw właściciela (protokoły czynności Policji
  i prokuratury: data, godzina, funkcjonariusz, czynność, cytat, sprzeczność z innym protokołem; dokumentacja
  medyczna: wpis, osoba, godzina, zlecenie, podstawa przymusu; korespondencja z organami: data, sygnatura, żądanie,
  termin odpowiedzi; decyzje i postanowienia: organ, rozstrzygnięcie, pouczenie, termin zaskarżenia → rejestr pkt 2).
  Wejście: znormalizowany MD z pkt 3 (znaczniki stron dają cytat i stronę bez `pdftotext`). Usunąć szablony
  korporacyjne.
- **B.** Wycofać skill (archive); funkcję zestawienia przejmuje `analizator-dowodow-v3` + `chronologia-stanowiska-pl`.

**Gotowe, gdy:** opis i szablony są po polsku, pod profil spraw, a test na fixture (3 protokoły) daje tabelę
z poprawną stroną w każdej komórce.

---

## 5. `rodo-dsar-pl`: perspektywa administratora zamiast podmiotu

**Stan.** Opis w `selection.yaml:57` przepisano na „własne żądanie wobec administratora”, ale treść upstreamu
została: „Żądanie podmiotu to zegar… decyzję o realizacji/odmowie i wysyłkę podejmuje administrator”, Krok 3
„Draft odpowiedzi + rejestr”, `gdpr_deadlines.py` liczy termin odpowiedzi administratora. Opis i treść sobie przeczą.

**Plan (zalecany: przebudowa jako własny skill, nie patch upstreamu).** `own-skills/rodo-zadania-podmiotu`
(albo moduł w `dr-11`), funkcje po stronie właściciela:
1. Żądanie (art. 15-22 RODO) do administratora: wybór prawa, zakres, identyfikacja bez nadmiarowych danych,
   żądanie kopii danych (art. 15 ust. 3), informacji o odbiorcach, źródle, okresie przechowywania.
2. Zegar po stronie podmiotu: art. 12 ust. 3 (1 miesiąc + przedłużenie o 2 z obowiązkiem poinformowania),
   wpis do rejestru terminów z pkt 2; `gdpr_deadlines.py` zostaje jako kalkulator, przepięty na tę perspektywę.
3. Ocena odpowiedzi administratora: kompletność wobec art. 15, zasadność odmowy (art. 12 ust. 5, art. 23 RODO,
   przepisy sektorowe: dokumentacja medyczna, akta postępowań karnych), luki.
4. Eskalacja: wezwanie ostateczne → skarga do Prezesa UODO (`uodo-grounding-pl` do orzecznictwa UODO) → droga
   cywilna art. 79/82 RODO. Skarga do UODO jako pismo z pełną kontrolą (pkt 10), nie jako „pismo proste”.
5. Upstream `rodo-dsar-pl` usunąć z `keep` (do `drop` z powodem „strona administratora”, jak `rodo-dpia-pl`).

**Gotowe, gdy:** w treści nie ma instrukcji dla administratora, termin trafia do `_stan`, eval: odpowiedź
szpitala na żądanie kopii dokumentacji z niepełnym zakresem → wskazanie luk i projekt wezwania.

---

## 6. `teczka-sprawy`: scaffolding z dwóch skryptów

**Stan.** SKILL.md 1,3 KB: uruchom `dokumenty_sprawy.py`, potem `teczka.py` → trzy DOCX. Brak opisu formatu
briefu, spisu i podsumowania, brak powiązania z `_dokumenty.md`/`_brief.md` z `ARTEFAKTY-SPRAWY.md`, brak testów,
wymaga `LEGAL_WORKSPACE`, `pandoc`, `python-docx` (nie działa w Cowork bez plików). Pokrywa się z rejestrem
z pkt 2 (stan sprawy) i z indeksem akt z pkt 3.

**Plan.** Decyzja D6: teczka jako **widok** (eksport DOCX) rejestru `_stan` i indeksu akt, nie jako osobne źródło.
1. Źródło prawdy: BM (`_stan`, indeks dokumentów z frontmatterów pkt 3); skrypty tylko renderują.
2. Specyfikacja trzech dokumentów (zawartość, kolejność, format zgodny z `FORMAT-PISMA.md`), z przykładem.
3. Albo wariant minimalny: scalić jako moduł `wiki-basic-memory/modules/teczka` (eksport), usuwając osobny skill.

**Gotowe, gdy:** DOCX powstaje z BM bez ręcznego briefu, test na sprawie wzorcowej.

---

## 7. `ralph-loop`, `implementation-planning`, `plan-review`, `karpathy-guidelines`, `hookify`

**Stan.** W tym repo, w pluginie `grounding-prawo` (ani w wersji synced 0032 z 29.10.2026) i w `legal/.claude`
żadnego z nich nie ma. Lokalnie istnieją tylko: `~/.agents/skills/ralph-loop` (własny, CLI dla 3 agentów)
oraz `hookify` i `ralph-loop` w pobranym marketplace `claude-plugins-official` (niewłączone w kontenerze).
`implementation-planning`, `plan-review`, `karpathy-guidelines` nie występują nigdzie na NAS.
Wniosek: są włączone w innym miejscu (konto claude.ai / Cowork, organizacja, inny marketplace). Decyzja D7:
wskazać, gdzie je widać; plan zależy od tego, czy mają wejść do pluginu (wtedy: przegląd, przekład, dopasowanie
do pracy nad pismami jak pętla szturmu) czy zostać narzędziami deweloperskimi tego repo (`.claude/skills/`).

---

## 8. `/transkrypcja`: komenda ad hoc

**Stan.** `commands/transkrypcja.md` (1 KB) każe modelowi przepisać rozmowę z pamięci kontekstu „dosłownie”.
Model nie ma dosłownego dostępu do całej historii po kompaktowaniu, więc wynik jest rekonstrukcją, a „dosłownie”
jest fikcją. Ścieżka zgadywana („katalog repozytorium określ na podstawie bieżącego workspace”). Brak schematu
pliku i brak użycia w pętli doskonalenia (nikt nie czyta `INBOX/` metodycznie).

**Plan.**
1. Źródło deterministyczne: skrypt czytający JSONL sesji Claude Code (`~/.claude/projects/<projekt>/<sesja>.jsonl`)
   i eksportujący prompty, odpowiedzi, wywołania skilli i zapisane artefakty; model dodaje tylko ocenę na końcu.
   W Cowork bez dostępu do JSONL: komenda zapisuje uczciwie „rekonstrukcja” w frontmatterze.
2. Schemat wpisu (frontmatter: sprawa, data, skille, ocena użytkownika, zgłoszone wady) pod pętlę z pkt 11:
   wada z transkrypcji → przypadek regresyjny w benchmarku.
3. Rozważyć hook `SessionEnd` zamiast komendy (wzór: plugin `handoff-doc` w synced).

---

## 9. Scalenia bez raportu: co zniknęło

Dowód: commity `40752040` (14.10.2026) i `8e739192` (porządki). Porównanie źródeł z wynikiem:

| Element | Stan | Ocena |
|---|---|---|
| IURA `pozew-cywilny`, `odpowiedz-na-pozew`, `apelacja-karna`, `zazalenie-na-postanowienie-prokuratora`, `zarzuty-do-opinii-bieglego`, `cofniecie-pozwu-…`, `wniosek-o-rozprawe-zdalna`, `notatka-prawna`, `eu-legal-memo` | moduły `pisma-procesowe-v3/modules/typy/*.md`, treść zachowana i rozszerzona (np. `apelacja-karna` 28,2 → 32,3 KB) | treść jest; **problem w wywołaniu**: tabela typów jest na linii ~855 z 52 KB SKILL.md, a opis skilla nie wymienia typów, więc model nie dociera do instrukcji pisma |
| IURA `decyzja-procesowa-prokuratora` (17,6 KB) | `archive/`, nie ma w pluginie | **utracone** |
| IURA `przeglad-umow` | referencja `analizator-umow-v1/modules/klauzule-kontraktowe-pl` | zachowane |
| IURA `przeglad-tabelaryczny` | `archive/`, zamiast niego generyczny `patron-przeglad-tabelaryczny` | zastąpione gorszym (pkt 4) |
| `pierwsze-wrazenie-sedziego-pl` i 6 innych soczewek | moduły `szturm-na-draft-pl/modules/*`, treść zachowana (różnica: frontmatter, blok shared-rules upstreamu, odwołanie do `let-it-be`; dopisany wyjątek zawiadomienia) | treść jest; **utracona tania iteracja**: brak osobnego wywołania, opis szturmu wymusza pełny cykl („każda soczewka obowiązkowa i pełna”); sekcja „Pojedyncza soczewka na żądanie” (`SKILL.md:130`) istnieje, ale żaden opis nie prowadzi do niej |
| matematic `jakosc-tresci`: `humanizer-pl`, `marko-pl-content` | `humanizer-pl` jako własna adaptacja, `marko-pl-content` jako soczewka szturmu | treść jest; `marko` działa tylko w szturmie, nie przy zwykłej redakcji (`pisz-po-polsku` → `humanizer-pl`) |
| matematic `akta-przeszukiwalne-pl`, `doc-intel-contract-pl` | usunięte w `dabca861` bez wpisu w `drop` | do oceny przy pkt 3 |

Spadek jakości pism ma więc dwie mierzalne hipotezy: (H1) instrukcje typu pisma nie są wczytywane, (H2) redakcja
zwykłego pisma omija soczewki jakości, bo działają tylko w pełnym szturmie. Obie sprawdzi benchmark (pkt 11, B3).

**Plan.**
1. Przywrócić `decyzja-procesowa-prokuratora` jako moduł typu w `pisma-procesowe-v3` (fold z IURA).
2. Przenieść tabelę typów na początek `pisma-procesowe-v3/SKILL.md` (patch) i dodać typy do opisu skilla.
3. `pierwsze-wrazenie-sedziego-pl` jako tani tryb: komenda `/pierwsze-wrazenie` albo skill-wrapper z własnym
   opisem kierujący do `szturm-na-draft-pl/modules/pierwsze-wrazenie-sedziego-pl` w trybie jednej soczewki
   bez pętli (decyzja D9: to odstępstwo od reguły „bez duplikatów funkcji”, więc wymaga zgody właściciela).
4. Raport scaleń jako stały artefakt: `scripts/report.py` generuje przy każdym buildzie tabelę
   „źródło → miejsce w pluginie → rozmiar przed/po”, a `build.py` odrzuca skill, który zniknął bez wpisu `drop`.

---

## 10. `pisma-proste-v2`: katalog niepasujący do profilu

**Stan.** 33 KB SKILL.md + 21 referencji (~220 KB). Schematy: sprzeciw, zarzuty, zawezwanie, ostateczne wezwanie,
reklamacja, odstąpienie, wypowiedzenie, interpretacje podatkowe/ZUS/GIP, skarga na komornika, oświadczenie SKD,
skarga do UODO. Z profilu właściciela pasuje tylko wezwanie i ostateczne wezwanie; skarga do UODO w jego sprawach
nie jest pismem prostym. `selection.yaml:26` trzyma skill, bo `shared` odwołuje się do niego 21 razy.

**Plan.**
1. Patch: zostawić schematy wezwanie/ostateczne wezwanie (i ewentualnie wniosek o wgląd/kopie akt, wniosek
   o sporządzenie uzasadnienia, wniosek o doręczenie, prośbę o informację o stanie sprawy: typowe pisma
   proste w sprawach karnych i wykroczeniowych; decyzja D10), resztę usunąć z pluginu regułą w `build.py`.
2. Skargę do UODO przenieść do ścieżki z pełną kontrolą (`pisma-procesowe-v3` typ albo skill RODO z pkt 5).
3. Ładowanie leniwe: SKILL.md tylko z katalogiem i odsyłaczem, schemat czytany dopiero po wyborze typu.
4. `lint_refs.py` pilnuje 21 odwołań z `shared`.

---

## 11. Benchmark: KPI, baseline i bramka w pipeline

**Stan.** `benchmark-lexmachina/` ma 14 kazusów korporacyjnych (arbitraż, upadłość, governance) z kluczem
autorskim i wynikami 7 przebiegów z września; `benchmark-matematic/` ma 3 umowy B2B z posianymi wadami. Oba są
poza profilem spraw właściciela. Wynik z 15.09: ChatGPT High bez skilli 9,16 i przewaga skilli 0,03 pkt, czyli
na tym korpusie plugin nie wykazywał wartości. Nic nie jest wpięte w CI.

**Projekt.**

*Korpus (zadania B1-B6), każde z kluczem i rubryką, budowane ze spraw zamkniętych lub z kazusów opartych na
nich (fakty zmienione tak, by klucz był jednoznaczny):*
- B1 analiza akt karnych/wykroczeniowych: sprzeczności protokołów Policji, kwalifikacja, braki postępowania;
- B2 zawiadomienie o przestępstwie z relacji pokrzywdzonego (kompletność epizodów, kwalifikacje, adresat);
- B3 pismo procesowe od zera: zażalenie na postanowienie prokuratora, apelacja, wniosek dowodowy, zarzuty do
  opinii biegłego (test H1, H2 z pkt 9);
- B4 ocena ryzyk i szans (pkt 1), B5 terminy: karta terminu i rejestr na fixture zarządzeń i doręczeń (pkt 2),
  B6 normalizacja MD akt (pkt 3, w pełni deterministyczny).

*Metryki (KPI):* zgodność z kluczem 0-10 według rubryki (metoda z `2026-09-08_METODOLOGIA.md`); zmyślenia
(przepis, sygnatura, cytat spoza akt) jako twarde zero; pokrycie przesłanek i faktów; poprawność terminów
(dokładna data, podstawa); koszt (tokeny, czas). Jakość pisma dodatkowo: ocena ślepa parami (A/B) przez sędziego
modelowego i próbka ręczna właściciela.

*Konfiguracje (baseline):* C0 model bez skilli i bez MCP; C1 bez skilli z MCP `lex`; C2 upstream LexMachina
niemodyfikowany + MCP; C3 upstream awesome-matematic niemodyfikowany + MCP; C4 C2+C3 razem; C5 plugin
`grounding-prawo` z bieżącego `main`; C6 plugin z gałęzi PR. Modele: Sonnet i Opus (ostatnie), 3 powtórzenia na
zadanie dla wariancji.

*Sędzia:* inny model niż wykonawca, z kluczem; odpowiedzi anonimizowane co do konfiguracji; zgodność sędziego
mierzona na 10% próbek ocenionych ręcznie.

*Pipeline:* `scripts/bench.py` (headless `claude -p` z `--plugin-dir` per konfiguracja, wyniki do `bench/wyniki/<data>/`),
w CI job uruchamiany na PR zmieniającym `own-skills/`, `selection/` lub `scripts/build.py`: szybki zestaw
(B5, B6 deterministyczne + 1 zadanie z każdej grupy), pełny zestaw tygodniowo i przed większym scaleniem. Bramka:
brak spadku średniej poniżej przedziału ufności C5 i zero zmyśleń; wynik w komentarzu PR.

*Pierwszy pomiar (przed jakąkolwiek przebudową z pkt 1-10):* C0, C2, C3, C5 na B1-B6. Jeśli C5 ≤ C0 lub C5 ≤ C2,
plugin w obecnym kształcie nie ma przewagi i przebudowa idzie od tego, co wnosi przewagę, a nie od listy skilli.

*Koszt:* pełny zestaw ok. 6 zadań × 7 konfiguracji × 2 modele × 3 powtórzenia = 252 przebiegi; szybki zestaw ok. 30.

---

## Korekta po recenzji (30.10.2026)

Recenzja niezależna (GPT) zweryfikowana w kodzie. Przyjęte poprawki zastępują odpowiednie fragmenty punktów 1-11.

**Potwierdzone w kodzie i dopisane do diagnozy:**
- CI publikuje bez kontroli jakości prawnej: job `upstream-bump` scala PR sam po buildzie, walidacji, lincie
  i 2 testach technicznych (`build-plugin.yml:149-188`), a bez uprawnienia do PR pushuje na `main`
  (`build-plugin.yml:97`, `:182`; dodane w PR #76). Job `build` też commituje wynik na `main` (`:68`).
- Build jest transformacją semantyczną, nie kopiowaniem: `fold()`, `merge()`, `scrub_file()` i
  `scripts/retire_layers.py` (604 linie podmian z asercjami). Raport rozmiarów nie dowodzi równoważności.
- `case-risk` odwołuje się do nieistniejących `civil_liability_and_litigation_risk_map.md`,
  `criminal_liability_medical_consent_map.md`, `court_administrative_supervision_map.md`,
  `mental_health_article_map.md` (`SKILL.md:149-152`) i do komendy `/tk-medical-consent-check`
  (`SKILL.md:75`, także w modułach `medical-consent` i `uoozp-compliance`); `lint_refs.py` tego nie łapie.
- Spadek jakości pism przez niewczytywanie modułów typów (H1) i omijanie soczewek (H2) to hipotezy:
  porównanie plików pokazuje tylko, że treść istnieje, nie że jest używana.

**Zmiany planu:**
1. **P0 bezpieczeństwo wydań** (nowy pierwszy krok): bez pushu na `main` z CI; podbicie upstreamu zawsze jako PR;
   auto-merge wyłącznie po przejściu testów A i B (niżej); job `build` zamiast commitu na `main` otwiera PR.
   Decyzja D0.
2. **P1 inwentaryzacja semantyczna**: `scripts/report.py` rozszerzony o bilans reguł per skill upstreamu:
   miejsce w pluginie, punkt wywołania (opis, router, odsyłacz), reguły bez zmian / zmienione / usunięte
   z powodem (z `scrub_file`, `retire_layers`, patchy), status testów. Osobny bilans IURA i soczewek MateMatic.
   Build odrzuca skill, który zniknął bez wpisu `drop`, i martwe odwołanie do pliku lub komendy.
3. **Ślad wykonania**: benchmark uruchamia `claude -p --output-format stream-json`, z którego wynika, które pliki
   skilli i modułów faktycznie przeczytano i które narzędzia MCP wywołano. Test routingu: „apelacja karna” →
   `prawny-router-v3` → `pisma-procesowe-v3` → odczyt `modules/typy/apelacja-karna.md` → pismo zgodne z checklistą
   modułu. Przeniesienie tabeli typów (pkt 9.2) to naprawa, ślad to dowód.
4. **pkt 1 `case-risk`**: rejestr bez iloczynu waga × prawdopodobieństwo jako miary szans. Pozycja: zagrożenie,
   skutek, ustalenia za i przeciw (z kotwicą w aktach), niepewność, działania, priorytet. Usunąć martwe odwołania.
5. **pkt 2**: osobny skill `stan-sprawy` (D2), kalkulator tylko liczy. Rejestr rozróżnia daty: sporządzenia,
   nadania, wpływu, doręczenia, zdarzenia wyzwalającego, końca terminu; każda zmiana statusu ma dokument lub
   potwierdzoną czynność. Przypomnienia poza sesją wymagają realnego harmonogramu (cron na NAS lub routine)
   i kanału powiadomień; przepis `wachta-terminow` w pluginie ich nie tworzy.
6. **pkt 3 kontrakt MD**: znacznik `==< <document_name> (Page x/y) >==` liczy strony dokumentu (wymóg właściciela).
   Gdy jeden PDF źródłowy zawiera kilka dokumentów, frontmatter dokumentu podaje `zrodlo_pdf` i
   `zrodlo_strony: [od, do]`, więc cytat da się odnieść do strony fizycznego pliku. Normalizator poprawia sam tylko
   zmiany bezpieczne mechanicznie (brak `---`, format znacznika przy jednoznacznej nazwie); konflikt nazw, zbiorcze
   `Page 1-4/4` i brak stron zgłasza do porównania z PDF. Wybór ekstraktora (`pdftotext -layout`, PyMuPDF,
   MarkItDown, OpenDataLoader) tylko po benchmarku ekstrakcji (tabele, dwie kolumny, pieczęcie, dopiski, strony
   mieszane), nie z góry.
7. **pkt 5 RODO**: skill rozróżnia reżimy: RODO; ustawa z 14.12.2018 o ochronie danych osobowych przetwarzanych
   w związku z zapobieganiem i zwalczaniem przestępczości (Policja, prokuratura); dostęp do akt z KPK/KPW;
   dokumentacja medyczna z ustawy o prawach pacjenta. Organ i sprawa wyznaczają reżim, nie odwrotnie.
8. **pkt 9.3 pierwsze wrażenie**: samodzielny skill-wrapper bez kopii treści (czyta moduł szturmu), kończy się
   raportem, bez pętli i bez poprawek; w szturmie usunąć sprzeczność między „każda soczewka obowiązkowa”
   a „pojedyncza soczewka na żądanie”.
9. **pkt 10 pisma proste**: router zawężony do profilu i leniwe ładowanie schematu po wyborze typu; usunięcie
   schematów spoza profilu dopiero po teście ablation, nie z góry. Skarga do UODO poza pismami prostymi.
10. **pkt 11 benchmark**, trzy warstwy:
    - A deterministyczne (pass/fail): MD, znaczniki stron, frontmatter, terminy, schematy BM, build, kompletność
      modułów, martwe odwołania;
    - B behawioralne (ze śladu wykonania): właściwy skill i moduł, kontrola cytatu wykonana, relacja zachowana,
      brak zbędnego pełnego szturmu;
    - C merytoryczne: rubryka, ocena parami A/B, sędzia kalibrowany na ocenach właściciela (zgodność mierzona).
    Korpus C: 24-36 odrębnych kazusów rozłożonych na typy spraw, każdy z materiałem, kluczem, twierdzeniami
    wymaganymi i niedopuszczalnymi oraz źródłami prawa na datę kazusu; poprawna alternatywna argumentacja nie traci
    punktów. Konfiguracje do oceny skilli mają ten sam dostęp do MCP (C1 vs C2-C6); C0 bez MCP mierzy tylko
    całe rozwiązanie. Ablation: `C5 minus <skill/moduł>` dla skilli, o których decydujemy. Błędy klasyfikowane
    wagą; krytyczne (zmyślony przepis, sygnatura lub cytat; błędny termin zawity) blokują wydanie, drobne obniżają
    wynik. Stare benchmarki LexMachina i MateMatic zostają jako osobny zestaw regresyjny. Wynik 9,16 / +0,03
    z 15.09 nie przesądza o wartości pluginu; pokazuje brak miary na właściwym korpusie.
11. **Pochodzenie ustaleń**: w ustaleniach wtórnych oddzielać bezpośrednie spostrzeżenia użytkownika, twierdzenia
    osób trzecich, treść dokumentów, wyniki weryfikacji i hipotezy; pełna treść relacji i dokumentów zostaje.
    Rejestr pochodzenia służy analizie sprzeczności, nie amerykańskim regułom dopuszczalności dowodu.

## Kolejność

1. **P0**: zabezpieczenie wydań (D0).
2. **P1**: inwentaryzacja semantyczna scaleń i build odrzucający martwe odwołania.
3. **P1**: testy A i B oraz mały korpus C; pomiar bazowy `main` z zamrożonymi wersjami modeli, promptów i MCP.
4. **P1**: routing typów pism (9.1, 9.2), `pierwsze-wrazenie-sedziego` (9.3), ślad wykonania jako test.
5. **P2**: kontrakt i normalizator MD (pkt 3), potem `stan-sprawy` z terminami i harmonogramem (pkt 2).
6. **P2**: RODO, rejestr ryzyk, przegląd tabelaryczny, teczka (pkt 5, 1, 4, 6), każdy osobnym PR z przypadkami
   regresyjnymi; `/transkrypcja` (pkt 8).
7. **P3**: pełny korpus, porównanie z upstreamami, ablation; usuwanie tylko elementów bez potwierdzonej wartości.
8. Pkt 7 po decyzji D7: narzędzia deweloperskie poza pluginem prawniczym, chyba że test wykaże korzyść.

Każdy krok: osobny PR, przebieg testów A i B (od P1 także szybki C), wynik w opisie PR.

## Decyzje właściciela

Przyjęte 30.10.2026 jako robocze (rekomendacja planu i recenzji zgodna): D2 osobny `stan-sprawy`; D4 przebudowa pod
akta; D5 nowy skill RODO po stronie podmiotu; D6 teczka jako widok z BM; D9 samodzielne `pierwsze-wrazenie-sedziego`;
D10 zawężony router i leniwe ładowanie. Otwarte:

- D0: wyłączyć push na `main` z CI i auto-merge upstreamu bez testów A i B (cofa PR #76).
- D7: gdzie są włączone `ralph-loop`, `implementation-planning`, `plan-review`, `karpathy-guidelines`, `hookify`.
- D11: budżet benchmarku (modele, powtórzenia) i czy sprawy zamknięte mogą być materiałem korpusu.
