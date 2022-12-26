from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
# Create your views here.
# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# About 
def about(request):
    return render(request, 'blog/about.html')

# Contact 
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard 
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup 
def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, "Congrats!! You have become an Author.")
                user = form.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)
                # un = form.cleaned_data['username']
                # fn= form.cleaned_data['first_name']
                # ln= form.cleaned_data['last_name']
                # en= form.cleaned_data['email']
                # p1= form.cleaned_data['password1']
                # p2= form.cleaned_data['password2']
                # reg = User(username=un, first_name=fn, last_name=ln, email=en, password1=p1, password2=p2)
                # messages.success(request, "Congrats!! YOu have become an Author.")
                # reg.save()
        else:        
            form = SignUpForm()
        return render(request, 'blog/signup.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Login 
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logeed in Successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
    else:
        return HttpResponseRedirect('/dashboard/')
    return render(request, 'blog/login.html', {'form':form})

# Add New Post 
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                messages.success(request, 'Post Added Successfully!!')
        else:
            fm = PostForm()
        return render(request, 'blog/addpost.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')





# Update Post 
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Edited Successfully!!')
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
    
    
    
# Delete Post 
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')