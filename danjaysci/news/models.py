import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        'lab_members.LabMember',
        on_delete = models.CASCADE,
    )    
    post_title = models.CharField(
        max_length = 200
    )
    post_text = models.TextField()
    pub_date = models.DateTimeField(
        'date published'
    )

    def __str__(self):
        return self.post_title

    def recently_published(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)
