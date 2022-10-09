from aiogram import Router
from aiogram import types
from aiogram.filters.command import Command
from sqlite_db import BotDB
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.for_questions import get_keyboard

router = Router()

BotDB = BotDB()


@router.message(Command(commands=["start", "hello-world", "s"], commands_prefix="/!"))
async def hello_world(message: types.Message, state: FSMContext):
    await state.set_state(state=None)
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await message.answer(
        f"Привет <b><i>{message.from_user.first_name}</i></b>!\n"
        "Чтобы посмотреть список самых <b>дешевых</b> отелей введи /lowprice.\n"
        "Для самых <b>дорогих</b> отелей лучше использовать /highprice.\n"
        "Если тебе нужно выбрать отель, <b>наиболее подходящих по цене и расположению от центра</b> то лучше "
        "использовать /bestdeal\n"
        "Посмотреть, что еще умеет бот можно с помощью команды /help", parse_mode='html')
