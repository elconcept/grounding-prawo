# Wniosek o rozszerzenie zakresu sprawy: {{NAZWA_SPRAWY}}

| Klient | {{KLIENT}} |
|---|---|
| Sprawa / kod | {{SPRAWA_REF}} |
| Numer umowy / oferty pierwotnej | {{UMOWA_REF}} |
| Data umowy / oferty | {{DATA_UMOWY}} |
| Data wniosku | {{DATA_WNIOSKU}} |
| Wspolnik prowadzacy | {{WSPOLNIK}} |

---

## 1. Pierwotny zakres umowy

Zgodnie z umowa o swiadczenie pomocy prawnej / oferta z dnia {{DATA_UMOWY}}, zakres obejmuje:

> {{CYTAT_KLAUZULI_ZAKRESU}}

---

## 2. Nowe zadanie - opis

Klient w wiadomosci z dnia {{DATA_ZAPYTANIA_KLIENTA}} zwrocil sie z prosba o:

> {{OPIS_NOWEGO_ZADANIA}}

---

## 3. Klasyfikacja - poza pierwotnym zakresem

Nowe zadanie **wykracza poza pierwotny zakres umowy** ze wzgledu na:

{{UZASADNIENIE_KLASYFIKACJI}}

---

## 4. Proponowany rozszerzony zakres

Proponujemy rozszerzenie zakresu o:

{{ZAKRES_ROZSZERZENIA}}

Czynnosci do wykonania:

{{LISTA_CZYNNOSCI}}

---

## 5. Wplyw budzetowy

| Pozycja | Wartosc |
|---|---|
| Model rozlicen | {{MODEL_ROZLICZEN}} *(stawka godzinowa / ryczalt / hybryda z success fee)* |
| Szacowany naklad pracy | {{NAKLAD_GODZIN}} *(jezeli stawka godzinowa)* |
| Dodatkowa kwota | {{DODATKOWA_KWOTA}} *(jezeli ryczalt; w przypadku stawki - obliczana wg polityki rozlicen kancelarii)* |
| Success fee cap (jezeli dotyczy) | {{SUCCESS_FEE_CAP}} *(z uwzglednieniem ograniczen art. 16 Kodeksu Etyki Adwokackiej / KEZRP)* |
| Termin platnosci | {{TERMIN_PLATNOSCI}} *(zgodnie z umowa pierwotna)* |

{{#IF_PACTUM_QUOTA}}
**UWAGA**: Proponowane rozliczenie obejmuje wynagrodzenie czesciowo zalezne od wyniku sprawy. Zgodnie z art. 16 Kodeksu Etyki Adwokackiej (analogicznie KEZRP dla radcow prawnych), wynagrodzenie wylacznie z udzialu w zasadzonym swiadczeniu (pactum de quota litis) jest niedozwolone. Proponowana konstrukcja stanowi success fee jako dodatek do stawki podstawowej.
{{/IF_PACTUM_QUOTA}}

---

## 6. Wplyw terminowy

{{WPLYW_NA_HARMONOGRAM}}

{{#IF_TERMIN_PROCESOWY_PILNY}}
**Pilne**: nowe zadanie wymaga interwencji do {{DEADLINE_PROCESOWY}}. Prosimy o decyzje do dnia {{DEADLINE_KLIENTA}}, w przeciwnym razie nie bedziemy mogli zapewnic dotrzymania terminu procesowego.
{{/IF_TERMIN_PROCESOWY_PILNY}}

---

## 7. Decyzja klienta

Prosimy o potwierdzenie:

- [ ] Akceptujemy rozszerzenie zakresu w proponowanej formie.
- [ ] Akceptujemy rozszerzenie z modyfikacjami (prosimy o kontakt).
- [ ] Nie akceptujemy rozszerzenia - prosimy o pozostanie przy pierwotnym zakresie umowy.

Termin decyzji: **{{TERMIN_DECYZJI}}**

W przypadku braku odpowiedzi do tego dnia, traktujemy zapytanie jako wstrzymane i kontynuujemy prace w pierwotnym zakresie.

---

## 8. Klauzula odpowiedzialnosci

Niniejszy wniosek stanowi propozycje rozszerzenia zakresu wspolpracy. Praca w rozszerzonym zakresie nie zostala podjeta i nie zostanie podjeta bez Panstwa pisemnej akceptacji niniejszego wniosku.

W razie pytan lub konsultacji prosimy o kontakt z wspolnikiem prowadzacym: **{{WSPOLNIK}}** ({{KONTAKT_WSPOLNIKA}}).

Z powazaniem,

{{PODPIS_KANCELARII}}

---

> *Wniosek wygenerowany przez scope-change-controller-pl v{{SKILL_VERSION}}. Skill jest asystentem. Decyzja o wyslaniu - tylko prawnik po przegladzie.*
> *Brand template: [Kancelaria]. Naglowek .docx zdefiniowany w `templates/[Kancelaria]_brand.docx`.*
