import uuid

from sqlalchemy import Column, ForeignKey, String, and_, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from menu_restaurant.database.confdb import Base


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    target_submenu_id = Column(ForeignKey('submenus.id', ondelete='cascade'))

    submenus_ = relationship('Submenus', back_populates='dishes_')


class Submenus(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    target_menu_id = Column(ForeignKey('menus.id', ondelete='cascade'))

    dishes_ = relationship('Dishes', back_populates='submenus_')
    menus_ = relationship('Menus', back_populates='submenus_')

    dishes_count = column_property(
        select(func.count(Dishes.id))
        .where(Dishes.target_submenu_id == id)
        .correlate_except(Dishes)
        .scalar_subquery()
    )


class Menus(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    submenus_ = relationship('Submenus', back_populates='menus_')
    submenus_count = column_property(
        select(func.count(Submenus.id))
        .where(Submenus.target_menu_id == id)
        .correlate_except(Submenus)
        .scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dishes.id))
        .join(Submenus)
        .where(and_(Submenus.target_menu_id == id,
                    Submenus.id == Dishes.target_submenu_id)
               )
        .correlate_except(Dishes)
        .scalar_subquery()
    )
