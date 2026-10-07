"""Maintained HTML -> Nift; no Markdown/MDX/JSX content rendering. OG images are maintained static assets."""
from compose import agent, changed
from measure import run_phase
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
publication=publish(root,'deno-agent')
changed('.generated/build-metrics.json',json.dumps({'model':'maintained HTML -> Nift -> publication/search','nift_preparation_and_composition_s':compose_s,'og_generation_s':0,'og_model':'maintained static publication assets; explicit updates outside routine builds','nift_process':json.loads((root/'.generated/nift-metrics.json').read_text()),**publication,'complete_s':time.perf_counter()-started},indent=2)+'\n')
