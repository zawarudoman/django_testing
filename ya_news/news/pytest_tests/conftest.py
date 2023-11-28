import pytest
from datetime import datetime, timedelta

from news.models import Comment, News


now = datetime.now()
today = datetime.today()
yesterday = today - timedelta(days=1)


@pytest.fixture
def author1(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client1(author1, client):
    client.force_login(author1)
    return client


@pytest.fixture
def author2(django_user_model):
    return django_user_model.objects.create(username='Автор2')


@pytest.fixture
def author_client2(author2, client):
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
