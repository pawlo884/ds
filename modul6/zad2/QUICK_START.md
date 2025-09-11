# 🚀 Szybki Start - Dashboard Ankiety

## ⚡ Uruchomienie w 3 krokach

### 1. Pobierz i zainstaluj Python

- Pobierz Python z [python.org](https://python.org)
- Podczas instalacji zaznacz "Add Python to PATH"

### 2. Uruchom aplikację

**Windows:**

```cmd
run_app.bat
```

**Linux/Mac:**

```bash
./run_app.sh
```

### 3. Otwórz przeglądarkę

- Przejdź do: `http://localhost:8501`
- Załaduj plik `sample_data.csv` lub `35__welcome_survey_cleaned.csv`

## 🎯 Co zobaczysz

### 📊 Wykresy

- **Demograficzne**: wiek, płeć, wykształcenie
- **Hobby**: popularność zainteresowań
- **Uczenie**: preferencje metod nauki
- **Motywacje**: czynniki motywujące
- **Branże**: rozkład zawodów

### 🔍 Funkcje

- **Filtry**: wiek, branża, płeć
- **Insights**: automatyczne wnioski
- **Interaktywne wykresy**: zoom, hover
- **Responsywny design**: działa na telefonie

## 🛠️ Rozwiązywanie problemów

### Błąd: "Python nie jest rozpoznawany"

- Zainstaluj Python z [python.org](https://python.org)
- Zaznacz "Add Python to PATH" podczas instalacji

### Błąd: "Nie można zainstalować pakietów"

- Sprawdź połączenie internetowe
- Uruchom jako administrator (Windows)

### Aplikacja nie uruchamia się

- Sprawdź czy port 8501 jest wolny
- Spróbuj: `streamlit run app.py --server.port 8502`

## 📱 Testowanie

1. Użyj `sample_data.csv` do szybkiego testu
2. Załaduj `35__welcome_survey_cleaned.csv` dla pełnej analizy
3. Przetestuj filtry w sidebar
4. Sprawdź różne wykresy

## 🎨 Dostosowywanie

- Edytuj `app.py` aby dodać nowe wykresy
- Zmień kolory w sekcji CSS
- Dodaj nowe filtry w sidebar

## 📞 Wsparcie

Jeśli masz problemy:

1. Sprawdź czy Python jest zainstalowany
2. Sprawdź połączenie internetowe
3. Uruchom jako administrator
4. Sprawdź logi błędów w terminalu
run
