from functions import load_model

classifier = load_model('data/classifier_model.pkl', 'Classifier')
regressor_lead = load_model('data/lead_regressor.pkl', 'Regressor Lead')
regressor_boulder = load_model('data/boulder_regressor.pkl', 'Regressor Boulder')
regressor_speed = load_model('data/speed_regressor.pkl', 'Regressor Speed')

REGRESSOR_MAP = {
    "lead": regressor_lead,
    "boulder": regressor_boulder,
    "speed": regressor_speed
}
