from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def get_select_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Топ самых дешёвых отелей')
    kb.button(text='Топ самых дорогих отелей')
    kb.button(text='Наиболее подходящие по цене и расположению от центра')
    kb.button(text='История поиска отелей')
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="no"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Топ самых дешёвых отелей", callback_data="/lowprice")
        ],
        [
            types.InlineKeyboardButton(text="Топ самых дорогих отелей", callback_data="/highprice")
        ],
        [
            types.InlineKeyboardButton(text="История поиска отелей", callback_data="history")
        ],
        [
            types.InlineKeyboardButton(text="Наиболее подходящие по цене и расположению от центра",
                                       callback_data="/bestdeal")
        ],
        [
            types.InlineKeyboardButton(text='Возможности бота', callback_data="/help")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard
