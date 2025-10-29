"""
Телеграм-бот для создания SEO-оптимизированных описаний товаров с OpenAI API (aiogram)

НАСТРОЙКА:
1. Установите зависимости: pip install -r requirements.txt
2. Создайте .env файл с переменными:
   OPENAI_API_KEY=ваш_ключ_openai
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   LANGFUSE_PUBLIC_KEY=ваш_публичный_ключ_langfuse (опционально)
   LANGFUSE_SECRET_KEY=ваш_секретный_ключ_langfuse (опционально)
   LANGFUSE_HOST=https://cloud.langfuse.com (опционально)

3. Получите токен бота:
   - Напишите @BotFather в Telegram
   - Создайте нового бота командой /newbot
   - Скопируйте полученный токен

МОНИТОРИНГ:
- Все запросы к OpenAI автоматически отслеживаются в Langfuse
- Можно просматривать трассировки, метрики и анализировать производительность
- При отсутствии ключей Langfuse приложение работает без мониторинга
"""

import asyncio
import logging
from typing import Dict, Any

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Инициализация Langfuse
langfuse = Langfuse(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_HOST
)

# Состояния FSM
class UserStates(StatesGroup):
    waiting_for_description = State()

# Хранилище состояний пользователей
user_states: Dict[int, str] = {}

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class SEOAssistantBot:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=OPENAI_API_KEY
        )
        
        # Создание промпта для SEO-описаний
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Составь SEO-оптимизированное описание для товара, следуя пошаговому рассуждению:

Шаг 1: Определи целевую аудиторию товара.
Шаг 2: Перечисли 3–4 ключевых преимущества товара.
Шаг 3: Включи ключевые слова естественным образом в текст.
Шаг 4: Сформулируй призыв к действию.
Шаг 5: Объедини всё в связный текст объёмом 150–200 слов.

Ограничение: до 500 слов.
Проверь текст на отсутствие противоречий и повторов.

Формат вывода:
🔹 **Название товара:**
[краткое и ёмкое название с УТП]

🔹 **Краткое описание (1–2 предложения):**
[одно сильное преимущество, мотивирующее купить]

🔹 **Полное описание (5–7 предложений):**
[описание функций, удобства, выгоды и сценария использования; ориентировано на покупателя]

🔹 **Преимущества:**
- [пункт 1]
- [пункт 2]
- [пункт 3]
- [пункт 4]

🔹 **Характеристики:**
- [параметр: значение]
- [параметр: значение]
- [параметр: значение]
- [параметр: значение]

🔹 **SEO-ключевые слова:**
[через запятую]"""),
            ("user", "Запрос пользователя: {user_input}")
        ])

    async def generate_seo_description(self, user_input: str, user_id: int) -> str:
        """Генерирует SEO-описание товара"""
        try:
            # Создание CallbackHandler для мониторинга через Langfuse
            langfuse_handler = CallbackHandler()
            
            # Создание цепочки
            chain = self.prompt | self.llm
            
            # Вызов цепочки с мониторингом
            response = chain.invoke(
                {"user_input": user_input},
                config={"callbacks": [langfuse_handler]}
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"Ошибка генерации описания для пользователя {user_id}: {e}")
            return f"❌ Произошла ошибка при генерации описания: {str(e)}"


# Создание экземпляра бота
seo_bot = SEOAssistantBot()


@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    user = message.from_user
    await state.set_state(UserStates.waiting_for_description)
    
    welcome_text = f"""🤖 Привет, {user.first_name}!

Я - SEO-ассистент для создания описаний товаров. Я помогу тебе создать профессиональные, SEO-оптимизированные описания для любых товаров.

📝 **Как пользоваться:**
1. Отправь мне описание товара или его название
2. Я создам структурированное SEO-описание
3. Получи готовый текст с ключевыми словами

🚀 **Начнем?** Просто отправь мне описание товара!"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать описание", callback_data="create_description")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """📚 **Помощь по использованию бота**

**Основные команды:**
/start - Запустить бота
/help - Показать эту справку
/status - Проверить статус мониторинга

**Как создать описание:**
1. Отправь название товара или его краткое описание
2. Бот создаст структурированное SEO-описание
3. Получи готовый текст с ключевыми словами

**Примеры запросов:**
• "Механическая клавиатура для программистов"
• "Беспроводные наушники с шумоподавлением"
• "Умные часы для спорта"

**Формат результата:**
• Название товара
• Краткое описание
• Полное описание
• Преимущества
• Характеристики
• SEO-ключевые слова"""
    
    await message.answer(help_text)


@dp.message(Command("status"))
async def status_command(message: types.Message):
    """Обработчик команды /status"""
    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        status_text = "✅ **Мониторинг активен**\n\nВсе запросы отслеживаются в Langfuse для анализа производительности."
    else:
        status_text = "⚠️ **Мониторинг отключен**\n\nДобавьте ключи Langfuse в .env файл для включения мониторинга."
    
    await message.answer(status_text)


@dp.message(UserStates.waiting_for_description)
async def handle_description_request(message: types.Message, state: FSMContext):
    """Обработчик запросов на создание описания"""
    user = message.from_user
    message_text = message.text
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer("🔄 Обрабатываю запрос...")
    
    # Генерируем описание
    result = await seo_bot.generate_seo_description(message_text, user.id)
    
    # Удаляем сообщение о обработке
    await processing_msg.delete()
    
    # Отправляем результат
    await message.answer(f"📝 **SEO-описание готово:**\n\n{result}")
    
    # Предлагаем создать еще одно описание
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать еще одно", callback_data="create_description")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    
    await message.answer("Хочешь создать еще одно описание?", reply_markup=keyboard)


@dp.callback_query(F.data == "create_description")
async def create_description_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки создания описания"""
    await state.set_state(UserStates.waiting_for_description)
    await callback.message.edit_text("📝 Отправь мне описание товара или его название, и я создам SEO-описание!")
    await callback.answer()


@dp.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    """Обработчик кнопки помощи"""
    help_text = """📚 **Помощь по использованию бота**

**Как создать описание:**
1. Отправь название товара или его краткое описание
2. Бот создаст структурированное SEO-описание
3. Получи готовый текст с ключевыми словами

**Примеры запросов:**
• "Механическая клавиатура для программистов"
• "Беспроводные наушники с шумоподавлением"
• "Умные часы для спорта"""
    
    await callback.message.edit_text(help_text)
    await callback.answer()


async def main():
    """Основная функция запуска бота"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
        return
    
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY не найден в переменных окружения!")
        return
    
    logger.info("🚀 Запуск SEO-ассистента бота на aiogram...")
    
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
