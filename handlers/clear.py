from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from keyboards.for_questions import get_yes_no_kb
from handlers.questions import BotDB
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class OrderFood(StatesGroup):
    get_delete = State()


@router.message(Command(commands=("clear", "c"), commands_prefix="/!"))
async def hello_world(message: types.Message, state: FSMContext):
    await message.answer('Вы действительно хотите очистить историю?', reply_markup=get_yes_no_kb())
    await state.set_state(OrderFood.get_delete)

    @router.callback_query(Text(text="yes"))
    async def callback(callback: types.CallbackQuery):
        message = callback.message
        BotDB.get_del_records(message.chat.id)
        await message.answer('Ваша история удалена. Начните новый запрос с помощью команды (/start)')

    @router.callback_query(Text(text="no"))
    async def callback(callback: types.CallbackQuery):
        message = callback.message
        await message.answer('Начните новый запрос с помощью команды (/start)')

