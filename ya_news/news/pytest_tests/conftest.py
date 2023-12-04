import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.test import Client
from django.urls import reverse


from news.models import Comment, News

now = datetime.now()
today = datetime.today()
yesterday = today - timedelta(days=1)


@pytest.fixture
def author1(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client1(author1):
    client = Client()
    client.force_login(author1)
    return client


@pytest.fixture
def author2(django_user_model):
    return django_user_model.objects.create(username='Автор2')


@pytest.fixture
def author_client2(author2):
    client = Client()
    client.force_login(author2)
    return client


@pytest.fixture
def news():
    news = News.objects.create(title='title', text='text', date=now)
    return news


@pytest.fixture
def comment1(news, author1):
    comment = Comment.objects.create(
        news=news,
        author=author1,
        text='text comment',
        created=now
    )
    return comment


@pytest.fixture
def comment2(news, author2):
    comment = Comment.objects.create(
        news=news,
        author=author2,
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
    return all_news


@pytest.fixture
def url_home():
    url_home = reverse('news:home')
    return url_home


@pytest.fixture
def url_detail(news):
    url_detail = reverse('news:detail', args=(news.id,))
    return url_detail


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
