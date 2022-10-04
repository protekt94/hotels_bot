import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import questions, low_high_price, bestdeal, history, clear, help


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token="5546523733:AAGz1My1HV2VDnvhedZ7efgUBPfSK7GUlos")

    dp.include_router(questions.router)
    dp.include_router(low_high_price.router)
    dp.include_router(bestdeal.router)
    dp.include_router(history.router)
    dp.include_router(clear.router)
    dp.include_router(help.router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
