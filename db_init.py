from Models import UserModel
from DB import DB


def init_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    um.init_table()
    um.insert('Danya', 394406731)
    um.insert('Maksim', 1027909953, boss=True)


init_tm_db()
