from Models import UserModel, TaskModel, ProjectModel, EmployeeModel
from DB import DB


def view_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    print(um.get_all())

    print('-----------------------------------------------')

    pm = ProjectModel(db.get_connection())
    print(pm.get_all())

    print('-----------------------------------------------')

    em = EmployeeModel(db.get_connection())
    print(em.get_all())

    print('-----------------------------------------------')

    tm = TaskModel(db.get_connection())
    print(tm.get_all())


view_tm_db()
