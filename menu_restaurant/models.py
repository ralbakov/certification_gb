from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import select, func, and_
import uuid
from menu_restaurant.database import Base

class Dishes(Base):
    __tablename__ = "dishes"

    target_dish_id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()), autoincrement='ignore_fk')
    target_dish_title = Column(String, nullable=False, unique=True)
    target_dish_description = Column(String, nullable=False)
    target_dish_price = Column(DECIMAL(scale=2), nullable=False)
    target_submenu_id = Column(ForeignKey("submenus.target_submenu_id", ondelete="cascade"))
    
    submenus_ = relationship("Submenus", back_populates="dishes_")


class Submenus(Base):
    __tablename__ = "submenus"

    target_submenu_id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    target_submenu_title = Column(String, nullable=False, unique=True)
    target_submenu_description = Column(String, nullable=False)
    target_menu_id = Column(ForeignKey("menus.target_menu_id", ondelete="cascade"))
    
    dishes_ = relationship("Dishes", back_populates="submenus_")
    menus_ = relationship("Menus", back_populates="submenus_")
    
    
    dishes_count = column_property(
        select(func.count(Dishes.target_dish_id))
        .where(Dishes.target_submenu_id == target_submenu_id)
        .correlate_except(Dishes)
        .scalar_subquery()
    )


class Menus(Base):
    __tablename__ = "menus"

    target_menu_id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    target_menu_title = Column(String, nullable=False, unique=True)
    target_menu_description = Column(String)
    submenus_ = relationship("Submenus", back_populates="menus_")
    submenus_count = column_property(
        select(func.count(Submenus.target_submenu_id))
        .where(Submenus.target_menu_id == target_menu_id)
        .correlate_except(Submenus)
    
    )
    dishes_count = column_property(
        select(func.count(Dishes.target_dish_id))
        .join(Submenus)
        .where(and_(Submenus.target_menu_id == target_menu_id, Submenus.target_submenu_id == Dishes.target_submenu_id))
        .correlate_except(Dishes)
        .scalar_subquery()
    )