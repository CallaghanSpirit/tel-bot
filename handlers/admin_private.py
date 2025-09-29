from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_product(message: types.Message):
    await message.answer("ОК, вот список товаров")


@admin_router.message(F.text == "Изменить товар")
async def change_product(message: types.Message):
    await message.answer("ОК, вот список товаров")


@admin_router.message(F.text == "Удалить товар")
async def delete_product(message: types.Message, counter):
    await message.answer("Выберите товар(ы) для удаления")


#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        "AddProduct:name": "Введите название товара",
        "AddProduct:description": "Введите описание товара",
        "AddProduct:price": "Введите стоимость товара",
        "AddProduct:image": "Загрузите изображение товара",
    }

@admin_router.message(StateFilter(None),F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)
    print(AddProduct.__all_states__)



@admin_router.message(StateFilter("*"),Command("отмена"))
@admin_router.message(StateFilter("*"),F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активных действий", reply_markup=ADMIN_KB)
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"),Command("назад"))
@admin_router.message(StateFilter("*"),F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer("Нет прошлого шага")
        return
    
    prev_state = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(prev_state)
            await message.answer(f"ок, вы вернулись к прошлому шагу \n{AddProduct.texts[prev_state.state]}")
            return
        prev_state = step


@admin_router.message(AddProduct.name,F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):

    await message.answer("Пожалуйста, введите текстом название товара")




@admin_router.message(AddProduct.description,F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.price,F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image,F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)

    data = await state.get_data()
    try:
        await orm_add_product(
            session=session,
            data=data)
        
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB)

    await state.clear()  # Завершаем машину состояний, очищая все данные
