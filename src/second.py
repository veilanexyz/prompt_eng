#тоже как в примере с клаудом + в доке есть нюансы можно руками дописать (добавить ягпт)
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
#добавь:нормальная классификация, использующая гптшку
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(api_key))

def calibrate_and_select_best(recommendations):
    best_recommendation = "1"
    return best_recommendation

def generate_recommendations(prompt, n=5):
    recommendations = []
    for _ in range(n):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Предложи несколько промптов для более хорошего ответа на основе этого промпта {prompt}"}],
            max_tokens=50
        )
        recommendation = response.choices[0].message.content
        recommendations.append(recommendation)
    
    return recommendations