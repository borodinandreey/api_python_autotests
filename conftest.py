import pytest
from helper.helper_user import create_fake_name, create_fake_email, create_fake_password
from methods.create_user import CreateUser


@pytest.fixture()
def user_payload():
    return {
        "email": create_fake_email(),
        "password": create_fake_password(),
        "name": create_fake_name()
    }

@pytest.fixture()
def delete_user():
    tokens = []
    yield tokens
    for token in tokens:
        CreateUser.delete_create_user(token)
