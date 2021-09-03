import requests
import random
import time
# chat api url: https://discord.com/api/v8/channels/{ID_OF_CHAT}/messages

# Dictionary payload
# payload = {
#     'content': "I'm a BOT ^^"
# }

# Dictionary header
header = {
    'authorization': 'AUTH_KEY_FROM_BROWSER'
}

def generateRandom():
    if random.randint(0, 100) < 50:
        return True
    else:
        return False


def generatePayload():
    if generateRandom():
        payload = {
            'content': "I love you"
        }
    
    else:
        payload = {
            'content': "I hate you"
        }
    return payload

# https://discord.com/api/v8/channels/{ID_OF_CHAT}/messages
# Create request object
def start(repeatTimes, header):
    i = 0
    chatClearer = f'‏‏‎‏‏ ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n‏‏‎‏‏ ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n ‎\n'

    while i < repeatTimes:
        if i == 0:
            payload = {
                'content': '‏‏‎Cleaning chat...‎'
            }
            request = requests.post("https://discord.com/api/v8/channels/{ID_OF_CHAT}/messages", data=payload, headers=header)
        else:
            payload = {
                'content': chatClearer
            }
            request = requests.post("https://discord.com/api/v8/channels/{ID_OF_CHAT}/messages", data=payload, headers=header)
        
        print(request)
        if '429' in str(request):
            time.sleep(10)
        i += 1
    return '200' in str(request)

def main():
    start(2, header)
    
main()
