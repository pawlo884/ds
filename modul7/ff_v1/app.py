import streamlit as st
import pandas as pd  # type: ignore

DATA = "welcome_survey_simple_v1.csv"


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
        "age": age,
        "edu_level": edu_level,
        "fav_animals": fav_animals,
        "fav_place": fav_place,
        "gender": gender,
    }
])

all_df = get_all_participants()

st.write("Wybrane opcje")
st.dataframe(person_df, hide_index=True)

st.write("Przykładowe osoby z bazy")
st.dataframe(all_df.sample(10), hide_index=True)
