# standardowe biblioteki
import numpy as np
import pandas as pd

# biblioteki zewnętrzne
import altair as alt
import streamlit as st

# lokalne
from functions import load_data, get_basic_input_fields
from constants import *
from models import classifier, REGRESSOR_MAP


menu = st.sidebar.radio("Wybierz opcję:", ["Predyspozycje zawodnika", "Symulacja zawodów"])

if menu == "Predyspozycje zawodnika":

    # Formularz danych wejściowych
    st.title("Predyspozycje zawodnika do dyscypliny wspinaczkowej")
    st.write("Wprowadź dane zawodnika:")

    with st.form("prediction_form"):
        age, height, arm_span, gender_binary = get_basic_input_fields()

        submitted = st.form_submit_button("Oblicz predyspozycje")

    st.write("")  # pusta linia

    # Predykcja i wizualizacja
    if submitted:
        input_data = np.array([[age, height, arm_span, gender_binary]])
        probs = classifier.predict_proba(input_data)[0]

        # Dane
        labels = list(DISCIPLINE_MAP.values())
        probs_percent = [round(p * 100, 2) for p in probs]

        # Długi DataFrame
        df_long = pd.DataFrame({
            "Dyscyplina": labels,
            "Procent": probs_percent
        })

        # Wykres
        bar = alt.Chart(df_long).mark_bar().encode(
            x=alt.X('sum(Procent):Q', stack='normalize', title="Procent predyspozycji"),
            y=alt.value(0),
            color=alt.Color('Dyscyplina:N'),
            tooltip=['Dyscyplina', alt.Tooltip('Procent:Q', format='.2f')]
        ).properties(
            width=600,
            height=100
        )

        # Wyświetlenie
        st.altair_chart(bar, use_container_width=True)

        # Wyświetlenie tabeli pod spodem
        st.subheader("Szczegóły predykcji:")
        df_long['Procent'] = df_long['Procent'].map(lambda x: f"{x:.2f}%")
        st.dataframe(df_long, hide_index=True)

elif menu == "Symulacja zawodów":
    st.title("Symulacja wyników zawodów")

    df = load_data()
    df_test = df.loc[df.groupby(['athlete_id'])['avg_rank'].idxmin()]
    df_test = df_test.reset_index(drop=True)
    st.write("Wybierz zawodników z bazy lub dodaj własnych:")

    mode = st.radio("Metoda dodawania zawodników:", ["Z bazy danych", "Ręcznie"])

    if 'competitors' not in st.session_state:
        st.session_state.competitors = []

    if mode == "Z bazy danych":
        st.session_state.competitors = []
        selected_names = st.multiselect("Wybierz zawodników", df_test['firstname'] + "  " + df_test['lastname'],
                                        key="selected_names", default=[])
        for name in selected_names:
            first, last = name.split("  ")
            row = df_test[(df_test['firstname'] == first) & (df_test['lastname'] == last)].iloc[0]
            st.session_state.competitors.append(row)

    elif mode == "Ręcznie":
        with st.form("manual_form"):
            firstname = st.text_input("Imię")
            lastname = st.text_input("Nazwisko")
            event_age, height, arm_span, gender_binary = get_basic_input_fields()
            same_disc_best = st.selectbox("Twoja najmocniejsza dyscyplina", ['boulder', 'lead', 'speed'])
            overall_best_disc = DISCIPLINE_INV_MAP.get(same_disc_best, 0)
            experience_years = st.number_input("Liczba lat doświadczenia", min_value=0, max_value=40, value=2)

            submitted_sim = st.form_submit_button("Dodaj zawodnika")

            if submitted_sim:
                if not firstname or not lastname:
                    st.error("Proszę podać imię i nazwisko zawodnika.")
                else:
                    manual_data = {
                        'firstname': firstname,
                        'lastname': lastname,
                        'event_age': event_age,
                        'height': height,
                        'arm_span': arm_span,
                        'gender': gender_binary,
                        'event_experience': DEFAULT_EVENT_EXPERIENCE,
                        'avg_rank_last_3': DEFAULT_AVG_RANK_LAST_3,
                        'rank_std_last_3': DEFAULT_RANK_STD_LAST_3,
                        'overall_best_discipline': overall_best_disc,
                        'season_peak_rank': DEFAULT_SEASON_PEAK_RANK,
                        'experience_years': experience_years
                    }
                    st.session_state.competitors.append(pd.Series(manual_data))

    if st.session_state.competitors:
        discipline = st.selectbox("Wybierz dyscyplinę:", ["lead", "boulder", "speed"])
        regression_model = REGRESSOR_MAP[discipline]

        # Konwersja do DataFrame
        competitors_df = pd.DataFrame(st.session_state.competitors)
        competitors_df = competitors_df.reset_index(drop=True)

        # Predykcja i sortowanie
        X_predict = competitors_df[REGRESSION_FEATURES]
        competitors_df['predicted_rank'] = regression_model.predict(X_predict)
        competitors_df = competitors_df.sort_values(by='predicted_rank')

        st.subheader("Symulowane wyniki zawodów:")
        df_display = competitors_df[['firstname', 'lastname', 'predicted_rank']].rename(columns={
            'firstname': 'Imię',
            'lastname': 'Nazwisko',
            'predicted_rank': 'Przewidywana pozycja'
        })

        st.dataframe(df_display, hide_index=True)

        if st.button("Wyczyść listę zawodników"):
            st.session_state.clear()
            st.rerun()
