---
name: subsumpcja-pl
description: 'Buduje jawny sylogizm prawniczy (subsumcję) dla zagadnienia - rozkłada rozumowanie na przesłankę większą (norma + wykładnia), przesłankę mniejszą (istotne fakty), podciągnięcie faktów pod normę i wniosek, a potem wskazuje słabe ogniwa: ukryte założenia, sporne fakty, wątpliwą wykładnię. Wymusza, by każdy krok był wypowiedziany i sprawdzalny, zamiast skoku od stanu faktycznego do tezy. Pairuje z adversarial-legal-review-pl (atak na sylogizm), citation-grounding-pl (weryfikacja powołanej normy) i struktura-wyroku-pl. Uzywaj gdy: "zbuduj subsumpcję", "sylogizm prawniczy", "podciągnij fakty pod normę", "rozpisz rozumowanie", "gdzie jest luka w argumentacji", "przesłanka większa i mniejsza", "uzasadnij krok po kroku", przy pisaniu opinii / uzasadnienia / pisma procesowego. Przy zawiadomieniu o przestępstwie szuka dodatkowych czynów, sprawców i naruszeń przez funkcjonariuszy; braki zamienia w pytania do pokrzywdzonego.'
license: Apache-2.0
allowed-tools:
- Read
metadata:
  author: Wiesław Mazur / MateMatic
  version: 1.0.0
  companion_skills: adversarial-legal-review-pl, citation-grounding-pl, struktura-wyroku-pl
  data-residency: local
  requires-human-approval: 'false'
  pii-egress: none
  attribution: '{"source": "Fuzi.Mingcha (irlab-sdu)", "license": "not-stated", "relationship": "pattern-only", "note": "Subsumcja (sylogizm prawniczy) to klasyczna metoda polskiej dogmatyki prawa. Pomysł jawnego scaffoldu sylogizmu dla AI zainspirowany m.in. projektem Fuzi.Mingcha (podejście major/minor/conclusion). Bez użycia jego kodu ani modeli; implementacja, reguły i kotwice PL napisane od zera.\n"}'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Na wejściu odczytaj adekwatny kontekst z projektu `model-memory` i sprawy z `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap w `model-memory` i sprawdź odczytem. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# Subsumpcja PL - jawny sylogizm prawniczy

## WYJĄTEK: ZAWIADOMIENIE — rola „kwalifikacje rozszerzające”

Przy recenzji zawiadomienia pokrzywdzonego lub jego uzupełnienia wykonaj
`shared/ZAWIADOMIENIE-RECENZJA-ROZSZERZAJACA.md` z HARDGATE-ZOP. Ten tryb zastępuje
poniższy zwykły workflow, kryteria i format wyniku; nie jest dodatkowym atakiem po nim.
Wyjdź od całej relacji, nie tylko od wybranego przepisu. Zbadaj sąsiednie czyny, innych sprawców, współdziałanie, następstwa i naruszenia przez funkcjonariuszy. Brakujące cechy zamień w otwarte pytania; po odpowiedziach sprawdź alternatywy/kumulację i inne reżimy odpowiedzialności. Nie dopisuj znamion ani przestępstwa z samego uchybienia proceduralnego.
Pracuj na relacji, odpowiedziach, mapie i drafcie. Zadaj krótką serię pytań, po odpowiedziach
rozbuduj opis i powtórz przegląd nowych gałęzi. Bez odpowiedzi nie wpisuj hipotezy jako faktu.
Brak dowodu ani różnica z protokołem nie osłabiają relacji i nie blokują pisma. Nie strofuj autora.
Dla innych pism stosuj zwykły tryb. Jeśli autor zlecił tylko samą recenzję, uszanuj ten zakres.

## Filozofia

**Błąd w opinii rzadko siedzi we wniosku - siedzi w przemilczanej przesłance.** Rozumowanie prawnicze
to sylogizm: norma (przesłanka większa), fakty (przesłanka mniejsza), podciągnięcie i wniosek. Gdy
któryś krok zostaje niewypowiedziany - „bo przecież oczywiste" - tam właśnie chowa się luka, którą
znajdzie druga strona albo sąd. Ten skill zmusza, by każdy krok wypowiedzieć i oznaczyć, co jest
pewne, a co sporne.

Skill **strukturyzuje** rozumowanie, nie rozstrzyga sprawy. Ocena i decyzja zostają prawnikowi.

## Workflow

1. **Przesłanka większa (norma + wykładnia)** - zidentyfikuj normę prawną (przepis), a potem jej
   wykładnię: jak rozumiane są przesłanki normy (językowo, systemowo, celowościowo). Powołaną normę
   przekaż do citation-grounding-pl do weryfikacji.
2. **Przesłanka mniejsza (fakty istotne)** - wypisz fakty, które mają znaczenie dla przesłanek normy.
   Oddziel fakty bezsporne od spornych i od ocen.
3. **Subsumcja (podciągnięcie)** - dla każdej przesłanki normy pokaż, który fakt ją spełnia (lub nie).
   To jest właściwa praca: dopasowanie faktu do znamienia normy.
4. **Wniosek** - skutek prawny wynikający z subsumcji.
5. **Test słabych ogniw** - oznacz: które przesłanki normy są sporne w wykładni, które fakty sporne
   dowodowo, jakie założenia przyjęto milcząco. To mapa dla adversarial-legal-review-pl.

## Format wyjścia

```
ZAGADNIENIE: <pytanie prawne>

