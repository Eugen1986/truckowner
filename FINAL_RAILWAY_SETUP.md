# Railway Deployment - Final Setup

## Минимальные файлы для успешного деплоя

```
main.py              ✅ Flask WSGI точка входа
requirements.txt     ✅ Python зависимости (standard format)
runtime.txt         ✅ python-3.11.8
Procfile           ✅ web: gunicorn --bind 0.0.0.0:$PORT main:app
railway.json       ✅ Упрощенная конфигурация
app.py             ✅ Основное приложение Flask
templates/         ✅ HTML шаблоны
static/            ✅ CSS, JS, изображения
```

## Убрано для совместимости

❌ pyproject.toml - конфликтует с Railway uv
❌ nixpacks.toml - вызывает nix errors
❌ deps.txt - переименован в requirements.txt

## Автоматическое определение Railway

Railway автоматически:
- Определяет Python проект по requirements.txt
- Использует runtime.txt для версии Python
- Запускает команду из Procfile
- Устанавливает зависимости через pip

## Переменные окружения

Минимально необходимые:
```
SESSION_SECRET=ваш-случайный-ключ
```

Опциональные:
```
TELEGRAM_BOT_TOKEN=ваш-токен-бота
SENDGRID_API_KEY=ваш-ключ-sendgrid
```

## Команда запуска

Railway выполнит: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app`

Порт $PORT автоматически назначается Railway.