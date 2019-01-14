from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # author comes from this package.
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # pass in now function
    date_posted = models.DateTimeField(default=timezone.now)   # auto_now --> set time to current time auto_now_add : will keep date
    author = models.ForeignKey(User, on_delete=models.CASCADE)    # on_delete --> what happens if user is deleted; delete post too

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})   # name of route, with key of spec. route