import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.settings import settings

st.set_page_config(page_title="Create agent")

if 'new_agent_name' not in st.session_state:
    st.session_state.new_agent_name = ''

if 'file' not in st.session_state:
    st.session_state.file = ''

if 'prompt' not in st.session_state:
    st.session_state.prompt = ''

if 'current_collection' not in st.session_state:
    st.session_state.current_collection = ''

def update_current_collection():
    st.session_state.current_collection = st.session_state.current_collection

st.title("Создание агента")

with st.form("my_form"):

    url = f'http://{settings.host}:{settings.port}/collection/get'
    result = requests.get(url=url)
    collection_names = [collection['collection_name'] for collection in result.json()]
    new_agent_name = st.text_input("Имя агента", st.session_state.new_agent_name)
    prompt = st.text_area("Системный промпт", '')

    collection = st.selectbox(
        label="Выберите коллекцию",
        options=collection_names
    )

    submitted = st.form_submit_button("Submit")
    if submitted:
        url = f'http://{settings.host}:{settings.port}/agent/create'
        payload={
            'agent_name' : new_agent_name,
            'agent_prompt': prompt,
            'collection_name': collection
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Ошибка: {response.status_code}")
            st.error(response.json()["detail"])
