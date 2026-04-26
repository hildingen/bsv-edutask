import pytest
from unittest.mock import MagicMock
from src.util.helpers import ValidationHelper


@pytest.fixture
def sut():
    mock_usercontroller = MagicMock()
    return ValidationHelper(usercontroller=mock_usercontroller)


@pytest.mark.unit
@pytest.mark.parametrize('age, expected', [
    (-1, 'invalid'),
    (0, 'underaged'),
    (1, 'underaged'),
    (17, 'underaged'),
    (18, 'valid'),
    (19, 'valid'),
    (119, 'valid'),
    (120, 'valid'),
    (121, 'invalid'),
])
def test_validateAge(sut, age, expected):
    sut.usercontroller.get.return_value = {'age': age}
    result = sut.validateAge(userid=None)
    assert result == expected