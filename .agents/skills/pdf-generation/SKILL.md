---
name: pdf-generation
description: Generuje profesjonalny PDF z dokumentu Markdown (pandoc + xelatex/MiKTeX), z szablonem prawniczym. Użyj gdy trzeba wygenerować PDF z .md do podpisu (kwalifikowanym podpisem elektronicznym lub ePUAP) albo jako pismo procesowe/oświadczenie do przedłożenia w sprawie.
---

# Generowanie PDF z Markdown

Narzędzie: `pandoc` (silnik `xelatex`, MiKTeX) + niestandardowy szablon LaTeX.
Wszystko w tym katalogu (`<skille>/pdf-generation/`) jest globalne — działa
w każdym projekcie, nie tylko tam, gdzie zostało pierwotnie napisane.

## Kiedy używać

- Trzeba wygenerować PDF z pliku `.md`, który ma zostać **podpisany cyfrowo**
  (kwalifikowany podpis elektroniczny lub podpis zaufany ePUAP) i użyty jako dowód
  lub pismo procesowe.
- Dokument musi wyglądać profesjonalnie — styl pisma sądowego/prawniczego, nie
  "wydruk z edytora tekstu".

## Zasada: frontmatter YAML nigdy nie trafia do PDF wprost

Pandoc traktuje blok YAML na górze pliku `.md` jako **zmienne szablonu**, nie jako
tekst dokumentu. Treść dokumentu w PDF to wyłącznie to, co jest **pod** blokiem
`---...---`. Szablon (`templates/*.latex`) decyduje, które zmienne z frontmatteru
w ogóle się pojawiają (np. `$data_dokumentu$`, `$sygnatura_akt$`) — pola, do których
szablon się nie odwołuje (np. `uwagi`, komentarze robocze), **nigdy nie trafiają do
PDF**, nawet jeśli są w pliku `.md`. To pozwala trzymać w `.md` notatki wewnętrzne
bez ryzyka, że wyciekną do dokumentu, który ktoś podpisze i złoży.

Nie pisz notatek roboczych w treści pod `---` (w ciele dokumentu) — tam trafiają
one do PDF dosłownie. Notatki należą wyłącznie do frontmattera.

## Użycie

```bash
python <skille>/pdf-generation/generate_pdf.py <plik.md>
```

Domyślnie: szablon `oswiadczenie`, silnik `xelatex`, wyjście `<plik>.pdf` obok
wejścia. Opcje: `--template <nazwa>` (szuka `templates/<nazwa>.latex`), `--engine`,
`--out <ścieżka>`.

Skrypt sam znajduje `xelatex`/MiKTeX nawet gdy nie ma go jeszcze w `PATH` bieżącej
powłoki (typowe zaraz po instalacji, przed restartem terminala).

## Szablon `oswiadczenie.latex`

Pismo w stylu prawniczym: Times New Roman 12pt, marginesy 2,5 cm, interlinia 1,5,
nagłówek z sygnaturą akt/sprawy (jeśli podana w frontmatterze), tytuł
"OŚWIADCZENIE", treść, blok podpisu z adnotacją o wymaganym podpisie kwalifikowanym
lub ePUAP. Nagłówek `#` w treści markdown renderuje się jako nienumerowany
podtytuł (nie jako kolejny rozdział) — tytuł "OŚWIADCZENIE" już nadaje strukturę.

Zmienne frontmatteru, które szablon renderuje w PDF: `data_dokumentu` (data, u góry
strony), `sygnatura_akt` / `sygnatura_rsow` (nagłówek strony), `skladajacy`
(podpis pod tekstem). Wszystkie inne pola frontmattera (`uwagi`, `numer_karty` itd.)
są niewidoczne w PDF — to zamierzone.

## Szablon `pismo-procesowe.latex`

Ogólne pismo procesowe do sądu, prokuratury lub innego organu (odpowiedź na
pozew, zażalenie, zawiadomienie, wniosek) — nie mylić z `oswiadczenie.latex`
(oświadczenie własne strony do podpisu kwalifikowanego/ePUAP wg reguły 2
`AGENTS.md`). **Pełna legenda kluczy frontmatteru dla tego szablonu żyje w
osobnym skillu [`frontmatter`](../frontmatter/SKILL.md)** — użyj go przy
pisaniu `.md`, żeby od razu użyć właściwych kluczy zamiast trafiać na ciche
fallbacki. Tu tylko podsumowanie zasad renderowania:

- **Czcionka**: Baskerville → Georgia → Times New Roman (pierwsza dostępna w
  systemie, sprawdzane w tej kolejności w czasie kompilacji przez
  `\IfFontExistsTF`). Baskerville/Georgia = 10pt bazowo; jeśli obie
  niedostępne, fallback Times New Roman = 12pt bazowo. Nazwy/nagłówki (patrz
  niżej) zawsze 14pt niezależnie od bazowego rozmiaru; adres pod nazwą
  wraca do rozmiaru bazowego automatycznie (zasięg brace w LaTeX-u).
- **Miejscowość**: z `miejscowosc`; brak klucza = puste pole „…………………” do wpisania.
- **Sygnatura**: `sygnatura_akt` / `sygnatura` / `sygn` (pierwszy znaleziony)
  — etykieta w nagłówku strony zawsze brzmi "sygn." (bez wariantów). Brak
  wszystkich trzech kluczy = normalna sytuacja (pismo bez przydzielonej
  sygnatury), brak nagłówka, bez błędu.
