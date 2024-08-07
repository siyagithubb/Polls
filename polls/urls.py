from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
 path('', views.index, name='index'),
 path('<int:question_id>/', views.detail, name='detail'),
 path('<int:question_id>/results/', views.results, name='results'),
 path('<int:question_id>/vote/', views.vote, name='vote'),
 path('signup/', views.signup, name='signup'),
 path('login/', views.MyLoginView.as_view(), name='login'),
 path('register/', views.register, name='register'),
path('logout/', views.logout_view, name='logout'),
]


