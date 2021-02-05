from django.forms import ModelForm
from .models import VideoPost
from .models import CommentPost

class VideoPostForm(ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title', 'descrip', 'video']

class CommentPostForm(ModelForm):
    class Meta:
        model = CommentPost
        fields = ['content']
