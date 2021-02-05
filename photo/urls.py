from django.contrib import admin
from django.urls import path, include
from .views import *
from account import *

urlpatterns = [
    path('dashboard', photos, name='dashboard'),
    path('', explore, name='explore'),
    path('<int:video_id>/watch', watch, name='watch'),
    path('comment', comment, name='comment'),
    path('vote', vote, name='vote'),
    path('getcomments', getcomments, name='getcomments'),
    path('delete?<int:video_id>', delete, name='delete')
]
