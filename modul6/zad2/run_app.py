#!/usr/bin/env python3
"""
Skrypt do uruchomienia aplikacji Streamlit
"""

import subprocess
import sys
import os


def install_requirements():
    """Instaluje wymagane pakiety"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Wymagane pakiety zostały zainstalowane")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd podczas instalacji pakietów: {e}")
        return False
    return True


def run_streamlit():
    """Uruchamia aplikację Streamlit"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplikacja została zatrzymana")
    except Exception as e:
        print(f"❌ Błąd podczas uruchamiania aplikacji: {e}")


if __name__ == "__main__":
    print("🚀 Uruchamianie aplikacji Streamlit...")

    # Sprawdź czy plik requirements.txt istnieje
    if os.path.exists("requirements.txt"):
        print("📦 Instalowanie wymaganych pakietów...")
        if install_requirements():
            print("🌐 Uruchamianie aplikacji...")
            run_streamlit()
        else:
            print("❌ Nie można zainstalować pakietów. Sprawdź połączenie internetowe.")
    else:
        print("❌ Nie znaleziono pliku requirements.txt")
        print("💡 Uruchom: pip install streamlit pandas plotly numpy")
        print("🌐 Następnie uruchom: streamlit run app.py")
