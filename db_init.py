from Models import UserModel, TaskModel, ProjectModel
from DB import DB


def init_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    um.init_table()
    um.insert(394406731, 'Danya')
    um.insert(1027909953, 'Maksim', boss=True)

    pm = ProjectModel(db.get_connection())
    pm.init_table()
    pm.insert('TEST')

    tm = TaskModel(db.get_connection())
    tm.init_table()
    tm.insert('test_1', 'tttteeeessssttt', 394406731, pm.get_id('TEST'))


init_tm_db()
