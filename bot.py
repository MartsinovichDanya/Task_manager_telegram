from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

from keyboards import create_main_boss_keyboard, create_edit_boss_keyboard, create_projects_boss_keyboard

db = DB('tm.db')
TOKEN = "1306952282:AAEYQicKyWmBDHGmJ-vhrgmOladw6AYpNao"

is_boss = False


def start(bot, update):
    global is_boss
    um = UserModel(db.get_connection())
    tg_id = update.message.from_user.id

    print(str(tg_id))

    # Левый чувак
    if not um.get(tg_id):
        update.message.reply_text('Вас нет в нашей базе данных.', reply_markup=ReplyKeyboardRemove())
    # Босс
    elif um.get(tg_id)[2]:
        update.message.reply_text('Добро пожаловать, Босс!', reply_markup=create_main_boss_keyboard())
        is_boss = True
    # Сотрудник
    else:
        update.message.reply_text('Добро пожаловать!', reply_markup=ReplyKeyboardRemove())


def edit(bot, update):
    update.message.reply_text('Редактирование', reply_markup=create_edit_boss_keyboard())


def project_names(bot, update):
    update.message.reply_text('<b>Список проектов:</b> 1) TEST, 2)... 3)...', reply_markup=create_projects_boss_keyboard(db), parse_mode='HTML')


def project_preview(bot, update):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    tasks = tm.get_by_project(pm.get_id('TEST'))

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача:</b><b><u>{task[1]}</u></b>
<b>Описание:</b> {task[2]}
<b>Исполнитель:</b> {em.get(task[3])[1]}
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


def employee_names(bot, update):
    update.message.reply_text('<b>Список исполнителей:</b> 1) Danya, 2)... 3)...', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


def employee_preview(bot, update):
    tm = TaskModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    tasks = tm.get_by_emp(em.get_id('Danya'))

    for task in tasks:
        update.message.reply_text(f'''
    <b>Задача:</b><b><u>{task[1]}</u></b>
    <b>Описание:</b> {task[2]}
    <b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


def callback_method(bot, update):
    update.message.reply_text('<i><b>Ю НОУ БЛИН</b></i>', reply_markup=ReplyKeyboardRemove(),
                              parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher

# Клавиатура Босса

# Клавиатура сотрудника

# обработчики для босса ю ноу блин чортомба


buttons = ['Start', 'Settings', 'Back']
markup = ReplyKeyboardMarkup.from_column(buttons)
dp.add_handler(MessageHandler(Filters.text(buttons), callback_method))

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
