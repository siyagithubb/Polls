"""
URL configuration for mySite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from polls.views import signup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Assuming home view is in polls.views
    path('polls/', include('polls.urls')),  # Include the polls app URLs
    path('user_auth/', include('user_auth.urls')),  # Include the user_auth app URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('polls/', views.polls_view, name='polls'),
    path('signup/', signup, name='signup'),
]




