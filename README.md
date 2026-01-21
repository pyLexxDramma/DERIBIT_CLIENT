# Deribit Client

Клиент для работы с криптобиржей Deribit. Получает цены BTC и ETH каждую минуту и предоставляет API для доступа к
сохраненным данным.

## Структура проекта



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

**Примечание**: После первого запуска подождите 1-2 минуты, чтобы Celery создал таблицу и собрал первые данные. Проверить можно через `docker-compose exec db psql -U deribit_user -d deribit_db -c "SELECT COUNT(*) FROM prices;"`

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

Краткое описание архитектурных решений. **Подробные объяснения с обоснованием каждого решения** см. в файле [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

**Clean Architecture**: Разделил проект на слои, потому что раньше сталкивался с проблемами, когда бизнес-логика была перемешана с деталями БД. Теперь легко заменить PostgreSQL на другую БД или добавить кэш без изменения use cases.

**Async/Await**: Выбрал asyncpg и aiohttp, потому что Celery задачи могут делать несколько запросов к API одновременно. Синхронный подход был бы медленнее, особенно при росте количества тикеров.

**Repository Pattern**: Вынес доступ к данным в PriceRepository, чтобы не тащить asyncpg Pool через все слои. Если понадобится добавить Redis-кэш, просто оберну репозиторий - use cases не изменятся.

**Use Cases**: Сделал отдельные классы для каждого действия, хотя они простые. Это упростило тесты - можно мокать только репозиторий, а не всю БД. Плюс если появятся дополнительные проверки (валидация тикера, лимиты), их легко добавить в один класс.

**Celery вместо cron**: Использовал Celery, потому что нужна была возможность масштабировать воркеры и обрабатывать ошибки с retry. Простой asyncio.sleep в отдельном процессе не дал бы такой гибкости.

**Dependency Injection через FastAPI**: Подключение к БД через lifespan events, потому что глобальные переменные усложняют тестирование. Теперь в тестах можно легко подменить Database на мок.

**Без миграций**: Таблица создается автоматически через `create_table_if_not_exists()`. Для production нужен Alembic, но для тестового задания это избыточно - схема простая и не меняется.

**DECIMAL для цены**: В БД храню как DECIMAL(20, 8), чтобы избежать проблем с точностью float при финансовых расчетах. В коде использую float для простоты, но при необходимости можно перейти на Decimal.

**Подробнее**: См. [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) для детального объяснения каждого решения с примерами кода и альтернативами.
