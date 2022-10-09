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
async def clear_history(message: types.Message, state: FSMContext):
    """
    Функция по очистке истории. Вопрос нужно ли отчистить
    :param message: команда
    :param state: состояние
    :return: None
    """
    await message.answer('Вы действительно хотите очистить историю?', reply_markup=get_yes_no_kb())
    await state.set_state(OrderFood.get_delete)

    @router.callback_query(Text(text="yes"), OrderFood.get_delete)
    async def callback(callback: types.CallbackQuery):
        """
        Функция по очистке с положительным вопросом
        :param callback: Да
        :return: очищает историю
        """
        message = callback.message
        record = BotDB.get_records(message.chat.id)
        if record:
            BotDB.get_del_records(message.chat.id)
            await message.answer('Ваша история удалена. Начните новый запрос с помощью команды (/start)')
        else:
            await message.answer(text='Вы еще не делали запросов. Начните новый запрос с помощью команды (/start)')

    @router.callback_query(Text(text="no"), OrderFood.get_delete)
    async def callback(callback: types.CallbackQuery):
        """
        Функция по очистке с отрицательным вопросом
        :param callback: Нет
        :return: не очищает историю
        """
        message = callback.message
        await message.answer('Начните новый запрос с помощью команды (/start)')

