import requests
from dotenv import load_dotenv
import os
load_dotenv()
c = os.getenv("CATALOG_API")
urlm = "gpt://" + str(c) + "/yandexgpt-lite"
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
            "text": f"Напиши ответ по этому промпту {recommendation}"
        }
    ]
}

yapi = os.getenv("YANDEXGPT_API_KEY")
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {yapi}"
}

response = requests.post(url, headers=headers, json=prompt)
result = response.text
print(result)