from pathlib import Path
import subprocess,os,json,shutil,hashlib,time
b=Path(__file__).resolve().parent;env={**os.environ,'DENO_BIN':str(b/'tools/deno'),'DENO_DIR':str(b/'cache')};reference={p.relative_to(b/'site').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(b/'site').rglob('*')if p.is_file()};out=[]
for model in ['deno','deno-agent']:
 dst=b/'clean-checkouts'/f'{model}-final-d9'
 if dst.exists():raise RuntimeError('Preserve existing fresh-checkout evidence')
 subprocess.run(['git','clone','--no-local',str(b.parent/model),str(dst)],check=True)
 revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=dst,text=True).strip()
 for rel in ['.generated','public','.nift/public']:assert not(dst/rel).exists(),rel
 start=time.perf_counter()
 with(b/'logs'/f'd9-fresh-{model}.log').open('w')as f:subprocess.run(['python3','scripts/build.py'],cwd=dst,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 files={p.relative_to(dst/'public').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in(dst/'public').rglob('*')if p.is_file()};assert files==reference
 status=subprocess.check_output(['git','status','--porcelain'],cwd=dst,text=True);assert not status,status
 subprocess.run(['nift','status'],cwd=dst,env=env,check=True)
 out.append({'model':model,'revision':revision,'publication_files':len(files),'html_documents':len([k for k in files if k.endswith('.html')]),'all_reference_bytes_equal':True,'source_clean_after_build':True,'application_state_empty_before_build':True,'verification_observation_s':time.perf_counter()-start,'boundary':'Dependencies and frozen maintained inputs prepared; this correctness run is not a benchmark sample.'});(b/'evidence/d9-final-fresh-checkouts.json').write_text(json.dumps(out,indent=2)+'\n');print(model,'fresh committed checkout exact and clean',flush=True)
