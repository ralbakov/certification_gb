from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.models import Submenus
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


async def get_submenus(target_menu_id: str,
                       db: AsyncSession = Depends(get_db),
                       ) -> list[Submenus] | list[None]:
    submenu = await db.execute(select(Submenus)
                               .filter(Submenus.target_menu_id == target_menu_id))
    return submenu.all()


async def create_submenu(target_menu_id: str,
                         submenu: SubmenusCreate,
                         db: AsyncSession = Depends(get_db),
                         ) -> dict[str, str]:
    submenu = (Submenus(target_menu_id=target_menu_id,
                        title=submenu.title,
                        description=submenu.description
                        )
               )
    db.add(submenu)
    await db.commit()
    await db.refresh(submenu)
    return {'target_submenu_id': str(submenu.id), 'submenu': submenu}


async def get_submenu(target_submenu_id: str,
                      db: AsyncSession = Depends(get_db),
                      ) -> Submenus | None:
    submenu = await db.get(Submenus, target_submenu_id)
    return submenu


async def update_submenu(target_submenu_id: str,
                         submenu: SubmenusUpdate,
                         db: AsyncSession = Depends(get_db)) -> Submenus | None:
    db_update_submenu = await db.get(Submenus, target_submenu_id)
    if db_update_submenu is None:
        return None
    db_update_submenu.title = submenu.title
    db_update_submenu.description = submenu.description
    db.add(db_update_submenu)
    await db.commit()
    await db.refresh(db_update_submenu)
    return db_update_submenu


async def delete_submenu(target_submenu_id: str,
                         db: AsyncSession = Depends(get_db)) -> None:
    submenu = await db.get(Submenus, target_submenu_id)
    await db.delete(submenu)
    await db.commit()
    return None
