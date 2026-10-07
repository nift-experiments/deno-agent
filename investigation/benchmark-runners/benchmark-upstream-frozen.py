"""Pinned upstream production phases with frozen external std inputs, no source edits."""
from pathlib import Path
import os,subprocess,time,json,hashlib,shutil,re
root=Path(__file__).resolve().parent;source=root.parent/'deno-upstream'
env={**os.environ,'PATH':str(root/'tools')+os.pathsep+os.environ['PATH'],'DENO_DIR':str(root/'cache'),'BUILD_TYPE':'FULL'}
checkout=root/'upstream-benchmark'
assert checkout.exists()
reference={p.relative_to(root/'site').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(root/'site').rglob('*')if p.is_file()}
assert not (root/'evidence/d9-final-upstream-benchmark.json').exists(), 'Preserve final evidence'
records=[]
def phase(label,name,command):
 log=root/'logs'/f'{label}-{name}.log';tfile=log.with_suffix('.time');start=time.perf_counter()
 with log.open('w')as f:subprocess.run(['/usr/bin/time','-v','-o',str(tfile),*command],cwd=checkout,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 return {'wall_s':time.perf_counter()-start,'maximum_measured_process_rss_mib':int(re.search(r'Maximum resident set size \(kbytes\): (\d+)',tfile.read_text())[1])/1024}
def build(label,prepared=False):
 start=time.perf_counter();parts={}
 if not prepared:parts['reference_types_and_doc']=phase(label,'reference',['deno','task','generate:reference'])
 parts['search']=phase(label,'search',['deno','task','generate:search'])
 parts['lume_publication']=phase(label,'lume',['deno','task','--eval','deno run --env-file -P=lume --config=deno.json '+str(root/'native-bootstrap.ts')])
 return time.perf_counter()-start,parts
# Initial cold construction is outside warm samples; it supplies native application cache.
# Completed primer preserved; resume the same checkout after a failed external fetch.
for case,count,prepared in [('warm-full',5,False),('application-cold',5,False),('prepared-input-warm-publication',5,True),('prepared-input-application-cold',5,True)]:
 for sample in range(count):
  if case in ['application-cold','prepared-input-application-cold']:
   for rel in ['_site','_cache']:
    if(checkout/rel).exists():shutil.rmtree(checkout/rel)
   if not prepared:
    for pattern in ['.gen-cache*.json','.node-incremental-cache.json']:
     for p in(checkout/'reference_gen').glob(pattern):p.unlink()
  if prepared:
   shutil.copytree(root/'generated-inputs/reference_gen/gen',checkout/'reference_gen/gen',dirs_exist_ok=True)
  label=f'd9-frozen-native-{case}-{sample+1}';duration,parts=build(label,prepared)
  manifest={p.relative_to(checkout/'_site').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(checkout/'_site').rglob('*')if p.is_file()}
  differences=[k for k in set(manifest)|set(reference)if manifest.get(k)!=reference.get(k)]
  html=[k for k in differences if k.endswith('.html')]
  if html:raise RuntimeError(('Unexpected upstream HTML drift',html[:10]))
  clean=not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=checkout,text=True)
  if not clean:raise RuntimeError('Upstream tracked source was modified')
  row={'model':'upstream','revision':'9e5dd8d930c8734defe1c3172986e6312353ac1c','case':case,'sample':sample+1,'whole_pipeline_s':duration,'components':parts,'maximum_measured_process_or_phase_rss_mib':max(x['maximum_measured_process_rss_mib']for x in parts.values()),'files':len(manifest),'bytes':sum(p.stat().st_size for p in(checkout/'_site').rglob('*')if p.is_file()),'html_reference_equal':not html,'reference_differing_files':differences,'tracked_source_clean':clean,'dependency_delivery':'Exact pinned resvg/esbuild WASM bytes from local Blob delivery; original compile count/worker lifecycle and initialization inside timing; direct CLI observations separate.','bootstrap_sha256':hashlib.sha256((root/'native-bootstrap.ts').read_bytes()).hexdigest(),'boundary':'Frozen acquired std docs in place. Official reference/search/Lume task phases; live std acquisition is excluded and disclosed. Dependency installations/cache prepared outside timing. Prepared-input publication additionally omits reference generation for the same generated-input ownership boundary as deno.'}
  records.append(row);(root/'evidence/d9-final-upstream-benchmark.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(row),flush=True)
# One changed-input production observation establishes complete publication behavior.
p=checkout/'runtime/run/index.md';original=p.read_text();p.write_text(original+'\n\nD7 upstream changed-input observation.\n')
try:
 duration,parts=build('d9-frozen-native-one-body')
 assert 'D7 upstream changed-input observation.'in(checkout/'_site/runtime/run/index.html').read_text()
 row={'model':'upstream','case':'one-body-production-publication','whole_pipeline_s':duration,'components':parts,'html_routes':len(list((checkout/'_site').rglob('*.html'))),'behavior':'Same production phase chain, including reference type/doc generation, local search and full Lume publication; not development-server hot reload.'}
 (root/'evidence/d9-final-upstream-changed-input.json').write_text(json.dumps(row,indent=2)+'\n')
finally:p.write_text(original)
