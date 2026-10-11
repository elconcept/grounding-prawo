---
status: ERROR
query_type: akt_prawny
source: isap
tool: isap.text
query: "{\"eli\": \"DU/2025/734\", \"find\": \"Art. 6.\"}"
identyfikator: DU/2025/734
tytul: "tresc tylko w PDF - HTML niedostepny"
status_obowiazywania: nieznany
data: ""
url: "https://api.sejm.gov.pl/eli/acts/DU/2025/734/text.html"
retrieved_at: "2026-10-03T23:56:05Z"
expires_at: "2026-10-04T23:56:05Z"
ttl_days: 1
confidence: deterministic
pii_risk: low
cache_key: ed5debd5ae041bd9
error_code: text_unavailable_use_pdf
eli: DU/2025/734
pdf_url: "https://api.sejm.gov.pl/eli/acts/DU/2025/734/text.pdf"
uwaga: "uzyj `isap pdf <ELI> --find \"Art. N.\"` - wyciagnie tresc wprost z PDF obowiazujacego tekstu jednolitego"
teksty_jednolite: [DU/2025/734, DU/2023/2119, DU/2022/2151, DU/2021/281, DU/2021/2008, DU/2019/821, DU/2018/618, DU/2015/1094, DU/2013/482, DU/2010/275]
---
```json
{
  "_error": "text_unavailable_use_pdf",
  "ELI": "DU/2025/734",
  "http": 200,
  "pdf": "https://api.sejm.gov.pl/eli/acts/DU/2025/734/text.pdf",
  "alternatywy": [
    "DU/2025/734",
    "DU/2023/2119",
    "DU/2022/2151",
    "DU/2021/281",
    "DU/2021/2008",
    "DU/2019/821",
    "DU/2018/618",
    "DU/2015/1094",
    "DU/2013/482",
    "DU/2010/275"
  ],
  "wskazowka": "sprobuj kolejnego tekstu jednolitego z listy - pierwszy z wersja HTML zwroci tresc (bedzie NIEAKTUALNY, podaj date)"
}
```
