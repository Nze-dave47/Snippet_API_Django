from django.db.models import Q
from rest_framework import filters, permissions, viewsets
from django.db import models

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'language']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Snippet.objects.filter(models.Q(is_private=False) | models.Q(owner=user))
        return Snippet.objects.filter(is_private=False)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
