# CHAT-RUNTIME — kontrakt host-neutralny dla biblioteki `shared`

## Zasada zakresu
Adapter nie zmienia zdefiniowanych przez LexMachina funkcji `prawny-router-v3` i `prawo-polskie-v2`, nie tworzy nowego routera ani nie zastępuje merytorycznych kryteriów walidacji. Przekształca polecenia zależne od środowiska w realne działania lub raport `NOT_CHECKED`.

### Resolver plików
- Pierwszeństwo ma wspólna, kompletna kopia `skills/shared/` z **tego samego bundla/release**. Historyczne `view shared/X` odnosi się do `skills/shared/X`; istniejące `shared/references/...` oznacza pliki tej kopii. W CHAT odczyt przez `skills__read` lub dostępną funkcję hosta; nie wnioskuj o instalacji wyłącznie z nazwy katalogu.
- Nie wybieraj źródła według najwyższej wersji z przypadkowego katalogu `~/.claude` czy `/mnt/skills`, jeżeli ten bundle zawiera kanoniczne `shared`; dołączonego `shared` nie łącz ze starszą wersją innej wtyczki.
- Odczyt obowiązkowego pliku wewnętrznego ma nastąpić realnie. Jeśli brak pliku, zgłoś brak i jego wpływ na wynik. Brak zasobu zewnętrznego **nie unieważnia automatycznie** możliwej analizy częściowej.

### Operacje
| Operacja historyczna | Wykonanie w CHAT |
|---|---|
| `view` / `Read` | Faktyczny odczyt określonego pliku / treści; brak odczytu ≠ przeczytano |
| `web_search`, `web_fetch`, `MCP`, Repertorium | Wybierz faktycznie dostępny kanał oficjalnego źródła, zapisz jego identyfikator i datę; brak kanału → `NOT_CHECKED` |
| `Basic Memory`, `model-memory`, `main`, `legal` | Integracja opcjonalna, wyłącznie po dostępnej autoryzacji i z ustalonym projektem; brak automatycznego zapisu lub udawanych recapów |
| Python/Node/Bash, `check_*`, `lens_runner.py`, subagent, Playwright | Wykonuj wyłącznie dostępne rzeczywiste narzędzie; opis testu nie dowodzi jego uruchomienia |
| `create_file`, DOCX/PDF, redline | Faktyczne wytworzenie zgodnego artefaktu albo jasna informacja o ograniczeniu; nie twórz fikcyjnej ścieżki |
| `show_widget`, `present_files` | Opcjonalna wizualizacja, nigdy warunek legalności wyniku |

### Stany i prowadzenie sprawy
- `SOURCE_VERIFIED`: odczytano właściwe źródło i konkretne brzmienie na określoną datę;
  `PARTIAL`: wykonano tylko część wymaganej kontroli; `NOT_CHECKED`: brak kontroli; `USER_SUPPLIED`: fakt z relacji użytkownika; `DOCUMENT_CLAIM`: twierdzenie zawarte w dokumentach; `INFERRED`: wniosek analityczny (podaj przesłanki).
- Nie awansuj `NOT_CHECKED` do `VERIFIED` na podstawie pamięci modelu, historycznego logu, zrzutu lub samej metryki. Brak dostępu do cytatu prawnego nie oznacza, że relacja użytkownika jest nieprawdziwa.
- Dla TK/NC obowiązuje kanon sprawy; nie resetuj ustaleń na podstawie niedostępności wcześniejszych plików. Zastrzeżenia i kontrargumenty stosuj symetrycznie, bez wymyślania nowych wersji przeciwnika.
- Tworzenie pisma: ocena według **typu** (zawiadomienie, zażalenie, pozew, apelacja itd.). Ciężar dowodu wyroku skazującego nie jest testem dopuszczalności zawiadomienia. Źródłowy wyjątek `ZAWIADOMIENIE-NARRATIVE-FIRST.md` obowiązuje, gdy właściwy.

### Prywatność
Nie deklaruj `pii-egress: none` dla sesji cloud wyłącznie dlatego, że skrypt lokalny nie wykonuje żądań HTTP. Każde wyjście do zewnętrznej usługi wymaga identyfikacji usługi, zakresu danych i uprawnienia. Nazwy endpointów w archiwum są **dokumentacją**, nie autoryzacją do wysłania akt.

### Integracja i zgodność
Nie zmieniaj macierzy wyboru skilli routera w `shared`. Poza scope są niezaadaptowane legacy skille i usługi; brak wymaganego routera albo modułu dziedzinowego należy zgłosić, nie zastępować wymyślonym narzędziem. Stany `PASS/FAIL/NOT_CHECKED` odnoszą się tylko do kontroli faktycznie wykonanych.
