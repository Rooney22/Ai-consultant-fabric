import streamlit as st

agents = ["Ag1", "Ag2", "Ag3"]

if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt =  {
        'Ag1': 1,
        'Ag2': 2,
        'Ag3': 3
    }

editing_agent = st.selectbox("Редактируемый агент", agents)

if "show_confirmation" not in st.session_state:
    st.session_state.show_confirmation = False

if st.button("Выбрать агента"):
    st.session_state.editing_agent = editing_agent
    st.session_state.show_confirmation = True

if st.session_state.show_confirmation:
    with st.form(f"Изменение агента {st.session_state.editing_agent}"):
        my_prompt = st.session_state.current_prompt[st.session_state.editing_agent]
        prompt = st.text_area("Системный промпт", my_prompt)

        submitted = st.form_submit_button("Изменить промпт")
        
        if submitted:
            st.session_state.current_prompt[st.session_state.editing_agent] = prompt
            st.success("Агент изменён")
