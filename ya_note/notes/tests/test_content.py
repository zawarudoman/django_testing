from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Первый пользователь')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Второй пользователь')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Test',
            text='Test description',
            slug='slug',
            author=cls.author
        )

    def test_create_and_edit_note_page_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                form = response.context.get('form')
                self.assertIn('form', response.context)
                self.assertIsInstance(form, NoteForm)

    def test_note_in_list_for_author(self):
        url = reverse('notes:list')
        response = self.author_client.get(url)
        object_context = response.context['object_list']
        self.assertIn(self.note, object_context)

    def test_note_not_in_list_for_another_user(self):
        url = reverse('notes:list')
        response = self.reader_client.get(url)
        object_context = response.context['object_list']
        self.assertIsNot(self.note, object_context)
