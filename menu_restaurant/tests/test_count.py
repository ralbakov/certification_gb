from ..tests.conftest import client
from ..tests.reverse import reverse

save_data = {}


def test_create_menu():
    """Тестирует создание меню."""

    response = client.post(
        reverse('Создает меню'),
        json={
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['id'] = data['id']
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['id'] == save_data['id']


def test_create_submenu():
    """Тестирует создание субменю."""

    target_menu_id = save_data['id']
    response = client.post(
        reverse('Создает подменю',
                **{'target_menu_id': target_menu_id}),
        json={
            'title': 'My submenu 1',
            'description': 'My submenu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['sub_id'] = data['id']
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    assert data['id'] == save_data['sub_id']


def test_create_dish_first():
    """Тестирует создание 1-го блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.post(
        reverse('Создает блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['dis_id'] = data['id']
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'
    assert data['id'] == save_data['dis_id']


def test_create_dish_second():
    """Тестирует создание 2-го блюда."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.post(
        reverse('Создает блюдо',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    save_data['dis_id'] = data['id']
    assert data['title'] == 'My dish 2'
    assert data['description'] == 'My dish description 2'
    assert data['price'] == '13.50'
    assert data['id'] == save_data['dis_id']


def test_get_submenu_dish_count():
    """Тестирует просмотр определенного меню с количеством субменю и блюд."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == target_menu_id
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


def test_get_dish_count():
    """Тестирует просмотр определенного субменю с количеством блюд."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == target_submenu_id
    assert data['dishes_count'] == 2


def test_delete_submenu():
    """Тестирует удаление субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.delete(
        reverse('Удаляет подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_submenus():
    """Тестирует список субменю."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_empty_dishes():
    """Тестирует просмотр списка блюд."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.get(
        reverse('Просматривает список блюд',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}
                ),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_one_menu():
    """Тестирует просмотр меню."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['id'] == target_menu_id


def test_delete_menu():
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_empty_menus():
    """Тестирует пустой список меню."""

    response = client.get(
        reverse('Просматривает список меню'),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
