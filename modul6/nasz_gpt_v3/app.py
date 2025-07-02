import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

env = load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title(":brain: Nasz GPT z pamięcią")


def get_chatbot_response(prompt, memory):
    messages=[
        {
            "role": "system", 
            "content": """
            Bądź jak Jack Sparrow, odpowiadaj na pytania w sposób zwięzły i zrozumiały"""
        },
        
    ]
    
    for message in memory:
        messages.append({"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return {
        "role": "assistant",
        "content": response.choices[0].message.content
    }


if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Wpisz co")
if prompt:
    user_message = {"role": "user", "content": prompt}
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state['messages'].append(
        {"role": "user", "content": prompt}
    )

    # wyświetlanie odpowiedzi
    with st.chat_message("assistant"):
        chatbot_message = get_chatbot_response(prompt, memory=st.session_state["messages"][-10:])
        st.markdown(chatbot_message["content"])

    st.session_state['messages'].append(chatbot_message)

with st.sidebar:
    with st.expander("historia rozmowy"):
        st.json(st.session_state.get("messages") or [])