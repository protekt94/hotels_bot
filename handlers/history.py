from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from handlers.questions import BotDB

router = Router()


@router.message(Command(commands=("history", "h"), commands_prefix="/!"))
async def hello_world(message: types.Message):
    records = BotDB.get_records(message.chat.id)
    if records:
        for r in records:
            await message.answer(text=f'Name: {r[2]}\n'
                                      f'Star rating: {r[3]}\n'
                                      f'Current price: {r[4]}\n'
                                      f'Request time" {r[5]}'
                                 )
    else:
        await message.answer(text='Вы еще не делали запросов. Начните новый запрос с помощью команды (/start)')


