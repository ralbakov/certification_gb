from ..tests.conftest import client
from ..tests.reverse import reverse

save_data = {}


def test_get_empty_menus():
    """Тестирует пустой список меню."""

    response = client.get(
        reverse('Просматривает список меню')
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


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


def test_get_menus():
    """Тестирует непустой список меню."""

    response = client.get(
        reverse('Просматривает список меню')
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


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
    assert data['id'] == f'{target_menu_id}'


def test_update_menu():
    """Тестирует обновление меню."""

    target_menu_id = save_data['id']
    response = client.patch(
        reverse('Обновляет меню',
                **{'target_menu_id': target_menu_id}),
        json={
            'title': 'My updated menu 1',
            'description': 'My updated menu description 1'
        }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'My updated menu 1'
    assert data['description'] == 'My updated menu description 1'
    assert data['id'] == f'{target_menu_id}'


def test_delete_menu():
    """Тестирует удаление меню."""

    target_menu_id = save_data['id']
    response = client.delete(
        reverse('Удаляет меню',
                **{'target_menu_id': target_menu_id})
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_menu_deleted():
    """Тестирует просмотр удаленного меню."""

    target_menu_id = save_data['id']
    response = client.get(
        reverse('Просматривает определенное меню',
                **{'target_menu_id': target_menu_id}),
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == 'menu not found'
