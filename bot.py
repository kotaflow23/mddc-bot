import discord
import responses
import random
import json
import re
from responses import*

c = open('data/config.json')
config = json.load(c)
TOKEN = config.get("Token")
#TOKEN = config.get("Test Token")

funny_list = ["Bazinga!", "Benghazi!","Bazooka!","Bronchitis!","Zimbabwe!","Babuska!"]
bazinga_count = 0


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_responses(user_message)
        if type(response) == discord.embeds.Embed:
            await message.author.send(embed=response) if is_private else await message.channel.send(embed=response)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
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
        if not message.content:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if user_message == '?embed':
            s = open('data/spells.json', 'r', encoding='utf-8')
            spells = json.load(s)
            s.close()
            spell = spells[0]
            spell_embed=discord.Embed(title="{name}".format(**spell), color=0x9B59B6)
            spell_embed.add_field(name="",value="*{type}*".format(**spell))
            spell_embed.add_field(name="",value="",inline=False)
            spell_embed.add_field(name="",value="**Casting Time:** {casting_time}".format(**spell),inline=False)
            spell_embed.add_field(name="",value="**Range:** {range}".format(**spell),inline=False)
            component_string = spell['components']['raw']
            spell_embed.add_field(name="",value=F"**Components:** {component_string}",inline=False)
            spell_embed.add_field(name="",value="**Duration:** {duration}".format(**spell),inline=False)
            class_string = ""
            for c in spell['classes']:
                c = c.capitalize()
                class_string += c
                class_string += " "
            spell_embed.add_field(name="",value=f"**Classes:** {class_string}",inline=False)
            spell_embed.add_field(name="",value="{description}".format(**spell),inline=False)
            if "higher_levels" in spell:
                spell_embed.add_field(name="",value="**At Higher Levels:** {high_levels}".format(**spell),inline=False)
            await message.channel.send(embed=spell_embed)
        
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