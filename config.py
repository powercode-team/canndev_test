SCORING_THRESHOLDS = {"HIGH_PRIORITY": 70, "MEDIUM_PRIORITY": 30, "LOW_PRIORITY": 10}

KEYWORDS = {
    "high": {
        "keywords": [
            "cannabis retail",
            "dispensary license",
            "application window",
            "ordinance approved",
            "licensing program",
            "application period",
            "merit-based selection",
            "conditional use permit approved",
            "second reading",
        ],
        "score": 10,
    },
    "medium": {
        "keywords": [
            "public hearing",
            "planning commission",
            "draft ordinance",
            "zoning amendment",
            "social equity",
            "moratorium lifted",
            "cannabis business",
            "study session",
        ],
        "score": 5,
    },
    "low": {
        "keywords": [
            "cannabis",
            "marijuana",
            "dispensary",
            "retail",
            "tax revenue",
            "budget discussion",
            "general mention",
        ],
        "score": 2,
    },
}

CONTEXT_MODIFIERS = [
    {"pattern": r"\b(approved|passed|effective|final)\b", "score": 3},
    {"pattern": r"\b(prohibited|banned|rejected)\b", "score": -3},
]

TITLE_HEADING_BONUS = 2

DATE_PATTERN = (
    r"\b(?:"
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+\d{4}"
    r"|\d{1,2}/\d{1,2}/\d{4}"
    r"|\d{4}-\d{2}-\d{2}"
    r")\b"
)

DATE_WINDOW_DAYS = 90
DATE_MATCH_SCORE = 5
