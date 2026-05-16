import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

@pytest.fixture
def dao_set():
    dao_mock = MagicMock()
    dao_mock.find.return_value = [ {"email": "yoda@starwars.com"}]
    user_controller = UserController(dao = dao_mock)
    
    return user_controller

def test_find_valid_user(dao_set):
    # Arrange
    # (dao_set)
    
    # Act
    result = dao_set.get_user_by_email("yoda@starwars.com")
    
    # Assert
    assert result == {"email": "yoda@starwars.com"}

def test_invalid_email_no_special_char(dao_set):
    # Arrange
    # (dao_set)
    
    # Act/assert
    with pytest.raises(ValueError):
        dao_set.get_user_by_email("r2d2starwars.com")

def test_invalid_email_no_dot(dao_set):
    # Arrange
    # (dao_set)
    
    # Act/assert
    with pytest.raises(ValueError):
        dao_set.get_user_by_email("r2d2@starwarscom")

def test_vaild_email_no_active_account():
    # Arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = []
    user_controller = UserController(dao = dao_mock)
    
    # Act
    result = user_controller.get_user_by_email("r2d2@starwars.com")

    # Assert
    assert result is None # ERROR: List index out of range

def test_invalid_email_no_active_account():
    # Arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = []
    user_controller = UserController(dao = dao_mock)
    
    # Act/assert
    with pytest.raises(ValueError):
        result = user_controller.get_user_by_email("r2d2starwars.com")

def test_valid_email_no_database_connection():
    # Arrange
    dao_mock = MagicMock()
    dao_mock.find.side_effect = Exception()
    user_controller = UserController(dao = dao_mock)
    
    # Act/assert
    with pytest.raises(Exception):
        result = user_controller.get_user_by_email("r2d2@starwars.com")

def test_invalid_email_no_database_connection():
    # Arrange
    dao_mock = MagicMock()
    dao_mock.find.side_effect = Exception()
    user_controller = UserController(dao = dao_mock)
    
    # Act/assert
    with pytest.raises(Exception):
        result = user_controller.get_user_by_email("r2d2starwars.com")

def test_valid_email_registred_user_no_database_connection():
    # Arrange
    dao_mock = MagicMock()
    dao_mock.find.return_value = [ {"email": "yoda@starwars.com"}]
    dao_mock.find.side_effect = Exception()
    user_controller = UserController(dao = dao_mock)
    
    # Act/assert
    with pytest.raises(Exception):
        result = dao_set.get_user_by_email("yoda@starwars.com")