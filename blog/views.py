from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request, 'blog/index.html', context)

class PostListView(ListView):
    model= Post
    template_name= 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']

class PostDetailView(DetailView):
    model= Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model= Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model= Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False




def about(request):
    return render(request, 'blog/about.html', {'title':'about'})


def sidebar_view(request):
    latest_post = Post.objects.latest('pub_date')  # Fetch the latest post based on the publication date
    return render(request, 'blog/sidebar.html', {'latest_post': latest_post})