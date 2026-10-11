---
status: ERROR
query_type: akt_prawny
source: isap
tool: isap.text
query: "{\"eli\": \"DU/2025/1814\", \"find\": \"124\"}"
identyfikator: DU/2025/1814
tytul: "tresc tylko w PDF - HTML niedostepny"
status_obowiazywania: nieznany
data: ""
url: "https://api.sejm.gov.pl/eli/acts/DU/2025/1814/text.html"
retrieved_at: "2026-10-03T23:56:36Z"
expires_at: "2026-10-04T23:56:36Z"
ttl_days: 1
confidence: deterministic
pii_risk: low
cache_key: cfaafd12e83a5b87
error_code: text_unavailable_use_pdf
eli: DU/2025/1814
pdf_url: "https://api.sejm.gov.pl/eli/acts/DU/2025/1814/text.pdf"
uwaga: "uzyj `isap pdf <ELI> --find \"Art. N.\"` - wyciagnie tresc wprost z PDF obowiazujacego tekstu jednolitego"
---
```json
{
  "_error": "text_unavailable_use_pdf",
  "ELI": "DU/2025/1814",
  "http": 200,
  "pdf": "https://api.sejm.gov.pl/eli/acts/DU/2025/1814/text.pdf",
  "alternatywy": [],
  "wskazowka": "sprobuj kolejnego tekstu jednolitego z listy - pierwszy z wersja HTML zwroci tresc (bedzie NIEAKTUALNY, podaj date)"
}
```
