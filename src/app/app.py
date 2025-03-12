import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.settings import settings

default_chat_name = 'Основной чат'

if 'chats' not in st.session_state:
    st.session_state.chats = {
        default_chat_name: []
    }

if 'current_chat' not in st.session_state:
    st.session_state.current_chat = default_chat_name
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "Test"

if 'show_new_chat_form' not in st.session_state:
    st.session_state.show_new_chat_form = False

def update_current_chat():
    st.session_state.current_chat = st.session_state.selected_chat

with st.sidebar:
    chat_keys = list(st.session_state.chats.keys())
    if st.session_state.current_chat not in chat_keys:
        st.session_state.current_chat = chat_keys[0] if chat_keys else None

    chat = st.selectbox(
        label="Выберите чат",
        options=chat_keys,
        key="selected_chat",
        on_change=update_current_chat
    )

    if st.button("Новый чат"):
        st.session_state.show_new_chat_form = True

    if st.session_state.show_new_chat_form:
        with st.form("new_chat_form"):
            chat_name = st.text_input("Название чата")
            url = f'http://{settings.host}:{settings.port}/agent/get'
            result = requests.get(url=url)
            agents = [agent['agent_name'] for agent in result.json()]
            agent = st.selectbox("Выберите агента", agents)
            if st.form_submit_button("Создать чат"):
                if chat_name in st.session_state.chats:
                    st.error("Чат с таким названием уже существует. Пожалуйста, выберите другое название.")
                else:
                    st.session_state.chats[chat_name] = []
                    st.session_state.current_chat = chat_name
                    st.session_state.selected_agent = agent
                    st.session_state.show_new_chat_form = False
                    st.success(f"Создан новый чат с агентом {agent}")
                    st.rerun()

if st.session_state.current_chat:
    st.write(f"Текущий чат: {st.session_state.current_chat}")
    st.write(f"Агент: {st.session_state.selected_agent}")
    st.write("Сообщения:")

    for message in st.session_state.chats[st.session_state.current_chat]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.chats[st.session_state.current_chat] = []

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        url = f'http://{settings.host}:{settings.port}/agent/answer'
        params = {
            "agent_name": st.session_state.selected_agent,
            "user_question": prompt  
        }
        response = requests.get(url, params=params)

        st.markdown(response.json()['answer'])
    
    st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})
