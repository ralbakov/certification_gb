from pydantic import BaseModel, UUID4
from typing import Optional
from decimal import Decimal


class DishesBase(BaseModel):
    title: str
    description: str | None
    price: Decimal

class DishesCreate(DishesBase):
    pass

class Dishes(DishesBase):
    # target_dish_id: Optional[UUID4]
    target_submenu_id: Optional[UUID4]

    class Config:
        orm_mode = True


class SubmenusBase(BaseModel):
    title: str
    description: str | None

class SubmenusCreate(SubmenusBase):
    pass

class Submenus(SubmenusBase):
    target_submenu_id: Optional[UUID4]
    target_menu_id: Optional[UUID4]
    dishes: list[Dishes] = []
    dishes_count: int

    class Config:
        orm_mode = True


class MenusBase(BaseModel):
    title: str
    description: str | None

class MenusCreate(MenusBase):
    pass

class Menus(MenusBase):
    id: Optional[UUID4]
    target_submenus: list[Submenus] = []
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True