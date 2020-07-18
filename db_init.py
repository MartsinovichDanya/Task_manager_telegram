from Models import UserModel
from DB import DB


def init_tm_db():
    db = DB('jfe.db')
    um = UserModel(db.get_connection())
    um.init_table()
    um.insert('test1', 'test1', '-')
    um.insert('test2', 'test2', '-')
    um.insert('admin', 'admin', '-', True)


init_tm_db()
