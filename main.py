from asyncio import run
from logging import basicConfig, INFO

from config import Bot
from modules import start, state_handler, admin

bot = Bot()

async def runner():
    bot.dp.include_routers(start.router, state_handler.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.dp.start_polling(bot)

if __name__ == "__main__":
    basicConfig(level=INFO)
    run(runner())
