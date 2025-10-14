import streamlit as st
import pandas as pd  # type: ignore
from pycaret.clustering import load_model, predict_model

DATA = "welcome_survey_simple_v1.csv"
MODEL_NAME = "welcome_survey_clustering_pipeline_v1"


def convert_age_to_range(age):
    """Konwertuje wiek na przedział wiekowy używany w modelu"""
    if age < 18:
        return "<18"
    elif age <= 24:
        return "18-24"
    elif age <= 34:
        return "25-34"
    elif age <= 44:
        return "35-44"
    elif age <= 54:
        return "45-54"
    elif age <= 64:
        return "55-64"
    else:
        return "65+"


@st.cache_data
def get_model():
    return load_model(MODEL_NAME)


@st.cache_data
def get_all_participants():
    all_df = pd.read_csv(DATA, sep=";")

    return all_df


with st.sidebar:
    st.header("Powiedz nam coś o sobie")
    st.markdown(
        "Pomożemy Ci znaleźć znajomych, którzy mają podobne zainteresowania i preferencje.")
    age = st.slider("Wiek", min_value=0, max_value=100, value=20)
    edu_level = st.selectbox(
        "Wykształcenie", ["Podstawowe", "Średnie", "Wyższe"])
    fav_animals = st.selectbox("Ulubione zwierzęta", [
                               "Psy", "Koty", "Brak ulubionych"])
    fav_place = st.selectbox("Ulubione miejsce", [
                             "Nad wodą", "W lesie", "W górach", ])
    gender = st.radio("Płeć", ["Mężczyzna", "Kobieta", ])

person_df = pd.DataFrame([
    {
        "age": convert_age_to_range(age),
        "edu_level": edu_level,
        "fav_animals": fav_animals,
        "fav_place": fav_place,
        "gender": gender
    }
])

model = get_model()
all_df = get_all_participants()


predicted_cluster_id = predict_model(model, data=person_df)[
    "Cluster"].values[0]
st.write(f"Przypisano do grupy: {predicted_cluster_id}")
