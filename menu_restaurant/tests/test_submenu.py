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


def test_get_empty_submenus():
    """Тестирует пустой список субменю."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


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


def test_get_submenus():
    """Тестирует непустой список субменю."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает список подменю',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


def test_get_one_submenu():
    """Тестирует просмотр субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    assert data['id'] == target_submenu_id


def test_update_submenu():
    """Тестирует обновление субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.patch(
        reverse('Обновляет подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
        json={
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My updated submenu 1'
    assert data['description'] == 'My updated submenu description 1'
    assert data['id'] == target_submenu_id


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


def test_get_submenu_deleted():
    """Тестирует просмотр удаленного субменю."""

    target_menu_id = save_data['id']
    target_submenu_id = save_data['sub_id']
    response = client.get(
        reverse('Просматривает определенное подменю',
                **{'target_menu_id': target_menu_id,
                   'target_submenu_id': target_submenu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == 'submenu not found'


def test_delete_menu():
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
