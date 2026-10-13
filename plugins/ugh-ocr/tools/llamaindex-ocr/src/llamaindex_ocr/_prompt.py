"""Domyslny prompt parsera LlamaCloud.

Nastawiony na wierna transkrypcje polskich dokumentow prawno-medycznych --
rozroznianie druku/odreki, pieczeci, podpisow, checkboxow i niepewnosci OCR,
z zachowaniem struktury tabel. Frontmatter NIE jest czescia promptu -- jest
budowany deterministycznie w Pythonie (patrz _frontmatter.py), tak samo jak
w markitdown-vision. Prosic model o wygenerowanie poprawnego YAML w markdown
byloby zawodne (formatowanie, cudzyslowy, znaki specjalne) -- ekstrakcja
tekstu i metadanych to dwa oddzielne zadania.

Wersja 3 (2026-09-06): v2 dodala regule "adnotacje w nawiasach kwadratowych",
umieszczona w srodku promptu -- model nadal pisal np. "logo: laptopshop.pl"
bez nawiasow na prawdziwym dokumencie (przetestowano na
RYD.EM9_2026-06-05_0819_Tomasz_Kaczmarczyk.ocr.pdf). v3: regula przeniesiona
na sam poczatek promptu (LLM-y silniej trzymaja sie instrukcji na poczatku/
koncu niz w srodku), z negatywnym przykladem dokladnie tego wzorca, i
powtorzona jeszcze raz na koncu jako przypomnienie.
"""

DEFAULT_CUSTOM_PROMPT = """CRITICAL FORMATTING RULE — read this first, apply to every line you write:

Verbatim text (printed or handwritten, exactly as it appears in the document) is transcribed directly, with NO brackets.
Anything that is YOUR OWN description of a visual element (not literal text you can read) MUST be wrapped in square brackets: `[typ]` or `[typ: opis]`. There is no third option — never write a bare "word: description" line to describe something visual. That reads as if it were real document content, which is exactly the ambiguity this rule exists to prevent.

WRONG (do not do this): logo: laptopshop.pl LAPTOPSHOP <info@laptopshop.pl>
RIGHT: [logo: napis "laptopshop.pl LAPTOPSHOP" z adresem info@laptopshop.pl]

Standard bracket types: `[logo: opis]`, `[pieczęć: opis]`, `[podpis]` or `[podpis: opis]`, `[checkbox pusty]`, `[checkbox zaznaczony]`, `[checkbox niepewny]`, `[przekreślone: co]`, `[nieczytelne]`, `[OCR niepewny]`, `[odręczne]` (prefix a handwritten line/paragraph once, not per word), `[rysunek/diagram: opis]`, `[kod kreskowy/QR: treść jeśli czytelna]`, `[znak wodny: opis]`, `[pole puste]`.

Document parsing and transcription:
- These are Polish legal-medical documents. Preserve document structure and visual hierarchy.
- Distinguish explicitly between printed system text, handwriting, stamps/seals, signatures, checkboxes, handwritten marks, logos/letterheads, and OCR uncertainty — using the bracket types above.
- Pay special attention to table structure: preserve rows, columns, headers, merged cells, field labels, empty cells, and the relationship between values and their labels.
- Do not flatten tables into ordinary prose unless explicitly asked. If a table is partially unreadable, preserve its structure and mark uncertain cells with `[OCR niepewny]`.
- Pay special attention to checkbox state. Do not infer checkbox state from surrounding text — if the visual mark is unclear, use `[checkbox niepewny]` rather than treating it as checked or empty.
- Do not merge visually separate fields or documents into one continuous narrative.
- Preserve original wording, spelling, dates, times, names, units, dosages, lab values, abbreviations, and line/field relationships as far as possible.
- Do not infer missing text from context unless clearly marked as interpretation.
- Do not output a YAML frontmatter block, a title, or any blank lines before the first real line of document content — start directly with the transcription. Frontmatter is added separately by the calling tool.

REMINDER: every visual-element description goes in `[brackets]`, no exceptions, even for logos, letterheads, and email signature images.
"""
