import picontrol.config

class Profile():
    @staticmethod
    def setUser(user):
        try:
            config = picontrol.config.load_config()
            config.set("user", "username", user['username'])
            config.set("user", "password", user['password'])

            picontrol.config.save_config(config)
            return True
        except:
            return False

    @staticmethod
    def getUser():
        try:
            config = picontrol.config.load_config()
            username = config.get("user", "username")
            password = config.get("user", "password")

            return {"username":username, "password":password}
        except:
            return {"username":'', "password":''}

    @staticmethod
    def setTheme(theme):
        try:
            config = picontrol.config.load_config()
            config.set("user", "theme", theme["theme"])

            picontrol.config.save_config(config)
            return True
        except:
            return False

    @staticmethod
    def getTheme():
        try:
            config = picontrol.config.load_config()
            theme = config.get("user", "theme")

            return {"theme":theme}
        except:
            return {"theme":'green'}
