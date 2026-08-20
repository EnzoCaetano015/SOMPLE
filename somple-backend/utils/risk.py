RISK_LEVEL_ORDER = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}

RISK_LEVEL_FROM_SCORE = (
    (25, "low"),
    (50, "medium"),
    (75, "high"),
    (101, "critical"),
)


def score_from_probabilities(probabilities: dict[str, float]) -> tuple[int, str]:
    expected = sum(RISK_LEVEL_ORDER[level] * prob for level, prob in probabilities.items())
    score = round((expected / 3) * 100)
    score = max(0, min(100, score))
    level = risk_level_from_score(score)
    return score, level


def risk_level_from_score(score: int) -> str:
    for threshold, level in RISK_LEVEL_FROM_SCORE:
        if score < threshold:
            return level
    return "critical"


def is_high_risk(level: str) -> bool:
    return level in {"high", "critical"}
