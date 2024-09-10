import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from first import recommendations
from second import calibrate_and_select_best, generate_recommendations
from yandexgpt import generate_answers

load_dotenv()

showSidebarNavigation = True


def show_input_form():
    st.write("Введите ваш Cloud ID:")
    cloud_id = st.text_input("Cloud ID")

    if st.button("Сохранить"):
        os.environ['CLOUD_ID'] = cloud_id
        st.success("Cloud ID сохранен. Переход к основной странице...")
        st.rerun()


def recommendation_page(prompt):
    if prompt:
        st.write("Ваш промпт: ", prompt)
        rec = recommendations(prompt)
        st.write("Рекомендации по улучшению промпта:")
        st.write(rec)


def improve_page(prompt):
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
    if selected_page == "Улучшение промпта":
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

    if selected_page == "Рекомендации":
        recommendation_page(prompt)
    elif selected_page == "Улучшение промпта":
        improve_page(prompt)


def sidebar_navigation():
    st.sidebar.title("Навигация")
    selected_page = st.sidebar.selectbox("Выберите страницу:", ["Рекомендации", "Улучшение промпта"])
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
