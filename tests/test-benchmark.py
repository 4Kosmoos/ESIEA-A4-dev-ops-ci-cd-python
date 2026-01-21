import os
import tempfile
import pytest
from app.api import create_app
from app.db import init_db, add_user
from app.utils import doThing, GLOBAL


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

def test_add_user(app, benchmark):
    def create_user():
        return add_user("user_added")
    result = benchmark(create_user)
    assert result is not None

def test_get_user(app, benchmark):
    user_id = add_user("user_to_get")
    def get_user_op():
        from app.db import get_user
        return get_user(user_id)
    result = benchmark(get_user_op)
    assert result is not None

def test_dothing(benchmark):
    GLOBAL["users"].clear()
    def do_thing_op():
        return doThing("user", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    result = benchmark(do_thing_op)
    assert result is True

def test_dothing_update(benchmark):
    GLOBAL["users"].clear()
    doThing("user_edited", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    def update_thing_op():
        return doThing("user_edited", 10, 20, 30, 40, 50, 60, 70, 80, 90)
    result = benchmark(update_thing_op)
    assert result is True