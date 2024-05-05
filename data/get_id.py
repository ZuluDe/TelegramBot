import sqlite3


async def user_id_in_table(user_id):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    sql_query = f"SELECT COUNT(*) FROM users WHERE id_u = '{user_id}'"
    cur.execute(sql_query)

    result = cur.fetchone()[0]

    db.commit()
    db.close()

    if result > 0:
        return True
    return False
    