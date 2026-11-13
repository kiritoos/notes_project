from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Category, Note, Tag

class IndexQueriesTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        user = get_user_model().objects.create(username="u")
        cat = Category.objects.create(name="c")
        tag = Tag.objects.create(name="t")
        for i in range(30):
            note = Note.objects.create(title=f"n{i}", owner=user, category=cat)
            note.tags.add(tag)

    def test_query_count_does_not_grow(self):
        # Проверяем, что для отрисовки страницы нужно ровно 4 запроса
        # (если вы видите на панели 4, поставьте 4)
        with self.assertNumQueries(4):
            self.client.get("/")