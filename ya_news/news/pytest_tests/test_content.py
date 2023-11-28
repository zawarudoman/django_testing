import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse

from news.models import News

URL = reverse('news:home')
now = datetime.now()


@pytest.fixture
def news_paginate():
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_paginate = News(
            title=f'title{index}',
            text='text',
            date=today - timedelta(days=index)
        )
        all_news.append(news_paginate)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.mark.django_db
def test_news_count(news_paginate, client):
    response = client.get(URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news):
    response = client.get(URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, comment1, comment2, news):
    response = client.get(reverse('news:detail', args=(news.id,)))
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(author_client1, news):
    response = author_client1.get(reverse('news:detail', args=(news.id,)))
    assert 'form' in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(client, news):
    response = client.get(reverse('news:detail', args=(news.id,)))
    assert 'form' not in response.context
