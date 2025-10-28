# Sakhatype - Typing Test Application

## Архитектура проекта

### Backend (Python FastAPI) - FSD структура

```
/app/backend/app/
├── core/                  # Ядро приложения
│   ├── config.py         # Конфигурация
│   ├── database.py       # База данных
│   └── security.py       # Безопасность и JWT
├── features/             # Функциональные модули
│   ├── auth/            # Аутентификация
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── router.py
│   ├── typing/          # Печатание
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── router.py
│   ├── user/            # Профиль пользователя
│   └── leaderboard/     # Таблица лидеров
└── shared/              # Общие утилиты
    └── dependencies.py
```

### Frontend (Vue 3 + TypeScript) - FSD структура

```
/app/frontend/src/
├── app/                  # Приложение
├── pages/               # Страницы (routes)
│   ├── home/
│   ├── leaderboard/
│   └── profile/
├── widgets/             # Сложные UI блоки
│   ├── header/
│   ├── footer/
│   └── typing-test/
├── features/            # Функции пользователя
│   ├── auth/
│   ├── typing/
│   └── sound/
├── entities/            # Бизнес-сущности
│   ├── user/
│   ├── test-result/
│   └── word/
└── shared/              # Переиспользуемый код
    ├── api/            # API клиенты
    ├── ui/             # UI компоненты (shadcn-vue)
    ├── lib/            # Утилиты
    └── composables/    # Vue composables
```

## Новые функции

### 1. ✅ Уровень пользователя в хедере
- Показывает уровень пользователя рядом с именем
- Бейдж "Таһым X" в выпадающем меню

### 2. ✅ Звуковая система
- Звук при каждом нажатии клавиши
- Звук при правильном символе
- Звук при неправильном символе
- Звук при завершении теста
- Переключатель звука в футере

**Как добавить звуки:**
Поместите ваши звуковые файлы в `/app/frontend/public/sounds/`:
- `keypress.mp3` - звук нажатия клавиши
- `correct.mp3` - правильный символ
- `incorrect.mp3` - неправильный символ
- `complete.mp3` - завершение теста

### 3. ✅ Улучшенная таблица лидеров
- Использует shadcn-vue Table компоненты
- Сортировка по всем колонкам
- Фильтрация/поиск по имени
- Красивое оформление медалей
- Отображение уровня каждого пользователя

### 4. ✅ Графики результатов (shadcn-vue charts)
- График WPM по времени
- График точности по времени
- Использует vue-chartjs с Chart.js
- Адаптивный дизайн

### 5. ✅ Улучшенное поле ввода (как в monkeytype)
- Плавная анимация курсора
- Показ лишних символов
- Анимация при ошибках
- Активное выделение текущего слова
- Более responsive и плавное

## Технологии

### Backend:
- FastAPI 0.119.1
- SQLAlchemy 2.0.44
- Pydantic 2.12.3
- Python-jose (JWT)
- Argon2 (password hashing)

### Frontend:
- Vue 3.5.22
- TypeScript
- Vite 7.1.11
- shadcn-vue (UI компоненты)
- Tailwind CSS 4.1.16
- Pinia (state management)
- Vue Router 4.6.3
- Chart.js + vue-chartjs (графики)
- @tanstack/vue-table (таблицы)

## Установка зависимостей

### Backend:
```bash
cd /app/backend
pip install -r requirements.txt
```

### Frontend:
```bash
cd /app/frontend
yarn install
```

## Запуск

Используйте supervisor для управления сервисами:
```bash
# Перезапустить все
sudo supervisorctl restart all

# Перезапустить только backend
sudo supervisorctl restart backend

# Перезапустить только frontend
sudo supervisorctl restart frontend

# Проверить статус
sudo supervisorctl status
```

## Структура API

### Authentication (`/api/auth`)
- `POST /register` - регистрация
- `POST /login` - вход
- `GET /me` - текущий пользователь

### Typing (`/api`)
- `GET /words` - получить слова
- `POST /results` - сохранить результат
- `GET /results/user/{username}` - результаты пользователя

### User Profile (`/api/profile`)
- `GET /{username}` - профиль пользователя

### Leaderboard (`/api/leaderboard`)
- `GET /wpm` - топ по WPM
- `GET /accuracy` - топ по точности

## База данных

SQLite база данных: `/app/backend/sakhatype.db`

Таблицы:
- `users` - пользователи
- `words` - слова для печати
- `test_results` - результаты тестов

## Разработка

Frontend имеет hot reload, изменения применяются автоматически.
Backend также имеет hot reload через uvicorn.

Только перезапускайте сервисы при:
- Установке новых зависимостей
- Изменении .env файлов
- Изменении конфигурации supervisor

## Лицензия

Сделано командой DotX
