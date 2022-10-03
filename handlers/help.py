from aiogram import Router, types
from aiogram.filters.text import Text

router = Router()


@router.callback_query(Text(text='/help'))
async def hello_world(callback: types.CallbackQuery):
    await callback.message.answer('/help - помощь по командам бота\n'
                                  '/lowprice - вывод самых дешевых отелей\n'
                                  '/highprice - вывод самых дорогих отелей\n'
                                  '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра.\n'
                                  '/clear - удаление истории поиска\n'
                                  '/history - вывод истории поиска'
                                  )
