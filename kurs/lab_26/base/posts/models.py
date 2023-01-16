from django.db import models


class Posts(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField()
    likes = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title
