import subprocess
import picontrol_processes as procs

f = open('/home/pi/scripts/picontrol/configs/status.conf', 'rw+')
line = f.readline()
if line != 'reset':
    #if procs.process_exists("emulationstation") == False:
    subprocess.call('emulationstation', shell=True)
f.seek(0)
f.truncate()
f.close()
