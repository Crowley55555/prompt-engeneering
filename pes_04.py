"""
Приложение для создания SEO-оптимизированных описаний товаров с мониторингом через Langfuse

НАСТРОЙКА:
1. Установите зависимости: pip install -r requirements.txt
2. Создайте .env файл с переменными:
   OPENAI_API_KEY=ваш_ключ_openai
   LANGFUSE_PUBLIC_KEY=ваш_публичный_ключ_langfuse
   LANGFUSE_SECRET_KEY=ваш_секретный_ключ_langfuse
   LANGFUSE_HOST=https://cloud.langfuse.com (или ваш хост)

3. Получите ключи Langfuse:
   - Зарегистрируйтесь на https://cloud.langfuse.com
   - Создайте проект
   - Скопируйте Public Key и Secret Key из настроек проекта

МОНИТОРИНГ:
- Все запросы к OpenAI автоматически отслеживаются в Langfuse
- Можно просматривать трассировки, метрики и анализировать производительность
- При отсутствии ключей Langfuse приложение работает без мониторинга
"""

import time  # Импорт модуля time для работы с временем и задержками
import openai  # Импорт официальной библиотеки OpenAI для взаимодействия с API

from openai import OpenAI  # Импорт класса OpenAI для создания клиентов API
from langchain_core.prompts import ChatPromptTemplate  # Импорт класса для работы с шаблонами чат-запросов из библиотеки LangChain
from langchain_openai import ChatOpenAI  # Импорт класса ChatOpenAI для работы с чат-моделью OpenAI через LangChain

import requests  # Импорт библиотеки requests для выполнения HTTP-запросов
import json  # Импорт модуля json для работы с JSON-данными
from dotenv import load_dotenv
import os

# Импорты для мониторинга через Langfuse
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Переменные окружения для Langfuse
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Инициализация Langfuse
langfuse = Langfuse(
    public_key=langfuse_public_key,
    secret_key=langfuse_secret_key,
    host=langfuse_host
)
url = "https://api.openai.com/v1/chat/completions"  # URL эндпойнта OpenAI API для создания чат-комплитов

# Функция для создания описания товара с использованием современного LangChain
def conversation(user_input):
  # Создание CallbackHandler для мониторинга через Langfuse
  langfuse_handler = CallbackHandler()
  
  # Инициализация модели ChatOpenAI с заданным именем модели и температурой (контроль креативности)
  llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key  # используем переменную из окружения
    )

  # Создание шаблона промпта с переменной user_input, задающего роль модели и параметры SEO-ключевых слов
  prompt = ChatPromptTemplate.from_messages([
      ("system", """Составь SEO-оптимизированное описание для товара, следуя пошаговому рассуждению:

Шаг 1: Определи целевую аудиторию товара.
Шаг 2: Перечисли 3–4 ключевых преимущества товара.
Шаг 3: Включи ключевые слова: «механическая клавиатура», «Keychron K8 Pro», «RGB подсветка», «для программистов и геймеров» — так, чтобы они звучали естественно.
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

  # Создание цепочки (chain) - современный подход с использованием оператора |
  chain = prompt | llm

  # Вызов цепочки с передачей user_input и callback handler для мониторинга
  response = chain.invoke(
      {"user_input": user_input}, 
      config={"callbacks": [langfuse_handler]}
  )

  # Возвращаем текст ответа для дальнейшего использования
  return response.content

# Функция для тестирования интеграции с Langfuse
def test_langfuse_connection():
    """Тестирует подключение к Langfuse запуском минимального вызова LLM с CallbackHandler."""
    try:
        # Проверяем наличие необходимых переменных окружения
        if not langfuse_public_key or not langfuse_secret_key:
            print("⚠️  Переменные окружения Langfuse не настроены!")
            print("Добавьте в .env файл:")
            print("LANGFUSE_PUBLIC_KEY=ваш_публичный_ключ")
            print("LANGFUSE_SECRET_KEY=ваш_секретный_ключ")
            print("LANGFUSE_HOST=https://cloud.langfuse.com")
            return False

        # Создаем CallbackHandler и выполняем минимальный вызов модели
        handler = CallbackHandler()

        test_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
            api_key=api_key
        )

        # Короткий пинг-запрос для проверки, что события доходят до Langfuse
        _ = test_llm.invoke("ping", config={"callbacks": [handler]})

        # Явная отправка накопленных событий SDK
        try:
            langfuse.flush()
        except Exception:
            # В некоторых версиях Python SDK flush может отсутствовать — это не критично
            pass

        print("✅ Подключение к Langfuse успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к Langfuse: {e}")
        return False

# Пример вызова функции conversation с запросом на описание товара
if __name__ == "__main__":
    print("🚀 Запуск приложения с мониторингом через Langfuse")
    print("="*60)
    
    # Тестируем подключение к Langfuse
    if test_langfuse_connection():
        print("📊 Мониторинг активен - все запросы будут отслеживаться в Langfuse")
    else:
        print("⚠️  Мониторинг отключен - приложение будет работать без отслеживания")
    
    print("="*60)
    
    try:
        text = input("Введите запрос на описание товара: ")
        print("\n🔄 Обработка запроса...")
        
        result = conversation(text)
        
        print("\n" + "="*50)
        print("📝 Результат:")
        print(result)
        print("="*50)
        
        if langfuse_public_key and langfuse_secret_key:
            print("📊 Данные отправлены в Langfuse для мониторинга")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Это может быть связано с недоступностью OpenAI API в вашем регионе.")