from Models import UserModel
from DB import DB


def init_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    um.init_table()
    um.insert(394406731, 'Danya')
    um.insert(1027909953, 'Maxim', boss=True)


init_tm_db()
