"""Complete publication ownership: assets, exports, redirects and sitemap."""
from pathlib import Path
import json
import shutil
import time


def publish(root, model):
    started=time.perf_counter()
    owned=[]
    copy_categories={name:0 for name in ['static_assets','og_assets','markdown_downloads','redirects','search','llms']}
    copy_s=0
    copied_bytes=0
    def copy(source,target):
        nonlocal copy_s,copied_bytes
        copy_start=time.perf_counter()
        dst=root/'public'/target
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dst)
        owned.append(target)
        copied_bytes+=source.stat().st_size
        elapsed=time.perf_counter()-copy_start
        copy_s+=elapsed
        relative=source.relative_to(root).as_posix()
        category='og_assets' if relative.startswith('assets/og/') else 'markdown_downloads' if source.suffix=='.md' else 'redirects' if 'redirects.json' in source.name else 'search' if 'orama-index' in source.name else 'llms' if source.name.startswith('llms') else 'static_assets'
        copy_categories[category]+=elapsed
    for p in sorted((root/'assets').rglob('*')):
        if p.is_file() and 'og' not in p.relative_to(root/'assets').parts:copy(p,p.relative_to(root/'assets').as_posix())
    if model=='deno':
        for family in ['runtime','deploy','sandbox','subhosting','examples','lint/rules']:
            for p in sorted((root/'authored'/family).rglob('*.md')):
                rel=p.relative_to(root/'authored').as_posix()
                if any(part.startswith('_')for part in Path(rel).parts):continue
                copy(p,rel)
        for p in (root/'.generated/search').glob('*.json'):copy(p,p.name)
        for p in (root/'.generated/llms').glob('*'):copy(p,p.name)
    else:
        route_rows=json.loads((root/'data/routes.json').read_text())
        declared={row['download'] for row in route_rows if 'download' in row}
        managed=set(json.loads((root/'data/download-ownership.json').read_text()))
        for p in (root/'exports').rglob('*.md'):
            relative=p.relative_to(root/'exports').as_posix()
            if relative in managed and relative not in declared:continue
            copy(p,relative)
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
    images=json.loads((root/'data/og-assets.json').read_text())
    images_by_route={image['route']:image for image in images}
    for url in urls:
        if url not in images_by_route:raise ValueError('Route has no maintained OG asset: '+url+'. Run the explicit OG maintenance workflow before publication.')
        image=images_by_route[url]
        copy(root/image['source'],image['output'])
    ledger=root/'.generated/publication-owned.json'
    old=json.loads(ledger.read_text())if ledger.exists()else['assets/css/style.css','assets/js/script.js']
    owned=sorted(set(owned))
    for stale in set(old)-set(owned):(root/'public'/stale).unlink(missing_ok=True)
    ledger.write_text(json.dumps(owned,indent=2)+'\n')
    return {'publication_s':time.perf_counter()-started,'non_html_outputs':len(owned),'copy_subset_s':copy_s,'copy_categories_subset_s':copy_categories,'copied_bytes':copied_bytes,'content_negotiation_generation_s':0,'content_negotiation_model':'maintained runtime middleware; copied Markdown download artifacts'}
