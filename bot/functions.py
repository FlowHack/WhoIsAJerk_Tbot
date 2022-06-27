import datetime as dt
from random import choice as rand_choice

import pytz
import scheduler.trigger as trigger
from aiogram import Bot, types
from pytz import timezone as pytz_timezone

from settings import API_TOKEN

from .keyboards import KEYBOARDS


async def check_admin(bot_api: Bot, id_group: int, id_user: int,
                      return_user: bool = False):
    """Функция проверки, является ли пользователь tg админом

    Args:
        bot_api (Bot): ОбЪект бота
        id_group (int): id группы в tg
        id_user (int): id пользователя, которого нужно проверить
        return_user (bool): Нужно ли возвращать объект пользователя. Defaults
        to False.

    Returns:
        (bool, dict[str, (bool, User)]): Возвращает либо булево значение,
        является ли админом, либо словарь, где 'admin' - является ли
        админом, а 'user' - объекта пользователя tg
    """
    user = await bot_api.get_chat_member(
        id_group, id_user
    )

    return user.status in ['administrator', 'creator'] if return_user  \
        is False else {
            'admin': user.status in ['administrator', 'creator'],
            'user': user
    }


async def check_group(message: types.Message, db, return_group: bool = False,
                      fraze_exist: str = None,
                      fraze_none: str = 'none_this_group',
                      keyboard_exist: types.InlineKeyboardMarkup = None,
                      keyboard_none: types.InlineKeyboardMarkup = KEYBOARDS['start']):  # noqa: E501
    """Функция определяет, есть ли такая группа в базе данных

    Args:
        message (types.Message): Объект сообщения tg
        db (BaseDataRequests): Класс Базы данных
        return_group (bool, optional): Возвращать ли группу. Defaults to False.
        fraze_exist (str, optional): Фраза, которую надо отправить, если
        имется такая группа. Defaults to None.
        fraze_none (str, optional): Фраза, которую надо отправить, если
        нет такой группы. Defaults to 'none_this_group'.
        keyboard_exist (types.InlineKeyboardMarkup, optional): Клавиатура,
        которую надо прикрепить, если имеется такая группа. Defaults to None.
        keyboard_none (types.InlineKeyboardMarkup, optional): Клавиатура,
        которую надо прикрепить, если нет такой группы. Defaults to
        KEYBOARDS['start'].

    Returns:
        (bool, dict[str, (bool, Group)]): Возвращает либо булево значение,
        есть ли такая группа, либо словарь, где 'result' - имеется ли,
        а 'group' - словарь группы
    """
    id_group = message.chat.id
    group = db.get(
        'groups', ['*' if return_group else 'id'],
        f'id_group={id_group}', exists=False if return_group else True
    )

    if return_group:
        if group is None:
            if fraze_none is not None:
                await message.answer(
                    db.get(
                        'frazes', ['text_fraze'], f'action="{fraze_none}"'
                    ), reply_markup=keyboard_none
                )
            return {'result': False, 'group': group}
        if fraze_exist is not None:
            await message.answer(
                db.get(
                    'frazes', ['text_fraze'], f'action="{fraze_exist}"'
                ), reply_markup=keyboard_exist
            )
        return {'result': True, 'group': group}

    if group and fraze_exist is not None:
        await message.answer(
            db.get(
                'frazes', ['text_fraze'], f'action="{fraze_exist}"'
            ), reply_markup=keyboard_exist
        )
    if not group and fraze_none is not None:
        await message.answer(
            db.get(
                'frazes', ['text_fraze'], f'action="{fraze_none}"'
            ), reply_markup=keyboard_none
        )

    return group


