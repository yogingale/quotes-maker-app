from unittest import TestCase

import pytest

import main
from tests.test_config import Config

# http://flask.pocoo.org/docs/1.0/testing/


@pytest.fixture(scope="session")
def app():
    app = main.create_app(config_class=Config)
    app.debug = True
    client = app.test_client(use_cookies=True)
    app.client = client
    return app


def test_index(app):
    res = app.client.get("/")
    print(res.status_code)
    assert res.status_code == 302


def test_get_login(app):
    with app.test_request_context():
        res = app.client.get("/auth/login")
        assert res.status_code == 200
        TestCase().assertIn(b"Anonymous User", res.data)


def login(app, username, password):
    return app.client.post(
        "/auth/login",
        data=dict(
            username=username, password=password, csrf_token=app.client.csrf_token
        ),
        follow_redirects=True,
        content_type="application/x-www-form-urlencoded",
    )


def logout(app):
    app.client.get("/auth/logout")


def test_login(app):
    with app.test_request_context():
        response = login(app, "user1", "user1")
        assert response.status_code == 200
        TestCase().assertIn(b"ROLE: NOT ADMIN", response.data)


def test_tables(app):
    res = app.client.get("/tables/")
    assert res.status_code == 200
    print(res.data)
