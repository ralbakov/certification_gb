from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.models import Menus
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


async def get_menus(db: AsyncSession = Depends(get_db)) -> list[Menus] | list[None]:
    result = await db.execute(select(Menus))
    return result.all()


async def get_menu(target_menu_id: str,
                   db: AsyncSession = Depends(get_db)) -> Menus | None:
    menu = await db.get(Menus, target_menu_id)
    return menu


async def create_menu(menu_schema: MenusCreate,
                      db: AsyncSession = Depends(get_db)
                      ) -> dict | ValueError:
    menu = Menus(title=menu_schema.title,
                 description=menu_schema.description)
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return {'target_menu_id': str(menu.id), 'menu': menu}


async def update_menu(target_menu_id: str,
                      menu_schema: MenusUpdate,
                      db: AsyncSession = Depends(get_db),
                      ) -> Menus | None:
    menu = await db.get(Menus, target_menu_id)
    if menu is None:
        return None
    menu.title = menu_schema.title
    menu.description = menu_schema.description
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def delete_menu(target_menu_id: str, db: AsyncSession = Depends(get_db)) -> None:
    menu = await db.get(Menus, target_menu_id)
    await db.delete(menu)
    await db.commit()
    return None
