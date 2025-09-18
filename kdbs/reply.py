from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Покупка'),
            KeyboardButton(text='Продажа'),
        ],
        [
            KeyboardButton(text='Проверка баланса'),
            KeyboardButton(text='Помощь'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)