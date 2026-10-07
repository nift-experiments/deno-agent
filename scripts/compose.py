"""Raw composition with explicit dependencies and an owned-output retirement ledger."""
from pathlib import Path
import hashlib
import json
import subprocess
from measure import run_phase
import html
import re

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
        tracked.append({'name': name, 'title': page['title'] or '', 'template': 'templates/template.html'})
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
    phase = run_phase('nift', ['nift', 'build'], cwd=ROOT)
    changed('.generated/nift-metrics.json', json.dumps(phase, indent=2) + '\n')


def split(html):
    start = html.index('<main ')
    stop = html.index('</main>', start) + len('</main>')
    return html[:start], html[start:stop], html[stop:]


def agent():
    model = json.loads((ROOT / 'data/routes.json').read_text())
    for row in model:
        row['dependencies'] = ['data/routes.json', 'scripts/compose.py']
        prefix = (ROOT / row['prefix']).read_text()
        body = (ROOT / row['body']).read_text()
        suffix = (ROOT / row['suffix']).read_text()
        if row.get('projection_body_sha256') != hashlib.sha256(body.encode()).hexdigest():
            raise ValueError('Maintained HTML changed without an acknowledged projection update: ' + row['route'] + '. Update its download/search/LLM sources and projection_body_sha256 together.')
        if 'navigation' in row:
            prefix = prefix.replace('<!--deno:main-navigation-->', (ROOT / row['navigation']).read_text())
            row['dependencies'].append(row['navigation'])
        original = row.get('original_title', row['title'])
        if row['title'] != original:
            title = html.escape(row['title'] or '')
            prefix = re.sub(r'<title>.*?</title>', '<title>' + title + ' | Deno Docs</title>', prefix)
            prefix = re.sub(r'(<meta (?:name|property)="(?:twitter:title|og:title)" content=")[^"]*', lambda m: m[1] + title, prefix)
            def breadcrumb(match):
                data = json.loads(match[1])
                data['itemListElement'][-1]['name'] = row['title']
                return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>'
            prefix = re.sub(r'<script type="application/ld\+json">(.*?)</script>', breadcrumb, prefix)
            body = re.sub(r'(<h1\b[^>]*>).*?(</h1>)', lambda m: m[1] + title + m[2], body, count=1, flags=re.S)
        old_route = row.get('original_route', row['route'])
        if row['route'] != old_route:
            # Only bind this page's head URLs; navigation links remain authored.
            head, separator, shell = prefix.partition('</head>')
            head = head.replace(old_route + '"', row['route'] + '"')
            head = head.replace(old_route + 'index.png', row['route'] + 'index.png')
            prefix = head + separator + shell
        old_download = row.get('original_download', row.get('download'))
        if old_download and row.get('download') != old_download:
            # Source download/edit links are separate from the canonical route.
            prefix = prefix.replace('/' + old_download, '/' + row['download'])
            body = body.replace('/' + old_download, '/' + row['download'])
        for key, value in [('prefix', prefix), ('body', body), ('suffix', suffix)]:
            source = row[key]
            row['dependencies'].append(source)
            target = '.generated/bound/' + row['route'].strip('/') + '/' + key + '.html'
            changed(target, value)
            row[key] = target
    compose(model)

if __name__ == '__main__':
    agent()
