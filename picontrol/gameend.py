import subprocess
from picontrol import processes as procs

with open(procs.PROCS_PATH, '+') as fin:
    line = fin.readline()
    if line != 'reset':
        #if procs.process_exists("emulationstation") == False:
        subprocess.call('emulationstation', shell=True)
    fin.seek(0)
    fin.truncate()
