from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def user_login(request):
    """
    Renders the login form.

    Returns:
        HttpResponse: Rendered HTML template for login.
    """
    return render(request, 'authentication/login.html')


def authenticate_user(request):
    """
    Authenticates the user based on POST data.

    If authentication succeeds, logs the user in and redirects to the user profile.
    If authentication fails, redirects back to the login page.

    Returns:
        HttpResponseRedirect: Redirects to either login or user profile page.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('user_auth:show_user'))
    
    return HttpResponseRedirect(reverse('user_auth:login'))


def show_user(request):
    """
    Renders the user profile page.

    Returns:
        HttpResponse: Rendered HTML template for user profile.
    """
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "password": request.user.password  # Note: Avoid displaying passwords in templates for security reasons.
    })
