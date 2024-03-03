from django.forms import ValidationError
from django.test import TestCase
from parameterized import parameterized

from .test_posts_base import PostMixin


class PostModelTest(TestCase, PostMixin):
    def test_valid_object_can_be_created_correctly(self):
        post = self.make_post_object()
        post.full_clean()
        post.save()
        self.assertTrue(post.pk)

    @parameterized.expand([
        ('username', 255),
        ('title', 255),
    ])
    def test_post_fields_max_length(self, field, max_length):
        post = self.make_post_object()
        post.full_clean()
        setattr(post, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_object_string_representation_returns_title(self):
        post = self.make_post_object()
        self.assertEqual(str(post), post.title)
