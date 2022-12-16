from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from collections import defaultdict
import re
import os
from dotenv import load_dotenv

from chooser import Client, Chooser

load_dotenv()

token = os.getenv('TOKEN')
updater = Updater(token=token)
users = defaultdict()

#bot_client = Client(years_before_retirement=years_before_retirement, expenses_per_month=expenses_per_month)

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
        [['/DetermineInvestorType']],
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


def salary(update, context):
    global years_before_retirement
    chat = update.effective_chat
    years_before_retirement_dirty = update.message.text
    years_before_retirement = int(re.sub("[^0-9]", "", years_before_retirement_dirty))

    context.bot.send_message(
        chat_id=chat.id,
        text='Сколько тратите в месяц? Заполни ответ по образцу. Пример: 10000 рублей(долларов, сом, евро)',

    )


def industries_lev1(update, context):
    global expenses_per_month
    chat = update.effective_chat
    expenses_per_month_dirty = update.message.text
    expenses_per_month = int(re.sub("[^0-9]", "", expenses_per_month_dirty))
    buttons = ReplyKeyboardMarkup([['Банки и финансы', 'Машиностроение'], ['Металлы и добыча']],
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
    buttons = ReplyKeyboardMarkup(
        [['Наука и инновации'], ['Нефть и газ', 'Потребительские товары']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='В компании из каких сфер деятельности хотел(а) бы вкладываться? Выбери 2 по приоритету',
        reply_markup=buttons

    )


def industries_lev3(update, context):
    global industry2
    chat = update.effective_chat
    industry2 = update.message.text
    buttons = ReplyKeyboardMarkup([['Прочие отрасли', 'Транспорт']], resize_keyboard=True)
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
    buttons = ReplyKeyboardMarkup([['Хочу узнать результат!']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Отлично! Бот составил для тебя индивидуальный инвестиционный план!',
        reply_markup=buttons

    )


def get_result(update, context):
    chat = update.effective_chat
    if update.message.chat_id not in users:
        users[chat.id] = Client(years_before_retirement=years_before_retirement, expenses_per_month=expenses_per_month)
    print(users[chat.id])
    result_text = Chooser().get_text_about_stocks(client=users[chat.id])
    context.bot.send_message(
        chat_id=chat.id,
        text= result_text,
    )


def motivation_quote(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Инвестирование должно напоминать наблюдение за тем, как сохнет краска или как растет трава.'
             ' Если вам нужен азарт, то возьмите 800 долларов и поезжайте в Лас-Вегас.',
    )


def main():
    updater.dispatcher.add_handler(CommandHandler('start', say_hi))
    updater.dispatcher.add_handler(CommandHandler('go', wake_up))
    updater.dispatcher.add_handler(CommandHandler('DetermineInvestorType', determine_type))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile('лет|года', re.IGNORECASE)), salary))

    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile('рублей|долларов|сом|тенге|евро', re.IGNORECASE)),
                       industries_lev1))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Банки и финансы|Машиностроение|Металлы и добыча',
        re.IGNORECASE)), industries_lev2))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Наука и инновации|Нефть и газ|Потребительские товары',
        re.IGNORECASE)), industries_lev3))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Прочие отрасли|Транспорт', re.IGNORECASE)), thanks))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Прочие отрасли|Транспорт', re.IGNORECASE)), thanks))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(
        'Хочу узнать результат!', re.IGNORECASE)), get_result))

    updater.start_polling()
    updater.idle()
    print(users)

if __name__ == '__main__':
    main()
