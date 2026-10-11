---
name: frontmatter
description: Legenda kluczy frontmatteru YAML dla skilla pdf-generation (szablony `oswiadczenie` i `pismo-procesowe`). Użyj PRZED napisaniem pliku .md, który ma trafić do generate_pdf.py — żeby od razu użyć właściwych kluczy zamiast trafiać na ciche fallbacki/defaulty.
---

# Legenda frontmatteru dla pdf-generation

Ten skill nie generuje PDF-ów sam — to ściąga referencyjna dla
[`pdf-generation`](../pdf-generation/SKILL.md). Konsultuj go **przed**
napisaniem frontmatteru pliku `.md`, który potem pójdzie przez
`generate_pdf.py`. Zasada ogólna (patrz też `pdf-generation/SKILL.md`):
pole, do którego żaden szablon się nie odwołuje, jest **niewidoczne w PDF**
— możesz trzymać w frontmatterze notatki robocze (`uwagi`, `numer_karty`,
`status` itd.) bez ryzyka wycieku do dokumentu.

## Szablon `pismo-procesowe` (`--template pismo-procesowe`)

Pismo procesowe do sądu, prokuratury lub innego organu — odpowiedź na pozew,
zażalenie, zawiadomienie, wniosek. **Nie** do oświadczeń własnych (patrz
szablon `oswiadczenie` niżej).

| Klucz | Typ | Domyślne / fallback | Znaczenie |
|---|---|---|---|
| `pismo_tytul` | string | fallback: `tytul` → `dokument` → `typ_dokumentu` → `rodzaj_dokumentu` → `pismo` (pierwszy znaleziony); jeśli żaden — brak tytułu w PDF | Tytuł pisma, wyśrodkowany, 14pt, automatyczne WERSALIKI |
| `miejscowosc` | string | puste pole „…………” jeśli brak | Miejscowość w prawym górnym rogu |
| `data` | string (bez "r.") | fallback: `data_dokumentu` → `data_pisma`; jeśli żaden — brak daty | Data pisma. Nie dopisuj "r." — szablon dopisuje sam |
| `sygnatura_akt` | string | fallback: `sygnatura` → `sygn`; jeśli żaden — brak sygnatury w nagłówku (poprawna sytuacja, np. sprawa bez nadanej sygnatury) | Sygnatura akt, powtarza się w nagłówku każdej strony jako "sygn. \<wartość\>" |
| `nadawca_nazwa` | string | brak / `""` = puste pole „……………” do wpisania | Imię i nazwisko/nazwa strony składającej pismo, 14pt |
| `nadawca_adres` | lista stringów | jeśli `nadawca_nazwa` brak: dwie puste linie „……………” do wpisania | Kolejne linie adresu/kontaktu nadawcy, rozmiar bazowy (10 lub 12pt) |
| `nadawca_rola` | string | brak = nie pokazuje się linia roli | Rola procesowa nadawcy, np. "Pozwany", "Wnioskodawca" (kursywa) |
| `odbiorca` | string **lub lista stringów** | brak = brak bloku odbiorcy (poprawna sytuacja, np. oświadczenie bez konkretnego adresata) | **Jeden string = jeden odbiorca.** Format: `"Nazwa, linia adresu 1, linia adresu 2, ..."` — każdy przecinek zaczyna nową linię, segment przed pierwszym przecinkiem to nazwa (14pt bold), reszta to adres (rozmiar bazowy). **Lista z >1 elementem**: pierwszy string = odbiorca główny, pozostałe renderują się pod nagłówkiem "Do wiadomości:", każdy sparsowany tak samo |
| `wartosc_przedmiotu_sporu` | string | brak = nie pokazuje się | Linia "Wartość przedmiotu sporu: ..." |
| `zalaczniki` | lista stringów | brak = brak sekcji | Numerowana lista załączników na końcu pisma, 9pt, bez pogrubienia |
| `skladajacy` | string | brak = brak bloku podpisu | Imię i nazwisko pod tekstem (prawa strona) |
| `bez_numeracji_stron` | bool | domyślnie numeracja WŁĄCZONA | `true` wyłącza numerację stron |

### Ważne o treści (ciało dokumentu, pod `---`)

- `#` (H1) jest **całkowicie ignorowany** — nawet jeśli go użyjesz, zniknie
  bez śladu z PDF. Tytuł pisma bierz wyłącznie z `pismo_tytul`/synonimów.
