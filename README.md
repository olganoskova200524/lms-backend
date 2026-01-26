# LMS Backend

Учебный проект — серверная часть LMS-системы, позволяющей размещать обучающие материалы, курсы и уроки.
Проект разработан на **Django + Django REST Framework** с использованием **Poetry** и базой данных **PostgreSQL**.

---

## Стек технологий

- **Python 3.12+**
- **Django 5.2x**
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

## Запуск проекта через Docker Compose

### 1. Подготовка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example` и заполните необходимые переменные.

Для запуска через Docker Compose важно указать:

```env
DB_HOST=postgres
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

### 2. Запуск проекта

Для запуска всех сервисов выполните команду:

```bash
docker compose up --build
```

Будут запущены следующие сервисы:

- **Backend** — Django-приложение
- **PostgreSQL** — база данных
- **Redis** — брокер сообщений и хранилище для Celery
- **Celery Worker** — обработка фоновых задач
- **Celery Beat** — планировщик периодических задач

При запуске через Docker Compose Celery Worker и Celery Beat стартуют автоматически.

## 3. Проверка работы сервисов

После запуска проекта убедитесь, что все сервисы работают корректно:

- **Backend** доступен по адресу:  
  http://localhost:8000

- **PostgreSQL** используется backend-сервисом в качестве базы данных

- **Redis** используется Celery в качестве брокера сообщений

- **Celery Worker** выполняет фоновые задачи

- **Celery Beat** запускает периодические задачи по расписанию

---

## Локальный запуск (без Docker)

### Установка зависимостей

```bash
poetry install
```

## Создание файла `.env`

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