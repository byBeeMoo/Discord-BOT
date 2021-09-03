from discord.ext import commands
import os
from settings import DEBUG

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_money_storage(self, member):
        pathToFile = f"./usersBank/{member}.txt"
        if not os.path.isfile(pathToFile):
            with open(pathToFile, "w") as file:
                file.write('money: 100')
    
    async def get_money(self, member):
        pathToFile = f"./usersBank/{member}.txt"
        with open(pathToFile, "r") as getBankMoney:
            return str(getBankMoney.readline().split()[1])
                    
    async def set_money(self, member, money):
        pathToFile = f"./usersBank/{member}.txt"
        setMoney = money + int(await self.get_money(member))
        
        with open(pathToFile, "w") as setBankMoney:
            setBankMoney.write("money: "+ str(setMoney))
            
### OUTSIDE CLASS ###
def setup(bot):
    bot.add_cog(Economy(bot))