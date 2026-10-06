import pytest

from vascular_age.preprocessing import validate_age


def test_valid_age():
    assert validate_age(35) == 35


def test_invalid_age_raises_value_error():
    with pytest.raises(ValueError):
        validate_age(150)