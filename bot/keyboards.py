from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_timezones():
    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = [
        InlineKeyboardButton(
            str(i), callback_data=f'timezone_btn_{i}'
        ) for i in range(1, 12)
    ]

    keyboard.add(*buttons[0:5])
    keyboard.add(*buttons[5:10])
    keyboard.add(buttons[10])

    return keyboard


def kb_start():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            'Установить таймзону', callback_data='set_timezone'
        )
    )

    return keyboard


def kb_join_game():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            'Присоедениться к игре', callback_data='join_game'
        )
    )

    return keyboard


def kb_admin_panel():
    keyboard = InlineKeyboardMarkup(row_width=3)

    keyboard.add(
        InlineKeyboardButton('Фразы', callback_data='admin_show_frazes')
    )
    keyboard.add(
        *[
            InlineKeyboardButton(
                'Изменить', callback_data='admin_edit_fraze'
            ),
            InlineKeyboardButton(
                'SQL', callback_data='admin_sql_frazes'
            ),
        ]
    )
    keyboard.add(
        InlineKeyboardButton('Ранги', callback_data='admin_show_ranks')
    )
    keyboard.add(
        *[
            InlineKeyboardButton(
                'Добавить', callback_data='admin_add_rank'
            ),
            InlineKeyboardButton(
                'Изменить', callback_data='admin_edit_rank',
            ),
            InlineKeyboardButton(
                'SQL', callback_data='admin_sql_ranks',
            )
        ]
    )
    keyboard.add(
        InlineKeyboardButton(
            'Статистика', callback_data='admin_show_stats'
        )
    )

    return keyboard


KEYBOARDS = {
    'set_timezone': kb_timezones(),
    'start': kb_start(),
    'admin_panel': kb_admin_panel(),
    'join_game': kb_join_game(),
}
