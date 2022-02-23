from operator import attrgetter
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from django.views import generic
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.utils import timezone

import requests
from requests.exceptions import ConnectionError

from .models import BlogPost
from .forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account

BLOG_POST_PER_PAGE = 4

# Create your views here.
def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
        context['success_message'] = "Post created!"
    
    context['form'] = form

    return render(request, 'blog/create_blog.html', context)

def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail.html', context)

def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Post updated!"
            blog_post = obj
    
    form = UpdateBlogPostForm(initial= {
        'title': blog_post.title,
        'body': blog_post.body,
        'image': blog_post.image,
    })

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)

def home_blog_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # blog_posts = BlogPost.objects.order_by('-date_published')
    blog_posts = sorted(search_blog_view(query), key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POST_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts
    context['title'] = 'HomeBlog'

    return render(request, 'blog/home_blog.html', context)

def search_blog_view(query=None):
    queryset = []
    queries = query.split(" ") #halo dunia baru = [halo, dunia, baru]
    for q in queries:
        blog_posts = BlogPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in blog_posts:
            queryset.append(post)

    return list(set(queryset))

def index(request):
    context = {}
    try:
        response = requests.get('http://127.0.0.1:7000/blogapi/').json()
        context = {'response':response}
    except ConnectionError as e:
        print(e)
        
    return render(request, 'blog/index.html', context)

# class IndexView(generic.ListView):
#     template_name = 'blog/index.html'

#     def get_queryset(self):
#         return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

# class DetailView(generic.DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
