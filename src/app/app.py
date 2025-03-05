import streamlit as st
import random
import time

if 'chats' not in st.session_state:
    st.session_state.chats = {'chat1': [], 'chat2': [], 'chat3': []}

if 'current_chat' not in st.session_state:
    st.session_state.current_chat = 'chat1'

if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = ''

if 'show_new_chat_form' not in st.session_state:
    st.session_state.show_new_chat_form = False

def update_current_chat():
    st.session_state.current_chat = st.session_state.selected_chat

with st.sidebar:
    st.write("Чат")

    chat = st.selectbox(
        label="Выберите чат",
        options=list(st.session_state.chats.keys()),
        index=list(st.session_state.chats.keys()).index(st.session_state.current_chat),
        key="selected_chat",
        on_change=update_current_chat
    )

    if st.button("Новый чат"):
        st.session_state.show_new_chat_form = True

    if st.session_state.show_new_chat_form:
        with st.form("new_chat_form"):
            agent = st.selectbox("Выберите агента", ["Agent1", "Agent2", "Agent3"])
            if st.form_submit_button("Создать чат"):
                new_chat_name = f"chat{len(st.session_state.chats) + 1}"
                st.session_state.chats[new_chat_name] = []
                st.session_state.current_chat = new_chat_name
                st.session_state.selected_agent = agent
                st.session_state.show_new_chat_form = False
                st.success(f"Создан новый чат с агентом {agent}")
                st.rerun()

if st.session_state.current_chat:
    st.write(f"Текущий чат: {st.session_state.current_chat}")
    st.write(f"Агент: {st.session_state.selected_agent}")
    st.write("Сообщения:")
    for message in st.session_state.chats[st.session_state.current_chat]:
        st.write(message)

if prompt := st.chat_input("Введите сообщение"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})

    def response_generator():
        response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        for word in response.split():
            yield word + " "
            time.sleep(0.08)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())

    st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})
