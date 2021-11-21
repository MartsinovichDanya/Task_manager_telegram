from Models import UserModel, TaskModel, ProjectModel, EmployeeModel, ReportModel
from DB import DB


def view_tm_db():
    db = DB('tm.db')
    um = UserModel(db.get_connection())
    print('Пользователи: ', um.get_all())

    print('-----------------------------------------------')

    pm = ProjectModel(db.get_connection())
    print('Проекты: ', pm.get_all())

    print('-----------------------------------------------')

    em = EmployeeModel(db.get_connection())
    print('Сотрудники: ', em.get_all())

    print('-----------------------------------------------')

    tm = TaskModel(db.get_connection())
    print('Задачи: ', tm.get_all())


def view_rdb():
    rdb = DB('reports.db')
    rm = ReportModel(rdb.get_connection())
    print(rm.get_all())


view_tm_db()
view_rdb()