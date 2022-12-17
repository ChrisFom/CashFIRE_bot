from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from collections import defaultdict
import re
import os
from dotenv import load_dotenv
from models.models import Client
# from chooser import Client, Chooser
from statistics.stocks import StocksStatistics
from  statistics.industries import IndustriesStatistics
from controller import Controller

load_dotenv()

token = os.getenv('TOKEN')
updater = Updater(token=token)
users = defaultdict()


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='Привет, я FIRE_assistant_bot! Давай создадим твой инвестиционный портфель вместе')
    buttons = ReplyKeyboardMarkup([['/go']],
                                  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы включили меня',

        reply_markup=buttons
    )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name

    buttons = ReplyKeyboardMarkup(
        [['/StartQuiz']],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Выбери с чего хочешь начать, {}!'.format(name),
        reply_markup=buttons

    )


def determine_type(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Через сколько лет вы хотите выйти на пенсию? Заполни ответ по образцу. Пример: 5 лет(2 года)',

    )
    print(context.args)


def get_years_before_retirement(update, context):
    chat = update.effective_chat
    years_before_retirement_dirty = update.message.text
    years_before_retirement = int(re.sub("[^0-9]", "", years_before_retirement_dirty))
    if update.message.chat_id not in users:
        users[chat.id] = Client(years_before_retirement=years_before_retirement)
    context.bot.send_message(
        chat_id=chat.id,
        text='Сколько тратите в месяц? Заполни ответ по образцу. Пример: 10000 рублей(долларов, сом, евро)',

    )


def industries_lev1(update, context):
    chat = update.effective_chat
    expenses_per_month_dirty = update.message.text
    expenses_per_month = int(re.sub("[^0-9]", "", expenses_per_month_dirty))
    if update.message.chat_id in users:
        users.get(chat.id).expenses_per_month = expenses_per_month

    buttons = ReplyKeyboardMarkup([['it', 'electricity'], ['machinery', 'eco_materials']],
                                  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='В компании из каких сфер деятельности хотел(а) бы вкладываться? Выбери 1 по приоритету',
        reply_markup=buttons

    )


def industries_lev2(update, context):
    global industry1
    chat = update.effective_chat
    industry1 = update.message.text
    if update.message.chat_id in users:
        users.get(chat.id).categories.append(industry1)
    buttons = ReplyKeyboardMarkup(
        [['obligations'], ['green_energetics', 'currency']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='В компании из каких сфер деятельности хотел(а) бы вкладываться? Выбери 2 по приоритету',
        reply_markup=buttons

    )


def industries_lev3(update, context):
    global industry2
    chat = update.effective_chat
    industry2 = update.message.text
    if update.message.chat_id in users:
        users.get(chat.id).categories.append(industry2)
    buttons = ReplyKeyboardMarkup([['finance', 'other', 'luxury_metals']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='В компании из каких сфер деятельности хотел(а) бы вкладываться? Выбери 3 по приоритету',
        reply_markup=buttons

    )


def thanks(update, context):
    global industry3
    chat = update.effective_chat
    industry3 = update.message.text
    print(industry3, '-индустрия 3')
    if update.message.chat_id in users:
        users.get(chat.id).categories.append(industry3)
    buttons = ReplyKeyboardMarkup([['Хочу узнать результат!']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Отлично! Бот составил для тебя индивидуальный инвестиционный план!',
        reply_markup=buttons

    )


def get_result(update, context):
    chat = update.effective_chat
    print(users[chat.id])
    controller = Controller()
    if update.message.chat_id in users:
        funds = controller.get_personal_funds(client=users.get(chat.id))
        users.get(chat.id).personal_funds = funds
    result_text = controller.get_text_about_stocks(client=users[chat.id])
    buttons = ReplyKeyboardMarkup([['Какие акции лежат в твоем портфеле?']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=result_text,
        reply_markup=buttons
    )


def get_top_stocks(update, context):
    chat = update.effective_chat
    stocks = StocksStatistics().get_top_stocks(weights=users.get(chat.id).personal_funds, n_top=10)
    buttons = ReplyKeyboardMarkup([['Топ отраслей из твоего портфеля?']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=stocks,
        reply_markup=buttons
    )


def get_top_industries(update, context):
    chat = update.effective_chat
    industries = IndustriesStatistics().get_top_industries(
        weights=users.get(chat.id).personal_funds, n_top=5)
    context.bot.send_message(
        chat_id=chat.id,
        text=industries,
    )


def main():
    updater.dispatcher.add_handler(CommandHandler('start', say_hi))
    updater.dispatcher.add_handler(CommandHandler('go', wake_up))
    updater.dispatcher.add_handler(CommandHandler('StartQuiz', determine_type))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile('лет|года', re.IGNORECASE)), get_years_before_retirement))

    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile('рублей|долларов|сом|тенге|евро', re.IGNORECASE)),
                       industries_lev1))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'it|electricity|machinery|eco_materials',
        re.IGNORECASE)), industries_lev2))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'obligations|green_energetics|currency',
        re.IGNORECASE)), industries_lev3))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'finance|other|luxury_metals', re.IGNORECASE)), thanks))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Хочу узнать результат!', re.IGNORECASE)), get_result))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Какие акции лежат в твоем портфеле?', re.IGNORECASE)), get_top_stocks))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Топ отраслей из твоего портфеля?', re.IGNORECASE)), get_top_industries))

    updater.start_polling()
    updater.idle()
    print(users)


if __name__ == '__main__':
    main()
