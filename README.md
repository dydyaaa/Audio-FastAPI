# Audio-FastAPI
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-3.1+-lightblue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0+-lightgrey.svg)
![Версия](https://img.shields.io/badge/Version-0.0.1-blue)

Это REST API для загрузки, управления и удаления аудиофайлов с авторизацией через Yandex OAuth. Проект предоставляет функционал для обычных пользователей и суперпользователей, включая управление пользователями и их файлами.

## Как авторизоваться

1. **Получение JWT-токена**:
   - Перейдите на `GET /auth/login` (например, через `http://localhost:8000/docs`).
   - Вы получите URL для авторизации через Yandex:
     ```
     {
         "auth_url": "https://oauth.yandex.ru/authorize?response_type=code&client_id=<your_client_id>"
     }
     ```
   - Перейдите по этому URL, авторизуйтесь через Yandex и получите jwt token. 
   - На Windows может быть проблема с редиректом. Необходимо заменить 0.0.0.0 на localhost. Фиксится деплоем на хостинг.
     ```
     {
         "message": "User authorized",
         "user_id": 1,
         "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
     }
     ```
   - Скопируйте `jwt_token`.

2. **Использование токена в Swagger UI**:
   - Откройте `http://localhost:8000/docs`.
   - Нажмите кнопку "Authorize" в правом верхнем углу.
   - Вставьте `jwt_token` (без `Bearer`, просто строку) и нажмите "Authorize".
   - Теперь все защищённые endpoint-ы будут использовать этот токен.

## Чем можно делать

### Для обычных пользователей
- **Управление аудиофайлами**:
  - `POST /audio/upload/` — Загрузить аудиофайл (форматы: .mp3, .wav, .ogg).
  - `GET /audio/files/` — Получить список своих аудиофайлов.
  - `DELETE /audio/delete/{audio_id}` — Удалить свой аудиофайл.
- **Управление профилем**:
  - `GET /users/me/` — Получить свой email.
  - `PUT /users/me/` — Изменить свой email (требуется JSON: `{"email": "new_email@example.com"}`).

### Для суперпользователей
- **Управление пользователями**:
  - `GET /super-users/users/{user_id}/` — Получить информацию о любом пользователе.
  - `GET /super-users/users/{user_id}/audio/` — Получить список аудиофайлов любого пользователя.
  - `DELETE /super-users/users/{user_id}/` — Удалить пользователя и все его файлы (кроме суперпользователей).

## Технологии

- **Backend**: FastAPI (Python 3.12)
- **База данных**: PostgreSQL (с асинхронным драйвером `asyncpg`)
- **ORM**: SQLAlchemy 2.0 (асинхронный режим)
- **Авторизация**: JWT (JSON Web Tokens) через Yandex OAuth
- **Миграции**: Alembic
- **Контейнеризация**: Docker и Docker Compose
- **Зависимости**: Pydantic (валидация), httpx (HTTP-запросы), jose (JWT)
- **Логирование**: Встроенный модуль Python `logging`

## Как развернуть через Docker

### Требования
- Установлены Docker и Docker Compose:
  ```bash
  docker --version
  docker-compose --version
    ```

## Шаги

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/dydyaaa/Audio-FastAPI.git
cd Audio-FastAPI
```

### 2. Создайте .env файл в корне проекта:
- Пример файла есть в репозитории .env.example
- Создайте приложение на https://oauth.yandex.ru/
- Redirect URI для веб-сервисов укажите http://0.0.0.0:8000/auth/callback
- Добавьте свой YANDEX_CLIENT_ID и YANDEX_CLIENT_SECRET в файл .env

### 3. Запустите Docker Compose:
```bash
docker compose up --build -d
```

### 4. Проверка
- Откройте http://localhost:8000/docs для Swagger UI.

### 5. Остановка
```bash
docker compose stop
```

## Дальнейшие улучшения
- Создание авто-тестов
- Добавление кэширования
- Интегрирование брокера сообщений 
- Добавление метрик и их визуализаций