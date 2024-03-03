from django.test import SimpleTestCase
from django.urls import reverse

from postlist.models import Post


class PostBaseTest(SimpleTestCase):
    def test_the_test(self):
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)
        self.assertIsNone(None)
        self.assertIsNotNone(0)


class PostMixin:
    url = reverse('postlist:postlist-api-list')
    details_url = 'postlist:postlist-api-detail'

    def make_post_object(self,
                         username='Username',
                         title='Title for a new post',
                         content='Hello!' * 30):
        return Post.objects.create(
            username=username,
            title=title,
            content=content,
        )

    def get_post_data(self,
                      username='Username',
                      title='Title for a new post',
                      content='Hello!' * 30,
                      change=''):
        return {
            'username': username + str(change),
            'title': title + str(change),
            'content': content + str(change),
        }

    def send_post_data(self, client, post_data,
                       url=reverse('postlist:postlist-api-list')):
        response = client.post(url, post_data, format='json')
        return response

    def send_post_data_in_batch(self, client, posts=11):
        for n in range(posts):
            self.send_post_data(client, self.get_post_data(change=n))
