import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import *
from handlers import common, cat_handler
from midlewares import AlbumsMiddleware


TOKEN = os.environ["TOKEN"]



async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(common.router)
    dp.include_router(cat_handler.router)
    
    middleware = AlbumsMiddleware(0.01)

    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())