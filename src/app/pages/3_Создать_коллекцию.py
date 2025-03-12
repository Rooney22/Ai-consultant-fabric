import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.settings import settings



st.set_page_config(page_title="Create collection")

st.title("Создание коллекции")

with st.form("my_form"):

    new_collection_name = st.text_input("Имя коллекции", '')
    description = st.text_area("Описание коллекции", '')
    files = st.file_uploader("Документация", type="pdf", accept_multiple_files=True)

    submitted = st.form_submit_button("Submit")
    if submitted:
        url = f'http://{settings.host}:{settings.port}/collection/create'
        data = {
            "collection_name": new_collection_name,
            "collection_description": description
        }
        new_files = []
        for uploaded_file in files:
            new_files.append(("files", (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")))
        response = requests.post(url=url, data=data, files=new_files)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Ошибка: {response.status_code}")
            st.error(response.json()["detail"])
