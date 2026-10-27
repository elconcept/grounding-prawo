"""Usuwa warstwę kancelaryjną, raportową, audytową (AI Act) i „local-first".

Uruchamiane po `scrub`, `tag_out_of_plugin` i `qualify_paths`, czyli na tekście,
który faktycznie trafia do klienta. Każda podmiana ma asercję: zmiana upstreamu,
która psuje kontekst, zatrzymuje build zamiast zostawiać szczątki.

Decyzje właściciela (22.10.2026): profil spraw własnych, bez raportów dla klienta,
bez bramek kosztu, bez pakietu audytowego AI Act i bez polityki „tylko lokalnie".
"""

import os
import sys


def _repl(base, path, old, new, count=1):
    full = os.path.join(base, path)
    text = open(full, encoding="utf-8").read()
    found = text.count(old)
    if found != count:
        sys.exit(f"retire_layers: {path}: oczekiwano {count}, znaleziono {found}: {old[:120]!r}")
    open(full, "w", encoding="utf-8").write(text.replace(old, new, count))


def _drop_line(base, path, needle, count=1):
    full = os.path.join(base, path)
    lines = open(full, encoding="utf-8").readlines()
    kept = [line for line in lines if needle not in line]
    removed = len(lines) - len(kept)
    if removed != count:
        sys.exit(f"retire_layers: {path}: usunięto {removed} linii dla {needle!r}, oczekiwano {count}")
    open(full, "w", encoding="utf-8").writelines(kept)


def _remove(base, path):
    full = os.path.join(base, path)
    if os.path.exists(full):
        os.remove(full)


def _drop_meta(base, path, key):
    import re
    full = os.path.join(base, path)
    lines = open(full, encoding="utf-8").readlines()
    kept = [line for line in lines if not re.match(rf"^\s*{re.escape(key)}:", line)]
    if len(lines) - len(kept) != 1:
        sys.exit(f"retire_layers: {path}: nie usunięto metadanej {key}")
    open(full, "w", encoding="utf-8").writelines(kept)


