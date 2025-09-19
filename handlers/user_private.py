from aiogram.filters import CommandStart,Command, or_f
from aiogram.enums import ParseMode
from aiogram import  types, Router, F
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter

from kdbs import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(chat_type=['private']))

@user_private_router.message(or_f(CommandStart(), F.text.lower().contains('привет')))
async def start_cmd(message:types.Message):
    await message.answer('Привет, я торговый бот на солане',
                        reply_markup=reply.start_kb3.as_markup(
                                                        resize_keyboard=True,
                                                        input_field_placeholder="Выберите действие"))

@user_private_router.message(Command('menu'))
async def menu(message:types.Message):
    await message.answer(f"Hello {message.from_user.id}{message.from_user.last_name}")
    await message.reply("<b>Вот меню:\n1. Покупка\n2. Продажа\n3. Проверка баланса\n4. Помощь</b>", reply_markup=reply.del_k)

@user_private_router.message(Command('about'))
async def help(message:types.Message):
    text = as_marked_section("О боте:",Bold("Привет!"), sep='\n')
    await message.answer("О боте:")

@user_private_router.message(F.contact)
async def get_contact(message:types.Message):
    await message.answer(f"Ваш номер: {str(message.contact.phone_number)}")

@user_private_router.message(F.location)
async def get_contact(message:types.Message):
    await message.answer(f"Ваше местоположение: {str(message.location)}")