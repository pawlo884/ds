import streamlit as st
from audiorecorder import audiorecorder  # type: ignore
from io import BytesIO

st.title("Audio Note v1")

st.set_page_config(page_title="Audio Note v1",
                   page_icon=":microphone:", layout="centered")

note_audio = audiorecorder(
    start_prompt="Nagraj notatkę",
    stop_prompt="Zatrzymaj nagrywanie",)

if note_audio:
    audio = BytesIO()
    note_audio.export(audio, format="mp3")
    note_audio_bytes = audio.getvalue()
    st.audio(note_audio_bytes, format="audio/mp3")
