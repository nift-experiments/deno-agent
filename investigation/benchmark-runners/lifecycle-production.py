"""Complete publication lifecycle, using coordinated maintained-source transactions."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,time,re,math,sys
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'deno-baseline'
ENV={**os.environ,'DENO_BIN':str(BASE/'tools/deno'),'DENO_DIR':str(BASE/'cache')}
RESULT=[]
RESUMED={(row['model'],row['case']) for row in RESULT}
MARKER='D7-lifecycle-verified @content $[literal] {{literal}}'
def manifest(root):return {p.relative_to(root/'public').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(root/'public').rglob('*')if p.is_file()}
def statistics(docs):
 lengths=[len(x['content'].encode('utf-16-le'))//2 for x in docs]; categories={};sections={}
 for d in docs:
  categories[d['category']]=categories.get(d['category'],0)+1;k=d['category']+'/'+d['section'];sections[k]=sections.get(k,0)+1
 longest=max(range(len(docs)),key=lambda i:lengths[i]);shortest=min(range(len(docs)),key=lambda i:lengths[i])
 return dict(totalDocuments=len(docs),totalCharacters=sum(lengths),averageDocumentLength=math.floor(sum(lengths)/len(docs)+.5),categoryCounts=categories,sectionCounts=sections,documentsWithTags=sum(bool(d.get('tags'))for d in docs),documentsWithDescriptions=sum(bool(d.get('description'))for d in docs),longestDocument=f"{docs[longest]['title']} ({lengths[longest]:,} chars)",shortestDocument=f"{docs[shortest]['title']} ({lengths[shortest]} chars)",apiDocuments=sum(d['docType']=='api-reference'for d in docs),markdownDocuments=sum(d['docType']=='markdown'for d in docs))
def transaction(root):
 saved={}
 def write(rel,data):
  p=root/rel
  if rel not in saved:saved[rel]=p.read_bytes()if p.exists()else None
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data.encode()if isinstance(data,str)else data)
 def remove(rel):
  p=root/rel
  if rel not in saved:saved[rel]=p.read_bytes()if p.exists()else None
  p.unlink(missing_ok=True)
 def restore():
  for rel,data in saved.items():
   p=root/rel
   if data is None:p.unlink(missing_ok=True)
   else:p.write_bytes(data)
  saved.clear()
 return write,remove,restore

def projections(root,write,route,marker='',title=None,newroute=None,delete=False,add=False):
 """Authoring-side coordinated projection edits; never part of routine rendering."""
 folder=root/'data/publication';full=json.loads((folder/'orama-index-full.json').read_text());summary=json.loads((folder/'orama-index-summary.json').read_text());llms=json.loads((folder/'llms.json').read_text())
 match=lambda d:d['url'].rstrip('/')=='https://docs.deno.com'+route.rstrip('/')
 old=[d for d in full['data']if match(d)]
 if add:
  doc={'id':'d7-proof','title':title,'content':marker,'url':'https://docs.deno.com'+route,'path':route,'category':'runtime','section':'d7-proof','subsection':'index.md','description':'Lifecycle evidence','tags':[],'headings':[],'lastModified':1791384146884,'docType':'markdown'}
  full['data'].append(doc);summary['data'].append({k:v for k,v in doc.items()if k not in ['content','headings','lastModified']})
 else:
  for index in [full,summary]:
   if delete:index['data']=[d for d in index['data']if not match(d)]
   else:
    for d in index['data']:
     if not match(d):continue
     if 'content'in d and marker:d['content']+='\n\n'+marker
     if title is not None:
      if 'content'in d and d['content'].startswith(d['title']+'\n'):d['content']=title+d['content'][len(d['title']):]
      d['title']=title
     if newroute:d['url']='https://docs.deno.com'+newroute;d['path']=newroute
 for index in [full,summary]:index['metadata']['stats']=statistics(full['data']);index['metadata']['totalDocuments']=len(full['data'])
 llms['metadata']['orama']=summary['metadata'];llms['data']=summary['data']
 for name,data in [('orama-index-full.json',full),('orama-index-summary.json',summary),('llms.json',llms)]:write('data/publication/'+name,json.dumps(data,ensure_ascii=False,indent=2))
 text=(folder/'llms-full.txt').read_text();pattern=re.compile(r'^# [^\n]*\n\n(?:> [^\n]*\n\n)?URL: ([^\n]*)\n\n',re.M);matches=list(pattern.finditer(text));chunks=[]
 for i,m in enumerate(matches):
  end=matches[i+1].start()if i+1<len(matches)else len(text);chunk=text[m.start():end]
  if m[1].rstrip('/')=='https://docs.deno.com'+route.rstrip('/'):
   if delete:chunk=''
   else:
    if marker:chunk=chunk.replace('\n\n---\n\n','\n\n'+marker+'\n\n---\n\n',1)
    if title is not None:chunk=re.sub(r'^# [^\n]*', '# '+title,chunk,count=1)
    if newroute:chunk=chunk.replace(m[1],'https://docs.deno.com'+newroute)
  chunks.append(chunk)
 if matches:text=text[:matches[0].start()]+''.join(chunks)
 if add:text+=f'# {title}\n\n> Lifecycle evidence\n\nURL: https://docs.deno.com{route}\n\n{marker}\n\n---\n\n'
 write('data/publication/llms-full.txt',text)
 text=(folder/'llms-summary.txt').read_text();lines=[]
 for line in text.splitlines(keepends=True):
  m=re.search(r'\((https://docs\.deno\.com[^)]*)\)',line)
  if m and m[1].rstrip('/')=='https://docs.deno.com'+route.rstrip('/'):
   if delete:continue
   if title is not None:line=re.sub(r'^- \[[^]]*\]', '- ['+title+']',line)
   if newroute:line=line.replace(m[1],'https://docs.deno.com'+newroute)
  lines.append(line)
 if add:lines.append(f'\n- [{title}](https://docs.deno.com{route}): Lifecycle evidence\n')
 write('data/publication/llms-summary.txt',''.join(lines))
 return len(old)

def run(model,phase):
 dst=BASE/'probes'/f'{phase}-lifecycle-{model}'
 if dst.exists():raise RuntimeError('Refusing to replace existing lifecycle evidence: '+str(dst))
 shutil.copytree(ROOT/model,dst,ignore=shutil.ignore_patterns('.git','node_modules','__pycache__'))
 write,remove,restore=transaction(dst)
 def build(label,force=False):
  log=BASE/'logs'/f'{phase}-{model}-{label}.log';tfile=log.with_suffix('.time');start=time.perf_counter()
  with log.open('w')as f:
   subprocess.run(['/usr/bin/time','-v','-o',str(tfile),'python3','scripts/build.py',*(['--force'] if force else [])],cwd=dst,env=ENV,stdout=f,stderr=subprocess.STDOUT,check=True)
   if force:subprocess.run(['nift','build','--all'],cwd=dst,env=ENV,stdout=f,stderr=subprocess.STDOUT,check=True)
  return time.perf_counter()-start,json.loads((dst/'.generated/build-metrics.json').read_text()),int(re.search(r'Maximum resident set size \(kbytes\): (\d+)',tfile.read_text())[1])/1024
 def check(case,assertion):
  if (model,case) in RESUMED:return
  duration,metrics,rss=build(case);before=manifest(dst);assertion()
  build(case+'-forced-full',True);after=manifest(dst)
  if before!=after:raise AssertionError((model,case,'incremental/full mismatch',[k for k in set(before)|set(after)if before.get(k)!=after.get(k)][:10]))
  row={'phase':phase,'model':model,'case':case,'whole_pipeline_s':duration,'components':metrics,'maximum_measured_process_rss_mib':rss,'files':len(before),'incremental_equals_forced_full':True,'expected_change_assertions':True,'source_transaction':'coordinated maintained inputs; authoring outside timed build'}
  RESULT.append(row);(BASE/'evidence'/f'{phase}-lifecycle.json').write_text(json.dumps(RESULT,indent=2)+'\n');print(json.dumps(row),flush=True)
 baseline_duration,baseline_metrics,baseline_rss=build('baseline')
 reference={p.relative_to(BASE/'site').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(BASE/'site').rglob('*')if p.is_file()}
 assert manifest(dst)==reference,(model,'D7 maintained-model changes failed frozen publication parity')
 humanrows=json.loads((ROOT/'deno/data/routes.json').read_text());agentrows=json.loads((dst/'data/routes.json').read_text())if model=='deno-agent'else None
 authored=[r for r in humanrows if r['kind']=='authored-markdown'and r['sourcePath'].endswith('.md')]
 authored.sort(key=lambda r:(r['url']!='/runtime/run/',r['url']))
 def body(row,marker=MARKER):
  if model=='deno':
   path='authored/'+row['sourcePath'].lstrip('/');write(path,(dst/path).read_text()+'\n\n'+marker+'\n')
  else:
   a=next(a for a in agentrows if a['route']==row['url']);value=(dst/a['body']).read_text().replace('</main>','<p>'+marker+'</p></main>');write(a['body'],value);a['projection_body_sha256']=hashlib.sha256(value.encode()).hexdigest()
   if 'download'in a:write('exports/'+a['download'],(dst/'exports'/a['download']).read_text()+'\n\n'+marker+'\n')
   projections(dst,write,a['route'],marker=marker);write('data/routes.json',json.dumps(agentrows,indent=2))
 for n in [1,10,100]:
  for row in authored[:n]:body(row)
  def assertion(n=n):
   for row in authored[:n]:
    assert MARKER in(dst/'public'/row['outputPath'].lstrip('/')).read_text()
    download=dst/'public'/row['sourcePath'].lstrip('/')
    if download.exists():assert MARKER in download.read_text()
    docs=json.loads((dst/'public/orama-index-full.json').read_text())['data']
    matching=[d for d in docs if d['url'].rstrip('/')=='https://docs.deno.com'+row['url'].rstrip('/')]
    for d in matching:assert MARKER in d['content']
   assert MARKER in(dst/'public/orama-index-full.json').read_text()
  check(f'{n}-bodies',assertion);restore();build(f'{n}-bodies-restored-primer')
  if model=='deno-agent':agentrows=json.loads((dst/'data/routes.json').read_text())
 template='templates/template.html';write(template,(dst/template).read_text().replace('@content','<!-- D7-shared-layout -->@content'))
 check('shared-layout',lambda:all('D7-shared-layout'in p.read_text()for p in(dst/'public').rglob('*.html'))or (_ for _ in []).throw(AssertionError('shared layout')));restore();build('layout-restored-primer')
 if model=='deno':
  p='authored/_data.json';data=json.loads((dst/p).read_text());data['navigation'][0]['name']='Runtime D7-navigation';write(p,json.dumps(data))
 else:
  for p in(dst/'templates/navigation').glob('*.html'):write(p.relative_to(dst).as_posix(),p.read_text().replace('Runtime</a>','Runtime D7-navigation</a>'))
 check('navigation',lambda:all('Runtime D7-navigation'in p.read_text()for p in(dst/'public').rglob('*.html'))or (_ for _ in []).throw(AssertionError('navigation')));restore();build('navigation-restored-primer')
 target=authored[0];title='Run code D7-title'
 if model=='deno':
  p='authored/'+target['sourcePath'].lstrip('/');text=(dst/p).read_text();write(p,re.sub(r'(?m)^title:.*$', 'title: '+json.dumps(title),text,count=1))
 else:
  a=next(a for a in agentrows if a['route']==target['url']);a['title']=title;write('data/routes.json',json.dumps(agentrows,indent=2));projections(dst,write,a['route'],title=title)
  if 'download'in a:
   p='exports/'+a['download'];write(p,re.sub(r'(?m)^title:.*$', 'title: '+json.dumps(title),(dst/p).read_text(),count=1))
 def title_assertion():
  s=(dst/'public/runtime/run/index.html').read_text();assert '<title>'+title+' | Deno Docs</title>'in s;assert title in(dst/'public/orama-index-full.json').read_text();assert hashlib.sha256((dst/'public/runtime/run/index.png').read_bytes()).hexdigest()==reference['runtime/run/index.png'];assert title in(dst/'public/runtime/run/index.md').read_text()
 check('title-metadata',title_assertion);restore();build('title-restored-primer')
 if model=='deno-agent':agentrows=json.loads((dst/'data/routes.json').read_text())
 if model=='deno':
  p='authored/reference_gen/gen/deno.json';data=json.loads((dst/p).read_text())
  value=data['./~/Deno.HttpServer.json']['symbol_group_ctx']['symbols'][0]['content'][0]['value'];assert isinstance(value['docs'],str);value['docs']+='<p>'+MARKER+'</p>';write(p,json.dumps(data))
 else:
  a=next(a for a in agentrows if a['route']=='/api/deno/http-server/');value=(dst/a['body']).read_text().replace('</main>','<p>'+MARKER+'</p></main>');write(a['body'],value);a['projection_body_sha256']=hashlib.sha256(value.encode()).hexdigest();write('data/routes.json',json.dumps(agentrows,indent=2))
  p='data/publication/orama-index-full.json';data=json.loads((dst/p).read_text());d=next(d for d in data['data']if d['docType']=='api-reference'and 'Deno.HttpServer'in d['url']);projections(dst,write,d['url'].removeprefix('https://docs.deno.com'),marker=MARKER)
 def generated_assertion():assert MARKER in(dst/'public/api/deno/http-server/index.html').read_text();assert MARKER in(dst/'public/orama-index-full.json').read_text()
 check('generated-reference-data',generated_assertion);restore();build('reference-restored-primer')
 # CRUD is one coherent authoring transaction spanning route/navigation/projection inputs.
 added='/runtime/d7-proof/';renamed='/runtime/d7-renamed/';rows=json.loads((dst/'data/routes.json').read_text());new=None
 def nav(old,new):
  if model=='deno':
   p='authored/_data.json';data=json.loads((dst/p).read_text())
   if old is None:data['navigation'].append({'name':'D7 lifecycle','href':new})
   elif new is None:data['navigation']=[x for x in data['navigation']if x['href']!=old]
   else:
    for x in data['navigation']:
     if x['href']==old:x['href']=new
   write(p,json.dumps(data))
  else:
   for p in(dst/'templates/navigation').glob('*.html'):
    text=p.read_text()
    if old is None:text=text.replace('</nav>',f'<a href="{new}">D7 lifecycle</a></nav>')
    elif new is None:text=text.replace(f'<a href="{old}">D7 lifecycle</a>','')
    else:text=text.replace(f'<a href="{old}">D7 lifecycle</a>',f'<a href="{new}">D7 lifecycle</a>')
    write(p.relative_to(dst).as_posix(),text)
 if model=='deno':
  new={'url':added,'outputPath':added+'index.html','sourcePath':'/runtime/d7-proof.md','layout':'doc.tsx','kind':'authored-markdown'};write('authored/runtime/d7-proof.md','---\ntitle: "D7 lifecycle"\ndescription: Lifecycle evidence\n---\n\n'+MARKER+'\n')
 else:
  new=dict(next(x for x in rows if x['route']=='/runtime/run/'));new.update(route=added,title='D7 lifecycle',body='html/runtime/d7-proof.html',download='runtime/d7-proof.md');value=(dst/'html/runtime/run.html').read_text().replace('</main>','<p>'+MARKER+'</p></main>');new['projection_body_sha256']=hashlib.sha256(value.encode()).hexdigest();write(new['body'],value);write('exports/'+new['download'],'---\ntitle: "D7 lifecycle"\n---\n\n'+MARKER+'\n');projections(dst,write,added,MARKER,title='D7 lifecycle',add=True)
  ownership=json.loads((dst/'data/download-ownership.json').read_text());ownership.extend(['runtime/d7-proof.md','runtime/d7-renamed.md']);write('data/download-ownership.json',json.dumps(ownership))
 image_rows=json.loads((dst/'data/og-assets.json').read_text());image=dict(next(x for x in image_rows if x['route']=='/runtime/run/'));image.update(route=added,output=added.lstrip('/')+'index.png');image_rows.append(image);write('data/og-assets.json',json.dumps(image_rows))
 rows.append(new);write('data/routes.json',json.dumps(rows,indent=2));nav(None,added)
 def add_assertion():
  assert(dst/'public/runtime/d7-proof/index.html').exists();assert(dst/'public/runtime/d7-proof/index.png').exists();assert(dst/'public/runtime/d7-proof.md').exists();assert added.rstrip('/') in(dst/'public/orama-index-full.json').read_text();assert added in(dst/'public/runtime/run/index.html').read_text()
 check('route-add',add_assertion)
 if model=='deno':
  source=(dst/'authored/runtime/d7-proof.md').read_text();remove('authored/runtime/d7-proof.md');write('authored/runtime/d7-renamed.md',source);new.update(url=renamed,outputPath=renamed+'index.html',sourcePath='/runtime/d7-renamed.md')
 else:
  source=(dst/'exports/runtime/d7-proof.md').read_text();remove('exports/runtime/d7-proof.md');write('exports/runtime/d7-renamed.md',source);new.update(route=renamed,download='runtime/d7-renamed.md');projections(dst,write,added,newroute=renamed)
 image.update(route=renamed,output=renamed.lstrip('/')+'index.png');write('data/og-assets.json',json.dumps(image_rows))
 write('data/routes.json',json.dumps(rows,indent=2));nav(added,renamed)
 def rename_assertion():
  for suffix in ['index.html','index.png']:assert not(dst/'public/runtime/d7-proof'/suffix).exists();assert(dst/'public/runtime/d7-renamed'/suffix).exists()
  assert not(dst/'public/runtime/d7-proof.md').exists();assert(dst/'public/runtime/d7-renamed.md').exists()
  for name in ['orama-index-full.json','orama-index-summary.json','llms.json','sitemap.xml']:assert added.rstrip('/') not in(dst/'public'/name).read_text();assert renamed.rstrip('/') in(dst/'public'/name).read_text()
  assert added not in(dst/'public/runtime/run/index.html').read_text()
 check('route-rename',rename_assertion)
 rows.remove(new);write('data/routes.json',json.dumps(rows,indent=2));nav(renamed,None)
 if model=='deno':remove('authored/runtime/d7-renamed.md')
 else:remove('exports/runtime/d7-renamed.md');projections(dst,write,renamed,delete=True)
 def delete_assertion():
  for suffix in ['index.html','index.png']:assert not(dst/'public/runtime/d7-renamed'/suffix).exists()
  assert not(dst/'public/runtime/d7-renamed.md').exists()
  for name in ['orama-index-full.json','orama-index-summary.json','llms.json','sitemap.xml','llms-full.txt','llms-summary.txt']:assert renamed.rstrip('/') not in(dst/'public'/name).read_text()
  assert renamed not in(dst/'public/runtime/run/index.html').read_text()
 check('route-delete',delete_assertion);restore()
 print(model+' lifecycle complete',flush=True)

if __name__=='__main__':
 phase=sys.argv[1]if len(sys.argv)>1 else'd7-initial'
 for model in ['deno','deno-agent']:run(model,phase)
