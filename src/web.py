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
        st.rerun()


def classification_page(prompt):
    if prompt:
        st.write("Ваш промпт: ", prompt)

        tag = classify_prompt(prompt)
        st.write(f"Классифицировано как: {tag}")
        recommendations = generate_recommendations(prompt)
        st.write("Рекомендованные промпты:")
        for rec in recommendations:
            st.write(rec)


def calibration_page(prompt):
    if prompt:
        recommendations = generate_recommendations(prompt)
        best_recommendation = calibrate_and_select_best(recommendations)
        st.write("Лучшая рекомендация:")
        st.write(best_recommendation)


def main_page(selected_page):
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

    # Вызываем функции в зависимости от выбранной страницы
    if selected_page == "Классификация":
        classification_page(prompt)
    elif selected_page == "Калибровка и улучшение":
        calibration_page(prompt)


def sidebar_navigation():
    st.sidebar.title("Навигация")
    selected_page = st.sidebar.selectbox("Выберите страницу:", ["Классификация", "Калибровка и улучшение"])
    return selected_page


def main():
    if 'CLOUD_ID' in os.environ:
        if showSidebarNavigation:
            selected_page = sidebar_navigation()
            main_page(selected_page)
    else:
        show_input_form()


if __name__ == "__main__":
    main()
