from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist, TaskNotFound

from keyboards import create_menu_keyboard
from keyboards import create_back_to_reports_keyboard

from datetime import datetime

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
У Вас новая задача
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


# report functions
def proj_report(update, l_date, r_date, proj):
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    pid = pm.get_id(proj)

    tm = TaskModel(db.get_connection())
    all_tasks = tm.get_by_project(pid)

    done_task_counter = 0

    for task in all_tasks:
        if not task[5]:
            continue
        if l_date <= task[6] <= r_date:
            done_task_counter += 1
            date = datetime.fromordinal(task[6])
            update.message.reply_text(f'''
<b>Проект: {pm.get_name(task[4])}</b>
<b>Задача: {task[1]}</b>
<b>Описание: {task[2]}</b>
<b>Сотрудник: {em.get(task[3])[1]}</b>
<b>Статус: Выполнена</b>
<b>Дата выполнения: {'.'.join(map(str, [date.day, date.month, date.year]))}</b>''', parse_mode='HTML')

    update.message.reply_text(f'<b>Выполнено {done_task_counter} задач из {len(all_tasks)}</b>',
                              reply_markup=create_back_to_reports_keyboard(), parse_mode='HTML')


def emp_report(update, l_date, r_date, emp):
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    eid = em.get_id(emp)

    tm = TaskModel(db.get_connection())
    all_tasks = tm.get_by_emp(eid)

    done_task_counter = 0

    for task in all_tasks:
        if not task[5]:
            continue
        if l_date <= task[6] <= r_date:
            done_task_counter += 1
            date = datetime.fromordinal(task[6])
            update.message.reply_text(f'''
<b>Проект: {pm.get_name(task[4])}</b>
<b>Задача: {task[1]}</b>
<b>Описание: {task[2]}</b>
<b>Сотрудник: {em.get(task[3])[1]}</b>
<b>Статус: Выполнена</b>
<b>Дата выполнения: {'.'.join(map(str, [date.day, date.month, date.year]))}</b>''', parse_mode='HTML')

    update.message.reply_text(f'<b>Выполнено {done_task_counter} задач из {len(all_tasks)}</b>',
                              reply_markup=create_back_to_reports_keyboard(), parse_mode='HTML')


def all_task_report(update, l_date, r_date):
    em = EmployeeModel(db.get_connection())
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    all_tasks = tm.get_all()

    done_task_counter = 0

    for task in all_tasks:
        if not task[5]:
            continue
        if l_date <= task[6] <= r_date:
            done_task_counter += 1
            date = datetime.fromordinal(task[6])
            update.message.reply_text(f'''
<b>Проект: {pm.get_name(task[4])}</b>
<b>Задача: {task[1]}</b>
<b>Описание: {task[2]}</b>
<b>Сотрудник: {em.get(task[3])[1]}</b>
<b>Статус: Выполнена</b>
<b>Дата выполнения: {'.'.join(map(str, [date.day, date.month, date.year]))}</b>''', parse_mode='HTML')

    update.message.reply_text(f'<b>Выполнено {done_task_counter} задач из {len(all_tasks)}</b>',
                              reply_markup=create_back_to_reports_keyboard(), parse_mode='HTML')


# employee functions

def set_done(bot, name, project):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    um = UserModel(db.get_connection())
    em = EmployeeModel(db.get_connection())

    project_id = pm.get_id(project)
    tid = tm.search(name, project_id)
    boss_id = um.get_boss_id()

    if tid:
        tm.set_done(tid)
        tm.set_done_date(tid)
        task = tm.get(tid)
        bot.sendMessage(boss_id, f'''
<b>Задача выполнена
<u>Исполнитель</u>: {em.get(task[3])[1]}
<u>Проект:</u> {pm.get_name(task[4])}
<u>Задача:</u> {task[1]}
<u>Описание задачи:</u> {task[2]}</b>''', parse_mode='HTML')
    else:
        raise TaskNotFound
