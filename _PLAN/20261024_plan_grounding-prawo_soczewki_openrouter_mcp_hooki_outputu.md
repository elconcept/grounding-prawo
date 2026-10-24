---
tytul: Plan zmian grounding-prawo - soczewki przez OpenRouter, stop przy awarii MCP, hooki ograniczające output
data: 2026-10-24
dotyczy: plugins/grounding-prawo/skills/szturm-na-draft-pl (SKILL.md, references/soczewki.md, scripts/), plugins/grounding-prawo/skills/shared (ZASADY-PLUGINU.md, MCP-INTEGRACJA.md), plugins/grounding-prawo/hooks (hooks.json + nowe skrypty)
wzorzec błędu: legal/sprawy/II_W_1342_26_kamera_TK_obwiniony/_robocze/20261024_1540_szturm_czytelnia/ (sesja 24.10.2026, szturm wniosku o sprostowanie protokołu i wniosku o ustalenie miejsca przedmiotu)
stan: do wdrożenia
priorytet: blokujący - pipeline szturmu nie jest używany do czasu wdrożenia
---

# Plan: soczewki poza modelem koordynującym, twardy stop przy awarii MCP, output ograniczony hookami

## 1. Polecenie użytkownika (24.10.2026, dosłownie)

1. „WPROWADZIĆ ABSOLUTNY ZAKAZ PROWADZENIA SOCZEWEK PRZEZ MODEL URUCHAMIAJĄCY SZTURM. SOCZEWKI MAJĄ BYĆ URUCHAMIANE W FORMIE ZAPYTANIA API DO OPENROUTER, NA ENDPOINT https://openrouter.ai/api/v1/chat/completions model openrouter/free”.
2. „JEŻELI JEST PROBLEM Z KTÓRYMŚ MCP, KTÓREGO MODEL ZAMIERZAŁ UŻYĆ, MUSI SIĘ ZATRZYMAĆ I ZAPYTAĆ INTERAKTYWNIE CO ZROBIĆ W ZWIĄZKU Z BRAKIEM ODPOWIEDZI PRZEZ MCP”.
3. „OUTPUT MODELU TRZEBA OGRANICZYĆ HOOKAMI, SAME ZASADY NIE WYSTARCZAJĄ”.

## 2. Co poszło źle w sesji 24.10.2026

| Nr | Zdarzenie | Naruszona reguła albo luka |
|---|---|---|
| B1 | Koordynator sam odegrał wszystkie soczewki (sędzia, przeciwnik, cytaty, styl, subsumpcja) w jednym kontekście i wpisał ich nazwy w pole `soczewki` ustaleń. Szturm faktycznie się nie odbył. | SKILL.md każe uruchamiać soczewki w osobnych kontekstach, ale niczego nie wymusza; `synteza.py` przyjmuje JSON z dowolną nazwą soczewki bez dowodu, że soczewka działała. |
| B2 | ISAP (`mcp__lex__isap_get_act_text`, `isap_search_acts`) zwrócił HTTP 502. Model bez pytania przeszedł na WebFetch, a potem na curl + pdftotext na komputerze użytkownika. | Brak reguły stop-and-ask; reguła „konektor offline → NIEPEWNE” zachęca do obejść. |
| B3 | Odpowiedź końcowa: tabele ustaleń, powtórzenie tych samych treści w trzech miejscach (tabela, komentarze, podsumowanie), sekcja „Pytania bez odpowiedzi” z trzema pozycjami: (1) pytanie o fakt, który autor już rozstrzygnął (czy wspomnieć w piśmie o nagraniu - autor nie prosił, korzyści brak); (2) propozycja pisma w innym wątku (wniosek dowodowy do Policji), o którym model nie miał żadnych danych; (3) oświadczenie bez pytania (ocena zgodności postępowania sędziego z art. 21 § 2 k.p.s.w. przy relacji, która tylko cytuje sędziego). | Szablon raportu w SKILL.md sam zawiera tabelę i sekcję pytań; brak hooka na odpowiedź końcową. |

## 3. Zmiana A - soczewki wyłącznie przez OpenRouter (zakaz absolutny)

### A.1 Reguła (SKILL.md, references/soczewki.md, shared/ZASADY-PLUGINU.md)

