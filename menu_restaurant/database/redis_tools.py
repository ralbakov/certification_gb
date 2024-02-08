import os
import pickle

import redis
from dotenv import load_dotenv

from menu_restaurant.database import models

load_dotenv('.env.work')

HASH_NAME: str = 'full_menu'
"""Переменная для присвоения имению хэшу"""


class RedisCache:
    """Класс для установки соединения с redis и работой с кешем."""
    __rd = redis.Redis(host=os.environ['REDIS_HOST'],
                       port=int(os.environ['REDIS_PORT'])
                       )

    @classmethod
    def get_all_menu_cache(cls) -> list[models.Menus] | list[None]:
        """Получить все меню из кэша redis."""

        result = cls.__rd.hvals(HASH_NAME)
        if result:
            all_menu = [pickle.loads(item_menu) for item_menu in result]
            return all_menu
        return []

    @classmethod
    def set_menu_cache(cls,
                       target_menu_id: str,
                       menu: models.Menus
                       ) -> None:
        """Записать меню в кэш redis."""

        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(menu))

    @classmethod
    def update_menu_cache(cls,
                          target_menu_id: str,
                          menu: models.Menus
                          ) -> None:
        """Обновить запись меню в кэше redis."""

        cls.__rd.hset(HASH_NAME, target_menu_id, pickle.dumps(menu))

    @classmethod
    def get_menu_cache(cls, target_menu_id: str) -> models.Menus:
        """Получить меню из кэша redis."""

        result = cls.__rd.hget(HASH_NAME, target_menu_id)
        assert isinstance(result, bytes)
        menu = pickle.loads(result)
        return menu

    @classmethod
    def delete_menu_cache(cls, target_menu_id: str) -> None:
        """Удалить меню из кэша redis."""

        all_keys_submenu = cls.__rd.hkeys(target_menu_id)
        for item_submenu in all_keys_submenu:
            all_keys_dish = cls.__rd.hkeys(item_submenu)
            for item_dish in all_keys_dish:
                cls.__rd.hdel(item_submenu, item_dish)
            cls.__rd.hdel(target_menu_id, item_submenu)

        cls.__rd.hdel(HASH_NAME, target_menu_id)
        return None

    @classmethod
    def get_all_keys_menu(cls) -> list[str]:
        """Получить все ключи (target_menu_id) кеша меню"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(HASH_NAME)]

    @classmethod
    def get_all_submenu_cache(cls,
                              target_menu_id: str
                              ) -> list[models.Submenus] | list[None]:
        """Получить все подменю из кэша redis."""

        result = cls.__rd.hvals(target_menu_id)
        if result:
            all_submenu = [pickle.loads(item_submenu) for item_submenu in result]
            return all_submenu
        return []

    @classmethod
    def set_submenu_cache(cls,
                          target_menu_id: str,
                          target_submenu_id: str,
                          submenu: models.Submenus
                          ) -> None:
        """Записать подменю в кэш redis."""

        cls.__rd.hset(target_menu_id,
                      target_submenu_id,
                      pickle.dumps(submenu))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        assert isinstance(get_menu, bytes)
        change_menu_count_submenu = pickle.loads(get_menu)
        change_menu_count_submenu.submenus_count += 1
        cls.__rd.hset(HASH_NAME,
                      target_menu_id,
                      pickle.dumps(change_menu_count_submenu))

    @classmethod
    def update_submenu_cache(cls,
                             target_menu_id: str,
                             target_submenu_id: str,
                             submenu: models.Submenus
                             ) -> None:
        """Обновить запись подменю в кэше redis."""

        cls.__rd.hset(target_menu_id,
                      target_submenu_id,
                      pickle.dumps(submenu)
                      )

    @classmethod
    def get_submenu_cache(cls,
                          target_menu_id: str,
                          target_submenu_id: str
                          ) -> models.Submenus:
        """Получить подменю из кэша redis."""

        result = cls.__rd.hget(target_menu_id,
                               target_submenu_id)
        assert isinstance(result, bytes)
        submenu = pickle.loads(result)
        return submenu

    @classmethod
    def delete_submenu_cache(cls,
                             target_menu_id: str,
                             target_submenu_id: str
                             ) -> None:
        """Удалить подменю из кэша redis."""

        all_keys_dish = cls.__rd.hkeys(target_submenu_id)
        for item in all_keys_dish:
            cls.__rd.hdel(target_submenu_id, item)

        cls.__rd.hdel(target_menu_id, target_submenu_id)

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        assert isinstance(get_menu, bytes)
        change_menu_count_submenu = pickle.loads(get_menu)
        change_menu_count_submenu.submenus_count -= 1
        change_menu_count_submenu.dishes_count = 0
        cls.__rd.hset(HASH_NAME,
                      target_menu_id,
                      pickle.dumps(change_menu_count_submenu))

        return None

    @classmethod
    def get_all_keys_submenu(cls, target_menu_id: str) -> list[str]:
        """Получить все ключи (target_menu_id) кеша подменю"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(target_menu_id)]

    @classmethod
    def get_all_dish_cache(cls,
                           target_submenu_id: str
                           ) -> list[models.Dishes] | list[None]:
        """Получить все блюда из кэша redis."""

        result = cls.__rd.hvals(target_submenu_id)
        if result:
            all_dish = [pickle.loads(item_dish) for item_dish in result]
            return all_dish
        return []

    @classmethod
    def set_dish_cache(cls,
                       target_menu_id: str,
                       target_submenu_id: str,
                       target_dish_id: str,
                       dish: models.Dishes
                       ) -> None:
        """Записать блюдо в кэш redis."""

        cls.__rd.hset(target_submenu_id,
                      target_dish_id,
                      pickle.dumps(dish))

        get_submenu = cls.__rd.hget(target_menu_id, target_submenu_id)
        assert isinstance(get_submenu, bytes)
        change_submenu_count_dish = pickle.loads(get_submenu)
        change_submenu_count_dish.dishes_count += 1
        cls.__rd.hset(target_menu_id,
                      target_submenu_id,
                      pickle.dumps(change_submenu_count_dish))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        assert isinstance(get_menu, bytes)
        change_menu_count_dish = pickle.loads(get_menu)
        change_menu_count_dish.dishes_count += 1
        cls.__rd.hset(HASH_NAME,
                      target_menu_id,
                      pickle.dumps(change_menu_count_dish)
                      )

    @classmethod
    def update_dish_cache(cls,
                          target_submenu_id: str,
                          target_dish_id: str,
                          dish: models.Dishes
                          ) -> None:
        """Обновить запись блюда в кэше redis."""

        cls.__rd.hset(target_submenu_id,
                      target_dish_id,
                      pickle.dumps(dish))

    @classmethod
    def get_dish_cache(cls,
                       target_submenu_id: str,
                       target_dish_id: str
                       ) -> models.Dishes:
        """Получить блюдо из кэша redis."""

        result = cls.__rd.hget(target_submenu_id, target_dish_id)
        assert isinstance(result, bytes)
        dish = pickle.loads(result)
        return dish

    @classmethod
    def delete_dish_cache(cls,
                          target_menu_id: str,
                          target_submenu_id: str,
                          target_dish_id: str
                          ) -> None:
        """Удалить бдюдо из кэша redis."""

        cls.__rd.hdel(target_submenu_id, target_dish_id)

        get_submenu = cls.__rd.hget(target_menu_id, target_submenu_id)
        assert isinstance(get_submenu, bytes)
        change_submenu_count_dish = pickle.loads(get_submenu)
        change_submenu_count_dish.dishes_count -= 1
        cls.__rd.hset(target_menu_id,
                      target_submenu_id,
                      pickle.dumps(change_submenu_count_dish))

        get_menu = cls.__rd.hget(HASH_NAME, target_menu_id)
        assert isinstance(get_menu, bytes)
        change_menu_count_dish = pickle.loads(get_menu)
        change_menu_count_dish.dishes_count -= 1
        cls.__rd.hset(HASH_NAME,
                      target_menu_id,
                      pickle.dumps(change_menu_count_dish))

        return None

    @classmethod
    def get_all_keys_dishes(cls, target_submenu_id: str) -> list[str]:
        """Получить все ключи (target_submenu_id) кеша блюда"""

        return [i.decode('utf-8') for i in cls.__rd.hkeys(target_submenu_id)]

    @classmethod
    def drob_all_cache(cls) -> None:
        """Очищает базу для тестов"""

        cls.__rd.flushall()
