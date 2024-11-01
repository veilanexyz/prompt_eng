import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

def generate_answers(recommendations):
    c = os.getenv("CATALOG_API")
    urlm = "gpt://" + str(c) + "/yandexgpt-lite"
    yapi = os.getenv("YANDEXGPT_API_KEY")
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yapi}"
    }
    result = []
    for recommendation in recommendations:
        prompt = {
            "modelUri": urlm,
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "1000"
            },
            "messages": [
                {
                    "role": "user",
                    "text": f"Напиши ответ по этому промпту: {recommendation}"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=prompt)
        response_json = response.json()
        if 'result' in response_json:
            try:
                message_text = response_json['result']['alternatives'][0]['message']['text']
                result.append(message_text)
            except (KeyError, IndexError):
                result.append("Ошибка: Невозможно извлечь текст ответа.")
        elif 'error' in response_json:
            error_message = response_json['error'].get('message', 'Неизвестная ошибка')
            result.append(f"Ошибка API: {error_message}")
        else:
            result.append("Ошибка: неожиданный формат ответа от API.")
    
    return result
