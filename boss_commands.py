from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

db = DB('tm.db')


def add_project(bot, update):
    name = ''  # получить от пользователя

    pm = ProjectModel(db.get_connection())
    pm.insert(name)


def add_task(bot, update):
    name, description = '', ''  # получить от пользователя
    emp_id, project_id = 0, 0  # получить от пользователя

    tm = TaskModel(db.get_connection())
    tm.insert(name, description, emp_id, project_id)


def add_employee(bot, update):
    name = ''  # получить от пользователя
    id = 0  # получить от пользователя

    um = UserModel(db.get_connection())
    um.insert(id, name)

    em = EmployeeModel(db.get_connection())
    em.auto_update()


def delete_project(bot, update):
    name = ''  # получить от пользователя

    pm = ProjectModel(db.get_connection())
    pm.delete(pm.get_id(name))


def delete_task(bot, update):
    id = 0  # получить от пользователя

    tm = TaskModel(db.get_connection())
    tm.delete(id)


def delete_employee(bot, update):
    id = 0  # получить от пользователя

    em = EmployeeModel(db.get_connection())
    em.delete(id)