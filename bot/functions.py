from settings import API_TOKEN
from aiogram import types, Bot
from .exceptions import BotNotAdmin


async def check_admin(bot: Bot, message: types.Message):
    member = await bot.get_chat_member(
        message.chat.id, API_TOKEN.split(":")[0]
    )

    if not isinstance(member, types.ChatMemberAdministrator):
        await bot.send_message(
            chat_id=message.chat.id,
            text='Ах ты гандон! В админы кто добавлять будет!?'
        )
        raise BotNotAdmin(f'Бот не админ в группе {message.chat.id}')
    else:
        return True
