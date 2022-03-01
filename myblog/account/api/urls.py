from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register', views.registration_view, name='register'),
    path('login', views.ObtainAuthTokenView.as_view(), name='login'),
    path('properties', views.account_properties_view, name='properties'),
    path('properties/update', views.update_account_view, name='update'),
]