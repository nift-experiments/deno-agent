"""Maintained HTML -> Nift. No Markdown, MDX, JSX, Deno or Lume renderer."""
from compose import agent, changed
import time
import json
import os
import subprocess
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
os.chdir(root)
sys.path.insert(0,str(root))
from publication.publish import publish

started=time.perf_counter()
agent()
compose_s=time.perf_counter()-started
og=json.loads((root/'data/og.json').read_text())
routes={r['route']:r for r in json.loads((root/'data/routes.json').read_text())}
og=[{**row,'title':routes[row['route']]['title']}for row in og if row['route']in routes]
changed('.generated/og-data.json',json.dumps(og))
og_start=time.perf_counter()
subprocess.run([os.environ.get('DENO_BIN','deno'),'run','--config','publication/deno.json','--lock','publication/deno.lock','--allow-read','--allow-write','--allow-env','--allow-sys','--allow-ffi','publication/og.ts','--agent'],check=True)
og_s=time.perf_counter()-og_start
publication=publish(root,'deno-agent')
changed('.generated/build-metrics.json',json.dumps({'model':'maintained HTML -> Nift -> publication/search','nift_preparation_and_composition_s':compose_s,'og_s':og_s,**publication,'complete_s':time.perf_counter()-started},indent=2)+'\n')
