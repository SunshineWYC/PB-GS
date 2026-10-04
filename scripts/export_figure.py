"""Export a reviewed PDF crop or source image without changing the original."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('--pdf', type=Path)
source.add_argument('--image', type=Path)
parser.add_argument('--page', type=int, default=1, help='PDF page number, starting at 1')
parser.add_argument('--crop', nargs=4, type=float, default=[0, 0, 1, 1], metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'), help='Normalized crop coordinates from 0 to 1')
parser.add_argument('--name', required=True, help='Lowercase output name, without extension')
parser.add_argument('--kind', choices=['diagram', 'render'], default='diagram')
parser.add_argument('--dpi', type=int, default=300)
parser.add_argument('--preview-width', type=int, default=2000)
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.name): parser.error('Use a lowercase hyphenated name')
l, t, r, b = args.crop
if not (0 <= l < r <= 1 and 0 <= t < b <= 1): parser.error('Crop must satisfy 0 <= left < right <= 1 and 0 <= top < bottom <= 1')
if args.dpi <= 0 or args.preview_width <= 0: parser.error('DPI and preview width must be positive')
try:
    from PIL import Image
except ImportError: parser.exit(1, 'Pillow is required. See docs/ASSETS.md for optional export dependencies.\n')
path = (args.pdf or args.image).resolve()
if not path.is_relative_to((ROOT / 'materials').resolve()): parser.error('Place source files under materials/ before exporting')
digest = hashlib.sha256(path.read_bytes()).hexdigest()
if args.pdf:
    try: import pymupdf as fitz
    except ImportError: parser.exit(1, 'PyMuPDF is required for PDF export. See docs/ASSETS.md.\n')
    with fitz.open(path) as document:
        if not 1 <= args.page <= len(document): parser.error('PDF page is out of range')
        page = document[args.page - 1]; box = page.rect
        clip = fitz.Rect(box.x0 + l * box.width, box.y0 + t * box.height, box.x0 + r * box.width, box.y0 + b * box.height)
        pix = page.get_pixmap(matrix=fitz.Matrix(args.dpi / 72, args.dpi / 72), clip=clip, alpha=False, colorspace=fitz.csRGB)
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
else:
    with Image.open(path) as opened:
        image = opened.convert('RGB')
        image = image.crop((round(l * image.width), round(t * image.height), round(r * image.width), round(b * image.height)))
folder = ROOT / 'site/assets/images'; folder.mkdir(parents=True, exist_ok=True)
ext = '.png' if args.kind == 'diagram' else '.webp'
full = folder / (args.name + ext); preview = folder / (args.name + '-preview' + ext)
if not args.overwrite and (full.exists() or preview.exists()): parser.error('Output exists; inspect before using --overwrite')
options = {'optimize': True} if ext == '.png' else {'quality': 94, 'method': 6}
image.save(full, **options)
small = image.copy(); small.thumbnail((args.preview_width, args.preview_width)); small.save(preview, **options)
assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, 'Source unexpectedly changed'
notes = ROOT / 'notes'; notes.mkdir(exist_ok=True)
record_path = notes / 'exports.json'
records = json.loads(record_path.read_text(encoding='utf-8')) if record_path.exists() else {}
records[args.name] = {'source': path.relative_to(ROOT).as_posix(), 'sha256': digest, 'page': args.page if args.pdf else None, 'crop': args.crop, 'fullSize': image.size, 'previewSize': small.size}
record_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
manifest_path = ROOT / 'site/assets/manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
paths = [p.relative_to(ROOT / 'site').as_posix() for p in (full, preview)]
manifest['assets'] = [e for e in manifest['assets'] if e['path'] not in paths]
manifest['assets'].extend({'path': p, 'role': args.kind, 'public_approved': False} for p in paths)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print('Exported ' + ', '.join(paths) + '. Review pixels and public-use status before release.')
