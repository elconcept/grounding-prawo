# ROUTING-BJ-BW — Ubezpieczenia Społeczne, Niepełnosprawność, Sądownictwo, Zawody Zaufania

> Plik wydzielony z prawny-router-v3/SKILL.md (R1).
> Wczytaj gdy: problem użytkownika pasuje do jednej z kategorii poniżej.
> Wywołanie: `view prawny-router-v3/references/ROUTING-BJ-BW.md`

---

## TABELA ROUTINGU

| Problem użytkownika | Moduł obowiązkowy |
|---|---|
| opinia biegłego, zarzuty do opinii, inny biegły, instytut | `dr-12-sadownictwo-prokuratura-zawody-prawnicze/modules/mod-KPC-biegli-sadowi-opinie.md` |
| ustrój sądów, skarga na sąd, przewlekłość, wyłączenie sędziego, organizacja sądu | `dr-01-ustroj-konstytucyjny-i-zrodla-prawa/modules/mod-USP-ustroj-sadow-powszechnych.md`; przewlekłość/dostęp → także `dr-05-prawo-administracyjne-sadowoadministracyjne/modules/mod-ustawa-skargi-przewleklosc-dostep-sadu.md` |
| ORA, OIRP, adwokat, radca, notariusz, komornik, lekarz, zawód zaufania | DR-12: `mod-ustawa-adwokatura.md` / `mod-ustawa-radcowie-prawni.md` / `mod-ustawa-notariat.md` / `mod-ustawa-komornicy-sadowi-zawod.md`; lekarz → `dr-10-zdrowie-farmacja-zywnosc-rolnictwo/modules/mod-ustawa-zawod-lekarza.md` |
| postępowanie dyscyplinarne zawodowe lub służbowe | zawody: `dr-12-sadownictwo-prokuratura-zawody-prawnicze/modules/mod-ustawa-odpowiedzialnosc-dyscyplinarna-zawodow.md`; służby: właściwy moduł konkretnej służby w DR-13 |
| prokuratura, policja, czynności organów ścigania, skargi służbowe | prokuratura → `dr-12-sadownictwo-prokuratura-zawody-prawnicze/modules/mod-PrProkuratura-organy-ochrony-prawa.md`; Policja → `dr-13-sluzby-bezpieczenstwo-informacje-niejawne/modules/mod-ustawa-policja.md` |
| komisje lekarskie, dokumentacja medyczna, RPP, orzecznictwo medyczne | `dr-10-zdrowie-farmacja-zywnosc-rolnictwo/modules/mod-ustawa-prawa-pacjenta-framework.md` + `mod-rzecznik-praw-pacjenta-RPP.md`; właściwy moduł zawodu/świadczenia według sprawy |
| edukacja specjalna, PPP, uczelnia, dostosowania dla niepełnosprawności | `dr-10-zdrowie-farmacja-zywnosc-rolnictwo/modules/mod-ustawa-edukacja-specjalna-dostepnosc.md` |
| służby mundurowe, dyscyplinarka, uposażenie, orzeczenia komisji | `dr-13-sluzby-bezpieczenstwo-informacje-niejawne/SKILL.md` → obowiązkowo właściwy istniejący moduł danej służby (Policja/SG/PSP/ABW-AW/CBA/SKW-SWW/ŻW/obrona) |
| koszty sądowe, wynagrodzenie biegłych, pomoc prawna, opłaty zawodowe | `dr-12-sadownictwo-prokuratura-zawody-prawnicze/modules/mod-KSCU-koszty-sadowe-i-pomoc-prawna.md` |
| przewlekłość, dostępność sądu, racjonalne dostosowanie, prawo do sądu | `dr-05-prawo-administracyjne-sadowoadministracyjne/modules/mod-ustawa-skargi-przewleklosc-dostep-sadu.md` + `dr-01-ustroj-konstytucyjny-i-zrodla-prawa/modules/mod-USP-ustroj-sadow-powszechnych.md` |

Ścieżki bazowe modułów: konkretne katalogi `modules/` właściwych DR-01–DR-16 wskazane w tabeli powyżej. Nie istnieje wspólny katalog modułów materialnych pod `prawo-polskie-v2`; używaj bezpośrednio katalogu `modules/` właściwego DR.

---

## MODUŁY SHARED — OBOWIĄZKOWE PRZY SPRAWACH BJ–BW

Dołącz odpowiednio do typu sprawy:

```text
view prawny-router-v3/references/SOCIAL-SECURITY-LAW-STANDARD.md        (ZUS, KRUS, renty)
view shared/DISABILITY-FUNCTIONAL-ASSESSMENT.md    (niepełnosprawność, PFRON)
view shared/EXPERT-OPINION-AUDIT.md                (biegli, opinie)
view prawny-router-v3/references/DISCIPLINARY-PROCEEDINGS-STANDARD.md   (dyscyplinarki zawodowe)
view prawny-router-v3/references/JUDICIARY-LEGAL-STANDARD.md            (ustrój sądów, zawody zaufania)
```

---

## DELEGACJA DO ROUTERÓW DZIEDZINOWYCH

Dla prawa polskiego router używa najpierw:
- `prawo-polskie-v2/ROUTING-MAP.md`
- `DR-01–DR-16`

Nie kieruj spraw bezpośrednio do pojedynczych modułów `prawo-polskie-v2`,
jeżeli istnieje właściwy router dziedzinowy DR-01–DR-16.

---

## DODATKOWE ROUTINGI V4

| Frazy / sprawa | Moduł |
|---|---|
| odwołanie od decyzji, ponaglenie, WSA | `dr-05-prawo-administracyjne-sadowoadministracyjne/modules/mod-KPA-postepowanie-administracyjne.md` + właściwy `mod-PPSA-*`; pismo → `pisma-procesowe-v3/modules/MOD-ADMIN.md` |
| UOKiK, klauzule, platforma | `dr-02-prawo-cywilne-rodzinne-gospodarcze/modules/mod-ustawa-UOKIK-antymonopolowe.md` + `mod-ustawa-prawa-konsumenta.md`; platforma → `dr-11-cyfrowe-cyber-ai-dane-ip/modules/mod-DSA-digital-services-act.md` |
| NIS2, UKE, DSA, incydent cyber | `dr-11-cyfrowe-cyber-ai-dane-ip/modules/mod-KSC-NIS2-cyberbezpieczenstwo-telekom.md`; dane osobowe → `mod-RODO-GDPR-2016-679.md`; przestępstwo → `dr-03-prawo-karne-wykroczenia-egzekucja/modules/mod-KK-art267-269c-cyberprzestepstwa.md` + `mod-KK-KPK-framework-karne.md` |
| upadłość, restrukturyzacja, syndyk | `dr-02-prawo-cywilne-rodzinne-gospodarcze/modules/mod-PrUpad-upadlosc-restrukturyzacja.md` + właściwy `mod-PrRestr-*`; zawód syndyka → `mod-ustawa-doradca-restrukturyzacyjny-zawod.md` |
