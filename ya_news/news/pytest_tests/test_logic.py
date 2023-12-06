from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS
from news.models import Comment


COMMENT_FORM_DATA = {'text': 'new_text_comment'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, url_detail):
    comment_count_up_to = Comment.objects.count()
    client.post(url_detail, data=COMMENT_FORM_DATA)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_up_to


@pytest.mark.django_db
def test_user_can_create_comment(
        first_author_client,
        news,
        first_author,
        url_detail
):
    comment_count_up_to = Comment.objects.count()
    response = first_author_client.post(url_detail, data=COMMENT_FORM_DATA)
    assertRedirects(response, f'{url_detail}#comments')
    comment_count = Comment.objects.count()
    assert comment_count_up_to + 1 == comment_count
    comment = Comment.objects.last()
    assert comment.news == news
    assert comment.text == COMMENT_FORM_DATA.get('text')
    assert comment.author == first_author


@pytest.mark.django_db
def test_user_cant_use_bad_words(news, first_author_client, url_detail):
    comment_count_up_to = Comment.objects.count()
    bad_words_data = {'text': f'Какой-тотекст, {choice(BAD_WORDS)}, еще текст'}
    first_author_client.post(url_detail, data=bad_words_data)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_up_to


@pytest.mark.django_db
def test_author_can_delete_comment(
        news,
        first_author_client,
        first_comment,
        url_delete
):
    first_author_client.delete(url_delete)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_another_user(
        news,
        second_author_client,
        first_comment,
        url_delete
):
    comment_count_up_to = Comment.objects.count()
    response = second_author_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == comment_count_up_to


@pytest.mark.django_db
def test_author_can_edit_comment(
        news,
        first_author_client,
        first_author,
        first_comment,
        url_edit
):
    news_up_to = news
    first_author_client.post(url_edit, data=COMMENT_FORM_DATA)
    first_comment.refresh_from_db()
    assert first_comment.text == COMMENT_FORM_DATA.get('text')
    assert first_comment.author == first_author
    assert news.text == news_up_to.text


@pytest.mark.django_db
def test_user_cant_edit_of_another_comment(
        news,
        second_author_client,
        first_comment,
        url_edit
):
    comment = first_comment
    response = second_author_client.post(url_edit, data=COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    first_comment.refresh_from_db()
    assert first_comment.text == comment.text
