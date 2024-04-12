from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm,BlogForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from wagtail.models import Page
from django.utils.text import slugify
from .models import PostPage
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            auth_login(request, new_user)
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')


def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            listings_page = Page.objects.get(title='Listings')  
            post_page = form.save(commit=False)
            post_page.author = request.user.username
            original_slug = slugify(post_page.title)
            unique_slug = original_slug
            num = 1
            while Page.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1
            post_page.slug = unique_slug
            categories = form.cleaned_data.get('categories')
            tags = form.cleaned_data.get('tags')
            for category in categories:
                post_page.categories.create(blog_category=category)
            for tag in tags:
                post_page.tags.add(tag)
            listings_page.add_child(instance=post_page)
            listings_page.save()
            return redirect('/', slug=post_page.slug) 
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})


def delete_blog(request, year, month, day, slug):
    post_page = get_object_or_404(PostPage, slug=slug)
    if request.user.is_authenticated and (request.user.is_superuser or post_page.author == request.user.username):
        if request.method == 'POST':
            post_page.delete()
            return redirect('/')
        return render(request, 'blog/delete_blog.html', {'post_page': post_page})
    else:
        return HttpResponseForbidden()
    

def edit_blog(request, year, month, day, slug):
    post_page = get_object_or_404(PostPage, slug=slug)
    
    if request.user.is_authenticated and (request.user.is_superuser or post_page.author == request.user.username):
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=post_page)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = BlogForm(instance=post_page)
        
        return render(request, 'blog/edit_blog.html', {'form': form, 'post_page': post_page})
    else:
        return HttpResponseForbidden()