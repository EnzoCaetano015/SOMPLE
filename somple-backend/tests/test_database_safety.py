import pytest

from conftest import _assert_test_database


@pytest.mark.parametrize(
    "url",
    [
        "postgresql://somple:secret@localhost:5432/somple",
        "postgresql://somple:secret@db.internal/production",
        "postgresql://somple:secret@db.internal/dev",
    ],
)
def test_database_guard_rejects_non_test_databases(url):
    with pytest.raises(RuntimeError, match="Refusing to run destructive tests"):
        _assert_test_database(url)


def test_database_guard_accepts_dedicated_test_database():
    _assert_test_database("postgresql://somple_test:secret@localhost:5433/somple_test")
