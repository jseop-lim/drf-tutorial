import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('user1', '1234')
        self.client.force_authenticate(self.user)
        Snippet.objects.create(code='foo = "bar"\n', owner=self.user)
        Snippet.objects.create(code='print("hello, world")\n', owner=self.user)


    def test_snippet_list_read(self):
        """
        READ Snippet List
        """    
        response = self.client.get(reverse('snippet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # HyperlinkedIdentityField는 request를 context로 전달해 주어야 함
        _request = self.factory.get(reverse('snippet-list'))
        
        serializer = SnippetSerializer(Snippet.objects.all(), many=True, context={'request': _request})
        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(Snippet.objects.count(), 2)
    
    
    def test_snippet_detail_read(self):
        """
        작성자는 Read/Write 권한, 작성자 아니거나 로그인 상태 아니면 Read Only
        """
        snippet_id = self.user.snippets.last().id
        
        # 작성자 읽기, 수정
        response = self.client.get(reverse('snippet-detail', args=[snippet_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('snippet-detail', args=[snippet_id]), {'code': 'changed_owner'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.get(pk=snippet_id).code, 'changed_owner')
        self.client.logout()
        
        # 비로그인 작성
        response = self.client.post(reverse('snippet-list'), {'code': 'user2_created'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Snippet.objects.count(), 3)
        
        # 비로그인 읽기, 수정
        response = self.client.get(reverse('snippet-detail', args=[snippet_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('snippet-detail', args=[snippet_id]), {'code': 'changed_anonymous'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Snippet.objects.get(pk=snippet_id).code, 'changed_owner')
        
        # 다른 사용자 작성
        user2 = User.objects.create_user('user2', '5678')
        self.client.force_authenticate(user2)
        response = self.client.post(reverse('snippet-list'), {'code': 'user2_created'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 3)
        
        # 다른 사용자 수정 (권한 X)
        response = self.client.get(reverse('snippet-detail', args=[snippet_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('snippet-detail', args=[snippet_id]), {'code': 'changed_other_user'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Snippet.objects.get(pk=snippet_id).code, 'changed_owner')

        
              
    def test_snippet_detail_create(self):
        """
        CREATE/READ 새로 Snippet 하나 생성하고 읽기
        """
        response = self.client.post(reverse('snippet-list'), {'code': 'test detail creation'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        snippet = response.content
        response = self.client.get(reverse('snippet-detail', args=[json.loads(snippet)['id']]))
        self.assertEqual(snippet, response.content)
        
        
    def test_snippet_detail_put(self):
        """
        PUT Snippet 하나 수정하고 바뀐 내용과 일치 여부 확인
        """
        snippet = Snippet.objects.create(code='test detail modify', owner=self.user)
      
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.put(url, {'code': 'SELECT * FROM db;', 'language': 'sql'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        snippet = Snippet.objects.get(id=snippet.id)
        self.assertEqual(snippet.language, 'sql')
        
        
    def tearDown(self):
        Snippet.objects.all().delete()
        return super().tearDown()
    
    
class UserViewTest(APITestCase):
    def test_user_create(self):
        """
        로그인
        """
        response = self.client.post(reverse('user-create'), {'username': 'test_user', 'password': '1234'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='test_user')
        
        self.assertTrue(self.client.login(username='test_user', password='1234'))
        response = self.client.get(reverse('user-detail', args=[user.id]))
        self.assertContains(response, user)