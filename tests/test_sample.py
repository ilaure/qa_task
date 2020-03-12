# -*- coding: utf-8 -*-
from http import HTTPStatus
import pytest
import requests


class TestBasicStatusCodes:
    def test_sample(self, app_url):
        response = requests.get(app_url)
        assert response.status_code == HTTPStatus.OK

    def test_get_response_hello_world(self, app_url):
        response = requests.get(app_url)
        assert response.text == 'Hello World!'

    def test_get_response_wrong_pass(self, app_url):
        response = requests.get(app_url + '/wrong_pass/')
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_post_to_app_url_minutes(self, app_url_minutes):
        response = requests.post(app_url_minutes, 'test post')
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestGetMinutes:
    @pytest.mark.parametrize("count, ending", [
        ('0', 'минут'), ('1', 'минуту'), ('2', 'минуты'), ('4', 'минуты'), ('5', 'минут'), ('10', 'минут'),
        ('11', 'минут'), ('12', 'минут'), ('13', 'минут'), ('14', 'минут'), ('20', 'минут'), ('21', 'минуту'),
        ('33', 'минуты'), ('42', 'минуты'), ('1000', 'минут')])
    def test_get_response_minutes(self, app_url_minutes, count, ending):
        response = requests.get(app_url_minutes + count)
        assert response.text == f'Вы ввели: {count} {ending}'

    @pytest.mark.parametrize("notint", ['notint', '#', 'текст', ' '])
    def test_get_response_not_int(self, app_url_minutes, notint):
        response = requests.get(app_url_minutes + notint)
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestPostCheckIdent:
    def test_post_check_ident_basic_ident(self, app_url_check_ident):
        response = requests.post(app_url_check_ident, json={"ident": "00000-00000 0"})
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'result': True}

    def test_post_check_ident_bad_request(self, app_url_check_ident):
        response = requests.post(app_url_check_ident, json={"bad request": "00000-00000 0"})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text == 'Content Type is not json'

    @pytest.mark.parametrize("ident", ['0-0 0', '00000-00000 X', 'XXXXX-XXXXX 0', 'XXXXX-XXXXX X', '?????-????? ?', '01234-5678X 2'])
    def test_post_check_ident_invalid_format(self, app_url_check_ident, ident):
        response = requests.post(app_url_check_ident, json={"ident": ident})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text == 'Invalid format'

    def test_post_check_ident_unsupported_media_type(self, app_url_check_ident):
        response = requests.post(app_url_check_ident, 'unsupported data')
        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        assert response.text == 'Content Type is not json'

    @pytest.mark.parametrize("ident, check_sum", [
        ('01234-56789', '2'),
        ('98765-43210', '9'),
        ('11111-11111', '9'),
        ('11111-11110', '9'),
        ('11111-11100', '8'),
        ('11111-11000', '7'),
        ('11111-10000', '6'),
        ('11111-00000', '5'),
        ('11110-00000', '4'),
        ('11100-00000', '3'),
        ('11000-00000', '2'),
        ('10000-00000', '1'),
        ('22222-22222', '5'),
        ('33333-33333', '1'),
        ('44444-44444', '1'),
        ('55555-55555', '1'),
        ('66666-66666', '2'),
        ('77777-77777', '2'),
        ('88888-88888', '5'),
        ('99999-99999', '2'),
        ('00000-00000', '0')
    ])
    def test_post_check_diff_ident(self, app_url_check_ident, ident, check_sum):
        response = requests.post(app_url_check_ident, json={"ident": ident + ' ' + check_sum})
        assert response.json() == {'result': True}
