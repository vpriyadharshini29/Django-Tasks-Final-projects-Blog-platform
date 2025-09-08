from django import forms
from .models import Comment, Post, Subscriber

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search blogs…", "class": "w-full"})
    )
    category = forms.CharField(required=False, widget=forms.HiddenInput())

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your comment..."})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "categories", "tags"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your blog content here…"}),
        }

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"})
        }
