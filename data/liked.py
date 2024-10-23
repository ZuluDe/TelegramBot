import sqlite3


async def reciprocity(state):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    data = await state.get_data()
    owner_id = data.get("id_user")
    other_id = data.get("id_other")

    cur.execute("SELECT * FROM user_ratings WHERE owner_id = ? AND liked_id LIKE ?",
                (owner_id, f'%{other_id}%'))
    result_id1 = cur.fetchone()

    cur.execute("SELECT * FROM user_ratings WHERE owner_id = ? AND liked_id LIKE ?",
                (other_id, f'%{owner_id}%'))
    result_id2 = cur.fetchone()

    db.close()

    if result_id1 and result_id2:
        return owner_id, other_id
    else:
        return None



async def assess_profile_like(state):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    data = await state.get_data()
    owner_id = data.get("id_user")
    other_id = data.get("id_other")

    cur.execute("SELECT * FROM user_ratings WHERE owner_id = ?", (owner_id,))
    existing_record = cur.fetchone()

    if existing_record is None:
        cur.execute("INSERT INTO user_ratings (owner_id, liked_id) VALUES (?, ?)", (owner_id, other_id))
    else:
        liked_ids = existing_record[1]
        liked_ids_str = liked_ids + ',' + other_id if liked_ids else other_id
        cur.execute("UPDATE user_ratings SET liked_id = ? WHERE owner_id = ?", (liked_ids_str, owner_id))

    db.commit()
    db.close()


async def asses_profile_dislike(state):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    data = await state.get_data()
    owner_id = data.get("id_user")
    other_id = data.get("id_other")

    cur.execute("SELECT * FROM user_ratings WHERE owner_id = ?", (owner_id,))
    existing_record = cur.fetchone()

    if existing_record is None:
        cur.execute("INSERT INTO user_ratings (owner_id, disliked_id) VALUES (?, ?)", (owner_id, other_id))
    else:
        disliked_ids = existing_record[1]
        disliked_ids_str = disliked_ids + ',' + other_id if disliked_ids else other_id
        cur.execute("UPDATE user_ratings SET disliked_id = ? WHERE owner_id = ?", (disliked_ids_str, owner_id))

    db.commit()
    db.close()
