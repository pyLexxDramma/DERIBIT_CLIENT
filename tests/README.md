# Тесты

Запуск всех тестов:
```bash
pytest
```

Запуск с выводом:
```bash
pytest -v
```

Запуск конкретного файла:
```bash
pytest tests/unit/test_use_cases.py
```

Запуск конкретного теста:
```bash
pytest tests/unit/test_use_cases.py::test_get_all_prices_returns_list
```
