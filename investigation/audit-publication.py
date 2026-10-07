"""Read-only frozen publication audit. Usage: python audit-publication.py SITE OUT."""
import collections
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urljoin, urlsplit, unquote


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = collections.Counter()
        self.links = []
        self.meta = []
        self.canonical = []
        self.headings = []
        self.jsonld = []
        self.title = ''
        self.active = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids[a['id']] += 1
        for attr in ('href', 'src'):
            if a.get(attr):
                self.links.append({'tag': tag, 'attribute': attr, 'value': a[attr]})
        if tag == 'meta':
            self.meta.append(a)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href'))
        if tag == 'title' or tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.active = {'tag': tag, 'id': a.get('id'), 'text': ''}
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.active = {'tag': 'jsonld', 'text': ''}

    def handle_data(self, text):
        if self.active:
            self.active['text'] += text

    def handle_endtag(self, tag):
        if self.active and (tag == self.active['tag'] or tag == 'script' and self.active['tag'] == 'jsonld'):
            r = self.active
            if tag == 'title':
                self.title = r['text']
            elif tag == 'script':
                self.jsonld.append(json.loads(r['text']))
            else:
                self.headings.append(r)
            self.active = None


def audit(root):
    files = {p.relative_to(root).as_posix(): p for p in root.rglob('*') if p.is_file()}
    pages = {}
    for name, path in sorted(files.items()):
        if name.endswith('/index.html'):
            pages['/' + name.removesuffix('index.html')] = Page(path.read_text())
    redirects = {}
    for name in ('_redirects.json', 'api/_redirects.json'):
        if name in files:
            redirects.update(json.loads(files[name].read_text()))
    rows, missing, fragments = [], [], []
    for route, p in pages.items():
        rows.append({'route': route, 'title': p.title, 'canonical': p.canonical,
                     'metadata': p.meta, 'structured_data': p.jsonld, 'headings': p.headings,
                     'ids': dict(p.ids), 'duplicate_ids': {k: v for k, v in p.ids.items() if v > 1}})
        for link in p.links:
            target = urlsplit(urljoin('https://docs.deno.com' + route, link['value']))
            if target.netloc != 'docs.deno.com' or target.scheme not in ('http', 'https'):
                continue
            path = unquote(target.path)
            dest = path.rstrip('/') + '/'
            exists = path.lstrip('/') in files or dest in pages or path in redirects or dest in redirects or path in ('/', '/health', '/llms.txt')
            record = {'route': route, **link, 'target': path, 'fragment': target.fragment}
            if not exists:
                missing.append(record)
            elif target.fragment and dest in pages and target.fragment not in pages[dest].ids and unquote(target.fragment) not in pages[dest].ids:
                fragments.append(record)
    return {'html_routes': len(pages), 'publication_files': len(files),
            'publication_bytes': sum(p.stat().st_size for p in files.values()),
            'note': 'Potential unresolved local links are an inherited baseline ledger, not an automatic parity failure. Wildcard/runtime routing may resolve entries. Both literal and decoded fragments are accepted.',
            'pages': rows, 'potential_unresolved_local_links': missing,
            'potential_unresolved_fragments': fragments}


if __name__ == '__main__':
    result = audit(Path(sys.argv[1]))
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('pages', 'potential_unresolved_local_links', 'potential_unresolved_fragments')}))
    print('duplicate-ID routes:', sum(bool(p['duplicate_ids']) for p in result['pages']))
    print('potential unresolved paths/fragments:', len(result['potential_unresolved_local_links']), len(result['potential_unresolved_fragments']))
