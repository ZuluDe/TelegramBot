import sqlite3
import random


async def get_profile(user_id):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    sql_query = f"SELECT name, age, clas, gender, about, photo FROM profiles WHERE id_u = '{user_id}'"
    cur.execute(sql_query)

    result = cur.fetchone()

    db.commit()
    db.close()

    if result:
        columns = ['Имя', 'Возраст', 'Класс', 'Пол', 'О себе', 'Фото']
        user_data = dict(zip(columns, result))
        return user_data
    else:
        return None
    

async def viewed_profiles(user_id):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM user_ratings WHERE owner_id = ?", (user_id,))
    row = cur.fetchone()

    db.commit()
    db.close()

    if row:
        liked_ids_str = row[1]
        disliked_ids_str = row[2]

        liked_ids = liked_ids_str.split(',') if liked_ids_str else []
        disliked_ids = disliked_ids_str.split(',') if disliked_ids_str else []

        return liked_ids + disliked_ids
    else:
        return None

    


async def get_random_user_id(user_id):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    cur.execute("SELECT id_u FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    viewed = await viewed_profiles(user_id)

    if viewed:
        viewed.append(user_id )
    else:
        viewed = [user_id]


    user_ids = [id_u for id_u in user_ids if id_u not in viewed]

    random_user_id = random.choice(user_ids) if user_ids else None

    db.commit()
    db.close()

    return random_user_id



async def get_profile_re(user_id):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    sql_query = f"SELECT name, age, clas, gender, about, username, photo FROM profiles WHERE id_u = '{user_id}'"
    cur.execute(sql_query)

    result = cur.fetchone()

    db.commit()
    db.close()

    if result:
        columns = ['Имя', 'Возраст', 'Класс', 'Пол', 'О себе','Username в Telegram', 'Фото']
        user_data = dict(zip(columns, result))
        return user_data
    else:
        return None