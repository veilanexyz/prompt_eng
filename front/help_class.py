from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from st_pages import Page

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(api_key))
def classify_prompt(prompt):
    if "вопрос" in prompt.lower():
        return "вопрос"
    elif "команда" in prompt.lower():
        return "команда"
    else:
        return "другое"

def generate_recommendations(prompt, n=10):
    recommendations = []
    for _ in range(n):
        response = client.completions.create(
            model="gpt-4o-mini",
            prompt=f"Generate a recommendation based on: {prompt}",
            max_tokens=50
        )
        recommendation = response.choices[0].text.strip()
        recommendations.append(recommendation)
    
    return recommendations
