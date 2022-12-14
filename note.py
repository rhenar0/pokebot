@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!help'):
        await message.channel.send('!help, !add, !delete, !update, !select, !all, !allby, !time, !pokemon, !life')

    if message.content.startswith('!updatetime'):
        db.db_update_player_timewait(conn, message.author.id, datetime.now())
        await message.channel.send('Time Update!')

    if message.content.startswith('!delete'):
        db.db_delete_player(conn, message.author.id)
        await message.channel.send('Deleted!')

    if message.content.startswith('!update'):
        db.db_update_player_life(conn, message.author.id, 200)
        await message.channel.send('Updated!')

    if message.content.startswith('!select'):
        await message.channel.send(db.db_select_player(conn, message.author.id))

    if message.content.startswith('!all'):
        await message.channel.send(db.db_select_all_players(conn))

    if message.content.startswith('!allby'):
        await message.channel.send(db.db_select_all_players_by_pokemon(conn, 'Pikachu'))

    if message.content.startswith('!time'):
        await message.channel.send(db.db_get_time(conn, message.author.id))

    if message.content.startswith('!pokemon'):
        await message.channel.send(db.db_get_pokemon(conn, message.author.id))

    if message.content.startswith('!life'):
        await message.channel.send(db.db_get_life(conn, message.author.id))




        if ctx.author.bot:
        return
    if db.db_check_player(conn, ctx.author.id) and db.db_check_player(conn, discord_user):
        if db.db_get_time(conn, ctx.author.id) > datetime.now():
            await ctx.send('Vous devez attendre 5 minutes entre chaque attaque !')
        else:
            if db.db_get_pokemon(conn, ctx.author.id) == db.db_get_pokemon(conn, discord_user):
                await ctx.send('Vous ne pouvez pas attaquer le même pokémon à chaque fois !')
            else:
                db.db_update_player_life(conn, discord_user, db.db_get_life(conn, discord_user) - pok.get_pokemon_attack(db.db_get_pokemon(conn, ctx.author.id)))
                db.db_update_player_timewait(conn, ctx.author.id, datetime.now())
                await ctx.send('Attaque!')


    if ctx.author.bot:
        return
    if pok.check_pokemon(pokemon):
        if db.db_check_player(conn, ctx.author.id):
            if db.db_get_pokemon_ko(conn, ctx.author.id)[0] == "NO":
                if db.db_get_time(conn, ctx.author.id)[0] < datetime.now():
                    if db.db_get_pokemon(conn, ctx.author.id)[0] == "Pikachu":
                        await ctx.send("Pikachu ne peut pas attaquer le Pokémon sauvage !")
                    else:
                        db.db_update_time(conn, ctx.author.id, datetime.now() + timedelta(minutes=1))
                        db.db_update_life(conn, ctx.author.id, db.db_get_life(conn, ctx.author.id)[0] - pok.get_pokemon_damage(pokemon))
                        if db.db_get_life(conn, ctx.author.id)[0] <= 0:
                            db.db_update_pokemon_ko(conn, ctx.author.id, "YES")
                            db.db_update_life(conn, ctx.author.id, 0)
                            await ctx.send("Votre Pokémon est KO !")
                        else:
                            await ctx.send("Vous venez d'attaquer le Pokémon sauvage !")
                else:
                    await ctx.send("Vous devez attendre avant de pouvoir attaquer à nouveau !")
            else:
                await ctx.send("Votre Pokémon est KO !")
        else:
            await ctx.send("Vous devez rejoindre le combat !")
    else:
        await ctx.send("Vous devez saisir un Pokémon présent dans la liste ! Utilisez la commande ?listepokemon pour voir la liste des Pokémons !")
