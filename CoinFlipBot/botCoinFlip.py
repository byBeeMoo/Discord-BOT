import discord
import random
import os.path
import datetime

DEBUG = False

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):      
               
        # Check if there is a message and its not written by a Discord Bot
        if len(message.content) > 0 and not message.author.bot:
            
            # Creating user variables
            userMessage = message.content.lower()
            authorMessage = message.author
            fileName = f'{message.author}.txt'
            pathToFile = f"./discordBotGameValues/{fileName}"
            
            
            """
            Check if user doesnt have its file, create one with defaults: money=100 bet=0
            Else print some debug information.
            """
            if not os.path.isfile(pathToFile):
                with open(pathToFile, "w") as file:
                    file.write('100\n0')
            else:
                if DEBUG:
                    with open("./logs.txt", "a") as log:
                        currentTime = datetime.datetime.now()
                        log.write(f"\n{currentTime} :\tUser author: {authorMessage}\n" \
                                    f"{currentTime} :\tChannel: {message.channel.type}\n" \
                                    f"{currentTime} :\tUser message: {userMessage}\n")

                
            # Reading from user file game Variables (money and bet)
            with open(pathToFile, 'r') as file:
                money = int(file.readline()[:-1])
                bet = int(file.readline())
                
            ################### Main functionallity of the game ##################
           
            if str(message.channel.type) == "private":              
                
                if 'yes' in userMessage or 'yep' in userMessage:
                    msg = f"How much do you want to bet [0-{money}]?"
                    await message.channel.send(f"{msg}")
                    
                elif 'no' in userMessage:       
                    msg = f"Bye!"
                    await message.channel.send(f"{msg}")    

                # If userMessage is a number (we assume its the bet) and its lenght is <= than its money, then ACCEPT BET
                elif userMessage[0] in '0123456789' and int(userMessage) <= money and int(userMessage) >= 0:
                    bet = int(userMessage)
                    msg = "Above or below 50?"
                    await message.channel.send(f"{msg}")
                    
                    # Save results of the bet into the user file
                    with open(pathToFile, "w") as updateBet:
                        updateBet.write(f"{money}\n{bet}")
                
                # Check if user wants to bet above or below a random generated value    
                elif userMessage in "above/below" :
                    
                    # Does the maths to establish if bet has been won, lost or is not acceptable.
                    if userMessage == "above":
                        if random.randint(0,100) > 50 and bet <= money:
                            money += bet
                            msg = f"Winner! you won {bet}\nTotal: {money}"
                            await message.channel.send(f"{msg}")
                        else:
                            money -= bet
                            msg = "You lost :c"
                            await message.channel.send(f"{msg}")
                    
                    # Does the maths to establish if bet has been won, lost or is not acceptable.
                    elif userMessage == "below":
                        if random.randint(0,100) < 50 and bet <= money:
                            money += bet
                            msg = f"Winner! you won {bet}\nTotal: {money}"
                            await message.channel.send(f"{msg}")
                        else:
                            money -= bet
                            msg = "You lost :c"
                            await message.channel.send(f"{msg}")
                            
                    # If a letter in "above/below" enters this condition, send an error to the user
                    else:
                        msg = f"Incorrect parameter '{userMessage}' received"
                        await message.channel.send(f"{msg}")
                    
                    # Save results of the bet into the user file
                    with open(pathToFile, "w") as updateMoney:
                        updateMoney.write(f"{money}\n{bet}")
                            
                # User views his money
                elif userMessage == "money":
                    msg = f"You have {money} BeemoCoins"
                    await message.channel.send(f"{msg}")
                    
                # Display help menu to user
                elif 'help' in userMessage:
                    msg = f"```prolog\n" \
                            "Usage: these are the option you can send to play the game\n" \
                            "'yes' - play the 'Python Coin Flip'\n" \
                            "'no' - stop playing the 'Python Coin Flip' and keep your BeemoCoins ;)\n" \
                            "'above or below' - where do you want to bet ('Above = +50 // Below = -50')\n" \
                            "'money' - the current BeemoCoins available to spend :wink:\n" \
                            "'*NUM*' - the amount of BeemoCoins you wish to bet ('this value has to be between 0 and *YourCoins*')\n" \
                            "'help' - display this help menu at anytime :partying_face:```\n"
                    await message.channel.send(f"{msg}")
                
                # Default game message when the user sends a DM to the bot
                else:
                    msg = f"Welcome {message.channel.recipient} to the Python Coin Flip\n" \
                            f":moneybag:\t\tYour money: {money} BeemoCoins\t\t:moneybag:\n" \
                            "\t\t\t:no_entry:\tDo you want to bet?\t:no_entry:\n" \
                            ":question:You can display help options by typing 'help':question:\n"
                    await message.channel.send(f"{msg}")    

            else:
                if "PythonGame" in str(message.channel.changed_roles[-1]) and not (userMessage[0] in '!"·$%&/()=?^ *Ç¨_><:;\\|@#~€¬][}{,.-ç´+`¡\'ºª'):
                    msg = f"Hey {authorMessage.mention}, message me in DM to play a game!"
                    await message.channel.send(f"{msg}")
                if DEBUG:
                    print(message.channel.changed_roles[-1])

## END OF BOT MyClient ##

## MAIN ##

# Debug?
if 'y' in input("Debug?[Y/n]: ").lower():
    DEBUG = True
    
## INSTANCE MyClient and RUN IT ##   
client = MyClient()
client.run('KEY_HERE')
## INSTANCE MyClient and RUN IT ##

## MAIN ##