import json
from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from handlers.questions import BotDB

router = Router()
media = []


@router.message(Command(commands=("history", "h"), commands_prefix="/!"))
async def hello_world(message: types.Message):
    global media
    records = BotDB.get_records(message.chat.id)
    if records:
        for r in records:
            media = []
            print(r)
            if r[5]:
                photos = json.loads(r[5])
                for i_photo in photos:
                    if i_photo == photos[0]:
                        media.append(types.InputMediaPhoto(type='photo', media=i_photo, caption=
                        f'Name: {r[2]}\n'
                        f'Star rating: {r[3]}\n'
                        f'Current price: {r[4]}\n'
                        f'Request time {r[6]}'
                                                           ))
                    else:
                        media.append(types.InputMediaPhoto(type='photo', media=i_photo))
                await message.answer_media_group(media=media)
            else:
                await message.answer(text=f'Name: {r[2]}\n'
                                          f'Star rating: {r[3]}\n'
                                          f'Current price: {r[4]}\n'
                                          f'Request time {r[6]}'
                                     )
    else:
        await message.answer(text='Вы еще не делали запросов. Начните новый запрос с помощью команды (/start)')
