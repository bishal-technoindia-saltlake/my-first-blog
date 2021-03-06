from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
#from .forms import UserForm
from .forms import SignupForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm()    
    return render(request,'blog/post_edit.html',{'form':form})  

@login_required
def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user 
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm(instance=post)    
    return render(request,'blog/post_edit.html',{'form':form}) 

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            #new_user = User.objects.create_user(**form.cleaned_data)
            #login(request,new_user)
            #return redirect('/')
            user=form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')    
    else:
        form=SignupForm()
    return render(request,'blog/signup.html',{'form':form})    