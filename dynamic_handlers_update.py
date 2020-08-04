from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup


def update_projects_handler(dp, handler, function, projects_list):
    dp.remove_handler(handler)
    projects_murkup = ReplyKeyboardMarkup.from_column(projects_list)
    handler = MessageHandler(Filters.text(projects_list), function)
    dp.add_handler(handler)


def update_employees_handler():
    pass

