from datetime import datetime, timedelta, date, time
import json
import db as db
import discord as discord
from discord.ext import commands
from discord.ext import tasks
import get_p as pok
import random
import asyncio

description = '''Bot pour les combats pokemon'''

conn = db.db_connect()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Log into {0.user}'.format(bot))
    random_pokemon.start()
    await asyncio.sleep(5)
    attaque_random_pokemon.start()
    await asyncio.sleep(5)
    check_ko.start()


@bot.command(name="aide", description="Affiche l'aide")
async def aide(ctx):
    embed = discord.Embed(title="Aide", description="Liste des commandes", color=0xeee657)
    embed.add_field(name="?aide", value="Affiche l'aide", inline=False)
    embed.add_field(name="?rejoindre <nom_pokemon> <son_nom>", value="Permet de rejoindre le combat", inline=False)
    embed.add_field(name="?quitter", value="Permet de quitter le combat", inline=False)
    embed.add_field(name="?monpoke", value="Afficher son Pokemon et ses caractéristiques", inline=False)
    embed.add_field(name="?listepokemon", value="Affiche la liste des Pokémons", inline=False)
    embed.add_field(name="?attaque <nom_attaque> <tag_du_joueur>", value="Attaque le joueur taggé dans le message", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='rejoindre', description='Rejoindre le combat')
async def add(ctx, pokemon: str, name: str):
    if ctx.author.bot:
        return
    if pok.check_pokemon(pokemon):
        db.db_insert_player(conn, ctx.author.id, pok.get_pokemon_life(pokemon), pokemon, name, "NO", datetime.now())
        await ctx.send('Vous venez de rejoindre le combat !')
    else:
        await ctx.send('Vous devez saisir un Pokemon présent dans la liste ! Utilisez la commande ?listepokemon pour voir la liste des Pokémons !')

@add.error
async def rejoindre_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.qualified_name == "rejoindre":
            embed = discord.Embed(title="Erreur !", description="Vous n'avez pas saisie la commande comme il le faut !", color=0xe05000)
            embed.add_field(name="Exemple :", value='?rejoindre Lucario Joe', inline=True)
            await ctx.send(embed=embed)

@bot.command(name='quitter', description='Quitter le combat')
async def delete(ctx):
    if ctx.author.bot:
        return
    db.db_delete_player(conn, ctx.author.id)
    await ctx.send('Vous venez de quitter le combat !')

@bot.command(name='monpoke', description='Afficher le pokemon')
async def pokemon(ctx):
    if ctx.author.bot:
        return
    if db.db_check_player(conn, ctx.author.id):
        get_level = db.db_get_level(conn, ctx.author.id)[0]
        get_xp = db.db_get_xp(conn, ctx.author.id)[0]
        get_nlevel_xp = db.db_get_nextxp(conn, ctx.author.id)[0]
        get_id = pok.get_pokemon_id(db.db_get_pokemon(conn, ctx.author.id)[0])

        date = db.db_get_time(conn, ctx.author.id)
        time = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S.%f')
        r_time = time - datetime.now()
        
        rest_time = db.db_get_recover(conn, ctx.author.id)[0]
        rest_time = datetime.strptime(str(rest_time), '%Y-%m-%d %H:%M:%S.%f')

        if rest_time < datetime.now():
            db.db_update_pokemon_ko(conn, ctx.author.id, "NO")

        if db.db_get_pokemon_ko == "YES":
            embed = discord.Embed(title="Mon Pokémon | " + db.db_get_pokemon_name(conn, ctx.author.id)[0], description="Caractéristiques de votre Pokémon | **KO**", color=0xe05000)
        else:
            embed = discord.Embed(title="Mon Pokémon | " + db.db_get_pokemon_name(conn, ctx.author.id)[0], description="Caractéristiques de votre Pokémon", color=0xe05000)
        
        embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(get_id) + ".png")
        embed.add_field(name="Votre Pokémon", value=db.db_get_pokemon(conn, ctx.author.id)[0], inline=True)
        embed.add_field(name="Points de vie", value=db.db_get_life(conn, ctx.author.id)[0], inline=True)
        embed.add_field(name="Vos attaques", value=str(pok.get_stuff(db.db_get_pokemon(conn, ctx.author.id)[0])), inline=True)
        embed.add_field(name="Niveau et XP", value=str(get_level) + " | " + str(get_xp), inline=True)
        embed.add_field(name="XP avant niveau suivant", value=str(get_nlevel_xp), inline=True)
        try : 
            h_time = datetime.strptime(str(r_time), '%H:%M:%S.%f')
            embed.add_field(name="Prochaine attaque", value=str(h_time.minute) + " minutes", inline=True)
        except :
            embed.add_field(name="Prochaine attaque", value="Maintenant !", inline=True)

        await ctx.send(embed=embed)
    else:
        await ctx.send('Vous devez rejoindre le combat !')

