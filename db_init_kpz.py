from Models_kpz import InnModel
from DB import DB


def init_kpz_db():
    db = DB('kpz.db')
    um = InnModel(db.get_connection())
    um.init_table()


init_kpz_db()
