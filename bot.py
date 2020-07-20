# from telegram.ext import Updater, Filters
# from telegram.ext import MessageHandler, CommandHandler
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

# Access token
TOKEN = "1306952282:AAEYQicKyWmBDHGmJ-vhrgmOladw6AYpNao"
#
# reply_keyboard = [['/start'],
#                   ['/phone', '/email'],
#                   ['/close']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#
#
# # обработчик сообщений
# def echo(bot, update):
#     # у update есть поле message с текстом сообщения
#     # а также метод reply_text, который отвечает на сообщение
#     update.message.reply_text(update.message.text)
#     print(update.message.from_user.id)
#
#
# def start(bot, update):
#     print(update.message.from_user.id)
#     update.message.reply_text(
#         'Привет, я Эхо-бот. Я буду повторять за вами!',
#         reply_markup=markup
#     )
#
#
# def help(bot, update):
#     update.message.reply_text(
#         'Я пока не умею помогать... Я только ваше эхо.'
#     )
#
#
# def email(bot, update):
#     update.message.reply_text(
#         'den.martsinovich@yandex.ru'
#     )
#
#
# def phone_number(bot, update):
#     update.message.reply_text(
#         '+7(965)309-57-21'
#     )
#
#
# def close_keyboard(bot, update):
#     update.message.reply_text('ok', reply_murkup=ReplyKeyboardRemove())
#
#
# def main():
#     # создаем объект updater
#     updater = Updater(TOKEN)
#
#     # получаем диспетчер из updater`а
#     dp = updater.dispatcher
#
#     # создаем обработчик типа Filter.text
#     text_handler = MessageHandler(Filters.text, echo)
#
#     # регистрируем обработчики в диспетчере
#     dp.add_handler(text_handler)
#     dp.add_handler(CommandHandler('start', start))
#     dp.add_handler(CommandHandler('help', help))
#     dp.add_handler(CommandHandler('email', email))
#     dp.add_handler(CommandHandler('phone', phone_number))
#     dp.add_handler(CommandHandler('close', close_keyboard))
#
#     # запускаем цикл приема и обработки сообщений
#     updater.start_polling()
#
#     # ждем завершения приложения
#     updater.idle()
#
#
# #if __name__ == '__main__':
# main()





# import logging
#
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#
# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
#
# logger = logging.getLogger(__name__)
#
#
# # Define a few command handlers. These usually take the two arguments update and
# # context. Error handlers also receive the raised TelegramError object in error.
# def start(update, context):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('Hi!')
#
#
# def help_command(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help! please')
#
#
# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)
#
#
# def main():
#     """Start the bot."""
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     updater = Updater(TOKEN, use_context=True)
#
#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher
#
#     # on different commands - answer in Telegram
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help_command))
#
#     # on noncommand i.e message - echo the message on Telegram
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()







# import logging
#
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# reply_keyboard = [['/start'],
#                   ['/close']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#
#
# def start(update, context):
#     keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
#                  InlineKeyboardButton("Option 2", callback_data='2')],
#
#                 [InlineKeyboardButton("Option 3", callback_data='3')]]
#
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     update.message.reply_text('Please choose:', reply_markup=reply_markup)
#
#
# def button(update, context):
#     query = update.callback_query
#
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#
#     query.edit_message_text(text="Selected option: {}".format(query.data))
#
#
# def help_command(update, context):
#     update.message.reply_text("Use /start to test this bot.")
#
#
# def main():
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     updater = Updater(TOKEN, use_context=True)
#
#     updater.dispatcher.add_handler(CommandHandler('start', start))
#     updater.dispatcher.add_handler(CallbackQueryHandler(button))
#     updater.dispatcher.add_handler(CommandHandler('help', help_command))
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()







from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def start(bot, update):
    update.message.reply_text('Вас приветствует командный Таскменеджер. В качестве теста нажмите: \n 1 - Вы босс \n 2 - Вы сотрудник', reply_markup=markup)


def close_keyboard(bot, update):
    update.message.reply_text('Закрываю клавиатуру', reply_markup=ReplyKeyboardRemove())


def echo(bot, update):
    update.message.reply_text('Ваше сообщение: ' + update.message.text)


updater = Updater(TOKEN)

# Получаем из него диспетчер сообщений.
dp = updater.dispatcher

reply_keyboard = [['закрыть клавиатуру', 'начать']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# Регистрируем обработчик команды "start" в диспетчере
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.regex('закрыть клавиатуру'), close_keyboard))
dp.add_handler(MessageHandler(Filters.regex('начать'), start))

# Создаём обработчик текстовых сообщений типа Filters.text
text_handler = MessageHandler(Filters.text, echo)

# Регистрируем обработчик в диспетчере
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()





