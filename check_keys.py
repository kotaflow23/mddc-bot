import json

s = open('data/spells.json', 'r', encoding='utf-8')
spells = json.load(s)
s.close()

list_of_keys = ['name', 'level', 'type', 'casting_time', 'duration', 'description', 'components', 'range', 'higher_levels', 'ritual', 'school', 'tags', 'classes']

""" for key in list_of_keys:
    count = 0
    for spell in spells:
        if not key in spell:
            count += 1
    if count > 0:
        print(f"{key} is not present in all spells")
    else:
        print(f"{key} is present in all spells") """
spell = spells[0]
#print(spell)

print(type(spell['components']))