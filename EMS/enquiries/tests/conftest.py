import pytest


@pytest.fixture
def user_data():
    return {
                "email": "test@localhost.app",
                "full_name": "testcase",
                "gender": "M",
                "password1": "some_strong_psw",
                "password2": "some_strong_psw"
            }
