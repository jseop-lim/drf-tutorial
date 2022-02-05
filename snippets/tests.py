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

    def test_snippets_list(self):
        response = self.client.get(reverse('snippets:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        self.assertEqual(json.loads(response.content), serializer.data)
        
    def test_snippets_detail(self):
        response = self.client.get(reverse('snippets:detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = SnippetSerializer(Snippet.objects.get(pk=2))
        self.assertEqual(json.loads(response.content), serializer.data)