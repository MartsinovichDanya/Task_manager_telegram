from Models_kpz import InnModel
from DB import DB


def view_kpz_db():
    db = DB('tm.db')
    um = InnModel(db.get_connection())
    print('ИНН: ', um.get_all())


view_kpz_db()
