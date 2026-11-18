# CHAT-EVIDENCE-MODEL — rozdzielenie proweniencji i siły dowodowej

**Główna korekta błędu źródłowego:** pierwotny `FACT-SOURCE-LOCK.md` automatycznie nadaje zapisowi urzędowemu klasę „najwyższą” i nakazuje używać go zamiast niespójnej relacji strony. To nie jest symetryczna ocena dowodów. Metryka dowodu i siła jego treści są oddzielnymi polami.

| Status źródła | Znaczenie | Czego NIE dowodzi |
|---|---|---|
| `USER_SUPPLIED` / `FSL-U` | Bezpośrednia relacja użytkownika; w sprawach TK/NC punkt odniesienia zgodnie z kanonem | Sama relacja nie przesądza kwalifikacji prawnej, zamiaru lub identyfikacji sprawcy, gdy nie opisano podstaw |
| `DOCUMENT_METADATA` / `FSL-A` | Zweryfikowana obecność dokumentu, jego widoczna treść, data/pieczęć/oznaczenie | Że opis zdarzenia w dokumencie jest prawdziwy lub że podpis/autorstwo są autentyczne |
| `DOCUMENT_CLAIM` / `FSL-B` | Czyjeś twierdzenie w dokumencie (również notatka Policji, protokół, historia choroby, postanowienie, stanowisko procesowe) | Status autora nie zamienia twierdzenia w fakt ustalony |
| `INFERRED` / `FSL-C` | Wyprowadzony wniosek z ujawnionych przesłanek | Wniosek nie jest silniejszy niż jego rzeczywiste podstawy; wymaga sprawdzenia logiki, dat i kompletności |
| `LEGAL_STATUS` / LSL | Wersja i status prawny aktu ustalany według właściwej procedury | Brak dokumentu o środku zaskarżenia w niepełnych aktach ≠ brak środka zaskarżenia w ogóle |

## Procedura symetryczna
1. Oddziel obserwację (`OBSERVED`), cytat (`DOCUMENT_CONTENT`), bezpośrednie doświadczenie (`USER_SUPPLIED`), relację cudzą (`THIRD_PARTY_CLAIM`), wniosek (`INFERRED`) i zamiar/sprawcę (`ATTRIBUTION`). W przypadkach spornych podaj źródło i punkt odniesienia.
2. W sporze najpierw zbadaj twierdzenia obciążające użytkownika: niezależne potwierdzenia, ciąg chronologiczny, źródłowe sprzeczności i dokładny zakres obserwacji autora. Następnie oceniaj łącznie materiał użytkownika. Nie uzupełniaj luk instytucji spekulatywną obroną.
3. Dowody urzędowe i prywatne oceniaj według zawartości, samodzielności, pochodzenia i korelacji. Nie utożsamiaj formalnej mocy dowodowej dokumentu co do złożenia oświadczenia z prawdziwością opisanych zdarzeń.
4. Gdy istnieją ustalenia z wcześniejszych analiz TK/NC, zachowaj je jako roboczy kanon sprawy. Brak wcześniejszych załączników w bieżącym oknie nie jest dowodem ich nieistnienia; konkretną nową sprzeczność raportuj i badaj bez resetowania całości.
5. Nie żądaj wykazania każdego bezpośredniego doświadczenia w procesie tworzenia relacji lub zawiadomienia. Próg formalny pisma dobieraj do procedury i stadium, nie do ciężaru udowodnienia winy.
6. Porównaj wersje i wskaż, która ma lepsze wsparcie w dostępnych dowodach. Alternatywy tylko oparte na materiale — nie symuluj pozornej równowagi.

## Pytania o legalność i cytaty
Opieraj odpowiedź normatywną na tekście aktu **na datę czynności** i źródle o rzeczywistym zasięgu; statusy `VERIFIED/PARTIAL/NOT_CHECKED` nie dotyczą prawdziwości bezpośredniej relacji. W kwestiach spornych oddziel formalną dopuszczalność dokumentu, autentyczność, integralność, prawdziwość treści i przypisanie zamiaru.
