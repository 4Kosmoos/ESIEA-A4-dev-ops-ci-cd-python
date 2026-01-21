import os
import tempfile
import pytest
from app.api import create_app
from app.db import init_db, add_user, get_user, User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    os.environ["APP_DB_PATH"] = db_path

    init_db()
    app = create_app()
    app.config["TESTING"] = True

    yield app

    os.close(db_fd)
    os.unlink(db_path)
@pytest.fixture
def client(app):
    return app.test_client()

def test_init_db(app):
    assert True

def test_add_user_success(app):
    user_id = add_user("John")
    assert user_id == 1
    user = get_user(user_id)
    assert user is not None
    assert user.name == "John"

def test_add_user_with_empty_name(app):
    with pytest.raises(ValueError) as excinfo:
        add_user("")
    assert "name must be non-empty" in str(excinfo.value)

def test_get_user_404(app):
    user = get_user(404)
    assert user is None

def test_add_multiple_users(app):
    id1 = add_user("John1")
    id2 = add_user("John2")
    id3 = add_user("John3")
    assert id1 == 1
    assert id2 == 2
    assert id3 == 3
    assert get_user(id1).name == "John1"
    assert get_user(id2).name == "John2"
    assert get_user(id3).name == "John3"


def test_user_dataclass():
    user = User(id=1, name="Test")
    assert user.id == 1
    assert user.name == "Test"

    with pytest.raises(AttributeError):
        user.name = "Modified"
