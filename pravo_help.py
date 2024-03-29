from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from keyboards import create_main_pravo_help_keyboard, create_payment_pravo_help_keyboard, create_menu_keyboard
from keyboards import create_service_pravo_help_keyboard
from Models_kpz import InnModel, KpzTaskModel, FileModel
from Models import UserModel, ReportModel
from commands import send_email, get_uniq_filename, get_cadastre_report, prepare_report_msg
from DB import DB
import os
from dotenv import load_dotenv
from loguru import logger

logger.add('logs/pravo_help.log.json', format='{time} | {name} | {level} | {message}', level='INFO', rotation='1 month',
           compression='zip',
           serialize=True)

logger.info('Start polling: Pravo_help Bot')

dotenv_path = os.path.join(os.path.dirname(__file__), 'Task_manager_telegram.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

dotenv_path = os.path.join(os.path.dirname(__file__), 'kpz_mail.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN2')
KPZ_FILES_DIR = 'kpz_files'
BOSS_EMAIL_ADDRESS = os.getenv('BOSS_ADDRESS')
JSON_REPORTS_DIR = 'cad_reports'

db = DB('kpz.db')
tm_db = DB('tm.db')
rdb = DB('reports.db')

is_juristic = False
is_consultation = False

is_cadastre_object = False


# Приветствие
def start(bot, update):
    logger.info(
        f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    if not update.message['chat']['username']:
        update.message.reply_text('''
<b>Пожалуйста, установите username в профиле.</b>
<b>Инструкция:</b> на мобильном устройстве перейдите в "Настройки", нажмите на "Имя пользователя" и напишите свой никнейм.
Это нужно для того, чтобы мы могли с Вами связаться в Telegram''',
                                  reply_markup=create_main_pravo_help_keyboard(), parse_mode='HTML')
    else:
        update.message.reply_text('''Чтобы получить информацию об объекте: выберите раздел «Услуги», а затем в разделе «Информация ЕГРН об объекте», введите кадастровый номер объекта.

<b>ВАЖНО! Бот запрашивает Росреестра в режиме он-лайн, поэтому информация не всегда оперативно выдается, иногда надо подождать.</b>''',
                                  reply_markup=create_main_pravo_help_keyboard(), parse_mode='HTML')


# Раздел "Оплата"
def payment(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    update.message.reply_text('<b>Выберите способ оплаты</b>', reply_markup=create_payment_pravo_help_keyboard(),
                              parse_mode='HTML')


# Раздел "Оплата" (Выставить счёт (юр. лицо))
def juristic_person(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    global is_juristic
    is_juristic = True
    update.message.reply_text('<b>Напишите свой ИНН (ОГРН)</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Раздел "Оплата" (Оплата картой (физ. лицо))
def natural_person(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    update.message.reply_text('<b>Переходим к "РобоКассе"</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text(
        'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=findtheowner&InvId=0&Culture=ru&Encoding=utf-8&OutSum=500&SignatureValue=ac288b7d40a1747dbe687d74aff91323',
        reply_markup=create_menu_keyboard(),
        parse_mode='HTML')


# Раздел "Услуги"
def service(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    update.message.reply_text('<b>Выберите тип услуги</b>', reply_markup=create_service_pravo_help_keyboard(),
                              parse_mode='HTML')


# Раздел "Кадастровый объект"
def cadastral_objects(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    global is_cadastre_object
    is_cadastre_object = True
    update.message.reply_text('<b>Введите кадастровый номер объекта</b>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Раздел "Консультация"
def consultation(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    global is_consultation
    is_consultation = True
    update.message.reply_text(
        '<b>Опишите проблему и задайте вопрос.\nВАЖНО! Вы можете отправлять юридический вопрос как с файлом, так и без него. Если к Вашему вопросу прилагается какой-либо документ, прикреплять его необходимо вместе с текстовым сообщением!</b>',
        reply_markup=create_menu_keyboard(),
        parse_mode='HTML')


# Глобальная функция
def global_function(bot, update):
    logger.info(f'{update.message["chat"]["id"]} ({update.message["chat"]["username"]} - {update.message["chat"]["first_name"]} {update.message["chat"]["last_name"]}) | "{update.message.text}"')

    global is_juristic, is_consultation, is_cadastre_object

    if is_consultation:
        is_consultation = False
        ktm = KpzTaskModel(db.get_connection())
        username = update.message['chat']['username']
        if not update.message.document:
            ktm.insert(update.message.text, '@' + username)

            send_email(BOSS_EMAIL_ADDRESS, f'''
<b>Юридический вопрос: <u>{update.message.text}</u></b><br>
<b>Контакты Заказчика: {'@' + username}</b>''')
        else:
            file_name = update.message.document.file_name
            file = update.message.document.get_file()
            file_id = file.file_id

            new_file_name = get_uniq_filename(file_name, username)
            file_path = os.path.join(os.getcwd(), KPZ_FILES_DIR, new_file_name)
            file.download(file_path)

            fm = FileModel(db.get_connection())
            fm.insert(file_id, file_name)
            ktm.insert(update.message['caption'], '@' + username,
                       file_id=fm.get_id(file_id))

            send_email(BOSS_EMAIL_ADDRESS, f'''
<b>Юридический вопрос: <u>{update.message['caption']}</u></b>\n
<b>Контакты Заказчика: {'@' + username}</b>''', file=file_path)

    elif is_juristic:
        is_juristic = False
        username = update.message['chat']['username']
        inn = update.message.text
        im = InnModel(db.get_connection())
        im.insert(inn, username)
        update.message.reply_text('<b>ИНН (ОГРН) записан</b>', reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')

    elif is_cadastre_object:
        is_cadastre_object = False
        update.message.reply_text('<b>Обработка заявки. Пожалуйста, подождите</b>', reply_markup=create_menu_keyboard(),
                                  parse_mode='HTML')

        um = UserModel(tm_db.get_connection())
        rm = ReportModel(rdb.get_connection())

        cad_number = update.message.text
        username = update.message['chat']['username']
        report = get_cadastre_report(cad_number)

        if 'error_code' in report:
            if report['error_code'] == 400:
                update.message.reply_text('<b>Введенное значение не является кадастровым номером</b>',
                                          reply_markup=create_menu_keyboard(),
                                          parse_mode='HTML')
            elif report['error_code'] == 500:
                update.message.reply_text('<b>Сервис поиска кадастровых объектов временно недоступен</b>',
                                          reply_markup=create_menu_keyboard(),
                                          parse_mode='HTML')
            elif report['error_code'] == 503:
                update.message.reply_text(
                    '<b>Непредвиденная ошибка сервиса поиска кадастровых объектов. Мы уже работаем над этим.</b>',
                    reply_markup=create_menu_keyboard(),
                    parse_mode='HTML')
        else:
            # report_file_name = cad_number.replace(':', '') + '.json'
            # with open(os.path.join(JSON_REPORTS_DIR, report_file_name), 'w') as rep_f:
            #     json.dump(report, rep_f)

            rm.insert('NONE_FILE', cad_number, report['details']['Адрес (местоположение)'], username)

            update.message.reply_text('<b>Ваша заявка принята. В ближайшее время ожидайте обратную связь</b>',
                                      reply_markup=create_menu_keyboard(),
                                      parse_mode='HTML')

        msg = prepare_report_msg(username, report)
        bot.sendMessage(um.get_boss_id(), msg, parse_mode='HTML')


updater = Updater(TOKEN)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.regex('Услуги'), service))
dp.add_handler(MessageHandler(Filters.regex('Консультация'), consultation))
dp.add_handler(MessageHandler(Filters.regex('Информация ЕГРН об объекте'), cadastral_objects))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.regex('Главное меню'), start))

dp.add_handler(MessageHandler(Filters.regex('Оплата картой для физ.лиц'), natural_person))
dp.add_handler(MessageHandler(Filters.regex('Выставить счёт для юр.лиц'), juristic_person))
# dp.add_handler(MessageHandler(Filters.regex('Оплата'), payment))


text_handler = MessageHandler(Filters.all, global_function)
# Регистрируем обработчик в диспетчере.
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
