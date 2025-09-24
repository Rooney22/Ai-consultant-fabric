import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.settings import settings

def get_info(agent_name: str, json: list[dict]) -> int:
    i = 0
    while json[i]['agent_name'] != agent_name:
        i += 1
    return (json[i]['agent_id'], json[i]['agent_prompt'])


url = f'http://{settings.host}:{settings.port}/agent/get'
result = requests.get(url=url)
agents = [agent['agent_name'] for agent in result.json()]
editing_agent = st.selectbox("Редактируемый агент", agents)

if "show_confirmation" not in st.session_state:
    st.session_state.show_confirmation = False

if st.button("Выбрать агента"):
    st.session_state.editing_agent = editing_agent
    st.session_state.show_confirmation = True

if st.session_state.show_confirmation:
    with st.form(f"Изменение агента {st.session_state.editing_agent}"):
        agent_id, agent_prompt = get_info(st.session_state.editing_agent, result.json())
        prompt = st.text_area("Системный промпт", agent_prompt)

        submitted = st.form_submit_button("Изменить промпт")
        
        if submitted:
            url = f'http://{settings.host}:{settings.port}/agent/update_prompt'
            params = {
                "agent_id": agent_id, 
                "new_prompt": prompt 
            }
            response = requests.put(url, params=params)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Ошибка: {response.status_code}")
                st.error(response.json()["detail"])
