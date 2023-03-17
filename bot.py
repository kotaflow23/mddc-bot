import discord
import responses
import random
import json
import re
from responses import*

c = open('data/config.json')
config = json.load(c)
TOKEN = config.get("Token")

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
            m = open('data/srd_5e_monsters.json', 'r', encoding='utf-8')
            monsters = json.load(m)
            m.close()
            monster = monsters[0]
            monster_embed=discord.Embed(title="{name}".format(**monster), color=0x9B59B6)
            monster_embed.add_field(name="", value="*{meta}*".format(**monster),inline=True)
            monster_embed.add_field(name="", value="----------",inline=False)
            monster_embed.add_field(name="", value="**Armor Class**\t{Armor Class}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="**Hit Points**\t{Hit Points}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="**Speed**\t{Speed}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="----------",inline=False)
            monster_embed.add_field(name="",value="**STR**\t\t**DEX**\t\t**CON**\t\t**INT**\t\t**WIS**\t\t**CHAR**\n\
            {STR}{STR_mod}\t{DEX}{DEX_mod}\t{CON}{CON_mod}\t{INT}{INT_mod}\t{WIS}{WIS_mod}\t{CHA}{CHA_mod}".format(**monster))
            monster_embed.add_field(name="", value="----------",inline=False)
            if 'Saving Throws' in monster:
                monster_embed.add_field(name="", value="**Saving Throws**\t{Saving Throws}".format(**monster),inline=False)
            if 'Skills' in monster:
                monster_embed.add_field(name="", value="**Skills**\t{Skills}".format(**monster),inline=False)
            if 'Damage Vulnerabilities' in monster:
                monster_embed.add_field(name="", value="**Damage Vulnerabilities**\t{Damage Vulnerabilities}".format(**monster),inline=False)
            if 'Damage Resistances' in monster:
                monster_embed.add_field(name="", value="**Damage Resistances**\t{Damage Resistances}".format(**monster),inline=False)
            if 'Damage Immunities' in monster:
                monster_embed.add_field(name="", value="**Damage Immunities**\t{Damage Immunities}".format(**monster),inline=False)
            if 'Condition Immunities' in monster:
                monster_embed.add_field(name="", value="**Condition Immunities**\t{Condition Immunities}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="**Languages**\t{Languages}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="**Challenge**\t{Challenge}".format(**monster),inline=False)
            monster_embed.add_field(name="", value="----------",inline=False)
            long_text = build_monster_embed_description(monster)
            chunk_size = 1024
            chunks = [long_text[i:i+chunk_size] for i in range(0, len(long_text), chunk_size)]
            for i, chunk in enumerate(chunks):
                inline = True if i < len(chunks) - 1 else False
                monster_embed.add_field(name="", value=chunk, inline=False)
            #monster_embed.add_field(name="", value=build_embed_description(monster))
            #print(type(monster_embed))
            await message.channel.send(embed=monster_embed)
        
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