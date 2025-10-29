# 🤖 Телеграм-боты на aiogram для SEO-описаний товаров

Два стабильных телеграм-бота для создания SEO-оптимизированных описаний товаров на базе **aiogram 3.x**:
- **OpenAI Bot** (`aiogram_bot_openai.py`) - на основе OpenAI GPT-4
- **GigaChat Bot** (`aiogram_bot_gigachat.py`) - на основе GigaChat API

## ✅ Преимущества aiogram

- **Стабильность** - нет проблем с event loop
- **Производительность** - быстрая обработка сообщений
- **Современность** - последняя версия библиотеки
- **Простота** - понятный и чистый код
- **FSM** - встроенная поддержка состояний

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Создайте `.env` файл и добавьте необходимые переменные:

```env
# OpenAI API ключ
OPENAI_API_KEY=sk-your-openai-api-key-here

# Telegram бот токен
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890

# Langfuse мониторинг (опционально)
LANGFUSE_PUBLIC_KEY=pk-your-langfuse-public-key-here
LANGFUSE_SECRET_KEY=sk-your-langfuse-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# GigaChat учетные данные (для GigaChat бота)
GIGACHAT_CREDENTIALS=./gigachat_credentials.json
```

### 3. Получение токена бота
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Выполните команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env` файл

### 4. Запуск ботов

#### OpenAI Bot
```bash
py aiogram_bot_openai_pes_06.py
```

#### GigaChat Bot
```bash
py aiogram_bot_gigachat.py
```

## 📱 Использование ботов

### Команды бота
- `/start` - Запустить бота и показать приветствие
- `/help` - Показать справку по использованию
- `/status` - Проверить статус мониторинга

### Создание SEO-описания
1. Отправьте боту название товара или его краткое описание
2. Бот создаст структурированное SEO-описание
3. Получите готовый текст с ключевыми словами

### Примеры запросов
- "Механическая клавиатура для программистов"
- "Беспроводные наушники с шумоподавлением"
- "Умные часы для спорта"
- "Смартфон с хорошей камерой"

## 🔧 Подробная настройка

### OpenAI Bot

1. **Получите OpenAI API ключ:**
   - Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
   - Перейдите в раздел API Keys
   - Создайте новый ключ

2. **Настройте .env файл:**
   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   OPENAI_API_KEY=sk-your-openai-api-key
   ```

### GigaChat Bot

1. **Получите учетные данные GigaChat:**
   - Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru)
   - Создайте приложение
   - Получите `client_id` и `client_secret`

2. **Создайте файл с учетными данными:**
   ```json
   {
     "client_id": "ваш_client_id",
     "client_secret": "ваш_client_secret",
     "scope": "GIGACHAT_API_PERS"
   }
   ```

3. **Настройте .env файл:**
   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   GIGACHAT_CREDENTIALS=./gigachat_credentials.json
   ```

### Мониторинг через Langfuse (опционально)

1. **Получите ключи Langfuse:**
   - Зарегистрируйтесь на [cloud.langfuse.com](https://cloud.langfuse.com)
   - Создайте проект
   - Скопируйте Public Key и Secret Key

2. **Добавьте в .env файл:**
   ```env
   LANGFUSE_PUBLIC_KEY=pk-your-public-key
   LANGFUSE_SECRET_KEY=sk-your-secret-key
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

## 📊 Мониторинг и аналитика

При включенном мониторинге Langfuse вы можете:

- **Просматривать трассировки** всех запросов к AI
- **Анализировать метрики** времени выполнения и токенов
- **Отслеживать качество** ответов и их соответствие промптам
- **Настраивать алерты** о проблемах с производительностью

## 🔍 Структура проекта

```
├── aiogram_bot_openai.py      # Бот на OpenAI (aiogram)
├── aiogram_bot_gigachat.py    # Бот на GigaChat (aiogram)
├── telegram_bot_openai.py     # Старый бот на python-telegram-bot
├── telegram_bot_gigachat.py   # Старый бот на python-telegram-bot
├── pes_06.py                  # Исходный файл
├── requirements.txt           # Зависимости
├── .env                       # Переменные окружения
├── README_aiogram_bots.md     # Эта документация
└── gigachat_credentials.json  # Учетные данные GigaChat
```

## 🛠 Устранение неполадок

### Ошибка "TELEGRAM_BOT_TOKEN не найден"
- Убедитесь, что токен бота указан в `.env` файле
- Проверьте правильность токена

### Ошибка "OPENAI_API_KEY не найден" (для OpenAI бота)
- Убедитесь, что API ключ указан в `.env` файле
- Проверьте правильность ключа

### Ошибка "GIGACHAT_CREDENTIALS не найден" (для GigaChat бота)
- Убедитесь, что путь к файлу с учетными данными указан правильно
- Проверьте, что файл `gigachat_credentials.json` существует

### Ошибка "Invalid credentials" в Langfuse
- Проверьте правильность ключей Langfuse
- Убедитесь, что хост указан корректно

### Бот не отвечает на сообщения
- Проверьте, что бот запущен
- Убедитесь, что токен бота действителен
- Проверьте логи на наличие ошибок

## 🔒 Безопасность

- **Никогда не публикуйте** ваши API ключи и токены
- Добавьте `.env` в `.gitignore`
- Регулярно обновляйте ключи
- Используйте разные токены для разных окружений

## 📈 Производительность

### OpenAI Bot
- Быстрая обработка запросов
- Высокое качество генерации
- Поддержка множества языков

### GigaChat Bot
- Работает на российской платформе
- Отличная поддержка русского языка
- Быстрая обработка запросов

## 🆚 Сравнение с python-telegram-bot

| Функция | aiogram | python-telegram-bot |
|---------|---------|-------------------|
| Стабильность | ✅ Высокая | ❌ Проблемы с event loop |
| Производительность | ✅ Быстрая | ⚠️ Средняя |
| FSM | ✅ Встроенная | ❌ Требует дополнительных библиотек |
| Современность | ✅ Активная разработка | ⚠️ Медленное обновление |
| Простота кода | ✅ Чистый код | ⚠️ Более сложный |

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

---

**Рекомендуется использовать ботов на aiogram для стабильной работы!** 🎉
