import subprocess
from picontrol import processes as procs

def main():
    with open(procs.PROCS_PATH, '+') as fin:
        line = fin.readline()
        if line != 'reset':
            #if procs.process_exists("emulationstation") == False:
            subprocess.call('emulationstation', shell=True)
        fin.seek(0)
        fin.truncate()

if __name__ == "__main__":
    main()
