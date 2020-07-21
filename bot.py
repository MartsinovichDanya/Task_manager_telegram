from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from DB import DB
from Models import UserModel

db = DB('tm.db')
TOKEN = "1306952282:AAEYQicKyWmBDHGmJ-vhrgmOladw6AYpNao"


def start(bot, update):
    um = UserModel(db.get_connection())
    tg_id = update.message.from_user.id

    print(str(tg_id))

    # Левый чувак
    if not um.get(tg_id):
        update.message.reply_text('Вас нет в нашей базе данных.', reply_markup=ReplyKeyboardRemove())
    # Босс
    elif um.get(tg_id)[2]:
        update.message.reply_text('Добро пожаловать, Босс!', reply_markup=boss_markup1)
    # Сотрудник
    else:
        update.message.reply_text('Добро пожаловать!', reply_markup=employee_markup)


def edit(bot, update):
    update.message.reply_text('Редактирование', reply_markup=boss_markup2)


def project_names(bot, update):
    update.message.reply_text('<b>Список проектов:</b> 1) TEST, 2)... 3)...', reply_markup=boss_markup3, parse_mode='HTML')


def project_preview(bot, update):
    update.message.reply_text('<b>Название проекта:</b> TEST', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


def employee_names(bot, update):
    update.message.reply_text('Просмотр по сотрудникам', reply_markup=ReplyKeyboardRemove())


updater = Updater(TOKEN)

dp = updater.dispatcher

# Клавиатура Босса
boss_reply_keyboard1 = [['Просмотр по проектам', 'Просмотр по сотрудникам', 'Редактирование']]
boss_reply_keyboard2 = [['Добавить проект', 'Добавить задачу', 'Добавить сотрудника'],
                        ['Удалить проект', 'Удалить задачу', 'Удалить сотрудника']]
boss_reply_keyboard3 = [['1']]
boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
boss_markup2 = ReplyKeyboardMarkup(boss_reply_keyboard2, one_time_keyboard=False)
boss_markup3 = ReplyKeyboardMarkup(boss_reply_keyboard3, one_time_keyboard=False)

# Клавиатура сотрудника
employee_reply_keyboard1 = [['Просмотр']]
employee_reply_keyboard2 = [['Выбрать задачу']]
employee_reply_keyboard3 = [['Выполнено']]
employee_markup = ReplyKeyboardMarkup(employee_reply_keyboard1, one_time_keyboard=False)


# Регистрируем обработчик команды "start" в диспетчере
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.regex('Редактирование'), edit))
dp.add_handler(MessageHandler(Filters.regex('Просмотр по проектам'), project_names))
dp.add_handler(MessageHandler(Filters.regex('Просмотр по сотрудникам'), employee_names))
dp.add_handler(MessageHandler(Filters.regex('1'), project_preview))

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()





