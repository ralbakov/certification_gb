from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.models import Dishes, Submenus
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


async def get_dishes(target_menu_id: str,
                     target_submenu_id: str,
                     db: AsyncSession = Depends(get_db)
                     ) -> list[Dishes] | list[None]:
    dishes = await db.execute(select(Dishes)
                              .filter(Dishes.target_submenu_id == target_submenu_id,
                                      Submenus.target_menu_id == target_menu_id
                                      )
                              )

    return dishes.all()


async def create_dish(target_menu_id: str,
                      target_submenu_id: str,
                      dish_schema: DishesCreate,
                      db: AsyncSession = Depends(get_db)) -> dict | ValueError:
    dish = ((await db.execute(select(Dishes)
                              .filter(Submenus.id == target_submenu_id,
                              Submenus.target_menu_id == target_menu_id,
                              Dishes.title == dish_schema.title
                                      )))
            .one_or_none()
            )
    if dish is not None:
        raise ValueError
    dish = Dishes(target_submenu_id=target_submenu_id,
                  title=dish_schema.title,
                  description=dish_schema.description,
                  price=dish_schema.price
                  )
    db.add(dish)
    await db.commit()
    await db.refresh(dish)
    return {'target_dish_id': str(dish.id), 'dish': dish}


async def get_dish(target_menu_id: str,
                   target_submenu_id: str,
                   target_dish_id: str,
                   db: AsyncSession = Depends(get_db)) -> Dishes | None:
    dish = await db.get(Dishes, target_dish_id)
    return dish


async def update_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      dish_schema: DishesUpdate,
                      db: AsyncSession = Depends(get_db)) -> Dishes | None | ValueError:
    dish = await db.get(Dishes, target_dish_id)
    if dish is None:
        return None
    if dish.title == dish_schema.title:
        raise ValueError
    dish.title = dish_schema.title
    dish.description = dish_schema.description
    dish.price = dish_schema.price
    db.add(dish)
    await db.commit()
    await db.refresh(dish)
    return dish


async def delete_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      db: AsyncSession = Depends(get_db)) -> None:
    dish = await db.get(Dishes, target_dish_id)
    await db.delete(dish)
    await db.commit()
    return None
