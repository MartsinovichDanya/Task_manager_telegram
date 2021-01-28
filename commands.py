from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist, TaskNotFound

from keyboards import create_back_to_reports_keyboard

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import os
from dotenv import load_dotenv


db = DB('tm.db')

# boss functions


def add_project(name):
    pm = ProjectModel(db.get_connection())
    if pm.get_id(name):
        raise ProjectAlreadyExist
    else:
        pm.insert(name)


def add_task(bot, name, description, emp_name, project_name, boss_link):
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tm = TaskModel(db.get_connection())
    emp_id = em.get_id(emp_name)
    if not emp_id:
        raise UserNotFound
    proj_id = pm.get_id(project_name)
    if not proj_id:
        raise ProjectNotFound
    tm.insert(name, description, emp_id, proj_id, boss_link, 0)
    em.add_project(emp_id, pm.get_id(project_name))
    bot.sendMessage(emp_id, f'''
У Вас новая задача
<b><u>Проект:</u> {project_name}
<u>Задача:</u> {name}
<u>Описание задачи:</u> {description}
<u>Контакты Лидера Команды:</u> {boss_link}</b>''', parse_mode='HTML')


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
<b>Время выполнения: {task[8]}</b>
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
<b>Время выполнения: {task[8]}</b>
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
<b>Время выполнения: {task[8].split(':')[0]} часа(-ов) {task[8].split(':')[1]} минут</b>
<b>Статус: Выполнена</b>
<b>Дата выполнения: {'.'.join(map(str, [date.day, date.month, date.year]))}</b>''', parse_mode='HTML')

    update.message.reply_text(f'<b>Выполнено {done_task_counter} задач из {len(all_tasks)}</b>',
                              reply_markup=create_back_to_reports_keyboard(), parse_mode='HTML')


# employee functions

def set_done(bot, name, project, time):
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
        tm.set_timer(tid, time)
        task = tm.get(tid)
        bot.sendMessage(boss_id, f'''
<b>Задача выполнена
<u>Исполнитель</u>: {em.get(task[3])[1]}
<u>Проект:</u> {pm.get_name(task[4])}
<u>Задача:</u> {task[1]}
<u>Описание задачи:</u> {task[2]}
<u>Время выполнения:</u> {task[8].split(':')[0]} часа(-ов) {task[8].split(':')[1]} минут
</b>''', parse_mode='HTML')
    else:
        raise TaskNotFound


def send_email(to, text, file=None):
    dotenv_path = os.path.join(os.path.dirname(__file__), 'kpz_mail.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    url = "smtp.yandex.ru"

    msg = MIMEMultipart()
    msg['Subject'] = 'Новое задание с PravoHelpBot'
    msg['From'] = login
    msg['To'] = to
    msg.attach(MIMEText(text, 'html'))

    if file is not None:
        header = 'Content-Disposition', 'attachment; filename="%s"' % file
        attachment = MIMEBase('application', "octet-stream")
        try:
            with open(file, "rb") as fh:
                data = fh.read()

            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            attachment.add_header(*header)
            msg.attach(attachment)
        except IOError:
            print("Error opening attachment file %s" % file)

    try:
        server = smtplib.SMTP_SSL(url, 465)
        server.login(login, password)
        server.sendmail(login, to, msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


def get_uniq_filename(filename, tg_username):
    fn, fe = filename.split('.')
    new_file_name = fn + f'({tg_username})' + '.' + fe
    return new_file_name
