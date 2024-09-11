from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from st_pages import Page

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(api_key))

def get_recs_data() -> str:
    folder_path = "../gpt-prompting-guide" 
    combined_text = ""
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + "\n" 
    
    return combined_text

metaprompt = get_recs_data()
#добавь: здесь будут выводиться рекомендации из доки по улучшению
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
