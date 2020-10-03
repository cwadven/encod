from django.db import models
from django.conf import settings

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Board(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_total', blank=True)
    ended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    

class VoteBoard(TimeStampedModel):
    boardid = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=100)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_user', blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.title

    def voter_count(self):
        return self.voter.count()