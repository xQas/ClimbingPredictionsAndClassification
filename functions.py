# standardowe biblioteki
import pandas as pd

# biblioteki zewnętrzne
import joblib
import streamlit as st


@st.cache_data
def load_data():
    """Odczytuje dataset "regressionNEW_df" z pliku .csv"""
    return pd.read_csv('data/regressionNEW_df.csv')


def load_model(path, name):
    """Wczytuje model z pliku .pkl z pomocą joblib"""
    try:
        return joblib.load(path)
    except FileNotFoundError:
        st.error(f"Nie znaleziono modelu: {name} (ścieżka: {path})")
        return None


def get_basic_input_fields(prefix=""):
    """
    Zwraca powtarzającą się cześć formularza.

    Output:
    height, arm_span, age, gender_binary
    """
    height = st.number_input(f"{prefix}Wzrost (cm)", min_value=120, max_value=220, value=175)
    arm_span = st.number_input(f"{prefix}Rozpiętość ramion (cm)", min_value=120, max_value=240, value=180)
    age = st.number_input(f"{prefix}Wiek", min_value=15, max_value=80, value=25)
    gender = st.radio(f"{prefix}Płeć", ["Mężczyzna", "Kobieta"])
    gender_binary = 1 if gender == "Mężczyzna" else 0
    return age, height, arm_span, gender_binary
