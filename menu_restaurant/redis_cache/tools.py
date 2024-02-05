import os
import pickle

import redis
from dotenv import load_dotenv

from menu_restaurant import models

load_dotenv()

HASH_NAME: str = 'full_menu'
"""Переменная для присвоения имению хэшу"""


class RedisCache:
    """Класс для установки соединения с redis и работой с кешем."""
    __rd = redis.Redis(host=f"{os.getenv('REDIS_HOST')}", port=os.getenv('REDIS_PORT'))  # type: ignore

    @classmethod
    def get_all_menu(cls) -> list[models.Menus] | None:
        """Получить все меню из кэша redis."""

        result = cls.__rd.hvals(HASH_NAME)
        if result:
            all_menu = [pickle.loads(item_menu) for item_menu in result]
            return all_menu
        return []

    @classmethod
    def set_menu(cls, id: str, menu: models.Menus) -> None:
        """Записать меню в кэш redis."""

        cls.__rd.hset(HASH_NAME, id, pickle.dumps(menu))

    @classmethod
    def update_menu(cls, id: str, menu: models.Menus) -> None:
        """Обновить запись меню в кэше redis."""

        cls.__rd.hset(HASH_NAME, id, pickle.dumps(menu))

    @classmethod
    def get_menu(cls, id: str) -> models.Menus | None:
        """Получить меню из кэша redis."""

        result = cls.__rd.hget(HASH_NAME, id)
        if result:
            menu = pickle.loads(result)
            return menu
        return None

    @classmethod
    def delete_menu(cls, id: str) -> dict[str, str]:
        """Удалить меню из кэша redis."""

        all_keys_submenu = cls.__rd.hkeys(id)
        for item_submenu in all_keys_submenu:
            all_keys_dish = cls.__rd.hkeys(item_submenu)
            for item_dish in all_keys_dish:
                cls.__rd.hdel(item_submenu, item_dish)
            cls.__rd.hdel(id, item_submenu)

        cls.__rd.hdel(HASH_NAME, id)
        return {'message': 'menu deleted'}

    @classmethod
    def get_all_keys_menu(cls):
        """Получить все ключи (id) кеша меню"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(HASH_NAME)]

    @classmethod
    def get_all_submenu(cls, target_menu_id: str) -> list[models.Submenus] | None:
        """Получить все подменю из кэша redis."""

        result = cls.__rd.hvals(target_menu_id)
        if result:
            all_submenu = [pickle.loads(item_submenu) for item_submenu in result]
            return all_submenu
        return []

    @classmethod
    def set_submenu(cls, target_menu_id: str, id: str, submenu: models.Submenus) -> None:
        """Записать подменю в кэш redis."""

        cls.__rd.hset(target_menu_id, id, pickle.dumps(submenu))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_submenu = pickle.loads(get_menu)  # type: ignore
        change_menu_count_submenu.submenus_count += 1
        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_submenu))

    @classmethod
    def update_submenu(cls, target_menu_id: str, id: str, submenu: models.Submenus) -> None:
        """Обновить запись подменю в кэше redis."""

        cls.__rd.hset(target_menu_id, id, pickle.dumps(submenu))

    @classmethod
    def get_submenu(cls, target_menu_id: str, id: str) -> models.Submenus | None:
        """Получить подменю из кэша redis."""

        result = cls.__rd.hget(target_menu_id, id)
        if result:
            submenu = pickle.loads(result)
            return submenu
        return None

    @classmethod
    def delete_submenu(cls, target_menu_id: str, id: str) -> dict[str, str]:
        """Удалить подменю из кэша redis."""

        all_keys_dish = cls.__rd.hkeys(id)
        for item in all_keys_dish:
            cls.__rd.hdel(id, item)

        cls.__rd.hdel(target_menu_id, id)

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_submenu = pickle.loads(get_menu)  # type: ignore
        change_menu_count_submenu.submenus_count -= 1
        change_menu_count_submenu.dishes_count = 0
        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_submenu))

        return {'message': 'submenu deleted'}

    @classmethod
    def get_all_keys_submenu(cls, target_menu_id: str):
        """Получить все ключи (id) кеша подменю"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(target_menu_id)]

    @classmethod
    def get_all_dish(cls, target_submenu_id: str) -> list[models.Dishes] | None:
        """Получить все блюда из кэша redis."""

        result = cls.__rd.hvals(target_submenu_id)
        if result:
            all_dish = [pickle.loads(item_dish) for item_dish in result]
            return all_dish
        return []

    @classmethod
    def set_dish(cls, target_menu_id: str, target_submenu_id: str, id: str, dish: models.Dishes) -> None:
        """Записать блюдо в кэш redis."""

        cls.__rd.hset(target_submenu_id, id, pickle.dumps(dish))

        get_submenu = cls.__rd.hget(target_menu_id, target_submenu_id)
        change_submenu_count_dish = pickle.loads(get_submenu)  # type: ignore
        change_submenu_count_dish.dishes_count += 1
        cls.__rd.hset(target_menu_id, target_submenu_id, pickle.dumps(change_submenu_count_dish))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_dish = pickle.loads(get_menu)  # type: ignore
        change_menu_count_dish.dishes_count += 1
        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_dish))

    @classmethod
    def update_dish(cls, target_submenu_id: str, id: str, dish: models.Dishes) -> None:
        """Обновить запись блюда в кэше redis."""

        cls.__rd.hset(target_submenu_id, id, pickle.dumps(dish))

    @classmethod
    def get_dish(cls, target_submenu_id: str, id: str) -> models.Dishes | None:
        """Получить блюдо из кэша redis."""

        result = cls.__rd.hget(target_submenu_id, id)
        if result:
            dish = pickle.loads(result)
            return dish
        return None

    @classmethod
    def delete_dish(cls, target_menu_id: str, target_submenu_id: str, id: str) -> dict[str, str]:
        """Удалить бдюдо из кэша redis."""

        cls.__rd.hdel(target_submenu_id, id)

        get_submenu = cls.__rd.hget(target_menu_id, target_submenu_id)
        change_submenu_count_dish = pickle.loads(get_submenu)  # type: ignore
        change_submenu_count_dish.dishes_count -= 1
        cls.__rd.hset(target_menu_id, target_submenu_id, pickle.dumps(change_submenu_count_dish))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_dish = pickle.loads(get_menu)  # type: ignore
        change_menu_count_dish.dishes_count -= 1
        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_dish))

        return {'message': 'dish deleted'}

    @classmethod
    def get_all_keys_dishes(cls, target_submenu_id: str):
        """Получить все ключи (id) кеша блюда"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(target_submenu_id)]
