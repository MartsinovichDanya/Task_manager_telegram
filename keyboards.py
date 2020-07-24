from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel


# Клавиатура Босса
def create_main_boss_keyboard():
    boss_reply_keyboard1 = [['Просмотр по проектам', 'Просмотр по сотрудникам', 'Редактирование']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_edit_boss_keyboard():
    boss_reply_keyboard2 = [['Добавить проект', 'Добавить задачу', 'Добавить сотрудника'],
                            ['Удалить проект', 'Удалить задачу', 'Удалить сотрудника']]
    boss_markup2 = ReplyKeyboardMarkup(boss_reply_keyboard2, one_time_keyboard=False)
    return boss_markup2


def create_projects_boss_keyboard(db):
    pm = ProjectModel(db.get_connection())
    projects = [el[1] for el in pm.get_all()]

    boss_reply_keyboard3 = []

    temp = []
    for p in projects:
        temp.append(p)
        if len(temp) == 4:
            boss_reply_keyboard3.append(temp)
            temp = []
    if temp:
        boss_reply_keyboard3.append(temp)

    boss_markup3 = ReplyKeyboardMarkup(boss_reply_keyboard3, one_time_keyboard=False)
    return boss_markup3


# Клавиатура сотрудника
def create_preview_employee_keyboard():
    employee_reply_keyboard1 = [['Просмотр задач']]
    employee_markup1 = ReplyKeyboardMarkup(employee_reply_keyboard1, one_time_keyboard=False)
    return employee_markup1


def create_tasks_employee_keyboard():
    employee_reply_keyboard2 = [['Задача1', 'Задача2', 'Задача3']]
    employee_markup2 = ReplyKeyboardMarkup(employee_reply_keyboard2, one_time_keyboard=False)
    return employee_markup2


def create_done_employee_keyboard():
    employee_reply_keyboard3 = [['Выполнено']]
    employee_markup3 = ReplyKeyboardMarkup(employee_reply_keyboard3, one_time_keyboard=False)
    return employee_markup3
