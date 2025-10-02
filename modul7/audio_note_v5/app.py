import streamlit as st
from audiorecorder import audiorecorder  # type: ignore
from io import BytesIO
from dotenv import dotenv_values
from openai import OpenAI
from hashlib import md5
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct



# zmiene gllobalne

env = dotenv_values("../../.env")

AUDIO_TRANSCRIPTION_MODEL = "whisper-1"

EMBEDDING_MODEL = "text-embedding-3-large"

EMBEDDING_DIM = 1536

QDRANT_COLLECTION_NAME = "notes"

title = "Audio Note v5"

st.title(title)

# koniec zmiennych globalnych

st.set_page_config(page_title=title,
                   page_icon=":microphone:", layout="centered")

# openai_client = get_openai_client()


if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]

    else:
        st.info("Podaj API key OpenAI")
        st.session_state["openai_api_key"] = st.text_input(
            "API key OpenAI", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()
# Session state initialization
if "note_audio_text" not in st.session_state:
    st.session_state["note_audio_bytes_md5"] = None

if "note_audio_bytes" not in st.session_state:
    st.session_state["note_audio_bytes"] = None

if "note_audio_text" not in st.session_state:
    st.session_state["note_audio_text"] = ""


def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])


def transcribe_audio(audio_bytes):
    openai_client = get_openai_client()
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_TRANSCRIPTION_MODEL,
        response_format="verbose_json",
    )
    return transcript.text


if "note_audio_bytes" not in st.session_state:
    st.session_state["note_audio_bytes"] = None

if "note_audio_text" not in st.session_state:
    st.session_state["note_audio_text"] = ""

note_audio = audiorecorder(
    start_prompt="Nagraj notatkę",
    stop_prompt="Zatrzymaj nagrywanie",)

if note_audio:
    audio = BytesIO()
    note_audio.export(audio, format="mp3")
    st.session_state["note_audio_bytes"] = audio.getvalue()
    current_md5 = md5(st.session_state["note_audio_bytes"]).hexdigest()
    if st.session_state["note_audio_bytes_md5"] != current_md5:
        st.session_state["note_audio_text"] = ""
        st.session_state["note_audio_bytes_md5"] = current_md5
        
    st.audio(st.session_state["note_audio_bytes"], format="audio/mp3")

    if st.button("Transkrypcja"):
        st.session_state["note_audio_text"] = transcribe_audio(
            st.session_state["note_audio_bytes"])

    if st.session_state["note_audio_text"]:
        st.text_area(
            "Transkrypcja", value=st.session_state["note_audio_text"], disabled=True, )
