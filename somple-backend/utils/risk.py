RISK_LEVEL_ORDER = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}

RISK_POLICY_VERSION = "score-thresholds-v1"
RISK_THRESHOLDS = {
    "low": {"min": 0, "max": 24},
    "medium": {"min": 25, "max": 49},
    "high": {"min": 50, "max": 74},
    "critical": {"min": 75, "max": 100},
}

def score_from_probabilities(probabilities: dict[str, float]) -> tuple[int, str]:
    expected = sum(RISK_LEVEL_ORDER[level] * prob for level, prob in probabilities.items())
    score = round((expected / 3) * 100)
    score = max(0, min(100, score))
    level = risk_level_from_score(score)
    return score, level


def risk_level_from_score(score: int) -> str:
    bounded_score = max(0, min(100, score))
    for level, bounds in RISK_THRESHOLDS.items():
        if bounds["min"] <= bounded_score <= bounds["max"]:
            return level
    return "critical"


def is_high_risk(level: str) -> bool:
    return level in {"high", "critical"}
