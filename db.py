from random import shuffle
import sqlite3

con = sqlite3.connect('db.db')
cur = con.cursor()
def add_player(id, name, role):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username, role) VALUES ({id}, {name}, {role})"
    cur.execute(sql)
    con.commit()
    con.close()
def select_roles():
    game_roles = count_roles()
    player_ids = count_players()
    for role, player_id in zip(game_roles, player_ids):
        sql = f"UPDATE players SET role = '{role}' WHERE plater_id = {player_id}"
    cur.execute(sql)
def vote(type, username, player_id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    sql = f"SELECT username FROM players WHERE player_id == {player_id} AND dead == 0 AND voted == 0"
    cur.execute(sql)
    if cur.fetchone():
        sql = f"UPDATE players SET {type} = {type} + 1 WHERE username = '{username}' "
        cur.execute(sql)
        sql = f"UPDATE players SET voted = 1 WHERE player_id = {player_id}"
        cur.execute(sql)
        con.commit()
        con.close()
        return True
    con.close()
    return False
def mafia_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor()

    cur.execute(f"SELECT MAX(mafia_vote) FROM players")
    max_votes = cur.fetchone()[0]

    cur.execute(f"SELECT COUNT(*) FROM players WHERE dead = 0 and role = 'Citizen' ")
    mafia_alive = cur.fetchone()[0]
    username_killed = 'никого'

    if max_votes == mafia_alive:
        cur.execute(f"SELECT username FROM players SET dead = 1 WHERE username = '{username_killed}' ")
        username_killed = cur.fetchone()[0]

        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}' ")
        con.commit()
    con.close()
    return username_killed
def citizen_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor()

    cur.execute(f"SELECT MAX(citizen_vote)")
    max_votes = cur.fetchone()[0]

    cur.execute(f"SELECT COUNT(*) FROM players WHERE citizen_vote = {max_votes} ")
    mafia_voted_count = cur.fetchone()[0]
    username_killed = 'никого'

    if mafia_voted_count == 1:
        cur.execute(f"SELECT username FROM players SET dead = 1 WHERE username = '{username_killed}' ")
        username_killed = cur.fetchone()[0]

        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}' ")
        con.commit()
    con.close()
    return username_killed
def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"UPDATE players SET citizen_vote = 0, mafia_vote = 0, voted = 0"
    if dead:
        sql += ', dead = 0'
    cur.execute(sql)
    con.commit()
    con.close()
# count functions 
def count_players():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql_func = f"SELECT username FROM players"
    cur.execute(sql_func)
    data = cur.fetchall()
    new_data = [row[0] for row in data]
    data = new_data
    con.commit()
    con.close()
    return data
def count_roles():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql_func = "SELECT role FROM players"
    cur.execute(sql_func)
    data = cur.fetchall() 
    new_data = [row[0] for row in data]
    data = new_data
    con.commit()
    con.close()
    return data
def count_alive():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql_func = "SELECT username FROM players WHERE dead = 0"
    cur.execute(sql_func)
    data = cur.fetchall()
    new_data = [row[0] for row in data]
    data = new_data
    con.commit()
    con.close()
    return data

count_players()

print(vote('citizen_vote', 'NULL', 1))

con.commit()
con.close()