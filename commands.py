from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist, TaskNotFound

db = DB('tm.db')

# boss functions


def add_project(name):
    pm = ProjectModel(db.get_connection())
    if pm.get_id(name):
        raise ProjectAlreadyExist
    else:
        pm.insert(name)


def add_task(bot, name, description, emp_name, project_name):
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tm = TaskModel(db.get_connection())
    emp_id = em.get_id(emp_name)
    if not emp_id:
        raise UserNotFound
    proj_id = pm.get_id(project_name)
    if not proj_id:
        raise ProjectNotFound
    tm.insert(name, description, emp_id, proj_id)
    em.add_project(emp_id, pm.get_id(project_name))
    bot.sendMessage(emp_id, f'''
<b><u>Проект:</u> {project_name}
<u>Задача:</u> {name}
<u>Описание задачи:</u> {description}</b>''', parse_mode='HTML')


def add_employee(name, eid):
    um = UserModel(db.get_connection())
    if um.get(eid):
        raise UserAlreadyExist
    else:
        um.insert(eid, name)
        em = EmployeeModel(db.get_connection())
        em.auto_update()


def delete_project(name):
    pm = ProjectModel(db.get_connection())
    pid = pm.get_id(name)
    pm.delete(pid)

    tm = TaskModel(db.get_connection())
    tm.delete_by_project(pid)


def delete_task(project_name, task_name):
    pm = ProjectModel(db.get_connection())
    pid = pm.get_id(project_name)

    tm = TaskModel(db.get_connection())
    tm.delete(pid, task_name)


def delete_employee(name):
    em = EmployeeModel(db.get_connection())
    uid = em.get_id(name)
    em.delete(uid)

    um = UserModel(db.get_connection())
    um.delete(uid)

    tm = TaskModel(db.get_connection())
    tm.delete_by_emp(uid)


# employee functions


def set_done(bot, name, project):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    project_id = pm.get_id(project)
    tid = tm.search(name, project_id)
    if tid:
        tm.set_done(tid)
    else:
        raise TaskNotFound
