import pytest
from src.util.helpers import hasAttribute,hasEmail,isTeenager,isPositive,isAdult,grade,hasName,isBetween

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

@pytest.mark.unit
def test_hasEmail_true(user):
    result = hasEmail(user)
    assert result == True

@pytest.mark.unit  
def test_hasEmail_None():
    result = hasEmail(None)
    assert result == False
    
@pytest.mark.unit  
def test_hasEmail_no_email(user):
    result = hasEmail(user)
    assert result == False
    
@pytest.mark.unit
@pytest.mark.parametrize('age, expected',[
    (12,False),
    (13,True),
    (14,True),
    (18,True),
    (19,True),
    (20,False),
])
def test_isTeenager(age,expected):
    result = isTeenager(age)
    assert result == expected
    
@pytest.mark.unit
@pytest.mark.parametrize('number,expected',[
    (-1,False),
    (0,False),
    (1,True),
])
def test_isPositive(number,expected):
    result = isPositive(number)
    assert result == expected
    
@pytest.mark.unit
@pytest.mark.parametrize('age,expected', [
    (17,False),
    (18,True),
    (19,True),
])
def test_isAdult(age,expected):
    result = isAdult(age)
    assert result == expected
    
@pytest.mark.unit
@pytest.mark.parametrize('score,expected',[
    (-1,'invalid'),
    (0,'fail'),
    (49,'fail'),
    (50,'pass'),
    (79,'pass'),
    (80,'distinction'),
    (81,'distinction'),
])
def test_isGrade(score,expected):
    result = grade(score)
    assert result == expected
    
@pytest.mark.unit
@pytest.mark.parametrize('name,expected',[
    ('name',True),
    ('None',False),
])
def test_hasName(name,expected):
    result = hasName(name)
    assert result == expected
    
@pytest.mark.unit
@pytest.mark.parametrize('value, low, hight ,expected',[
    (9, 10, 20, False ),
    (10, 10, 20, True ),
    (20, 10, 20, True ),
    (21, 10, 20, False ),
])
def test_isBetween(value,low,hight,expected):
    assert isBetween(value,low,hight) == expected