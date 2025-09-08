from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    add_comment, CommentUpdateView, CommentDeleteView, SubscribeView
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>/comment/", add_comment, name="comment_add"),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_edit"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
