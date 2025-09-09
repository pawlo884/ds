import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Konfiguracja strony
st.set_page_config(
    page_title="Analiza Ankiety - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def load_data(uploaded_file):
    """Ładuje dane z pliku CSV"""
    try:
        # Próba odczytu z różnymi separatorami
        for sep in [';', ',', '\t']:
            try:
                df = pd.read_csv(uploaded_file, sep=sep, encoding='utf-8')
                if len(df.columns) > 1:
                    break
            except Exception:
                continue

        # Czyszczenie danych
        df = df.dropna(how='all')  # Usuń puste wiersze
        return df
    except Exception as e:
        st.error(f"Błąd podczas ładowania danych: {e}")
        return None


def clean_data(df):
    """Czyści i przygotowuje dane do analizy"""
    # Zamień puste wartości na 'Nieznane'
    df = df.fillna('Nieznane')

    # Zamień 'unknown' na 'Nieznane'
    df = df.replace('unknown', 'Nieznane')

    # Zamień puste stringi na 'Nieznane'
    df = df.replace('', 'Nieznane')

    return df


def create_demographic_charts(df):
    """Tworzy wykresy demograficzne"""
    st.subheader("📈 Analiza Demograficzna")

    col1, col2 = st.columns(2)

    with col1:
        # Wykres wieku
        age_counts = df['age'].value_counts()
        fig_age = px.pie(
            values=age_counts.values,
            names=age_counts.index,
            title="Rozkład Wiekowy",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_age.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_age, use_container_width=True)

        # Wykres płci
        if 'gender' in df.columns:
            gender_counts = df['gender'].value_counts()
            gender_labels = {1.0: 'Kobieta', 0.0: 'Mężczyzna'}
            gender_counts.index = gender_counts.index.map(
                gender_labels).fillna('Nieznane')

            fig_gender = px.bar(
                x=gender_counts.index,
                y=gender_counts.values,
                title="Rozkład Płci",
                color=gender_counts.values,
                color_continuous_scale='Blues'
            )
            fig_gender.update_layout(showlegend=False)
            st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        # Wykres wykształcenia
        edu_counts = df['edu_level'].value_counts()
        fig_edu = px.bar(
            x=edu_counts.values,
            y=edu_counts.index,
            orientation='h',
            title="Poziom Wykształcenia",
            color=edu_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_edu.update_layout(showlegend=False)
        st.plotly_chart(fig_edu, use_container_width=True)

        # Wykres doświadczenia
        exp_counts = df['years_of_experience'].value_counts()
        fig_exp = px.bar(
            x=exp_counts.index,
            y=exp_counts.values,
            title="Lata Doświadczenia",
            color=exp_counts.values,
            color_continuous_scale='Plasma'
        )
        fig_exp.update_layout(showlegend=False)
        st.plotly_chart(fig_exp, use_container_width=True)


def create_hobby_analysis(df):
    """Analizuje hobby respondentów"""
    st.subheader("🎨 Analiza Hobby i Zainteresowań")

    # Przygotuj dane hobby
    hobby_cols = [col for col in df.columns if col.startswith('hobby_')]
    hobby_data = []

    for col in hobby_cols:
        hobby_name = col.replace('hobby_', '').replace('_', ' ').title()
        count = df[col].sum() if df[col].dtype in [
            'int64', 'float64'] else (df[col] == 1).sum()
        hobby_data.append({'Hobby': hobby_name, 'Liczba': count})

    hobby_df = pd.DataFrame(hobby_data).sort_values('Liczba', ascending=True)

    col1, col2 = st.columns(2)

    with col1:
        # Wykres słupkowy hobby
        fig_hobby = px.bar(
            hobby_df,
            x='Liczba',
            y='Hobby',
            orientation='h',
            title="Popularność Hobby",
            color='Liczba',
            color_continuous_scale='RdYlBu'
        )
        st.plotly_chart(fig_hobby, use_container_width=True)

    with col2:
        # Wykres kołowy hobby
        fig_hobby_pie = px.pie(
            hobby_df,
            values='Liczba',
            names='Hobby',
            title="Rozkład Hobby",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_hobby_pie, use_container_width=True)


def create_learning_preferences(df):
    """Analizuje preferencje uczenia się"""
    st.subheader("📚 Preferencje Uczenia Się")

    # Przygotuj dane preferencji uczenia
    learning_cols = [
        col for col in df.columns if col.startswith('learning_pref_')]
    learning_data = []

    for col in learning_cols:
        learning_name = col.replace(
            'learning_pref_', '').replace('_', ' ').title()
        count = df[col].sum() if df[col].dtype in [
            'int64', 'float64'] else (df[col] == 1).sum()
        learning_data.append({'Metoda': learning_name, 'Liczba': count})

    learning_df = pd.DataFrame(learning_data).sort_values(
        'Liczba', ascending=False)

    # Wykres radarowy preferencji uczenia
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=learning_df['Liczba'],
        theta=learning_df['Metoda'],
        fill='toself',
        name='Preferencje Uczenia',
        line_color='rgb(32, 201, 151)'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, learning_df['Liczba'].max()]
            )),
        showlegend=True,
        title="Radar Preferencji Uczenia"
    )

    st.plotly_chart(fig_radar, use_container_width=True)


