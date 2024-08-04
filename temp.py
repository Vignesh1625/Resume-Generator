tab_titles = [f"Project {i+1}" for i in range(num_proj)]
tabs = st.tabs(tab_titles)

for i, tab in enumerate(tabs):
    with tab:
        st.session_state.projects[i]['title'] = st.text_input(f"Project Title {i + 1}", key=f'title_proj_{i}')
        st.session_state.projects[i]['date'] = st.text_input(f"Project Date {i + 1}", key=f'date_proj_{i}')
        st.session_state.projects[i]['summary'] = st.text_area(f"Project Summary {i + 1}", key=f'summary_proj_{i}')
        st.session_state.projects[i]['links'] = st.text_input(f"Project Links {i + 1}", key=f'links_proj_{i}')