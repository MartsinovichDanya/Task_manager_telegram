from Models_kpz import InnModel, KpzTaskModel, FileModel
from DB import DB


def init_kpz_db():
    db = DB('kpz.db')
    um = InnModel(db.get_connection())
    um.init_table()
    ktm = KpzTaskModel(db.get_connection())
    ktm.init_table()
    fm = FileModel(db.get_connection())
    fm.init_table()


init_kpz_db()
