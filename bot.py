import discord
import responses
import random
import json
import re

c = open('config.json')
config = json.load(c)
TOKEN = config.get("Token")

funny_list = ["Bazinga!", "Benghazi!","Bazooka!","Bronchitis!","Zimbabwe!","Babuska!"]
bazinga_count = 0


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_responses(user_message)
        if response is not None:
            if len(response) < 2000:
                print(len(response))
                print("Less than 2000")
                response = '>>> ' + response
                await message.author.send(response) if is_private else await message.channel.send(response)
            else:
                print(len(response))
                print("More than 2000")
                split_response = response.split("-----------")
                if len(split_response) == 3:
                    if len(split_response[2]) > 2000:
                        split_legendary = split_response[2].split('\n\n',3)
                        split_response.pop()
                        split_response += split_legendary 
                split_prepend = ['>>> ' + part for part in split_response]
                split_response = split_prepend
                for response_part in split_response:
                    await message.author.send(response_part) if is_private else await message.channel.send(response_part)
    except Exception as e:
        print(e)
    
def run_discord_bot():
    bazinga_count = 0
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        #print(type(user_message))
        #print(f"{username} said: {user_message} in {channel}.")

        if message.content.startswith('?funny'):
            bazinga = f"{username}\'s most famous quote is {funny_list[random.randint(0,5)]}"
            global bazinga_count
            bazinga_count += 1
            if bazinga_count > 10:
                bazinga_count = 0
                await message.channel.send("Please stop making me say bazinga, I'm begging you.")
            else:
                await message.channel.send(bazinga)
                await message.channel.send(bazinga)
                await message.channel.send(bazinga)
        try:
            if user_message[0] == '!':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)
        except Exception as e:
            print(Exception)
            print(user_message)
            await send_message(message, user_message, is_private=False)
        
    client.run(TOKEN)