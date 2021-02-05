from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Create your models here.
class VideoPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(['mp4', 'avi', 'mpg'])])
    title = models.CharField(max_length=100)
    descrip = models.CharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    def get_title(self):
        return self.title

class CommentPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.IntegerField()
    content = models.CharField(max_length=250)
    time = models.CharField(max_length=10)
    score = models.IntegerField()

class UserHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.CharField(max_length=10000, blank=True)
