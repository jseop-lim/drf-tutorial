from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from snippets.serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers


@api_view(['GET'])
def api_root(request, format=None):
    """
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    """ [root view]
    List all snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 사용자 권한에 따라 POST 요청 허용
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    
    # POST 요청 시에 호출되며, serializer로 쓰기가 불가능하므로 인스턴스에 직접 저장
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """ [instance view]
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 사용자 권한에 따라 PUT, DELETE 요청 허용
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    

class SnippetHighlight(generics.GenericAPIView):
    """ [property view]
    snippet의 highlighted 속성을 HTML 형식으로 반환
    """
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()  # TODO 왜 pk 전달 안해도 괜찮?
        return Response(snippet.highlighted)
    

class UserList(generics.ListAPIView):
    # ListAPIView는 여러 인스턴스에 대한 GET 요청만 허용 (READ ONLY)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # RetrieveAPIView는 단일 인스턴스에 대한 GET 요청만 허용 (READ ONLY)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer