from picontrol import processes as procs

if procs.process_exists("emulationstation") == True:
    procs.killTasks('emulationstation')
