from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardRemove

from datetime import datetime

from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel, ReportModel
from Models_kpz import InnModel, KpzTaskModel, FileModel

from keyboards import create_main_boss_keyboard, create_projects_boss_keyboard
from keyboards import create_menu_keyboard, create_project_options_boss_keyboard
from keyboards import create_employee_options_boss_keyboard, create_task_options_boss_keyboard
from keyboards import create_employee_boss_keyboard, create_cad_reports_employee_keyboard
from keyboards import create_main_employee_keyboard, create_tasks_employee_keyboard
from keyboards import create_tasks_in_project_boss_keyboard
from keyboards import create_report_boss_keyboard
from keyboards import create_report_projects_boss_keyboard, create_report_employee_boss_keyboard
from keyboards import create_report_task_boss_keyboard, create_kpz_boss_keyboard, create_cadastral_options_boss_keyboard
from keyboards import create_comment_employee_keyboard, create_cad_reports_boss_keyboard
from keyboards import create_cadastral_options_employee_keyboard

from commands import add_project, add_task, add_employee, delete_project, delete_task, delete_employee, set_done
from commands import all_task_report, emp_report, proj_report, get_uniq_filename, prepare_report_msg

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist, TaskNotFound

import os
from dotenv import load_dotenv
import json


dotenv_path = os.path.join(os.path.dirname(__file__), 'Task_manager_telegram.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN')
KPZ_FILES_DIR = 'kpz_files'
JSON_REPORTS_DIR = 'cad_reports'

db = DB('tm.db')
rdb = DB('reports.db')

is_add_project = False
is_add_task = False
is_add_employee = False
is_delete_project = False
is_delete_task = False
is_delete_employee = False
is_task_selected = False
is_time_selected = False
is_proj_add_task = False
is_proj_delete_task = False

is_report = False
is_report_proj = False
is_report_employee = False

is_select_cad_report = False
is_employee_select_cad_report = False
is_cad_report_assign_employee = False
is_comment_cad_report = False

latest_project = ''
l_d = 0
r_d = 0
task = ''
cad_report_id = 0


# Приветствие
def start(bot, update):
    global is_add_project, is_add_task, is_add_employee, is_delete_project, is_delete_task, is_delete_employee
    global is_proj_add_task, is_proj_delete_task, is_report_proj, is_report_employee
    global is_report, is_task_selected, is_time_selected, is_select_cad_report, is_cad_report_assign_employee
    global is_employee_select_cad_report, is_comment_cad_report

    is_add_project = False
    is_add_task = False
    is_add_employee = False
    is_delete_project = False
    is_delete_task = False
    is_delete_employee = False
    is_task_selected = False
    is_time_selected = False
    is_proj_add_task = False
    is_proj_delete_task = False

    is_report = False
    is_report_proj = False
    is_report_employee = False

    is_select_cad_report = False
    is_employee_select_cad_report = False
    is_cad_report_assign_employee = False
    is_comment_cad_report = False

    um = UserModel(db.get_connection())
    tg_id = update.message.from_user.id
    print(update.message['chat']['username'])
    # Левый чувак
    if not um.get(tg_id):
        update.message.reply_text(f'<b>Вас нет в нашей базе данных.\nВаш ID: {tg_id}</b>', reply_markup=ReplyKeyboardRemove(),
                                  parse_mode='HTML')
    # Босс
    elif um.get(tg_id)[2]:
        update.message.reply_text('<b>Добро пожаловать, Лидер команды!</b>', reply_markup=create_main_boss_keyboard(),
                                  parse_mode='HTML')
    # Сотрудник
    else:
        update.message.reply_text('<b>Добро пожаловать!</b>', reply_markup=create_main_employee_keyboard(), parse_mode='HTML')


# Раздел "Отчёты"
def back_to_report(bot, update):
    update.message.reply_text('<i><b>Выберите тип отчёта</b></i>', reply_markup=create_report_employee_boss_keyboard(),
                              parse_mode='HTML')


def report(bot, update):
    global is_report
    is_report = True

    update.message.reply_text('''
<b>Раздел "Отчёты"
Напишите временной промежуток.
Пример: дд.мм.гггг-дд.мм.гггг</b>''', reply_markup=create_report_boss_keyboard(),
                              parse_mode='HTML')


