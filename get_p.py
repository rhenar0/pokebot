import json

def check_pokemon(u_pokemon):
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            return True
    return False

def get_pokemon_key(u_pokemon):
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            return key
    return 0

def get_pokemon_life(u_pokemon):
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            return pokemon[key]["life"]
    return 0

def get_pokemon_attack(u_pokemon, u_attack):
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    atk = data[0]["ATK_STUFF"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            for keyt in pokemon[key]["atk_stuff"]:
                l_att = pokemon[key]["atk_stuff"][keyt]
                if l_att == u_attack:
                    return atk[l_att]["dmg"]
    return 0

def calc_pokemon_attack(u_pokemon, u_attack, u_pokemontarget):
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    atk = data[0]["ATK_STUFF"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            for keyt in pokemon[key]["atk_stuff"]:
                l_att = pokemon[key]["atk_stuff"][keyt]
                if l_att == u_attack:
                    l_dmg = atk[l_att]["dmg"]
                    l_type = atk[l_att]["type"]
                    l_type_target = pokemon[get_pokemon_key(u_pokemontarget)]["type"]["minor_res_type"]
                    for keyt in l_type_target:
                        tempo_type = l_type_target[keyt]
                        if tempo_type == l_type:
                            return l_dmg * 2
                    return l_dmg
    return 0

def get_stuff(u_pokemon):
    l_stuff = ""
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    atk = data[0]["ATK_STUFF"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        if l_poke == u_pokemon:
            for keyt in pokemon[key]["atk_stuff"]:
                l_att = atk[pokemon[key]["atk_stuff"][keyt]]["name"]
                l_stuff += l_att + " | "
            return l_stuff
    return 0

def get_pokemon_list():
    l_pokemon = ""
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    for key in pokemon:
        l_poke = pokemon[key]["name"]
        l_pokemon += l_poke + " | "
    return l_pokemon

def get_pokemon_id(u_pokemon):
    l_pokemon = ""
    with open('pdx.json') as json_file:
        data = json.load(json_file)
    
    pokemon = data[0]["POKEMON"]
    for key in pokemon:
        if u_pokemon == pokemon[key]["name"]:
            return pokemon[key]["id"]
            