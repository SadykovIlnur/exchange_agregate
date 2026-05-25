# Exchange agregate

## Описание проекта

Python-скрипт который:
  1. Получает список валют и их курсы к доллару США с открытого API https://www.exchangerate-api.com/.
  2. Делает бекап этих данных из ответа в json формате.
  3. Парсит данные в pandas.DataFrame с колонками:
    - Currency (код валюты)
    - Rate_to_USD (курс к доллару)
  4. Сохраняет результат в xlsx и csv в корневой папке.

В проекте настроено логирование.


## Запуск приложения

1. Клонировать репозиторий 

```bash
git clone git@github.com:SadykovIlnur/exchange_agregate.git
```

2. Cоздать виртуальное окружение:

```bash
# Если у вас Linux/macOS:
python3 -m venv venv  
# Если у вас Windows:
python -m venv venv
```

3. Активировать виртуальное окружение

```bash
# Если у вас Linux/macOS:
. venv/bin/activate
# Если у вас Windows:
. venv/Scripts/activate
```

4. Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

5. Запустить скрипт:

```bash
# Если у вас Linux/macOS:
python3 exchange_agregate.py
# Если у вас Windows:
python exchange_agregate.py
```


# Используемые технологии

- Python
- Pandas
- Request


# Автор

[Sadykov Ilnur](https://github.com/SadykovIlnur)
