from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, ReplyKeyboardMarkup as markup, KeyboardButton as button
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiohttp
import os
import json
import db_operations

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

with open(BASEDIR + '/database/info.json', 'r', encoding='utf-8') as js:
    infos = json.load(js)


class Step(StatesGroup):
    start = State()
    vuz = State()
    prof = State()
    chance = State()
    contacts = State()
    application = State()
    rating = State()
    questions = State()


def default_menu():
    menu = markup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    menu.row(button('О вузе'))
    menu.row(button('Проф. тестирование'),
             button('Шанс поступить'),
             button('Узнать рейтинг'))
    menu.row(button('Вопросы - Ответы'),
             button('Онлайн заявка'),
             button('Контакты'))
    return(menu)


@dp.message_handler(commands=['start'], state="*")
async def startMessage(message, state: FSMContext):
    await bot.send_message(message.chat.id, infos['welcome_message'], reply_markup=default_menu())
    await Step.start.set()


@dp.message_handler(state="*", text_contains='Назад')
async def backMessage(message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Выберите действие', reply_markup=default_menu())
    await Step.start.set()


@dp.message_handler(state=Step.start)
async def firstStep(message, state: FSMContext):
    if message.text == 'О вузе':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        btn2 = button('Подробнее о факультетах')
        menu.row(btn1)
        menu.row(btn2)
        await bot.send_message(message.chat.id, infos['nstu_info'], reply_markup=menu)
        await Step.vuz.set()
    if message.text == 'Проф. тестирование':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['test_info'], reply_markup=menu)
        await Step.prof.set()
    if message.text == 'Шанс поступить':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['chance_info'], reply_markup=menu)
        await Step.chance.set()
    if message.text == 'Контакты':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Приемная комиссия')
        btn2 = button('Деканаты факультетов')
        btn3 = button('Назад')
        menu.row(btn1)
        menu.row(btn2)
        menu.row(btn3)
        await bot.send_message(message.chat.id, infos['contacts_info'], reply_markup=menu)
        await Step.contacts.set()
    if message.text == 'Онлайн заявка':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['online_application'], reply_markup=menu)
        await Step.application.set()
    if message.text == 'Узнать рейтинг':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['rating_info'], reply_markup=menu)
        await Step.rating.set()
    if message.text == 'Вопросы - Ответы':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=True)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['questions_info'], reply_markup=menu)
        await Step.questions.set()


@dp.message_handler(state=Step.vuz)
async def vuzStep(message, state: FSMContext):
    if message.text == 'Подробнее о факультетах':
        menu = markup(row_width=5, resize_keyboard=True,
                      one_time_keyboard=False)
        btn1 = button('АВТФ')
        btn2 = button('ФЛА')
        btn3 = button('МТФ')
        btn4 = button('ФМА')
        btn5 = button('ФПМИ')
        btn6 = button('РЭФ')
        btn7 = button('ФТФ')
        btn8 = button('ФЭН')
        btn9 = button('ФБ')
        btn10 = button('ФГО')
        btn11 = button('Назад')
        menu.row(btn1, btn2, btn3, btn4, btn5)
        menu.row(btn6, btn7, btn8, btn9, btn10)
        menu.row(btn11)
        await bot.send_message(message.chat.id, infos['faculties_info'], reply_markup=menu)
    elif message.text != 'Назад':
        msg = db_operations.get_faculties(message.text)
        await bot.send_message(message.chat.id, msg)


@dp.message_handler(state=Step.contacts)
async def contactsStep(message, state: FSMContext):
    if message.text == 'Приемная комиссия':
        menu = markup(row_width=1, resize_keyboard=True,
                      one_time_keyboard=False)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['comission_contacts'], reply_markup=menu)
    if message.text == 'Деканаты факультетов':
        menu = markup(row_width=5, resize_keyboard=True,
                      one_time_keyboard=False)
        btn1 = button('АВТФ')
        btn2 = button('ФЛА')
        btn3 = button('МТФ')
        btn4 = button('ФМА')
        btn5 = button('ФПМИ')
        btn6 = button('РЭФ')
        btn7 = button('ФТФ')
        btn8 = button('ФЭН')
        btn9 = button('ФБ')
        btn10 = button('ФГО')
        btn11 = button('Назад')
        menu.row(btn1, btn2, btn3, btn4, btn5)
        menu.row(btn6, btn7, btn8, btn9, btn10)
        menu.row(btn11)
        await bot.send_message(message.chat.id, infos['faculties_contacts'], reply_markup=menu)
    elif message.text != 'Назад':
        msg = db_operations.get_faculties_contacts(message.text)
        await bot.send_message(message.chat.id, msg)

if __name__ == '__main__':
    executor.start_polling(dp)
