from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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

del_k = ReplyKeyboardRemove()
start_kb2= ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Покупка'),
    KeyboardButton(text='Продажа'),
    KeyboardButton(text='Проверка баланса'),
    KeyboardButton(text='Помощь'),
)
start_kb2.adjust(2)

start_kb3= ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text='Отмена'),)


test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать опрос', request_poll=KeyboardButtonPollType()),

        ],
        [
            KeyboardButton(text='Отправить номер🧏‍♂️', request_contact=True),
            KeyboardButton(text='Отправить местоположение🙆‍♂️', request_location=True),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

