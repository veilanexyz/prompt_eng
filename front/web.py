from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from st_pages import Page, show_pages

load_dotenv()  # take environment variables from .env.
show_pages( #они обновили, надо иначе писать
    [
        Page("web.py", "Главная", "🏠"),
        Page("pages/help_class.py", "Поиск достопримечательности по фотографии", "🖼️"),
        Page("pages/text2place.py", "Поиск достопримечательности по тексту", icon="🔎"),
        Page("pages/calibr.py", "Построение маршрута", icon="🌎")
    ]
)
# Отображение формы для ввода cloud_id
def show_input_form():
    st.write("Введите ваш cloud_id:")
    cloud_id = st.text_input("Cloud ID")

    if st.button("Сохранить"):
        # Сохранение cloud_id в переменные окружения
        os.environ['CLOUD_ID'] = cloud_id
        st.success("Cloud ID сохранен. Переход к основной странице...")
        st.rerun()  # Перезапуск приложения для перехода к основной странице

# Основная страница, к которой пользователь допускается после ввода cloud_id
def main_page():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
# Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    st.title("Мы поможем улучшить Ваш промпт!")
    if "placeholder" not in st.session_state:
        st.session_state.placeholder = ''
    if "messages" not in st.session_state:
        st.session_state.messages = []
    prompt = st.text_input(
            "Напишите промпт 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder,
        )
    instr = st.text_area(
            "Напишите инструкцию 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder,
        )
    bad_answer = st.text_area(
            "Напишите плохой ответ 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder,
        )
    if prompt:
        st.write("Ваш промпт: ", prompt)
        st.write("Рекомендованные промпты: ")
        st.write("Ответ при предложенном промпте")
        client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

def main():
    #st.title("Аутентификация по cloud_id")
    
    #st.page_link("web.py", label="Home", icon="🏠")
    #st.page_link("pages/help_class.py", label="Page 1", icon="1️⃣")
    #st.page_link("pages/calibr.py", label="Page 2", icon="2️⃣")
    if 'CLOUD_ID' in os.environ:
        main_page()
    else:
        show_input_form()

if __name__ == "__main__":
    main()