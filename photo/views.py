from django.shortcuts import render
from .models import VideoPost, CommentPost, UserHistory
from .forms import VideoPostForm, CommentPostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
import ast

# Account dashboard: allow user to upload videos and view their previously uploaded videos
@login_required
def photos(request):
    context = {'photos': VideoPost.objects.all()}
    if request.method == 'POST':
        form = VideoPostForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
        context['form'] = form
    return render(request, 'photo/photos.html', context)

# Render the explore page, or home page, by displaying all uploaded videos as well as the user's history
def explore(request):
    context = {'photos': VideoPost.objects.all(), 'history': '[]'}
    if request.user.is_authenticated:
        histories = UserHistory.objects.filter(owner=request.user)
        if not histories:
            history = UserHistory.objects.create(owner=request.user, history="[]")
            context['history'] = history.history
        else:
            history = histories[0]
            context['history'] = history.history
    int_arr = ast.literal_eval(context['history'])
    context['history'] = int_arr
    return render(request, 'photo/explore.html', context);

# Render the watch page for the video id and add the video to the front of the user's history
def watch(request, video_id=None):
    videos = VideoPost.objects.filter(id=video_id)
    comments = CommentPost.objects.filter(video_id=video_id)
    if not videos:
        return HttpResponseNotFound('<h1>Video not found!</h1>')
    video = videos[0]

    context = {'video': video, 'comments': comments, 'video_id': video.id, 'history': []}

    if request.user.is_authenticated:
        # Get the history associated with the user who sent the request
        histories = UserHistory.objects.filter(owner=request.user)

        # If no history for this user exists, create an empty one
        if not histories:
            history = UserHistory.objects.create(owner=request.user, history="[]")
        else:
            history = histories[0]
        int_arr = ast.literal_eval(history.history)

        # Check if the video is already in the user's history– if it is, remove it
        if video.id in int_arr:
            int_arr.remove(video.id)

        # Add the video to the front of the users history and convert to a string value to save in the database
        int_arr.insert(0, video.id)
        str_arr = ('[' + ', '.join(str(i) for i in int_arr) + ']')
        history.history = str_arr
        history.save()

        context['history'] = int_arr

    return render(request, 'photo/watch.html', context)

# Create a new comment and save it to the database
def comment(request):
    context = {}
    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.content = request.POST.get('content')
            inst.video_id = request.POST.get('video')
            inst.time = request.POST.get('time')
            inst.score = request.POST.get('score')
            inst.save()

    # Empty response because comment updating happens in the background
    return HttpResponse('')

# Upvote or downvote a comment by changing it's score by +1 or -1
def vote(request):
    context = {}
    if request.method == 'POST':
        comments = CommentPost.objects.filter(id=request.POST.get('id'))
        comment = comments[0]
        comment.score += int(request.POST.get('change'))
        comment.save()

    # Empty response because comment updating happens in the background
    return HttpResponse('')

# Return all comments and users in a JSON object
def getcomments(request):
    eventList = CommentPost.objects.filter(video_id=request.GET.get('video_id')).values()
    userList = User.objects.values()
    return JsonResponse({"comments": list(eventList), "users": list(userList)})

# Delete a video entry
def delete(request, video_id):
    videos = VideoPost.objects.filter(id=video_id)
    comments = CommentPost.objects.filter(video_id=video_id)
    if not videos:
        return HttpResponseNotFound('<h1>Video not found!</h1>')
    video = videos[0]
    video.delete()
    for c in comments:
        c.delete()
    return HttpResponseRedirect(reverse('dashboard'))
