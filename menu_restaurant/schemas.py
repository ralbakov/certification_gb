from pydantic import BaseModel, UUID4, StrictStr, StrictInt, StrictFloat

class DishesBase(BaseModel):
    title: StrictStr
    description: StrictStr | None
    price: StrictStr

class DishesCreate(DishesBase):
    pass

class Dishes(DishesBase):
    target_dish_id: UUID4
    target_submenu_id: UUID4

    class Config:
        orm_mode = True


class SubmenusBase(BaseModel):
    title: StrictStr
    description: StrictStr | None

class SubmenusCreate(SubmenusBase):
    pass

class Submenus(SubmenusBase):
    target_submenu_id: UUID4
    target_menu_id: UUID4
    dishes: list[Dishes] = []
    dishes_count: StrictInt

    class Config:
        orm_mode = True


class MenusBase(BaseModel):
    title: StrictStr
    description: StrictStr | None

class MenusCreate(MenusBase):
    pass

class Menus(MenusBase):
    id: UUID4
    target_submenus: list[Submenus] = []
    submenus_count: StrictInt
    dishes_count: StrictInt

    class Config:
        orm_mode = True