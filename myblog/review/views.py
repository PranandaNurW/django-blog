from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature
from account.models import Account

# Create your views here.
def index(request):
    features = Feature.objects.all()
    accounts = Account.objects.all()
    context = {
        'features':features
    }

    return render(request, 'review/index.html', context)

