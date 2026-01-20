# Deribit Client

Клиент для работы с криптобиржей Deribit. Получает цены BTC и ETH каждую минуту и предоставляет API для доступа к сохраненным данным.

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
8. Запустить Celery worker: `celery -A src.infrastructure.tasks.celery_app worker --loglevel=info`
9. Запустить API: `uvicorn src.presentation.api.main:app --reload`

## API Endpoints

- `GET /api/prices/all?ticker={ticker}` - получить все сохраненные данные по валюте
- `GET /api/prices/last?ticker={ticker}` - получить последнюю цену валюты
- `GET /api/prices/by-date?ticker={ticker}&date={timestamp}` - получить цену по дате

## Design Decisions

_Будет заполнено в процессе разработки_
