Rest API приложение для работы с меню ресторана. Проект использует БД PostgreSQL.

## Копирование репозитория
```bash
mkdir 'your some folder'
cd 'your some folder'
git init
git git clone https://github.com/ralbakov/y_lab_tasks.git
cd y_lab_tasks
```
## Установка
```bash
 python3 -m venv venv
 source venv/bin/activate
 venv/bin/pip install -r requirements.txt 
```
## Создание в PostgreSQL пользователя - _someuser_ c паролем - _somepassword_ и БД - _menu_
Сначала подключаемся к PostgreSQL с Вашими правами администратора.
Создаем пользователя с паролем.
Назначаем ему кодировку.
Назначаем этому пользователю новую БД.
```bash
sudo psql -U 'пользователь_важен_регистр' -d postgres
CREATE USER someuser WITH PASSWORD somepassword;
ALTER ROLE someuser SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE menu TO someuser;
```
## Запуск сервера
```
uvicorn menu_restaurant.main:app --reload
```