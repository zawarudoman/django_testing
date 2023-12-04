import pytest
from datetime import datetime

from django.conf import settings


now = datetime.now()


@pytest.mark.django_db
def test_news_count(news_paginate, client, url_home):
    response = client.get(url_home)
    object_context = response.context['object_list']
    news_count = len(object_context)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news, url_home):
    response = client.get(url_home)
    object_context = response.context['object_list']
    all_dates = [news.date for news in object_context]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, comment1, comment2, news, url_detail):
    response = client.get(url_detail)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(author_client1, news, url_detail):
    response = author_client1.get(url_detail)
    assert 'form' in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(client, news, url_detail):
    response = client.get(url_detail)
    assert 'form' not in response.context
