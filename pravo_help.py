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

from keyboards import create_main_pravo_help_keyboard, create_payment_pravo_help_keyboard, create_menu_keyboard
from Models_kpz import InnModel
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'Task_manager_telegram.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN2')
db = DB('kpz.db')
is_juristic = False


# Приветствие
def start(bot, update):
    update.message.reply_text('<b>Выберите раздел "Консультация", если хотите рассказать о проблеме и задать вопрос, или раздел "Оплата", чтобы оплатить за ранее оказанную помощь</b>',
                              reply_markup=create_main_pravo_help_keyboard(), parse_mode='HTML')


# Раздел "Оплата"
def payment(bot, update):
    update.message.reply_text('<b>Выберите способ оплаты</b>', reply_markup=create_payment_pravo_help_keyboard(),
                              parse_mode='HTML')


# Раздел "Оплата" (Выставить счёт (юр. лицо))
def juristic_person(bot, update):
    global is_juristic
    is_juristic = True
    update.message.reply_text('<b>Напишите свой ИНН (ОГРН)</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Раздел "Оплата" (Оплата картой (физ. лицо))
def natural_person(bot, update):
    update.message.reply_text('<b>Переходим к "РобоКассе"</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Раздел "Консультация"
def consultation(bot, update):
    update.message.reply_text('<b>Опишите проблему и задайте вопрос</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Глобальная функция
def global_function(bot, update):
    global is_juristic

    if is_juristic:
        is_juristic = False
        inn = update.message.text
        im = InnModel(db.get_connection())
        im.insert(inn)
        update.message.reply_text('<b>ИНН записан</b>', reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.regex('Главное меню'), start))

dp.add_handler(MessageHandler(Filters.regex('Оплата картой для физ.лиц'), natural_person))
dp.add_handler(MessageHandler(Filters.regex('Выставить счёт для юр.лиц'), juristic_person))
dp.add_handler(MessageHandler(Filters.regex('Оплата'), payment))

dp.add_handler(MessageHandler(Filters.regex('Консультация'), consultation))

text_handler = MessageHandler(Filters.text, global_function)
# Регистрируем обработчик в диспетчере.
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
