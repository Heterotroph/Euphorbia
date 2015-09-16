from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html')

def register_advertizer(request):
    return render_to_response('register_advertizer.html')

def register_publisher(request):
    if request.method == 'GET':
        return render_to_response('register_publisher.html')
    elif request.method == 'POST':
        return render_to_response('base.html')
