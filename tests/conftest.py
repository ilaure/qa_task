import pytest


def pytest_make_parametrize_id(val):
    return repr(val)


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="localhost")
    parser.addoption("--port", action="store", default="5000")


@pytest.fixture(scope='session')
def app_url(pytestconfig):
    host = pytestconfig.getoption("host")
    port = pytestconfig.getoption("port")
    return f'http://{host}:{port}'


@pytest.fixture(scope='session')
def app_url_minutes(app_url):
    return f'{app_url}/minutes/'


@pytest.fixture(scope='session')
def app_url_check_ident(app_url):
    return f'{app_url}/check_ident'

