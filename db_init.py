from Models import UserModel, TaskModel, ProjectModel, EmployeeModel
from DB import DB


def init_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    um.init_table()
    # um.insert(394406731, 'Danya')
    um.insert(1027909953, 'Maxim')
    um.insert(1579583, 'Евгений Викторович', boss=True)
    # um.insert(60880374, 'Виталий Викторович', boss=True)

    pm = ProjectModel(db.get_connection())
    pm.init_table()

    tm = TaskModel(db.get_connection())
    tm.init_table()

    em = EmployeeModel(db.get_connection())
    em.init_table()
    em.auto_update()


init_tm_db()
