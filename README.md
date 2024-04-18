#  Clean Architecture. Шаблон проекта.

Разделение по фичам
```
/src/
    /src/posts/
    /src/users/
    /src/feature_1/
```

Каждая фича должна как можно меньше зависеть от других. Должна быть возможность выкинуть фичу из проекта, и после минимальных изменениях в других фичах (или вообще без них) заставить проект снова работать.

Разделение по слоям
```
/src/posts/
    /src/posts/data/
        /src/posts/data/repositories/ - реализации репозиториев
            /src/posts/data/repositories/mock/ - моковые репозитории
            /src/posts/data/repositories/network/ - репозитории, запрашивающие данные по сети (например http)
            /src/posts/data/repositories/database/ - репозитории, запрашивающие данные из БД сервиса
                /src/posts/data/repositories/database/models/ - ORM модели, непосредственные запросы к БД
                /src/posts/data/repositories/database/mappers/ - мапперы на уровне данных из DTO или моделей в entity
    /src/posts/domain/
        /src/posts/domain/entities/
        /src/posts/domain/interactors/ - компоненты, реализующие бизнес логику. используют интерфейсы репозиториев
        /src/posts/domain/repositories/ - интерфейсы репозиториев
    /src/posts/presentation/
        /src/posts/presentation/http/
            /src/posts/presentation/http/views/
                /src/posts/presentation/http/views/schemas/
```

Для упрощения в качестве entity используются pydantic модели. pydantic предоставляет функционал десериализации и валидации данных, приходящих извне (например по http в json). Как альтернатива - можно использовать dataclasses, маппить на уровне view из pydantic модели в датаклассы и обратно.


Настройка зависимостей в `src/setup.py`

```python
posts_repository_factory = database_posts_repository_factory # использовать боевую реализацию (запрос данных из БД)
posts_repository_factory = mock_posts_repository_factory # использовать моковый репозиторий
```

## Запуск проекта в Docker

```bash
cd env/local/docker
docker compose up -d --build
```

Доступ к API после запуска - http://localhost:8000 \
Документация - http://localhost:8000/docs или http://localhost:8000/openapi.json

## TODO
- Репозитории должны бросать ошибку доменного уровня
- Добавить маппинг ошибки доменного уровня в HTTP ответы (на уровне HTTP)
- Доработать пример бизнес логики (с использованием users_repository)