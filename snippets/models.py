from django.db import models
from django.contrib.auth.models import User


class Snippet(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=100, blank=True)
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')

    def __str__(self):
        return self.title