- Model uruchamiający szturm (koordynator) **nie formułuje ustaleń soczewek**. Robi tylko: E0 (przyjęcie zmian, snapshot), wywołanie skryptu soczewek, E5-E6 (`synteza.py`), E7 (redline), E9 (rejestry).
- Każda soczewka E1-E4 (w tym `atak-przeciwnika-pl`, `pierwsze-wrazenie-sedziego-pl`, `adversarial-legal-review-pl`, `subsumpcja-pl`, `marko-pl-content`, `deliverable-fidelity-pl`, `ocena-outputu-pl`) = jedno zapytanie API (debata = osobne zapytania na rolę).
- Zakaz obejmuje także: „soczewki w jednym kontekście”, subagentów tego samego hosta zamiast API i wpisywanie nazwy soczewki do ustaleń napisanych przez koordynatora.
- Brak klucza, błąd HTTP, limit dzienny albo niepoprawny JSON z API → stop i pytanie interaktywne (zmiana B), nigdy zastępcze odegranie roli przez koordynatora.

### A.2 Wywołanie (wzorzec użytkownika)

```json
{
  "method": "POST",
  "url": "https://openrouter.ai/api/v1/chat/completions",
  "headers": {
    "Authorization": "Bearer OPENROUTER_API_KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "openrouter/free",
    "messages": [
      {"role": "user", "content": "This is Free Tier Random Model Endpoint limited to 1000 requests per day!"}
    ]
  }
}
```

- Klucz ze zmiennej środowiskowej `OPENROUTER_API_KEY` (nie w repo, nie w logach, nie w plikach przebiegu).
- `openrouter/free` to losowy darmowy model z limitem 1000 zapytań dziennie: skrypt zapisuje w odpowiedzi pole `model` (faktycznie użyty model) i liczy zapytania sesji.

### A.3 Nowy skrypt `szturm-na-draft-pl/scripts/soczewka_openrouter.py`

- Wejście: `--soczewka <nazwa>`, `--draft <clean.md>`, `--teza <plik>`, opcjonalnie `--akta <katalog>` (tylko dla soczewek, którym mandat w `references/soczewki.md` daje akta; sędzia i przeciwnik dostają sam draft i tezę), `--out RUN/ustalenia/<NN>_<soczewka>.json`.
- Prompt systemowy = mandat soczewki z `references/soczewki.md` + `references/schemat-ustalenia.json` + polecenie zwrotu wyłącznie tablicy JSON.
- Walidacja odpowiedzi schematem; przy niezgodności 1 ponowienie, potem kod wyjścia ≠ 0 (stop).
- Do każdego ustalenia skrypt dopisuje pole `_proweniencja`: `{"endpoint", "model_zadany": "openrouter/free", "model_uzyty", "id_odpowiedzi", "czas", "sha256_promptu", "sha256_odpowiedzi"}`. Surowa odpowiedź API idzie do `RUN/api/<NN>_<soczewka>.json`.

### A.4 Wymuszenie w kodzie

- `synteza.py`: ustalenie bez `_proweniencja` albo z hashem niezgodnym z plikiem w `RUN/api/` → odrzucone przez schemat (exit 1). Wyjątek tylko dla soczewek deterministycznych E1 uruchamianych skryptem (`citation-grounding-pl`), które mają własną proweniencję skryptu.
- Hook `PreToolUse` (Write/Edit/device write) blokuje zapis do `*/ustalenia/*.json` innym narzędziem niż `soczewka_openrouter.py` (koordynator nie może ręcznie zapisać pliku ustaleń).

## 4. Zmiana B - awaria MCP = stop i pytanie interaktywne

### B.1 Reguła (shared/ZASADY-PLUGINU.md, shared/MCP-INTEGRACJA.md, szturm-na-draft-pl/SKILL.md)

- Błąd, timeout, HTTP 5xx/4xx albo pusta odpowiedź narzędzia MCP, którego model zamierzał użyć (lex: isap, ustawy, repertorium, saos, nsa, ocr; basic-memory; IURA), zatrzymuje pracę.
- Kolejne wywołanie po błędzie to wyłącznie narzędzie pytań interaktywnych (AskUserQuestion), z nazwą narzędzia, błędem i opcjami: ponów teraz / poczekaj i ponów / użyj wskazanego źródła zastępczego / pomiń ten krok z adnotacją w piśmie / przerwij.
- Zakaz samodzielnych obejść: WebFetch, curl, pobieranie PDF, inne MCP, pamięć modelu - tylko po wyborze użytkownika.
- Usunąć ze SKILL.md szturmu regułę „Konektor offline → wynik oznaczony jako niezweryfikowany … nigdy OK” jako alternatywę dla zatrzymania; zostaje tylko jako adnotacja po decyzji użytkownika „pomiń”.

### B.2 Wymuszenie hookami (`plugins/grounding-prawo/hooks/`)

