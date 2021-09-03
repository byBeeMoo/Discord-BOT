from discord.ext import commands
import os
import random
from settings import DEBUG

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def flip(self):
        return random.randint(0,1)
        
    def handleMessage(self):
        pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        messageAuthor = message.author
        if not message.author.bot:
            userMessage = message.content
            logger = self.bot.get_cog("Logger")
            economy = self.bot.get_cog("Economy")
            ## LOAD USERS REACTION && CREATE USERS LOGFILES IF YET NOT DONE ##
            await logger.createLogfile(messageAuthor)
            await economy.create_money_storage(messageAuthor)
            userReactions = await logger.getLogfileData(messageAuthor)
            botCommands = await logger.getLogfileData(messageAuthor, optional=True)
            
            if str(message.channel.type) != "private" and "PythonGame" in str(message.channel.changed_roles):
                msg = f"Hey {messageAuthor.mention}, say 'hello' in DM to play a game!"
                await message.channel.send(msg)
            else:
                if ':)' in userMessage or ':slight_smile:' in userMessage:
                    msg = f"I'm glad you are happy :blush:\n"
                    await message.channel.send(msg)
                elif ':(' in userMessage or ':frowning:' in userMessage:
                    msg = f"Ohh, don't be sad :cry:\n"
                    await message.channel.send(msg)
                elif any(userMessage.lower() in listMessage[:-1] for listMessage in userReactions):
                    msg = f"Come on... You already know that <{userMessage}> does nothing... Are you ok?\n"
                    await message.channel.send(msg)
                else:
                    ## WRITE USER REACTIONS, ANY REACTION DIFFERENT THAN A COMMAND WILL GET LOGGED ##
                    if not any(userMessage.split()[0].lower() in knownCommand for knownCommand in botCommands):
                        async for text in message.channel.history(limit=3):
                            print(f"Text content: {text.content}")
                            if text.content.lower() == "yes" and not text.author.bot:
                                lastMessage = True
                            else:
                                lastMessage = False
                        if not lastMessage:
                            await logger.saveToLogfile(messageAuthor, userMessage)    
                        else:
                            await logger.saveToLogfile(messageAuthor, userMessage, True)
                            msg = "Great!\n" \
                                "To start betting simply type: coinflip <money>\n" \
                                "Good luck ;)!\n"
                            await message.channel.send(msg)
                    
                if DEBUG:
                    ## THIS SHOULD BE LOGGED ##
                    print(f"{messageAuthor}: {userMessage}\n" \
                        f"Channel type: {str(message.channel.type)}")

    @commands.command()
    async def hello(self, ctx):
        if str(ctx.channel.type) == "private":
            economy = self.bot.get_cog("Economy")
            money = await economy.get_money(ctx.author)
            if DEBUG: ## if not hasAccount
                msg = f"Hey {ctx.message.content}, welcome to Python Coin Flip!\n" \
                    "You need to login to start playing!\n" \
                    "Create account?[yes/no]\n"
                await ctx.send(msg)
            else:
                msg = f"Hey {ctx.message.content}, welcome to Python Coin Flip!\n" \
                    f"Your current BeemoCoins are {money}!\n" \
                    "Would you like to play now [yes/no]?!\n"
                await ctx.send(msg)

    @commands.command()
    async def yes(self, ctx):
        if str(ctx.message.channel.type) == "private":
            if DEBUG:
                msg = "Great!\n" \
                    "Type your new password:\n"
                await ctx.send(msg)
            else:
                msg = "Great!\n" \
                    "To start betting simply type: coinflip <money>\n" \
                    "Good luck ;)!\n"
                await ctx.send(msg)

    @commands.command()
    async def no(self, ctx):
        if str(ctx.message.channel.type) == "private":
            await ctx.send("Bye!")
            
    @commands.command()
    async def money(self, ctx):
        if str(ctx.message.channel.type) == "private":
            userEconomy = self.bot.get_cog("Economy")
            money = await userEconomy.get_money(ctx.author)
            msg = f"You have {money} BeemoCoins"
            await ctx.send(msg)

    @commands.command()
    async def coinflip(self, ctx, bet: int): 
        userEconomy = self.bot.get_cog("Economy")
        userMoney = int(await userEconomy.get_money(ctx.author))
        if str(ctx.message.channel.type) == "private":
            if bet <= userMoney and bet > 0:    
                if userEconomy is not None:
                    if self.flip() == 1:
                        await userEconomy.set_money(ctx.author, bet) 
                        msg = f"Winner!\n" \
                            f"you won {bet}"
                        await ctx.send(msg)
                    else:
                        if not 'megachamii' in str(ctx.author):
                            bet -= 2 * bet
                            await userEconomy.set_money(ctx.author, bet)
                            msg = "You lost :c"
                            await ctx.send(msg)
                        else:
                            msg = f"You are {ctx.author} so you cant lose :heart:\n" \
                                "Also the money you just bet im gonna be giving x5 back to you"
                            await userEconomy.set_money(ctx.author, (bet * 5)) 
                            await ctx.send(msg)
            else:
                msg = f"You cant bet {bet} you only have {userMoney}"
                await ctx.send(msg)
                    
    @commands.command()
    async def tobalito(self, ctx):
        msg = "Pues tobalito es un streamer en auge que deberias estar viendo ahora mismo.\n" \
                "https://www.twitch.tv/tobalito"
        await ctx.send(msg)
        
    @commands.command()
    async def sofi(self, ctx):
        with open("./sofiImages/pollito420.png", "r") as photo:
            await ctx.send(content="Te mato", file=photo)

### OUTSIDE CLASS ###
def setup(bot):
    bot.add_cog(Coinflip(bot))