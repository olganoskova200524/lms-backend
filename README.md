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

## Deployment & CI/CD

### Общая схема

Проект деплоится автоматически с помощью **GitHub Actions**.

Схема работы:

1. Разработка ведётся в feature-ветках
2. Создаётся Pull Request в ветку `develop`
3. При push / merge в `develop`:
    - запускаются тесты
    - при успешных тестах выполняется деплой на сервер

---

### Требования к серверу

Удалённый сервер (Ubuntu) должен иметь:

- Python 3.12+
- Poetry
- PostgreSQL
- Redis
- systemd
- Открытые порты: `22`, `80` (и `8000`, если доступ к backend осуществляется напрямую без Nginx)

---

### Размещение проекта на сервере

Проект разворачивается в каталоге:

```bash
/home/ubuntu/apps/lms-backend
```

Код на сервере всегда находится в ветке develop

Если **Nginx не настроен**, backend доступен напрямую по адресу:

```text
http://<SERVER_IP>:8000
```

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
- `DB_HOST=127.0.0.1`
- `DB_PORT=5432`
- `REDIS_URL=redis://127.0.0.1:6379/0`
- `CELERY_BROKER_URL=redis://127.0.0.1:6379/0`
- `CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1`

## ⚠️ Важно

Значения:

- `DB_HOST=postgres`
- `redis://redis:6379/...`

используются **только при запуске через Docker Compose**.

При деплое на сервер **без Docker** необходимо использовать:

```text
127.0.0.1
```

Файл `.env` **не коммитится** и добавлен в `.gitignore`.

## CI (тесты)

Workflow **GitHub Actions**:

- запускается при каждом `push`;
- устанавливает зависимости через **Poetry**;
- выполняет команду:

```bash
poetry run python manage.py test
```

При ошибках тестов деплой не выполняется.

## 🚚 CD (деплой)

Деплой выполняется **только для ветки `develop`** после успешного прохождения тестов.

### Во время деплоя выполняются шаги:

- **GitHub Actions** подключается к серверу по **SSH**;
- выполняется обновление кода:

```bash
git pull origin develop
```

- устанавливаются зависимости:

```bash
poetry install --no-interaction --no-root
```

- применяются миграции базы данных:

```bash
poetry run python manage.py migrate --noinput
```

- перезапускается backend-сервис:

```bash
sudo systemctl restart lms-backend.service
```

## Управление приложением

Backend-приложение запускается через **Gunicorn** и управляется **systemd**.

- сервис: `lms-backend.service`
- автоматический перезапуск при падении
- перезапуск при деплое

### Проверка состояния сервиса на сервере

```bash
sudo systemctl status lms-backend.service
sudo journalctl -u lms-backend.service -n 50 --no-pager
```
---

## Автор

**Olga Noskova**