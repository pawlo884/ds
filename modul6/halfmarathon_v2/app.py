import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analiza półmaratonu wrocławskiego 2024")

df = pd.read_csv("halfmarathon_wroclaw_2024__final.csv", sep=";")

with st.sidebar:
    name = st.text_input("Podaj imię zawodnika")
    countries = st.multiselect(
        "Wybierz kraj",
         sorted(df["Kraj"].dropna().unique())
    )
    age_categories = st.multiselect(
        "Wybierz kategorię wieku",
        sorted(df["Kategoria wiekowa"].dropna().unique())
    )
    gender = st.radio(
        "Wybierz płeć",
        ["Wszystkie", "Mężczyźni", "Kobiety"]
    )

if name:
    df = df[df["Imię"].str.contains(name, case=False)]
    
if countries:
    df = df[df["Kraj"].isin(countries)]

if age_categories:
    df = df[df["Kategoria wiekowa"].isin(age_categories)]

if gender == "Mężczyźni":
    df = df[df["Płeć"] == "M"]
    
if gender == "Kobiety":
    df = df[df["Płeć"] == "K"]


c0, c1, c2 = st.columns(3)
with c0:
    st.metric("Liczba zawodników", len(df))

with c1:
    st.metric("Liczba mężczyzn", len(df[df["Płeć"] == "M"]))

with c2:
    st.metric("Liczba kobiet", len(df[df["Płeć"] == "K"]))

st.header("10 losowych wierszy")
sample_size = min(10, len(df))
st.dataframe(df.sample(sample_size), use_container_width=True, hide_index=True)

# top 5

st.header("Top 5 najszybszych zawodników")
top_columns = ['Miejsce', "Numer startowy", "Imię", 'Nazwisko', 'Miasto', 'Kraj', 'Czas']
st.dataframe(df.sort_values(by="Miejsce", ascending=True).head(5)[top_columns], use_container_width=True, hide_index=True)

# barplot krajów

st.header("Pochodzenie zawodników")
gdf = df.groupby('Kraj', as_index=False).count().rename(columns={"Miejsce": "Liczba zawodników"})
st.bar_chart(gdf, x="Kraj", y="Liczba zawodników")

# Histogram czasu na mecie

st.header("Histogram czasu na mecie")
df['Czas'] = pd.to_datetime(df['Czas'], format="%H:%M:%S", errors="coerce")

plt.figure(figsize=(10, 6))
plot = sns.histplot(df['Czas'].apply(lambda x: x.hour * 60 + x.minute + x.second/60), kde=True)

st.pyplot(plot.figure)

# macierz koleracji

st.header("Macierz koleracji")
corr_matrix = df.corr(numeric_only=True)
plt.figure(figsize=(16, 12))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
st.pyplot(plt.gcf())