from django.urls import path

from blog.models import Post
from . import views
from .views import PostListView, PostDetailView, PostUpdateView, PostCreateView, PostDeleteView, UserPostListView, PostVoteUpdateView, BestPostView, CreateCommentView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('bestblogs/', BestPostView.as_view(), name='best-blogs'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name='post-comment'),
    path('post/<int:pk>/vote/<int:vt>/', PostVoteUpdateView.as_view(), name='post-vote'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
]