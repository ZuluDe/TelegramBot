import sqlite3


async def new_profile(state):
    db = sqlite3.connect('data_base.db')
    cur = db.cursor()

    data = await state.get_data()
    fields = ['id_u', 'username', 'name', 'age', 'clas', 'gender', 'about', 'photo']

    values = tuple(data.get(field, '') for field in fields)

    cur.execute(f"INSERT INTO profiles VALUES({', '.join(['?' for _ in range(len(fields))])})", values)
    cur.execute(f"INSERT INTO users VALUES('{data.get('id_u', '')}')")
    
    db.commit()
    db.close()