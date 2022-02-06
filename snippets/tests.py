import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

class SnippetViewTest(APITestCase):
    def setUp(self):
        Snippet.objects.create(code='foo = "bar"\n')
        Snippet.objects.create(code='print("hello, world")\n')

    def test_snippets_list_read(self):
        response = self.client.get(reverse('snippets:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(Snippet.objects.count(), 2)
              
    def test_snippets_detail_create(self):
        response = self.client.post(reverse('snippets:list'), {'code': 'test detail creation'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        snippet = response.content
        response = self.client.get(reverse('snippets:detail', args=[json.loads(snippet)['id']]))
        self.assertEqual(snippet, response.content)
        
    def test_snippets_detail_put(self):
        snippet = Snippet.objects.create(code='test detail modify')
        
        url = reverse('snippets:detail', args=[snippet.id])
        response = self.client.put(url, {'code': 'SELECT * FROM db;', 'language': 'sql'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        snippet = Snippet.objects.get(id=snippet.id)
        self.assertEqual(snippet.language, 'sql')
        
    def tearDown(self):
        Snippet.objects.all().delete()
        return super().tearDown()