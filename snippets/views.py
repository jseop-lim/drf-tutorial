from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

from rest_framework import generics
from rest_framework import permissions

class SnippetList(generics.ListCreateAPIView):
    """ [root view]
    List all snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 사용자 권한에 따라 POST 요청 허용
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # POST 요청 시에 호출되며, serializer로 쓸 수 없으므로 인스턴스에 직접 저장
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """ [instance view]
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 사용자 권한에 따라 PUT, DELETE 요청 허용
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    

class UserList(generics.ListAPIView):
    # ListAPIView는 여러 인스턴스에 대한 GET 요청만 허용 (READ ONLY)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # RetrieveAPIView는 단일 인스턴스에 대한 GET 요청만 허용 (READ ONLY)
    queryset = User.objects.all()
    serializer_class = UserSerializer