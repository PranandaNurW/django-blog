from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('account:index'))
        else:
            messages.info(request, 'Credentials Invalid')
            return HttpResponseRedirect(reverse('account:login_page'))
    else:
        return render(request, 'account/login.html')

def register_page(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return HttpResponseRedirect(reverse('account:register_page'))
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return HttpResponseRedirect(reverse('account:register_page'))
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Register Succeed')
                return HttpResponseRedirect(reverse('account:login_page'))
        else:
            messages.info(request, 'Password does not match')
            return HttpResponseRedirect(reverse('account:register_page'))
    else:
        return render(request, 'account/register.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('account:index'))