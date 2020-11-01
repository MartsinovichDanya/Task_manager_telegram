from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardRemove

from datetime import datetime

from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel
from keyboards import create_employee_boss_keyboard
from keyboards import create_main_employee_keyboard
from keyboards import create_tasks_in_project_boss_keyboard
from keyboards import create_report_boss_keyboard
from keyboards import create_report_projects_boss_keyboard, create_report_employee_boss_keyboard
from keyboards import create_report_task_boss_keyboard

from commands import add_project, add_task, add_employee, delete_project, delete_task, delete_employee, set_done
from commands import all_task_report, emp_report, proj_report

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist, TaskNotFound

import requests

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'Task_manager_telegram.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN2')


# Приветствие
def start(bot, update):
    update.message.reply_text('<b>Это бот по юридической помощи</b>', parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))


# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()