- `##` i `###` renderują się identycznie: WERSALIKI, bez pogrubienia, bez
  numeracji. Używaj ich do części pisma (np. `## Uzasadnienie`) i podsekcji
  (np. `### Stan faktyczny`) — wizualnie nie ma między nimi różnicy, więc
  wybór poziomu to kwestia struktury dokumentu, nie wyglądu.
- Listy numerowane/wypunktowane renderują się normalnie (przydatne np. do
  petitum: "wnoszę o: 1. ... 2. ...").

### Przykład — odpowiedź na pozew, jeden odbiorca

```yaml
---
pismo_tytul: "Odpowiedź na pozew"
data: "6 września 2026"
sygnatura_akt: "I C 123/26"
nadawca_rola: "Pozwany"
odbiorca: "Sąd Rejonowy dla Warszawy-Śródmieścia, I Wydział Cywilny, ul. Marszałkowska 82, 00-517 Warszawa"
wartosc_przedmiotu_sporu: "10 000,00 zł"
zalaczniki:
  - "odpis pełnomocnictwa"
  - "dowód nadania odpisu pisma pełnomocnikowi powoda"
skladajacy: "Jan Kowalski"
---

W imieniu własnym, w odpowiedzi na pozew (...), wnoszę o:

1. oddalenie powództwa w całości;
2. zasądzenie kosztów postępowania według norm przepisanych.

## Uzasadnienie

### Stan faktyczny

(...)
```

`nadawca_nazwa`/`nadawca_adres` pominięte - szablon wstawi puste pola nadawcy
do wpisania. Nie uzupełniaj ich danymi z innej sprawy: gdy nadawca nie jest znany,
zostaw klucze puste (`nadawca_nazwa: ""`).

### Przykład — zawiadomienie z kilkoma odbiorcami ("Do wiadomości")

```yaml
---
pismo_tytul: "Zawiadomienie o podejrzeniu popełnienia przestępstwa"
sygn: "PR 1 Ds. 45.2026"
odbiorca:
  - "Prokuratura Rejonowa Warszawa-Śródmieście, ul. Wiślicka 6, 02-114 Warszawa"
  - "Rzecznik Praw Obywatelskich"
zalaczniki:
  - "kopia nagrania"
---

## Uzasadnienie zawiadomienia

(...)
```

Pierwszy element listy (Prokuratura) trafia do głównego bloku adresata,
drugi (Rzecznik) pod "Do wiadomości:".

## Szablon `oswiadczenie` (`--template oswiadczenie`, domyślny)

Oświadczenie własne strony przeznaczone do podpisu kwalifikowanego lub
ePUAP (mechanizm reguły 2 `AGENTS.md` w repo `kancelaria`) — **nie** pismo
procesowe do konkretnego adresata (do tego służy `pismo-procesowe` wyżej).

| Klucz | Typ | Znaczenie |
|---|---|---|
| `data_dokumentu` | string (bez "r.") | Data u góry strony |
| `sygnatura_akt` | string | Nagłówek strony, prawa strona: "Sygn. akt: ..." |
| `sygnatura_rsow` | string | Nagłówek strony, lewa strona: "Sygn. RSOW: ..." |
| `skladajacy` | string | Podpis pod tekstem, z adnotacją o wymaganym podpisie kwalifikowanym/ePUAP |

Tytuł "OŚWIADCZENIE" jest zawsze stały (nie konfigurowalny frontmatterem).
`#` w treści renderuje się jako nienumerowany podtytuł kursywą (nie jako
kolejna sekcja pisma).

## Klucze wspólne obu szablonom

`skladajacy` i `sygnatura_akt` działają tak samo pojęciowo w obu szablonach
(podpis / sygnatura), ale renderują się w innym miejscu strony — sprawdź
sekcję właściwego szablonu wyżej, nie zakładaj identycznego wyglądu.

## Dodawanie nowych kluczy

Jeśli dodajesz nowy klucz do `templates/pismo-procesowe.latex` lub
`templates/oswiadczenie.latex`, zaktualizuj też ten plik — inaczej przyszła
sesja (własna lub inna) będzie zgadywać nazwy kluczy albo pisać pisma bez
wykorzystania nowej funkcjonalności szablonu.
