"""Wall time and maximum measured process RSS for a single production phase."""
from pathlib import Path
import re
import subprocess
import time


def run_phase(name, command, *, cwd=None):
    folder=Path(__file__).resolve().parents[1]/'.generated/phase-rss'
    folder.mkdir(parents=True,exist_ok=True)
    report=folder/(name+'.time')
    timer=Path('/usr/bin/time')
    measured=[str(timer),'-v','-o',str(report),*command]if timer.exists()else command
    started=time.perf_counter()
    subprocess.run(measured,cwd=cwd,check=True)
    duration=time.perf_counter()-started
    rss=None
    if timer.exists():
        match=re.search(r'Maximum resident set size \(kbytes\): (\d+)',report.read_text())
        if match:rss=int(match[1])/1024
    return {'wall_s':duration,'maximum_measured_process_rss_mib':rss}
