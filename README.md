# LMS Backend

Backend-часть учебной LMS-системы для управления курсами, уроками и пользователями.

Проект реализован на **Django + Django REST Framework**  
и включает полноценную инфраструктуру:

- Docker Compose
- Celery + Redis
- PostgreSQL
- CI/CD через GitHub Actions

---

## Стек технологий

- **Python 3.12**
- **Django 5.x**
- **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Celery + django-celery-beat**
- **Poetry**
- **Docker / Docker Compose**
- **Nginx**
- **GitHub Actions (CI/CD)**

---

## Структура проекта

```
lms_backend/
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline (lint, tests, docker build, deploy)
│
├── config/                       # Основные настройки Django-проекта
│   ├── __init__.py
│   ├── asgi.py                   # ASGI-конфигурация
│   ├── celery.py                 # Конфигурация Celery
│   ├── settings.py               # Основные настройки проекта
│   ├── urls.py                   # Корневые URL
│   └── wsgi.py                   # WSGI-конфигурация
│
├── materials/                    # Приложение: Курсы и Уроки
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # Модели Course и Lesson
│   ├── paginators.py
│   ├── serializers.py
│   ├── tasks.py                  # Celery-задачи
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   ├── views.py
│   └── views_subscriptions.py
│
├── users/                        # Приложение: Пользователи
│   ├── fixtures/                 # Фикстуры для загрузки данных
│   │   ├── groups.json
│   │   └── payments.json
│   ├── migrations/
│   ├── services/
│   │   └── stripe.py             # Интеграция со Stripe
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # Кастомная модель пользователя
│   ├── permissions.py
│   ├── serializers.py
│   ├── tasks.py                  # Celery-задачи пользователей
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── nginx/
│   └── default.conf              # Конфигурация Nginx (опционально)
│
├── .env                          # Переменные окружения (не коммитится)
├── .env.example                  # Пример файла переменных окружения
├── .dockerignore
├── .flake8                       # Настройки flake8
├── .gitignore
├── celerybeat-schedule           # Файл расписания Celery Beat
├── coverage.txt
├── docker-compose.yaml           # Docker Compose (backend, postgres, redis, celery)
├── Dockerfile                    # Docker-образ backend
├── entrypoint.sh                 # Entrypoint для контейнера backend
├── manage.py                     # Django management script
├── poetry.lock
├── pyproject.toml                # Зависимости Poetry
└── README.md                     # Документация проекта
```

---

## Установка (опционально, без Docker)

```bash
git clone https://github.com/olganoskova200524/lms-backend.git
cd lms-backend
poetry install
```

## Запуск проекта через Docker Compose

### 1. Подготовка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example` и заполните необходимые переменные.

```bash
cp .env.example .env
```

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
docker compose up -d --build
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
  http://localhost:8080

- **PostgreSQL** используется backend-сервисом в качестве базы данных

- **Redis** используется Celery в качестве брокера сообщений

- **Celery Worker** выполняет фоновые задачи

- **Celery Beat** запускает периодические задачи по расписанию

---

## Локальный запуск (без Docker)

### Установка зависимостей

Убедитесь, что Poetry установлен, затем выполните:

```bash
poetry install
```

### Создание файла `.env`

Для локального запуска (без Docker) создайте файл `.env` со следующими переменными:

```env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lms
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

### Применение миграций и запуск сервера

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## API

Базовый URL API:

```text
/api/
```

### Курсы

`/api/courses/`

- **GET** — получить список курсов
- **POST** — создать курс

`/api/courses/{id}/`

- **GET** — получить один курс
- **PUT** — изменить полностью
- **PATCH** — изменить частично
- **DELETE** — удалить курс

### Уроки

`/api/lessons/`

- **GET** — получить список уроков
- **POST** — создать урок

`/api/lessons/{id}/`

- **GET** — получить один урок
- **PUT** — изменить полностью
- **PATCH** — изменить частично
- **DELETE** — удалить урок

### Аутентификация

API использует JWT-аутентификацию.

Доступ к защищённым эндпоинтам возможен только при передаче токена в заголовке:

```http
Authorization: Bearer <token>
```

### Документация API

В проекте используется **drf-spectacular** для генерации схемы API.

При включённой документации в настройках проекта доступны следующие эндпоинты:

- Swagger UI — `/swagger/`
- Redoc — `/redoc/`

### Celery & Celery Beat

В проекте используется Celery для фоновых задач и django-celery-beat для их планирования.

Реализована периодическая задача, которая:

- проверяет пользователей по полю `last_login`
- если пользователь не заходил более 30 дней — устанавливает `is_active=False`

Задача запускается ежедневно в 03:00 (Europe/Moscow).

При локальном запуске без Docker:

```bash
celery -A config worker -l info
celery -A config beat -l info
```

## Deployment & CI/CD

### Общая схема

Проект деплоится автоматически с помощью **GitHub Actions**.

Схема работы:

1. Разработка ведётся в feature-ветках
2. Создаётся Pull Request в ветку `develop`
3. При push / merge в `develop`:
    - выполняются проверки CI (lint, тесты, сборка Docker-образов)
    - при успешных проверках проект автоматически разворачивается на сервере через Docker Compose

---

### Требования к серверу

Удалённый сервер (Ubuntu) должен иметь:

- Docker
- Docker Compose
- SSH-доступ
- Открытые порты: `22`, `80`

---

### Размещение проекта на сервере

Проект разворачивается в каталоге:

```bash
/home/ubuntu/apps/lms-backend
```

Код на сервере всегда находится в ветке `develop`.

Проект разворачивается и запускается на сервере с помощью **Docker Compose**.

## Переменные окружения

Все чувствительные данные хранятся вне репозитория.

На сервере используется файл `.env`, который создаётся на основе шаблона:

```bash
cp .env.example .env
```

### Пример используемых переменных

- `SECRET_KEY=your_secret_key`
- `DEBUG=False`
- `ALLOWED_HOSTS=127.0.0.1,localhost,<SERVER_IP>`
- `DB_NAME=lms_backend`
- `DB_USER=lms_user`
- `DB_PASSWORD=strong_password`
- `DB_PORT=5432`

### Переменные для Docker Compose

- `DB_HOST=postgres`
- `REDIS_URL=redis://redis:6379/0`
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/1`

### Переменные для локального запуска без Docker

- `DB_HOST=127.0.0.1`
- `REDIS_URL=redis://127.0.0.1:6379/0`

### GitHub Secrets

Для автоматического деплоя используются GitHub Secrets:

- `SSH_KEY` — приватный SSH-ключ для подключения к серверу
- `SSH_USER` — пользователь сервера (ubuntu)
- `SERVER_IP` — публичный IP сервера
- `DEPLOY_DIR` — путь к проекту на сервере

Secrets используются в GitHub Actions workflow и не хранятся в репозитории.

## Важно

Значения:

- `DB_HOST=postgres`
- `redis://redis:6379/...`

используются **только при запуске через Docker Compose**.

Файл `.env` **не коммитится** и добавлен в `.gitignore`.

## CI (Continuous Integration)

CI запускается автоматически при каждом `push` в репозиторий.

На этапе CI выполняются следующие шаги:

- проверка кода с помощью **flake8**
- запуск тестов Django
- проверка сборки Docker-образов

## CD (Continuous Deployment)

Деплой выполняется **только для ветки `develop`** после успешного прохождения CI.

Во время деплоя выполняются следующие шаги:

- подключение к серверу по SSH
- обновление кода из ветки `develop`
- сборка и запуск сервисов через Docker Compose
- перезапуск контейнеров приложения

---

## Автор

**Olga Noskova**