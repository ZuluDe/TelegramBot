import asyncio
from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import bot_messages, user_commands, questionaire, liked



async def main():
    bot= Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        questionaire.router,
        liked.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())