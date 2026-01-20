# Deribit Client

Клиент для работы с криптобиржей Deribit. Получает цены BTC и ETH каждую минуту и предоставляет API для доступа к
сохраненным данным.

## Структура проекта

Проект следует принципам Clean Architecture:

- `src/domain/` - доменные модели и сущности
- `src/application/` - бизнес-логика и use cases
- `src/infrastructure/` - реализация внешних зависимостей (БД, API клиенты, Celery)
- `src/presentation/` - FastAPI endpoints и схемы

## Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать окружение: `venv\Scripts\activate` (Windows)
4. Установить зависимости: `pip install -r requirements.txt`
5. Скопировать `.env.example` в `.env` и заполнить настройки
6. Настроить PostgreSQL и Redis
7. Запустить миграции БД
8. Запустить Celery worker: `celery -A src.infrastructure.tasks worker --loglevel=info`
9. Запустить API: `uvicorn src.presentation.api.main:app --reload`

## Развертывание через Docker

1. Убедитесь, что установлен Docker и Docker Compose
2. Запустите все сервисы: `docker-compose up -d`
3. API будет доступен по адресу: `http://localhost:8000`
4. Celery worker автоматически начнет получать цены каждую минуту
5. Для просмотра логов: `docker-compose logs -f`
6. Для остановки: `docker-compose down`

Docker Compose включает:
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- FastAPI приложение (порт 8000)
- Celery worker

## API Endpoints

- `GET /api/prices/all?ticker={ticker}` - получить все сохраненные данные по валюте
- `GET /api/prices/last?ticker={ticker}` - получить последнюю цену валюты
- `GET /api/prices/by-date?ticker={ticker}&date={timestamp}` - получить цену по дате

## Проверка работоспособности

**Через Docker:**
- API: http://localhost:8000/docs (Swagger UI)
- Проверка статуса: `docker-compose ps`
- Логи: `docker-compose logs -f`
- БД: `docker-compose exec db psql -U deribit_user -d deribit_db -c "SELECT * FROM prices LIMIT 5;"`
- Celery: `docker-compose logs -f celery`

**Unit тесты:**
```bash
docker-compose exec api pytest tests/ -v
```

**Проверка endpoints через curl:**
```bash
curl "http://localhost:8000/api/prices/all?ticker=BTC_USD"
curl "http://localhost:8000/api/prices/last?ticker=BTC_USD"
curl "http://localhost:8000/api/prices/by-date?ticker=BTC_USD&date=1768910133"
```

## Design Decisions

**Clean Architecture**: Проект разделен на слои (domain, application, infrastructure, presentation) для изоляции бизнес-логики от деталей реализации. Это упрощает тестирование и замену компонентов.

**Async/Await**: Использован asyncpg и aiohttp для асинхронной работы с БД и внешним API. Это повышает производительность при множественных запросах.

**Repository Pattern**: Доступ к данным инкапсулирован в PriceRepository, что позволяет легко заменить БД или добавить кэширование без изменения use cases.

**Use Cases**: Бизнес-логика вынесена в отдельные классы (GetAllPricesUseCase, GetLastPriceUseCase и т.д.), что делает код более читаемым и тестируемым.

**Celery для периодических задач**: Использован Celery вместо простого cron или asyncio.sleep, так как это позволяет масштабировать задачи и обрабатывать ошибки более надежно.

**Dependency Injection через FastAPI**: Подключение к БД управляется через lifespan events и передается через app.state, что исключает глобальные переменные и упрощает тестирование.

**Отсутствие миграций**: Таблица создается автоматически при первом запуске через `create_table_if_not_exists()`. Для production лучше использовать Alembic, но для тестового задания этого достаточно.

**DECIMAL для цены**: В БД цена хранится как DECIMAL(20, 8) для точности финансовых расчетов, хотя в коде используется float для простоты.
