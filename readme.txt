Group Members
Name: Michael Hollingshead
ID: 260729276

http://127.0.0.1:8000

Django version: 3.0.5

Python version: 3.8
(Had to run everything with 'python3.8 manage.py runserver' or 'python3.8 manage.py test', not sure if the '.8' is required for whoever will be running the app but it was required for me)

websocket runs with channels/redis as shown in class/examples

static root should be movment/staticfiles/static
media root should be movment/staticfiles/media
(just in case, these should already be correct in settings)

Notes:
– For some reason no video files would load in Safari, but loaded fine in Chrome and Firefox
– Sometimes the custom video controls init function is called before the comments are loaded to the page by django. Because the init function depends on the comment area, this could cause the progress bar/video time to be a bit glitchy. If correct video time (0:00/x:xx) or comment ticks (if there are comments on the video) aren't displaying, try reloading the page. (I'm sorry about this, I couldn't find a workaround. It seems to have to do with the size of the video, doesn't seem to be a problem with smaller ones [sub 20 seconds])
– I removed the larger video files shown in the demo and replaced them with one short video for demo/testing purposes.
