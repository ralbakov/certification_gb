from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://someuser:somepassword@localhost:5432/test_menu"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def pytest_namespace():
    return {
        'shared': None, 
        'shared_sub_id': None,
        'shared_dish_id': None,
    }


def test_get_empty_menus():
    '''
    Тестирует пустой список меню.
    '''
    response = client.get(
        "/api/v1/menus",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_create_menu():
    '''
    Тестирует создание меню.
    '''
    response = client.post(
        "/api/v1/menus",
        json={
                "title": "My menu 1", 
                "description": "My menu description 1"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    pytest.shared = data['id']
    assert data['title'] == "My menu 1"
    assert data['description'] == "My menu description 1"
    assert data['id'] == f"{pytest.shared}"


def test_get_menus():
    '''
    Тестирует непустой список меню.
    '''
    response = client.get(
        "/api/v1/menus",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


def test_get_one_menu():
    '''
    Тестирует просмотр меню.
    '''
    target_menu_id = pytest.shared
    response = client.get(
        f"/api/v1/menus/{target_menu_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My menu 1"
    assert data['description'] == "My menu description 1"
    assert data['id'] == f"{target_menu_id}"


def test_update_menu():
    '''
    Тестирует обновление меню.
    '''
    target_menu_id = pytest.shared
    response = client.patch(
        f"/api/v1/menus/{target_menu_id}", 
        json={
                "title": "My updated menu 1", 
                "description": "My updated menu description 1"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My updated menu 1"
    assert data['description'] == "My updated menu description 1"
    assert data['id'] == f"{target_menu_id}"


def test_get_empty_submenus():
    '''
    Тестирует пустой список субменю.
    '''
    target_menu_id = pytest.shared
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_create_submenu():
    '''
    Тестирует создание субменю.
    '''
    target_menu_id = pytest.shared
    response = client.post(
        f"/api/v1/menus/{target_menu_id}/submenus",
        json={
                "title": "My submenu 1", 
                "description": "My submenu description 1"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    pytest.shared_sub_id = data['id']
    assert data['title'] == "My submenu 1"
    assert data['description'] == "My submenu description 1"
    assert data['id'] == f"{pytest.shared_sub_id}"


def test_get_submenus():
    '''
    Тестирует непустой список субменю.
    '''
    target_menu_id = pytest.shared
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


def test_get_one_submenu():
    '''
    Тестирует просмотр субменю.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My submenu 1"
    assert data['description'] == "My submenu description 1"
    assert data['id'] == f"{target_submenu_id}"


def test_update_submenu():
    '''
    Тестирует обновление субменю.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.patch(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", 
        json={
                "title": "My updated submenu 1", 
                "description": "My updated submenu description 1"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My updated submenu 1"
    assert data['description'] == "My updated submenu description 1"
    assert data['id'] == f"{target_submenu_id}"


def test_get_empty_dishes():
    '''
    Тестирует просмотр пустых блюд (когда еще нет блюд).
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_create_dish():
    '''
    Тестирует создание блюда.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.post(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
        json={
                "title": "My dish 1", 
                "description": "My dish description 1", 
                "price": "12.50"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 201, response.text
    data = response.json()
    pytest.shared_dish_id = data['id']
    assert data['title'] == "My dish 1"
    assert data['description'] == "My dish description 1"
    assert data['price'] == "12.50"
    assert data['id'] == f"{pytest.shared_dish_id}"


def test_get_dishes():
    '''
    Тестирует просмотр, когда список блюд непустой.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data != []


def test_get_dish():
    '''
    Тестирует просмотр блюда.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    target_dish_id = pytest.shared_dish_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My dish 1"
    assert data['description'] == "My dish description 1"
    assert data['price'] == "12.50"
    assert data['id'] == f"{target_dish_id}"


def test_update_dish():
    '''
    Тестирует обновление блюда.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    target_dish_id = pytest.shared_dish_id
    response = client.patch(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
        json={
                "title": "My updated dish 1", 
                "description": "My updated dish description 1", 
                "price": "14.50"
            }
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == "My updated dish 1"
    assert data['description'] == "My updated dish description 1"
    assert data['price'] == "14.50"
    assert data['id'] == f"{target_dish_id}"


def test_delete_dish():
    '''
    Тестирует удаление блюда.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    target_dish_id = pytest.shared_dish_id
    response = client.delete(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_dish_deleted():
    '''
    Тестирует просмотр удаленного блюда.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    target_dish_id = pytest.shared_dish_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "dish not found"


def test_delete_submenu():
    '''
    Тестирует удаление субменю.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.delete(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", 
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_submenu_deleted():
    '''
    Тестирует просмотр удаленного субменю.
    '''
    target_menu_id = pytest.shared
    target_submenu_id = pytest.shared_sub_id
    response = client.get(
        f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", 
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "submenu not found"


def test_delete_menu():
    '''
    Тестирует удаление меню.
    '''
    target_menu_id = pytest.shared
    response = client.delete(
        f"/api/v1/menus/{target_menu_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 200, response.text


def test_get_menu_deleted():
    '''
    Тестирует просмотр удаленного меню.
    '''
    target_menu_id = pytest.shared
    response = client.get(
        f"/api/v1/menus/{target_menu_id}",
    )
    assert response.headers.get('content-type') == 'application/json', 'Is not application/json'
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "menu not found"