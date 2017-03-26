import sys, psutil, os, re, subprocess, time, ConfigParser, socket, threading

## killTasks
def killTasks(procnames):
    try:
        for proc in psutil.process_iter():
            if proc.name() in procnames:
                pid = str(proc.as_dict(attrs=['pid'])['pid'])
                name = proc.as_dict(attrs=['name'])['name']
                subprocess.call(["sudo", "kill", "-15", pid])

        kodiproc = ["kodi", "kodi.bin"]  # kodi needs SIGKILL -9 to close
        for proc in psutil.process_iter():
            if proc.name() in kodiproc:
                pid = str(proc.as_dict(attrs=['pid'])['pid'])
                name = proc.as_dict(attrs=['name'])['name']
                subprocess.call(["sudo", "kill", "-9", pid])
    except:
        pass

## getEmulatorPath
def getEmulatorpath(console):
    path = "/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ " + console + " "
    return path

## getGamePath
def getGamePath(console, game):
    # escape the spaces and brackets in game filename
    game = game.replace(" ", "\ ")
    game = game.replace("(", "\(")
    game = game.replace(")", "\)")
    game = game.replace("'", "\\'")

    gamePath = "/home/pi/RetroPie/roms/" + console + "/" + game
    return gamePath

def process_exists(proc_name):
    try:
        ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
        ps_pid = ps.pid
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        for line in output.split("\n"):
            res = re.findall("(\d+) (.*)", line)
            if res:
                pid = int(res[0][0])
                if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                    return True
        return False
    except:
        return False

def process_id(proc_name):
    try:
        ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
        ps_pid = ps.pid
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        for line in output.split("\n"):
            res = re.findall("(\d+) (.*)", line)
            if res:
                pid = int(res[0][0])
                if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                    return pid
        return 0
    except:
        return 0

PROCS_PATH = '/tmp/picontrol.procs'
## runGame
def runGame(console, game, source):
    try:
        # update status
        with open(PROCS_PATH, 'w') as fout:
            fout.write(source)

        emulationstationRunning = process_exists('emulationstation')

        procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                    "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                    "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                    "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                    "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                    "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                    "wolf4sdl", "solarus", "emulationstation"]
        killTasks(procnames)

        pid = os.fork()
        if not pid:
            try:
                if ((emulationstationRunning == False and source == '') or console == ''):
                    subprocess.call('emulationstation', shell=True)
                else:
                    subprocess.call(getEmulatorpath(console) + getGamePath(console,game), shell=True)
            except:
                pass
            os._exit(0)
        else:
            response = {'type':'success','data':'','message':'Successfully started game.'}
            return response
    except:
        return {'type':'error','data':'','message':'Failed to start game.'}

#////////////
