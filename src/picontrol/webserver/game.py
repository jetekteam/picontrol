#!/usr/bin/python 
#game.py

import sys, os, json
from xml.dom import minidom

sys.path.append('/home/pi/scripts/picontrol')

import picontrol_processes as procs

class Game():
    @staticmethod
    def getConsoleList():
        consoles = []
        try:
            consoleDoc = minidom.parse('/etc/emulationstation/es_systems.cfg')
            consoleList = consoleDoc.getElementsByTagName('system')
            
            for console in consoleList:
                consoleObj = {}
                if console.getElementsByTagName('name'):
                    consoleObj["name"] = str(console.getElementsByTagName('name')[0].firstChild.nodeValue)
                if console.getElementsByTagName('fullname'):
                    consoleObj["fullName"] = str(console.getElementsByTagName('fullname')[0].firstChild.nodeValue)
                if console.getElementsByTagName('path'):
                    consoleObj["path"] = str(console.getElementsByTagName('path')[0].firstChild.nodeValue)
                if console.getElementsByTagName('extension'):
                    consoleObj["extensions"] = str(console.getElementsByTagName('extension')[0].firstChild.nodeValue)
                if console.getElementsByTagName('platform'):
                    if console.getElementsByTagName('platform')[0].firstChild:
                        consoleObj["platform"] = str(console.getElementsByTagName('platform')[0].firstChild.nodeValue)
                if console.getElementsByTagName('theme'):
                    consoleObj["theme"] = str(console.getElementsByTagName('theme')[0].firstChild.nodeValue)

                files = []
                for (dirpath, dirnames, filenames) in os.walk(consoleObj["path"]):
                    files.extend(filenames)
                    break
                
                consoleObj["fileCount"] = len(files)

                consoles.append(consoleObj)
        except:
            pass

        return consoles

    @staticmethod
    def getGameList(consoleInfo):
        gameList = {"games": []}
        try:
            xmldoc = minidom.parse('/opt/retropie/configs/all/emulationstation/gamelists/' + consoleInfo['name'] + '/gamelist.xml')
            xmlList = xmldoc.getElementsByTagName('game')    

            
            files = []
            for (dirpath, dirnames, filenames) in os.walk(consoleInfo["path"]):
                files.extend(filenames)
                break

            games = []
            files = sorted(files)

            for file in files:
                try:
                    gameName = file[::-1]
                    gameName = gameName[(gameName.index(".") + 1):]
                    gameName = gameName[::-1]

                    extension = file[(file.index(".") + 1):]

                    if consoleInfo["extensions"].find(extension) > -1:
                        #loop through the gamelist xml file and grab additional info
                        description = ''
                        playCount = 'NA'
                        fileName = file

                        for game in xmlList:
                            path = game.getElementsByTagName('path')[0].firstChild.nodeValue
                            fileSplitter = len(path.split('/'))
                            fileNameTest = path.split('/')[fileSplitter - 1]     
                            if fileNameTest == file:
                                fileName = fileNameTest
                                gameName = game.getElementsByTagName('name')[0].firstChild.nodeValue
                                if game.getElementsByTagName('playcount'):
                                    playCount = str(game.getElementsByTagName('playcount')[0].firstChild.nodeValue)
                                if game.getElementsByTagName('desc'):
                                    description = game.getElementsByTagName('desc')[0].firstChild.nodeValue

                        gameInfo = { 
                            "romString": {'console': consoleInfo['name'],'rom': fileName}, 
                            "name": gameName, 
                            "console": consoleInfo['fullName'],
                            "image": "", 
                            "description": description, 
                            "playCount": playCount,
                            "path": consoleInfo["path"] + '/' + fileName
                        }
                        games.append(gameInfo)
                except:
                    pass
                    
            gameList["games"] = games
        except:
            pass
                
        return gameList

    @staticmethod
    def uploadGames(request):
        response = {'type': '', 'message': '', 'data': ''}
        try:
            consoleInfo = json.loads(request.form['console'])
            fileCount = int(request.form.get('fileCount'))

            print(str(fileCount))
            for i in range(fileCount):
                file = request.files["file_" + str(i)]
                if file.filename != '':
                    file.save(consoleInfo["path"] + "/" + file.filename)
            response['type'] = 'success'
            response['message'] = 'Game(s) uploaded successfully.'
            response['data'] = ''
        except:
             response['type'] = 'error'
             response['message'] = 'Unable to upload game(s).'
             response['data'] = ''
        return response

    @staticmethod
    def deleteGame(path):
        response = {'type': '', 'message': '', 'data': ''}
        try:
            os.system("rm -R \"" + path + "\"")
            response['type'] = 'success'
            response['message'] = 'Game deleted successfully.'
            response['data'] = ''
        except:
            response['type'] = 'error'
            response['message'] = 'Unable to delete game.'
            response['data'] = ''
        return response

    @staticmethod
    def runGame(gameInfo):
        try:
            print(gameInfo)
            gameInfo = json.loads(gameInfo)
            return procs.runGame(gameInfo['console'], gameInfo['rom'], 'web')
        except:
            return False