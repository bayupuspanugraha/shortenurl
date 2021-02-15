from django.db import models

# Create your models here.


class ShortenURL(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    originalURL = models.TextField()

    def __str__(self):
        return self.originalURL
