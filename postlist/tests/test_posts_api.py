from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from .test_posts_base import PostMixin


class PostApiGETTest(APITestCase, PostMixin):
    def test_api_get_call_on_empty_database_returns_status_code_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_initial_results_list_is_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])

    def test_api_get_initial_next_and_previous_pointers_are_null(self):
        response = self.client.get(self.url)
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_post_details_can_be_retrieved_correctly(self):
        post_data = self.get_post_data()
        response = self.send_post_data(self.client, post_data)
        pk = response.data.get('id')
        response = self.client.get(self.url, args=(pk,))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0].get('id'), pk)
        self.assertEqual(response.data['results'][0].get(
            'title'), post_data.get('title'))
        self.assertEqual(response.data['results'][0].get('content'),
                         post_data.get('content'))

    def test_get_call_to_invalid_post_returns_404(self):
        response = self.client.get(
            reverse(self.details_url, args=(9999, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_pagination_returns_correct_number_of_results(self):
        posts = 12
        self.send_post_data_in_batch(self.client, posts=posts)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), posts)
        self.assertIsNotNone(response.data.get('next'))

    def test_get_call_does_not_show_hidden_updated_datetime_field(self):
        post_data = self.get_post_data()
        response = self.send_post_data(self.client, post_data)
        pk = response.data.get('id')
        response = self.client.get(reverse(self.details_url, args=(pk,)))
        self.assertIsNotNone(response.data.get('created_datetime'))
        self.assertIsNone(response.data.get('updated_datetime'))


class PostApiPOSTTest(APITestCase, PostMixin):
    def test_valid_api_post_call_returns_status_code_201(self):
        post_data = self.get_post_data()
        response = self.send_post_data(self.client, post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @parameterized.expand([
        ('username',),
        ('title',),
        ('content',),
    ])
    def test_missing_fields_return_status_code_400(self, field_name):
        post_data = self.get_post_data()
        del post_data[field_name]
        response = self.send_post_data(self.client, post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostApiPATCHTest(APITestCase, PostMixin):
    def test_patch_call_to_valid_post_updates_post_correctly(self):
        response = self.send_post_data(self.client, self.get_post_data())
        pk = response.data.get('id')
        new_title = 'This is a new title'
        new_content = 'New Content' * 30
        response = self.client.patch(
            reverse(self.details_url, args=(pk, )),
            {'title': new_title, 'content': new_content})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), new_title)
        self.assertEqual(response.data.get('content'), new_content)

    def test_patch_call_to_invalid_post_returns_400(self):
        response = self.client.patch(
            reverse(self.details_url, args=(9999,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_cannot_be_changed_by_patch_call(self):
        response = self.send_post_data(self.client, self.get_post_data())
        pk = response.data.get('id')
        username1 = response.data.get('username')
        username2 = username1 + 'XXXXXXXXXXXX'
        response = self.client.patch(
            reverse(self.details_url, args=(pk,)),
            {'username': username2})
        self.assertEqual(response.data.get('username'), username1)

    def test_empty_patch_json_returns_status_code_400(self):
        response = self.send_post_data(self.client, self.get_post_data())
        pk = response.data.get('id')
        response = self.client.patch(reverse(self.details_url, args=(pk,)), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostApiDELTest(APITestCase, PostMixin):
    def test_delete_call_to_invalid_post_returns_404(self):
        response = self.client.delete(reverse(self.details_url, args=(9999,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_call_to_valid_post_returns_204(self):
        response = self.send_post_data(self.client, self.get_post_data())
        pk = response.data.get('id')
        response = self.client.delete(reverse(self.details_url, args=(pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_pagination_after_delete_call_is_correct(self):
        self.send_post_data_in_batch(self.client, posts=11)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 11)
        self.assertIsNotNone(response.data.get('next'))
        pk = response.data.get('results')[0].get('id')
        self.client.delete(reverse(self.details_url, args=(pk,)))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 10)
        self.assertIsNone(response.data.get('next'))
