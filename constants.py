DEFAULT_EVENT_EXPERIENCE = 21.88
DEFAULT_AVG_RANK_LAST_3 = 25.89
DEFAULT_RANK_STD_LAST_3 = 12.97
DEFAULT_SEASON_PEAK_RANK = 14.62

DISCIPLINE_MAP = {0: "głazownictwo", 1: "na trudność", 2: "na czas"}
DISCIPLINE_INV_MAP = {v: k for k, v in DISCIPLINE_MAP.items()}

REGRESSION_FEATURES = [
    'event_age', 'height', 'arm_span', 'gender',
    'event_experience', 'avg_rank_last_3', 'rank_std_last_3',
    'overall_best_discipline', 'season_peak_rank', 'experience_years'
]