@bot.command(name='listepokemon', description='Afficher la liste des pokemon')
async def listepokemon(ctx):
    if ctx.author.bot:
        return
    await ctx.send("Voici les Pokémons disponible : " + pok.get_pokemon_list())

@bot.command(name='attaquesauvage', description='Attaque le Pokémon sauvage indiqué par son nom')
async def attaquesauvage(ctx, attaque: str, pokemon: str):
    if ctx.author.bot:
        return

    try:
        id = db.db_get_ps_by_name(conn, pokemon)[0]
    except:
        await ctx.send("Le Pokémon sauvage n'existe pas !")
        return

    if db.db_get_ps_ko(conn, id)[0] == "YES" or db.db_get_ps_life(conn, id)[0] <= 0 or db.db_get_pokemon_ko(conn, ctx.author.id)[0] == "YES" or db.db_get_life(conn, ctx.author.id)[0] <= 0:
        await ctx.send("Le Pokémon sauvage est KO ou vous êtes KO !")
        return

    date = datetime.strptime(str(db.db_get_time(conn, ctx.author.id)[0]), '%Y-%m-%d %H:%M:%S.%f')

    if  date > datetime.now():
        await ctx.send("Vous devez attendre avant de pouvoir attaquer !")
        return
    
    l_now = int(db.db_get_ps_life(conn, id)[0])
    u_pokemon = db.db_get_pokemon(conn, ctx.author.id)[0]
    u_pokemon_atk = db.db_get_ps_name_by_id(conn, id)[0]
    cal_atk = pok.calc_pokemon_attack(u_pokemon, attaque, u_pokemon_atk)

    t_atk = "Coup Normal"

    be_atk = pok.get_pokemon_attack(u_pokemon_atk, attaque)
    if be_atk < cal_atk:
        t_atk = "Coup Critique !"
    elif be_atk > cal_atk:
        t_atk = "C'est pas très efficace..."

    if cal_atk == 0:
        t_atk = "Manqué !"
        win_xp = 0

    life = l_now - cal_atk
    db.db_update_ps_life(conn, id, life)
    db.db_update_player_timewait(conn, ctx.author.id, datetime.now() + timedelta(minutes=2))
    embed = discord.Embed(title="Attaque !", description="Une attaque est lancé !", color=0xe05000)
    embed.add_field(name=t_atk, value=f'Vous attaquez un {u_pokemon_atk} sauvage, il lui reste ' + str(life) + ' PV !', inline=True)
    await ctx.send(embed=embed)


@bot.command(name='attaque')
async def attaque(ctx, attaque: str):
    try:    
        members = ctx.message.mentions
        first_member_id = members[0].id
    except:
        await ctx.send("Vous devez tagger un joueur !")
        return

    if ctx.author.bot:
        return
    if db.db_check_player(conn, ctx.author.id) and db.db_check_player(conn, first_member_id):

        rest_time = db.db_get_recover(conn, ctx.author.id)[0]
        rest_time = datetime.strptime(str(rest_time), '%Y-%m-%d %H:%M:%S.%f')

        if rest_time < datetime.now():
            db.db_update_pokemon_ko(conn, ctx.author.id, "NO")

        if db.db_get_pokemon_ko(conn, ctx.author.id)[0] == "YES":
            await ctx.send("Votre Pokémon est KO !")
            return

        date = db.db_get_time(conn, ctx.author.id)
        time = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S.%f')

        get_level = db.db_get_level(conn, ctx.author.id)[0]
        get_level_oppo = db.db_get_level(conn, first_member_id)[0]
        get_xp = db.db_get_xp(conn, ctx.author.id)[0]
        get_nlevel_xp = db.db_get_nextxp(conn, ctx.author.id)[0]

        if time > datetime.now():
            await ctx.send('Vous devez attendre 5 minutes entre chaque attaques !')
        else:
            if ctx.author.id == first_member_id:
                await ctx.send('Vous ne pouvez pas attaquer votre propre Pokémon !')
            elif db.db_get_pokemon_ko(conn, ctx.author.id) == "YES" or db.db_get_pokemon_ko(conn, first_member_id) == "YES":
                await ctx.send('Vous ne pouvez pas attaquer un Pokémon KO !')
            else:
                t_atk = "Coup Normal"

                l_now = db.db_get_life(conn, first_member_id)
                l_now = int(l_now[0])
                u_pokemon = db.db_get_pokemon(conn, ctx.author.id)[0]
                u_pokemon_atk = db.db_get_pokemon(conn, first_member_id)[0]
                cal_atk = pok.calc_pokemon_attack(u_pokemon, attaque, u_pokemon_atk)
                
                win_xp = ((get_level_oppo % get_level) + 1) * 2

                be_atk = pok.get_pokemon_attack(u_pokemon_atk, attaque)
                if be_atk < cal_atk:
                    t_atk = "Coup Critique !"
                    win_xp = ((get_level_oppo % get_level) + 1) * 4
                elif be_atk > cal_atk:
                    t_atk = "C'est pas très efficace..."
                    win_xp = ((get_level_oppo % get_level) + 1) * 1

                if cal_atk == 0:
                    t_atk = "Manqué !"
                    win_xp = 0

                all_xp = get_xp + win_xp

                life = l_now - cal_atk
                db.db_update_player_life(conn, first_member_id, life)
                db.db_update_player_timewait(conn, ctx.author.id, datetime.now() + timedelta(minutes=5))
                db.db_update_xp(conn, ctx.author.id, all_xp)
                embed = discord.Embed(title="Attaque !", description="Une attaque est lancé !", color=0xe05000)
                embed.add_field(name=t_atk, value=f'Vous attaquez {members[0].mention} et son ' + u_pokemon_atk + ', il lui reste ' + str(life) + ' PV !', inline=True)
                await ctx.send(embed=embed)

                g_xp_ac = db.db_get_nextxp(conn, ctx.author.id)[0]

                if all_xp >= g_xp_ac:
                    new_xp = 0.8 * ((get_level + 1)**3)
                    db.db_update_level(conn, ctx.author.id, get_level + 1)
                    db.db_update_nextxp(conn, ctx.author.id, g_xp_ac + new_xp)
                    await ctx.send(f'Bravo {ctx.author.mention}, votre Pokémon a gagné un niveau ! Il est désormais niveau {get_level + 1} !')

                if life <= 0:
                    embed = discord.Embed(title="KO !", description="Vite ! Le Centre Pokémon !", color=0xe05000)
                    embed.add_field(name="Oh...", value='Il semble que le ' + u_pokemon_atk + f' de {members[0].mention} soit KO...', inline=True)
                    await ctx.send(embed=embed)
                    db.db_update_pokemon_ko(conn, first_member_id, "YES")

