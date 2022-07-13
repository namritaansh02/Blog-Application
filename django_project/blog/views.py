from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Activity, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class BestPostView(PostListView):
    ordering = ['-votes']

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def post_detail(request, pk):
    post = Post.objects.get(id = pk)
    comments = Comment.objects.filter(post = post).order_by('-votes')
    context = {
        'object' : post,
        'comments' : comments,
    }
    return render(request, 'blog/post_detail.html', context)

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment 
    fields = ['content']

    def form_valid(self, form):
        post = Post.objects.get(id = self.kwargs['pk'])
        form.instance.author = self.request.user 
        form.instance.post = post 
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def post(self, request):
        user = request.user 
        user.profile.credit += 100
        user.save()
        return super().post(request)

    def get(self, request):
        return super().get(request)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostVoteUpdateView(PostDetailView):
    def get(self, request, pk, vt):
        user = request.user
        post = Post.objects.get(id = pk)
        user_post_activity = Activity.objects.filter(user = user, post = post)
        print(user_post_activity)
        if user_post_activity.count()==0:
            if vt==1: 
                activity_tp = 'U'
                post.votes += 1
            if vt==0:
                activity_tp = 'D'
                post.votes -= 1
            post.save() # to update only votes of attribute and not change user
            activity = Activity.objects.create(user = user, activity_type=activity_tp, post = post)
            activity.save()
        if user_post_activity.count()>0:
            prev_activity = user_post_activity.last()
            print(prev_activity.activity_type)
            if vt==1 and prev_activity.activity_type=='D': 
                activity_tp = 'U'
                post.votes += 2
                post.save() # to update only votes of attribute and not change user
                activity = Activity.objects.create(user = user, activity_type=activity_tp, post = post)
                activity.save()
            if vt==0 and prev_activity.activity_type=='U':
                activity_tp = 'D'
                post.votes -= 2
                post.save() # to update only votes of attribute and not change user
                activity = Activity.objects.create(user = user, activity_type=activity_tp, post = post)
                activity.save()
        return redirect('post-detail', pk = pk)

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

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

@login_required
def activity(request):
    activity = Activity.objects.create(user = request.user, activity_type='U', post = request.post)
    activity.save()
    return HttpResponse('Good Morning')