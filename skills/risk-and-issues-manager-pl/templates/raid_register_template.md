# RAID Register - {{NAZWA_SPRAWY}}

> Plik logiczny - render do .xlsx z 4 arkuszami. W repo trzymany jako markdown dla wygody review.

| Klient | {{KLIENT}} |
|---|---|
| Sprawa / kod | {{SPRAWA_REF}} |
| Data ostatniej aktualizacji | {{DATA_AKTUALIZACJI}} |
| Wlasciciel rejestru | {{WSPOLNIK_PROWADZACY}} |

---

## Arkusz 1 - Ryzyka (Risks)

> Rzecz ktora MOZE sie wydarzyc, jeszcze nie nastapila. Ma prawdopodobienstwo i wplyw.

| ID | Data ident. | Opis ryzyka | Prawd. | Wplyw | RAG | Mitigacja | Wlasciciel | Termin walidacji | Status |
|---|---|---|---|---|---|---|---|---|---|
| R-{{ID}} | {{DATA}} | {{OPIS}} | {{PRAWD}} | {{WPLYW}} | {{RAG}} | {{MITIGACJA}} | {{WLASCICIEL}} | {{TERMIN}} | {{STATUS}} |

### Konwencja oceny

**Prawdopodobienstwo (P)**:
- Niskie (<25%) | Srednie (25-60%) | Wysokie (>60%) | Pewne (>90%, klasyfikuj jako Problem)

**Wplyw (W)**:
- Niski - nieznaczny, mozemy ogarnac.
- Sredni - opoznienie milestone'u 1-2 tyg, zmiana strategii, dowieziemy.
- Wysoki - opoznienie miesieczne, zagrozenie wyniku, eskalacja wspolnik.
- Krytyczny - utrata sprawy / naruszenie tajemnicy / RODO incydent / dyscyplinarka, eskalacja klient + zarzad.

**RAG**:
- Zielony: W niski OR P niskie.
- Bursztynowy: W sredni + P srednie.
- Czerwony: W wysoki AND P srednie+; lub W krytyczny.

**Status**:
- Otwarte | Mitigacja w toku | Zaakceptowane (decyzja "akceptujemy ryzyko") | Zamkniete (juz nieaktualne lub przeszlo w Problem).

---

## Arkusz 2 - Zalozenia (Assumptions)

> Rzecz ktora przyjmujemy za prawde bez weryfikacji. Wymaga walidacji do okreslonej daty.

| ID | Data ident. | Opis zalozenia | Zrodlo zalozenia | Termin walidacji | Status walidacji | Notatki |
|---|---|---|---|---|---|---|
| Z-{{ID}} | {{DATA}} | {{OPIS}} | {{ZRODLO}} | {{TERMIN_WALIDACJI}} | {{STATUS_WALIDACJI}} | {{NOTATKI}} |

### Konwencja

**Status walidacji**:
- Otwarte | W toku | Zwalidowane (potwierdzone) | Falsyfikowane (zalozenie bledne -> przenosi do Ryzyk lub Problemow) | Nieaktualne.

---

## Arkusz 3 - Problemy (Issues)

> Rzecz ktora JUZ sie wydarzyla i blokuje sprawe. Wymaga rozwiazania.

| ID | Data wystapienia | Opis problemu | Wplyw | Plan rozwiazania | Wlasciciel | Termin | Status |
|---|---|---|---|---|---|---|---|
| P-{{ID}} | {{DATA}} | {{OPIS}} | {{WPLYW}} | {{PLAN}} | {{WLASCICIEL}} | {{TERMIN}} | {{STATUS}} |

### Konwencja

**Status**:
- Otwarte | Rozwiazanie w toku | Eskalowane | Rozwiazane | Zaakceptowane (decyzja "zyjemy z tym").

---

## Arkusz 4 - Decyzje (Decisions)

> Decyzja JUZ podjeta z konsekwencjami dla sprawy. Wymaga zapisu dla audytu i przyszlych raportow.

| ID | Data | Decyzja | Decydent | Uzasadnienie | Wplyw na sprawe | Notatki |
|---|---|---|---|---|---|---|
| D-{{ID}} | {{DATA}} | {{DECYZJA}} | {{DECYDENT}} | {{UZASADNIENIE}} | {{WPLYW}} | {{NOTATKI}} |

### Konwencja

**Decydent**:
- Wlasna kancelaria: aplikant / radca prawny / wspolnik prowadzacy / wspolnik zarzadzajacy.
- Klient: osoba kontaktowa / zarzad / rada nadzorcza.
- Zewnetrzni: sad (postanowienie) / organ administracji / biegly.

---

## Konwencja ID

Format: `{R|Z|P|D}-YYYY-MM-XXX`, gdzie XXX = kolejny numer w danym miesiacu w obrebie tej sprawy.

Przyklad: `R-2026-05-003` = trzecie ryzyko zidentyfikowane w maju 2026 w tej sprawie.

---

## Eskalacje powiazane

| Data eskalacji | RAID ID | Adresat | Status | Plik eskalacji |
|---|---|---|---|---|
| {{DATA}} | {{RAID_ID}} | {{ADRESAT}} | {{STATUS}} | [{{LINK}}](path) |

---

> *RAID prowadzony przez risk-and-issues-manager-pl v{{SKILL_VERSION}}. Skill jest asystentem. Klasyfikacja konfliktu interesow i RODO incydentow wymaga konsultacji wspolnika zarzadzajacego.*
