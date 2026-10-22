#!/usr/bin/env python3
"""Generuje _log/selekcja.md z selection/selection.yaml."""
import os, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = yaml.safe_load(open(os.path.join(ROOT, "selection/selection.yaml"), encoding="utf-8"))
k = d["keep"]
folded = [x for x in k if x.get("fold_into")]
vis = [x for x in k if not x.get("internal") and not x.get("fold_into")]
inn = [x for x in k if x.get("internal") and not x.get("fold_into")]
L = ["# Selekcja skilli - grounding-prawo", "",
     "Własna analiza (14.10.2026) z korektami właściciela. Analizy GPT i Sonnet były doradcami.", "",
     f"- w pluginie: **{len(k) - len(folded)}** skilli: **{len(vis)}** widocznych dla modelu i **{len(inn)}** pomocniczych (również dostępnych dla modelu),",
     f"- **{len(folded)}** skilli scalonych jako moduły typów pism w `pisma-procesowe-v3`,",
     f"- poza pluginem: **{len(d['drop'])}**, w tym {sum(1 for x in d['drop'] if x.get('archive'))} unikatów w `archive/` (płasko).", "",
     "## Zasady", "",
     "1. Jeden router (`prawny-router-v3`), bez bramek kosztu; pełna ścieżka kontroli zawsze.",
     "2. Silnik LexMachina zostaje spójny (`shared` odwołuje się do `audyt-systemu-v4` 33 razy). Moduły dziedzinowe poza profilem (DR-04/06/07/08/09/15) usunięte, a martwe wiersze routingu wycinane przez `scripts/build.py`.",
     "3. Brak anonimizacji, pseudonimizacji i zakazu chmury: KROK 0A zamknięty patchem, odwołania do `let-it-be` i `tajemnica-preflight` wycinane w buildzie.",
     "4. Źródła prawa: jeden konektor, portal MCP `lex.xlap.pl/mcp`. Skille cache i wrappery SAOS usunięte.",
     "5. Zmiany względem upstreamu to patche (`selection/patches/`) i reguły `build.py`; upstream zostaje przypięty w submodułach.", "",
     "## Plugin", "", "| Skill | Źródło | Rola | Uzasadnienie |", "|---|---|---|---|"]
for x in k:
    rola = "moduł w pisma-procesowe-v3" if x.get("fold_into") else ("wewnętrzny" if x.get("internal") else "widoczny")
    if x.get("transitional"): rola += ", przejściowy"
    L.append(f"| `{x['name']}` | {x['from']} | {rola} | {x['why']} |")
L += ["", "## Poza pluginem", "", "| Skill | Gdzie | Powód |", "|---|---|---|"]
for x in d["drop"]:
    L.append(f"| `{x['name']}` | {'archive/' if x.get('archive') else 'upstream'} | {x['why']} |")
L += ["", "## Znane problemy i rzeczy niezrobione", "",
      "- Po usunięciu skilli zostają odwołania w prozie (ok. 150 miejsc, głównie w `shared`, `analizator-umow-v1`, `citation-grounding-pl`); nie są to ścieżki wczytywane przez router, ale wymagają stopniowego sprzątania.",
      "- Patche routera zmieniają pliki objęte `CHECKSUMS.sha256`; sumy w skillu się nie zgadzają.",
      "- `ekstraktor-cytatow-pl` ma tylko SKILL.md, bez kodu: ekstrakcja idzie promptem.",
      "- Komentarze w `iura`-pochodnych skillach nadal wspominają `text_unavailable_use_pdf`.",
      "- `pisz-po-polsku`: pliki skopiowane z upstreamu, zmiany `humanizer-pl` i `naturalne-pisanie` trzeba przenosić ręcznie.",
      "- Upstream LexMachina jest na GPL v3; publiczny marketplace z przerobionymi skillami oznacza dystrybucję na GPL. Repo jest prywatne.",
      "- Nie sprawdzono, czy claude.ai i chatgpt.com przyjmują ten układ marketplace."]
open(os.path.join(ROOT, "_log/selekcja.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")