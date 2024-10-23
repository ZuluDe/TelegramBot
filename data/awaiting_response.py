import sqlite3

async def update_awaiting_response(owner_id, other_id):
    connection = sqlite3.connect('data_base.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM awaiting_response WHERE owner_id = ?', (owner_id,))
    existing_row = cursor.fetchone()

    if existing_row is None:
        cursor.execute('INSERT INTO awaiting_response (owner_id, liked_id) VALUES (?, ?)', (owner_id, other_id))
    else:
        liked_ids = existing_row[1]

        if liked_ids is None or liked_ids == '':
            cursor.execute('UPDATE awaiting_response SET liked_id = ? WHERE owner_id = ?', (other_id, owner_id))
        else:
            new_liked_ids = f'{liked_ids},{other_id}'
            cursor.execute('UPDATE awaiting_response SET liked_id = ? WHERE owner_id = ?', (new_liked_ids, owner_id))


    connection.commit()
    connection.close()


async def find_and_extract(owner_id_to_find):
    connection = sqlite3.connect('data_base.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM awaiting_response WHERE owner_id = ?', (owner_id_to_find,))
    existing_row = cursor.fetchone()

    result_array = []

    if existing_row is not None:
        disliked_ids_str = existing_row[1]


        if disliked_ids_str is not None and disliked_ids_str != '':
            result_array = disliked_ids_str.split(',')

    connection.commit()

    cursor.execute("DELETE FROM awaiting_response WHERE owner_id = ?", (owner_id_to_find,))

    connection.commit()

    connection.close()

    return result_array
