from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    (
        pytest.lazy_fixture('url_home'),
        pytest.lazy_fixture('url_detail'),
        pytest.lazy_fixture('url_login'),
        pytest.lazy_fixture('url_logout'),
        pytest.lazy_fixture('url_signup')
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    (
        pytest.lazy_fixture('url_edit'),
        pytest.lazy_fixture('url_delete'),
    )
)
@pytest.mark.django_db
def test_user_edit_and_delete_comment(
        first_comment,
        author_create_comment_client,
        news,
        name
):
    response = author_create_comment_client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    (
        pytest.lazy_fixture('url_edit'),
        pytest.lazy_fixture('url_delete'),
    )
)
@pytest.mark.django_db
def test_anonymous_user_redirect_upon_attempt_edit_and_delete_comment(
        client,
        news,
        name
):
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'name',
    (
        pytest.lazy_fixture('url_edit'),
        pytest.lazy_fixture('url_delete'),
    )
)
@pytest.mark.django_db
def test_anonymous_user_redirect_upon_attempt_edit_and_delete_commnet(
        first_comment,
        reader_news_client,
        news,
        name
):
    response = reader_news_client.get(name)
    assert response.status_code == HTTPStatus.NOT_FOUND
