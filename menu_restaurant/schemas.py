from pydantic import UUID4, BaseModel, StrictInt, StrictStr


class DishesBase(BaseModel):
    title: StrictStr
    description: StrictStr | None
    price: StrictStr


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
