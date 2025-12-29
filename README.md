# LMS Backend

Учебный проект — серверная часть LMS-системы, позволяющей размещать обучающие материалы, курсы и уроки.
Проект разработан на **Django + Django REST Framework** с использованием **Poetry** и базой данных **PostgreSQL**.

---

## Стек технологий

- **Python 3.12+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL**
- **Poetry** — менеджер зависимостей
- **Pillow** — для работы с изображениями (аватарки, превью)

---

## Структура проекта

```
lms_backend/
├── config/                 # настройки проекта Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── materials/              # приложение: Курсы и Уроки
│   ├── models.py           # модели Course и Lesson
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── users/                  # приложение: Пользователи
│   ├── models.py           # кастомная модель User
│   ├── admin.py
│   └── ...
├── manage.py
├── pyproject.toml          # зависимости Poetry
├── poetry.lock
└── README.md
```

---

## Установка

```bash
git clone https://github.com/olganoskova200524/lms-backend.git
cd lms-backend
poetry install
```

## Создание файла `.env`

Создайте в корне проекта файл `.env` и добавьте в него параметры подключения к базе данных:

```env
DB_NAME=lms
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Применить миграции и запустить сервер:

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## API

### Курсы — `/api/courses/`

- **GET** — получить список курсов
- **POST** — создать курс
- **GET `/api/courses/{id}/`** — получить один курс
- **PUT `/api/courses/{id}/`** — изменить полностью
- **PATCH `/api/courses/{id}/`** — изменить частично
- **DELETE `/api/courses/{id}/`** — удалить курс


### Уроки — `/api/lessons/`

- **GET** — получить список уроков
- **POST** — создать урок
- **GET `/api/lessons/{id}/`** — получить один урок
- **PUT `/api/lessons/{id}/`** — изменить полностью
- **PATCH `/api/lessons/{id}/`** — изменить частично
- **DELETE `/api/lessons/{id}/`** — удалить урок


### Celery & Celery Beat

В проекте используется Celery для фоновых задач и django-celery-beat для их планирования.

Реализована периодическая задача, которая:
- проверяет пользователей по полю `last_login`
- если пользователь не заходил более 30 дней — устанавливает `is_active=False`

Задача запускается ежедневно в 03:00 (Europe/Moscow).

Для запуска:
```bash
celery -A config worker -l info
celery -A config beat -l info
```

---

## Автор

**Olga Noskova**