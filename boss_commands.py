from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

db = DB('tm.db')


def add_project(name):
    pm = ProjectModel(db.get_connection())
    pm.insert(name)


def add_task(name, description, emp_name, project_name):
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tm = TaskModel(db.get_connection())
    tm.insert(name, description, em.get_id(emp_name), pm.get_id(project_name))
    em.add_project(em.get_id(emp_name), pm.get_id(project_name))


def add_employee(name, id):
    um = UserModel(db.get_connection())
    um.insert(id, name)

    em = EmployeeModel(db.get_connection())
    em.auto_update()


def delete_project(name):
    pm = ProjectModel(db.get_connection())
    pm.delete(pm.get_id(name))


def delete_task(id):
    tm = TaskModel(db.get_connection())
    tm.delete(id)


def delete_employee(id):
    em = EmployeeModel(db.get_connection())
    em.delete(id)

    um = UserModel(db.get_connection())
    um.delete(id)