async def check_bot_admin(bot_api: Bot, message: types.Message,
                          db_requests, return_user_admin: bool = False,
                          user_id: int = None, return_user: bool = False):
    """Функция определяет, является ли администратором бот и пользователь,
    который запросил команду. В завиимости от результата отправляется сообщение

    Args:
        bot_api (Bot): Объект бота tg
        message (types.Message): Объект сообщения tg
        db_requests (BaseDataRequests): База данных
        return_user_admin (bool, optional): Нужно ли вернуть результат,
        является ли пользователь админом. Defaults to False.
        user_id (int): id пользователя tg. Defaults to None.
        return_user (bool, optional): Возвращать ли пользователя. Defaults to
        False.
    """
    user_admin = await check_admin(
        bot_api, message.chat.id,
        message.from_user.id if user_id is None else user_id,
        return_user=return_user
    )
    bot_admin = await check_admin(
        bot_api, message.chat.id, API_TOKEN.split(':')[0]
    )

    if not bot_admin:
        if not return_user:
            fraze = 'bot_not_admin' if user_admin  \
                else 'bot_not_admin_and_user_to'
            text = db_requests.get(
                'frazes', ['text_fraze'], f'action="{fraze}"'
            )
            result = {'bot': False, 'user': user_admin} if return_user_admin  \
                else False
        else:
            fraze = 'bot_not_admin' if user_admin['admin']  \
                else 'bot_not_admin_and_user_to'
            text = db_requests.get(
                'frazes', ['text_fraze'], f'action="{fraze}"'
            )
            result = {
                'bot': False,
                'user_admin': user_admin['admin'],
                'user': user_admin['user']
            } if return_user_admin else {
                'bot': False, 'user': user_admin['user']
            }
        await message.answer(text, parse_mode='Markdown')
        return result

    if return_user:
        return {
            'bot': True,
            'user_admin': user_admin['admin'],
            'user': user_admin['user']
        } if return_user_admin else {
            'bot': True, 'user': user_admin['user']
        }
    else:
        return {'bot': True, 'user': user_admin} if return_user_admin else True


async def create_sheduller_if_start(db_get):
    pass


async def sheduller(timezone: str, schedule, bot, id, task, db_get, db_update,
                    daily=True):
    TIMEZONE = pytz.timezone(timezone)
    trigger_ist = dt.time(hour=0, tzinfo=TIMEZONE)
    if daily:
        schedule.daily(
            trigger_ist, lambda: task(bot, db_get, db_update),
            args=(TIMEZONE,), id=str(id)
        )


def get_random_rank(db):
    """Функция получается раномный ранг

    Args:
        db (BaseDataRequests): Класс базу данных

    Returns:
        dict: Словарь ранга
    """
    ranks = db.get('ranks', ['*'], many=True)
    return rand_choice(ranks)


def get_now_date(timezone: str) -> dt.datetime.date:
    """Вычисляет нынешнюю дату в зависимости от таймзоны

    Args:
        timezone (str): Таймзона, для которой необходимо вычислить дату

    Returns:
        dt.datetime.date: Дата
    """
    return dt.datetime.now(tz=pytz_timezone(timezone)).date()


def get_difference_day(date: str, timezone: str):
    """Функция вычисляет разницу между датами в днях

    Args:
        date (str): Дата от которой ведётся отсчёт дней
        timezone (str): Таймзона для которой необходимо вчислить

    Returns:
        int, dt.datetime.date: Возвращает разницу в днях и сегодняшнюю дату
    """
    date_today = dt.datetime.now(tz=pytz_timezone(timezone)).date()
    date = dt.datetime.strptime(date, '%Y-%m-%d').date()

    difference = date_today - date
    return difference.days, date_today


def plus_count_request(db) -> None:
    date = get_now_date('UTC')

    if db.get('stat_requests', where=f'date={date}', exists=True):
        requests = int(db.get('stat_requests', ['requests'], f'date={date}'))
        requests += 1
        db.update_stat_requests(date, requests)
        return

    request = f'''
INSERT INTO stat_requests(date, requests) VALUES
({date}, 1)
'''
    db.post_request(request)
