import pickle

import redis

from menu_restaurant import models

HASH_NAME: str = 'full_menu'
"""Переменная для присвоения имению хэшу"""


class RedisCache:
    """Класс для установки соединения с redis и работой с кешем."""

    rd = redis.Redis(host='localhost', port=6379)

    @classmethod
    def get_all_menu(cls) -> list[models.Menus] | None:
        """Получить все меню из кэша redis."""

        result = cls.rd.hvals(HASH_NAME)
        if result:
            all_menu = [pickle.loads(item_menu) for item_menu in result]
            return all_menu
        return []

    @classmethod
    def set_menu(cls, id: str, menu: models.Menus) -> None:
        """Записать меню в кэш redis."""

        cls.rd.hset(HASH_NAME, id, pickle.dumps(menu))

    @classmethod
    def update_menu(cls, id: str, menu: models.Menus) -> None:
        """Обновить запись меню в кэше redis."""

        cls.rd.hset(HASH_NAME, id, pickle.dumps(menu))

    @classmethod
    def get_menu(cls, id: str) -> models.Menus | None:
        """Получить меню из кэша redis."""

        result = cls.rd.hget(HASH_NAME, id)
        if result:
            menu = pickle.loads(result)
            return menu
        return None

    @classmethod
    def delete_menu(cls, id: str):
        """Удалить меню из кэша redis."""

        all_keys_submenu = cls.rd.hkeys(id)
        for item_submenu in all_keys_submenu:
            all_keys_dish = cls.rd.hkeys(item_submenu.decode('utf-8'))
            for item_dish in all_keys_dish:
                cls.rd.hdel(item_submenu.decode('utf-8'), item_dish.decode('utf-8'))
            cls.rd.hdel(id, item_submenu.decode('utf-8'))

        cls.rd.hdel(HASH_NAME, id)

        return {'message': 'menu deleted'}

    @classmethod
    def cache_menu(cls):
        """Получить все ключи (id) кеша меню"""

        return [i.decode('utf-8') for i in cls.rd.hkeys(HASH_NAME)]

    @classmethod
    def get_all_submenu(cls, target_menu_id: str) -> list[models.Submenus] | None:
        """Получить все подменю из кэша redis."""

        result = cls.rd.hvals(target_menu_id)
        if result:
            all_submenu = [pickle.loads(item_submenu) for item_submenu in result]
            return all_submenu
        return []

    @classmethod
    def set_submenu(cls, target_menu_id: str, id: str, submenu: models.Submenus) -> None:
        """Записать подменю в кэш redis."""

        cls.rd.hset(target_menu_id, id, pickle.dumps(submenu))

        get_menu = cls.rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_submenu = pickle.loads(get_menu)  # type: ignore
        change_menu_count_submenu.submenus_count += 1
        cls.rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_submenu))

    @classmethod
    def update_submenu(cls, target_menu_id: str, id: str, submenu: models.Submenus) -> None:
        """Обновить запись подменю в кэше redis."""

        cls.rd.hset(target_menu_id, id, pickle.dumps(submenu))

    @classmethod
    def get_submenu(cls, target_menu_id: str, id: str) -> models.Submenus | None:
        """Получить подменю из кэша redis."""

        result = cls.rd.hget(target_menu_id, id)
        if result:
            submenu = pickle.loads(result)
            return submenu
        return None

    @classmethod
    def delete_submenu(cls, target_menu_id: str, id: str):
        """Удалить подменю из кэша redis."""

        all_keys_dish = cls.rd.hkeys(id)
        for item in all_keys_dish:
            cls.rd.hdel(id, item.decode('utf-8'))

        cls.rd.hdel(target_menu_id, id)

        get_menu = cls.rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_submenu = pickle.loads(get_menu)  # type: ignore
        change_menu_count_submenu.submenus_count -= 1
        change_menu_count_submenu.dishes_count = 0
        cls.rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_submenu))

        return {'message': 'submenu deleted'}

    @classmethod
    def cache_submenu(cls, target_menu_id: str):
        """Получить все ключи (id) кеша подменю"""

        return [i.decode('utf-8') for i in cls.rd.hkeys(target_menu_id)]

    @classmethod
    def get_all_dish(cls, target_submenu_id: str) -> list[models.Dishes] | None:
        """Получить все блюда из кэша redis."""

        result = cls.rd.hvals(target_submenu_id)
        if result:
            all_dish = [pickle.loads(item_dish) for item_dish in result]
            return all_dish
        return []

    @classmethod
    def set_dish(cls, target_menu_id: str, target_submenu_id: str, id: str, dish: models.Dishes) -> None:
        """Записать блюдо в кэш redis."""

        cls.rd.hset(target_submenu_id, id, pickle.dumps(dish))

        get_submenu = cls.rd.hget(target_menu_id, target_submenu_id)
        change_submenu_count_dish = pickle.loads(get_submenu)  # type: ignore
        change_submenu_count_dish.dishes_count += 1
        cls.rd.hset(target_menu_id, target_submenu_id, pickle.dumps(change_submenu_count_dish))

        get_menu = cls.rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_dish = pickle.loads(get_menu)  # type: ignore
        change_menu_count_dish.dishes_count += 1
        cls.rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_dish))

    @classmethod
    def update_dish(cls, target_submenu_id: str, id: str, dish: models.Dishes) -> None:
        """Обновить запись блюда в кэше redis."""

        cls.rd.hset(target_submenu_id, id, pickle.dumps(dish))

    @classmethod
    def get_dish(cls, target_submenu_id: str, id: str) -> models.Dishes | None:
        """Получить блюдо из кэша redis."""

        result = cls.rd.hget(target_submenu_id, id)
        if result:
            dish = pickle.loads(result)
            return dish
        return None

    @classmethod
    def delete_dish(cls, target_menu_id: str, target_submenu_id: str, id: str):
        """Удалить бдюдо из кэша redis."""

        cls.rd.hdel(target_submenu_id, id)

        get_submenu = cls.rd.hget(target_menu_id, target_submenu_id)
        change_submenu_count_dish = pickle.loads(get_submenu)  # type: ignore
        change_submenu_count_dish.dishes_count -= 1
        cls.rd.hset(target_menu_id, target_submenu_id, pickle.dumps(change_submenu_count_dish))

        get_menu = cls.rd.hget(HASH_NAME, target_menu_id)
        change_menu_count_dish = pickle.loads(get_menu)  # type: ignore
        change_menu_count_dish.dishes_count -= 1
        cls.rd.hset(HASH_NAME, target_menu_id, pickle.dumps(change_menu_count_dish))

        return {'message': 'dish deleted'}

    @classmethod
    def cache_dish(cls, target_submenu_id: str):
        """Получить все ключи (id) кеша блюда"""

        return [i.decode('utf-8') for i in cls.rd.hkeys(target_submenu_id)]
