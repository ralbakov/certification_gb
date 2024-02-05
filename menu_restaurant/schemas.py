from decimal import Decimal

from pydantic import UUID4, BaseModel, Field, StrictInt, StrictStr
from typing_extensions import Annotated


class DishesBase(BaseModel):
    title: StrictStr
    description: StrictStr | None
    price: Annotated[Decimal, Field(decimal_places=2)]


class DishesCreate(DishesBase):
    pass


class DishesUpdate(DishesBase):
    pass


class Dishes(DishesBase):
    id: UUID4
    target_submenu_id: UUID4

    class Config:
        orm_mode = True


class SubmenusBase(BaseModel):
    title: StrictStr
    description: StrictStr | None


class SubmenusCreate(SubmenusBase):
    pass


class SubmenusUpdate(SubmenusBase):
    pass


class Submenus(SubmenusBase):
    id: UUID4
    target_menu_id: UUID4
    dishes_count: StrictInt

    class Config:
        orm_mode = True


class MenusBase(BaseModel):
    title: StrictStr
    description: StrictStr | None


class MenusCreate(MenusBase):
    pass


class MenusUpdate(MenusBase):
    pass


class Menus(MenusBase):
    id: UUID4
    submenus_count: StrictInt
    dishes_count: StrictInt

    class Config:
        orm_mode = True
