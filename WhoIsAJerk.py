from ast import parse
from bd import BaseData
from telebot import TeleBot
import logging

from aiogram import Bot, Dispatcher, types, executor
from settings import API_TOKEN, ADMIN_ID, API_TOKEN
from bot import check_admin, BotNotAdmin


logging.basicConfig(level=logging.INFO)
bot_app = TeleBot(API_TOKEN)
bd = BaseData(bot_app)

bot_api = Bot(token=API_TOKEN)
dp = Dispatcher(bot_api)
BOT_ID = API_TOKEN.split(":")[0]


@dp.message_handler(commands=['start', 'help'])
async def hello(message: types.Message):
    await message.answer('Hi')


@dp.message_handler(commands=['who_gandon'])
async def who_gandon(message: types.Message):
    try:
        await check_admin(bot_api, message)
    except BotNotAdmin:
        return
    await message.answer('Ваня Отжариков Гандонище!\nА Димочка умничка')


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    new_member = message.new_chat_members[0]

    if new_member.id == int(BOT_ID):
        await bot_api.send_message(message.chat.id, 'Всем чмоки в этом чатике')
        return

    await bot_api.send_message(
        message.chat.id,
        text=f'Очередной гандон прибыл!\n\n{new_member.mention}'
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
