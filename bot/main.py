from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
import aiohttp
import os
import config
import json

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
config.step = 0

with open(BASEDIR + '/info.json','r', encoding='utf-8') as js:
    infos = json.load(js)

def default_menu():
    menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    menu.row(types.KeyboardButton('О вузе'))
    menu.row(types.KeyboardButton('Проф. тестирование'),
    types.KeyboardButton('Шанс поступить'),
    types.KeyboardButton('Узнать рейтинг'))
    menu.row(types.KeyboardButton('Вопросы - Ответы'),
    types.KeyboardButton('Онлайн заявка'),
    types.KeyboardButton('Контакты'))
    return(menu)


@dp.message_handler(commands = ['start'])
async def startMessage(message):    
    await bot.send_message(message.chat.id,infos['welcome_message'],reply_markup=default_menu())
    config.step = 'start'

@dp.message_handler()
async def secondStep(message):  
    if message.text == 'Назад':
        await bot.send_message(message.chat.id,'Выберите действие',reply_markup=default_menu())
        config.step = 'start'
    if message.text == 'О вузе':
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton('Назад')
        menu.row(btn1)
        await bot.send_message(message.chat.id,infos['nstu_info'],reply_markup=menu)
        config.step = message.text
    

if __name__ == '__main__':
    executor.start_polling(dp)