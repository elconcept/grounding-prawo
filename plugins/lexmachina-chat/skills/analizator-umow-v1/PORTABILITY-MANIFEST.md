# Portability — analizator-umow-v1, ChatGPT CHAT, etap 5/8

- Oryginalny dokument: `references/upstream/PORTABILITY-MANIFEST.md`, zachowany byte-for-byte.
- Pochodzenie i notice: `NOTICE`; GPL-3.0 w źródłowym repozytorium LexMachina oraz atrybucje Apache-2.0 wskazane w plikach pochodnych; `modules/klauzule-kontraktowe-pl/LICENSE` oryginalny bez zmian.
- Oryginalny `SKILL.md`: `SKILL.upstream.md`, do audytu; aktywny profil CHAT poprzedza nienaruszony korpus `# Skill: Analizator Umów ...`.
- `shared`: wyłącznie kanoniczny sibling skill, bez powielania folderu; oryginalne SELECTOR G/H/I/K, DOMAIN J, J0, MA, workflow i A–F niezmienione.
- Source `CHECKSUMS.sha256` historyczny znajduje się w `references/upstream/CHECKSUMS.sha256`; aktywny checksum odzwierciedla aktualne bajty pakietu.
- Oryginalna tabela routingu [1]–[11] należy do `prawny-router-v3`, a nie do analizatora umów.
- Poprzednie fragmenty dotyczące Repertorium, Basic Memory, `present_files`, konsoli i natychmiastowej dostępności są historyczne, nie gwarantują realnej usługi w CHAT; oznacz `NOT_CHECKED/NOT_RUN`.
- Przypadki benchmarkowe są fixtures, nie tekstem umowy klienta ani poleceniami wykonania.
