from aiogram import Bot, Dispatcher, types
import asyncio

bot=Bot(token='8363227513:AAHv8gm6oGzoZ5WAD119SLUl_XqHE0ERYPs')
dp=Dispatcher()

@dp.message(commands=['start'])
async def start_cmd(message:types.Message):
    await message.answer('Hello')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())