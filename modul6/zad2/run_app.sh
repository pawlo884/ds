#!/bin/bash

echo "🚀 Uruchamianie aplikacji Streamlit..."
echo

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany"
    echo "💡 Zainstaluj Python3 używając menedżera pakietów"
    exit 1
fi

echo "📦 Instalowanie wymaganych pakietów..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Błąd podczas instalacji pakietów"
    exit 1
fi

echo "✅ Pakiety zainstalowane pomyślnie"
echo "🌐 Uruchamianie aplikacji..."
echo
echo "📱 Aplikacja będzie dostępna pod adresem: http://localhost:8501"
echo "🛑 Aby zatrzymać aplikację, naciśnij Ctrl+C"
echo

streamlit run app.py