def apply(base):
    # --- router: koniec z workflow kancelaryjnym ---
    _repl(base, "prawny-router-v3/references/KROK1-detekcja.md",
"""## KROK 1C — CENTRALNE JĄDRO KANCELARYJNE

Po detekcji trybu i przed przekazaniem sprawy do skilla dziedzinowego — wczytaj zależnie od potrzeby:

```text
Zawsze dla pism / strategii / akt / terminów / ryzyka / dowodów:
  view prawny-router-v3/references/KANCELARIA-WORKFLOW.md
  view shared/TRYBY-PROCESOWE.md
""",
"""## KROK 1C — CENTRALNE JĄDRO PROCESOWE

Po detekcji trybu i przed przekazaniem sprawy do skilla dziedzinowego — wczytaj zależnie od potrzeby:

```text
Zawsze dla pism / strategii / akt / terminów / ryzyka / dowodów:
  view shared/SCIEZKI-PRACY.md
  view shared/TRYBY-PROCESOWE.md
""")

    # --- pisma-procesowe-v3: bramka informacyjna bez blokowania pracy ---
    _repl(base, "pisma-procesowe-v3/SKILL.md",
"""  │ Czy akceptujesz powyższe warunki i chcesz kontynuować?                 │
  │  a) Tak, akceptuję — wczytaj checklistę i rozpocznij                   │
  │  b) Nie — zakończ lub wyjaśnij wątpliwości                             │
  └─────────────────────────────────────────────────────────────────────────┘

  ⛔ ZAKOŃCZ ODPOWIEDŹ PO WYŚWIETLENIU CG-1. Czekaj na decyzję a/b.
  ⛔ NIE wykonuj żadnego kroku merytorycznego przed akceptacją.

KROK CG-2 — PO OTRZYMANIU AKCEPTACJI „a" (WCZYTANIE CHECKLISTY):""",
"""  │ Po tym komunikacie wczytuję checklistę i przechodzę do KROKU 0.         │
  └─────────────────────────────────────────────────────────────────────────┘

  CG-GATE jest informacyjny. Po wyświetleniu od razu przechodzisz do CG-2:
  autor prowadzi własne sprawy i zna pipeline, więc bramka nie zatrzymuje pracy.

KROK CG-2 — WCZYTANIE CHECKLISTY (natychmiast po CG-1):""")
    _repl(base, "pisma-procesowe-v3/SKILL.md",
"""  │ Po Twojej akceptacji wczytam pełną listę kroków i checklistę,          │
  │ a następnie przystąpię do pracy.                                        │
  │                                                                         │
  │ Po tym komunikacie wczytuję checklistę i przechodzę do KROKU 0.         │""",
"""  │ Po tym komunikacie wczytuję checklistę i przechodzę do KROKU 0.         │""")
    _repl(base, "pisma-procesowe-v3/SKILL.md",
"""⛔ ZAKAZ-15 (bezwzględny — nowy):
  • ZAKAZ pominięcia CG-GATE na starcie sesji.
  • ZAKAZ rozpoczęcia jakiegokolwiek kroku merytorycznego bez akceptacji „a".
  • ZAKAZ wczytania checklisty bez wyświetlenia najpierw bloku INFORMACJA WSTĘPNA.
  • Polecenie „zacznij pismo" / „pisz" / „generuj od razu" NIE zwalnia z CG-GATE.""",
"""⛔ ZAKAZ-15 (bezwzględny):
  • ZAKAZ pominięcia CG-GATE na starcie sesji.
  • ZAKAZ wczytania checklisty bez wyświetlenia najpierw bloku INFORMACJA WSTĘPNA.
  • CG-GATE jest informacyjny: po jego wyświetleniu przechodzisz do CG-2 bez pytania o zgodę.""")
    _repl(base, "pisma-procesowe-v3/SKILL.md",
"""> Wyjątek od CG-GATE: gdy użytkownik w tej samej wiadomości co trigger pisma
> explicite napisał „pomijam informację wstępną, znam pipeline" lub podobny
> jednoznaczny sygnał świadomości — CG-1 można zastąpić jednolinijkowym
> potwierdzeniem wczytania checklisty i natychmiast wykonać CG-2.
> Bez takiego sygnału: zawsze pełny CG-1 + czekanie na odpowiedź.""",
"""> CG-GATE jest jawnym komunikatem, nie pytaniem o zgodę. Wyświetl CG-1
> i natychmiast wykonaj CG-2.""")

    # --- citation-grounding-pl: bez RODO/AI Act i bez „zero-cloud" ---
    _drop_meta(base, "citation-grounding-pl/SKILL.md", "data-residency")
    _drop_meta(base, "citation-grounding-pl/SKILL.md", "pii-egress")
    _repl(base, "citation-grounding-pl/SKILL.md",
"""## Ochrona danych (RODO)

- Skill działa **w całości lokalnie** - normalizacja i string-match w Node, bez wywołań sieciowych.
  (Rozwiązywanie kotwic przez SAOS/EUR-Lex robi agent osobnym krokiem - skrypt dostaje gotowy `anchor_resolved`.)
- Skrypt nie zapisuje logów poza katalogiem zadania.

## Integracja z AI Act

Mechaniczny grounding to dowód należytej staranności i element dokumentacji z art. 12 (rejestrowanie
zdarzeń) oraz nadzoru człowieka z art. 14. Gradient dodaje wymiar **kalibracji ryzyka**: poziom
weryfikacji per twierdzenie to ślad, jak mocno każda teza jest osadzona. Raport grounding wkładaj
do `legal-ai-audit-bundle (poza pluginem)` obok deliverable.

""", "")
    _repl(base, "citation-grounding-pl/SKILL.md",
          "oba przed wysłaniem high-stakes.", "oba przed wysłaniem pisma.")
    _repl(base, "citation-grounding-pl/SKILL.md",
"""co łamie kontrakt
  zero-cloud; z repo bierzemy tylko lokalną, jurysdykcyjnie-neutralną heurystykę nazw stron.""",
"""co wymaga wywołania sieciowego i tokenu; z repo bierzemy tylko
  jurysdykcyjnie-neutralną heurystykę nazw stron.""")
    _repl(base, "citation-grounding-pl/SKILL.md",
          "silnik string-match pod lokalne źródła PL (RODO, zero-egress).",
          "silnik string-match pod polskie źródła.")
    _repl(base, "citation-grounding-pl/references/szkielet-weryfikatora-domenowego/SKILL.template.md",
          "  i czy oddaje stanowisko organu. Przeciwdziała halucynacjom, RODO-safe (lokalnie).",
          "  i czy oddaje stanowisko organu. Przeciwdziała halucynacjom.")
    _drop_line(base, "citation-grounding-pl/references/szkielet-weryfikatora-domenowego/README.md",
               "Reguła RODO", 1)
    _repl(base, "citation-grounding-pl/modules/ekstraktor-cytatow-pl/MODULE.md",
          "cytatów mógłby jeden przeoczyć albo dopowiedzieć. Lokalnie, RODO-safe.",
          "cytatów mógłby jeden przeoczyć albo dopowiedzieć. Działa na plikach w katalogu sprawy.")

    # --- redline / kalkulatory / rodo-dsar: bez metadanych lokalności ---
    for name in ("redline-docx-pl", "kalkulatory-procesowe-pl", "rodo-dsar-pl"):
        _drop_meta(base, f"{name}/SKILL.md", "data-residency")
        _drop_meta(base, f"{name}/SKILL.md", "pii-egress")
    _repl(base, "redline-docx-pl/SKILL.md",
          "Cala praca lokalnie (uvx, brak chmury). Silnik testowany",
          "Konwersja przez `uvx`. Silnik testowany")
    _repl(base, "kalkulatory-procesowe-pl/SKILL.md",
          "- Skill działa lokalnie na danych sprawy (RODO-safe); jedyny ruch na",
          "- Dane sprawy zostają w katalogu sprawy; jedyny ruch na")
    _repl(base, "kalkulatory-procesowe-pl/modules/terminy-procesowe-pl/MODULE.md",
          "- Skill działa lokalnie na danych sprawy (RODO-safe); jedyny ruch na zewnątrz to",
          "- Dane sprawy zostają w katalogu sprawy; jedyny ruch na zewnątrz to")

    # --- deliverable-fidelity: bez AI Act ---
    fidelity = "szturm-na-draft-pl/modules/deliverable-fidelity-pl/MODULE.md"
    _repl(base, fidelity,
"""To wymog rejestrowania zdarzen
z art. 12 AI Act sprowadzony do arytmetyki - argument wprost pod PATRONa.""",
"""To wymog przejrzystosci werdyktu:
kazdy odtworzy wynik z liczb, bez pytania modelu o uzasadnienie.""")
    _repl(base, fidelity,
"""## Ochrona danych (RODO)


## Integracja z AI Act

Weryfikacja wiernosci to dowod, ze nadzor czlowieka (art. 14) dostaje pelen obraz - deliverable nie ukrywa
przed decydentem ustalen, ktore analiza wykryla. Raport wiernosci wkladaj do `legal-ai-audit-bundle (poza pluginem)`.

""", "")

    # --- adversarial: bez bramki kosztu, limitu rund i pakietu audytowego ---
    adv = "szturm-na-draft-pl/modules/adversarial-legal-review-pl/MODULE.md"
    _repl(base, adv, "## Profil właściciela: bez bramki kosztu", "## Tryb pracy: zawsze pełny cykl")
    _repl(base, adv,
"""### 0. Bramka high-stakes
Oceń, czy sprawa kwalifikuje (tabela wyżej). Jeśli nie - stop, zaproponuj zwykły review.

""", "")
    _repl(base, adv,
          "- **Limit rund per stawka:** wysoka = maks. 3 rundy; tryb szybki = maks. 1.",
          "- **Limit rund:** brak limitu narzuconego przez koszt. Pętla kończy się na `GOTOWE` albo decyzją autora.")
    _repl(base, adv,
"""1. **Czysta akceptacja** - wszyscy recenzenci zaakceptowali, 0 blokerów →
   `zaakceptowano_na_vN`.
2. **COFNIĘCIE PO REGRESJI (N≥2)** - `wynik_zbiorczy(vN) < wynik_zbiorczy(v_najlepsza)` →
   odrzuć vN, przywróć `v_najlepsza`, wyjdź jako `wymuszone_wyjscie_na_v<najlepsza>_z_otwartymi`
   z banerem „runda N pogorszyła deliverable - przywrócono najlepszą wersję".
3. **Wczesne wyjście na plateau (N≥2)** - wynik ≥ próg (domyślnie 85), ale poprawa < 1,0
   pkt względem poprzedniej → `zaakceptowano_wczesnie_na_vN` (nie palić tokenów na
   marginalny zysk).
4. **Kontynuuj** - są blokery, limit nieosiągnięty, brak regresji i plateau → kolejna runda
   celowanych poprawek.
5. **Wymuszone wyjście na limicie** - limit osiągnięty, blokery zostały →
   `wymuszone_wyjscie_na_limicie` + baner z listą nierozstrzygniętych zarzutów.

Powód limitu: nieskończone polerowanie maskuje problem zamiast go rozstrzygać. Jeśli
trzy rundy nie domknęły zarzutu, redakcja go nie domknie - spór jest merytoryczny albo
brakuje dowodu, a to rozstrzyga prawnik, nie kolejny przebieg modelu. Licznik rund
i stan końcowy zapisuj w raporcie (patrz Output).""",
"""1. **Czysta akceptacja** - wszyscy recenzenci zaakceptowali, 0 blokerów →
   `GOTOWE` (na vN).
2. **COFNIĘCIE PO REGRESJI (N≥2)** - `wynik_zbiorczy(vN) < wynik_zbiorczy(v_najlepsza)` →
   odrzuć vN, przywróć `v_najlepsza` i próbuj innej poprawki; nie zamykaj pętli.
3. **Stagnacja** - ta sama uwaga wraca drugą rundę z rzędu albo poprawki oscylują →
   pokaż autorowi konflikt i poproś o rozstrzygnięcie; nie maskuj go kolejną redakcją.
4. **Kontynuuj** - są blokery → kolejna runda celowanych poprawek na nowej wersji.
5. **Przerwanie przez autora** - stan `NIEGOTOWE` z listą otwartych uwag i pytań;
   nigdy „gotowe z zastrzeżeniami".

Blokery rozwiązuje się merytorycznie: brak dowodu, sporną wykładnię albo decyzję
strategiczną rozstrzyga autor, nie kolejny przebieg modelu. Licznik rund i stan
końcowy zapisuj w raporcie (patrz Output).""")
    _repl(base, adv,
"""`zaakceptowano_na_vN` | `zaakceptowano_wczesnie_na_vN` | `wymuszone_wyjscie_na_v<najlepsza>`
(regresja) | `wymuszone_wyjscie_na_limicie` | `porazka_z_fallbackiem` (np. brak danych
źródłowych - dostarcz, co masz, plus powód).""",
"""`GOTOWE` (na vN) | `NIEGOTOWE` (przerwane przez autora albo stagnacja) |
`porazka_z_fallbackiem` (np. brak danych źródłowych - dostarcz, co masz, plus powód).""")
    _repl(base, adv,
"""Baner zawsze pokazuje: stan końcowy, którą wersję draftu dostarczono, jakie blokery
zostały. **Governance:** skill produkuje rekomendację i wersje draftu; NIE wysyła
dokumentu. Decyzja „wysłać mimo `wymuszone_wyjscie_na_limicie` z blokerami" zostaje przy
człowieku. Transkrypt wszystkich wersji v1..vN idzie jako załącznik do paczki audytowej -
dowód ograniczonej rewizji i ewentualnego cofnięcia (AI Act art. 12/14).""",
"""Baner zawsze pokazuje: stan końcowy, którą wersję draftu dostarczono, jakie blokery
zostały. Skill produkuje rekomendację i wersje draftu; NIE wysyła dokumentu. Decyzję
o wysłaniu podejmuje autor.""")
    _repl(base, adv,
"""Wagi i progi są wypisane w skillu celowo: audytor ma odtworzyć werdykt z samych liczb,
bez pytania modelu "dlaczego". To wymóg rejestrowania zdarzeń z art. 12 AI Act
zamieniony na arytmetykę - argument wprost pod PATRONa.""",
"""Wagi i progi są wypisane w skillu celowo: czytelnik ma odtworzyć werdykt z samych liczb,
bez pytania modelu "dlaczego".""")
    _repl(base, adv,
"""rewizji z sekcji 4a - limit rund per stawka dotyczy poprawek deliverable po
verifierze, a panel ma własny, jeszcze twardszy limit: jedno głosowanie + jedno
powtórzenie z dowodem. Eskalacja do człowieka to ten sam mechanizm, co
`wymuszone_wyjscie_na_limicie` w drzewie wyjścia.""",
"""rewizji z sekcji 4a - panel ma własny limit: jedno głosowanie + jedno powtórzenie
z dowodem, niezależnie od liczby rund poprawek deliverable. Eskalacja do człowieka
jest częścią pętli: autor rozstrzyga spór merytoryczny.""")
    _repl(base, adv, "Stawka: WYSOKA (kwalifikuje)\nFilary tezy:", "Filary tezy:")
    _repl(base, adv,
"""Pełny zapis debaty (transcript builder/attacker/synthesizer, wszystkie wersje v1..vN)
zwróć jako załącznik do `legal-ai-audit-bundle (poza pluginem)` - to dowód kontradyktoryjnej weryfikacji
i ograniczonej rewizji.

## Ochrona danych (RODO)

- Pobieranie kontr-orzecznictwa przez companion-skille (saos / eu-sparql) - publiczne źródła.
- Skill nie zapisuje deliverable poza katalogiem sprawy.

## Integracja z AI Act

Kontradyktoryjna weryfikacja + jawny poziom pewności + transcript = operacjonalizacja nadzoru
człowieka (art. 14) i dokumentacji (art. 12). Człowiek dostaje nie "gotową odpowiedź", lecz
mapę tego, co przetrwało atak i z jaką pewnością - i na tej podstawie decyduje.

""",
"""Pełny zapis debaty (transcript builder/attacker/synthesizer, wszystkie wersje v1..vN)
zostaw w katalogu sprawy jako ślad kontradyktoryjnej weryfikacji.

""")
    _repl(base, adv,
"""Limit 2 rund
z v1.1.0 zastąpiony: gwarancja „nigdy gorsza wersja" pokrywa też tamten przypadek, a limit
rund jest teraz jawnym parametrem per stawka.""",
"""Limit 2 rund
z v1.1.0 zastąpiony: gwarancja „nigdy gorsza wersja" pokrywa też tamten przypadek, a liczba
rund nie jest ograniczona kosztem.""")

    # --- atak-przeciwnika: bez gradientu kosztu ---
    _repl(base, "szturm-na-draft-pl/modules/atak-przeciwnika-pl/MODULE.md",
"""To jest JEDNOPRZEBIEGOWY, tani atak - niższy szczebel gradientu kosztu.

| Szczebel | Narzędzie | Koszt | Kiedy |
|---|---|---|---|
| 1 | zwykła odpowiedź | minimalny | pytanie rutynowe, notatka robocza |
| 2 | **atak-przeciwnika-pl (ten skill)** | niski, jeden przebieg | sparing pisma, przygotowanie do rozprawy, wstępny filtr |
| 3 | adversarial-legal-review-pl | wysoki, cztery role | deliverable wysokiej stawki przed wysłaniem do klienta lub sądu |

O wyborze szczebla decyduje `legal-request-router-pl (poza pluginem)`. Praktyczna reguła: jeśli po ataku
jednoprzebiegowym padły dwa lub więcej filarów tezy, a stawka jest wysoka - eskaluj do
pełnej debaty. Jeden przebieg nie zastąpi syntezy i kontroli końcowej verifiera.""",
"""To jest JEDNOPRZEBIEGOWY atak, ale nie tańsza alternatywa dla pełnej debaty. W `szturm-na-draft-pl`
uruchamiasz go zawsze razem z `adversarial-legal-review-pl`: ten lens daje szybki, surowy atak,
a debata dokłada syntezę i kontrolę końcową verifiera. Jeden przebieg nie zastępuje drugiej soczewki.""")

    # --- webwright: bez pakietu audytowego ---
    _repl(base, "patron-prawo-pl-zrodla/modules/webwright-legal-pl/MODULE.md",
"""`meta.json` jest zgodny ze schematem oczekiwanym przez `citation-grounding-pl`
oraz `legal-ai-audit-bundle (poza pluginem)`: pola `url` i `pobrano_at` umożliwiają późniejszy
audit trail.""",
"""`meta.json` jest zgodny ze schematem oczekiwanym przez `citation-grounding-pl`:
pola `url` i `pobrano_at` umożliwiają późniejszą weryfikację źródła.""")
    _repl(base, "patron-prawo-pl-zrodla/modules/webwright-legal-pl/scripts/fetch_eurlex.py",
          "Kontrakt meta.json (zgodny z citation-grounding-pl + legal-ai-audit-bundle):",
          "Kontrakt meta.json (zgodny z citation-grounding-pl):")
    _repl(base, "patron-prawo-pl-zrodla/modules/webwright-legal-pl/scripts/fetch_orzeczenie.py",
          "Kontrakt meta.json (zgodny z PATRON / citation-grounding-pl / legal-ai-audit-bundle):",
          "Kontrakt meta.json (zgodny z PATRON / citation-grounding-pl):")

    # --- redline: koniec z odniesieniem do anonimizacji ---
    _repl(base, "redline-docx-pl/THIRD_PARTY_INSPIRATIONS.md",
"""
## Powiazania

- `let-it-be` - anonimizacja TRESCI (PII PL); adeu sanitize czysci METADANE pliku.
  Dwie rozne warstwy, lancuch: let-it-be tresc -> redline -> adeu sanitize metadane.
""", "")

    # --- ostatnie ślady warstwy anonimizacji i pakietu audytowego ---
    _drop_line(base, "dr-11-cyfrowe-cyber-ai-dane-ip/modules/mod-RODO-DSAR-zadania-osob.md",
               "| Anonimizacja kopii dokumentów | KROK 0A routera (anonimizer) |", 1)
    _repl(base, "patron-prawo-pl-zrodla/modules/webwright-legal-pl/MODULE.md",
          "pobiera pełną treść konkretnego CELEX (do citation grounding i audit bundle).",
          "pobiera pełną treść konkretnego CELEX (do citation grounding).")
    _repl(base, "citation-grounding-pl/modules/ekstraktor-cytatow-pl/MODULE.md",
          """- Wzorce pokrywają najczęstsze formaty; nietypowy zapis sygnatury może umknąć - przy audycie
  wysokiej stawki przejrzyj też ręcznie.""",
          """- Wzorce pokrywają najczęstsze formaty; nietypowy zapis sygnatury może umknąć - przy kontroli
  pisma przejrzyj też ręcznie.""")

    _repl(base, "szturm-na-draft-pl/modules/atak-przeciwnika-pl/MODULE.md",
          """- `adversarial-legal-review-pl` - wyższy szczebel: pełna debata builder/attacker/
  synthesizer/verifier dla spraw wysokiej stawki""",
          """- `adversarial-legal-review-pl` - pełny cykl: debata builder/attacker/synthesizer/
  verifier z syntezą i kontrolą końcową""")
    _repl(base, "szturm-na-draft-pl/modules/atak-przeciwnika-pl/MODULE.md",
          "wymogi apelacji), pozycjonowanie na gradiencie kosztu względem adversarial-legal-review-pl,",
          "wymogi apelacji), rola uzupełniająca wobec adversarial-legal-review-pl,")

    # --- raporty klienta/sytuacyjne: usuń z aktywnych skilli ---
    _repl(base, "analizator-dowodow-v3/SKILL.md",
          ', "przesluchanie-swiadkow", "raport-sytuacyjny", "raport-klienta"]}\'',
          ', "przesluchanie-swiadkow"]}\'')
    _drop_line(base, "analizator-dowodow-v3/SKILL.md", "| Raport stanu sprawy (widget interaktywny)", 1)
    _drop_line(base, "analizator-dowodow-v3/SKILL.md", "| Raport dla klienta (zewnętrzny", 1)
    _repl(base, "analizator-dowodow-v3/modules/MD-NARR-raport-narracyjny.md",
"""  - chce przekazać analizę osobie trzeciej (np. innemu prawnikowi, klientowi
    w wersji PRAWNIK — nie mylić z raport-klienta-v1 (poza pluginem), który jest uproszczony
    dla LAIK)""",
"""  - chce przekazać analizę osobie trzeciej (np. innemu prawnikowi lub klientowi
    w wersji PRAWNIK)""")

    _repl(base, "przewodnik-prawny-v2/SKILL.md",
"""3. Zaproponuj Raport Sytuacyjny jeśli sprawa złożona:
   view shared/raport-sytuacyjny-integracja.md
4. PRAWNIK — zaproponuj raport dla klienta:
   "Czy wygenerować raport statusu sprawy dla klienta?
   → Powiedz 'raport dla klienta' żebym przygotował dokument zewnętrzny."
   (wywołuje raport-klienta-v1 (poza pluginem) po potwierdzeniu)
5. → KROK I (co dalej?)""",
"""3. → KROK I (co dalej?)""")
    _repl(base, "przewodnik-prawny-v2/SKILL.md",
"""Raport sytuacyjny sprawy
  → "Tworzę przegląd całej sprawy — co wiadomo, co brakuje,
     co pilne."
  → view raport-sytuacyjny-v2/SKILL.md (poza pluginem) → widget → KROK I

""", "")
    _drop_line(base, "przewodnik-prawny-v2/SKILL.md",
               "Raport sytuacyjny             → raport-sytuacyjny-integracja.md", 1)

    for path in ("pisma-procesowe-v3/references/W3-WERYFIKACJA.md",
                 "pisma-procesowe-v3/references/MODULY-MAPA.md",
                 "shared/DISCLAIMER.md"):
        _drop_line(base, path, "view shared/raport-sytuacyjny-integracja.md", 1)

    _repl(base, "shared/MOD-HISTORIA-STRATEGII.md",
"""> Status: shared canonical. Konsumowany przez `MOD-WARIANTY-POZWU.md`,
> `MOD-PRIORYTETY-ASPEKTOW.md`, oraz zakładkę "Historia strategii" w
> `raport-sytuacyjny-v2`.""",
"""> Status: shared canonical. Konsumowany przez `MOD-WARIANTY-POZWU.md`
> i `MOD-PRIORYTETY-ASPEKTOW.md`.""")

    _repl(base, "analiza-sadowa-v6/SKILL.md",
"""WIADOMOŚĆ 6 — WIDGET RAPORTU SYTUACYJNEGO [OBOWIĄZKOWY]

Wykonaj natychmiast po §11 raportu końcowego, bez pytania o zgodę.

SEKWENCJA:
  1. view shared/raport-sytuacyjny-integracja.md
     (tylko jeśli nie wczytano w tej sesji)

  2. Zbuduj blueprint JSON ze schematu w raport-sytuacyjny-v2/SKILL.md (poza pluginem)
     → dane wyłącznie z rozmowy / dokumentów; pola nieznane → null
     → tryb: "A" (po pełnej analizie)

  3. show_widget(path="raport-sytuacyjny-v2/assets/widget-raport-sytuacyjny.html (poza pluginem)",
                 data=BLUEPRINT) — bez kodu; host wstawia dane i pasek IO.
     Host bez pola `data`: raport-sytuacyjny-v2/SKILL.md (poza pluginem) § WIDGET — WYKONANIE BEZ POLA `data`.

  Poprzedź widgetem komunikat:
  "Poniżej aktualny raport sytuacyjny sprawy —
   możesz uzupełnić brakujące dane lub skorygować automatycznie rozpoznane informacje."

WYJĄTEK: pomiń wiadomość 6 tylko gdy użytkownik zadał jedno pytanie
         bez dokumentów i bez stanu faktycznego sprawy.

---

WIADOMOŚĆ 7 — OFERTA PISMA PROCESOWEGO

Po widgecie (lub gdy wyjątek powyżej — bezpośrednio po raporcie):""",
"""WIADOMOŚĆ 6 — OFERTA PISMA PROCESOWEGO

Po raporcie końcowym:""")

    _repl(base, "chronologia-sprawy-v1/SKILL.md",
"""→ raport-sytuacyjny-v2 (poza pluginem) [NOWE — v1.1]:
   Po zakończeniu ekstrakcji TRYB A lub TRYB B:
   Przekaż dane chronologii jako tablicę JSON do blueprintu raportu sytuacyjnego.
   Format zgodny ze schematem raport-sytuacyjny-v2 (poza pluginem):
     chronologia: [
       { data, zdarzenie, zrodlo, status_zrodla, znaczenie_procesowe, ryzyko }
     ]
   Wywołanie: raport-sytuacyjny-v2 (poza pluginem) TRYB [A] odbiera tablicę automatycznie
   z historii rozmowy. Żeby zasilić go danymi z chronologii:
   Po KROK A4 lub B3 — dodaj do odpowiedzi gotową strukturę JSON z zakodowanymi
   zdarzeniami, opatrzoną nagłówkiem:
   ## DANE CHRONOLOGICZNE DLA RAPORTU SYTUACYJNEGO
   [tablica JSON]
   Raport sytuacyjny wyciągnie ją automatycznie przy budowie blueprintu.

""", "")

    _drop_line(base, "analizator-umow-v1/SKILL.md",
               "| Po Raporcie F — widget statusu sprawy |", 1)
    _repl(base, "analizator-umow-v1/SKILL.md",
          "*             MOD-WALIDACJA_v2 · FAKTY_v2 · terminy · raport-sytuacyjny-integracja*",
          "*             MOD-WALIDACJA_v2 · FAKTY_v2 · terminy*")
    _repl(base, "analizator-umow-v1/references/mod-core-checklist.md",
"""### F.3 Widget statusu sprawy (po raporcie)

Po zakończeniu analizy (Raport F.1 / F.1-LITE / F.2) → wczytaj i zastosuj sekwencję:
```
view shared/raport-sytuacyjny-integracja.md
```
Widget renderowany inline jako show_widget HTML — nie jako present_files.
Dane wbudowane bezpośrednio w HTML jako literały JS.

---

""", "")
    _repl(base, "analizator-umow-v1/references/mod-core-checklist.md",
"""Po zakończeniu raportu F.1 / F.1-LITE / F.2 — widget statusu sprawy:
  → view shared/raport-sytuacyjny-integracja.md

""", "")
    _drop_line(base, "analizator-umow-v1/references/mod-shared-economic.md",
               "raport-klienta-v1 (poza pluginem): eksport danych do raportu biznesowego", 1)

    # --- shared: ślady raportu i kancelarii ---
    _drop_line(base, "shared/SKILL.md", "`raport-sytuacyjny-integracja.md` | Sekwencja wywołania", 1)
    _drop_line(base, "shared/SKILL.md", "view shared/raport-sytuacyjny-integracja.md", 1)
    _drop_line(base, "shared/SKILL.md", "tools/append_event.py` + `tools/hash_chain_verify.py`", 1)
    _repl(base, "shared/SKILL.md",
"""> **Uwaga:** `raport-sytuacyjny-integracja.md` jest wywoływany przez `prawny-router-v3`
> opisowo (punkty self-check [A]/[B]/[C]). Skille dziedzinowe nie wywołują go przez `view` —
> logika wyzwalania jest w routerze. `FAKTY_v2.md` jest wbudowany bezpośrednio w `pisma-procesowe-v3`
> i `pisma-proste-v2` (sekcje MOD-FAKTY / M-FAKTY) — wywołanie przez `view` możliwe gdy potrzebna
> jest pełna wersja modułu.""",
"""> **Uwaga:** `FAKTY_v2.md` jest wbudowany bezpośrednio w `pisma-procesowe-v3`
> i `pisma-proste-v2` (sekcje MOD-FAKTY / M-FAKTY) — wywołanie przez `view` możliwe gdy potrzebna
> jest pełna wersja modułu.""")
    _repl(base, "shared/SKILL.md",
          " MOD-MAPA-PRZEPISOW.md → analizator-przepisow-v2/SKILL.md; raport-sytuacyjny-integracja.md → raport-sytuacyjny-v2/SKILL.md. (poza pluginem)",
          " MOD-MAPA-PRZEPISOW.md → analizator-przepisow-v2/SKILL.md.")
    _repl(base, "shared/SKILL.md",
          "`prawny-router-v3/references/`: KANCELARIA-WORKFLOW, SOCIAL-SECURITY-LAW-STANDARD",
          "`prawny-router-v3/references/`: SOCIAL-SECURITY-LAW-STANDARD")

    _drop_line(base, "shared/DEPENDENCY-GRAPH.md", "`AUDIT-TRAIL-SPEC.md` | ACTIVE", 1)
    _drop_line(base, "shared/DEPENDENCY-GRAPH.md", "`tools/hash_chain_verify.py` + `append_event.py`", 1)
    _drop_line(base, "shared/DEPENDENCY-GRAPH.md", "`raport-sytuacyjny-integracja.md` | ACTIVE", 1)

    _drop_line(base, "shared/tools/README.md", "| `append_event.py` + `hash_chain_verify.py`", 1)
    _repl(base, "shared/tools/README.md",
"""Przy naprawie okazało się, że **ten sam commit usunął też 5 dalszych narzędzi**,
nigdzie w rejestrze F-206 niewymienionych, choć wciąż opisanych jako „ACTIVE"
w `shared/DEPENDENCY-GRAPH.md`, `shared/AUDIT-TRAIL-SPEC.md` i
`shared/MCP-INTEGRACJA.md`: `append_event.py`, `hash_chain_verify.py`,
`router_event_parser.py` (log audytowy hash-chain), oraz `test_mcp_protocol.py`,
`connector_health_check.py` (testy/health-check connectorów MCP). Wszystkie 8
przywrócono bajt-w-bajt z rodzica tego commitu (klon repozytorium, dostęp
odczytu) i zweryfikowano funkcjonalnie:""",
"""Przy naprawie okazało się, że **ten sam commit usunął też 2 dalsze narzędzia**,
nigdzie w rejestrze F-206 niewymienionych, choć wciąż opisanych jako „ACTIVE"
w `shared/DEPENDENCY-GRAPH.md` i `shared/MCP-INTEGRACJA.md`:
`test_mcp_protocol.py`, `connector_health_check.py` (testy/health-check
connectorów MCP). Wszystkie 5 przywrócono bajt-w-bajt z rodzica tego commitu
(klon repozytorium, dostęp odczytu) i zweryfikowano funkcjonalnie:""")

    _repl(base, "shared/MOD-WEJSCIE-DOKUMENTU.md",
"""> `pisma-procesowe-v3`, `pisma-proste-v2`, `przesluchanie-swiadkow-v2-min90`,
> `raport-sytuacyjny-v2 (poza pluginem)`. Treści NIE kopiuje się do skilli — skill woła ten plik""",
"""> `pisma-procesowe-v3`, `pisma-proste-v2`, `przesluchanie-swiadkow-v2-min90`.
> Treści NIE kopiuje się do skilli — skill woła ten plik""")
    _repl(base, "shared/MOD-MAPA-PRZEPISOW.md",
"""Pozwala to w zakładce "Historia strategii" (raport-sytuacyjny-v2 (poza pluginem)) porównać,
czy między wersjami zmieniła się ocena zgodności tezy dla danego przepisu""",
"""Pozwala to porównać między wersjami, czy zmieniła się ocena zgodności tezy dla danego przepisu""")
    _repl(base, "shared/MOD-WALIDACJA_v2.md",
"""Raport podsumuje: strony, żądania, dowody, terminy, ryzyka i kolejne kroki —
w formie interaktywnego widgetu gotowego do wydruku lub edycji.

Wpisz 'raport' lub kliknij aby uruchomić."

→ Na potwierdzenie: wywołaj raport-sytuacyjny-v2 (poza pluginem) natychmiast.
→ Raport generuje się automatycznie z danych rozmowy (bez ponownego podawania).
```

```
RAPORT WALIDACJI PISMA PROCESOWEGO""",
"""```

```
RAPORT WALIDACJI PISMA PROCESOWEGO""")
    _repl(base, "shared/MOD-PRIORYTETY-ASPEKTOW.md",
          "istnieje, checkbox steruje TYLKO czy trafia do dashboardu/raport-sytuacyjny).",
          "istnieje, checkbox steruje TYLKO czy trafia do dashboardu).")
    _repl(base, "shared/MOD-WARIANTY-POZWU.md",
          "  Ryzyko:       [P1/P2/P3 — zgodnie z konwencją raport-sytuacyjny-v2 (poza pluginem)",
          "  Ryzyko:       [P1/P2/P3 — zgodnie z konwencją P1/P2/P3")
    _repl(base, "shared/MOD-WARIANTY-POZWU.md",
          "  (raport-sytuacyjny-v2 (poza pluginem)), nie wymyślone ad hoc?",
          "  nie wymyślone ad hoc?")
    methods = "shared/MOD-METODY-BADAWCZE.md"
    for old, new in (
        ("mapę ryzyk w `raport-sytuacyjny-v2 (poza pluginem)`, oraz", "mapę ryzyk w dashboardzie sprawy oraz"),
        ("Wyjście zasila MET-FTL-tab w raport-sytuacyjny-v2 (poza pluginem).", "Wyjście zasila MET-FTL-tab w dashboardzie sprawy."),
        ("raport-sytuacyjny-v2 (poza pluginem) jeśli wykryto niespójność roli.", "dashboard sprawy, jeśli wykryto niespójność roli."),
        ('sekcję "Stan faktyczny" w raport-sytuacyjny-v2 (poza pluginem).', 'sekcję "Stan faktyczny" w dashboardzie sprawy.'),
        ("tego pliku — MET-PT był osiągalny tylko z raport-sytuacyjny-v2 (poza pluginem).", "tego pliku — MET-PT był osiągalny tylko z dashboardu sprawy."),
        ("raport-sytuacyjny-v2 (poza pluginem)) → auto-aktywacja.", "dashboard sprawy) → auto-aktywacja."),
        ("INTEGRACJA:  Wejście: SOURCE-STATUS-MATRIX (raport-sytuacyjny-v2 (poza pluginem)) + MD4-pokrycie.", "INTEGRACJA:  Wejście: SOURCE-STATUS-MATRIX (dashboard sprawy) + MD4-pokrycie."),
        ('Wyjście: zasila "Luki dowodowe" w raport-sytuacyjny-v2 (poza pluginem) oraz', 'Wyjście: zasila "Luki dowodowe" w dashboardzie sprawy oraz'),
    ):
        _repl(base, methods, old, new)

    _repl(base, "odczyt-dokumentow/document_contract/scripts/contract.py",
"""Zero zaleznosci zewnetrznych (Python 3.11+ stdlib). RODO-safe, offline.
Article I (zero-cloud), Article IV (determinizm/audyt) konstytucji projektu.""",
"""Zero zaleznosci zewnetrznych (Python 3.11+ stdlib). Offline.
Article I (offline), Article IV (determinizm/audyt) konstytucji projektu.""")

    # --- CHECKSUMS i rejestr audytu: usuń wpisy usuniętych plików ---
    stale = {
        "shared/CHECKSUMS.sha256": ["./AUDIT-TRAIL-SPEC.md", "./raport-sytuacyjny-integracja.md",
                                    "./tools/append_event.py", "./tools/hash_chain_verify.py",
                                    "./tools/router_event_parser.py"],
        "prawny-router-v3/CHECKSUMS.sha256": ["./references/KANCELARIA-WORKFLOW.md"],
    }
    for path, needles in stale.items():
        full = os.path.join(base, path)
        lines = open(full, encoding="utf-8").readlines()
        kept = [line for line in lines if not any(n in line for n in needles)]
        if len(kept) == len(lines):
            sys.exit(f"retire_layers: {path}: nie usunięto wpisów CHECKSUMS")
        open(full, "w", encoding="utf-8").writelines(kept)
    _drop_line(base, "audyt-systemu-v4/references/CHECKLIST-DEDUP.md",
               "Audit-trail / hash-chain zdarzeń zgodny z art. 12 AI Act", 1)

    # --- pliki warstwy kancelaryjnej i audytowej ---
    for path in ("prawny-router-v3/references/KANCELARIA-WORKFLOW.md",
                 "shared/raport-sytuacyjny-integracja.md",
                 "shared/AUDIT-TRAIL-SPEC.md",
                 "shared/tools/append_event.py",
                 "shared/tools/hash_chain_verify.py",
                 "shared/tools/router_event_parser.py"):
        _remove(base, path)


def strip_restored_host_rules(base):
    """Blok `shared-rules` to governance obcego pluginu, nie mechanika skilla.

    `humanizer-pl` jest przywracany 1:1 ze źródła po `retire_layers.apply`, więc blok
    trzeba zdjąć osobno - inaczej wraca sprzeczność („wynik to draft", „bez konektorów",
    odwołanie do nieistniejącego w tym pluginie pluginu weryfikacyjnego).
    """
    import re
    path = os.path.join(base, "humanizer-pl/SKILL.md")
    text = open(path, encoding="utf-8").read()
    block = re.search(r"\n?<!-- shared-rules:begin.*?<!-- shared-rules:end -->\n?", text, re.S)
    if not block:
        sys.exit("retire_layers: humanizer-pl/SKILL.md: brak bloku shared-rules do zdjęcia")
    text = text[:block.start()] + (
        "\nReguły pracy (zakres, bramka decyzji autora, weryfikacja źródeł) są w `shared/ZASADY-PLUGINU.md`.\n"
    ) + text[block.end():]
    open(path, "w", encoding="utf-8").write(text)
