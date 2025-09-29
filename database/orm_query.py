
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from sqlalchemy import select, update, delete


async def  orm_add_product(session: AsyncSession, data: dict):
    

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image=data['image']
    )
    session.add(new_product)
    await session.commit()
    # await session.refresh(new_product)
    # return new_product

async def orm_get_all_products(session: AsyncSession):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return products

async def orm_get_product_by_id(session: AsyncSession, product_id: int):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    return product

async def orm_update_product(session: AsyncSession, product_id: int, data: dict):
    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image=data['image'],
    )
    await session.execute(query)
    await session.commit()

async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()