from django.urls import path
from . import views
from .models import BlogPost

app_name = 'blog'
urlpatterns = [
    path('', views.home_blog_view, name='index'),
    path('create/', views.create_blog_view, name='create'),
    path('<slug>/', views.detail_blog_view, name='detail'),
    path('<slug>/edit', views.edit_blog_view, name='edit'),
    # path('', views.IndexView.as_view(), name='index'),
    # path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
]