@attaque.error
async def attaque_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.qualified_name == "attaque":
            embed = discord.Embed(title="Erreur !", description="Vous n'avez pas saisie la commande comme il le faut !", color=0xe05000)
            embed.add_field(name="Exemple :", value='?attaque Eclair @Rhenar', inline=True)
            await ctx.send(embed=embed)

@tasks.loop(seconds=3)
async def check_ko():
    channel = bot.get_channel(710549738482827318)
    try: 
        u_id = db.db_get_ps_last_id(conn)[0]
    except:
        return
    
    if db.db_get_ps_init(conn, u_id) != "YES":
        return

    life = db.db_get_ps_life(conn, u_id)[0]
    pokemon = db.db_get_ps_name_by_id(conn, u_id)[0] 
    ko = db.db_get_ps_ko(conn, u_id)[0]
    get_level_oppo = db.db_get_ps_level(conn, u_id)[0]

    if life <= 0:
        db.db_update_ps_ko(conn, u_id, "YES")
    else:
        return

    lmoy = int(db.db_get_moy_lvl_players(conn)[0])
    xp_calc = ((get_level_oppo % lmoy) + 1) * 4
    money = ((get_level_oppo % lmoy) + 1) * 10

    db.db_give_xp_everyone_no_ko(conn, xp_calc)
    db.db_give_money_everyone_no_ko(conn, money)
    
    embed = discord.Embed(title="KO !", description="Un beau combat !", color=0xe05000)
    embed.add_field(name="Félicitations !", value='Vous avez réussi à terrasser ' + pokemon + f'. Il rapporte {xp_calc} XP et {money} € a tout les Pokémons encore debout.', inline=True)
    await channel.send(embed=embed)
    db.db_delete_ps(conn, u_id)

@tasks.loop(seconds=300)
async def attaque_random_pokemon():
    await bot.wait_until_ready()
    channel = bot.get_channel(710549738482827318)

    try: 
        u_id = db.db_get_ps_last_id(conn)[0]
    except:
        return

    u_pokemon = db.db_get_ps_name_by_id(conn, u_id)[0]
    r_atk = pok.get_pokemon_random_atk(u_pokemon)
    r_id = db.db_get_random_player_id_no_ko(conn)[0]
    life_poke = db.db_get_life(conn, r_id)[0]

    membre = await bot.fetch_user(r_id)

    u_pokemon_atk = db.db_get_pokemon(conn, r_id)[0]

    cal_atk = pok.calc_pokemon_attack(u_pokemon, r_atk, u_pokemon_atk)

    db.db_update_player_life(conn, r_id, life_poke - cal_atk)

    embed = discord.Embed(title="Attaque !", description="Une attaque est lancé !", color=0xe05000)
    embed.add_field(name=r_atk, value=f'Un {u_pokemon} attaque {membre.mention} avec {r_atk}, il inflige ' + str(cal_atk) + ' dégats !', inline=True)
    await channel.send(embed=embed)

