import streamlit as st
from time import sleep
import pandas as pd


st.title('Refresh cycle app')
country = st.selectbox('Wybierz kraj', ['Polska', 'Niemcy', 'Francja'])

df = pd.read_csv("population_gdp_data.csv")
c0, c1 = st.columns(2)

sleep(3)
with c0:
    if country:
        st.image(f"{country.lower()}_kultura.webp", use_column_width=True)

sleep(3)
country_df = df[df["Kraj"] == country]
with c1:
    st.dataframe(country_df, use_container_width=True, hide_index=True)

what = st.selectbox('Co narysować?', ['PKB', 'Populacja'])

sleep(3)
st.bar_chart(data=country_df, x="Rok", y=what)
