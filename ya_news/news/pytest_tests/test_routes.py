from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(
        client,
        url_home,
        url_detail,
        url_login,
        url_logout,
        url_signup
):
    urls = (url_home, url_detail, url_login, url_logout, url_signup)
    for url in urls:
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
def test_anonymous_user_redirect_upon_attempt_edit_and_delete_comment(
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
