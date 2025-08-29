from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart

bot=Bot(token='8363227513:AAHv8gm6oGzoZ5WAD119SLUl_XqHE0ERYPs')
dp=Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message:types.Message):
    await message.answer('Hello')

@dp.message()
async def echo(message:types.Message):
    await message.answer(f"Hello {message.from_user.id}{message.from_user.last_name}")
    await message.reply(message.text)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

  
asyncio.run(main())