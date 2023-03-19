import random
import re
from random import*
import json
import discord


books_data = "```Currently Approved Books for Character Creation are:\n\
    • The Core Rules (SRD, PHB, DMG, MM)\n\
    • Xanathar’s Guide to Everything\n\
    • Tasha's Cauldron of Everything\n\
    • Volo’s Guide to Monsters\n\
    • Mordenkainen’s Tome of Foes\n\
    • Sword Coast Adventurer's Guide\n\
    • The Tortle Package\n\
    • Locathah Rising\n\
    • Elemental Evil Player's Companion\n\
    • Monsters of the Multiverse\n\
    • Fizban's Treasury of Dragons\n\
    • The Wild Beyond the Witchlight\n\
Updated: 3/9/2023```"

help_data = "```The following commands have been implemented:\n\
    \n\t?books - Lists books allowed by the club for character creation.\n\
    ?help - lists and describes commands.\n\
    ?hello - Debug command. The bot will greet you with a hello.\n\
    ?monster name - Display the selected monster from the srd. If no monster is specified, a random monster is selected.\n\
    ?roll xdy - Dice Roller. \"x\" is the number of rolls you want to make and \"y\" is the dice type. Defaults to rolling once if you don't \n\
    include an x value.\n\
    ?spell name - Display the selected spell from the srd. If no spell is specified, a random spell is selected.\n\
    ?funny - Possibly my greatest achievement as a CS major.\n\
    \nStart any command with a question mark and it will be sent to you in a private message.\n```"

roll_format_message = "```Error: Rolls commands must use this format:\n\
\n?roll xdy, where x is the number of times you want to roll, and y is the number of sides of the dice you want to roll.\n\
If you do not specify the number of rolls, it will default to one.```"

def handle_responses(message):

    p_message = message.lower()

    if p_message == '?hello':
        return "Hello! :wave:"

    if p_message.startswith('?roll'):
        p_message = p_message[6:]
        return handle_rolls(p_message)
    
    if p_message == '?help':
        return help_data
    
    if p_message == '?books':
        return books_data
    
    if p_message.startswith('?monster'):
        #p_message = p_message[4:]
        return handle_monsters(p_message)
    
    if p_message.startswith('?spell'):
        return handle_spells(p_message)
pass

def handle_rolls(roll):
    roll_pattern = re.compile("^[0-9]{0,2}d{1}[0-9]{1,3}$")
    if roll_pattern.match(roll) is not None:
        split_roll = re.split('d', roll)
        if not split_roll[0]:
            split_roll[0] = '1'
        roll_number = int(split_roll[0])
        dice_type = int(split_roll[1])
        if roll_number == 0:
            return "Error: You can't roll 0 dice."
        if dice_type == 0:
            return "Error: There's no such thing as a 0-sided die"
        if roll_number == 1:
            result = str(randint(1,dice_type))
            return f"`You roll a d{dice_type}. The result is {result}.`"
        else:
            rolls = []
            final_result = 0 
            for roll in range(roll_number):
                roll_result = randint(1,dice_type)
                rolls.append(roll_result)
                final_result += roll_result
            return f"```You roll {roll_number}d{dice_type}. The results are {rolls}.\n\
                    \nThe total is {final_result}.```"
    return roll_format_message

def handle_monsters(user_message):
    m = open('data/srd_5e_monsters.json', 'r', encoding='utf-8')
    monsters = json.load(m)
    m.close()
    if user_message == '?monster':
        monster = monsters[randint(0,(len(monsters)-1))]
        # code to prevent vampire from being rolled due to vampire length. remove after work around
        if monster['name'] == 'Vampire':
            monster = monsters[0]
        #monster_result = format_monster(monster)
        print(monster['name'])
        monster_result = build_monster_embed(monster)
        return monster_result
    else:
        name_pattern = re.compile("^\?monster\s[a-zA-Z]*")
        if name_pattern.match(user_message):
            monster = None
            #Matched the pattern for name searching."
            monster_name = user_message[9:].lower()
            # code to prevent vampire from being searched due to vampire length. remove after work around
            print(monster_name)
            if monster_name == 'vampire':
                monster_result = '```Error: Vampire Not Supported Currently Due to Statblock Length.```'
                return monster_result
            for m in monsters:
                if m['name'].lower() == monster_name.lower():
                    monster = m
            if monster is not None:
                monster_result = build_monster_embed(monster)
            else:
                monster_result = '```Error: Monster Not Found.```'
        else:
            monster_result = '```Error: Invalid Monster Search Format.```'
        return monster_result

def handle_spells(user_message):
    s = open('data/spells.json', 'r', encoding='utf-8')
    spells = json.load(s)
    s.close()
    if user_message == '?spell':
        spell = spells[randint(0,(len(spells)-1))]
        #monster_result = format_monster(monster)
        print(spell['name'])
        spell_result = build_spell_embed(spell)
        return spell_result
    else:
        name_pattern = re.compile("^\?spell\s[a-zA-Z]*")
        if name_pattern.match(user_message):
            spell = None
            #Matched the pattern for name searching."
            spell_name = user_message[7:].lower()
            print(spell_name)
            for s in spells:
                if s['name'].lower() == spell_name.lower():
                    spell = s
            if spell is not None:
                spell_result = build_spell_embed(spell)
            else:
                spell_result = '```Error: Spell Not Found.```'
        else:
            spell_result = '```Error: Invalid Spell Search Format.```'
        return spell_result

def format_html(key):
    key = key.replace("<p>","\n")
    key = key.replace("</p>","\n")
    key = key.replace("<em>","*")
    key = key.replace("</em>","*")
    key = key.replace("<strong>","**")
    key = key.replace("</strong>","**")
    return key

def build_spell_embed(spell):
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
        spell_embed.add_field(name="",value="**At Higher Levels:** {higher_levels}".format(**spell),inline=False)
    return(spell_embed)

def build_monster_embed_description(monster):
    monster_description = ""
    if 'Traits' in monster:
        monster["Traits"] = format_html(monster["Traits"])
        monster_description += '{Traits}'.format(**monster)
    if 'Actions' in monster:
        monster["Actions"] = format_html(monster["Actions"])
        monster_description += '\n**Actions**\n-----------{Actions}'.format(**monster)
    if 'Legendary Actions' in monster:
        monster["Legendary Actions"] = format_html(monster["Legendary Actions"])
        monster_description += '\n**Legendary Actions**\n-----------{Legendary Actions}'.format(**monster)
    #print(monster_description)
    return monster_description

def build_monster_embed(monster):
    monster_embed=discord.Embed(title="{name}".format(**monster), color=0x9B59B6)
    monster_embed.set_image(url="{img_url}".format(**monster))
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
    return monster_embed
    