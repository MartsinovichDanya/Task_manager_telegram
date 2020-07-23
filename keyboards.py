from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel


# Клавиатура Босса
def create_boss_keyboard1():
    boss_reply_keyboard1 = [['Просмотр по проектам', 'Просмотр по сотрудникам', 'Редактирование']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_boss_keyboard2():
    boss_reply_keyboard2 = [['Добавить проект', 'Добавить задачу', 'Добавить сотрудника'],
                            ['Удалить проект', 'Удалить задачу', 'Удалить сотрудника']]
    boss_markup2 = ReplyKeyboardMarkup(boss_reply_keyboard2, one_time_keyboard=False)
    return boss_markup2


def create_boss_keyboard3(db):
    pm = ProjectModel(db.get_connection())
    projects = [el[1] for el in pm.get_all()]
    boss_reply_keyboard3 = [projects]
    boss_markup3 = ReplyKeyboardMarkup(boss_reply_keyboard3, one_time_keyboard=False)
    return boss_markup3


# Клавиатура сотрудника
def create_employee_keyboard1():
    employee_reply_keyboard1 = [['Просмотр задач']]
    employee_markup1 = ReplyKeyboardMarkup(employee_reply_keyboard1, one_time_keyboard=False)
    return employee_markup1


def create_employee_keyboard2():
    employee_reply_keyboard2 = [['Задача1', 'Задача2', 'Задача3']]
    employee_markup2 = ReplyKeyboardMarkup(employee_reply_keyboard2, one_time_keyboard=False)
    return employee_markup2


def create_employee_keyboard3():
    employee_reply_keyboard2 = [['Выполнено']]
    employee_markup2 = ReplyKeyboardMarkup(employee_reply_keyboard2, one_time_keyboard=False)
    return employee_markup2