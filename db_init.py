from Models import UserModel, TaskModel, ProjectModel, EmployeeModel
from DB import DB


def init_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    um.init_table()
    um.insert(394406731, 'Danya')
    um.insert(1027909953, 'Maksim', boss=True)
    um.insert(102790995, 'Maksik loh')

    pm = ProjectModel(db.get_connection())
    pm.init_table()
    pm.insert('TEST')
    pm.insert('TEST1')

    tm = TaskModel(db.get_connection())
    tm.init_table()
    tm.insert('test_1', 'tttteeeessssttt', 394406731, pm.get_id('TEST'))
    tm.insert('test_2', 'ttsdfsdfsdfsftteeeessssttt', 394406731, pm.get_id('TEST1'))

    em = EmployeeModel(db.get_connection())
    em.init_table()
    em.insert(394406731, 'Danya', str(pm.get_id('TEST')))
    em.insert(102790995, 'Maksik loh', str(pm.get_id('TEST')))


init_tm_db()
