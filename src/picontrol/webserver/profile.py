from picontrol.webserver.config import Config

class Profile():
    @staticmethod
    def setUser(user):
        try:
            config = Config.loadConfig()
            config.set("user", "username", user['username'])   
            config.set("user", "password", user['password'])

            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getUser():
        try:
            config = Config.loadConfig()
            username = config.get("user", "username")
            password = config.get("user", "password")   

            return {"username":username, "password":password}
        except:
            return {"username":'', "password":''}

    @staticmethod
    def setTheme(theme):
        try:
            config = Config.loadConfig()
            config.set("user", "theme", theme["theme"])
            
            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getTheme():
        try:
            config = Config.loadConfig()
            theme = config.get("user", "theme")

            return {"theme":theme}
        except:
            return {"theme":'green'}

            
