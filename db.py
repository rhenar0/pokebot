import sqlite3
from datetime import datetime

def db_connect(): # Connect to database
    conn = sqlite3.connect('pdx.sqlite')
    return conn

def db_close(conn): # Close connection
    conn.close()

def db_create_table_players(conn): # Create table
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, d_id TEXT, life INT, pokemon TEXT, name TEXT, ko TEXT, timewait TIMESTAMP, level INT, xp INT, nextxp INT, recover TIMESTAMP, money INT)')
    conn.commit()

def db_create_table_pokemon_sauvage(conn): # Create table
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS pokemon_sauvage (id INTEGER PRIMARY KEY AUTOINCREMENT, pokemon TEXT, life INT, ko TEXT, level INT, timewait TIMESTAMP, init TEXT)')
    conn.commit()

def db_delete_table_players(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE players')
    conn.commit()

def db_delete_table_pokemon_sauvage(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE pokemon_sauvage')
    conn.commit()

def db_insert_player(conn, d_id, life, pokemon, name, ko, timewait): # Insert a row of data
    cursor = conn.cursor()
    cursor.execute('INSERT INTO players (d_id, life, pokemon, name, ko, timewait, level, xp, nextxp, recover, money) VALUES (?, ?, ?, ?, ?, ?, 1, 1, 4, ?, 100)', (d_id, life, pokemon, name, ko, timewait, timewait))
    print(conn.commit())

def db_insert_pokemon_sauvage(conn, pokemon, life, ko, level, timewait): # Insert a row of data
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pokemon_sauvage (pokemon, life, ko, level, timewait, init) VALUES (?, ?, ?, ?, ?, "NO")', (pokemon, life, ko, level, timewait))
    print(conn.commit())

def db_give_money(conn, d_id, money): # Give money
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET money = money + ? WHERE d_id = ?', (money, d_id))
    conn.commit()

def db_get_ps_last_id(conn): # Get pokemon
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM pokemon_sauvage ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()

def db_get_ps_by_id(conn, id): # Get pokemon
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_get_ps_name_by_id(conn, id): # Get pokemon
    cursor = conn.cursor()
    cursor.execute('SELECT pokemon FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_update_player_life(conn, d_id, life): # Update life
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET life = ? WHERE d_id = ?', (life, d_id))
    conn.commit()

def db_update_ps_life(conn, id, life): # Update life
    cursor = conn.cursor()
    cursor.execute('UPDATE pokemon_sauvage SET life = ? WHERE id = ?', (life, id))
    conn.commit()

def db_update_player_pokemon(conn, d_id, pokemon): # Update pokemon
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET pokemon = ? WHERE d_id = ?', (pokemon, d_id))
    conn.commit()

def db_update_player_timewait(conn, d_id, timewait): # Update timewait
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET timewait = ? WHERE d_id = ?', (timewait, d_id))
    conn.commit()

def db_update_ps_timewait(conn, id, timewait): # Update timewait
    cursor = conn.cursor()
    cursor.execute('UPDATE pokemon_sauvage SET timewait = ? WHERE id = ?', (timewait, id))
    conn.commit()

def db_update_pokemon_name(conn, d_id, name): # Update pokemon name
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET name = ? WHERE d_id = ?', (name, d_id))
    conn.commit()

def db_update_pokemon_ko(conn, d_id, ko): # Update pokemon ko
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET ko = ? WHERE d_id = ?', (ko, d_id))
    conn.commit()

def db_update_ps_ko(conn, id, ko): # Update pokemon ko
    cursor = conn.cursor()
    cursor.execute('UPDATE pokemon_sauvage SET ko = ? WHERE id = ?', (ko, id))
    conn.commit()

def db_delete_player(conn, d_id): # Delete a row of data
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players WHERE d_id = ?', (d_id,))
    conn.commit()

def db_delete_ps(conn, id): # Delete a row of data
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pokemon_sauvage WHERE id = ?', (id,))
    conn.commit()

def db_select_player(conn, d_id): # Select a row of data
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_select_all_players(conn): # Select all rows of data
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players')
    return cursor.fetchall()

def db_select_all_players_by_pokemon(conn, pokemon): # Select all rows of data by pokemon
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE pokemon = ?', (pokemon,))
    return cursor.fetchall()

def db_get_time(conn, d_id): # Get time
    cursor = conn.cursor()
    cursor.execute('SELECT timewait FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_get_pokemon(conn, d_id): # Get pokemon
    cursor = conn.cursor()
    cursor.execute('SELECT pokemon FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_get_life(conn, d_id): # Get life
    cursor = conn.cursor()
    cursor.execute('SELECT life FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_check_player(conn, d_id): # Check if player exists
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_get_pokemon_name(conn, d_id): # Get pokemon name
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_get_pokemon_ko(conn, d_id): # Get pokemon ko
    cursor = conn.cursor()
    cursor.execute('SELECT ko FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_update_xp(conn, d_id, xp): # Update xp
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET xp = ? WHERE d_id = ?', (xp, d_id))
    conn.commit()

def db_get_xp(conn, d_id): # Get xp
    cursor = conn.cursor()
    cursor.execute('SELECT xp FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_update_level(conn, d_id, level): # Update level
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET level = ? WHERE d_id = ?', (level, d_id))
    conn.commit()

def db_get_level(conn, d_id): # Get level
    cursor = conn.cursor()
    cursor.execute('SELECT level FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_update_recover(conn, d_id, recover): # Update recover
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET recover = ? WHERE d_id = ?', (recover, d_id))
    conn.commit()

def db_get_recover(conn, d_id): # Get recover
    cursor = conn.cursor()
    cursor.execute('SELECT recover FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_get_nextxp(conn, d_id): # Get nextxp
    cursor = conn.cursor()
    cursor.execute('SELECT nextxp FROM players WHERE d_id = ?', (d_id,))
    return cursor.fetchone()

def db_update_nextxp(conn, d_id, nextxp): # Update nextxp
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET nextxp = ? WHERE d_id = ?', (nextxp, d_id))
    conn.commit()

def db_get_moy_lvl_players(conn): # Get moy lvl players
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(level) FROM players')
    return cursor.fetchone()

def db_get_nb_players(conn): # Get nb players
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM players')
    return cursor.fetchone()

def db_get_random_player_id(conn): # Get random player id
    cursor = conn.cursor()
    cursor.execute('SELECT d_id FROM players ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()

def db_get_random_player_id_no_ko(conn): # Get random player id no ko
    cursor = conn.cursor()
    cursor.execute('SELECT d_id FROM players WHERE ko = "NO" ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()

def db_get_ps_ko(conn, id): # Get pokemon ko
    cursor = conn.cursor()
    cursor.execute('SELECT ko FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_give_xp_everyone_no_ko(conn, xp): # Give xp to everyone no ko
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET xp = xp + ? WHERE ko = "NO"', (xp,))
    conn.commit()

def db_give_money_everyone_no_ko(conn, money): # Give money to everyone no ko
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET money = money + ? WHERE ko = "NO"', (money,))
    conn.commit()

def db_nb_players_no_ko(conn): # Get nb players no ko
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM players WHERE ko = "NO"')
    return cursor.fetchone()

def db_get_ps_life(conn, id): # Get pokemon life
    cursor = conn.cursor()
    cursor.execute('SELECT life FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_get_ps_by_name(conn, name): # Get pokemon by name
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM pokemon_sauvage WHERE pokemon = ?', (name,))
    return cursor.fetchone()

def db_get_ps_level(conn, id): # Get pokemon level
    cursor = conn.cursor()
    cursor.execute('SELECT level FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_get_ps_init(conn, id): # Get pokemon init
    cursor = conn.cursor()
    cursor.execute('SELECT init FROM pokemon_sauvage WHERE id = ?', (id,))
    return cursor.fetchone()

def db_set_ps_init_yes(conn, id): # Set pokemon init yes
    cursor = conn.cursor()
    cursor.execute('UPDATE pokemon_sauvage SET init = "YES" WHERE id = ?', (id,))
    conn.commit()