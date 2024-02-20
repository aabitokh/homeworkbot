import asyncio
from utils.init_app import init_app
from homeworkbot import bot



async def main():
    await asyncio.gather(
        bot.infinity_polling(request_timeout=90)
    )

if __name__ == '__main__':
    init_app()
    asyncio.run(main())