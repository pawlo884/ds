import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path


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

# CONVERSATION HISTORY AND DATABASE


DEFAULT_PERSONALITY = """
Jesteś pomocnikiem, który odpowiada na wszystkie pytania użytkownika. Odpowiadaj an pytania w sposób zwięzły i zrozumiały.
""".strip()

DB_PATH = Path("db")
DB_CONVERSATIONS_PATH = DB_PATH / "conversations"


def load_conversation_to_state(conversation):
    st.session_state["id"] = conversation["id"]
    st.session_state["name"] = conversation["name"]
    st.session_state["messages"] = conversation["messages"]
    st.session_state["chatbot_personality"] = conversation["chatbot_personality"]


def load_current_conversation():
    if not DB_PATH.exists():
        DB_PATH.mkdir()
        DB_CONVERSATIONS_PATH.mkdir()
        conversation_id = 1
        conversation = {
            "id": conversation_id,
            "name": "Konwersacja 1",
            "chatbot_personality": DEFAULT_PERSONALITY,
            "messages": [],
        }

        # tworzymy nową konwersację
        with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "w") as f:
            f.write(json.dumps(conversation))

        # która od razu staje się aktualną
        with open(DB_PATH / "current.json", "w") as f:
            f.write(json.dumps({
                "current_conversation_id": conversation_id,
            }))

        # ładujemy konwersację do session_state
        load_conversation_to_state(conversation)

    else:
        # sprawdzamy, która konwersacja jest aktualna
        with open(DB_PATH / "current.json", "r") as f:
            data = json.loads(f.read())
            conversation_id = data["current_conversation_id"]

        # wczytujemy konwersację
        with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "r") as f:
            conversation = json.loads(f.read())

        load_conversation_to_state(conversation)


def save_current_conversation_messages():
    conversation_id = st.session_state["id"]
    new_messages = st.session_state["messages"]

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "r") as f:
        conversation = json.loads(f.read())

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "w") as f:
        f.write(json.dumps({
            **conversation,
            "messages": new_messages,
        }))


def save_current_conversation_name():
    conversation_id = st.session_state["id"]
    new_conversation_name = st.session_state["new_conversation_name"]

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "r") as f:
        conversation = json.loads(f.read())

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "w") as f:
        f.write(json.dumps({
            **conversation,
            "name": new_conversation_name,
        }))


def save_current_conversation_personality():
    conversation_id = st.session_state["id"]
    new_chatbot_personality = st.session_state["new_chatbot_personality"]

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "r") as f:
        conversation = json.loads(f.read())

    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "w") as f:
        f.write(json.dumps({
            **conversation,
            "chatbot_personality": new_chatbot_personality,
        }))


def create_new_conversation():
    # poszukajmy ID dla naszej kolejnej konwersacji
    conversation_ids = []
    for p in DB_CONVERSATIONS_PATH.glob("*.json"):
        conversation_ids.append(int(p.stem))

    # conversation_ids zawiera wszystkie ID konwersacji
    # następna konwersację będzie miała ID o 1 większe niż największe ID z listy
    conversation_id = max(conversation_ids) + 1
    personality = DEFAULT_PERSONALITY
    if "chatbot_personality" in st.session_state and st.session_state["chatbot_personality"]:
        personality = st.session_state["chatbot_personality"]

    conversation = {
        "id": conversation_id,
        "name": f"Konwersacja {conversation_id}",
        "chatbot_personality": personality,
        "messages": [],
    }

    # tworzymy nową konwersację
    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "w") as f:
        f.write(json.dumps(conversation))

    # która od razu staje się aktualną
    with open(DB_PATH / "current.json", "w") as f:
        f.write(json.dumps({
            "current_conversation_id": conversation_id,
        }))

    load_conversation_to_state(conversation)
    st.rerun()


def switch_conversation(conversation_id):
    with open(DB_CONVERSATIONS_PATH / f"{conversation_id}.json", "r") as f:
        conversation = json.loads(f.read())

    with open(DB_PATH / "current.json", "w") as f:
        f.write(json.dumps({
            "current_conversation_id": conversation_id,
        }))

    load_conversation_to_state(conversation)
    st.rerun()


def list_conversations():
    conversations = []
    for p in DB_CONVERSATIONS_PATH.glob("*.json"):
        with open(p, "r") as f:
            conversation = json.loads(f.read())
            conversations.append({
                "id": conversation["id"],
                "name": conversation["name"],
            })

    return conversations

# MAIN PROGRAM


load_current_conversation()

st.title(":classical_building: Nasz GPT")


for message in st.session_state.get('messages', []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Wpisz co chcesz spytać?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    st.session_state['messages'].append(
        {"role": "user", "content": prompt}
    )

    # wyświetlanie odpowiedzi
    with st.chat_message("assistant"):
        chatbot_message = get_chatbot_response(
            prompt, memory=st.session_state.get("messages", [])[-20:])
        st.markdown(chatbot_message["content"])

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    st.session_state['messages'].append(
        {"role": "assistant", "content": chatbot_message["content"], "usage": chatbot_message["usage"]})
    save_current_conversation_messages()


with st.sidebar:
    st.subheader("Aktualna konwersacja")
    total_cost = 0
    for message in st.session_state["messages"] or []:
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

    st.session_state["name"] = st.text_input(
        "Nazwa konwersacji",
        value=st.session_state.get("name", "Konwersacja 1"),
        key="new_conversation_name",
        on_change=save_current_conversation_name,
    )

    st.session_state["chatbot_personality"] = st.text_area(
        "Opisz osobowość chatbota",
        max_chars=1000,
        height=200,
        value=st.session_state.get("chatbot_personality", DEFAULT_PERSONALITY),
        key="new_chatbot_personality",
        on_change=save_current_conversation_personality,
    )

    st.subheader("Konwersacje")
    if st.button("Nowa konwersacja"):
        create_new_conversation()

    # pokazujemy tylko top 5 konwersacji
    conversations = list_conversations()
    sorted_conversations = sorted(
        conversations, key=lambda x: x["id"], reverse=True)
    for conversation in sorted_conversations[:5]:
        c0, c1 = st.columns([10, 3])
        with c0:
            st.write(conversation["name"])

        with c1:
            if st.button("załaduj", key=conversation["id"], disabled=conversation["id"] == st.session_state.get("id", 0)):
                switch_conversation(conversation["id"])
