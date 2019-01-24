from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   # add to classes, far left, same as @login_required
from django.contrib.auth.models import User
from django.views.generic import (
     ListView,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView
)
from .models import Post    # import Post class created for data


class PostListView(ListView):
    # model to query
    model = Post
    # set new template
    template_name = 'blog/home.html'
    # set variable name (originally object_list)
    context_object_name = 'posts'
    # set ordering
    ordering = ['-date_posted']

    paginate_by = 5


class PostDetailView(DetailView):
    # model to query
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # override form_valid method

    def form_valid(self, form):
        # specifies author of form being current user (before form is submitted)
        form.instance.author = self.request.user
        # now we can validate form, running on parent class (done anyways)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False


"""
Similar to detail view, need user to be logged in and
user to be author of post
Success attribute sends url to home page
"""


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

"""
Personal Profile view
"""


class UserPostListView(ListView):
    # model to query
    model = Post
    # set new template
    template_name = 'blog/user_posts.html'
    # set variable name (originally object_list)
    context_object_name = 'posts'
    # set ordering

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))    # kwargs is query parameters, if user exists in query
        return Post.objects.filter(author=user).order_by('-date_posted')


def home(request):
    context = {
        'posts': Post.objects.all()     # make sure keys/values same in dummy dictionary as in Post query
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')