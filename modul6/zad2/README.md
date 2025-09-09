# 📊 Dashboard Ankiety - Streamlit

Aplikacja do wizualizacji i analizy danych z ankiety zbudowana w Streamlit.

## 🚀 Funkcjonalności

### 📈 Wizualizacje

- **Wykresy demograficzne**: rozkład wieku, płci, wykształcenia
- **Analiza hobby**: popularność różnych zainteresowań
- **Preferencje uczenia**: radar preferencji metod uczenia
- **Analiza motywacji**: czynniki motywujące respondentów
- **Analiza branż**: rozkład branż zawodowych
- **Mapa korelacji**: korelacje między zmiennymi numerycznymi

### 🔍 Interaktywne Funkcje

- **Upload plików**: możliwość załadowania własnego pliku CSV
- **Filtry**: filtrowanie po wieku, branży, płci
- **Automatyczne insights**: kluczowe wnioski z danych
- **Statystyki**: podsumowanie statystyczne

### 🎨 Design

- **Responsywny layout**: dostosowany do różnych rozmiarów ekranu
- **Kolorowe wykresy**: różne palety kolorów dla lepszej czytelności
- **Interaktywne wykresy**: możliwość zoom, hover, kliknięcia

## 📋 Wymagania

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy
- Seaborn
- Matplotlib

## 🛠️ Instalacja i Uruchomienie

### Opcja 1: Automatyczne uruchomienie (Zalecane)

**Windows:**

```cmd
run_app.bat
```

**Linux/Mac:**

```bash
chmod +x run_app.sh
./run_app.sh
```

### Opcja 2: Ręczne uruchomienie

1. Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```

2. Uruchom aplikację:

```bash
streamlit run app.py
```

3. Otwórz przeglądarkę i przejdź do: `http://localhost:8501`

### Opcja 3: Użycie Python skryptu

```bash
python run_app.py
```

## 📁 Format Danych

Aplikacja obsługuje pliki CSV z następującą strukturą:

### Wymagane kolumny:

- `age` - grupa wiekowa
- `edu_level` - poziom wykształcenia
- `gender` - płeć (0.0 = mężczyzna, 1.0 = kobieta)
- `industry` - branża
- `years_of_experience` - lata doświadczenia

### Opcjonalne kolumny:

- `hobby_*` - hobby (wartości 0/1)
- `learning_pref_*` - preferencje uczenia (wartości 0/1)
- `motivation_*` - motywacje (wartości 0/1)
- `fav_animals` - ulubione zwierzęta
- `fav_place` - ulubione miejsce
- `sweet_or_salty` - preferencje smakowe

### Przykład danych:

```csv
age;edu_level;gender;industry;hobby_books;hobby_sport;learning_pref_online_courses;motivation_career
25-34;Wyższe;0.0;IT;1;0;1;1
35-44;Średnie;1.0;Edukacja;0;1;1;0
```

### Pliki przykładowe:

- `sample_data.csv` - przykładowe dane do testowania
- `35__welcome_survey_cleaned.csv` - pełne dane z ankiety

## 🎯 Użycie

1. **Załaduj dane**: Użyj sidebar do załadowania pliku CSV
2. **Zastosuj filtry**: Wybierz interesujące Cię grupy respondentów
3. **Przeglądaj wykresy**: Analizuj różne aspekty danych
4. **Czytaj insights**: Sprawdź automatycznie wygenerowane wnioski
5. **Eksploruj korelacje**: Sprawdź zależności między zmiennymi

## 📊 Typy Wykresów

- **Wykresy kołowe**: rozkłady kategoryczne
- **Wykresy słupkowe**: porównania wartości
- **Wykresy radarowe**: wielowymiarowe porównania
- **Mapy cieplne**: korelacje i zależności
- **Wykresy horyzontalne**: długie listy kategorii

## 🔧 Dostosowywanie

Aplikacja jest łatwa do dostosowania:

1. **Dodaj nowe wykresy**: Rozszerz funkcje w `app.py`
2. **Zmień kolory**: Modyfikuj palety kolorów w Plotly
3. **Dodaj filtry**: Rozszerz sekcję filtrów w sidebar
4. **Dostosuj insights**: Zmodyfikuj logikę generowania wniosków

## 📝 Licencja

Projekt edukacyjny - do użytku osobistego i naukowego.

## 🤝 Wsparcie

W przypadku problemów sprawdź:

1. Format pliku CSV
2. Kodowanie pliku (UTF-8)
3. Separatory (średnik, przecinek)
4. Zainstalowane pakiety