def project_report(bot, update):
    global is_report_proj
    is_report_proj = True
    update.message.reply_text('<b>Раздел "Отчёты по Проектам"</b>', reply_markup=create_report_projects_boss_keyboard(db),
                              parse_mode='HTML')


def employee_report(bot, update):
    global is_report_employee
    is_report_employee = True
    update.message.reply_text('<b>Раздел "Отчёты по Сотрудникам"</b>', reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


def task_report(bot, update):
    update.message.reply_text('<b>Раздел "Отчёты по Задачам"</b>', reply_markup=create_report_task_boss_keyboard(),
                              parse_mode='HTML')
    all_task_report(update, l_d, r_d)


# Главное меню
def project_options(bot, update):
    update.message.reply_text('<b>Раздел "Проекты"</b>', reply_markup=create_project_options_boss_keyboard(),
                              parse_mode='HTML')


def employee_options(bot, update):
    update.message.reply_text('<b>Раздел "Сотрудники"</b>', reply_markup=create_employee_options_boss_keyboard(),
                              parse_mode='HTML')


def task_options(bot, update):
    update.message.reply_text('<b>Раздел "Задачи"</b>', reply_markup=create_task_options_boss_keyboard(),
                              parse_mode='HTML')


# Выбор проекта/сотрудника
def select_project(bot, update):
    update.message.reply_text('<b>Выберите проект из предложенного списка</b>',
                              reply_markup=create_projects_boss_keyboard(db),
                              parse_mode='HTML')


def select_employee(bot, update):
    update.message.reply_text('<b>Выберите сотрудника из предложенного списка</b>',
                              reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


# Просмотр
def project_preview(update, project):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    tasks = sorted(tm.get_by_project(pm.get_id(project)), key=lambda t: t[5])

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача: <u>{task[1]}</u></b>
<b>Описание:</b> {task[2]}
<b>Исполнитель:</b> {em.get(task[3])[1]}
<b>Время выполнения: {'-' if not task[5] else task[8]}</b> 
<b>Статус: {'Выполнена' if task[5] else 'В процессе'}</b>
''', reply_markup=create_tasks_in_project_boss_keyboard(), parse_mode='HTML')


def employee_preview(update, employee):
    tm = TaskModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    eid = em.get_id(employee)
    tasks = sorted(tm.get_by_emp(eid), key=lambda t: t[5])

    for task in tasks:
        update.message.reply_text(f'''
<b>Проект: <u>{pm.get_name(task[4])}</u></b>
<b>Задача: {task[1]}</b>
<b>Описание:</b> {task[2]}
<b>Время выполнения: {'-' if not task[5] else task[8]}</b>
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


def task_preview(bot, update):
    tm = TaskModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tasks = sorted(tm.get_all(), key=lambda t: t[5])

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача: <u>{task[1]}</u></b>
<b>Проект: {pm.get_name(task[4])}</b>
<b>Описание: {task[2]}</b>
<b>Сотрудник: {em.get(task[3])[1]}</b>
<b>Время выполнения: {'-' if not task[5] else task[8]}</b>
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


# Проекты
def write_add_project(bot, update):
    global is_add_project
    is_add_project = True
    update.message.reply_text(
        '<i><b>Напишите название проекта.\nЗапрещаются специальные символы: !, `, @, №, $, %, &, ?, /, :, ;</b></i>',
        reply_markup=create_menu_keyboard(),
        parse_mode='HTML')


def write_delete_project(bot, update):
    global is_delete_project
    is_delete_project = True
    update.message.reply_text('<i><b>Напишите название проекта, который Вы хотели бы удалить</b></i>',
                              reply_markup=create_projects_boss_keyboard(db),
                              parse_mode='HTML')


# Задачи
def write_add_task(bot, update):
    global is_add_task
    is_add_task = True
    update.message.reply_text('<i><b>Используйте ";" для разделения требуемых параметров</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text('''
<i><b>Напишите название задачи, описание, имя сотрудника, название проекта.
Пример: задача1;описание1;имя1;проект1</b></i>''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


def write_delete_task(bot, update):
    global is_delete_task
    is_delete_task = True
    update.message.reply_text('<i><b>Напишите название проекта и название задачи</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Задачи в проекте
def write_proj_add_task(bot, update):
    global is_proj_add_task, is_add_task
    is_proj_add_task, is_add_task = True, True
    update.message.reply_text('<i><b>Используйте ";" для разделения требуемых параметров</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text('''
<i><b>Напишите название задачи, описание задачи, имя сотрудника.
Пример: задача1;описание1;имя1</b></i>''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


def write_proj_delete_task(bot, update):
    global is_proj_delete_task, is_delete_task
    is_proj_delete_task, is_delete_task = True, True
    update.message.reply_text('<i><b>Напишите название задачи, которую Вы хотели бы удалить в данном проекте</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Сотрудники
def write_add_employee(bot, update):
    global is_add_employee
    is_add_employee = True
    update.message.reply_text('<i><b>Используйте ";" для разделения требуемых параметров</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text('<i><b>Напишите имя и ID сотрудника.\nПример: имя1;0123456789</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


def write_delete_employee(bot, update):
    global is_delete_employee
    is_delete_employee = True
    update.message.reply_text('<i><b>Напишите имя сотрудника, которого Вы хотели бы удалить</b></i>',
                              reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


# Глобальная функция
def global_function(bot, update):
    # Отправляем http запрос
    global is_add_project, is_add_task, is_add_employee, is_delete_project, is_delete_task, is_delete_employee
    global projects_list, employee_list
    global latest_project, is_proj_add_task, is_proj_delete_task
    global is_report, is_report_employee, is_report_proj, r_d, l_d, task
    global is_time_selected, is_task_selected
    global is_select_cad_report, is_cad_report_assign_employee
    global is_employee_select_cad_report, is_comment_cad_repor, cad_report_id

    update.message.reply_text('<i><b>Команда выполнена</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    if update.message['text'].isdigit() and (is_select_cad_report or is_employee_select_cad_report):
        cad_report_id = int(update.message['text'])
        rm = ReportModel(rdb.get_connection())
        report_metadata = rm.get(cad_report_id)
        report_file_name = report_metadata[1]

        with open(os.path.join(JSON_REPORTS_DIR, report_file_name), 'r') as rep_f:
            full_report = json.load(rep_f)

        msg = prepare_report_msg(report_metadata[7], full_report)
        if is_select_cad_report:
            update.message.reply_text(msg, reply_markup=create_cadastral_options_boss_keyboard(),
                                  parse_mode='HTML')
        else:
            update.message.reply_text(msg, reply_markup=create_cadastral_options_employee_keyboard(),
                                      parse_mode='HTML')

    elif update.message['text'] in projects_list and not is_delete_project and not is_add_task and not is_add_project:
        project = update.message['text']

        if is_report_proj:
            proj_report(update, l_d, r_d, project)
        else:
            update.message.reply_text(f"<i><b>Просмотр задач по проекту: {project}</b></i>",
                                      reply_markup=create_tasks_in_project_boss_keyboard(), parse_mode='HTML')
            project_preview(update, project)
            latest_project = update.message['text']

    elif update.message['text'] in employee_list and not is_delete_employee:
        employee = update.message['text']

        if is_report_employee:
            emp_report(update, l_d, r_d, employee)
        elif is_cad_report_assign_employee:
            is_cad_report_assign_employee = False
            rm = ReportModel(rdb.get_connection())
            rm.set_assignee(cad_report_id, employee)
            update.message.reply_text('<i><b>Отчёт назначен</b></i>',
                                      reply_markup=create_menu_keyboard(),
                                      parse_mode='HTML')
            em = EmployeeModel(db.get_connection())
            emp_id = em.get_id(employee)
            report_data = rm.get(cad_report_id)
            bot.sendMessage(emp_id, f'''
У Вас новый кадастровый отчёт
<b>Кад. номер: </b>{report_data[2]}
<b>Адрес: </b>{report_data[3]}''', parse_mode='HTML')

        else:
            update.message.reply_text(f"<i><b>Просмотр задач сотрудника: {employee}</b></i>",
                                      reply_markup=create_tasks_in_project_boss_keyboard(), parse_mode='HTML')
            employee_preview(update, employee)

    elif is_add_project:
        is_add_project = False
        name = update.message['text']
        projects_list.append(name)
        try:
            add_project(name)
        except ProjectAlreadyExist:
            update.message.reply_text("Проект уже существует")
            is_add_project = True

    elif is_add_task:
        is_add_task = False
        if is_proj_add_task:
            is_proj_add_task = False
            params = update.message['text']
            name, description, emp_name = params.split(';')
            project_name = latest_project
        else:
            params = update.message['text']
            name, description, emp_name, project_name = params.split(';')

        try:
            add_task(bot, name, description, emp_name, project_name, '@'+update.message['chat']['username'])
        except ProjectNotFound:
            update.message.reply_text("Проект не найден")
            is_add_task = True
        except UserNotFound:
            update.message.reply_text("Сотрудник не найден")
            is_add_task = True

    elif is_add_employee:
        is_add_employee = False
        params = update.message['text']
        name, uid = params.split(';')
        try:
            add_employee(name, uid)
            employee_list.append(name)
        except UserAlreadyExist:
            update.message.reply_text("Пользователь уже существует")
            is_add_employee = True

    elif is_delete_project:
        is_delete_project = False
        name = update.message['text']
        delete_project(name)
        del projects_list[projects_list.index(name)]

    elif is_delete_task:
        is_delete_task = False
        if is_proj_delete_task:
            is_proj_delete_task = False
            task_name = update.message['text']
            project_name = latest_project
        else:
            params = update.message['text']
            project_name, task_name = params.split(';')
        delete_task(project_name, task_name)

    elif is_delete_employee:
        is_delete_employee = False
        name = update.message['text']
        delete_employee(name)
        del employee_list[employee_list.index(name)]

    elif is_task_selected:
        is_task_selected = False
        task = update.message['text']
        update.message.reply_text('<i><b>Введите время выполнения задачи.\nПример: 2:45, 3:00, 1:30.\nВАЖНО! Целое количество часов вводится также через двоеточние (1, 2, 3 часа будут записаны в виде "1:00", "2:00", "3:00" и т.д.)</b></i>', parse_mode='HTML')
        is_time_selected = True

    elif is_time_selected:
        is_time_selected = False
        time = update.message['text']
        hours, minutes = time.split(':')
        if not hours.isdigit() or not minutes.isdigit():
            is_time_selected = True
            update.message.reply_text("<i><b>Введено некорректное значение времени</b></i>", parse_mode='HTML')
        else:
            project, name = task.split(': ')
            set_done(bot, name, project, time)

    elif is_report:
        is_report = False
        update.message.reply_text('<i><b>Выберите тип отчёта</b></i>', reply_markup=create_report_employee_boss_keyboard(),
                                  parse_mode='HTML')
        l_string, r_string = update.message['text'].split('-')
        l_day, l_month, l_year = [int(el) for el in l_string.split('.')]
        r_day, r_month, r_year = [int(el) for el in r_string.split('.')]
        try:
            l_d = datetime.toordinal(datetime(l_year, l_month, l_day))
            r_d = datetime.toordinal(datetime(r_year, r_month, r_day))
        except ValueError:
            update.message.reply_text('<i><b>Некорректно введена дата</b></i>',
                                      reply_markup=create_menu_keyboard(),
                                      parse_mode='HTML')
            report(bot, update)

    elif is_comment_cad_report:
        is_comment_cad_report = False
        comment = update.message['text']
        rm = ReportModel(rdb.get_connection())
        rm.close(cad_report_id, comment)
        update.message.reply_text('<i><b>Отчёт закрыт</b></i>',
                                  reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')
        um = UserModel(db.get_connection())
        boss_id = um.get_boss_id()
        report_data = rm.get(cad_report_id)
        bot.sendMessage(boss_id, f'''
{report_data[4]} оставил(а) комментарий к кад. отчету {report_data[0]}
<b>Кад. номер: </b>{report_data[2]}
<b>Адрес: </b>{report_data[3]}
<b>Комментарий : </b>{comment}''', parse_mode='HTML')


# Часть сотрудника нахрен
def select_done_task(bot, update):
    global is_task_selected
    is_task_selected = True

    update.message.reply_text('<i><b>Выберите задачу</b></i>', reply_markup=create_tasks_employee_keyboard(db, update.message.from_user.id),
                              parse_mode='HTML')


def employee_task_preview(bot, update):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tasks = (task for task in tm.get_by_emp(update.message.from_user.id) if not task[5])

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача: <u>{task[1]}</u></b>
<b>Описание:</b> {task[2]}
<b>Проект: {pm.get_name(task[4])}</b>
<b>Контакты Лидера Команды: {task[7]}</b>
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''',
                                  reply_markup=create_main_employee_keyboard(), parse_mode='HTML')


def employee_cadastral_objects_preview(bot, update):
    global is_employee_select_cad_report
    is_employee_select_cad_report = True

    rm = ReportModel(rdb.get_connection())
    um = UserModel(db.get_connection())
    username = um.get(update.message.from_user.id)[1]
    cad_reports = rm.get_by_assignee(username)

    for cad_report in cad_reports:
        update.message.reply_text(f'''
<b><i>Запрос {cad_report[0]}</i></b>
<b>Клиент: </b>@{cad_report[7]}
<b>Кад. номер: </b>{cad_report[2]}
<b>Адрес: </b>{cad_report[3]}
<b>Комментарий: </b>{cad_report[5] if cad_report[5] else '-'}
<b>Дата закрытия: </b>{cad_report[6] if cad_report[6]!='2222-01-01' else 'Открыт'}
''', reply_markup=create_cad_reports_employee_keyboard(rdb, username),
              parse_mode='HTML')


def employee_write_cadastral_comment(bot, update):
    global is_comment_cad_report
    is_comment_cad_report = True
    update.message.reply_text('<i><b>Напишите по выбранному отчёту комментарий длиной до 4096 символов</b></i>',
                              reply_markup=create_kpz_boss_keyboard(),
                              parse_mode='HTML')


# КЫ ПЫ ЗЫ нахрен блын
def kpz(bot, update):
    update.message.reply_text('<i><b>Выберите раздел</b></i>',
                              reply_markup=create_kpz_boss_keyboard(),
                              parse_mode='HTML')


# Просмотр ИНН
def kpz_inn_preview(bot, update):
    # if len(update.message['text']) > 3:
    #     global_function(bot, update)
    #     return
    update.message.reply_text('<i><b>Здесь выводятся ИНН</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    kpz_db = DB('kpz.db')
    im = InnModel(kpz_db.get_connection())
    for inn in im.get_all():
        update.message.reply_text(f'''
<i><b>ИНН: {inn[1]}</b></i>
<i><b>Контакты Заказчика: {inn[2]}</b></i>''',
                                  reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')


# Просмотр юр. вопросов
def kpz_juristic_questions(bot, update):
    update.message.reply_text('<i><b>Здесь выводятся вопросы</b></i>',
                              parse_mode='HTML')

    kpz_db = DB('kpz.db')
    ktm = KpzTaskModel(kpz_db.get_connection())
    fm = FileModel(kpz_db.get_connection())
    for task in ktm.get_all():
        update.message.reply_text(f'''
<b>Юридический вопрос: <u>{task[1]}</u></b>\n
<b>Контакты Заказчика: {task[3]}</b>
<b>Файл:</b> {'Не прикреплен' if task[4] == -1 else '↓'}''',
                                  reply_markup=create_menu_keyboard(), parse_mode='HTML')
        try:
            new_file_name = get_uniq_filename(fm.get(task[4])[2], task[3][1:])
            tg_doc = open(os.path.join(os.getcwd(), KPZ_FILES_DIR, new_file_name), 'rb')
            update.message.reply_document(tg_doc, filename=new_file_name,
                                          reply_markup=create_menu_keyboard())
        except Exception as e:
            print('kpz_juristic_questions', e)


# Просмотр Кадастровых Объектов
def kpz_cadastral_object_preview(bot, update):
    global is_select_cad_report
    is_select_cad_report = True

    rm = ReportModel(rdb.get_connection())
    cad_reports = rm.get_all()

    for cad_report in cad_reports:
        update.message.reply_text(f'''
<b><i>Запрос {cad_report[0]}</i></b>
<b>Клиент: </b>@{cad_report[7]}
<b>Кад. номер: </b>{cad_report[2]}
<b>Адрес: </b>{cad_report[3]}
<b>Комментарий: </b>{cad_report[5] if cad_report[5] else '-'}
<b>Ответственный: </b>{cad_report[4] if cad_report[4] else '-'}
<b>Дата закрытия: </b>{cad_report[6] if cad_report[6]!='2222-01-01' else 'Открыт'}
''', reply_markup=create_cad_reports_boss_keyboard(rdb),
                  parse_mode='HTML')


# Просмотр Кадастровых Объектов
def kpz_cadastral_object_options(bot, update):
    update.message.reply_text('<i><b>Выберите действие</b></i>',
                              reply_markup=create_cadastral_options_boss_keyboard(),
                              parse_mode='HTML')


# Удаление Кадастрового Объекта
def kpz_delete_cadastral_object(bot, update):
    rm = ReportModel(rdb.get_connection())
    rm.delete(cad_report_id)
    update.message.reply_text('<i><b>Отчёт удалён</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')

# Назначение Кадастрового Объекта Сотруднику
def kpz_share_cadastral_object(bot, update):
    global is_cad_report_assign_employee
    is_cad_report_assign_employee = True
    update.message.reply_text('<i><b>Выберите сотрудника</b></i>',
                              reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))


# Клавиатура Босса
dp.add_handler(MessageHandler(Filters.regex('Добавить задачу в проект'), write_proj_add_task))
dp.add_handler(MessageHandler(Filters.regex('Удалить задачу из проекта'), write_proj_delete_task))

dp.add_handler(MessageHandler(Filters.regex('Проекты'), project_options))
dp.add_handler(MessageHandler(Filters.regex('Задачи'), task_options))
dp.add_handler(MessageHandler(Filters.regex('Сотрудники'), employee_options))

dp.add_handler(MessageHandler(Filters.regex('Добавить проект'), write_add_project))
dp.add_handler(MessageHandler(Filters.regex('Удалить проект'), write_delete_project))
dp.add_handler(MessageHandler(Filters.regex('Просмотр проектов'), select_project))

dp.add_handler(MessageHandler(Filters.regex('Добавить задачу'), write_add_task))
dp.add_handler(MessageHandler(Filters.regex('Удалить задачу'), write_delete_task))
dp.add_handler(MessageHandler(Filters.regex('Просмотр задач'), task_preview))

dp.add_handler(MessageHandler(Filters.regex('Добавить сотрудника'), write_add_employee))
dp.add_handler(MessageHandler(Filters.regex('Удалить сотрудника'), write_delete_employee))
dp.add_handler(MessageHandler(Filters.regex('Просмотр сотрудников'), select_employee))

dp.add_handler(MessageHandler(Filters.regex('Главное меню'), start))

dp.add_handler(MessageHandler(Filters.regex('Отчёты по Проектам'), project_report))
dp.add_handler(MessageHandler(Filters.regex('Отчёты по Задачам'), task_report))
dp.add_handler(MessageHandler(Filters.regex('Отчёты по Сотрудникам'), employee_report))
dp.add_handler(MessageHandler(Filters.regex('Отчёты'), report))


dp.add_handler(MessageHandler(Filters.regex('Назад'), back_to_report))
# КПЗ от pravo_help бота
dp.add_handler(MessageHandler(Filters.regex('КПЗ'), kpz))
dp.add_handler(MessageHandler(Filters.regex('Просмотр юр. вопросов'), kpz_juristic_questions))
dp.add_handler(MessageHandler(Filters.regex('Просмотр ИНН'), kpz_inn_preview))
dp.add_handler(MessageHandler(Filters.regex('Кадастровые объекты'), kpz_cadastral_object_preview))

dp.add_handler(MessageHandler(Filters.regex('Удалить кад. объект'), start))
dp.add_handler(MessageHandler(Filters.regex('Назначить сотруднику'), kpz_share_cadastral_object))


# Клавиатура сотрудника
dp.add_handler(MessageHandler(Filters.regex('Просмотр моих задач'), employee_task_preview))
dp.add_handler(MessageHandler(Filters.regex('Просмотр кад. отчётов'), employee_cadastral_objects_preview))
dp.add_handler(MessageHandler(Filters.regex('Написать комментарий'), employee_write_cadastral_comment))
dp.add_handler(MessageHandler(Filters.regex('Выполнено'), select_done_task))

# Создаём и удаляем тестовый обработчик текстовых сообщений (команд)
projects_list = []
employee_list = []

em = EmployeeModel(db.get_connection())
for e in em.get_all():
    employee_list.append(e[1])

pm = ProjectModel(db.get_connection())
for p in pm.get_all():
    projects_list.append(p[1])

# Создаём обработчик текстовых сообщений типа Filters.text
text_handler = MessageHandler(Filters.text, global_function)
# Регистрируем обработчик в диспетчере.
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