- `mcp_awaria.py` na zdarzeniu błędu narzędzia (PostToolUse z błędem albo PostToolUseFailure - zależnie od wersji hosta; dopasowanie `mcp__.*`): zapisuje stan `awaria_mcp` (narzędzie, błąd, czas) w pliku stanu sesji.
- `mcp_awaria_blokada.py` na `PreToolUse` (wszystkie narzędzia): gdy stan `awaria_mcp` jest aktywny, przepuszcza tylko AskUserQuestion; reszta → `deny` z komunikatem „Awaria MCP <narzędzie>: zapytaj użytkownika (AskUserQuestion), zanim użyjesz innego narzędzia”. Odpowiedź użytkownika (PostToolUse AskUserQuestion) czyści stan.
- Rejestracja w `hooks.json` obok istniejących `SessionStart` i `PreCompact`.

## 5. Zmiana C - output ograniczony hookami

### C.1 Szablon raportu (SKILL.md szturmu, sekcja „Raport dla użytkownika”)

- Raport końcowy szturmu = najwyżej 6 linii bez tabel: stan GOTOWE/NIEGOTOWE, liczby ustaleń, wynik E1, ścieżki plików z liczbą w:ins/w:del, ograniczenia (tylko gdy są).
- Usunąć sekcję „Pytania bez odpowiedzi” z szablonu. Pytania padają wyłącznie w trakcie pętli przez AskUserQuestion; w odpowiedzi końcowej ich nie ma.
- Lista ustaleń zostaje w plikach (`raport_synteza.md`, komentarze Worda), nie w czacie.

### C.2 Zakazy treści pytań i raportu (reguła + test w hooku)

- Nie pytać o fakty i decyzje, które autor już podał albo które wynikają z jego materiału (np. czy ujawnić w piśmie źródło informacji, którego autor nie kazał ujawniać).
- Nie proponować pism, wniosków ani czynności w innych wątkach niż zlecony; szturm dotyczy wyłącznie wskazanych pism.
- Nie przedstawiać jako pytania oceny legalności zachowania organu, gdy pismo tylko relacjonuje to zachowanie; nie oczekiwać od autora „oceny” cytatu.
- Każde pytanie musi być pytaniem (kończy się „?”), dotyczyć zmiany w piśmie objętym szturmem i mieć opcje odpowiedzi.

### C.3 Hook `Stop` - `kontrola_outputu.py`

Sprawdza ostatnią odpowiedź modelu przed oddaniem jej użytkownikowi; przy naruszeniu `decision: block` z powodem (model poprawia odpowiedź):

| Test | Próg (do kalibracji) |
|---|---|
| tabele markdown (`\|---`) bez słowa „tabel” w ostatnim poleceniu użytkownika | 0 |
| długość odpowiedzi końcowej szturmu | ≤ 1200 znaków |
| nagłówki sekcji `Pytania`, `Pytania bez odpowiedzi`, `Do decyzji` w odpowiedzi końcowej | 0 |
| punkty w sekcji pytań bez „?” | 0 |
| powtórzenia: zdania o podobieństwie ≥ 0,8 (shingle 5-słowne) w obrębie odpowiedzi | 0 |
| sygnatury, numery spraw i nazwy pism spoza teczki zleconej sprawy | 0 |

Licznik blokad w stanie sesji: po 2 blokadach z rzędu hook przepuszcza odpowiedź z dopisaną linią „[kontrola_outputu: naruszenia N]”, żeby nie zapętlić sesji.

## 6. Kolejność wdrożenia

1. Zmiana B (hooki awarii MCP) - najmniejsza, odblokowuje pracę na innych skillach.
2. Zmiana A (skrypt OpenRouter, proweniencja w `synteza.py`, blokada zapisu ustaleń).
3. Zmiana C (szablon raportu, hook `Stop`).
4. `tests/smoke_test.sh`: przypadki testowe dla A (ustalenie bez proweniencji → exit 1), B (symulowany błąd MCP → następne narzędzie inne niż AskUserQuestion zablokowane), C (odpowiedź z tabelą i sekcją pytań → block).
5. Podbicie wersji pluginu i wpis w `_log/`.

## 7. Kryterium odbioru

- Szturm na piśmie testowym: w `RUN/api/` jest surowa odpowiedź OpenRouter dla każdej soczewki, a każde ustalenie w `ustalenia.scalone.json` ma `_proweniencja` zgodną z tym plikiem.
- Wymuszony błąd ISAP: model zatrzymuje się i zadaje pytanie interaktywne; zero wywołań WebFetch/curl przed odpowiedzią.
- Odpowiedź końcowa szturmu: bez tabel, ≤ 6 linii, bez sekcji pytań, bez treści spoza zleconych pism.
