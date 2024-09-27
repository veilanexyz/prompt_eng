from openai import OpenAI
import streamlit as st
from yandexgpt import generate_answers
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(api_key), base_url="https://openai-proxy-vercel-gamma.vercel.app/v1/")

file_path = os.path.join(os.getcwd(), "combined_text.md")

def get_metaprompt():
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

metaprompt = get_metaprompt()

def calibrate_and_select_best(recommendations, n=5):
    for i in range(n):
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", 
                        "content": f"Выведи цифру {recommendations[i]}"
                        }],
                max_tokens=1
            )
        rec = {
                i: response.choices[0].message.content,
                "ans":recommendations[i]
            }
    print(rec)
    #best_recommendation = rec[0]
    return 1

def generate_recommendations(prompt, n=5):
    #recommendations = []
    #for _ in range(n):
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", 
                       "content": f"Предложи промпт для более хорошего ответа на основе этого промпта {prompt}. Используй для качественного составления руководство {metaprompt}, но не предлагай ответы из него, оно только для тебя"
                       }],
            max_tokens=500,
            n = 5
        )
    
    recommendations = response.choices
    print(recommendations)
    #recommendations.append(recommendation)
    return recommendations