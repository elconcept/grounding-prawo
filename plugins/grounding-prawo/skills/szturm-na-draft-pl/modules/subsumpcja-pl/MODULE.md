# Moduł `subsumpcja-pl` skilla `szturm-na-draft-pl`

> Dawniej osobny skill; scalony, żeby ta sama funkcja nie była powielana. Ścieżki `scripts/`, `references/` itd. są względne wobec tego katalogu.
>
> Zastosowanie: soczewka: pokrycie przesłanek faktami, słabe ogniwa sylogizmu; przy zawiadomieniu dodatkowe czyny i sprawcy

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

