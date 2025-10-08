from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, or_f
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard
from kbds.inline import get_callback_btns

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import *



admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент товаров",
    placeholder="Выберите действие",
    sizes=(2,),
)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    product_for_change = None

    texts = {
        "AddProduct:name": "Введите название товара",
        "AddProduct:description": "Введите описание товара",
        "AddProduct:price": "Введите стоимость товара",
        "AddProduct:image": "Загрузите изображение товара",
    }


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Ассортимент товаров")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_all_products(session=session):
        await message.answer_photo(product.image, 
                                caption=f"<strong>{product.name}</strong>\n{product.description}\nCтоимость: {round(product.price,2)} руб.",
                                reply_markup=get_callback_btns(btns={
                                    "Удалить": f"delete_{product.id}",
                                    "Редактировать": f"edit_{product.id}"
                                    }))
    await message.answer("ОК, вот список товаров")

@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session=session, product_id=int(product_id))
    await callback.message.answer("Товар удален", reply_markup=ADMIN_KB)
    await callback.answer("Товар удален")

@admin_router.callback_query(StateFilter(None),F.data.startswith("edit_"))
async def edit_product(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm_get_product_by_id(session=session, product_id=int(product_id))

    AddProduct.product_for_change = product_for_change
    await callback.answer()
    await callback.message.answer("Введите новое название товара", reply_markup=types.ReplyKeyboardRemove()
                                        )
    await state.set_state(AddProduct.name)

#Код ниже для машины состояний (FSM)


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
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
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


@admin_router.message(AddProduct.name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text)


    
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):

    await message.answer("Пожалуйста, введите текстом название товара")




@admin_router.message(AddProduct.description,or_f(F.text, F.text == "."))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)

    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.price,or_f(F.text, F.text == "."))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            message.text = float(message.text)
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB)
            return
        await state.update_data(price=message.text)

    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image,or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session=session,product_id=AddProduct.product_for_change.id,data=data)
            await message.answer("Товар обновлен", reply_markup=ADMIN_KB)

        else: 
            await orm_add_product(session=session,data=data)
            await message.answer("Товар добавлен", reply_markup=ADMIN_KB)

        
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB)
    finally:
        await state.clear()


    # Завершаем машину состояний, очищая все данные
