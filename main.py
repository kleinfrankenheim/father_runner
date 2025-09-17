import asyncio
import os

from aiogram import Bot, Dispatcher

from handlers import help, frame_bot, feedback, characters_list

from dotenv import load_dotenv

load_dotenv()

fatherrunner_token = os.getenv('FATHERRUNNER_TOKEN')


async def main():
    bot = Bot(token=fatherrunner_token)
    dp = Dispatcher()

    dp.include_routers(frame_bot.router, help.router, feedback.router, characters_list.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
