import streamlit as st


st.title(":parrot: Papuga!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Wpisz co")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state['messages'].append(
        {"role": "user", "content": prompt}
    )

    # wyświetlanie odpowiedzi
    with st.chat_message("assistant"):
        response = f"Powtarzam: {prompt}"
        st.markdown(response)

    st.session_state['messages'].append({"role": "assistant", "content": response})