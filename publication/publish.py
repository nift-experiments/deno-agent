"""Complete publication ownership: assets, exports, redirects and sitemap."""
from pathlib import Path
import json
import shutil
import time


def publish(root, model):
    started=time.perf_counter()
    owned=[]
    def copy(source,target):
        dst=root/'public'/target
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dst)
        owned.append(target)
    for p in sorted((root/'assets').rglob('*')):
        if p.is_file():copy(p,p.relative_to(root/'assets').as_posix())
    if model=='deno':
        for family in ['runtime','deploy','sandbox','subhosting','examples','lint/rules']:
            for p in sorted((root/'authored'/family).rglob('*.md')):
                rel=p.relative_to(root/'authored').as_posix()
                if any(part.startswith('_')for part in Path(rel).parts):continue
                copy(p,rel)
        for p in (root/'.generated/search').glob('*.json'):copy(p,p.name)
        for p in (root/'.generated/llms').glob('*'):copy(p,p.name)
    else:
        for p in (root/'exports').rglob('*.md'):copy(p,p.relative_to(root/'exports').as_posix())
        for p in (root/'data/publication').glob('*'):copy(p,p.name)
    copy(root/'data/redirects.json','_redirects.json')
    api=root/'.generated/api-redirects.json'if model=='deno'else root/'data/api-redirects.json'
    copy(api,'api/_redirects.json')
    dates=json.loads((root/'data/sitemap-dates.json').read_text())
    routes=json.loads((root/'data/routes.json').read_text())
    urls=sorted(p.get('url',p.get('route'))for p in routes)
    sitemap_urls=[url for url in urls if url!='/404/']
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for url in sitemap_urls:
        xml+='  <url>\n    <loc>https://docs.deno.com'+url+'</loc>\n    <lastmod>'+dates.get(url,'2026-10-07T00:00:00.000Z')+'</lastmod>\n  </url>\n'
    xml+='</urlset>'
    (root/'public/sitemap.xml').write_text(xml);owned.append('sitemap.xml')
    for url in urls:owned.append(url.lstrip('/')+'index.png')
    ledger=root/'.generated/publication-owned.json'
    old=json.loads(ledger.read_text())if ledger.exists()else['assets/css/style.css','assets/js/script.js']
    owned=sorted(set(owned))
    for stale in set(old)-set(owned):(root/'public'/stale).unlink(missing_ok=True)
    ledger.write_text(json.dumps(owned,indent=2)+'\n')
    return {'publication_s':time.perf_counter()-started,'non_html_outputs':len(owned)}
