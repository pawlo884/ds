@echo off
echo 🚀 Uruchamianie aplikacji Streamlit...
echo.

REM Sprawdź czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nie jest zainstalowany lub nie jest w PATH
    echo 💡 Zainstaluj Python z https://python.org
    pause
    exit /b 1
)

echo 📦 Instalowanie wymaganych pakietów...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Błąd podczas instalacji pakietów
    pause
    exit /b 1
)

echo ✅ Pakiety zainstalowane pomyślnie
echo 🌐 Uruchamianie aplikacji...
echo.
echo 📱 Aplikacja będzie dostępna pod adresem: http://localhost:8501
echo 🛑 Aby zatrzymać aplikację, naciśnij Ctrl+C
echo.

streamlit run app.py

pause

