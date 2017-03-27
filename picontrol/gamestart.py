from picontrol import processes as procs

def main():
    if procs.process_exists("emulationstation") == True:
        procs.killTasks('emulationstation')

if __name__ == "__main__":
    main()
