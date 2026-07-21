### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/russinArtem/async-yacut.git
```

```
cd async-yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В корне проекта создать файл `.env` и указать в нем переменные из файла `.env.example`. В `.env` присвойте переменным свои актуальные значения.

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```

---

## Стек технологий

- **Backend:** Python 3.12, Flask 3.0.2;
- **База данных:** SQLite (SQLAlchemy 2.0.21);
- **Миграции:** Flask-Migrate (Alembic);
- **Фронтенд:** HTML, CSS (Bootstrap 5);
- **Асинхронные запросы:** aiohttp 3.10.5;
- **Документация API:** OpenAPI 3.0.3;
- **Тестирование:** pytest, pytest-aiohttp, pytest-asyncio;
- **Линтинг:** flake8;
- **Работа с облачными хранилищами:** REST API Яндекс Диска.

---

## Документация API

После запуска сервера доступна по адресу [http://127.0.0.1:5000/redoc/](http://127.0.0.1:5000/redoc/)

## Автор

**Артем Руссин**

GitHub: [russinArtem](https://github.com/russinArtem/)

Email: [russinartem@yandex.ru](mailto:russinartem@yandex.ru)
