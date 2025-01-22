from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method=='POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to Log in')
            return redirect('login')
    else:
        form=UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form= UserUpdateForm(request.POST, instance=request.user)
        p_form= ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)

def author_info(request, username):
    # Fetch the user and profile based on the username
    author = get_object_or_404(User, username=username)
    profile=author.profile
    context = {
        'author': author,
        'profile': author.profile,
        'bio': profile.bio,
    }
    return render(request, 'users/author_info.html', context)


def author_posts(request, username):
    author = get_object_or_404(User, username=username)  # Get the user based on username
    posts = Post.objects.filter(author=author)  # Get posts by this author

    context = {
        'author': author,
        'posts': posts
    }
    return render(request, 'blog/author_posts.html', context)