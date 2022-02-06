from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    """ [root view]
    List all snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """ [instance view]
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer