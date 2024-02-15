Rest API приложение для работы с меню ресторана.
## Стек:
API - FlaskAPI  \
ORM - sqlalchemy  \
БД - PostgreSQL  \
Тестирование - pytest  \
DevOps - Docker \
Cache - Redis

## Копирование репозитория
```
git clone https://github.com/ralbakov/certification_gb.git

После завершения клонирования репозитория, необходимо перейти в папку "certification_gb".
Для этого в терминале выполните нижеуказанную команду:

cd certification_gb
```

## Запуск
### Основное приложение
```
Находясь в папке "y_lab_tasks", в командной строке выполните команду:
docker-compose -f prod.yml up -d
```
### Тестирование приложения
```
Находясь в папке "y_lab_tasks", в командной строке выполните команду:
docker-compose -f test.yml up
```