# Evenement aléatoire qui fait apparaitre un pokemon sauvage
@tasks.loop(seconds=600)
async def random_pokemon():
    await bot.wait_until_ready()
    channel = bot.get_channel(710549738482827318)
    pokemon = pok.get_random_pokemon()

    if db.db_nb_players_no_ko(conn)[0] == 0:
        return

    # évenement aléatoire
    if random.randint(1, 10) == 1:
        b_life = pok.get_pokemon_life(pokemon)
        nb_players = db.db_get_nb_players(conn)[0]
        timewait = datetime.now()
        get_id = pok.get_pokemon_id(pokemon)

        lmoy = int(db.db_get_moy_lvl_players(conn)[0])
        l_life = b_life * (nb_players * 0.5)

        db.db_insert_pokemon_sauvage(conn, pokemon, l_life, "NO", lmoy, timewait)

        embed = discord.Embed(title="Un Pokémon Sauvage !" , description="Un Pokémon sauvage vient d'apparaitre !", color=0xe05000)
            
        embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(get_id) + ".png")
        embed.add_field(name="Le Pokémon", value=pokemon, inline=True)
        embed.add_field(name="Points de vie", value=l_life, inline=True)
        embed.add_field(name="Niveau", value=str(lmoy), inline=True)
        embed.add_field(name="Durée du Combat", value="10 Minutes", inline=True)
        await channel.send(embed=embed)

        dn.db_set_ps_init_yes(conn, db.get_ps_id(conn)[0])

        await asyncio.sleep(590)

        embed = discord.Embed(title="Le Pokémon s'échappe" , description="Le Pokémon sauvage est entrain de s'enfuire !", color=0xe05000)
        embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(get_id) + ".png")
        await channel.send(embed=embed)
        db.db_delete_ps(conn, db.get_ps_id(conn)[0])


@bot.command(name='boom', description='Boom')
async def boom(ctx):
    if ctx.author.bot:
        return
    if ctx.author.id == 173731309120651264:
        try:
            db.db_delete_table_players(conn)
            db.db_delete_table_pokemon_sauvage(conn)
            await ctx.send('Boom !')
        except:
            await ctx.send("Il n'y avait rien à boom !")
        try:
            db.db_create_table_players(conn)
            db.db_create_table_pokemon_sauvage(conn)
            await ctx.send("Recréation terminé !")
        except:
            await ctx.send("Erreur lors de la recréation !")
    else:
        await ctx.send("T'as cru que tu pouvais le faire ?")

@bot.command(name='debug_pokemon', description='Debug Pokemon')
async def debug_pokemon(ctx):
    await bot.wait_until_ready()
    channel = bot.get_channel(710549738482827318)
    pokemon = pok.get_random_pokemon()

    if ctx.author.id != 173731309120651264:
        return

    if db.db_nb_players_no_ko(conn)[0] == 0:
        return

    b_life = pok.get_pokemon_life(pokemon)
    nb_players = db.db_get_nb_players(conn)[0]
    timewait = datetime.now()
    get_id = pok.get_pokemon_id(pokemon)

    lmoy = int(db.db_get_moy_lvl_players(conn)[0])
    l_life = b_life * (nb_players * 0.5)

    db.db_insert_pokemon_sauvage(conn, pokemon, l_life, "NO", lmoy, timewait)

    embed = discord.Embed(title="Un Pokémon Sauvage !" , description="Un Pokémon sauvage vient d'apparaitre !", color=0xe05000)
        
    embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(get_id) + ".png")
    embed.add_field(name="Le Pokémon", value=pokemon, inline=True)
    embed.add_field(name="Points de vie", value=l_life, inline=True)
    embed.add_field(name="Niveau", value=str(lmoy), inline=True)
    embed.add_field(name="Durée du Combat", value="10 Minutes", inline=True)
    await channel.send(embed=embed)

    await asyncio.sleep(600)

    embed = discord.Embed(title="Le Pokémon s'échappe" , description="Le Pokémon sauvage est entrain de s'enfuire !", color=0xe05000)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(get_id) + ".png")
    await channel.send(embed=embed)
    db.db_delete_ps(conn, db.get_ps_id(conn)[0])

with open('config.json') as config_file:
    config = json.load(config_file)

db.db_delete_table_players(conn)
db.db_delete_table_pokemon_sauvage(conn)
db.db_create_table_players(conn)
db.db_create_table_pokemon_sauvage(conn)

bot.run(config[0]['token'])
