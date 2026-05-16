import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {'name':'Jane'}
def user():
    return {'email':'Tuan'}
@pytest.mark.unit
def test_hasAttribute_true(obj):
    result = hasAttribute(obj, 'name')
    assert result == True

@pytest.mark.unit
def test_hasAttribute_false(obj):
    result = hasAttribute(obj, 'age')
    assert result == False

@pytest.mark.unit
def test_hasAttribute_none():
    result = hasAttribute(None, 'name')
    assert result == False
