import sqlite3
from datetime import datetime

def db_connect(): # Connect to database
    conn = sqlite3.connect('pdx.sqlite')
    return conn

def db_close(conn): # Close connection
    conn.close()

def db_create_table(conn): # Create table
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, d_id TEXT, life INT, pokemon TEXT, name TEXT, ko TEXT, timewait TIMESTAMP, level INT, xp INT, nextxp INT, recover TIMESTAMP)')
    conn.commit()

def db_delete_table(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE players')
    conn.commit()

def db_insert_player(conn, d_id, life, pokemon, name, ko, timewait): # Insert a row of data
    cursor = conn.cursor()
    cursor.execute('INSERT INTO players (d_id, life, pokemon, name, ko, timewait, level, xp, nextxp, recover) VALUES (?, ?, ?, ?, ?, ?, 1, 1, 4, ?)', (d_id, life, pokemon, name, ko, timewait, timewait))
    print(conn.commit())

def db_update_player_life(conn, d_id, life): # Update life
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET life = ? WHERE d_id = ?', (life, d_id))
    conn.commit()

def db_update_player_pokemon(conn, d_id, pokemon): # Update pokemon
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET pokemon = ? WHERE d_id = ?', (pokemon, d_id))
    conn.commit()

def db_update_player_timewait(conn, d_id, timewait): # Update timewait
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET timewait = ? WHERE d_id = ?', (timewait, d_id))
    conn.commit()

def db_update_pokemon_name(conn, d_id, name): # Update pokemon name
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET name = ? WHERE d_id = ?', (name, d_id))
    conn.commit()

def db_update_pokemon_ko(conn, d_id, ko): # Update pokemon ko
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET ko = ? WHERE d_id = ?', (ko, d_id))
    conn.commit()

def db_delete_player(conn, d_id): # Delete a row of data
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players WHERE d_id = ?', (d_id,))
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