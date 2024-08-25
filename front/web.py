import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from help_class import classify_prompt, generate_recommendations
from calibr import calibrate_and_select_best

load_dotenv() 


showSidebarNavigation = True


def show_input_form():
    st.write("Введите ваш Cloud ID:")
    cloud_id = st.text_input("Cloud ID")

    if st.button("Сохранить"):
        os.environ['CLOUD_ID'] = cloud_id
        st.success("Cloud ID сохранен. Переход к основной странице...")
        st.experimental_rerun()  

def main_page():
    st.title("Мы поможем улучшить Ваш промпт!")

    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    if "placeholder" not in st.session_state:
        st.session_state.placeholder = ''
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Ввод данных пользователем
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

        tag = classify_prompt(prompt)
        st.write(f"Классифицировано как: {tag}")
        recommendations = generate_recommendations(prompt)
        st.write("Рекомендованные промпты:")
        for rec in recommendations:
            st.write(rec)


        best_recommendation = calibrate_and_select_best(recommendations)
        st.write("Лучшая рекомендация:")
        st.write(best_recommendation)


def sidebar_navigation():
    st.sidebar.title("Навигация")
    selected_page = st.sidebar.selectbox("Выберите страницу:", ["Классификация", "Калибровка и улучшение"])
    
    if selected_page == "Классификация":
        st.sidebar.write("Страница классификации промптов")
    elif selected_page == "Калибровка и улучшение":
        st.sidebar.write("Страница калибровки и улучшения")


def main():
    if 'CLOUD_ID' in os.environ:
        if showSidebarNavigation:
            sidebar_navigation()
        main_page()
    else:
        show_input_form()

if __name__ == "__main__":
    main()
