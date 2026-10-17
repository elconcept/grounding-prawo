#!/usr/bin/env python3
"""File conversion with a single cloud OCR path and doc-intel output contract."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'document_contract/scripts'))
sys.path.insert(0, str(BASE / 'tools/the-ocr/src'))
from contract import Block, build_contract, validate

VERSION = '0.3.0'
# the-ocr names; azure-di and google-vision stay accepted as aliases
PROVIDERS = ('datalab', 'llamaparse', 'azure', 'google_vision', 'rapidocr', 'azure-di', 'google-vision')
TEXT = {'.txt', '.md', '.csv', '.json', '.xml', '.log', '.yaml', '.yml'}
IMAGES = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.webp'}
OFFICE = {'.docx', '.xlsx', '.pptx', '.html', '.htm', '.rtf', '.epub'}


def from_ocr(document):
    document.validate()
    aliases = {'heading': 'title', 'text': 'paragraph', 'photo': 'figure', 'graphic': 'figure',
               'logo': 'figure', 'handnote': 'paragraph'}
    blocks = []
    for page in document.pages:
        for b in page.blocks:
            confidence = b.confidence
            if confidence is not None and (not math.isfinite(confidence) or not 0 <= confidence <= 1):
                raise ValueError(f'Invalid confidence for {b.id}')
            flags = []
            if b.bbox is None: flags.append('partial')
            if confidence is None: flags.append('confidence_unknown')
            blocks.append(Block(b.id, page.number, list(b.bbox) if b.bbox else None,
                                aliases.get(b.block_type, b.block_type), b.text, confidence, flags))
    return blocks


def cloud_ocr(path, provider):
    from the_ocr.config import all_providers, default_providers
    from the_ocr.chain import run_chain
    result = run_chain(path, all_providers() if provider else default_providers(), force=provider)
    if not result.ok:
        raise RuntimeError('; '.join(f'{a.provider}: {a.outcome}: {a.reason}' for a in result.attempts))
    return result.result.document


def extract(path, provider=None, force_ocr=False):
    import pymupdf
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        with pymupdf.open(path) as pdf:
            pages = len(pdf)
            texts = [p.get_text('text').strip() for p in pdf]
            # A scan with a small printed header still needs OCR. Mixed files use cloud OCR once.
            needs_ocr = force_ocr or any((not text) or (len(text) < 100 and p.get_images())
                                        for p, text in zip(pdf, texts))
            if not needs_ocr:
                blocks = []
                for n, page in enumerate(pdf, 1):
                    for b in page.get_text('blocks', sort=True):
                        if len(b) > 6 and b[6] != 0: continue
                        if not b[4].strip(): continue
                        rect = (pymupdf.Rect(b[:4]) * page.rotation_matrix) & page.rect
                        if rect.is_empty: continue
                        box = [rect.x0/page.rect.width, rect.y0/page.rect.height,
                               rect.x1/page.rect.width, rect.y1/page.rect.height]
                        blocks.append(Block(f'p{n:04d}-b{len(blocks)+1:04d}', n, box,
                                            'paragraph', b[4].strip(), None, ['native_text', 'confidence_unknown']))
                return blocks, 'pymupdf', pages, None
        doc = cloud_ocr(path, provider)
        return from_ocr(doc), doc.provider, len(doc.pages), doc
    if suffix in IMAGES:
        # Convert only the transport format; preserve source and page aspect ratio.
        with tempfile.TemporaryDirectory(prefix='document-read-') as tmp:
            pdf_path = Path(tmp)/'input.pdf'
            from PIL import Image, ImageSequence
            with Image.open(path) as image, pymupdf.open() as pdf:
                for frame in ImageSequence.Iterator(image):
                    import io
                    buf = io.BytesIO(); frame.convert('RGB').save(buf, format='PNG')
                    page = pdf.new_page(width=frame.width, height=frame.height)
                    page.insert_image(page.rect, stream=buf.getvalue())
                pdf.save(pdf_path)
            doc = cloud_ocr(pdf_path, provider)
        return from_ocr(doc), doc.provider, len(doc.pages), doc
    if suffix in TEXT:
        text = path.read_text(encoding='utf-8-sig')
        engine = 'text'
    elif suffix in OFFICE:
        from markitdown import MarkItDown
        text = MarkItDown(enable_plugins=False).convert(str(path)).text_content
        engine = 'markitdown'
    else:
        raise ValueError(f'Unsupported format: {suffix}; no silent OCR fallback')
    blocks = [Block('segment-0001', 1, None, 'paragraph', text, None,
                    ['no_physical_pagination', 'partial', 'confidence_unknown'])] if text.strip() else []
    return blocks, engine, None, None


def convert(path, output, provider=None, force_ocr=False, refresh=False):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    config = {'version': VERSION, 'provider': provider, 'ocr': force_ocr,
              'chain': os.getenv('THE_OCR_CHAIN', ''), 'suffix': path.suffix.lower()}
    key = hashlib.sha256((digest+json.dumps(config, sort_keys=True)).encode()).hexdigest()
    folder = output/key
    result_path = folder/'result.json'
    if result_path.exists() and not refresh:
        result = json.loads(result_path.read_text())
        if all((folder/n).is_file() for n in ['document.md','contract.json']):
            result.update(source=str(path), cached=True)
            return result
    blocks, engine, pages, doc = extract(path, provider, force_ocr)
    contract = build_contract(blocks, engine=engine, raw=raw, path=str(path), pages=pages)
    errors = validate(contract)
    if errors: raise ValueError('; '.join(errors))
    physical = pages is not None
    page_numbers = range(1, pages+1) if physical else [1]
    md_blocks = {b.id: b.markdown for page in doc.pages for b in page.blocks} if doc else {}
    markdown = '\n\n'.join((f'## Page {n}\n\n' if physical else '') +
                           '\n\n'.join(md_blocks.get(b.id, b.text) for b in blocks if b.page == n) for n in page_numbers)
    empty = [n for n in page_numbers if not any(b.text.strip() for b in blocks if b.page == n)]
    quality = {'empty_or_unreadable_pages': empty if physical else [],
               'review_required': contract['gating']['review_required'],
               'unlocated_blocks': contract['gating']['ungroundable']}
    if empty:
        contract['gating']['verdict'] = 'degraded' if blocks else 'failed'
        contract['gating']['note'] += '; empty pages require visual review'
    content = '\n'.join(b.text for b in blocks)
    normalized = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', content)).strip()
    result = {'source': str(path), 'sha256': digest, 'engine': engine, 'pages': pages,
              'markdown': str(folder/'document.md'), 'contract': str(folder/'contract.json'),
              'text_sha256': hashlib.sha256(normalized.encode()).hexdigest() if normalized else None,
              'status': contract['gating']['verdict'], 'quality': quality, 'cached': False}
    folder.mkdir(parents=True, exist_ok=True)
    # result.json is the completion marker; failed writes are never reusable.
    result_path.unlink(missing_ok=True)
    (folder/'document.md').write_text(markdown+'\n', encoding='utf-8')
    (folder/'contract.json').write_text(json.dumps(contract, ensure_ascii=False, indent=2)+'\n')
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    return result


def read_documents(source, output, provider=None, force_ocr=False, refresh=False):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.exists(): raise ValueError(f'No such input: {source}')
    if source == output or source.is_relative_to(output): raise ValueError('Output must not contain input')
    files = sorted(p for p in source.rglob('*') if p.is_file() and not p.is_relative_to(output)
                   and not any(part.startswith('.') or part in {'@eaDir','archive'} for part in p.relative_to(source).parts)) if source.is_dir() else [source]
    results = []
    for path in files:
        try: results.append(convert(path, output, provider, force_ocr, refresh))
        except Exception as exc:
            results.append({'source': str(path), 'status': 'failed', 'error': f'{type(exc).__name__}: {exc}'})
    duplicates = {}
    for label, field in [('identical_files','sha256'), ('same_text','text_sha256')]:
        groups = {}
        for item in results:
            if item.get(field): groups.setdefault(item[field], []).append(item['source'])
        duplicates[label] = [group for group in groups.values() if len(group)>1]
    manifest = {'version': VERSION, 'documents': results, 'duplicates': duplicates}
    output.mkdir(parents=True, exist_ok=True)
    (output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--provider', choices=PROVIDERS)
    parser.add_argument('--ocr', action='store_true')
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    try: result = read_documents(args.input,args.output,args.provider,args.ocr,args.refresh)
    except (OSError,ValueError) as exc: parser.exit(20, f'{exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    statuses = {r['status'] for r in result['documents']}
    return 20 if not statuses or 'failed' in statuses else 10 if 'degraded' in statuses else 0

if __name__ == '__main__':
    raise SystemExit(main())
