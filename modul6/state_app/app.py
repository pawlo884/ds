import streamlit as st
import time

st.title("Notatki")

if 'notatki' not in st.session_state:
    st.session_state['notatki'] = []

notatka = st.text_area("Wpisz notatkę", height=100, max_chars=100)

if st.button("Dodaj"):
    st.session_state['notatki'].append(notatka.strip())

with st.expander("Notatki"):
    st.json(st.session_state['notatki'])


if st.button("Zapisz notatki"):
    with open('notatki.txt', "a") as f:
        notatki_txt = '\n'.join(st.session_state['notatki'])
        f.write(f"\n{notatki_txt}")

    st.session_state['notatki'] = []
    st.success("Notatki zostały zapisane")
    time.sleep(2)
    st.rerun()








