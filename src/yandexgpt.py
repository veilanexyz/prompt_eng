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
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "user",
                    "text": f"Напиши ответ по этому промпту: {recommendation}"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=prompt)

        try:
            response_json = response.json()
            message_text = response_json['result']['alternatives'][0]['message']['text']
            result.append(message_text)
        except (json.JSONDecodeError, KeyError):
            result.append("Ошибка: не удалось получить корректный ответ.")

    return "\n".join(result) 

