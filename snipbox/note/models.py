from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Snippet(models.Model):
    title = models.CharField(max_length=120)
    note = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, related_name="snippets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    existence_status = models.BooleanField(default=1)

    def __str__(self):
        return self.title
