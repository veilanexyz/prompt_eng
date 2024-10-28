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

def calibrate_and_select_best(recommendations, ans, n):
    ranked_recommendations = {}

    for i in range(n):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user", 
                "content": f"Оцени ответ по шкале от 1 до 10, где 10 — лучший: {ans[i]}. Ответь только числом. Не нужны ни приветствия, ни подтверждения того, что ты меня поняла. Только число от 1 до 10. Тебе нельзя использовать слова, можно использовать только число от 1 до 10"
            }],
            max_tokens=100
        )
        
        rank_text = response.choices[0].message.content.strip()
        print(rank_text)
        try:
            rank = int(rank_text)
        except ValueError:
            print(f"Невалидный ответ: {rank_text}, пропускаю...")
            continue
        ranked_recommendations[rank] = recommendations[i]
    
    if not ranked_recommendations:
        return None
    
    best_rank = max(ranked_recommendations.keys())
    best_recommendation = ranked_recommendations[best_rank]
    return best_recommendation

def generate_recommendations(prompt, n=5):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user", 
            "content": f"Предложи промпт для более хорошего ответа на основе этого промпта: {prompt}. Используй для качественного составления руководство {metaprompt}, но не предлагай ответы из него, оно только для тебя."
        }],
        max_tokens=500,  
        n=n
    )
    
    recommendations = [choice.message.content for choice in response.choices]
    return recommendations