def create_motivation_analysis(df):
    """Analizuje motywacje respondentów"""
    st.subheader("💪 Analiza Motywacji")

    # Przygotuj dane motywacji
    motivation_cols = [
        col for col in df.columns if col.startswith('motivation_')]
    motivation_data = []

    for col in motivation_cols:
        motivation_name = col.replace(
            'motivation_', '').replace('_', ' ').title()
        count = df[col].sum() if df[col].dtype in [
            'int64', 'float64'] else (df[col] == 1).sum()
        motivation_data.append({'Motywacja': motivation_name, 'Liczba': count})

    motivation_df = pd.DataFrame(
        motivation_data).sort_values('Liczba', ascending=True)

    # Wykres słupkowy motywacji
    fig_motivation = px.bar(
        motivation_df,
        x='Liczba',
        y='Motywacja',
        orientation='h',
        title="Czynniki Motywujące",
        color='Liczba',
        color_continuous_scale='Sunset'
    )
    st.plotly_chart(fig_motivation, use_container_width=True)


def create_industry_analysis(df):
    """Analizuje branże respondentów"""
    st.subheader("🏢 Analiza Branż")

    # Przygotuj dane branż
    industry_counts = df['industry'].value_counts().head(15)  # Top 15 branż

    col1, col2 = st.columns(2)

    with col1:
        # Wykres słupkowy branż
        fig_industry = px.bar(
            x=industry_counts.values,
            y=industry_counts.index,
            orientation='h',
            title="Top 15 Branż",
            color=industry_counts.values,
            color_continuous_scale='Turbo'
        )
        fig_industry.update_layout(showlegend=False)
        st.plotly_chart(fig_industry, use_container_width=True)

    with col2:
        # Wykres kołowy branż
        fig_industry_pie = px.pie(
            values=industry_counts.values,
            names=industry_counts.index,
            title="Rozkład Branż (Top 15)",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_industry_pie, use_container_width=True)


def create_correlation_heatmap(df):
    """Tworzy mapę cieplną korelacji"""
    st.subheader("🔥 Mapa Korelacji")

    # Wybierz tylko kolumny numeryczne
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()

    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        title="Korelacje między Zmiennymi Numerycznymi",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


