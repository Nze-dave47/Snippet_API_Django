from django.urls import include, path
from rest_framework import routers

from .views import SnippetViewSet

router = routers.DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')

urlpatterns = [
    path('', include(router.urls)),
]