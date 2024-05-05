import sqlite3

async def main():
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS profiles (
        id_u text, 
        username text,
        name text,
        age text,
        clas text,
        gender text,
        about text,
        photo text
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id_u text
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS user_ratings (
        owner_id text,
        liked_id text,
        disliked_id text
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS awaiting_response (
        owner_id text,
        liked_id text
    )""")



    db.commit()
    db.close()