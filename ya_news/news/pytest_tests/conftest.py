from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.test import Client
from django.urls import reverse


from news.models import Comment, News

today = datetime.today()
yesterday = today - timedelta(days=1)


@pytest.fixture
def first_author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def first_author_client(first_author):
    client = Client()
    client.force_login(first_author)
    return client


@pytest.fixture
def second_author(django_user_model):
    return django_user_model.objects.create(username='Автор2')


@pytest.fixture
def second_author_client(second_author):
    client = Client()
    client.force_login(second_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='title',
        text='text',
        date=datetime.now()
    )
    return news


@pytest.fixture
def first_comment(news, first_author):
    comment = Comment.objects.create(
        news=news,
        author=first_author,
        text='text comment',
        created=datetime.now()
    )
    return comment


@pytest.fixture
def second_comment(news, second_author):
    comment = Comment.objects.create(
        news=news,
        author=second_author,
        text='text comment',
        created=yesterday
    )
    return comment


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


@pytest.fixture
def url_home():
    url_home = reverse('news:home')
    return url_home


@pytest.fixture
def url_detail(news):
    url_detail = reverse('news:detail', args=(news.id,))
    return url_detail


@pytest.fixture
def url_edit(first_comment):
    url_edit = reverse('news:edit', args=(first_comment.id,))
    return url_edit


@pytest.fixture
def url_delete(news):
    url_delete = reverse('news:delete', args=(news.id,))
    return url_delete


@pytest.fixture
def url_login(news):
    url_login = reverse('users:login')
    return url_login


@pytest.fixture
def url_logout(news):
    url_logout = reverse('users:logout')
    return url_logout


@pytest.fixture
def url_signup(news):
    url_signup = reverse('users:signup')
    return url_signup
