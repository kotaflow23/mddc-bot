import random
import re
from random import*
import json


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
    ?monster - Prints a random monster from the SRD. Abilities and Actions not included yet.\n\
    ?roll xdy - Dice Roller. \"x\" is the number of rolls you want to make and \"y\" is the dice type. Defaults to rolling once if you don't \n\
    include an x value.\n\
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
        return handle_srd()
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

def handle_srd():
    m = open('srd_5e_monsters.json')
    monsters = json.load(m)
    m.close()
    monster = monsters[randint(0,(len(monsters)-1))]

    monster_formatted = format_monster(monster)

    return monster_formatted

def format_monster(monster):
    monster_formatted = '**{name}**\n\
*{meta}*\n\
----------\n\
**Armor Class** {Armor Class}\n\
**Hit Points** {Hit Points}\n\
**Speed {Speed}**\n\
**STR** **DEX** **CON** **INT** **WIS** **CHAR**\n\
{STR}{STR_mod} {DEX}{DEX_mod} {CON}{CON_mod} {INT}{INT_mod} {WIS}{WIS_mod} {CHA}{CHA_mod}\n\
----------\n'.format(**monster)
    if 'Saving Throws' in monster:
        monster_formatted += '**Saving Throws** {Saving Throws}\n'.format(**monster)
    if 'Skills' in monster:
        monster_formatted += '**Skills** {Skills}\n'.format(**monster)
    if 'Damage Vulnerabilities' in monster:
        monster_formatted += '**Damage Vulnerabilities** {Damage Vulnerabilities}\n'.format(**monster)
    if 'Damage Resistances' in monster:
        monster_formatted += '**Damage Resistances** {Damage Resistances}\n'.format(**monster)
    if 'Damage Immunities' in monster:
        monster_formatted += '**Damage Immunities** {Damage Immunities}\n'.format(**monster)
    if 'Condition Immunities' in monster:
        monster_formatted += '**Condition Immunities** {Condition Immunities}\n'.format(**monster)
    if 'Skills' in monster:
        monster_formatted += '**Skills** {Skills}\n'.format(**monster)
    monster_formatted += '**Senses** {Senses}\n\
**Languages** {Languages}\n\
**Challenge** {Challenge}\n\
-----------\n'.format(**monster)
    
    
    if 'Traits' in monster:
        monster["Traits"] = format_html(monster["Traits"])
        monster_formatted += '{Traits}'.format(**monster)
    if 'Actions' in monster:
        monster["Actions"] = format_html(monster["Actions"])
        monster_formatted += '\n**Actions**\n-----------{Actions}'.format(**monster)

    if 'Legendary Actions' in monster:
        monster["Legendary Actions"] = format_html(monster["Legendary Actions"])
        monster_formatted += '{Legendary Actions}'.format(**monster)
    
    print(monster["name"])
    return monster_formatted

def format_html(key):
    key = key.replace("<p>","\n")
    key = key.replace("</p>","\n")
    key = key.replace("<em>","*")
    key = key.replace("</em>","*")
    key = key.replace("<strong>","**")
    key = key.replace("</strong>","**")
    return key