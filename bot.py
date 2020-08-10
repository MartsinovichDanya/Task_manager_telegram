from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from DB import DB
from Models import UserModel, TaskModel, ProjectModel, EmployeeModel

from keyboards import create_main_boss_keyboard, create_projects_boss_keyboard
from keyboards import create_menu_keyboard, create_project_options_boss_keyboard
from keyboards import create_employee_options_boss_keyboard, create_task_options_boss_keyboard
from keyboards import create_employee_boss_keyboard

from boss_commands import add_project, add_task, add_employee, delete_project, delete_task, delete_employee

from exceptions import UserNotFound, UserAlreadyExist, ProjectNotFound, ProjectAlreadyExist


db = DB('tm.db')
TOKEN = "1306952282:AAEYQicKyWmBDHGmJ-vhrgmOladw6AYpNao"
is_add_project = False
is_add_task = False
is_add_employee = False
is_delete_project = False
is_delete_task = False
is_delete_employee = False


# Приветствие
def start(bot, update):
    global is_add_project, is_add_task, is_add_employee, is_delete_project, is_delete_task, is_delete_employee
    is_add_project = False
    is_add_task = False
    is_add_employee = False
    is_delete_project = False
    is_delete_task = False
    is_delete_employee = False
    um = UserModel(db.get_connection())
    tg_id = update.message.from_user.id

    # Левый чувак
    if not um.get(tg_id):
        update.message.reply_text('<b>Вас нет в нашей базе данных.</b>', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
    # Босс
    elif um.get(tg_id)[2]:
        update.message.reply_text('<b>Добро пожаловать, Лидер команды!</b>', reply_markup=create_main_boss_keyboard(), parse_mode='HTML')
        is_boss = True
    # Сотрудник
    else:
        update.message.reply_text('<b>Добро пожаловать!</b>', reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


# Главное меню
def project_options(bot, update):
    update.message.reply_text('<b>Раздел "Проекты"</b>', reply_markup=create_project_options_boss_keyboard(), parse_mode='HTML')


def employee_options(bot, update):
    update.message.reply_text('<b>Раздел "Сотрудники"</b>', reply_markup=create_employee_options_boss_keyboard(), parse_mode='HTML')


def task_options(bot, update):
    update.message.reply_text('<b>Раздел "Задачи"</b>', reply_markup=create_task_options_boss_keyboard(), parse_mode='HTML')


# Выбор проекта/сотрудника
def select_project(bot, update):
    update.message.reply_text('<b>Выберите проект из предложенного списка</b>', reply_markup=create_projects_boss_keyboard(db),
                              parse_mode='HTML')


def select_employee(bot, update):
    update.message.reply_text('<b>Выберите сотрудника из предложенного списка</b>', reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


# Просмотр
def project_preview(update, project):
    tm = TaskModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    tasks = tm.get_by_project(pm.get_id(project))

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача: <u>{task[1]}</u></b>
<b>Описание:</b> {task[2]}
<b>Исполнитель:</b> {em.get(task[3])[1]}
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


def employee_preview(update, employee):
    tm = TaskModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    eid = em.get_id(employee)
    tasks = tm.get_by_emp(eid)

    for task in tasks:
        update.message.reply_text(f'''
<b>Проект: <u>{pm.get_name(task[4])}</u></b>
<b>Задача: {task[1]}</b>
<b>Описание:</b> {task[2]}
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


def task_preview(bot, update):
    tm = TaskModel(db.get_connection())
    em = EmployeeModel(db.get_connection())
    pm = ProjectModel(db.get_connection())
    tasks = tm.get_all()

    for task in tasks:
        update.message.reply_text(f'''
<b>Задача: <u>{task[1]}</u></b>
<b>Проект: {pm.get_name(task[4])}</b>
<b>Описание: {task[2]}</b>
<b>Сотрудник: {em.get(task[3])[1]}</b>
<b>Статус:</b> {'Выполнена' if task[5] else 'В процессе'}''', reply_markup=create_menu_keyboard(), parse_mode='HTML')


# Проекты
def write_add_project(bot, update):
    global is_add_project
    is_add_project = True
    update.message.reply_text('<i><b>Напишите название проекта. Запрещаются специальные символы: !, `, @, №, $, %, &, ?, /</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


def write_delete_project(bot, update):
    global is_delete_project
    is_delete_project = True
    update.message.reply_text('<i><b>Напишите название проекта, который Вы хотели бы удалить</b></i>', reply_markup=create_projects_boss_keyboard(db),
                              parse_mode='HTML')


# Задачи
def write_add_task(bot, update):
    global is_add_task
    is_add_task = True
    update.message.reply_text('<i><b>Используйте ";" для разделения требуемых параметров</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text('<i><b>Напишите название задачи, описание, имя сотрудника, название проекта.\nПример: задача1;описание1;имя1;проект1</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


def write_delete_task(bot, update):
    global is_delete_task
    is_delete_task = True
    update.message.reply_text('<i><b>Напишите ID задачи, которую Вы хотели бы удалить</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Сотрудники
def write_add_employee(bot, update):
    global is_add_employee
    is_add_employee = True
    update.message.reply_text('<i><b>Используйте ";" для разделения требуемых параметров</b></i>',
                              reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    update.message.reply_text('<i><b>Напишите имя и ID сотрудника.\nПример: имя1;0123456789</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


def write_delete_employee(bot, update):
    global is_delete_employee
    is_delete_employee = True
    update.message.reply_text('<i><b>Напишите имя сотрудника, которого Вы хотели бы удалить</b></i>', reply_markup=create_employee_boss_keyboard(db),
                              parse_mode='HTML')


# Тестовая функция
def callback_method(bot, update):
    update.message.reply_text('<i><b>Ю НОУ БЛИН</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')


# Глобальная функция
def global_function(bot, update):
    global is_add_project, is_add_task, is_add_employee, is_delete_project, is_delete_task, is_delete_employee
    global projects_list, employee_list
    update.message.reply_text('<i><b>Глобал ю ноу блин</b></i>', reply_markup=create_menu_keyboard(),
                              parse_mode='HTML')
    print(projects_list)
    if update.message['text'] in projects_list and not is_delete_project:
        project = update.message['text']
        update.message.reply_text(f"Просмотр задач по проекту: {project}")
        project_preview(update, project)

    elif update.message['text'] in employee_list and not is_delete_employee:
        employee = update.message['text']
        update.message.reply_text(f"Просмотр задач сотрудника: {employee}")
        employee_preview(update, employee)

    elif is_add_project:
        is_add_project = False
        name = update.message['text']
        projects_list.append(name)
        try:
            add_project(name)
        except ProjectAlreadyExist:
            update.message.reply_text("Проект уже существует")
            is_add_project = True

    elif is_add_task:
        is_add_task = False
        params = update.message['text']
        name, description, emp_name, project_name = params.split(';')
        try:
            add_task(bot, name, description, emp_name, project_name)
        except ProjectNotFound:
            update.message.reply_text("Проект не найден")
            is_add_task = True
        except UserNotFound:
            update.message.reply_text("Сотрудник не найден")
            is_add_task = True

    elif is_add_employee:
        is_add_employee = False
        params = update.message['text']
        name, id = params.split(';')
        try:
            add_employee(name, id)
            employee_list.append(name)
        except UserAlreadyExist:
            update.message.reply_text("Пользователь уже существует")
            is_add_employee = True

    elif is_delete_project:
        is_delete_project = False
        name = update.message['text']
        delete_project(name)
        del projects_list[projects_list.index(name)]

    elif is_delete_task:
        is_delete_task = False
        id = int(update.message['text'])
        delete_task(id)

    elif is_delete_employee:
        is_delete_employee = False
        name = update.message['text']
        delete_employee(name)
        del employee_list[employee_list.index(name)]


updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))


# Клавиатура Босса
dp.add_handler(MessageHandler(Filters.regex('Проекты'), project_options))
dp.add_handler(MessageHandler(Filters.regex('Задачи'), task_options))
dp.add_handler(MessageHandler(Filters.regex('Сотрудники'), employee_options))

dp.add_handler(MessageHandler(Filters.regex('Добавить проект'), write_add_project))
dp.add_handler(MessageHandler(Filters.regex('Удалить проект'), write_delete_project))
dp.add_handler(MessageHandler(Filters.regex('Просмотр проектов'), select_project))

dp.add_handler(MessageHandler(Filters.regex('Добавить задачу'), write_add_task))
dp.add_handler(MessageHandler(Filters.regex('Удалить задачу'), write_delete_task))
dp.add_handler(MessageHandler(Filters.regex('Просмотр задач'), task_preview))

dp.add_handler(MessageHandler(Filters.regex('Добавить сотрудника'), write_add_employee))
dp.add_handler(MessageHandler(Filters.regex('Удалить сотрудника'), write_delete_employee))
dp.add_handler(MessageHandler(Filters.regex('Просмотр сотрудников'), select_employee))

dp.add_handler(MessageHandler(Filters.regex('Главное меню'), start))

# Клавиатура сотрудника
dp.add_handler(MessageHandler(Filters.regex('Просмотр задач'), callback_method))
dp.add_handler(MessageHandler(Filters.regex('Выполнено'), callback_method))

# Создаём и удаляем тестовый обработчик текстовых сообщений (команд)
projects_list = []
employee_list = []

em = EmployeeModel(db.get_connection())
for e in em.get_all():
    employee_list.append(e[1])

# Создаём обработчик текстовых сообщений типа Filters.text
text_handler = MessageHandler(Filters.text, global_function)
# Регистрируем обработчик в диспетчере.
dp.add_handler(text_handler)

# Запускаем цикл приема и обработки сообщений
updater.start_polling()

# Ждём завершения приложения при нажатии клавиш Ctrl+C
updater.idle()
