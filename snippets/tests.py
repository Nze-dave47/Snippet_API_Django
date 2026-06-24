from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Snippet


class SnippetAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_a = User.objects.create_user(username='usera', password='passA')
        self.user_b = User.objects.create_user(username='userb', password='passB')

        self.private_snippet = Snippet.objects.create(
            title='User A Private',
            content='print("secret")',
            language='python',
            is_private=True,
            owner=self.user_a,
        )

        self.public_snippet = Snippet.objects.create(
            title='Shared Public',
            content='print("shared")',
            language='python',
            is_private=False,
            owner=self.user_b,
        )

        self.list_url = reverse('snippet-list')
        self.detail_url = reverse('snippet-detail', args=[self.private_snippet.pk])

    def test_owner_can_manage_private_snippet(self):
        self.client.login(username='usera', password='passA')

        create_response = self.client.post(
            self.list_url,
            {
                'title': 'Owned Private',
                'content': 'print("owned")',
                'language': 'python',
                'is_private': True,
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        owned_id = create_response.data['id']
        self.assertEqual(create_response.data['owner'], self.user_a.id)

        detail_url = reverse('snippet-detail', args=[owned_id])
        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data['title'], 'Owned Private')
        self.assertTrue(retrieve_response.data['is_private'])

        update_response = self.client.patch(
            detail_url,
            {'title': 'Updated Owned Private'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], 'Updated Owned Private')

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Snippet.objects.filter(pk=owned_id).exists())

    def test_other_user_cannot_read_private_snippet(self):
        self.client.login(username='userb', password='passB')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_other_user_cannot_mutate_private_snippet(self):
        self.client.login(username='userb', password='passB')

        put_response = self.client.put(
            self.detail_url,
            {
                'title': 'Hijacked',
                'content': 'print("hijacked")',
                'language': 'python',
                'is_private': True,
            },
            format='json',
        )
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)

        delete_response = self.client.delete(self.detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_filters_out_foreign_private_snippets(self):
        self.client.login(username='userb', password='passB')
        response = self.client.get(self.list_url, {'search': 'shared'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [item['title'] for item in response.data]
        self.assertIn('Shared Public', titles)
        self.assertNotIn('User A Private', titles)
