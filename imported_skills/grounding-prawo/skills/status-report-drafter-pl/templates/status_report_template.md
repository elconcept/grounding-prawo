# Status sprawy: {{NAZWA_SPRAWY}}

| Klient | {{KLIENT}} |
|---|---|
| Sprawa / kod | {{SPRAWA_REF}} |
| Okres raportowy | {{OD_DATA}} - {{DO_DATA}} |
| Autor raportu | {{AUTOR}} |
| Data raportu | {{DATA_RAPORTU}} |
| Poprzedni RAG | {{POPRZEDNI_RAG}} |

---

## Ocena ogolna - RAG

**{{RAG_KOLOR}}** - {{RAG_KROTKIE_UZASADNIENIE}}

### Uzasadnienie (patrzac na nastepne 2 tygodnie)

{{RAG_UZASADNIENIE_DLUGIE}}

> *Konwencja*: Zielony = milestone'y w 2-tyg horyzoncie pewne, brak otwartych eskalacji. Bursztynowy = jeden lub wiecej milestone'ow w zagrozeniu - patrz "Plan powrotu do Zielonego" ponizej. Czerwony = milestone nie do dowiezienia bez interwencji wspolnika lub klienta - patrz "Sciezka eskalacji" ponizej.

{{#IF_BURSZTYNOWY}}
### Plan powrotu do Zielonego

{{PLAN_POWROTU}}
{{/IF_BURSZTYNOWY}}

{{#IF_CZERWONY}}
### Sciezka eskalacji

- **Decydent**: {{ESKALACJA_DECYDENT}}
- **Wymagana decyzja**: {{ESKALACJA_DECYZJA}}
- **Termin decyzji**: {{ESKALACJA_TERMIN}}
- **Konsekwencja braku decyzji**: {{ESKALACJA_KONSEKWENCJA}}
{{/IF_CZERWONY}}

---

## Postep w okresie

{{POSTEP_LISTA}}

> *Konwencja*: postep ma date i mierzalny rezultat. "27.02 zlozono apelacje w SA Warszawa. 01.03 otrzymano postanowienie o przyjeciu do rozpoznania" - postep. "12 telefonow w tym tygodniu" - aktywnosc (patrz nizej).

---

## Aktywnosc bez postepu

{{AKTYWNOSC_LISTA}}

> *Jezeli wpis tu istnieje przez 2+ okresy raportowe - sygnal eskalacji.*

---

## Luki i cisze

{{LUKI_LISTA}}

> *Konwencja*: cisza to status, nie luka inputu. "Od 14 dni brak odpowiedzi z sadu na wniosek z 5.02" - raportowalne.

---

## Akcje na nastepny okres

| # | Akcja | Wlasciciel | Termin twardy | Eskalacja przy braku |
|---|---|---|---|---|
{{AKCJE_TABELA}}

> *Konwencja*: kazda akcja MUSI miec termin twardy i eskalacja. Brak = wpis WADLIWA, raport zwracany do uzupelnienia.

---

## Eskalacje otwarte

### Poziom zespol
{{ESKALACJE_ZESPOL}}

### Poziom wspolnik
{{ESKALACJE_WSPOLNIK}}

### Poziom klient
{{ESKALACJE_KLIENT}}

> *Test eskalacyjny*: "Jezeli sprawa pojdzie zle a wspolnik / klient nie wiedzial - czy to nasza wina raportowa?". Jezeli tak - eskalacja.

---

## Budzet

| Pozycja | Wartosc |
|---|---|
| Model rozlicen | {{MODEL_ROZLICZEN}} *(stawka godzinowa / ryczalt / hybryda / success fee z capem)* |
| % spalenia | {{PROCENT_SPALENIA}} |
| Prognoza-do-konca | {{PROGNOZA_DO_KONCA}} |
| Ostrzezenia overrun | {{OVERRUN_FLAGI}} |
| Zmiany scope w okresie | {{SCOPE_CHANGES}} *(z scope-change-controller-pl)* |

{{#IF_BUDZET_OK}}
Budzet w zakresie planowanym.
{{/IF_BUDZET_OK}}

{{#IF_BUDZET_RYZYKO}}
**UWAGA**: {{BUDZET_OSTRZEZENIE}}
{{/IF_BUDZET_RYZYKO}}

---

## Notatka dla wspolnika prowadzacego

{{NOTATKA_WSPOLNIK}}

---

> *Status wygenerowany przez status-report-drafter-pl v{{SKILL_VERSION}}. Skill jest asystentem. Decyzja o wyslaniu klientowi - tylko po przegladzie prawnika.*
> *Brand template: [Kancelaria]. Naglowek .docx zdefiniowany w `templates/[Kancelaria]_brand.docx`.*
