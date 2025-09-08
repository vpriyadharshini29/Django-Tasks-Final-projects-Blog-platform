from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)

from .models import Post, Comment, Category, Tag, Subscriber
from .forms import SearchForm, CommentForm, PostForm, SubscribeForm

# --------- Auth ----------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("post_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# --------- Posts ----------
class PostListView(ListView):
    model = Post
    paginate_by = 6
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        qs = super().get_queryset().select_related("author").prefetch_related("categories", "tags")
        q = self.request.GET.get("q", "").strip()
        cat_slug = self.request.GET.get("category")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)).distinct()
        if cat_slug:
            qs = qs.filter(categories__slug=cat_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = SearchForm(initial={
            "q": self.request.GET.get("q", ""),
            "category": self.request.GET.get("category", ""),
        })
        ctx["categories"] = Category.objects.all()
        ctx["active_category"] = self.request.GET.get("category", "")
        ctx["subscribe_form"] = SubscribeForm()
        return ctx

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this post.")
        return redirect(self.get_object().get_absolute_url())

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "posts/post_confirm_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)

# --------- Comments ----------
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        cm = form.save(commit=False)
        cm.post = post
        cm.user = request.user
        cm.save()
        messages.success(request, "Comment added.")
    return redirect(post.get_absolute_url())

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        messages.success(self.request, "Comment deleted.")
        return self.object.post.get_absolute_url()

# --------- Subscribe ----------
class SubscribeView(FormView):
    form_class = SubscribeForm
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Subscribed! You'll be notified of new posts.")
        return super().form_valid(form)
