Rest API приложение для работы с меню ресторана. 
## Стек: 
API - FlaskAPI  \
ORM - sqlalchemy  \
БД - PostgreSQL  \
Тестирование - pytest  \
DevOps - Docker  
# Задача
В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после Вебинара №1.

Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде “docker-compose up -d” или той которая описана вами в readme.md.

Образы для Docker:
(API) python:3.10-slim
(DB) postgres:15.1-alpine

1.Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
2.Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md
3.* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
4.** Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
Если FastAPI синхронное - тесты синхронные, Если асинхронное - тесты асинхронные

*Оборачиваем приложение в докер.
**CRUD – create/update/retrieve/delete.

# Решение

Ответ на вопрос № 3 реализован в файле: [menu_restaurant/models.py](https://github.com/ralbakov/y_lab_tasks/blob/main/menu_restaurant/models.py) строки с 46 по 59


## Копирование репозитория
```
git clone https://github.com/ralbakov/y_lab_tasks.git  
  
После завершения клонирования репозитория, необходимо перейти в папку "y_lab_tasks".   
Для этого в терминале выполните нижеуказанную команду:  
  
cd y_lab_tasks
```

## Запуск
### Основное приложение
```
Находясь в папке "y_lab_tasks", в командной строке выполните команду:  
docker-compose -f prod.yml up
```
### Тестирование приложения
```
Находясь в папке "y_lab_tasks", в командной строке выполните команду:  
docker-compose -f test.yml up
``` 