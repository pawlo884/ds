import streamlit as st
import pandas as pd  # type: ignore
from pycaret.clustering import load_model, predict_model
import plotly.express as px  # type: ignore
import json
import os

DATA = "welcome_survey_simple_v1.csv"
MODEL_NAME = "welcome_survey_clustering_pipeline_v1.pkl"
CLUSTER_NAMES_AND_DESCRIPTIONS = "welcome_survey_cluster_names_and_descriptions_v1.json"


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
    # Użyj pełnej ścieżki do pliku modelu
    model_path = os.path.join(os.path.dirname(__file__), MODEL_NAME)
    return load_model(model_path)


@st.cache_data
def get_cluster_names_and_descriptions():
    # Użyj pełnej ścieżki do pliku JSON
    json_path = os.path.join(os.path.dirname(
        __file__), CLUSTER_NAMES_AND_DESCRIPTIONS)
    return json.load(open(json_path, encoding='utf-8'))


@st.cache_data
def get_all_participants():
    model = get_model()
    # Użyj pełnej ścieżki do pliku CSV
    csv_path = os.path.join(os.path.dirname(__file__), DATA)
    all_df = pd.read_csv(csv_path, sep=";")
    df_with_cluster = predict_model(model, data=all_df)

    return df_with_cluster


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
cluster_names_and_descriptions = get_cluster_names_and_descriptions()

predicted_cluster_id = predict_model(model, data=person_df)[
    "Cluster"].values[0]
predicted_cluster_data = cluster_names_and_descriptions[predicted_cluster_id]


st.header(f"Przypisano do klastra: {predicted_cluster_data['name']}")
st.markdown(predicted_cluster_data['description'])
same_cluster_df = all_df[all_df["Cluster"] == predicted_cluster_id]
st.metric("Liczba osób w klastrze", len(same_cluster_df))

st.header("Osoby z grupy")
fig = px.histogram(same_cluster_df.sort_values("age"), x="age")
fig.update_layout(
    title="Rozkład wieku w grupie",
    xaxis_title="Wiek",
    yaxis_title="Liczba osób",
)
st.plotly_chart(fig)

fig = px.histogram(same_cluster_df, x="edu_level")
fig.update_layout(
    title="Rozkład wykształcenia w grupie",
    xaxis_title="Wykształcenie",
    yaxis_title="Liczba osób",
)
st.plotly_chart(fig)

fig = px.histogram(same_cluster_df, x="fav_animals")
fig.update_layout(
    title="Rozkład ulubionych zwierząt w grupie",
    xaxis_title="Ulubione zwierzęta",
    yaxis_title="Liczba osób",
)
st.plotly_chart(fig)

fig = px.histogram(same_cluster_df, x="fav_place")
fig.update_layout(
    title="Rozkład ulubionych miejsc w grupie",
    xaxis_title="Ulubione miejsce",
    yaxis_title="Liczba osób",
)
st.plotly_chart(fig)

fig = px.histogram(same_cluster_df, x="gender")
fig.update_layout(
    title="Rozkład płci w grupie",
    xaxis_title="Płeć",
    yaxis_title="Liczba osób",
)
st.plotly_chart(fig)
