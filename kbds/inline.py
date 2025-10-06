from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_btns(
        *,
        btns:dict[str,str],
        sizes: tuple[int] = (2,),
        row_width: int = 2,
        placeholder: str = None,
        ):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup(
        row_width=row_width,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    
)

def get_url_btns(
        *,
        btns:dict[str,str],
        sizes: tuple[int] = (2,),
        row_width: int = 2,
        placeholder: str = None,
        ):
    keyboard = InlineKeyboardBuilder()
    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=url))
        
    return keyboard.adjust(*sizes).as_markup(
        row_width=row_width,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    
)

