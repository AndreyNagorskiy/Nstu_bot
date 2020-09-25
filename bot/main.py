from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, ReplyKeyboardMarkup as markup, KeyboardButton as button
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

with open(BASEDIR + './database/info.json', 'r', encoding='utf-8') as js:
    infos = json.load(js)


class Step():
    start = 'start'
    vuz = 'vuz'
    prof = 'prof'
    chance = 'chance'
    contacts = 'contacts'
    application = 'application'
    rating = 'rating'
    waitng_for_rate = 'waitng_for_rate'
    questions = 'questions'


class RatingCache:
    cache = {}
    def __init__(self,name,msg):
        self.cache[name] = msg 


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


@dp.message_handler(commands=['start'])
async def startMessage(message):
    await bot.send_message(message.chat.id, infos['welcome_message'], reply_markup=default_menu())
    db_operations.add_state(message.chat.id,Step.start)


@dp.message_handler(text_contains='Назад')
async def backMessage(message):
    await bot.send_message(message.chat.id, 'Выберите действие', reply_markup=default_menu())
    db_operations.add_state(message.chat.id,Step.start)


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.start)
async def firstStep(message):
    if message.text == 'О вузе':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Подробнее о факультетах')
        btn2 = button('Назад')
        menu.row(btn1)
        menu.row(btn2)
        await bot.send_message(message.chat.id, infos['nstu_info'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.vuz)
    if message.text == 'Проф. тестирование':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Техника, машины и механизмы'))
        menu.row(button('Финансы'))
        menu.row(button('Иностранные языки'))
        menu.row(button('Компьютеры и программы'))
        menu.row(button('Физика, химия и энергетика'))
        menu.row(button('Гуманитарные специальности'))
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, infos['test_info'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.prof)
    if message.text == 'Шанс поступить':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['chance_info'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.chance)
    if message.text == 'Контакты':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Приемная комиссия')
        btn2 = button('Деканаты факультетов')
        btn3 = button('Назад')
        menu.row(btn1)
        menu.row(btn2)
        menu.row(btn3)
        await bot.send_message(message.chat.id, infos['contacts_info'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.contacts)
    if message.text == 'Онлайн заявка':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['online_application'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.application)
    if message.text == 'Узнать рейтинг':
        menu = markup(row_width=5, resize_keyboard=True, one_time_keyboard=False)
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
        await bot.send_message(message.chat.id, 'Выберите факультет', reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.rating)
    if message.text == 'Вопросы - Ответы':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['questions_info'], reply_markup=menu)
        db_operations.add_state(message.chat.id,Step.questions)


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.vuz)
async def vuzStep(message):
    if message.text == 'Подробнее о факультетах':
        menu = markup(row_width=5, resize_keyboard=True, one_time_keyboard=False)
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


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.contacts)
async def contactsStep(message):
    if message.text == 'Приемная комиссия':
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        btn1 = button('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id, infos['comission_contacts'], reply_markup=menu)
    if message.text == 'Деканаты факультетов':
        menu = markup(row_width=5, resize_keyboard=True, one_time_keyboard=False)
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


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.application)
async def applicationStep(message):
    menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    btn1 = button('Назад')
    menu.row(btn1)
    await bot.send_message(message.chat.id, infos['online_application'], reply_markup=menu)


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.rating)
async def ratingStep(message):
    if len(message.text) < 10:
        courses = db_operations.get_courses_by_faculty(message.text)
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        for course in courses:
            menu.row(button(course[0]))
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, 'Выберите нужное направление', reply_markup=menu)
    else:
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        RatingCache(message.chat.id,message.text)
        await bot.send_message(message.chat.id,'Введите ФИО', reply_markup=menu)        
        db_operations.add_state(message.chat.id,Step.waitng_for_rate)


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.waitng_for_rate)
async def place_in_rating_Step(message):
    course = RatingCache.cache[message.chat.id]
    menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    menu.row(button('Назад'))
    msg = db_operations.get_rating(course,message.text)
    await bot.send_message(message.chat.id, msg, reply_markup=menu)
    if msg != 'ФИО не найдено':
        del RatingCache.cache[message.chat.id]


@dp.message_handler(lambda message: db_operations.get_state(message.chat.id) == Step.prof)
async def testStep(message):
    key1 = None
    key2 = None
    key3 = None
    # 1 уровень "Техника, машины и механизмы"
    if message.text == 'Техника, машины и механизмы':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Технологии'))
        menu.row(button('Радиотехника'))
        menu.row(button('Летательные аппараты'))
        menu.row(button('Машиностроение'))
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)
    # 2 уровень "Техника, машины и механизмы"
    if message.text == 'Технологии':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Робототехника'))
        menu.row(button('Нанотехнологии'))
        menu.row(button('Оптика'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)  
    # last  
    if message.text == 'Радиотехника':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Летательные аппараты':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    if message.text == 'Машиностроение':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Приборостроение'))
        menu.row(button('Обслуживание и эксплуатация'))
        menu.row(button('Оптика'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu) 
    # 3 уровень "Техника, машины и механизмы"
    # last
    if message.text == 'Приборостроение':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Робототехника':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Нанотехнологии':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Обслуживание и эксплуатация':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Оптика':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)

    # 1 уровень "Финансы"
    if message.text == 'Финансы':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Экономика'))
        menu.row(button('Менеджмент')) 
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)
    # 2 уровень "Финансы"
    # last
    if message.text == 'Менеджмент':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Экономика':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # 1 уровень "Иностранные языки"
    # last        
    if message.text == 'Иностранные языки':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # 1 уровень "Компьютеры и программы"
    if message.text == 'Компьютеры и программы':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Программирование'))
        menu.row(button('Информационная безопасность')) 
        menu.row(button('Автоматизация')) 
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)
    # 2 уровень "Компьютеры и программы"
    # last
    if message.text == 'Программирование':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Информационная безопасность':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # last
    if message.text == 'Автоматизация':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # 1 уровень "Физика, химия и энергетика"
    if message.text == 'Физика, химия и энергетика':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Прикладная физика'))
        menu.row(button('Электроэнергетика и электротехника')) 
        menu.row(button('Физико-химия материалов и процессов')) 
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)
    # 2 уровень "Физика, химия и энергетика"
    # last
    if message.text == 'Прикладная физика':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    if message.text == 'Электроэнергетика и электротехника':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Энергетика'))
        menu.row(button('Экология'))
        await bot.send_message(message.chat.id, 'Выберите интересующую вас область знаний', reply_markup=menu)  
    # last
    if message.text == 'Физико-химия материалов и процессов':
        key2 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)
    # 3 уровень "Физика, химия и энергетика"
    # last
    if message.text == 'Энергетика':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)    
    # last
    if message.text == 'Экология':
        key3 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True) 
    # 1 уровень "Гуманитарные специальности"
    # last
    if message.text == 'Гуманитарные специальности':
        key1 = message.text
        menu = markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
        menu.row(button('Назад'))
        await bot.send_message(message.chat.id, db_operations.get_courses_by_keys(key1,key2,key3), parse_mode='html', reply_markup=menu, disable_web_page_preview=True)

if __name__ == '__main__':
    executor.start_polling(dp)
