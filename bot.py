from telegram.ext import Updater, Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

# Access token
TOKEN = "1306952282:AAEYQicKyWmBDHGmJ-vhrgmOladw6AYpNao"

reply_keyboard = [['/help'],
                  ['/phone', '/email'],
                  ['/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


# обработчик сообщений
def echo(bot, update):
    # у update есть поле message с текстом сообщения
    # а также метод reply_text, который отвечает на сообщение
    update.message.reply_text(update.message.text)


def start(bot, update):
    update.message.reply_text(
        'Привет, я Эхо-бот. Я буду повторять за вами!',
        reply_markup=markup
    )


def help(bot, update):
    update.message.reply_text(
        'Я пока не умею помогать... Я только ваше эхо.'
    )


def email(bot, update):
    update.message.reply_text(
        'den.martsinovich@yandex.ru'
    )


def phone_number(bot, update):
    update.message.reply_text(
        '+7(965)309-57-21'
    )


def close_keyboard(bot, update):
    update.message.reply_text('ok', reply_murkup=ReplyKeyboardRemove())


def main():
    # создаем объект updater
    updater = Updater(TOKEN)

    # получаем диспетчер из updater`а
    dp = updater.dispatcher

    # создаем обработчик типа Filter.text
    text_handler = MessageHandler(Filters.text, echo)

    # регистрируем обработчики в диспетчере
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('email', email))
    dp.add_handler(CommandHandler('phone', phone_number))
    dp.add_handler(CommandHandler('close', close_keyboard))

    # запускаем цикл приема и обработки сообщений
    updater.start_polling()

    # ждем завершения приложения
    updater.idle()


#if __name__ == '__main__':
main()