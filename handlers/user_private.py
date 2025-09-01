from aiogram.filters import CommandStart,Command
from aiogram import  types, Router

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message:types.Message):
    await message.answer('Привет, я торговый бот на солане')

@user_private_router.message(Command('menu'))
async def menu(message:types.Message):
    await message.answer(f"Hello {message.from_user.id}{message.from_user.last_name}")
    await message.reply("Вот меню:\n1. Покупка\n2. Продажа\n3. Проверка баланса\n4. Помощь")