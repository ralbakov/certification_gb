Rest API приложение для работы с меню ресторана.

## Стек':'

API - FlaskAPI  \
ORM - sqlalchemy  \
БД - PostgreSQL  \
Тестирование - pytest  \
DevOps - Docker \
Cache - Redis

## Копирование репозитория

```bash
git clone https://github.com/ralbakov/certification_gb.git
```

```text
После завершения клонирования репозитория, необходимо перейти в папку "certification_gb".
Для этого в терминале выполните нижеуказанную команду:
```

```bash
cd certification_gb
```

## Запуск

### Основное приложение

```text
Находясь в папке "certification_gb", в командной строке выполните команду:
docker-compose -f prod.yml up -d
```

### Тестирование приложения

```text
Находясь в папке "certification_gb", в командной строке выполните команду:
docker-compose -f test.yml up
```
