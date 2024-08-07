from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def signup(request):
    # Your signup view logic here
    return render(request, 'registration/signup.html')

def polls_view(request):
    # Your view logic goes here
    return render(request, 'polls.html')