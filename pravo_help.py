from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from keyboards import create_main_pravo_help_keyboard, create_payment_pravo_help_keyboard, create_menu_keyboard
from Models_kpz import InnModel, KpzTaskModel, FileModel
from DB import DB

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'Task_manager_telegram.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN2')
db = DB('kpz.db')
is_juristic = False
is_consultation = False
kpz_files_dir = 'kpz_files'


# Приветствие
def start(bot, update):
    update.message.reply_text('<b>Выберите раздел "Консультация", если хотите рассказать о проблеме и задать вопрос, или раздел "Оплата", чтобы оплатить ранее оказанную помощь</b>',
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
    update.message.reply_text('https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=findtheowner&InvId=0&Culture=ru&Encoding=utf-8&OutSum=500&SignatureValue=ac288b7d40a1747dbe687d74aff91323', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Раздел "Консультация"
def consultation(bot, update):
    global is_consultation
    is_consultation = True
    update.message.reply_text('<b>Опишите проблему и задайте вопрос.\nВАЖНО! Вы можете отправлять юридический вопрос как с файлом, так и без него. Если к Вашему вопросу прилагается какой-либо документ, прикреплять его необходимо вместе с текстовым сообщением!</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')

#
# def file_saver(bot, update):
#     file_name = update.message.document.file_name
#     file = update.message.document.get_file()
#     file_id = file.file_id
#     file.download(os.path.join(os.getcwd(), kpz_files_dir, file_name))
#     update.message.reply_document(file_id)


# Глобальная функция
def global_function(bot, update):
    global is_juristic, is_consultation
    print(update)

    if is_consultation:
        is_consultation = False
        ktm = KpzTaskModel(db.get_connection())
        if not update.message.document:
            ktm.insert(update.message.text, '@'+update.message['chat']['username'])
        else:
            file_name = update.message.document.file_name
            file = update.message.document.get_file()
            file_id = file.file_id

            file.download(os.path.join(os.getcwd(), kpz_files_dir, file_name))

            fm = FileModel(db.get_connection())
            fm.insert(file_id, file_name)
            ktm.insert(update.message['caption'], '@' + update.message['chat']['username'],
                       file_id=fm.get_id(file_id))

    if is_juristic:
        is_juristic = False
        inn = update.message.text
        im = InnModel(db.get_connection())
        im.insert(inn)
        update.message.reply_text('<b>ИНН (ОГРН) записан</b>', reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.regex('Консультация'), consultation))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.regex('Главное меню'), start))

dp.add_handler(MessageHandler(Filters.regex('Оплата картой для физ.лиц'), natural_person))
dp.add_handler(MessageHandler(Filters.regex('Выставить счёт для юр.лиц'), juristic_person))
dp.add_handler(MessageHandler(Filters.regex('Оплата'), payment))



text_handler = MessageHandler(Filters.all, global_function)
# Регистрируем обработчик в диспетчере.
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
