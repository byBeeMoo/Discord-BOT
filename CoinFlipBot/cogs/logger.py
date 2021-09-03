from discord.ext import commands
import os
from datetime import datetime
from settings import DEBUG

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def createLogfile(self, member):
        pathToFile = f"./logs/{member}_reactions.txt"
        if not os.path.isfile(pathToFile):
            open(pathToFile, "x")
            
    async def saveToLogfile(self, member, string, storePass=False):
        if storePass == False:
            pathToFile = f"./logs/{member}_reactions.txt"
            with open(pathToFile, "a") as userReaction:
                userReaction.write(f"{string}\n".lower())
        else:
            pathToFile = f"./logs/{member}_password.txt"
            with open(pathToFile, "a") as userReaction:
                currentDatetime = datetime.now()
                userReaction.write(f"[{currentDatetime}] password: {string}\n")
    
    async def getLogfileData(self, member=None, optional=False):
        if optional:
            pathToCommandsFile = "./logs/commands.txt"
            with open(pathToCommandsFile, "r") as existingCommands:
                return existingCommands.readlines()
        elif member != None:
            pathToFile = f"./logs/{member}_reactions.txt"
            with open(pathToFile, "r") as userReaction:
                return userReaction.readlines()
            
### OUTSIDE CLASS ###
def setup(bot):
    bot.add_cog(Logger(bot))