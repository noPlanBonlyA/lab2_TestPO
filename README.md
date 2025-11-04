# Lab 2: Integration Testing

## Описание проекта
Калькулятор с историей операций и возможностью сохранения в файл - демонстрационный проект для изучения интеграционного тестирования.

## Структура проекта
```
lab2/
├── calculator.py          # Модуль математических операций
├── history.py            # Модуль управления историей операций
├── persistence.py        # Модуль сохранения/загрузки данных
├── main.py              # Основной модуль интеграции
├── test_integration.py  # Интеграционные тесты
├── requirements.txt     # Зависимости проекта
└── README.md           # Документация
```

## Установка
```bash
pip install -r requirements.txt
```

## Запуск тестов
```bash
# Запуск всех тестов
pytest test_integration.py -v

# Запуск с покрытием кода
pytest test_integration.py -v --cov=. --cov-report=html

# Запуск конкретного теста
pytest test_integration.py::TestCalculatorHistoryIntegration::test_operation_with_history_recording -v
```

## Использование
```python
from main import CalculatorWithHistory

# Создание калькулятора
calc = CalculatorWithHistory()

# Выполнение операций
result = calc.add(10, 5)
calc.multiply(3, 7)

# Просмотр истории
history = calc.get_history()

# Получение статистики
stats = calc.get_statistics()

# Сохранение истории в файл
calc = CalculatorWithHistory(persistence_file="history.json")
calc.add(10, 5)
calc.save_to_file()

# Загрузка истории из файла
calc.load_from_file()
```

## Точки интеграции
1. **Calculator ↔ CalculatorWithHistory** - выполнение операций и получение результатов
2. **History ↔ CalculatorWithHistory** - запись и получение истории операций
3. **HistoryPersistence ↔ CalculatorWithHistory** - сохранение и загрузка данных
4. **History ↔ File System** - работа с JSON файлами

## Покрытие тестами
- Базовая интеграция Calculator-History
- Цепочки последовательных операций
- Обработка ошибок между модулями
- Генерация статистики
- Управление размером истории
- Сохранение и загрузка данных
- Целостность данных при сериализации
- Сложные пользовательские сценарии
- Восстановление после ошибок
- Граничные случаи
