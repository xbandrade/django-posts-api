from django.db import models
from django.forms import ValidationError


class Post(models.Model):
    username = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        exceeded_text = ' exceeds maximum length of '
        if len(self.username) > 255:
            raise ValidationError(
                {'username': 'Username' + exceeded_text + '255 characters.'})
        if len(self.title) > 255:
            raise ValidationError(
                {'title': 'Title' + exceeded_text + '255 characters.'})
