---
name: patron-pismo-procesowe-pl
description: Projekt polskiego pisma procesowego lub administracyjnego (pozew, odpowiedź na pozew, apelacja, zażalenie, skarga do WSA, odwołanie od decyzji, wniosek, wezwanie do zapłaty) oraz edycja istniejącego pisma lub umowy z zachowaniem numeracji i odesłań. Użyj, gdy użytkownik prosi o napisanie, przeredagowanie albo poprawienie pisma lub umowy po polsku.
---

> **Pliki przebiegu (reguła kanoniczna):** zapisuj według `shared/MOD-PLIKI-INKREMENTALNE.md` - nowym plikiem jest
> tylko wersja wynikowa (`drafty/<pismo>/rrrrMMdd_<nazwa>_vN.*`); logi, raporty, ustalenia i recapy przebiegu
> dopisuj do istniejących plików inkrementalnych (`_PRZEBIEGI.md`, `_SUBSUMPCJA*.md`, `_FINDINGS.md` …), a pliki
> jednorazowe zostawiaj w `_robocze/` sprawy.

# Pismo procesowe PL - projekt do podpisu prawnika

## Zanim zaczniesz
Ustal z dokumentów sprawy albo pytając: sąd lub organ, sygnaturę (jeśli nadana), strony
z adresami, wartość przedmiotu sporu, żądanie, fakty z dowodami, podstawę prawną, terminy.
Braków nie zgaduj - wstaw widoczny znacznik `[DO UZUPEŁNIENIA: ...]`.

## Pismo procesowe (sprawy cywilne i karne, sądy powszechne)
- Nagłówek: oznaczenie sądu, sygnatura akt (jeśli nadana), strony (powód/pozwany albo
  oskarżyciel/oskarżony) z adresami.
- Tytuł pisma (POZEW, ODPOWIEDŹ NA POZEW, APELACJA, SKARGA KASACYJNA, WNIOSEK O ...).
- Wartość przedmiotu sporu (gdy wymagana, w pozwie cywilnym).
- Treść: wnioski (żądania) numerowane I, II, III; uzasadnienie z faktami i podstawą prawną
  w odrębnych akapitach.
- Załączniki - lista numerowana.
- Miejsce, data (DD.MM.RRRR), podpis.

## Skarga do WSA
- Nagłówek: WSA w X za pośrednictwem organu, którego decyzję się skarży.
- Strony: skarżący i organ.
- Tytuł: SKARGA na decyzję ... z dnia ... znak ...
- Żądanie: uchylenie decyzji w całości lub w części, zwrot kosztów.
- Zarzuty (numerowane) i uzasadnienie każdego zarzutu.
- Wniosek o wstrzymanie wykonania (gdy istotne).

## Odwołanie od decyzji administracyjnej (k.p.a. art. 127-141)
- Do organu wyższego stopnia za pośrednictwem organu I instancji.
- Termin: 14 dni od doręczenia (chyba że ustawa szczególna stanowi inaczej).
- Nie wymaga uzasadnienia, ale wskazanie zarzutów wzmacnia odwołanie.

## Nie myl pojęć
- „Odwołanie” - do organu wyższego stopnia w postępowaniu administracyjnym. „Skarga” - do WSA
  na decyzję (po wyczerpaniu odwołania) albo bezpośrednio w wybranych sprawach.
- „Pozew” inicjuje proces cywilny. „Wniosek” inicjuje postępowanie nieprocesowe albo jest
  pismem incydentalnym.
- „Wyrok” rozstrzyga co do istoty. „Postanowienie” - kwestie wpadkowe lub odrzucenie pisma.
  „Nakaz zapłaty” - postępowanie upominawcze lub nakazowe.
- „Apelacja” - od wyroku I instancji do II instancji. „Skarga kasacyjna” - od wyroku II instancji
  do SN (cywilne, karne) albo do NSA (administracyjne).
- „Zażalenie” - na postanowienie w sprawach incydentalnych.

## Cytowanie prawa
- Akt: pełna nazwa + (Dz.U. ROK poz. NUMER) przy pierwszym przywołaniu, dalej skrót
  („art. 6 ust. 1 lit. f RODO”, „art. 415 k.c.”).
- Orzeczenie: sygnatura + data + sąd („wyrok NSA z 12.05.2026 r., III OSK 1377/23”).
- Przepisy i orzeczenia sprawdzaj w konektorach (skill `patron-prawo-pl-zrodla`), nie z pamięci.
- Daty w treści pisma: DD.MM.RRRR r. (12.05.2026 r.), nie 2026-05-12.

## Formuły
- Sąd: „Wysoki Sądzie” w wystąpieniu, „Wysoki Sąd” w piśmie („Wysoki Sąd uzna za zasadne...”).
- Organ administracji: „Szanowny Organie”, „Szanowna Pani Wojewodo / Szanowny Panie Wojewodo”.
- Strony: „powód”, „pozwany”, „oskarżony”, „obrońca” - nie imiona bez kontekstu.
- Zakończenie: „Mając na uwadze powyższe, wnoszę jak na wstępie” albo „Z powyższych względów
  wnoszę o uwzględnienie skargi w całości”.

## Zasada projektu
NIGDY nie podpisuj się za prawnika. Na końcu pisma zawsze:
„[Podpis - imię, nazwisko, tytuł zawodowy, nr wpisu na listę adwokatów/radców prawnych]”.
Nie wstawiaj wymyślonych nazwisk.

## Plik Word
Zapisz projekt jako Markdown (`<nazwa>.md`); jeśli jest `pandoc`, konwertuj:
`pandoc pismo.md -o pismo.docx`. Struktura (reguły generatora DOCX Patrona):
- Nagłówki bez przeskoków poziomów (H1 → H2 → H3).
- Numeracja zawsze od 1, nigdy od 0; nie dopisuj numeru do tekstu nagłówka.
- Nie powtarzaj tytułu dokumentu jako pierwszego nagłówka.
- Umowa: komparycja i preambuła („zważywszy, że...”) bez numeracji; numeracja od pierwszego
  postanowienia operacyjnego; blok podpisów na końcu, na osobnej stronie, bez numeracji.

## Edycja istniejącego pisma lub umowy
- Każde dodanie, usunięcie lub przestawienie numerowanego paragrafu, ustępu, punktu
  czy załącznika przesuwa dalszą numerację. W tej samej zmianie popraw kolejne numery
  ORAZ wszystkie odesłania do nich („zgodnie z § 5 ust. 2”, „o którym mowa w pkt 3”,
  „Załącznik nr 3”), także w definicjach i załącznikach.
- Przed zmianą przeszukaj cały dokument pod kątem odesłań (np. `grep -n "§ 5"`); nie zakładaj,
  że są tylko obok miejsca zmiany. W razie wątpliwości, czy odesłanie dotyczy przesuniętego
  numeru - popraw i zaznacz to w podsumowaniu.
- Usuwając nawiasy kwadratowe, usuń oba: `[` i `]`.
- Uwagi bez zmiany brzmienia („rozważ, czy zapis nie jest abuzywny”, „brak klauzuli
  poufności”) zapisuj jako komentarze z krótkim cytatem fragmentu, a nie jako przeróbkę tekstu.
- `.docx`: `pandoc umowa.docx -o umowa.md`, edycja, `pandoc umowa.md -o umowa-v2.docx`
  (formatowanie może się uprościć - uprzedź o tym użytkownika).

## Po napisaniu
- Podaj krótko: co to za pismo, jego strukturę i z których dokumentów korzystałeś.
- Zaproponuj skill `patron-obrona-pisma` (recenzja, kontrargumenty, styl) i `patron-weryfikacja-cytatow`
  dla cytatów z akt.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/chat/prompts.ts`
(DRAFTING_PL, DOCX GENERATION, DOCUMENT EDITING, DOCUMENT REVIEW).
