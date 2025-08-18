import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

model_pricing = {
    "gpt-4o": {
        "input_tokens": 5.00 / 1_000_000,  # per token
        "output_tokens": 15.00 / 1_000_000,  # per token
    },
    "gpt-4o-mini": {
        "input_tokens": 0.150 / 1_000_000,  # per token
        "output_tokens": 0.600 / 1_000_000,  # per token
    }
}

MODEL = "gpt-4o"
USD_TO_PLN = 4.50
PRICING = model_pricing[MODEL]

env = load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title(":floppy_disk: Nasz GPT z pamięcią")


def get_chatbot_response(prompt, memory):
    messages = [
        {
            "role": "system",
            "content": st.session_state["chatbot_personality"],
        },

    ]
    # dodaj wszystkie poprzednie wiadomości do historii
    for message in memory:
        messages.append(
            {"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    usage = {}
    if response.usage:
        usage = {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "usage": usage,
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
        chatbot_message = get_chatbot_response(
            prompt, memory=st.session_state["messages"][-10:])
        st.markdown(chatbot_message["content"])

    st.session_state['messages'].append(chatbot_message)

    with open("current_conversation.json", "w") as f:
        f.write(json.dumps({
            "chatbot_personality": st.session_state["chatbot_personality"],
            "messages": st.session_state["messages"],
        }))

with st.sidebar:
    total_cost = 0
    for message in st.session_state["messages"]:
        if "usage" in message:
            total_cost += message["usage"]["prompt_tokens"] * \
                PRICING["input_tokens"]
            total_cost += message["usage"]["completion_tokens"] * \
                PRICING["output_tokens"]

    c0, c1 = st.columns(2)
    with c0:
        st.metric("Koszt rozmowy (USD)", f"{total_cost:.4f}")

    with c1:
        st.metric("Koszt rozmowy (PLN)", f"{total_cost * USD_TO_PLN:.4f}")

    st.session_state["chatbot_personality"] = st.text_area(
        "Opisz osobowość chatbota",
        max_chars=1000,
        height=200,
        value="""
Jesteś pomocnikiem, który odpowiada na wszystkie pytania użytkownika.
Odpowiadaj na pytania w sposób zwięzły i zrozumiały.
    """.strip()
    )
