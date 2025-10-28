### Python venv (виртуальное окружение)

```bash
py -m venv venv         # Создание виртуального окружения
venv\Scripts\activate   # Активация виртуального окружения (Windows)
```

> 💡 Если активация не работает, откройте PowerShell от имени администратора и выполните:

```powershell
Set-ExecutionPolicy RemoteSigned
```

---

### Запуск Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080   # Запуск
```
---

### Работа с зависимостями (requirements.txt)

```bash
pip install -r requirements.txt    # Установка зависимостей
pip freeze > requirements.txt      # Сохранение зависимостей
```