PRZESŁANKA WIĘKSZA (norma): <przepis> - "<treść/znamiona>"
  Wykładnia: <jak rozumiane są znamiona; rozbieżności w doktrynie/orzecznictwie>

PRZESŁANKA MNIEJSZA (fakty istotne):
  - bezsporne: <...>
  - sporne (dowodowo): <...>

SUBSUMCJA (znamię -> fakt):
  - <znamię 1> : spełnione przez <fakt> | NIE spełnione | sporne
  - <znamię 2> : ...

WNIOSEK: <skutek prawny>

SŁABE OGNIWA (do adversarial-legal-review-pl):
  - wykładnia: <które znamię sporne i dlaczego>
  - fakty: <co wymaga dowodu>
  - założenia milczące: <...>
```

## Granice

- Sylogizm porządkuje rozumowanie - nie zastępuje wykładni ani ustaleń dowodowych. Trafność normy,
  wykładni i oceny faktów rozstrzyga prawnik.
- Skill nie waży argumentów za i przeciw (od tego jest adversarial-legal-review-pl) - układa je tak,
  by atak i weryfikacja miały na czym pracować.
- Subsumcja zakłada normę o znamionach. Dla klauzul generalnych i ważenia zasad sam sylogizm bywa
  niewystarczający - oznacz to jako rozumowanie ważące, nie subsumpcyjne.

## Atrybucja

Subsumcja (sylogizm prawniczy) to klasyczna metoda polskiej dogmatyki prawa. Pomysł jawnego
scaffoldu sylogizmu dla AI zainspirowany m.in. projektem **Fuzi.Mingcha** (irlab-sdu) - bez użycia
jego kodu ani modeli. Reguły, format i kotwice PL to oryginalne opracowanie MateMatic.
Interpretacja MateMatic, nie stanowisko NRA ani KRRP.

<!-- shared-rules:begin (wygenerowane z ../../SHARED-RULES.md przez scripts/shared-rules-sync.py - nie edytuj tutaj) -->
## Wspólne reguły wtyczki fundament-weryfikacyjny (Fundament weryfikacyjny)

Te reguły obowiązują w każdym skillu tej wtyczki, także gdy sam skill milczy. Są skopiowane do każdego skilla, więc działają zarówno po instalacji całej wtyczki, jak i pojedynczego skilla. Pełniejszy standard: https://github.com/matematicsolutions/awesome-matematic-skills-pl/tree/main/references

### Pięć warstw ochrony (przed każdym disclaimerem)

1. **Weryfikacja źródła** - przepisy i orzecznictwo z baz, nie z pamięci modelu.
2. **Klasa pewności** - każda teza prawna oznaczona: zweryfikowane / do sprawdzenia / nie używać.
3. **Kontrola przesłanek** - fakty od użytkownika sprawdza się przed analizą.
4. **Jawny zakres ujemny** - każdy skill mówi, czego NIE robi.
5. **Bramka człowieka** - uprawniona osoba sprawdza i zatwierdza wynik.

Jeśli błąd przeszedłby bez zatrzymania przez warstwy 1-5, wina jest w skillu. Naprawiamy narzędzie, nie dopisujemy noty. Nota "to nie porada prawna" nie zatrzymuje błędu i nie przenosi odpowiedzialności.

### Tagi pewności

- **Zweryfikowane** - źródło sprawdzone w sesji, z pełną sygnaturą: `(kodeks cywilny art. 415)`, `(wyrok SN II CSK NN/RR, SAOS)`.
- **Do sprawdzenia** - prawdopodobne, niezweryfikowane: `[sprawdź w SAOS]`.
- **Nie używać** - zmyślona sygnatura lub przepis. Pomiń, nigdy nie wymyślaj numeru.

Tag stoi przy linii, której dotyczy. Samo istnienie sygnatury nie wystarcza - treść trzeba sprawdzić.

### Bramka człowieka

Nic nie zostaje wysłane, złożone, podpisane ani opublikowane, zanim sprawdzi i zatwierdzi to uprawniony człowiek. Wynik skilla to projekt, nie gotowy dokument.

### Zakres pluginu

Fundament weryfikacyjny jest neutralny jurysdykcyjnie - to rdzeń metody, nie substancja prawa. Nie łączy się z żadnym źródłem zewnętrznym (brak konektorów MCP) i nie wysyła danych na zewnątrz. Substancję dostarczają osobne pluginy (orzecznictwo, dokumenty).
<!-- shared-rules:end -->

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** draft i zweryfikowane przepisy (`analizator-przepisow-v2`)
- **Wynik zapisz w:** `drafty/<pismo>/_SUBSUMPCJA.md` (rejestr stały; dopisek przebiegu) (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pierwsze-wrazenie-sedziego-pl`, `atak-przeciwnika-pl`
- **Basic Memory (`legal`):** czytaj lekcje teczki i notatkę pisma (stan pętli); po każdej rundzie zapisz w notatce pisma wersję, otwarte uwagi i pytania, lekcje w `## Lekcje` (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
