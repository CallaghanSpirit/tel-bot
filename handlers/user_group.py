from string import punctuation
from aiogram import F, types, Router
from filters.chat_types import ChatTypeFilter

user_group_router =  Router()
user_group_router.message.filter(ChatTypeFilter(chat_type=['group', 'supergroup']))

restricted_words = {"мудак", "тварь", "ублюдок"}

def clean_text(text:str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.edited_message()
@user_group_router.message()
async def restricted_words_filter(message:types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):

        await message.answer(f"{message.from_user.username}, не сквернословить!")


        await message.delete()
