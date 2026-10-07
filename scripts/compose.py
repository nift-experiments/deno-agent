"""Raw composition with explicit dependencies and an owned-output retirement ledger."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def changed(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def emit(path):
    return '@dep(' + json.dumps(path) + ')$[rawHtml(' + json.dumps(path) + ')]'


def compose(model):
    tracked, owned = [], []
    for page in model:
        name = page['route'].strip('/') + '/index'
        wrapper = ''.join('@dep(' + json.dumps(p) + ')' for p in page['dependencies'])
        wrapper += ''.join(emit(page[k]) for k in ('prefix', 'body', 'suffix'))
        changed('.generated/content/' + name + '.html', wrapper)
        tracked.append({'name': name, 'title': page['title'], 'template': 'templates/template.html'})
        owned.append('public/' + name + '.html')
    changed('.nift/tracked.json', json.dumps({'tracked': tracked}, indent=2) + '\n')
    ledger = ROOT / '.generated/owned.json'
    old = json.loads(ledger.read_text()) if ledger.exists() else []
    for stale in set(old) - set(owned):
        # Only retire files explicitly owned by this builder, never arbitrary assets.
        (ROOT / stale).unlink(missing_ok=True)
        (ROOT / (stale + '.info.json')).unlink(missing_ok=True)
    changed('.generated/owned.json', json.dumps(owned, indent=2) + '\n')
    if not (ROOT / 'templates/template.html').exists():
        changed('templates/template.html', '@script { fn(rawHtml(path)) { f := file(path); f.open(); value := f.read_all(); f.close(); return value; } }@content')
    subprocess.run(['nift', 'build'], cwd=ROOT, check=True)


def split(html):
    start = html.index('<main ')
    stop = html.index('</main>', start) + len('</main>')
    return html[:start], html[start:stop], html[stop:]


def agent():
    model = json.loads((ROOT / 'data/routes.json').read_text())
    for row in model:
        row['dependencies'] = ['data/routes.json', 'scripts/compose.py']
    compose(model)

if __name__ == '__main__':
    agent()
