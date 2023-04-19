from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
#Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

#About
def about(request):
    return render(request, 'blog/about.html')

#Contact Form
def contact(request):
    return render(request, 'blog/contact.html')

#Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations You have become an Author')
            user = form.save()
            group = Group.objects.get(name='Authors')
            user.groups.add(group)
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form':form})

#Login
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
                    messages.success(request, "Logged in Successfully")
                    return HttpResponseRedirect('/dashboard')
        else:
            form = LoginForm()
        form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    
    
    # Add New Post 
@login_required(login_url='/login/')
def add_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                messages.success(request, "Post Added Successfully")
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()    
        return render(request, 'blog/addpost.html', {'form':form})

    

# Update Post 
    
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
           pi = Post.objects.get(pk=id) 
           form = PostForm(request.POST, instance=pi)
           if form.is_valid():
               form.save()
               messages.success(request, "Post Updated Successfully")
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
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request, 'Congrats Brother You have deleted successfully!!')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
