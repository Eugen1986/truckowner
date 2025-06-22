# Railway.com Deployment Fix

## Проблема
Railway использует uv для установки пакетов, который конфликтует с pyproject.toml без поля `name`.

## Решение
Удален проблематичный pyproject.toml, настроены альтернативные конфигурации.

## Файлы для загрузки в GitHub

### Обязательные файлы:
```
main.py                 # Точка входа приложения
app.py                  # Основное Flask приложение  
requirements.txt        # Зависимости Python (переименован из deps.txt)
runtime.txt            # Версия Python для Railway
railway.json           # Настройки Railway (упрощенный)
Procfile              # Команда запуска
setup.py              # Альтернативная конфигурация зависимостей
```

### Структура репозитория:
```
your-repo/
├── main.py              ✅ ОБЯЗАТЕЛЬНО
├── app.py               ✅ Flask приложение
├── requirements.txt     ✅ Зависимости (НЕ deps.txt!)
├── nixpacks.toml       ✅ Nixpacks конфигурация
├── railway.json        ✅ Railway настройки
├── Procfile           ✅ Команда запуска
├── setup.py           ✅ Альтернативные зависимости
├── telegram_bot.py    ✅ Telegram функционал
├── email_service.py   ✅ Email сервис
├── forms.py           ✅ Формы
├── templates/         ✅ HTML шаблоны
├── static/            ✅ CSS, JS, изображения
└── uploads/           ✅ Директория файлов
```

### НЕ загружайте:
- ❌ pyproject.toml (конфликтует с uv)
- ❌ ZIP архивы
- ❌ deps.txt (переименован в requirements.txt)

## Инструкции

1. **Удалите из репозитория:**
   - pyproject.toml
   - Любые ZIP файлы
   - deps.txt

2. **Загрузите обновленные файлы:**
   - requirements.txt (содержит все зависимости)
   - nixpacks.toml (настройка сборки)
   - railway.json (упрощенная конфигурация)

3. **Настройте переменную окружения в Railway:**
   ```
   SESSION_SECRET=your-random-secret-key-here
   ```

4. **Попробуйте деплой снова**

Railway теперь будет использовать стандартный pip install -r requirements.txt вместо проблематичного uv.