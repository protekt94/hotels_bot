from aiogram import Router
from aiogram import types
from aiogram.filters.command import Command


from keyboards.for_questions import get_keyboard

router = Router()


@router.message(Command(commands=["start", "hello-world"]))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет {message.from_user.first_name}, что тебя интересует?",
        reply_markup=get_keyboard()
    )
