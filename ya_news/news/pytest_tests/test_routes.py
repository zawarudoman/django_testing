import pytest
from datetime import datetime

from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects

now = datetime.now()


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_pages_news_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_user_edit_and_delete_comment(comment1, author_client1, name, news):
    url = reverse(name, args=(comment1.id,))
    response = author_client1.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_anonymous_user_redirect_upon_attempt_edit_and_delete_commnet(
        client,
        name,
        news
):
    login_url = reverse('users:login')
    url = reverse(name, args=(news.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_anonymous_user_redirect_upon_attempt_edit_and_delete_commnet(
        comment1,
        author_client2,
        name,
        news
):
    url = reverse(name, args=(news.id,))
    response = author_client2.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
