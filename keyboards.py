from telegram import ReplyKeyboardMarkup
from Models import ProjectModel, EmployeeModel


# Клавиатура Босса
def create_main_boss_keyboard():
    boss_reply_keyboard1 = [['Проекты', 'Задачи', 'Сотрудники'],
                            ['Отчёты']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_project_options_boss_keyboard():
    boss_reply_keyboard1 = [['Добавить проект', 'Удалить проект', 'Просмотр проектов'],
                            ['КПЗ'],
                            ['Главное меню']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_employee_options_boss_keyboard():
    boss_reply_keyboard1 = [['Добавить сотрудника', 'Удалить сотрудника', 'Просмотр сотрудников'],
                            ['Главное меню']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_task_options_boss_keyboard():
    boss_reply_keyboard1 = [['Добавить задачу', 'Удалить задачу', 'Просмотр задач'],
                            ['Главное меню']]
    boss_markup1 = ReplyKeyboardMarkup(boss_reply_keyboard1, one_time_keyboard=False)
    return boss_markup1


def create_projects_boss_keyboard(db):
    pm = ProjectModel(db.get_connection())
    projects = [el[1] for el in pm.get_all()]
    boss_reply_keyboard3 = []

    temp = []
    for p in projects:
        temp.append(p)
        if len(temp) == 4:
            boss_reply_keyboard3.append(temp)
            temp = []
    if temp:
        boss_reply_keyboard3.append(temp)

    boss_reply_keyboard3.append(['Главное меню'])
    boss_markup3 = ReplyKeyboardMarkup(boss_reply_keyboard3, one_time_keyboard=False)
    return boss_markup3


def create_employee_boss_keyboard(db):
    em = EmployeeModel(db.get_connection())
    staff = [el[1] for el in em.get_all()]

    boss_reply_keyboard4 = []

    temp = []
    for emp in staff:
        temp.append(emp)
        if len(temp) == 4:
            boss_reply_keyboard4.append(temp)
            temp = []
    if temp:
        boss_reply_keyboard4.append(temp)
    boss_reply_keyboard4.append(['Главное меню'])
    boss_markup4 = ReplyKeyboardMarkup(boss_reply_keyboard4, one_time_keyboard=False)
    return boss_markup4


def create_tasks_in_project_boss_keyboard():
    boss_reply_keyboard = [['Добавить задачу в проект', 'Удалить задачу из проекта'],
                            ['Главное меню']]
    boss_markup = ReplyKeyboardMarkup(boss_reply_keyboard, one_time_keyboard=False)
    return boss_markup


# ОТЧЁТЫ
def create_report_boss_keyboard():
    # boss_reply_keyboard = [['Отчёт по Проектам', 'Отчёт по Задачам', 'Отчёт по Сотрудникам'],
    #                        ['Главное меню']]
    boss_reply_keyboard = [['Главное меню']]
    boss_markup = ReplyKeyboardMarkup(boss_reply_keyboard, one_time_keyboard=False)
    return boss_markup


def create_report_projects_boss_keyboard(db):
    pm = ProjectModel(db.get_connection())
    projects = [el[1] for el in pm.get_all()]
    boss_reply_keyboard = []

    temp = []
    for p in projects:
        temp.append(p)
        if len(temp) == 4:
            boss_reply_keyboard.append(temp)
            temp = []
    if temp:
        boss_reply_keyboard.append(temp)

    boss_reply_keyboard.append(['Главное меню'])
    boss_markup = ReplyKeyboardMarkup(boss_reply_keyboard, one_time_keyboard=False)
    return boss_markup


def create_report_employee_boss_keyboard():
    boss_reply_keyboard = [['Отчёты по Проектам', 'Отчёты по Задачам', 'Отчёты по Сотрудникам'],
                           ['Главное меню']]
    boss_markup = ReplyKeyboardMarkup(boss_reply_keyboard, one_time_keyboard=False)
    return boss_markup


def create_report_task_boss_keyboard():
    boss_reply_keyboard = [['Отчёты по Проектам', 'Отчёты по Задачам', 'Отчёты по Сотрудникам'],
                           ['Главное меню']]
    boss_markup = ReplyKeyboardMarkup(boss_reply_keyboard, one_time_keyboard=False)
    return boss_markup


# Клавиатура сотрудника
def create_main_employee_keyboard():
    employee_reply_keyboard1 = [['Просмотр моих задач', 'Выполнено']]
    employee_markup1 = ReplyKeyboardMarkup(employee_reply_keyboard1, one_time_keyboard=False)
    return employee_markup1


def create_done_employee_keyboard():
    employee_reply_keyboard3 = [['Выполнено']]
    employee_markup3 = ReplyKeyboardMarkup(employee_reply_keyboard3, one_time_keyboard=False)
    return employee_markup3


# Клавиатура возврата на главное меню
def create_menu_keyboard():
    menu_keyboard = [['Главное меню']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
    return menu_markup


# Клавиатура возврата из Отчётов
def create_back_to_reports_keyboard():
    menu_keyboard = [['Назад'],
                     ['Главное меню']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
    return menu_markup


# Главная клавиатура pravo_help
def create_main_pravo_help_keyboard():
    pravo_help_keyboard = [['Консультация', 'Оплата']]
    pravo_help_markup = ReplyKeyboardMarkup(pravo_help_keyboard, one_time_keyboard=False)
    return pravo_help_markup


# Клавиатура оплаты pravo_help
def create_payment_pravo_help_keyboard():
    pravo_help_keyboard = [['Выставить счёт для юр.лиц', 'Оплата картой для физ.лиц'],
                           ['Главное меню']]
    pravo_help_markup = ReplyKeyboardMarkup(pravo_help_keyboard, one_time_keyboard=False)
    return pravo_help_markup
