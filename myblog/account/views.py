import email
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from blog.models import BlogPost
from .forms import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm

# Create your views here.
# def login_page(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']

#         user = authenticate(email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('review:index')
#         else:
#             messages.info(request, 'Credentials Invalid')
#             return redirect('account:login_page')
#     else:
#         return render(request, 'account/login.html')

# def register_page(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Already Used')
#                 return HttpResponseRedirect(reverse('account:register_page'))
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Already Used')
#                 return HttpResponseRedirect(reverse('account:register_page'))
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()
#                 messages.success(request, 'Register Succeed')
#                 return HttpResponseRedirect(reverse('account:login_page'))
#         else:
#             messages.info(request, 'Password does not match')
#             return HttpResponseRedirect(reverse('account:register_page'))
#     else:
#         return render(request, 'account/register.html')

def register_page(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register Succeed')
            return redirect('account:login_page')
        else:
            context['registration_form'] = form
    else: #get request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register1.html', context)

def login_page(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('review:index')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('review:index')
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login1.html', context)

def logout_page(request):
    logout(request)
    return redirect('account:login_page')

def account_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial ={
                'email': request.POST['email'],
                'username': request.POST['username'],
            }
            form.save()

            context['success_message'] = "Updated!"
    else:
        form = AccountUpdateForm(initial={
            'email': request.user.email,
            'username': request.user.username,
        })
    
    context['account_form'] = form

    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts
    
    return render(request, 'account/account1.html', context)

def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
    
