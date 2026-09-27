import pytest

from utils.risk import risk_level_from_score


@pytest.mark.parametrize(
    ("score", "expected"),
    [(0, "low"), (24, "low"), (25, "medium"), (49, "medium"),
     (50, "high"), (74, "high"), (75, "critical"), (100, "critical")],
)
def test_risk_level_boundaries(score, expected):
    assert risk_level_from_score(score) == expected