- **Data**: `data` / `data_dokumentu` / `data_pisma` (pierwszy znaleziony),
  wartość BEZ przyrostka "r." — szablon dopisuje go sam.
- **Tytuł pisma**: `pismo_tytul` / `tytul` / `dokument` / `typ_dokumentu` /
  `rodzaj_dokumentu` / `pismo` (pierwszy znaleziony), wyśrodkowany, 14pt,
  automatyczne WERSALIKI. Nagłówek `#` (H1) w treści markdown jest
  **całkowicie ignorowany** — nie renderuje się wcale (usuwany już na
  poziomie markdown przez `pismo-procesowe_pre.py`, więc pandoc nigdy nie
  widzi z niego `\section`). Tytuł pochodzi wyłącznie z frontmatteru.
- **Nadśródsekcje `##`/`###`**: WERSALIKI, bez pogrubienia, bez numeracji,
  bez rozróżnienia poziomu (oba poziomy renderują się identycznie).
- **Nadawca** (`nadawca_nazwa`, `nadawca_adres` lista, `nadawca_rola`):
  jeśli `nadawca_nazwa` brak albo jest pusty, szablon wstawia puste pola
  „……………” (nazwa + 2 linie adresu) do wpisania - bez niczyich danych domyślnych.
- **Odbiorca**: JEDEN klucz `odbiorca` — string lub lista stringów. Każdy
  string to nazwa+adres rozdzielone przecinkami (pierwszy segment = nazwa,
  kolejne = kolejne linie adresu). Brak klucza = poprawnie (np. oświadczenie
  bez konkretnego adresata) — bez błędu/ostrzeżenia. Lista z >1 elementem:
  pierwszy = odbiorca główny, reszta pod nagłówkiem "Do wiadomości:".
  Parsowanie robi `templates/pismo-procesowe_pre.py` (pandoc nie ma języka
  do dzielenia stringów po przecinku) — patrz sekcja "Mechanizm
  preprocessingu" niżej.
- **Załączniki** (`zalaczniki`, lista): bez pogrubienia, 9pt.
- `bez_numeracji_stron`: `true` wyłącza numerację stron (domyślnie włączona).
- `skladajacy`: imię i nazwisko pod tekstem (blok podpisu, wspólne z
  `oswiadczenie.latex`).

Pola spoza tej listy (np. `uwagi`) są niewidoczne w PDF — tak samo jak
w `oswiadczenie.latex`.

Przykład wywołania:

```bash
python <skille>/pdf-generation/generate_pdf.py work/pisma/odpowiedz-na-pozew.md --template pismo-procesowe
```

### Mechanizm preprocessingu (`<template>_pre.py`)

`generate_pdf.py` sprawdza przed wywołaniem pandoca, czy obok szablonu
istnieje plik `templates/<nazwa>_pre.py` z funkcją `preprocess(input_path:
Path) -> Path`. Jeśli tak — wywołuje ją, a wynikową ścieżkę (może być
tymczasowy plik z rozszerzonym frontmatterem, jak w przypadku `odbiorca`)
używa zamiast oryginału do wywołania pandoca; plik tymczasowy jest sprzątany
po kompilacji. Oryginalny `.md` nigdy nie jest modyfikowany. Brak
`<nazwa>_pre.py` dla danego szablonu = zero zmiany zachowania (np.
`oswiadczenie.latex` nie ma swojego `_pre.py` i działa jak dotychczas).
Używaj tego mechanizmu tylko dla logiki, której **nie da się** wyrazić w
języku szablonów pandoc (`$if$`/`$for$`/dostęp kropkowy) — czyli w praktyce
tylko do manipulacji stringami (np. dzielenie po przecinku).

## Dodawanie nowego szablonu

Nowy typ dokumentu (np. pismo procesowe inne niż oświadczenie) — dodaj
`templates/<nazwa>.latex` obok istniejącego jako punkt odniesienia. Zachowaj:
- `\providecommand{\tightlist}{...}` — bez tego pandoc wywala się na listach,
- `fontspec` + `polyglossia` z `\setdefaultlanguage{polish}` dla polskich znaków,
- font o pełnym pokryciu Unicode dla symboli typu ≥/≤/— (przetestowano Times New
  Roman z Windows — nie każdy font ma te glify, sprawdzaj ostrzeżenia
  "Missing character" w stderr pandoca po zmianie fontu).

## Znane zastrzeżenia

- Jeśli terminal działa z podniesionymi uprawnieniami (Administrator), MiKTeX
  drukuje ostrzeżenia "security risk: running with elevated privileges" na
  stderr — to nieszkodliwe dla samego renderowania, ale MiKTeX odradza pracę
  jako admin. Nie wymaga akcji ze strony tego skilla.
- PDF generowany tym narzędziem **nie jest jeszcze dowodem** — dopiero podpisanie
  go kwalifikowanym podpisem elektronicznym lub podpisem zaufanym ePUAP nadaje mu
  status oświadczenia. Przypominaj o tym po każdym wygenerowaniu.
