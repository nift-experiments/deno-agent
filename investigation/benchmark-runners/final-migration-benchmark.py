from pathlib import Path
import json,os,subprocess,time,hashlib,shutil,re
base=Path(__file__).resolve().parent;root=base.parent
env={**os.environ,'DENO_BIN':str(base/'tools/deno'),'DENO_DIR':str(base/'cache')}
ref={p.relative_to(base/'site').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (base/'site').rglob('*')if p.is_file()}
assert not (base/'evidence/d9-final-profile-benchmark.json').exists(), 'Preserve prior final evidence'
records=[]
for case,count in [('warm-normal-publication',5),('warm-forced-full',5),('application-cold',5)]:
 for sample in range(count):
  for model in (['deno','deno-agent'] if sample%2==0 else ['deno-agent','deno']):
   checkout=root/model
   if case=='application-cold':
    for path in ['.generated','public','.nift/public']:
     if (checkout/path).exists():shutil.rmtree(checkout/path)
   label=f'd9-final-profile-{model}-{case}-{sample+1}';log=base/'logs'/f'{label}.log';rssfile=log.with_suffix('.time');start=time.perf_counter()
   with log.open('w')as f:subprocess.run(['/usr/bin/time','-v','-o',str(rssfile),'python3','scripts/build.py',*(['--force'] if case=='warm-forced-full' else [])],cwd=checkout,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
   wall=time.perf_counter()-start
   got={p.relative_to(checkout/'public').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (checkout/'public').rglob('*')if p.is_file()}
   assert got==ref,(model,case,'parity')
   row={'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip(),'model':model,'case':case,'sample':sample+1,'whole_pipeline_s':wall,'maximum_measured_process_rss_mib':int(re.search(r'Maximum resident set size \(kbytes\): (\d+)',rssfile.read_text())[1])/1024,'files':len(got),'baseline_bytes_equal':True,'components':json.loads((checkout/'.generated/build-metrics.json').read_text())}
   records.append(row);(base/'evidence/d9-final-profile-benchmark.json').write_text(json.dumps(records,indent=2)+'\n');print(model,case,sample+1,round(wall,3),flush=True)
