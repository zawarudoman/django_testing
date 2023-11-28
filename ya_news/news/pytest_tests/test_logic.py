from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS


@pytest.fixture
def form_data():
    form_data = {'text': 'text_comment'}
    return form_data


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, form_data):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client1, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = author_client1.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comment_count = Comment.objects.count()
    assert comment_count == 1
    comment = Comment.objects.get()
    assert comment.news == news


@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client1):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    author_client1.post(url, data=bad_words_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(news, author_client1, comment1):
    author_client1.delete(reverse('news:delete', args=(news.id,)))
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_another_user(news, author_client2, comment1):
    response = author_client2.delete(reverse('news:delete', args=(news.id,)))
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
