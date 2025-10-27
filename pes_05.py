import time  # Импорт модуля time для работы с временем и задержками
import openai  # Импорт официальной библиотеки OpenAI для взаимодействия с API

from openai import OpenAI  # Импорт класса OpenAI для создания клиентов API
from langchain_core.prompts import ChatPromptTemplate  # Импорт класса для работы с шаблонами чат-запросов из библиотеки LangChain
from langchain_openai import ChatOpenAI  # Импорт класса ChatOpenAI для работы с чат-моделью OpenAI через LangChain

import requests  # Импорт библиотеки requests для выполнения HTTP-запросов
import json  # Импорт модуля json для работы с JSON-данными
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"  # URL эндпойнта OpenAI API для создания чат-комплитов

# Пример 1: Использование OpenAI API напрямую через requests
print("=== Пример 1: Прямое использование OpenAI API ===")

headers = {
    "Authorization": f"Bearer {api_key}",  # Заголовок авторизации с Bearer токеном API ключа
    "Content-Type": "application/json"  # Указание, что тело запроса будет в формате JSON
}

data = {
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Привет! Расскажи, как приготовить картошку фри во фритюрнице."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 300
}

# Отправка POST-запроса к API с заголовками и сериализованными данными JSON
response = requests.post(url, headers=headers, data=json.dumps(data))

# Вывод JSON-ответа в удобном для чтения виде, с поддержкой русских символов
print(f"Статус ответа: {response.status_code}")  # Вывод HTTP-статуса ответа (например, 200 - успешно)

if response.status_code == 200:
    result = response.json()
    print(f"Ответ от OpenAI: {result['choices'][0]['message']['content']}")
else:
    print(f"Ошибка: {response.text}")

print("\n" + "="*50 + "\n")

# Пример 2: Использование LangChain (современный подход)
print("=== Пример 2: Использование LangChain (современный подход) ===")

try:
    # Создание экземпляра ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=300,
        api_key=api_key
    )
    
    # Создание шаблона промпта
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Привет! Расскажи, как приготовить картошку фри во фритюрнице.")
    ])
    
    # Создание цепочки (chain) - современный подход
    chain = prompt | llm
    
    # Выполнение запроса
    response = chain.invoke({})
    
    print(f"Ответ от LangChain: {response.content}")
    
except Exception as e:
    print(f"Ошибка при использовании LangChain: {e}")

print("\n" + "="*50 + "\n")

# Пример 3: Использование OpenAI Python SDK
print("=== Пример 3: Использование OpenAI Python SDK ===")

try:
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Привет! Расскажи, как приготовить картошку фри во фритюрнице."}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    print(f"Ответ от OpenAI SDK: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"Ошибка при использовании OpenAI SDK: {e}")

print("\nПрограмма завершена!")