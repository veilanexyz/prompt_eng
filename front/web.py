import streamlit as st
import os

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

def main():
    #st.title("Аутентификация по cloud_id")

    if 'CLOUD_ID' in os.environ:
        main_page()
    else:
        show_input_form()

if __name__ == "__main__":
    main()