def create_insights(df):
    """Generuje automatyczne insights"""
    st.subheader("💡 Kluczowe Insights")

    insights = []

    # Insight 1: Najpopularniejsze hobby
    hobby_cols = [col for col in df.columns if col.startswith('hobby_')]
    hobby_totals = {}
    for col in hobby_cols:
        hobby_name = col.replace('hobby_', '').replace('_', ' ').title()
        count = df[col].sum() if df[col].dtype in [
            'int64', 'float64'] else (df[col] == 1).sum()
        hobby_totals[hobby_name] = count

    if hobby_totals:
        top_hobby = max(hobby_totals.keys(), key=lambda x: hobby_totals[x])
        insights.append(
            f"🎯 **Najpopularniejsze hobby**: {top_hobby} ({hobby_totals[top_hobby]} osób)")

    # Insight 2: Dominująca grupa wiekowa
    top_age = df['age'].value_counts().index[0]
    age_count = df['age'].value_counts().iloc[0]
    insights.append(
        f"👥 **Dominująca grupa wiekowa**: {top_age} ({age_count} osób)")

    # Insight 3: Najczęstsza branża
    top_industry = df['industry'].value_counts().index[0]
    industry_count = df['industry'].value_counts().iloc[0]
    insights.append(
        f"🏢 **Najczęstsza branża**: {top_industry} ({industry_count} osób)")

    # Insight 4: Preferencje uczenia
    learning_cols = [
        col for col in df.columns if col.startswith('learning_pref_')]
    learning_totals = {}
    for col in learning_cols:
        learning_name = col.replace(
            'learning_pref_', '').replace('_', ' ').title()
        count = df[col].sum() if df[col].dtype in [
            'int64', 'float64'] else (df[col] == 1).sum()
        learning_totals[learning_name] = count

    if learning_totals:
        top_learning = max(learning_totals.keys(),
                           key=lambda x: learning_totals[x])
        insights.append(
            f"📚 **Najpopularniejsza metoda uczenia**: {top_learning} ({learning_totals[top_learning]} osób)")

    # Insight 5: Rozkład płci
    if 'gender' in df.columns:
        gender_counts = df['gender'].value_counts()
        total_responses = len(df)
        if 1.0 in gender_counts.index:
            women_pct = (gender_counts[1.0] / total_responses) * 100
            insights.append(f"👩 **Procent kobiet**: {women_pct:.1f}%")

    # Wyświetl insights
    for insight in insights:
        st.markdown(
            f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


def create_statistics_summary(df):
    """Tworzy podsumowanie statystyczne"""
    st.subheader("📊 Podsumowanie Statystyczne")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Liczba respondentów", len(df))

    with col2:
        st.metric("Liczba pytań", len(df.columns))

    with col3:
        if 'age' in df.columns:
            unique_ages = df['age'].nunique()
            st.metric("Grupy wiekowe", unique_ages)

    with col4:
        if 'industry' in df.columns:
            unique_industries = df['industry'].nunique()
            st.metric("Branże", unique_industries)


def main():
    # Nagłówek
    st.markdown('<h1 class="main-header">📊 Dashboard Ankiety</h1>',
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("⚙️ Ustawienia")

    # Upload pliku
    uploaded_file = st.sidebar.file_uploader(
        "📁 Wybierz plik CSV z danymi ankiety",
        type=['csv'],
        help="Załaduj plik CSV z danymi ankiety"
    )

    if uploaded_file is not None:
        # Ładowanie danych
        df = load_data(uploaded_file)

        if df is not None:
            # Czyszczenie danych
            df = clean_data(df)

            # Filtry w sidebar
            st.sidebar.subheader("🔍 Filtry")

            # Filtr wieku
            if 'age' in df.columns:
                age_options = ['Wszystkie'] + df['age'].unique().tolist()
                selected_age = st.sidebar.selectbox(
                    "Grupa wiekowa", age_options)
                if selected_age != 'Wszystkie':
                    df = df[df['age'] == selected_age]

            # Filtr branży
            if 'industry' in df.columns:
                industry_options = ['Wszystkie'] + \
                    df['industry'].unique().tolist()
                selected_industry = st.sidebar.selectbox(
                    "Branża", industry_options)
                if selected_industry != 'Wszystkie':
                    df = df[df['industry'] == selected_industry]

            # Filtr płci
            if 'gender' in df.columns:
                gender_options = ['Wszystkie', 'Kobieta', 'Mężczyzna']
                selected_gender = st.sidebar.selectbox("Płeć", gender_options)
                if selected_gender == 'Kobieta':
                    df = df[df['gender'] == 1.0]
                elif selected_gender == 'Mężczyzna':
                    df = df[df['gender'] == 0.0]

            # Informacje o danych
            st.sidebar.subheader("ℹ️ Informacje")
            st.sidebar.info(f"Załadowano: {len(df)} rekordów")
            st.sidebar.info(f"Kolumny: {len(df.columns)}")

            # Główna zawartość
            if len(df) > 0:
                # Podsumowanie statystyczne
                create_statistics_summary(df)

                # Insights
                create_insights(df)

                # Wykresy demograficzne
                create_demographic_charts(df)

                # Analiza hobby
                create_hobby_analysis(df)

                # Preferencje uczenia
                create_learning_preferences(df)

                # Analiza motywacji
                create_motivation_analysis(df)

                # Analiza branż
                create_industry_analysis(df)

                # Mapa korelacji
                create_correlation_heatmap(df)

                # Tabela danych
                st.subheader("📋 Pełne Dane")
                st.dataframe(df, use_container_width=True)

            else:
                st.warning("Brak danych spełniających wybrane kryteria.")

    else:
        # Instrukcje gdy nie ma pliku
        st.info("👆 Załaduj plik CSV z danymi ankiety, aby rozpocząć analizę")

        # Przykładowe dane
        st.subheader("📝 Przykładowa struktura danych")
        st.code("""
        age;edu_level;fav_animals;fav_place;gender;hobby_art;hobby_books;hobby_movies;industry;learning_pref_books;learning_pref_online_courses;motivation_career;motivation_money_and_job;years_of_experience
        25-34;Wyższe;Psy;Nad wodą;0.0;0;0;1;IT;1;1;0;0;6-10
        35-44;Średnie;Koty;W górach;1.0;1;1;0;Edukacja;0;1;1;1;11-15
        """)


if __name__ == "__main__":
    main()
