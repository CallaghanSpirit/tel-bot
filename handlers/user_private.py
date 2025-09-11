from aiogram.filters import CommandStart,Command, or_f
from aiogram import  types, Router, F
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(chat_type=['private']))

@user_private_router.message(or_f(CommandStart(), F.text.lower().contains('привет')))
async def start_cmd(message:types.Message):
    await message.answer('Привет, я торговый бот на солане')

@user_private_router.message(Command('menu'))
async def menu(message:types.Message):
    await message.answer(f"Hello {message.from_user.id}{message.from_user.last_name}")
    await message.reply("Вот меню:\n1. Покупка\n2. Продажа\n3. Проверка баланса\n4. Помощь")

@user_private_router.message(Command('about'))
async def help(message:types.Message):
    await message.answer("О боте:")


