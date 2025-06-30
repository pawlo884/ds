import streamlit as st

st.title('Notatki')

if "notatki" not in st.session_state:
    st.session_state["notatki"] = []

notatka = st.text_area(
    "Wpisz notatkę",
    height=200,
    max_chars=1000,
)

if st.button("Dodaj"):
    st.session_state["notatki"].append(notatka.strip())

st.metric(
    "Masz niezapisane notatki",
    len(st.session_state["notatki"])
)
with st.expander("Zobacz notatki"):
    st.json(st.session_state["notatki"])

if st.button("Wyczyść"):
    st.session_state["notatki"] = []
    st.rerun()

if st.button("Zapisz notatki"):
    with open("notatki.txt", "a") as f:
        notatki_txt = "\n".join(st.session_state["notatki"])
        f.write(f"\n{notatki_txt}")

    st.session_state["notatki"] = []
    st.rerun()
