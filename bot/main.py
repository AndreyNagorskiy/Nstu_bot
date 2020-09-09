from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
import aiohttp
import os
import config

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
config.step = 0


@dp.message_handler(commands=['start'])
async def startMessage(message: types.Message):
    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('О вузе')
    menu.row(btn1)
    await bot.send_message(message.chat.id, 'Хуюзе', reply_markup=menu)
    config.step = 0
    print(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp)
