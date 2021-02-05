from django.test import TestCase
from django.contrib.auth.models import User
from .models import VideoPost, CommentPost, UserHistory
from .forms import VideoPostForm, CommentPostForm
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your tests here.
class TestVideos(TestCase):
    def test_unsuccessful_video_upload(self):
        u = User.objects.create(username="test1", email="test1@mail.com", password="pass123")
        test_video = SimpleUploadedFile(name='test_phone.mov', content=open(os.path.join(BASE_DIR, 'staticfiles/test_files/test_phone.mov'), 'rb').read(), content_type='video/mov')
        data = {'title': 'test_video', 'descrip': 'description', 'owner': u}
        form = VideoPostForm(data=data, files={'video': SimpleUploadedFile(name='test_phone.mov', content=open(os.path.join(BASE_DIR, 'staticfiles/test_files/test_phone.mov'), 'rb').read(), content_type='video/mov')})
        self.assertFalse(form.is_valid())

    def test_successful_video_upload(self):
        u = User.objects.create(username="test2", email="test2@mail.com", password="pass123")
        form = VideoPostForm(data={})
        assert form.is_valid() is False
        data = {'title': 'test_video', 'descrip': 'description', 'owner': u}
        form = VideoPostForm(data=data, files={'video': SimpleUploadedFile(name='test_beach.mp4', content=open(os.path.join(BASE_DIR, 'staticfiles/test_files/test_beach.mp4'), 'rb').read(), content_type='video/mp4')})
        self.assertTrue(form.is_valid())
