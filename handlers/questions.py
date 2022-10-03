from aiogram import Router
from aiogram import types
from aiogram.filters.command import Command
from sqlite_db import BotDB

from keyboards.for_questions import get_keyboard

router = Router()

BotDB = BotDB('user.db')


@router.message(Command(commands=["start", "hello-world", "s"], commands_prefix="/!"))
async def cmd_start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await message.answer(
        f"Привет <b><i>{message.from_user.first_name}</i></b>, что тебя интересует?",
        reply_markup=get_keyboard(), parse_mode='html'
    )
