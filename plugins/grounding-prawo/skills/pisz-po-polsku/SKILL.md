---
name: pisz-po-polsku
description: "Pisanie i redakcja tekstów po polsku tak, by brzmiały naturalnie, konkretnie i bez manier generycznego stylu AI, z zachowaniem faktów, cytatów, przepisów, sygnatur i stopnia pewności. Używaj przy redakcji pism, notatek, relacji i opisów po polsku oraz gdy tekst brzmi sztucznie. Łączy minimalną ingerencję (naturalne-pisanie), katalog 36 wzorców AI-slop z bramką wierności po przepisaniu (humanizer-pl) i zasady z Patrona (pisz-po-ludzku). Nie zmienia petitum, zarzutów ani ustaleń faktycznych."
---

# Pisz po polsku

Jeden skill redakcji polskiego tekstu. Zastępuje `humanizer-pl`, `patron-pisz-po-ludzku` i `naturalne-pisanie`.
Poprawia sposób wypowiedzi, nigdy treść stanowiska.

## Zasada nadrzędna: minimalna potrzebna ingerencja

Najpierw wykonaj polecenie użytkownika. Potem poprawiaj tylko to, co realnie pogarsza tekst.
Zachowuj trafne, charakterystyczne sformułowania autora. Fragment naturalny i precyzyjny zostaw bez zmian;
brak zmiany jest prawidłowym wynikiem redakcji. Nie obiecuj niewykrywalności dla detektorów AI.

## Reguły twarde (zawsze)

- Zachowaj bez zmian: daty, kwoty, numery przepisów, sygnatury, cytaty, nazwy własne, terminologię prawną.
- Zachowaj siłę twierdzeń: nie osłabiaj kategorycznego sformułowania i nie wzmacniaj ostrożnego.
- Nie wymyślaj faktów, cytatów, źródeł, danych ani doświadczeń autora.
- Nie humanizuj przez celowe błędy, literówki ani przypadkowe kolokwializmy.
- Nie zastępuj naturalnego słowa rzadszym synonimem dla pozornej różnorodności.
- Nie ruszaj petitum, zarzutów, wniosków dowodowych ani ustaleń faktycznych w piśmie. Redagujesz uzasadnienie i opis, nie stanowisko.

## Tryby

| Tryb | Kiedy | Co robisz |
|---|---|---|
| Redakcja | użytkownik daje tekst | rozpoznaj, co warto zachować; popraw tylko realne wady; zwróć wersję i krótką listę zmian, jeśli o nią poprosi |
| Pisanie od zera | użytkownik daje materiał | najpierw treść i kolejność, potem szlif; `references/naturalny-styl.md` |
| Pismo prawnicze | pismo procesowe, uzasadnienie, relacja | `references/tekst-prawniczy.md`; formuły procesowe („wnoszę o", „powód") zostają, to nie slop |
| Relacja pokrzywdzonego | zawiadomienie o przestępstwie | formuły procesowe są tu wadą; rządzi `zawiadomienie-o-przestepstwie` (references/styl.md) |

## Kolejność pracy

1. Rozpoznaj gatunek, odbiorcę i rejestr; to wyznacza, co jest wadą.
2. Przeczytaj tekst i zaznacz, co zostaje.
3. Przejdź `references/katalog-wzorcow-humanizer.md` (36 wzorców: inflacja znaczenia, slop-słownictwo PL, imiesłowy pozornej głębi,
   reguła trójki, negatywne paralelizmy, strona bierna ukrywająca sprawcę, kalki z angielskiego, wypełniacze, artefakty czatbota,
   monotonny rytm, typografia PL). Pojedynczy sygnał (myślnik, „kluczowy", lista trzech) to nie wada; reaguj na skupiska i niedopasowanie do gatunku.
4. Polszczyznę sprawdzaj wg `references/polszczyzna.md` (reforma pisowni 2026, interpunkcja, cudzysłowy „…", łącznik zamiast pauzy).
5. **Bramka po przepisaniu** (obowiązkowa dla pism): `python3 scripts/audyt_po_przepisaniu.py <przed> <po>` sprawdza, czy nie zginęły
   daty, kwoty, przepisy, sygnatury, cytaty i siła twierdzeń. Wynik FAIL lub NEEDS_REVIEW = popraw przepisanie, nie bramkę.
6. Po redakcji pisma wraca kontrola merytoryczna (cytaty, subsumpcja); redakcja nie zwalnia z niej.

## Pliki

| Plik | Kiedy |
|---|---|
| `references/naturalny-styl.md`, `references/polszczyzna.md`, `references/polszczyzna-przyklady.md` | pisanie od zera, wątpliwości językowe |
| `references/tekst-prawniczy.md` | teksty prawnicze |
| `references/katalog-wzorcow-humanizer.md` | redakcja: lista kontrolna wzorców |
| `references/skrot-patron.md` | krótka wersja zasad do szybkiej redakcji |
| `scripts/audyt_po_przepisaniu.py`, `tests/` | bramka wierności po przepisaniu |

Pochodzenie: humanizer-pl (MIT, MateMatic), naturalne-pisanie (elconcept), pisz-po-ludzku (Patron, AGPL-3.0). Zob. pliki NOTICE-*.
