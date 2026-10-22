# MOD-TEKST-JEDNOLITY — dojście do obowiązującego brzmienia przepisu

> Moduł wspólny (GROUNDING-PRAWO, 2026-09-13, plan integracji P4; przepisany 2026-10-22: źródła ustawy + Repertorium).
> Czytaj przed każdym dosłownym cytatem przepisu. Źródła: MCP `ustawy` (37 aktów z komentarzem, portal
> `lex.xlap.pl/mcp`) i MCP Repertorium (`repertorium_szukaj_repertorium`, pola `tekst_jednolity`, `eli`).

## Źródła i ich zakres
- **`ustawy`** (`ustawy_artykul`, `ustawy_cytat`, `ustawy_szukaj`, `ustawy_akty`): dosłowne brzmienie artykułu
  z zindeksowanego tekstu jednolitego wskazanego w polach `tekst_jednolity` i `eli`, plus komentarz. Zakres: 37 aktów
  z `ustawy_akty`. Poza zakresem nie zwraca nic, co można cytować.
- **Repertorium** (`repertorium_szukaj_repertorium`): wyszukuje akt, jego ELI i tekst jednolity. Służy do
  ustalenia identyfikatora aktu i sprawdzenia nowelizacji, nie do odczytu brzmienia.
- **Urzędowe ELI** (`api.sejm.gov.pl`, dziennik-ustaw ELI, odczyt PDF tam, gdzie tekst jest tylko w PDF):
  jedyny dowód, że brzmienie jest aktualne. Obowiązkowe przy każdym dosłownym cytacie.

## Procedura (kolejność wiążąca)
1. **Ustal akt i identyfikator:** `ustawy_akty` (skróty, ELI, tekst jednolity). Akt spoza 37 → Repertorium
   (`repertorium_szukaj_repertorium`), żeby wziąć ELI aktualnego tekstu jednolitego.
2. **Odczytaj brzmienie:** `ustawy_artykul(akt, art)`; dosłowność sprawdź przez `ustawy_cytat(akt, art, fragment)`.
   Podaj `tekst_jednolity` i ELI z odpowiedzi.
3. **Sprawdź nowelizacje po dacie tekstu jednolitego:** w urzędowym ELI aktu (`api.sejm.gov.pl`) lub przez
   Repertorium. Jeśli po dacie t.j. była nowelizacja zmieniająca przepis, nie cytuj brzmienia z `ustawy`
   bez odczytu nowszego tekstu jednolitego z ELI.
4. **Brak potwierdzenia:** gdy akt jest poza `ustawy`, Repertorium nie zwraca ELI albo ELI nie daje tekstu
   obowiązującego, przyznaj to wprost: „brzmienie niezweryfikowane”. Nie zgaduj i nie podstawiaj aktu bazowego
   ani wersji pierwotnej jako obowiązującej.

## Pułapka: obowiązujący tekst jednolity kodeksu bywa tylko w PDF
Sprawdzone 11.09.2026: dla KC, KPC, KPK i KP obowiązujący tekst jednolity może nie mieć wersji HTML. Wtedy
`ustawy` i Repertorium podają ELI, a brzmienie czytasz z PDF pod tym ELI (natywny `Read` z `pages`, potem
WebFetch). Konkretnych ELI nie cytuj z pamięci, wylistuj je na bieżąco.

Cytat dosłowny sprawdź wzrokowo w PDF: ekstrakcja gubi pojedyncze spacje, a artykuły z indeksem górnym
wychodzą jako `Art. 205[1]`. Podawaj je jako `205¹` lub `205^1` (zgodnie z `ustawy_artykul`).

## Co wolno cytować
- Cytowalne jako obowiązujące: brzmienie z `ustawy_artykul` potwierdzone krokiem 3 (ELI, data odczytu w śladzie
  weryfikacji) albo brzmienie z PDF urzędowego tekstu jednolitego pod tym ELI.
- Starszy tekst jednolity: tylko z adnotacją daty tego t.j. i informacją, że późniejsze nowelizacje nie są
  uwzględnione.
- Wersja pierwotna (`tekst_ogloszony`): wyłącznie materiał historyczny, z adnotacją.

> W piśmie procesowym, w którym brzmienie przepisu jest sporne, potrzebny jest odczyt z urzędowego ELI.
> Samo `ustawy_artykul` nie wystarcza.
