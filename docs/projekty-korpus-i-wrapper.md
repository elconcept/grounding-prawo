# Korpus orzeczeń, wrapper MCP i korpus prawa (projekt, 14.10.2026)

Stan zmierzony, propozycje do akceptacji. Nic z tego nie zostało wdrożone.

## 1. Orzeczenia z cache, których nie ma w SAOS

Zmierzone: `mcp/cache/orzeczenia/` ma 54 ręcznie wyselekcjonowane orzeczenia (frontmatter: `source`, `sygnatura`, `data`, `confidence: reczna_kuracja`).
Lokalny dump SAOS (`/workspace/docker/mcp-saos/data/saos.sqlite`) ma 543 536 orzeczeń.

| Źródło w cache | Plików | W dumpie SAOS (dopasowanie po sygnaturze) |
|---|---|---|
| `saos` (SN, SA Warszawa) | 46 | 16 jest, **30 brak** |
| `echr` (ETPCz) | 6 | nigdy nie były w SAOS |
| `cbosa` (NSA/WSA) | 2 | nigdy nie były w SAOS |

Razem 38 spoza dumpu. Ty podajesz 34; różnica to pewnie dopasowanie sygnatur (zapis „III CZP 66/16" vs w dumpie) i wymaga ręcznego przejrzenia listy.
Część braków to orzeczenia z lat 2025 (II CSKP 1048/24, V KK 331/24): dump może być po prostu starszy niż data wydania, i wtedy inkrementalna synchronizacja je dociągnie sama.

**Propozycja (zgodna z Twoją sugestią, że baza SAOS ma zostać wierna dumpowi):** osobny magazyn `orzeczenia_uzupelniajace`, plik SQLite obok `saos.sqlite`, nigdy w tej samej bazie.
- Schemat: `zrodlo` (reczny/echr/cbosa/playwright), `sad`, `sygnatura`, `data`, `ecli`, `tresc`, `url`, `pobrano`, `weryfikacja`.
- Ingest z istniejących plików `.md` (frontmatter już jest) jednym skryptem; dopisywanie nowych przez Playwright (orzeczenia.ms.gov.pl, sn.pl, TK) zastępuje skill `webwright-legal-pl`.
- Wyszukiwanie obejmuje oba magazyny; wynik zawsze niesie pole `zrodlo`, więc widać, co pochodzi z dumpu, a co z kuracji.
- Zadanie uzgadniające: po każdej synchronizacji SAOS usuwa z magazynu uzupełniającego wpisy, które pojawiły się już w dumpie (klucz: sygnatura + data).
- Do `mcp-saos` warto przenieść jedyną wartość skilla `szukaj-orzeczen-v2`: statystyki zbioru wyników (sądy, powoływane przepisy, sędziowie) jako narzędzie `saos_stats`. To zmiana w Twoim kodzie `mcp-saos`, więc czeka na Twoją zgodę (propozycja, nie diff).

## 2. Wrapper MCP (inspiracja: prawo-pl-mcp)

`prawo-pl-mcp` ma dobry wzorzec: 4 narzędzia zamiast 42 (`pl_list_sources`, `pl_search`, `pl_get_document`, `pl_call`), jedna konwencja parametrów (`page` od 1, `date_from`/`date_to`), paginacja długich dokumentów po ok. 5000 znaków.
Ale on uruchamia konektory przez `npx`/`uvx`, a Twoje stoją już w Dockerze za portalem. Różnice:
- zamiast spawnowania wywołuje istniejące serwery po sieci Dockera (sieci `cf_<nazwa>`), więc nic nie instaluje;
- dodaje źródło `uzupelniajace` z punktu 1 oraz źródło `prawo` (korpus z punktu 3);
- ujednolica paginację i nazwy parametrów (to, co Ci poprawiano osobno w każdym MCP, robi raz w jednym miejscu).
Pytanie otwarte: czy portal Cloudflare `lex.xlap.pl/mcp` już agreguje na tym poziomie, czy tylko proxuje. Jeśli tylko proxuje, wrapper stoi za portalem jako kolejny serwer.

## 3. Korpus prawa (git-as-law) w Basic Memory

Zmierzone: `/projects/legal/vendor` ma 106 repozytoriów `Komentar-PL-*`, 1011 plików `.md`, 92 MB. Format: plik na rozdział, w środku `### Art. N`, `**Brzmienie przepisu:**` w cytacie i komentarz.
Basic Memory ma semantyczne wyszukiwanie zawsze włączone (CHANGELOG #1696, indeks wektorowy z chunkowaniem), więc osobne embeddingi nie są potrzebne.

**Propozycja:** osobny projekt Basic Memory `prawo`, notatka = jeden plik rozdziału (1011 notatek, bez cięcia na artykuły; chunkowanie robi indeks wektorowy).
- Frontmatter dodany skryptem: `akt`, `eli`/`dz_u`, `art_od`, `art_do`, `rodzaj: komentarz`, `repo`, `commit`.
- Linków między projektami nie ma, więc `legal` powołuje się na przepis tekstem (akt + artykuł), nie linkiem; nic się nie psuje.
- Pilotaż najpierw: KC, KPK, KK, KPC, UoOZP. Zmierzyć czas synchronizacji i jakość wyszukiwania (czy zapytanie o „art. 192 kk zgoda pacjenta" zwraca właściwy rozdział), dopiero potem reszta.
- Źródło prawdy o brzmieniu obowiązującym nadal wymaga ISAP (komentarze mają datę): korpus służy do komentarza i szukania, a przy cytowaniu przepisu obowiązuje bramka aktualności routera.

## Decyzje do podjęcia
1. Czy zatwierdzasz osobny magazyn `orzeczenia_uzupelniajace` obok `saos.sqlite` (zamiast wciągania ich do SAOS).
2. Czy wolno dodać `saos_stats` do `mcp-saos`.
3. Czy wrapper ma stać za portalem, czy portal jest już agregatorem.
4. Czy zaczynam pilotaż projektu `prawo` od 5 kodeksów.
