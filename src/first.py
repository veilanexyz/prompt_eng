from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from st_pages import Page
from functools import lru_cache

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(api_key), base_url="https://openai-proxy-vercel-gamma.vercel.app/v1/")
file_path = os.path.join(os.getcwd(), "combined_text.md")
    
@lru_cache(maxsize=1)
def get_metaprompt():
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

metaprompt = get_metaprompt()

def recommendations(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
            "content": f"Напиши несколько рекомендаций для данного промпта: {prompt}, используя для составления рекомендаций данное руководство: {metaprompt}. Напиши законченный ответ не превышающий 1000 токенов"}],
            max_tokens=1000
    )
    recommendation = response.choices[0].message.content
    return recommendation
