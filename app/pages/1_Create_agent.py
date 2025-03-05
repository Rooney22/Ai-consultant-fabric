import streamlit as st

st.set_page_config(page_title="Create agent")

if 'new_agent_name' not in st.session_state:
    st.session_state.new_agent_name = ''

if 'file' not in st.session_state:
    st.session_state.file = ''

if 'prompt' not in st.session_state:
    st.session_state.prompt = ''

st.title("Создание агента")

with st.form("my_form"):

    new_agent_name = st.text_input("Имя агента", st.session_state.new_agent_name)
    prompt = st.text_area("Системный промпт", '')
    file = st.file_uploader("Документация", type="pdf")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Agent name '{new_agent_name}' returned!")
        st.session_state.new_agent_name = new_agent_name
        st.session_state.file = file
        st.session_state.prompt = prompt
        print(new_agent_name)
