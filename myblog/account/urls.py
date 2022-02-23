from unicodedata import name
from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.account_page, name='profile_page'),
    path('must_authenticate/', views.must_authenticate_view, name='must_authenticate'),
    # path('register1/', views.register_page1, name='register1'),
]
    