from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm, PostForm,CommentForm
from django.db import transaction
from .models import Followers
from . models import Following, Post, Comments
#from .models import Profile
#from .models import UserProfile

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request,'core/signup.html', {'form': form})        



def index(request):
    return render(request, 'core/home.html')

@login_required
def temp(request):
    return redirect('core:profile', username= request.user.username )


@login_required
def ProfileView(request, username):
    if username == request.user.username:
        user  = User.objects.get(username=username)
        following= request.user.profile.following_set.all()
        feeds  = Post.objects.all()
        comments= Comments.objects.all()
        return render(request, 'core/profile.html',{'user' : user, 'following': following, 'feeds':feeds, 'comments':comments} )

    else :
        user  = User.objects.get(username=username)
        feeds  = Post.objects.all()
        return render(request, 'core/other_profile.html',{'user' : user, 'feeds':feeds} )






@login_required
#@transaction.atomic
def update_profile(request, username):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('core:profile', username=username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })   


@login_required
def follow(request, username):
    request.user.profile.following_set.create(following_name= username)
    return redirect('core:profile', username=username)


@login_required
def create_post(request,username):
    if request.method=='POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            
            a= User.objects.get(username=username)
            post.profile=a.profile
            # post.heading = post_form.heading
            # post.content = post_form.content
            #post_form.heading = request.POST['heading']
            #post_form.content = request.POST['content']
            post.save()
            #post_form.save()
            
            #messages.success(request, 'Your profile was successfully updated!')
            return redirect('core:profile', username=username)
    else:
        post_form=PostForm()
    return render(request,'core/post.html',{'post_form':post_form})            


@login_required
def create_comment(request,username,post_id):
    post=Post.objects.get(pk=post_id)
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            post=Post.objects.get(id=post_id)
            a=Post.objects.get(id=post_id)
            comment.post=a
            comment.commenter=username
            # post.heading = post_form.heading
            # post.content = post_form.content
            #post_form.heading = request.POST['heading']
            #post_form.content = request.POST['content']
            comment.save()
            #post_form.save()
            
            #messages.success(request, 'Your profile was successfully updated!')
            return redirect('core:profile', username=username)
    else:
        comment_form=CommentForm()
        #post=Post.objects.get(pk=post_id)
    return render(request,'core/comment.html',{'post':post, 'comment_form':comment_form}) 


















# class UserProfileCreate(generic.edit.CreateView):
#      model = UserProfile    
#      fields = ['FirstName', 'LastName', 'email', 'college']
#      success_url = reverse_lazy('core:home')

