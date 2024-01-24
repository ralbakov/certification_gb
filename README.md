Rest API приложение для работы с меню ресторана. Проект использует БД PostgreSQL.

## Копирование репозитория
```bash
mkdir 'your some folder'
cd 'your some folder'
git init
git clone https://github.com/ralbakov/y_lab_tasks.git
cd y_lab_tasks
```
## Установка
```bash
 python3 -m venv venv
 source venv/bin/activate
 venv/bin/pip install -r requirements.txt 
```
## Создание в PostgreSQL пользователя - _someuser_ c паролем - _somepassword_ и БД - _menu_
```
Создать пользователя PostgreSQL в графическом интерфейсе.
С помощью pgAdmin подключимся к базе данных и в разделе Login/Group Roles вызовем контекстное меню и выберем Create — Login/Group Role.
![Postgre_Create_Login_Group-Role](/Postgre_Create_Login_Group-Role.png).
Создаем пользователя с именем _"someuser"_ - именно это название пользователя.
![Create login](/Create_login.png)
На вкладке Definition зададим пароль _"somepassword"_ - именно этот пароль.
На вкладке Privileges дополнительно ставим полномочия: Can login, Create role, Create databases и сохраняем.
Далее идем во вкладку Databases вызовем контекстное меню и выберем Create — Database...
![Create Database](/Create_database.png)
Вводим имя даты базы _menu_, в строке Owner выбираем _someuser_ и сохраняем.
```
## Запуск сервера
```
uvicorn menu_restaurant.main:app --reload
```