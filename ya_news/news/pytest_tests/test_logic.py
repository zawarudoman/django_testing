from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS


TEXT_COMMENT = {'text': 'new_text_comment'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, url_detail):
    client.post(url_detail, data=TEXT_COMMENT)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client1, news, author1, url_detail):
    comment_count_up_to = Comment.objects.count()
    response = author_client1.post(url_detail, data=TEXT_COMMENT)
    assertRedirects(response, f'{url_detail}#comments')
    comment_count = Comment.objects.count()
    assert comment_count_up_to < comment_count
    comment = Comment.objects.last()
    assert comment.news == news
    assert comment.text == TEXT_COMMENT.get('text')
    assert comment.author == author1


@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client1, url_detail):
    bad_words_data = {'text': f'Какой-тотекст, {choice(BAD_WORDS)}, еще текст'}
    author_client1.post(url_detail, data=bad_words_data)
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


@pytest.mark.django_db
def test_author_can_edit_comment(news, author_client1, comment1):
    url = reverse('news:edit', args=(comment1.id,))
    response = author_client1.post(url, data=TEXT_COMMENT)
    comment1.refresh_from_db()
    assert comment1.text == TEXT_COMMENT.get('text')


@pytest.mark.django_db
def test_user_cant_edit_of_another_comment(news, author_client2, comment1):
    url = reverse('news:edit', args=(comment1.id,))
    response = author_client2.post(url, data=TEXT_COMMENT)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment1.refresh_from_db()
    assert comment1.text == 'text comment'
